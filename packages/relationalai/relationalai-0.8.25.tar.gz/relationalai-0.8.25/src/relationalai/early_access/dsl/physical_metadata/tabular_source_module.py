import pandas as pd

from relationalai.early_access.dsl import DateTime, Date, Decimal
from relationalai.early_access.dsl.core import std
from relationalai.early_access.dsl.core.relations import rule, Relation
from relationalai.early_access.dsl.physical_metadata.tabular_source import TabularSource

class TabularSourceModule:
    def generate(self, table: TabularSource, data: pd.DataFrame):
        for index, row in data.iterrows():
            for column in data.columns:
                value = row[column]
                if pd.notna(value):
                    column_type = table._schema[column].root_unconstrained_type()
                    relation = table.__getattribute__(column)
                    if column_type.name() == Date.name():
                        self._row_to_date_value_rule(relation, index, value)
                    elif column_type.name() == DateTime.name():
                        self._row_to_date_time_value_rule(relation, index, value)
                    elif column_type.name() == Decimal.name():
                        self._row_to_decimal_value_rule(relation, index, value)
                    else:
                        self._row_to_value_rule(relation, index, value)

    @staticmethod
    def _row_to_value_rule(relation: Relation, row, value):
        with relation:
            @rule()
            def row_to_value(r, v):
                r == row
                v == value

    @staticmethod
    def _row_to_date_value_rule(relation: Relation, row, value):
        with relation:
            @rule()
            def row_to_value(r, v):
                r == row
                std.parse_date(value, 'Y-m-d', v)

    @staticmethod
    def _row_to_date_time_value_rule(relation: Relation, row, value):
        with relation:
            @rule()
            def row_to_value(r, v):
                r == row
                std.parse_datetime(value, 'Y-m-d HH:MM:SS z', v)

    @staticmethod
    def _row_to_decimal_value_rule(relation: Relation, row, value):
        with relation:
            @rule()
            def row_to_value(r, v):
                r == row
                std.parse_decimal(64, 4, value, v)