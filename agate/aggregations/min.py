#!/usr/bin/env python

from agate.aggregations.base import Aggregation
from agate.data_types import Date, DateTime, Number
from agate.exceptions import DataTypeError


class Min(Aggregation):
    """
    Calculate the minimum value in a column. May be applied to columns containing
    :class:`.DateTime` or :class:`.Number` data.
    """
    def __init__(self, column_name):
        self._column_name = column_name

    def get_aggregate_data_type(self, table):
        column = table.columns[self._column_name]

        if (isinstance(column.data_type, Number) or
        isinstance(column.data_type, Date) or
        isinstance(column.data_type, DateTime)):
            return column.data_type

    def validate(self, table):
        column = table.columns[self._column_name]

        if not (isinstance(column.data_type, Number) or
        isinstance(column.data_type, Date) or
        isinstance(column.data_type, DateTime)):
            raise DataTypeError('Min can only be applied to columns containing DateTime orNumber data.')

    def run(self, table):
        column = table.columns[self._column_name]

        return min(column.values_without_nulls())
