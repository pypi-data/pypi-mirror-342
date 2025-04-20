from __future__ import annotations
from dataclasses import dataclass, field
from typing import cast, Optional

from relationalai.early_access.metamodel import ir, factory as f, helpers
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

    class Frame():
        """ The scope of a Logical. """
        binders = (ir.Lookup, ir.Not, ir.Exists, ir.ForAll)
        effects = (ir.Update, ir.Output)

        def __init__(self, task: ir.Logical):
            # the set of task a logical adds to scope. These are tasks in the body of a logical
            # that bind variables, so they must be part the conjunction in inner scopes.
            self.scope: list[ir.Task] = []

            # TODO: we are conservatively pushing these nodes down, but we could be more
            # selective if we did a dataflow analysis

            for t in task.body:
                if isinstance(t, Flatten.Frame.binders):
                    self.scope.append(t)

        def updated_scope_binding(self, all_scope_was_bound: Optional[bool], t: ir.Task, scope_was_bound: bool):
            """ Determine the new state of all_scope_was_bound once task t was handled and returned this scope_was_bound. """
            # for nested logicals, update based on what was returned for the logical
            if isinstance(t, ir.Logical):
                return scope_was_bound and (all_scope_was_bound is None or all_scope_was_bound)

            # if the task is not a binder or an effect, no impact in the flag
            if isinstance(t, Flatten.Frame.binders) or isinstance(t, Flatten.Frame.effects):
                return all_scope_was_bound

            # any other task sets the flag to false
            return False

    @dataclass
    class Context():
        # the logicals that will be at the top level at the end of the rewrite
        top_level: list[ir.Logical] = field(default_factory=list)
        # new relations created during the pass
        relations: list[ir.Relation] = field(default_factory=list)
        # the stack of frames
        frames: list[Flatten.Frame] = field(default_factory=list)

        def compute_scope(self) -> OrderedSet[ir.Task]:
            """ Get all tasks in scope, from all frames in scope. """
            tasks = ordered_set()
            for frame in self.frames:
                tasks.update(frame.scope)
            return tasks

    @dataclass
    class HandleResult():
        """ The result of the handle methods. """
        # when a task is handled, the replacement for it, if any; if the task is not changed,
        # this can be the task itself; if the task was extracted as a new logical, for
        # for example, this can be a lookup to the connection relationl; if all sub-tasks
        # became logicals with effects, this can be empty.
        replacement: Optional[ir.Task]

        # True if the flattening of the task bound the scope passed to it; this is used to
        # determine if the scope can be removed from the caller, essentially because it was
        # used by all  children.
        scope_was_bound: bool = field(default=False)

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

        # create frame to process the logical
        frame = Flatten.Frame(task)
        ctx.frames.append(frame)

        # recursively handle children, collecting the replacements in the body
        body:OrderedSet[ir.Task] = ordered_set()
        all_scope_was_bound = None
        for t in task.body:
            x = self.handle(t, ctx)
            if x.replacement is not None:
                self._extend_body(body, x.replacement)
            all_scope_was_bound = frame.updated_scope_binding(all_scope_was_bound, t, x.scope_was_bound)
        ctx.frames.pop()

        # if the scope was bound to all relevant children, it can be removed from the body
        if all_scope_was_bound:
            body = body - frame.scope

        # all children were extracted
        if not body:
            return Flatten.HandleResult(None)

        # short-circuit when there's a single child that is a logical, return it
        if len(body) == 1 and isinstance(body.some(), ir.Logical):
            t = cast(ir.Logical, body.some())
            engine = task.engine if t.engine is None else t.engine
            return Flatten.HandleResult(ir.Logical(engine, task.hoisted, t.body))

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
            body = ctx.compute_scope() | body
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
            body = ctx.compute_scope() | body

            # extract a new logical for the aggregate
            exposed_vars = list(agg.group) + helpers.aggregate_outputs(agg)
            connection = self._extract(agg, body, exposed_vars, ctx)

            # return a reference to the connection relation
            reference = f.logical([f.lookup(connection, exposed_vars)], self._merge_var_list(exposed_vars, task.hoisted))
            return Flatten.HandleResult(reference, True)

        return Flatten.HandleResult(ir.Logical(task.engine, task.hoisted, tuple(body)))


    def handle_match(self, match: ir.Match, ctx: Context):
        # TODO: how to deal with malformed input like this?
        if not match.tasks:
            return Flatten.HandleResult(match)

        body = ctx.compute_scope()
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
                branch_body = OrderedSet.from_iterable([f.union([f.logical(branch_body.list), reference])])
            connection = self._extract(branch, branch_body, exposed_vars, ctx, "match")
            reference = f.logical([f.lookup(connection, exposed_vars)], exposed_vars)

        return Flatten.HandleResult(reference, True)


    def handle_union(self, union: ir.Union, ctx: Context):
        # TODO: how to deal with malformed input like this?
        if not union.tasks:
            return Flatten.HandleResult(union)

        body = ctx.compute_scope()
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
