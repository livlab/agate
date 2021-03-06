#!/usr/bin/env python

from collections import OrderedDict

from agate.data_types import Text
from agate.tableset import TableSet
from agate import utils


@utils.allow_tableset_proxy
def group_by(self, key, key_name=None, key_type=None):
    """
    Create a new :class:`Table` for unique value and return them as a
    :class:`.TableSet`. The :code:`key` can be either a column name
    or a function that returns a value to group by.

    Note that when group names will always be coerced to a string,
    regardless of the format of the input column.

    :param key:
        Either the name of a column from the this table to group by, or a
        :class:`function` that takes a row and returns a value to group by.
    :param key_name:
        A name that describes the grouped properties. Defaults to the
        column name that was grouped on or "group" if grouping with a key
        function. See :class:`.TableSet` for more.
    :param key_type:
        An instance of any subclass of :class:`.DataType`. If not provided
        it will default to a :class`.Text`.
    :returns:
        A :class:`.TableSet` mapping where the keys are unique values from
        the :code:`key` and the values are new :class:`Table` instances
        containing the grouped rows.
    """
    key_is_row_function = hasattr(key, '__call__')

    if key_is_row_function:
        key_name = key_name or 'group'
        key_type = key_type or Text()
    else:
        column = self.columns[key]

        key_name = key_name or column.name
        key_type = key_type or column.data_type

    groups = OrderedDict()

    for row in self.rows:
        if key_is_row_function:
            group_name = key(row)
        else:
            group_name = row[column.name]

        group_name = key_type.cast(group_name)

        if group_name not in groups:
            groups[group_name] = []

        groups[group_name].append(row)

    output = OrderedDict()

    for group, rows in groups.items():
        output[group] = self._fork(rows)

    return TableSet(output.values(), output.keys(), key_name=key_name, key_type=key_type)
