from __future__ import annotations

from relationalai.early_access.metamodel import ir, factory as f, util, helpers
from relationalai.early_access.metamodel.compiler import Pass, group_tasks
from relationalai.early_access.metamodel.util import OrderedSet

class ExtractCommonLookups(Pass):
    """
    Extracts common lookups in the body of a logical as a new logical that derives those
    lookups in a temporary relation.

    From:
        Logical
            Logical
                lookup1
                lookup2
                Logical
                    x
                Logical
                    y
    To:
        Logical
            Logical
                lookup1
                lookup2
            Logical
                tmp
                Logical
                    x
                Logical
                    y
    """

    def rewrite(self, model: ir.Model, cache) -> ir.Model:
        if isinstance(model.root, ir.Logical):
            new_body = []
            new_relations:list[ir.Relation] = []
            for child in model.root.body:
                if isinstance(child, ir.Logical):
                    groups = group_tasks(child.body, {
                        "lookups": (ir.Lookup),
                        "logicals": (ir.Logical),
                        "aggregates": (ir.Aggregate),
                        "effects": (ir.Update, ir.Output)
                    })
                    # many lookups to extract because we have multiple logicals, and no aggregates
                    if len(groups["lookups"]) > 1 and len(groups["logicals"]) > 1 and not groups["aggregates"]:
                        new_logicals, relation = self._rewrite(child, groups)
                        new_body.extend(new_logicals)
                        new_relations.append(relation)
                    else:
                        new_body.append(child)
            if new_relations:
                new_relations.extend(model.relations)
                return ir.Model(
                    model.engines,
                    util.FrozenOrderedSet.from_iterable(new_relations),
                    model.types,
                    f.logical(new_body)
                )
        return model


    def _rewrite(self, node: ir.Logical, groups: dict[str, OrderedSet[ir.Task]]):
        new_logicals = []
        new_body = []

        # extract lookups as its own logical, deriving into a tmp relation
        extracted_rule, relation, exposed_vars = self._extract_common_lookups(node, groups)
        new_logicals.append(extracted_rule)

        lookup = ir.Lookup(node.engine, relation, tuple(exposed_vars.list))
        new_body.append(lookup)
        new_body.extend(groups["logicals"])
        if "aggregates" in groups:
            new_body.extend(groups["aggregates"])
        if "other" in groups:
            new_body.extend(groups["other"])
        if "effects" in groups:
            new_body.extend(groups["effects"])
        new_logicals.append(f.logical(new_body))

        return new_logicals, relation


    def _extract_common_lookups(self, node: ir.Logical, groups: dict[str, OrderedSet[ir.Task]]):
        lookups = groups["lookups"]
        effects = groups["effects"]

        # a bit of variable order optimization: if there's an effect in the node, try to use
        # the same variable order for the extracted relation
        lookup_vars = util.ordered_set()
        for lookup in lookups:
            lookup_vars.update(helpers.collect_vars(lookup))

        effect_vars = util.ordered_set()
        for e in effects:
            effect_vars.update(helpers.collect_vars(e))

        # first add the effect vars, and then the rest
        search_vars = util.ordered_set()
        for v in effect_vars:
            if v in lookup_vars:
                search_vars.add(v)
        search_vars.update(lookup_vars)

        # collect all variables used in the lookups, which are also used in other nodes
        exposed_vars: OrderedSet[ir.Var] = util.ordered_set()
        for v in search_vars:
            for task in node.body:
                if task not in lookups:
                    exposed_vars.add(v)

        # create a tmp relation to expose those vars
        relation = f.relation(f"common_{node.id}", [f.field(v.name, v.type) for v in exposed_vars])

        # create the new logical (a rule) that will derive into this relation
        # note that his logical reuses the lookup objects; exposed_vars also reuses the variable objects.
        body = []
        for lookup in lookups:
            body.append(lookup)
        body.append(f.derive(relation, exposed_vars.list))
        extracted_rule = f.logical(body)

        # return the extracted rule, the new temporary relation, and the variables exposed by it
        return extracted_rule, relation, exposed_vars
