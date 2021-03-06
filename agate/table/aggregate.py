#!/usr/bin/env python

from agate import utils


def aggregate(self, aggregations):
    """
    Aggregate data from the columns in this self by applying a sequence of
    :class:`.Aggregation` instances.

    :param aggregations:
        A single :class:`.Aggregation` instance or sequence of them.
    :returns:
        If the input was a single :class:`Aggregation` then a single result
        will be returned. If it was a sequence then a tuple of results will
        be returned.
    """
    if utils.issequence(aggregations):
        results = []

        for agg in aggregations:
            agg.validate(self)

        for agg in aggregations:
            results.append(agg.run(self))

        return tuple(results)
    else:
        aggregations.validate(self)

        return aggregations.run(self)
