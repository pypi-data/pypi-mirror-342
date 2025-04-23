from collections import defaultdict

from relationalai.early_access.dsl.adapters.orm.parser import ORMParser
from relationalai.early_access.dsl.core.types.standard import Integer, UnsignedInteger, String, DateTime, Date, Decimal
from relationalai.early_access.dsl.ontologies.models import Model
from relationalai.early_access.dsl.types.entities import AbstractEntityType


class ORMAdapter:

    def __init__(self, orm_file_path: str):
        self._parser = ORMParser(orm_file_path)
        self._relationship_role_value_constraints = defaultdict()
        self.model = self.orm_to_model()

    def orm_to_model(self):
        model = Model(self._parser.model_name())

        self._add_value_types(model)
        self._add_entity_types(model)
        self._add_subtype_relationships(model)
        self._add_relationships(model)
        self._add_external_identifying_relationships(model)
        self._add_role_value_constraints(model)

        return model

    def _add_value_types(self, md):
        for vt in self._parser.value_types().values():
            md.value_type(vt.name, self._map_datatype(vt.data_type))

    def _add_entity_types(self, md):
        for et in self._parser.entity_types().values():
            md.entity_type(et.name)

    def _add_subtype_relationships(self, md):
        for parent, children in self._parser.subtype_facts().items():
            supertype = md.lookup_concept(parent)
            subtypes = []
            for child in children:
                sub = md.lookup_concept(child)
                subtypes.append(sub)
            md.subtype_arrow(supertype, subtypes)

    def _add_relationships(self, md):
        object_types = self._parser.object_types()
        role_value_constraints = self._parser.role_value_constraints()
        internal_uniqueness_constraints = self._parser.internal_uniqueness_constraints()
        fact_type_to_roles = self._parser.fact_type_to_roles()
        fact_type_to_unique_constraints = self._parser.fact_type_to_unique_constraints()
        for fact_type, reading_orders in self._parser.fact_type_readings().items():
            with (md.relationship() as rel):
                role_idx_to_player = list()
                # Use the first reading to add the players
                for role in fact_type_to_roles[fact_type]:
                    role_name = role.name if role.name != "" else None
                    p = md.lookup_concept(object_types[role.player].name)
                    rel.role(p, name=role_name)
                    role_idx_to_player.append(p)
                    if role.id in role_value_constraints:
                        self._relationship_role_value_constraints[rel] = role_value_constraints[role.id]
                # Create the readings
                for rdo in reading_orders:
                    argz = []
                    for player, txt in zip(rdo.players, rdo.texts):
                        p = md.lookup_concept(object_types[player].name)
                        role_idx = role_idx_to_player.index(p)
                        rl = rel.role_at(role_idx)
                        argz.append(rl)
                        if txt != "":
                            argz.append(txt)
                    rel.relation(*argz)
                # Marking identifying relationships
                if fact_type in fact_type_to_unique_constraints:
                    for uc_id in fact_type_to_unique_constraints[fact_type]:
                        uc = internal_uniqueness_constraints[uc_id]
                        if uc.identifies:
                            et = md.lookup_concept(object_types[uc.identifies].name)
                            role_name = role_idx_to_player.index(et)
                            md.ref_scheme(rel.relations()[role_name])

    def _add_external_identifying_relationships(self, model):
        roles = self._parser.roles()
        object_types = self._parser.object_types()
        for uc_id, uc in self._parser.external_uniqueness_constraints().items():
            et = model.lookup_concept(object_types[uc.identifies].name)
            identifying_rel = []
            for ro in uc.roles:
                relationship = model.lookup_relationship(roles[ro].relationship_name)
                for rl in relationship.roles():
                    if rl.player_type == et:
                        idx = relationship.roles().index(rl)
                        identifying_rel.append(relationship.relations()[idx])
            model.ref_scheme(*identifying_rel)

    def _add_role_value_constraints(self, model):
        for rel, values in self._relationship_role_value_constraints.items():
            for rls in rel.relations():
                if isinstance(rls.reading().role_at(0).player(), AbstractEntityType):
                    model.role_value_constraint(rls, values=values)
                    break

    @staticmethod
    def _map_datatype(dt):
        mapping = {
            "AutoCounterNumericDataType": Integer,
            "UnsignedIntegerNumericDataType": UnsignedInteger,
            "VariableLengthTextDataType": String,
            "DateAndTimeTemporalDataType": DateTime,
            "DecimalNumericDataType": Decimal,
            "DateTemporalDataType": Date
        }
        return mapping.get(dt, String)