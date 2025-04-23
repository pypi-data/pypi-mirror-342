from __future__ import annotations
from dataclasses import dataclass, field
from typing import cast, Optional

from relationalai.early_access.metamodel import ir, factory as f, helpers, visitor
from relationalai.early_access.metamodel.compiler import Pass, group_tasks
from relationalai.early_access.metamodel.util import OrderedSet, ordered_set


class Flatten(Pass):
    """
    Traverses the model's root to flatten it as much as possible. The result of this pass is
    a Logical root where all nested tasks that represent a rule in Rel are extraced to the
    top level.

    - nested logical with updates becomes a top-level logical (a rule)

    From:
        Logical
            Logical
                lookup1   <- scope is spread
                Logical
                    lookup2
                    derive foo
                Logical
                    lookup3
                    derive bar
    To:
        Logical
            Logical
                lookup1
                lookup2
                derive foo
            Logical
                lookup1
                lookup3
                derive bar

    - nested logical with aggregates becomes a top-level logical (a rule representing an aggregation)

    From:
        Logical
            Logical
                lookup1
                Logical
                    lookup2
                    aggregate1
                Logical
                    lookup3
                    aggregate2
                output
    To:
        Logical
            Logical
                lookup1
                lookup2
                aggregate1
                derive tmp1
            Logical
                lookup1
                lookup3
                aggregate2
                derive tmp2
            Logical
                lookup1
                lookup tmp1
                lookup tmp2
                output

    - a union becomes a top-level logical for each branch, writing into a temporary relation,
    and a lookup from that relation.

    From:
        Logical
            Logical
                Union
                    Logical
                        lookup1
                    Logical
                        lookup2
                output
    To:
        Logical
            Logical
                lookup1
                derive tmp1
            Logical
                lookup2
                derive tmp1
            Logical
                lookup tmp1
                output

    - a match becomes a top-level logical for each branch, each writing into its own temporary
    relation and a lookup from the last relation. The top-level logical for a branch derives
    into the temporary relation negating the previous branch:

    From:
        Logical
            Logical
                Match
                    Logical
                        lookup1
                    Logical
                        lookup2
                output
    To:
        Logical
            Logical
                lookup1
                derive tmp1
            Logical
                Union            <- tmp1() or (not temp1() and lookup2())
                    lookup tmp1
                    Logical
                        Not
                            lookup tmp1
                        lookup2
                        derive tmp2
            Logical
                lookup tmp2
                output
    """

    #--------------------------------------------------
    # Public API
    #--------------------------------------------------
    def rewrite(self, model: ir.Model, cache) -> ir.Model:

        ctx = Flatten.Context()

        # rewrite the root
        root = self.handle(model.root, ctx)

        # the new body contains the extracted top level logicals and maybe the rewritten root
        body = ctx.top_level if root.replacement is None else ctx.top_level + [root.replacement]

        # create the new model, updating relations and root
        return ir.Model(
            model.engines,
            OrderedSet.from_iterable(model.relations).update(ctx.relations).frozen(),
            model.types,
            ir.Logical(model.root.engine, tuple(), tuple(body))
        )


    #--------------------------------------------------
    # Helper Classes
    #--------------------------------------------------

    @dataclass
    class ExtractedBindersInfo():
        """ Information about binders extracted from a logical into a top-level logical. """
        common_reference: ir.Lookup
        binders: OrderedSet[ir.Task]
        exposed_vars: OrderedSet[ir.Var]

    class Frame():
        """ Scope information about the logical being analyzed. """
        def __init__(self, parent: Optional[Flatten.Frame], task: ir.Logical):
            # the parent frame, if any
            self.parent = parent
            # binders in the task
            self.binders: OrderedSet[ir.Task] = ordered_set()
            # variables provided by binders or hoisted by composites
            self.locals: OrderedSet[ir.Var] = ordered_set()
            # from task to the locals it provides
            self.task_bindings: dict[ir.Task, OrderedSet[ir.Var]] = dict()
            # from locals to the tasks that provided them
            self.task_by_var: dict[ir.Var, OrderedSet[ir.Task]] = dict()

            # populate the info above
            self._populate(task)

            # may be set by the analysis
            self.extracted_binders: Optional[Flatten.ExtractedBindersInfo] = None


        def intersection(self, tasks: OrderedSet[ir.Task]) -> OrderedSet[ir.Var]:
            """ Return the intersection of variables needed by all task bindings from these tasks. """
            intersection = OrderedSet.from_iterable(self.task_bindings[tasks.some()])
            for t in tasks:
                for v in intersection:
                    if v not in self.task_bindings[t]:
                        intersection.remove(v)
            return intersection

        def local_binders(self, task: ir.Logical) -> list[ir.Task]:
            """ Get all the binders in this frame that do not use hoisted variables from this task. """
            result = []
            hoisted = helpers.hoisted_vars(task.hoisted)
            for binder in self.binders:
                if all([v not in hoisted for v in self.task_bindings[binder]]):
                    result.append(binder)
            return result

        def _populate(self, task):
            """ Analyze this task to populate the frame. """

            # local cache for collect_vars
            collected_vars: dict[ir.Task, OrderedSet[ir.Var]] = dict()

            # populate locals and binders
            for t in task.body:
                if isinstance(t, helpers.BINDERS):
                    self.binders.add(t)
                    collected_vars[t] = helpers.collect_vars(t)
                    self.locals.update(collected_vars[t])
                elif isinstance(t, helpers.COMPOSITES):
                    self.locals.update(helpers.hoisted_vars(t.hoisted))

            # compute all variables in scope
            scope = ordered_set()
            self._collect_variables_in_scope(scope)

            # populate bindings per task
            for t in task.body:
                if isinstance(t, helpers.BINDERS):
                    for v in collected_vars[t]:
                        self._register(self.task_bindings, t, v)
                elif isinstance(t, helpers.COMPOSITES):
                    # - all vars - hoisted - local (not in outer, not in hoisted)
                    expected = (helpers.collect_vars(t) - helpers.hoisted_vars(t.hoisted)) & scope
                    for v in expected:
                        self._register(self.task_bindings, t, v)

            # populate tasks per var
            for t, vars in self.task_bindings.items():
                for v in vars:
                    self._register(self.task_by_var, v, t)

        def _collect_variables_in_scope(self, scope: OrderedSet[ir.Var]):
            """ Recursively collect locals from parents. """
            if self.parent:
                self.parent._collect_variables_in_scope(scope)
            scope.update(self.locals)

        def _register(self, map, key, val):
            """ Register key -> val in this map, assuming the map holds ordered sets of vals. """
            if key not in map:
                map[key] = ordered_set()
            map[key].add(val)

    @dataclass
    class Context():
        # the logicals that will be at the top level at the end of the rewrite
        top_level: list[ir.Logical] = field(default_factory=list)
        # new relations created during the pass
        relations: list[ir.Relation] = field(default_factory=list)
        # the stack of frames
        frames: list[Flatten.Frame] = field(default_factory=list)

        def peek(self):
            """ Get the last frame or None. """
            if self.frames:
                return self.frames[-1]
            return None

        def compute_scope(self, task: ir.Task) -> OrderedSet[ir.Task]:
            # get the expected vars for this task on the current frame
            frame = self.peek()
            assert frame
            expected_vars = frame.task_bindings.get(task, ordered_set())

            # compute tasks from previous frames that these vars may depend upon
            tasks = ordered_set()
            for frame in self.frames:
                if frame.extracted_binders:
                    tasks.add(frame.extracted_binders.common_reference)

                if expected_vars:
                    dependencies: OrderedSet[ir.Task] = ordered_set()
                    self._compute_dependencies(expected_vars, frame, dependencies)
                    tasks.update(dependencies)
            return tasks

        def _compute_dependencies(self, vars: OrderedSet[ir.Var], frame: Flatten.Frame, dependencies: OrderedSet[ir.Task]):
            # compute dependencies for these vars
            for var in vars:
                # the var has some outer tasks that depend on it
                if var in frame.task_by_var:
                    # if the var is was already in the common extracted logical, no need to bind it again
                    if frame.extracted_binders and var in frame.extracted_binders.exposed_vars:
                        continue
                    # bring all the binders that this variable needs
                    for t in frame.task_by_var[var]:
                        if t in frame.binders and t not in dependencies:
                            dependencies.add(t)
                            if t in frame.task_bindings:
                                self._compute_dependencies(frame.task_bindings[t], frame, dependencies)


    @dataclass
    class HandleResult():
        """ The result of the handle methods. """
        # when a task is handled, the replacement for it, if any; if the task is not changed,
        # this can be the task itself; if the task was extracted as a new logical, for
        # for example, this can be a lookup to the connection relationl; if all sub-tasks
        # became logicals with effects, this can be empty.
        replacement: Optional[ir.Task]

        # True if the task was extracted as its own top-level logical.
        extracted: bool = field(default=False)

    #--------------------------------------------------
    # IR handlers
    #--------------------------------------------------

    def handle(self, task: ir.Task, ctx: Context):
        if isinstance(task, ir.Logical):
            return self.handle_logical(task, ctx)
        elif isinstance(task, ir.Union):
            return self.handle_union(task, ctx)
        elif isinstance(task, ir.Match):
            return self.handle_match(task, ctx)
        else:
            return Flatten.HandleResult(task)

    def handle_logical(self, task: ir.Logical, ctx: Context):

        # create frame to process the children
        frame = Flatten.Frame(ctx.peek(), task)
        ctx.frames.append(frame)

        # process the original body
        groups = group_tasks(task.body, {
            "binders": helpers.BINDERS,
            "composites": helpers.COMPOSITES,
            "effects": helpers.EFFECTS
        })

        # potentially extract common binders and register a reference to it in the current frame
        # note that at this point we are only extracting this common relation if the composites
        # are extractable. But once we implement proper handling of nulls, we may need to extract
        # also if the nested logical is nullable.
        common_reference = None
        if len(groups["binders"]) > 1 and len(groups["composites"]) > 1 and len(self._extractables(groups["composites"])) > 1:
            exposed_vars = frame.intersection(groups["composites"])
            common_connection = self._extract(task, groups["binders"], exposed_vars.list, ctx, "common")
            common_reference = f.lookup(common_connection, exposed_vars.list)
            frame.extracted_binders = Flatten.ExtractedBindersInfo(common_reference, groups["binders"], exposed_vars)

        # recursively handle children, collecting the replacements in the body
        body:OrderedSet[ir.Task] = ordered_set()
        all_composites_extracted = None
        for t in task.body:
            if t in groups["binders"]:
                body.add(t)
            elif t in groups["composites"]:
                x = self.handle(t, ctx)
                if x.replacement is not None:
                    self._extend_body(body, x.replacement)
                all_composites_extracted = x.extracted and (all_composites_extracted is None or all_composites_extracted)
            else:
                body.add(self.handle(t, ctx).replacement)
                if t not in groups["effects"]:
                    all_composites_extracted = False

        # pop the frame used to process the children
        ctx.frames.pop()

        # if the binders where extracted or pushed down when all other nodes are composites, remove them from the body
        if common_reference or (all_composites_extracted and not groups["effects"] and not groups["other"]):
            body = body - frame.local_binders(task)
        # if the binders where extracted but not pushed down, add a reference to the connection
        if common_reference and not all_composites_extracted:
            body.add(common_reference)

        # all children were extracted, drop it
        if not body:
            return Flatten.HandleResult(None)

        # now process the rewritten body
        groups = group_tasks(body.list, {
            "outputs": ir.Output,
            "updates": ir.Update,
            "aggregates": ir.Aggregate,
        })

        # if there are outputs, currently assume it's already at top level, so just return
        # the rewritten body
        if groups["outputs"]:
            return Flatten.HandleResult(ir.Logical(task.engine, task.hoisted, tuple(body)))

        # if there are updates, extract as a new top level rule
        if groups["updates"]:
            # add whatever was in scope at the start of the body
            body = ctx.compute_scope(task) | body
            ctx.top_level.append(ir.Logical(task.engine, task.hoisted, tuple(body)))

            # no need to refer to the extracte logical because it is an update
            return Flatten.HandleResult(None, True)

        if groups["aggregates"]:
            if len(groups["aggregates"]) > 1:
                # stop rewritting as we don't know how to handle this yet
                return Flatten.HandleResult(task)

            # there must be only one
            agg = cast(ir.Aggregate, groups["aggregates"].some())

            # add whatever was in scope at the start of the body
            scoped = ctx.compute_scope(task)
            body = scoped | body

            # extract a new logical for the aggregate, exposing aggregate group-by and results
            frame = ctx.peek()
            exposed_vars = ordered_set()
            exposed_vars.update(list(agg.group) + helpers.aggregate_outputs(agg))
            # make sure aggregation projection variables are not exposed
            for v in agg.projection:
                exposed_vars.remove(v)
            connection = self._extract(agg, body, exposed_vars.list, ctx)

            # return a reference to the connection relation
            reference = f.logical([f.lookup(connection, exposed_vars.list)], self._merge_var_list(exposed_vars.list, task.hoisted))
            return Flatten.HandleResult(reference, True)

        return Flatten.HandleResult(ir.Logical(task.engine, task.hoisted, tuple(body)))


    def handle_match(self, match: ir.Match, ctx: Context):
        # TODO: how to deal with malformed input like this?
        if not match.tasks:
            return Flatten.HandleResult(match)

        body = ctx.compute_scope(match)
        exposed_vars = helpers.collect_vars(*body)
        exposed_vars.update(helpers.hoisted_vars(match.hoisted))
        exposed_vars = exposed_vars.list

        connection = None
        reference = None

        for branch in match.tasks:
            # process the branch
            x = self.handle(branch, ctx)
            assert(x.replacement)

            branch_body: OrderedSet[ir.Task] = OrderedSet.from_iterable(body)
            self._extend_body(branch_body, x.replacement)
            if reference:
                branch_body.add(self._negate(reference, len(match.hoisted)))
                branch_body = OrderedSet.from_iterable([f.union([f.logical(branch_body.list, match.hoisted), reference], match.hoisted)])
            connection = self._extract(branch, branch_body, exposed_vars, ctx, "match")
            reference = f.logical([f.lookup(connection, exposed_vars)], exposed_vars)

        return Flatten.HandleResult(reference, True)


    def handle_union(self, union: ir.Union, ctx: Context):
        # TODO: how to deal with malformed input like this?
        if not union.tasks:
            return Flatten.HandleResult(union)

        body = ctx.compute_scope(union)
        exposed_vars = helpers.collect_vars(*body)
        exposed_vars.update(helpers.hoisted_vars(union.hoisted))
        exposed_vars = exposed_vars.list

        connection = None

        for branch in union.tasks:
            # process the branch
            x = self.handle(branch, ctx)
            assert(x.replacement)

            branch_body: OrderedSet[ir.Task] = OrderedSet.from_iterable(body)
            self._extend_body(branch_body, x.replacement)

            if connection is None:
                # first branch, extract making a connection relation
                connection = self._extract(branch, branch_body, exposed_vars, ctx, "union")
            else:
                # subsequent branch, extract reusing the connection relation
                # add derivation to the extracted body
                branch_body.add(f.derive(connection, exposed_vars))

                # extract the body
                ctx.top_level.append(ir.Logical(union.engine, tuple(), tuple(branch_body)))

        # return a reference to the connection
        assert(connection)
        reference = f.logical([f.lookup(connection, exposed_vars)], exposed_vars)
        return Flatten.HandleResult(reference, True)

    #--------------------------------------------------
    # Helpers
    #--------------------------------------------------

    def _negate(self, reference: ir.Logical, values: int):
        """
        Return a negation of this reference, where the last `values` arguments are to
        be replaced by wildcards (i.e. len(reference.args) - values are keys so they need
        to be bound in the Not.)
        """
        lookup = cast(ir.Lookup, reference.body[0])
        args = []
        i = 0
        last = len(lookup.args) - values
        for arg in lookup.args:
            args.append(f.wild()) if i >= last else args.append(arg)
            i += 1

        return ir.Not(reference.engine, f.lookup(lookup.relation, args))

    def _extractable(self, t: ir.Task):
        """
        Whether this task is a Logical that will be extracted as a top level by this
        pass, because it has an aggregation, effects, match, union, etc.
        """
        return isinstance(t, ir.Logical) and len(visitor.collect_by_type((ir.Update, ir.Aggregate, ir.Match, ir.Union), t)) > 0

    def _extractables(self, composites: OrderedSet[ir.Task]):
        """ Filter the set of composites, keeping only the extractable ones. """
        return list(filter(self._extractable,composites))

    def _extract(self, task: ir.Task, body: OrderedSet[ir.Task], exposed_vars: list[ir.Var], ctx: Context, prefix: Optional[str]=None) -> ir.Relation:
        """
        Extract into this context a new top level Logical that contains this body plus a
        derive task into a new temporary relation, which is also registered with the ctx.
        The exposed_vars determine the arguments of this temporary relation. The prefix
        can be used to customize the name of the relation, which defaults to the task kind.

        Return the temporary relation created for the extraction.
        """

        # TODO: review variable rewrites, i.e. when we extract a new logical, we should remap variables
        p = prefix if prefix else task.kind

        # new relation to derive the aggregation into
        connection = f.relation(f"_{p}_{task.id}", [f.field(v.name, v.type) for v in exposed_vars])
        ctx.relations.append(connection)

        # add derivation to the extracted body
        body.add(f.derive(connection, exposed_vars))

        # extract the body
        ctx.top_level.append(ir.Logical(task.engine, tuple(), tuple(body)))

        # return a reference to the connection relation
        return connection


    def _merge_var_list(self, vars: list[ir.Var], hoisted: tuple[ir.VarOrDefault, ...]) -> list[ir.VarOrDefault]:
        """ Merge vars and hoisted, making sure that hoisted vars have precedence since they may have defaults. """
        r = []
        hoisted_vars = helpers.hoisted_vars(hoisted)
        for v in vars:
            if v not in hoisted_vars:
                r.append(v)
        r.extend(hoisted)
        return r

    def _extend_body(self, body: OrderedSet[ir.Task], extra: ir.Task):
        """ Add the extra task to the body, but if the extra is a simple logical, just
        inline its subtasks. """
        if isinstance(extra, ir.Logical):
            if extra.hoisted:
                # hoists, remove things that are already in the body to avoid duplicates
                logical_body = []
                for t in extra.body:
                    if t not in body:
                        logical_body.append(t)
                if len(logical_body) == len(extra.body):
                    # no duplicates
                    body.add(extra)
                else:
                    # some duplicate, remove them
                    body.add(ir.Logical(
                        extra.engine,
                        extra.hoisted,
                        tuple(logical_body)
                    ))
            else:
                # no hoists, just inline
                body.update(extra.body)
        else:
            body.add(extra)
