# pyright: reportArgumentType=false
from itertools import product
from typing import cast, Union

from relationalai.early_access.dsl.core.namespaces import Namespace
from relationalai.early_access.dsl.core.types import Type
from relationalai.early_access.dsl.core.types.constrained.nominal import ValueType
from relationalai.early_access.dsl.ontologies.relationships import Relationship, Reading
from relationalai.early_access.dsl.ontologies.roles import Role
from relationalai.early_access.dsl.bindings.tables import Binding, ColumnRef, SubtypeBinding, IdentifierBinding, \
    RoleBinding, SnowflakeTable
from relationalai.early_access.dsl.codegen.relations import EntityMap, ValueMap, EntitySubtypeMap, RoleMap
from relationalai.early_access.dsl.core.relations import rule, Relation
from relationalai.early_access.dsl.core.rules import Annotation, Vars
from relationalai.early_access.dsl.core.types import AbstractValueType
from relationalai.early_access.dsl.core.types.standard import RowId
from relationalai.early_access.dsl.core.utils import camel_to_snake
from relationalai.early_access.dsl.ontologies.constraints import Unique, Mandatory
from relationalai.early_access.dsl.types.entities import EntityType
from relationalai.early_access.metamodel.util import OrderedSet


class PotentiallyBoundRelationship:
    _relationship: 'Relationship'
    _table: 'SnowflakeTable'
    _bindings: list['Binding']

    def __init__(self, relationship: 'Relationship', table: 'SnowflakeTable'):
        self._relationship = relationship
        self._table = table
        self._bindings = []

    def __hash__(self):
        # hash based on the relationship and the table
        return hash((self._relationship, self._table))

    @property
    def relationship(self):
        return self._relationship

    @property
    def table(self):
        return self._table

    @property
    def bindings(self):
        return self._bindings


