import json
import re
from collections import defaultdict

import xmltodict

from relationalai.early_access.dsl.adapters.orm.model import ORMEntityType, ORMValueType, ORMRole, SubtypeArrow, \
    ORMUniquenessConstraint, ORMReading


class ORMParser:

    def __init__(self, orm_file_path):
        with open(orm_file_path) as orm_file:
            data = xmltodict.parse(orm_file.read())

        self._ontology = json.loads(json.dumps(data))

        self._model_name = self._parse_model_name()
        self._entity_types = self._parse_entity_types()
        self._value_types = self._parse_value_types()
        self._object_types = {**self._value_types, **self._entity_types}
        self._roles = self._parse_roles()
        self._role_value_constraints = self._parse_role_value_constraints()
        self._subtype_facts = self._parse_subtype_facts()
        self._internal_uniqueness_constraints, self._external_uniqueness_constraints = self._parse_uniqueness_constraints()
        self._fact_type_readings = self._parse_fact_types_reading_orders()

    def model_name(self):
        return self._model_name

    def entity_types(self) -> dict[str, ORMEntityType]:
        return self._entity_types

    def object_types(self):
        return self._object_types

    def value_types(self):
        return self._value_types

    def roles(self):
        return self._roles

    def role_value_constraints(self):
        return self._role_value_constraints

    def subtype_facts(self):
        return self._subtype_facts

    def internal_uniqueness_constraints(self):
        return self._internal_uniqueness_constraints

    def external_uniqueness_constraints(self):
        return self._external_uniqueness_constraints

    def fact_type_readings(self):
        return self._fact_type_readings

    def fact_type_to_roles(self):
        fact_type_data = defaultdict(list)
        for role in self._roles.values():
            relationship_name = role.relationship_name
            fact_type_data[relationship_name].append(role)
        return fact_type_data

    def fact_type_to_unique_constraints(self):
        fact_type_to_uc = defaultdict(list)

        for uc_id, uc in self._internal_uniqueness_constraints.items():
            role_id = uc.roles[0]
            role = self._roles.get(role_id)

            if not role or not role.relationship_name:
                continue

            fact_type_to_uc[role.relationship_name].append(uc_id)

        return fact_type_to_uc

    def _parse_model_name(self):
        model_name = self._get_nested(self._ontology, "ormRoot:ORM2", "orm:ORMModel", "@Name")
        return model_name if model_name else "ORMModel"

    def _parse_entity_types(self):
        entity_types = {}
        orm_entity_types = self._get_nested(self._ontology, "ormRoot:ORM2", "orm:ORMModel",
                                            "orm:Objects", "orm:EntityType")
        if orm_entity_types:
            for et in orm_entity_types:
                id = et["@id"]
                name = et['@Name']
                reference_mode = et.get("@_ReferenceMode")
                preferred_id = None if reference_mode == "" else name + "_" + reference_mode
                entity_types[id] = ORMEntityType(id, name, preferred_id)
        return entity_types

    def _parse_value_types(self):
        value_types = {}
        data_types = self._parse_data_types()
        orm_value_types = self._get_nested(self._ontology, "ormRoot:ORM2", "orm:ORMModel",
                                            "orm:Objects", "orm:ValueType")
        if orm_value_types:
            for vt in orm_value_types:
                id = vt["@id"]
                name = vt['@Name']
                data_type = data_types[vt["orm:ConceptualDataType"]["@ref"]]
                value_types[id] = ORMValueType(id, name, data_type)
        return value_types

    def _parse_data_types(self):
        data_types = {}
        orm_data_types = self._get_nested(self._ontology, "ormRoot:ORM2", "orm:ORMModel", "orm:DataTypes")
        if orm_data_types:
            for k, v in orm_data_types.items():
                if v is not None:
                    data_types[v["@id"]] = k[4:]
        return data_types

    def _parse_roles(self):
        roles = {}
        role_to_player = self._parse_role_player()
        orm_fact_types = self._get_nested(self._ontology, "ormRoot:ORM2", "orm:ORMModel", "orm:Facts", "orm:Fact")
        if orm_fact_types:
            for ft in orm_fact_types:
                relationship_name = (ft['@_Name'])
                orm_roles = self._get_nested(ft, "orm:FactRoles", "orm:Role")
                if orm_roles:
                    roles_list = orm_roles if isinstance(orm_roles, list) else [orm_roles]
                    for ro in roles_list:
                        role_id = ro["@id"]
                        role_name = ro["@Name"]
                        roles[role_id] = ORMRole(role_id, role_name, relationship_name, role_to_player[role_id])
        return roles

    def _parse_role_player(self):
        role_to_player = {}
        object_types = ((self._get_nested(self._ontology, "ormRoot:ORM2", "orm:ORMModel", "orm:Objects", "orm:EntityType") or []) +
                        (self._get_nested(self._ontology, "ormRoot:ORM2", "orm:ORMModel", "orm:Objects", "orm:ValueType") or []))
        for ot in object_types:
            roles = self._get_nested(ot, "orm:PlayedRoles", "orm:Role")
            if roles:
                roles_list = roles if isinstance(roles, list) else [roles]
                for role in roles_list:
                    role_to_player[role["@ref"]] = ot["@id"]
        return role_to_player

    def _parse_role_value_constraints(self):
        role_value_constraints = defaultdict(list)
        fact_types = self._get_nested(self._ontology, "ormRoot:ORM2", "orm:ORMModel", "orm:Facts", "orm:Fact")
        if fact_types:
            for ft in fact_types:
                roles = self._get_nested(ft,"orm:FactRoles", "orm:Role")
                if roles and isinstance(roles, list):
                    for ro in roles:
                        value_ranges = self._get_nested(ro, "orm:ValueRestriction", "orm:RoleValueConstraint",
                                                        "orm:ValueRanges", "orm:ValueRange")
                        if value_ranges:
                            for rvc in value_ranges:
                                if rvc.get("@MinValue") != rvc.get("@MaxValue"):
                                    raise Exception("Unsupported value range constraint.")
                                role_value_constraints[ro["@id"]].append(rvc["@MinValue"])
        return role_value_constraints

    def _parse_subtype_facts(self):
        subtype_of = {}
        object_types = self._object_types
        for subtype_arrow in self._parse_subtype_arrows():
            subtype = object_types[subtype_arrow.start]
            supertype = object_types[subtype_arrow.end]
            if subtype_of.get(supertype.name) is not None:
                subtype_of[supertype.name].append(subtype.name)
            else:
                subtype_of[supertype.name] = [subtype.name]
        return subtype_of

    def _parse_subtype_arrows(self):
        subtype_of = []
        orm_subtype_facts = self._get_nested(self._ontology, "ormRoot:ORM2", "orm:ORMModel",
                                             "orm:Facts", "orm:SubtypeFact")
        if orm_subtype_facts:
            subtype_facts = orm_subtype_facts if isinstance(orm_subtype_facts, list) else [orm_subtype_facts]
            for sft in subtype_facts:
                subtype_of.append(self._parse_subtype_arrow(sft))
        return subtype_of

    def _parse_subtype_arrow(self, subtype_fact):
        fact_roles = subtype_fact["orm:FactRoles"]
        subtype = self._get_nested(fact_roles, "orm:SubtypeMetaRole", "orm:RolePlayer", "@ref")
        supertype = self._get_nested(fact_roles, "orm:SupertypeMetaRole", "orm:RolePlayer", "@ref")
        return SubtypeArrow(subtype, supertype)

    def _parse_uniqueness_constraints(self):
        internal = {}
        external = {}
        orm_ucs = self._get_nested(self._ontology, "ormRoot:ORM2", "orm:ORMModel",
                                   "orm:Constraints", "orm:UniquenessConstraint")
        if orm_ucs:
            for uc in orm_ucs:
                uc_id = uc["@id"]
                pid = uc.get("orm:PreferredIdentifierFor", None)
                identifies = None
                if pid is not None and pid["@ref"] in self._entity_types:
                    identifies = pid["@ref"]
                uc_roles = []
                roles = self._get_nested(uc, "orm:RoleSequence", "orm:Role")
                if roles:
                    roles_list = roles if isinstance(roles, list) else [roles]
                    for ro in roles_list:
                        role_id = ro["@ref"]
                        uc_roles.append(role_id)
                constraint = ORMUniquenessConstraint(uc_id, uc_roles, identifies)
                target = internal if uc.get("@IsInternal") == "true" else external
                target[uc_id] = constraint
        return internal, external

    def _parse_fact_types_reading_orders(self):
        fact_types_readings = defaultdict(list)
        fact_types = self._get_nested(self._ontology, "ormRoot:ORM2", "orm:ORMModel", "orm:Facts", "orm:Fact")
        if fact_types:
            for ft in fact_types:
                relationship_name = (ft['@_Name'])
                reading_orders = self._get_nested(ft, "orm:ReadingOrders", "orm:ReadingOrder")
                if reading_orders:
                    ros = reading_orders if isinstance(reading_orders, list) else [reading_orders]
                    for ro in ros:
                        reading = self._parse_fact_types_reading_order(ro)
                        if reading:
                            fact_types_readings[relationship_name].append(self._parse_reading(reading))
        return fact_types_readings

    def _parse_fact_types_reading_order(self, reading_order):
        reading = self._get_nested(reading_order, "orm:Readings", "orm:Reading", "orm:Data")
        if reading:
            roles = self._get_nested(reading_order, "orm:RoleSequence", "orm:Role")
            if roles:
                roles_list = roles if isinstance(roles, list) else [roles]
                for i, seq in enumerate(roles_list):
                    role_id = seq["@ref"]
                    player = self._roles[role_id].player
                    reading = reading.replace(f"{{{i}}}", f"{{{player}}}")
            return reading
        return None

    @staticmethod
    def _parse_reading(reading):
        pattern = r'(\{_[0-9A-Fa-f\-]{36}\})\s*(.*?)\s*(?=\{_[0-9A-Fa-f\-]{36}\}|$)'
        matches = re.findall(pattern, reading)
        players = []
        texts = []

        for match in matches:
            player, text = match
            players.append(player.strip('{}'))
            texts.append(text.strip())
        return ORMReading(players, texts)

    @staticmethod
    def _get_nested(d, *keys):
        for key in keys:
            d = d.get(key)
            if d is None:
                return None
        return d