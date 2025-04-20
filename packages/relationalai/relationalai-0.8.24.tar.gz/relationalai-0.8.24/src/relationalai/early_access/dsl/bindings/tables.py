import dataclasses
from typing import Optional

from relationalai.early_access.dsl.bindings.common import BindableAttribute, BindableTable
from relationalai.early_access.dsl.bindings.relations import AttributeView
from relationalai.early_access.dsl.core.types import Type
from relationalai.early_access.dsl.core.types.standard import String, Integer, Decimal, Date, DateTime, Boolean, \
    BigInteger, Float, RowId
from relationalai.early_access.dsl.core.utils import generate_stable_uuid
from relationalai.early_access.dsl.core.relations import Relation
from relationalai.early_access.dsl.core.namespaces import Namespace
from relationalai.early_access.dsl.types.entities import EntityType
from relationalai.early_access.dsl.ontologies.roles import Role
#=
# Physical metadata for a Snowflake table.
#=

@dataclasses.dataclass(frozen=True)
class ColumnRef:
    table: str
    column: str

@dataclasses.dataclass
class ForeignKey:
    name: str
    source_columns: list[ColumnRef] = dataclasses.field(default_factory=list)
    target_columns: list[ColumnRef] = dataclasses.field(default_factory=list)

    def __hash__(self):
        return hash(self.name)

@dataclasses.dataclass
class SchemaMetadata:
    name: str
    foreign_keys: list[ForeignKey] = dataclasses.field(default_factory=list)

@dataclasses.dataclass
class ColumnMetadata:
    name: str
    datatype: str
    is_nullable: bool
    numeric_precision: Optional[int] = None
    numeric_precision_radix: Optional[int] = None
    numeric_scale: Optional[int] = None

@dataclasses.dataclass
class TabularMetadata:
    name: str
    columns: list[ColumnMetadata] = dataclasses.field(default_factory=list)
    foreign_keys: set[ForeignKey] = dataclasses.field(default_factory=set)

@dataclasses.dataclass(frozen=True)
class Binding:
    column: 'BindableColumn'

@dataclasses.dataclass(frozen=True)
class RoleBinding(Binding):
    role: 'Role'

@dataclasses.dataclass(frozen=True)
class IdentifierBinding(Binding):
    entity_type: 'EntityType'

@dataclasses.dataclass(frozen=True)
class SubtypeBinding(Binding):
    sub_type: 'EntityType'
    parent_type: 'EntityType'

_sf_type_mapping = {
    'varchar': String,
    'char': String,
    'text': String,
    'date': Date,
    'datetime': DateTime,
    'timestamp_ntz': DateTime,
    'boolean': Boolean,
    'float': Float,
}
def _map_rai_type(col: ColumnMetadata) -> 'Type':
    datatype = col.datatype.lower()
    # TODO: do better with integer type conversion
    if datatype == 'number':
        if col.numeric_scale is not None and col.numeric_scale > 0:
            return Decimal
        elif col.numeric_precision is not None and col.numeric_precision > 9:
            return BigInteger
        else:
            return Integer
    else:
        return _sf_type_mapping[datatype]

class BindableColumn(BindableAttribute):
    _metadata: 'ColumnMetadata'
    _table: 'SnowflakeTable'
    _references: Optional['ColumnRef']

    def __init__(self, metadata: 'ColumnMetadata', table: 'SnowflakeTable', model):
        self._metadata = metadata
        self._table = table
        self._model = model
        self._datatype = _map_rai_type(self._metadata)
        self._references = None
        self._attr_relation = AttributeView(Namespace.top, self)

    def __call__(self, *args):
        return self.relation()(*args)

    def identifies(self, entity_type: 'EntityType'):
        binding = IdentifierBinding(column=self, entity_type=entity_type)
        self._model.role_binding(binding)

    def binds_to(self, role: 'Role'):
        binding = RoleBinding(role=role, column=self)
        self._model.role_binding(binding)

    def references_subtype(self, sub_type: 'EntityType', parent_type: 'EntityType'):
        binding = SubtypeBinding(column=self, sub_type=sub_type, parent_type=parent_type)
        self._model.role_binding(binding)

    def binds(self, relation: 'Relation'):
        roles = relation.reading().roles
        # this binds to the last role in binary relations
        role = roles[-1]
        binding = RoleBinding(role=role, column=self)
        self._model.role_binding(binding)

    def relation(self):
        return self._attr_relation

    @property
    def metadata(self):
        return self._metadata

    @property
    def table(self):
        return self._table

    @property
    def references(self):
        return self._references

    @references.setter
    def references(self, ref: 'ColumnRef'):
        self._references = ref

    def physical_name(self):
        return self._metadata.name

    def type(self):
        return _map_rai_type(self._metadata)

    def guid(self):
        return generate_stable_uuid(f'$attr:{self._table.physical_name()}_{self.physical_name()}')

    def ref(self):
        return ColumnRef(self._table.name, self._metadata.name)


class SnowflakeTable(BindableTable):
    _name: str
    _columns: dict[str, BindableColumn]
    _foreign_keys: set[ForeignKey]

    def __init__(self, metadata: 'TabularMetadata', model):
        self._name = metadata.name
        self._columns = {col.name: BindableColumn(col, self, model) for col in metadata.columns}
        self._foreign_keys = metadata.foreign_keys
        for fk in self._foreign_keys:
            # TODO : this doesn't work for composite FKs
            for col in fk.source_columns:
                target_col = fk.target_columns[0]
                self._columns[col.column].references = target_col

    def __getattr__(self, key):
        if key in self.__dict__:
            return self.__dict__[key]
        if key in self._columns:
            return self._columns[key]
        else:
             raise AttributeError(f'Snowflake table "{self._name}" has no column named "{key}"')

    def __str__(self):
        # returns the name of the table, as well as the columns and their types
        return self._name + ':\n' + '\n'.join(
            [f' {col.metadata.name} {col.metadata.datatype}' for _, col in self._columns.items()]
        ) + '\n' + '\n'.join(
            [f' {fk.source_columns} -> {fk.target_columns}' for fk in self._foreign_keys]
        )

    @property
    def name(self):
        return self._name

    def physical_name(self):
        # physical relation name is always in the form of `{database}_{schema}_{table}
        return self._name.lower().replace('.', '_')

    def key_type(self):
        return RowId