class Weaver:
    # Bindings
    _value_type_bindings: OrderedSet['Binding'] = OrderedSet()
    _entity_type_bindings: OrderedSet['Binding'] = OrderedSet()
    _constructor_bindings: OrderedSet[Union['IdentifierBinding', 'SubtypeBinding']] = OrderedSet()
    _referent_constructor_bindings: OrderedSet[Union['IdentifierBinding', 'SubtypeBinding']] = OrderedSet()
    _referent_bindings: OrderedSet['RoleBinding'] = OrderedSet()
    _subtype_bindings: OrderedSet['SubtypeBinding'] = OrderedSet()
    _subtype_binding_references: dict['SubtypeBinding', 'Role'] = {}
    _constructor_binding_binds_to: dict['IdentifierBinding', 'Role'] = {}
    _role_bound_thru: dict['Role', list['Binding']] = {}
    _ref_binding_to_ctor_binding: dict['Binding', 'Binding'] = {}

    # Relationships & Ontological Constraints
    _unary_relationships: OrderedSet['Relationship'] = OrderedSet()
    _binary_relationships: OrderedSet['Relationship'] = OrderedSet()
    _identifier_relationships: OrderedSet['Relationship'] = OrderedSet()
    _entity_identifier_relationships: OrderedSet['Relationship'] = OrderedSet()
    _entity_type_identifier: dict['EntityType', 'Relationship'] = {}
    _bound_relationships: OrderedSet['Relationship'] = OrderedSet()
    _preferred_uc: list['Unique'] = []
    _constructor_roles: OrderedSet['Role'] = OrderedSet()
    _internal_uc_roles: OrderedSet['Role'] = OrderedSet()
    _mandatory_roles: OrderedSet['Role'] = OrderedSet()
    _bound_role: dict['Role', list['Binding']] = {}
    _subtype_of: dict['EntityType', 'EntityType'] = {}
    _inclusive_entity_types: OrderedSet['EntityType'] = OrderedSet()
    _composite_entity_types: OrderedSet['EntityType'] = OrderedSet()
    _subtype_map: dict['EntityType', OrderedSet['EntityType']] = {}
    _subtype_closure: dict['EntityType', OrderedSet['EntityType']] = {}
    _supertype_map: dict['EntityType', 'EntityType'] = {}

    # Physical Relations & Classification
    _relations: dict[str, 'Relation'] = {}
    _preferred_id_relations: OrderedSet['Relation'] = OrderedSet()
    _identifier_relations: OrderedSet['Relation'] = OrderedSet()
    _entity_map_relations: OrderedSet['Relation'] = OrderedSet()
    _subtype_entity_map_relations: OrderedSet['Relation'] = OrderedSet()
    _value_map_relations: OrderedSet['Relation'] = OrderedSet()
    _entity_population_relations: OrderedSet['Relation'] = OrderedSet()

    _binding_to_value_map: dict['Binding', 'Relation'] = {}
    _constructor_binding_to_value_map: dict['Binding', 'Relation'] = {}
    _col_ref_to_pid_concept: dict['ColumnRef', 'EntityType'] = {}
    _entity_to_id_relations: dict['EntityType', 'Relation'] = {}
    _concept_to_identifies_relations: dict['Type', 'Relation'] = {}
    _subtype_to_entity_map: dict['EntityType', 'Relation'] = {}

    def __init__(self, model):
        self._model = model

    def analyze(self):
        self._analyze_subtypes()
        potentially_bound_rels = self._analyze_bindings()
        self._analyze_constraints()
        self._analyze_relationships()
        self._analyze_bound_relationships(potentially_bound_rels)

    def _analyze_subtypes(self):
        for subtype_arrow in self._model._subtype_arrows:
            parent = subtype_arrow.end
            if parent not in self._subtype_map:
                self._subtype_map[parent] = OrderedSet()
            self._subtype_map[parent].add(subtype_arrow.start)
            self._supertype_map[subtype_arrow.start] = parent

        self._subtype_closure = {parent: OrderedSet() for parent in self._subtype_map}
        for parent in self._subtype_map.keys():
            self._subtype_closure_dfs(parent, parent)

    def _subtype_closure_dfs(self, prt, curr):
        for chld in self._subtype_map.get(curr, []):
            cls = self._subtype_closure[prt]
            if chld not in cls:
                cls.add(chld)
                self._subtype_closure_dfs(prt, chld)

    def _analyze_bindings(self):
        potentially_bound_rels = {}
        for binding in self._model._bindings:
            role = self._process_binding(binding)
            assert role is not None
            if role not in self._bound_role:
                self._bound_role[role] = []
            self._bound_role[role].append(binding)
            self._categorize_binding(binding, role)

            # Group bindings by relationship and table
            rel = PotentiallyBoundRelationship(role.part_of, binding.column.table)
            if rel not in potentially_bound_rels:
                potentially_bound_rels[rel] = []
            potentially_bound_rels[rel].append(binding)
        return potentially_bound_rels

    def _process_binding(self, binding: 'Binding'):
        if isinstance(binding, SubtypeBinding):
            binding = cast(SubtypeBinding, binding)
            role = self._lookup_ctor_role(binding.parent_type)
            self._subtype_binding_references[binding] = role
            self._subtype_bindings.add(binding)
            self._subtype_of[binding.sub_type] = binding.parent_type
        elif isinstance(binding, IdentifierBinding):
            binding = cast(IdentifierBinding, binding)
            role = self._lookup_ctor_role(binding.entity_type)
            self._constructor_binding_binds_to[binding] = role
        elif isinstance(binding, RoleBinding):
            binding = cast(RoleBinding, binding)
            role = binding.role
        else:
            raise Exception(f'Binding {binding} is not supported')
        return role

    def _categorize_binding(self, binding: 'Binding', role: 'Role'):
        player = role.player()
        if isinstance(player, AbstractValueType):
            self._value_type_bindings.add(binding)
        elif isinstance(player, EntityType):
            self._entity_type_bindings.add(binding)
        else:
            raise Exception(f'Binding {binding} is not supported')

    def _analyze_constraints(self):
        for constraint in self._model.constraints():
            if isinstance(constraint, Unique):
                self._process_unique_constraint(constraint)
            elif isinstance(constraint, Mandatory):
                self._mandatory_roles.update(constraint.roles())

    def _process_unique_constraint(self, constraint: 'Unique'):
        if not constraint.is_preferred_identifier:
            return

        self._preferred_uc.append(constraint)
        roles = constraint.roles()
        self._constructor_roles.update(roles)  # Mark as constructor roles

        if len(roles) != 1:
            raise Exception('Complex preferred identifier case not supported yet')

        constructor_role = roles[0]
        rel = constructor_role.part_of

        if rel.arity() != 2:
            raise Exception('Invalid Identifier relationship configuration')

        player = constructor_role.player()
        if isinstance(player, AbstractValueType):
            self._identifier_relationships.add(rel)
        elif isinstance(player, EntityType):
            self._entity_identifier_relationships.add(rel)
        else:
            raise Exception(f'Identifier relationship {rel.pprint()} has unsupported player type {player.name()}')

        concept = constructor_role.sibling().player()
        self._entity_type_identifier[concept] = rel
        self._inclusive_entity_types.add(concept)

        # Classify bindings
        if constructor_role not in self._bound_role:
            return

        for binding in self._bound_role[constructor_role]:
            if isinstance(binding, IdentifierBinding):
                if not binding.column.references:
                    role = self._lookup_binding_role(binding)
                    self._col_ref_to_pid_concept[binding.column.ref()] = role.player()
                    self._constructor_bindings.add(binding)
                else:
                    self._referent_constructor_bindings.add(binding)
            elif isinstance(binding, SubtypeBinding):
                self._referent_constructor_bindings.add(binding)

    def _analyze_relationships(self):
        for relationship in self._model.relationships():
            arity = relationship.arity()
            if arity == 1:
                self._unary_relationships.add(relationship)
            elif arity == 2:
                self._binary_relationships.add(relationship)

    def _analyze_bound_relationships(self, potentially_bound_rels):
        for rel, bindings in potentially_bound_rels.items():
            rel.bindings.extend(bindings)
            self._analyze_bound_relationship(rel)

    def _lookup_ctor_role(self, entity_type: 'EntityType'):
        # TODO: implement bottom up lookup
        id_rel = self._model.identifier_of(entity_type)
        if id_rel is None:
            raise Exception(f'Identifier relationship for {entity_type} not found')
        for role in id_rel.roles():
            if role.player() == entity_type:
                # ctor role is the only sibling of the constructed entity type role
                return role.sibling()

    def _analyze_bound_relationship(self, meta: 'PotentiallyBoundRelationship'):
        rel = meta.relationship
        arity = rel.arity()

        if arity == 1:
            # Handle unary relationships
            if meta.bindings:
                self._bound_relationships.add(meta)
            return

        if arity != 2:
            raise Exception('N-ary (3+) bound relationship case not supported yet')

        # Handle binary relationships
        key_role, value_role = self._identify_roles(rel)
        key_type, value_type = key_role.player(), value_role.player()

        # TODO : this below should really check if they bound for the same table
        key_role_is_bound = key_role in self._bound_role
        value_role_is_bound = value_role in self._bound_role
        value_role_is_ctor = value_role in self._constructor_roles

        key_role_infers_emap = self._infer_key_role_emap(key_type, meta.table, key_role_is_bound, value_role_is_ctor)
        fully_bound = value_role_is_bound and (key_role_is_bound or key_role_infers_emap)

        is_bound_value_type_relationship = isinstance(value_type, AbstractValueType) and fully_bound
        is_bound = self._is_bound_identifier_relationship(value_role_is_ctor, value_role_is_bound, key_role_is_bound) or \
                   is_bound_value_type_relationship or \
                   self._is_bound_entity_type_relationship(key_type, value_type, key_role, value_role, meta.table)
        if is_bound:
            self._bound_relationships.add(meta)
        else:
            raise Exception('Bound relationship must have at least one bound role and one inferred entity map')

    def _identify_roles(self, rel: 'Relationship') -> tuple['Role', 'Role']:
        key_role, value_role = None, None
        for role in rel.roles():
            if isinstance(role.player(), AbstractValueType):
                value_role = role
            # if both roles are entity types, arbitrarily pick one as the key role
            elif key_role is None and role not in self._constructor_roles:
                key_role = role
            else:
                value_role = role
        assert key_role is not None
        assert value_role is not None
        return key_role, value_role

    def _infer_key_role_emap(self, key_type, table, key_role_is_bound, value_role_is_ctor):
        if key_role_is_bound or value_role_is_ctor:
            return False
        return self._exists_ctor_binding(key_type, table) or self._exists_ref_binding(key_type, table)

    @staticmethod
    def _is_bound_identifier_relationship(value_role_is_ctor, value_role_is_bound, key_role_is_bound):
        if value_role_is_ctor and value_role_is_bound:
            if key_role_is_bound:
                raise Exception('Identifier relationship must not have the key role bound')
            return True
        return False

    def _is_bound_entity_type_relationship(self, key_type, value_type, key_role, value_role, table):
        if isinstance(value_type, EntityType) and isinstance(key_type, EntityType):
            value_role_infers_emap = self._exists_ctor_binding(value_type, table) or self._exists_ref_binding(value_type, table)
            return (
                (key_role in self._bound_role and value_role in self._bound_role) or
                (value_role in self._bound_role and value_role_infers_emap) or
                (key_role in self._bound_role and value_role_infers_emap)
            )
        if isinstance(value_type, AbstractValueType) and isinstance(key_type, AbstractValueType):
            raise Exception('Binary Relationship cannot have more than one ValueType role')
        return False

    def _exists_ctor_binding(self, entity_type: 'EntityType', table: 'SnowflakeTable'):
        return self._lookup_ctor_binding(entity_type, table) is not None

    def _lookup_ctor_binding(self, entity_type: 'EntityType', table: 'SnowflakeTable'):
        # TODO : implement more efficient lookup
        for binding, role in self._constructor_binding_binds_to.items():
            sibling_role = role.sibling()
            assert sibling_role is not None
            if sibling_role.player() == entity_type and binding.column.table == table:
                return binding
        if entity_type in self._subtype_closure:
            for subtype in self._subtype_closure[entity_type]:
                cand = self._lookup_ctor_binding(subtype, table)
                if cand:
                    return cand
        return None

    def _exists_ref_binding(self, entity_type: 'EntityType', table: 'SnowflakeTable'):
        return self._lookup_ref_binding(entity_type, table) is not None

    def _lookup_ref_binding(self, entity_type: 'EntityType', table: 'SnowflakeTable'):
        # TODO : implement more efficient lookup
        for binding, role in self._subtype_binding_references.items():
            if isinstance(binding, SubtypeBinding):
                binding = cast(SubtypeBinding, binding)
                sibling_role = role.sibling()
                assert sibling_role is not None
                if sibling_role.player() == binding.parent_type and binding.column.table == table and entity_type == binding.sub_type:
                    return binding
        if entity_type in self._subtype_closure:
            for subtype in self._subtype_closure[entity_type]:
                cand = self._lookup_ref_binding(subtype, table)
                if cand:
                    return cand
        return None

    def _lookup_binding_role(self, binding: 'Binding'):
        if isinstance(binding, IdentifierBinding):
            role = self._constructor_binding_binds_to[binding]
        elif isinstance(binding, RoleBinding):
            role = binding.role
        elif isinstance(binding, SubtypeBinding):
            role = self._subtype_binding_references[binding]
        else:
            raise Exception(f'Binding {binding} is not supported')
        return role

    def generate(self):
        self._process_bound_relationships()
        self._process_referent_bindings()
        self._generate_value_maps()
        self._generate_entity_maps()
        self._generate_subtype_entity_maps()
        self._generate_entity_populations()
        self._generate_non_identifier_relationships()

    def _process_bound_relationships(self):
        for rel_meta in self._bound_relationships:
            if self._is_identifier_relationship(rel_meta.relationship):
                self._process_identifier_relationship(rel_meta)
            else:
                self._process_non_identifier_relationship(rel_meta)

    def _is_identifier_relationship(self, relationship):
        return relationship in self._identifier_relationships or \
               relationship in self._entity_identifier_relationships

    def _process_identifier_relationship(self, rel_meta):
        roles = rel_meta.relationship.roles()
        ctor_role, concept_role = self._classify_identifier_roles(roles)
        ctor_role_bindings, concept_role_bindings = self._categorize_bindings(rel_meta.bindings)
        self._update_role_bound_thru(ctor_role, ctor_role_bindings)
        self._update_role_bound_thru(concept_role, concept_role_bindings)

    def _classify_identifier_roles(self, roles):
        ctor_role = next((role for role in roles if role in self._constructor_roles), None)
        concept_role = next((role for role in roles if role != ctor_role), None)
        return ctor_role, concept_role

    def _categorize_bindings(self, bindings):
        ctor_role_bindings = []
        concept_role_bindings = []
        for binding in bindings:
            if binding in self._constructor_bindings:
                ctor_role_bindings.append(binding)
                concept_role_bindings.append(binding)
            elif binding in self._referent_constructor_bindings:
                ctor_role_bindings.append(binding)
                concept_role_bindings.append(binding)
            elif binding in self._subtype_bindings:
                concept_role_bindings.append(binding)
        return ctor_role_bindings, concept_role_bindings

    def _update_role_bound_thru(self, role, bindings):
        if role not in self._role_bound_thru:
            self._role_bound_thru[role] = []
        self._role_bound_thru[role].extend(bindings)

    def _process_non_identifier_relationship(self, rel_meta):
        role_bindings = {}
        for binding in rel_meta.bindings:
            role = self._lookup_binding_role(binding)
            role_bindings.setdefault(role, []).append(binding)
            if isinstance(binding, RoleBinding) and isinstance(binding.role.player(), EntityType):
                self._referent_bindings.add(binding)
        self._role_bound_thru.update(role_bindings)

    def _process_referent_bindings(self):
        for binding in self._referent_bindings:
            ctor_binding = self._lookup_binding_reference(binding)
            self._ref_binding_to_ctor_binding[binding] = ctor_binding

    def _generate_value_maps(self):
        for binding in self._value_type_bindings:
            self._gen_value_map(binding)

    def _generate_entity_maps(self):
        for binding in self._constructor_bindings:
            self._gen_entity_map(binding)
            self._gen_preferred_id(binding)
        for binding in self._referent_constructor_bindings:
            self._gen_entity_map(binding)

    def _generate_subtype_entity_maps(self):
        for binding in self._subtype_bindings:
            self._gen_subtype_entity_map(binding)

    def _generate_entity_populations(self):
        for entity_type, relation in self._entity_to_id_relations.items():
            self._gen_entity_population(entity_type, relation)
        for subtype, relation in self._subtype_to_entity_map.items():
            self._gen_entity_population(subtype, relation)

    def _generate_non_identifier_relationships(self):
        for rel_meta in self._bound_relationships:
            if not self._is_identifier_relationship(rel_meta.relationship):
                self._gen_semantic_predicate(rel_meta)

    def _lookup_binding_reference(self, binding):
        ref_concept = binding.role.player()
        # case 1: ref_concept is an entity type with a reference scheme - just look up the ID relationship
        if ref_concept in self._inclusive_entity_types:
            return self._lookup_inclusive_type_binding(ref_concept, binding)
        # case 2: ref_concept is an entity type with a composite reference scheme
        elif ref_concept in self._composite_entity_types:
            # TODO implement composite reference scheme
            raise Exception('Composite reference scheme not supported yet')
        # case 3: ref_concept has no reference scheme, i.e. exclusive entity type
        else:
            # In this case we look up an IdentifierBinding that has the same column as the binding
            # and role player as the same entity type played by the binding. It must be unique,
            # otherwise we raise an exception.
            #
            # NOTE: this is oversimplified now, as we check subtype closure AND immediate supertype.
            cand_bindings = []
            supertype = self._supertype_map.get(ref_concept)
            if supertype and supertype in self._inclusive_entity_types:
                cand = self._lookup_inclusive_type_binding(supertype, binding)
                if cand:
                    cand_bindings.append(cand)
            else:
                subtype_closure = self._subtype_closure[ref_concept]
                for cand_binding in self._constructor_bindings:
                    ctor_role = self._lookup_binding_role(cand_binding)
                    # to be precise, we need to compare with the sibling role, as it is the one that
                    # is played by the entity type in question
                    sibling_role = ctor_role.sibling()
                    assert sibling_role is not None
                    concept = sibling_role.player()
                    assert isinstance(concept, EntityType)
                    if cand_binding.column == binding.column and concept in subtype_closure:
                        cand_bindings.append(cand_binding)
            if len(cand_bindings) != 1:
                raise Exception(f'Binding {binding} has no unique reference to an IdentifierBinding')
            else:
                return cand_bindings[0]

    def _lookup_inclusive_type_binding(self, ref_concept: 'EntityType', binding: 'Binding'):
        identifier_relationship = self._model.identifier_of(ref_concept)
        # TODO optimize
        ctor_binding = None
        concept_role = None
        for role in identifier_relationship.roles():
            if role in self._constructor_roles:
                concept_role = role.sibling()
            else:
                concept_role = role
            break
        for cand_binding in self._role_bound_thru[concept_role]:
            if isinstance(cand_binding, IdentifierBinding) and binding.column == cand_binding.column:
                ctor_binding = cand_binding
                break
        return ctor_binding

    def _gen_preferred_id(self, binding: Union['IdentifierBinding', 'SubtypeBinding']):
        # =
        # Simple case: single role, hence the preferred id is the role itself.
        #
        # We generate the following rules:
        #
        #   def {concept}:id(v, c): ...
        # =
        ctor_role = self._lookup_binding_role(binding)
        value_concept = ctor_role.player()
        val_role = ctor_role.sibling()
        assert val_role is not None
        entity_concept = val_role.player()

        # find the relations that have been created
        pref_id_relation = None
        identifies_relation = None
        for reading in ctor_role.part_of.readings():
            roles = reading.roles
            rel_name = reading.rel_name
            if roles[0] == ctor_role:
                if isinstance(value_concept, EntityType) or isinstance(value_concept, ValueType):
                    identifies_relation = getattr(value_concept, rel_name)
            else:
                assert isinstance(entity_concept, EntityType)
                pref_id_relation = entity_concept[rel_name]

        rel_nm = self._fqn_preferred_id(entity_concept)
        assert pref_id_relation is not None
        with pref_id_relation:
            @rule()
            def identifier(c, i):
                row = Vars(RowId)
                self._ref_value_map(binding)(row, i)
                self._ref_constructor_entity_map(binding)(row, c)
        self._register_relation(rel_nm, pref_id_relation, self._preferred_id_relations)
        self._entity_to_id_relations[entity_concept] = pref_id_relation

        # multiple bindings can exist, but we only need to transpose once
        rel_nm = self._fqn_identifies(value_concept)
        # TODO: fix this one below
        if isinstance(value_concept, AbstractValueType) and rel_nm not in self._relations:
            identifies_relation = self._model.external_relation(rel_nm, value_concept, entity_concept)
        assert identifies_relation is not None
        if identifies_relation not in self._identifier_relations:
            assert pref_id_relation is not None
            with identifies_relation:
                @rule()
                def identifies(i, c):
                    pref_id_relation(c, i)
            self._register_relation(rel_nm, identifies_relation, self._identifier_relations)
            self._concept_to_identifies_relations[value_concept] = identifies_relation

    @staticmethod
    def _fqn_preferred_id(concept: 'EntityType'):
        return f'{camel_to_snake(concept.name())}__id'

    def _ref_identifies(self, binding: 'Binding'):
        pid_ref = binding.column.references
        if pid_ref:
            concept = self._col_ref_to_pid_concept[pid_ref]
        else:
            role = self._lookup_binding_role(binding)
            concept = role.player()
        fqn = self._fqn_identifies(concept)
        return self._lookup_relation_by_fqn(fqn)

    @staticmethod
    def _fqn_identifies(concept: 'Type'):
        if isinstance(concept, EntityType):
            concept = cast(EntityType, concept)
            ref_schema_nm = concept.ref_schema_name()
        else:
            ref_schema_nm = 'identifies'
        return f'{camel_to_snake(concept.name())}__{ref_schema_nm}'

    def _transpose(self, relation: 'Relation', fqn: str):
        if fqn in self._relations:
            return self._relations[fqn]
        if relation.arity() != 2:
            raise Exception('Transposition only supported for binary relations')
        (left_concept, right_concept) = relation.signature().types()
        rel = self._model.external_relation(fqn, right_concept, left_concept)
        with rel:
            @rule()
            def transpose(left, right):
                relation(right, left)
        self._relations[fqn] = rel
        return rel

    def _gen_entity_map(self, binding: 'Binding'):
        vt_role = self._lookup_binding_role(binding)
        et_role = vt_role.sibling()
        assert et_role is not None
        value_concept = vt_role.player()
        entity_concept = et_role.player()
        assert isinstance(entity_concept, EntityType)
        rel_nm = self._fqn_entity_map_indexed(binding, et_role)
        rel = EntityMap(Namespace.top, rel_nm, RowId, binding.column.relation(), et_role)
        role_map = self._ref_value_map(binding) if isinstance(value_concept,
                                                              AbstractValueType) else self._ref_constructor_entity_map(
            binding)
        with rel:
            @rule()
            def entity_map(row, et):
                val = Vars(value_concept)
                role_map(row, val)
                if binding.column.references:
                    self._ref_identifies(binding)(val, et)
                else:
                    _ = entity_concept ^ (val, et)  # `_=` is not strictly needed, but it makes IDEs happy ;)
        self._register_relation(rel_nm, rel, self._entity_map_relations)
        self._constructor_binding_to_value_map[binding] = rel

    def _ref_constructor_entity_map(self, binding: 'Binding'):
        role = self._lookup_binding_role(binding)
        return self._ref_entity_map(binding, role.sibling())

    def _fqn_entity_map_indexed(self, binding: 'Binding', role: 'Role'):
        role_bindings = self._role_bound_thru[role]
        idx = role_bindings.index(binding)
        fqn = self._fqn_entity_map(binding, role.player())
        fqn = f'{fqn}{idx}' if idx > 0 else fqn
        return fqn

    def _ref_entity_map(self, binding: 'Binding', role: 'Role'):
        fqn = self._fqn_entity_map_indexed(binding, role)
        return self._lookup_relation_by_fqn(fqn)

    def _ref_subtype_entity_map(self, binding: 'SubtypeBinding'):
        fqn = self._fqn_entity_map(binding, binding.sub_type)
        return self._lookup_relation_by_fqn(fqn)

    @staticmethod
    def _fqn_entity_map(binding: 'Binding', concept: 'EntityType'):
        assert isinstance(concept, EntityType)
        concept_nm = camel_to_snake(concept.name())
        source_nm = binding.column.table.physical_name()
        return f'{concept_nm}__impl__{source_nm}_row_to_{concept_nm}'

    def _gen_subtype_entity_map(self, binding: 'SubtypeBinding'):
        subtype = binding.sub_type
        rel_nm = self._fqn_entity_map(binding, subtype)
        rel = EntitySubtypeMap(Namespace.top, rel_nm, RowId, binding)
        with rel:
            @rule()
            def subtype_entity_map(row, et):
                self._ref_constructor_entity_map(binding)(row, et)
        self._register_relation(rel_nm, rel, self._subtype_entity_map_relations)
        self._subtype_to_entity_map[subtype] = rel

    def _gen_value_map(self, binding: 'Binding'):
        role = self._lookup_binding_role(binding)
        rel_nm = self._fqn_value_map_indexed(binding)
        rel = ValueMap(Namespace.top, rel_nm, RowId, binding.column.relation(), role)
        with rel:
            @rule(Annotation.INLINE)
            def value_map(row, val):
                rel.attr_view()(row, val)
        self._binding_to_value_map[binding] = rel
        self._register_relation(rel_nm, rel, self._value_map_relations)

    def _fqn_value_map(self, binding: 'Binding'):
        role = self._lookup_binding_role(binding)
        concept = role.player()
        assert isinstance(concept, AbstractValueType)
        concept_nm = camel_to_snake(concept.name())
        source_nm = binding.column.table.physical_name()
        return f'{concept_nm}__impl__{source_nm}_row_to_{concept_nm}'

    def _fqn_value_map_indexed(self, binding: 'Binding'):
        role = self._lookup_binding_role(binding)
        role_bindings = self._role_bound_thru[role]
        idx = role_bindings.index(binding)
        fqn = self._fqn_value_map(binding)
        fqn = f'{fqn}{idx}' if idx > 0 else fqn
        return fqn

    def _ref_value_map(self, binding: 'Binding'):
        fqn = self._fqn_value_map_indexed(binding)
        return self._lookup_relation_by_fqn(fqn)

    def _gen_entity_population(self, entity_type: 'EntityType', lookup_rel: 'Relation'):
        rel_nm = self._fqn_entity_population(entity_type)
        rel = self._model.external_relation(rel_nm, entity_type)
        if lookup_rel in self._preferred_id_relations:
            val_type = self._get_last_type(lookup_rel)
            with rel:
                @rule()
                def entity_population(et):
                    row = Vars(val_type)
                    lookup_rel(et, row)
        elif lookup_rel in self._subtype_entity_map_relations:
            with rel:
                @rule()
                def entity_population(et):
                    row = Vars(RowId)
                    lookup_rel(row, et)
        else:
            raise Exception(f'Unsupported weaving type for relation `{lookup_rel.qualified_name()}`')
        self._register_relation(rel_nm, rel, self._entity_population_relations)

    @staticmethod
    def _fqn_entity_population(entity_type: 'EntityType'):
        # entity population name is the same as the entity type name, with the first letter uppercased
        return entity_type.name()

    def _lookup_relation_by_fqn(self, fqn: str):
        if fqn in self._relations:
            return self._relations[fqn]
        else:
            raise Exception(f'Relation with fully qualified name {fqn} not found in the model')

    def _gen_semantic_predicate(self, rel_meta: 'PotentiallyBoundRelationship'):
        relationship = rel_meta.relationship
        if relationship.arity() > 2:
            raise Exception(
                f'Cannot generate semantic predicate for relationship {relationship.pprint()} with arity {relationship.arity()} (more than 2)')
        roles = relationship.roles()
        # Each role should either be covered by a value map (AbstractValueType role) or by an entity map
        # (EntityType role), which either can be inferred if unique exists for the EntityType or must be
        # generated by the respective EntityBinding.
        role_to_role_map = {}
        for role in roles:
            player = role.player()
            # for ValueTypes just look up ValueMap relations
            if isinstance(player, AbstractValueType):
                if role not in self._bound_role:
                    raise Exception(f'ValueType role {role.name()} is not bound')
                else:
                    value_maps = [self._ref_value_map(binding) for binding in self._bound_role[role]]
                    if len(value_maps) == 0:
                        raise Exception(f'ValueType role {role.name()} is not correctly bound')
                    if role not in role_to_role_map:
                        role_to_role_map[role] = OrderedSet()
                    role_to_role_map[role].update(value_maps)
            elif isinstance(player, EntityType):
                entity_maps = OrderedSet()
                if role not in self._bound_role:
                    if player in self._subtype_of:
                        binding = self._lookup_ref_binding(player, rel_meta.table)
                        if binding is None:
                            raise Exception(f'EntityType({player.name()}) role {role.name()} is not bound')
                        entity_map = self._ref_subtype_entity_map(binding)
                        entity_maps.add(entity_map)
                    else:
                        binding = self._lookup_ctor_binding(player, rel_meta.table)
                        if binding is None:
                            raise Exception(f'EntityType({player.name()}) role {role.name()} is not bound')
                        entity_map = self._ref_constructor_entity_map(binding)
                        entity_maps.add(entity_map)
                else:
                    bindings = self._bound_role[role]
                    for binding in bindings:
                        if isinstance(binding, RoleBinding) and binding in self._referent_bindings:
                            binding = self._ref_binding_to_ctor_binding[binding]
                        entity_map = self._ref_constructor_entity_map(binding)
                        assert entity_map is not None
                        entity_maps.add(entity_map)
                if len(entity_maps) == 0:
                    raise Exception(f'EntityType role {role.name()} is not correctly bound')
                if role not in role_to_role_map:
                    role_to_role_map[role] = OrderedSet()
                role_to_role_map[role].update(entity_maps)
            else:
                raise Exception(f'Role {role.name()} is not bound to a ValueType or EntityType')
        # if we got all roles with role maps, we can generate the rule
        items = role_to_role_map.items()
        if len(items) != relationship.arity():
            raise Exception(f'Not all roles of relationship {relationship.pprint()} are bound')
        for reading in relationship.readings():
            concept = reading.roles[0].player()
            rel_nm = reading.rel_name
            relation = concept[rel_nm]

            role_map_combinations = self._permute_role_maps(role_to_role_map, as_in=reading)
            for role_map1, role_map2 in role_map_combinations:
                with relation:
                    @rule()
                    def semantic_predicate(c, v):
                        row = Vars(RowId)
                        role_map1(row, c)
                        role_map2(row, v)

    @staticmethod
    def _permute_role_maps(role_to_role_map: dict['Role', OrderedSet['RoleMap']], as_in: 'Reading'):
        try:
            role_map_combinations = product(*(role_to_role_map[role] for role in as_in.roles))
            return [list(combination) for combination in role_map_combinations]
        except KeyError as e:
            missing_role = e.args[0]
            raise Exception(f'Cannot permute role maps to match reading `{as_in.rel_name}`, role `{missing_role.name()}` not found')

    @staticmethod
    def _get_last_type(lookup_rel: 'Relation'):
        return lookup_rel.signature().types()[-1]

    def _register_relation(self, name: str, rel: 'Relation', population: OrderedSet['Relation'] = None):
        if isinstance(rel, RoleMap) or isinstance(rel, EntitySubtypeMap):
            self._model._add_relation(rel)
        self._relations[name] = rel
        if population is not None:
            population.add(rel)
