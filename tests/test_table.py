#!/usr/bin/env python

import unittest2 as unittest

import journalism

class TestTable(unittest.TestCase):
    def setUp(self):
        self.rows = [
            [1, 2, 'a'],
            [2, 3, 'b'],
            [None, 4, 'c']
        ]
        self.column_names = ['one', 'two', 'three']
        self.column_types = [int, int, unicode]

    def test_create_table(self):
        table = journalism.Table.from_rows(self.rows, self.column_types, self.column_names)

        self.assertEqual(len(table), 3)

        self.assertEqual(type(table['one']), journalism.IntColumn)
        self.assertEqual(type(table['two']), journalism.IntColumn)
        self.assertEqual(type(table['three']), journalism.TextColumn)

        self.assertEqual(table['one'], [1, 2, None])
        self.assertEqual(table['two'], [2, 3, 4])
        self.assertEqual(table['three'], ['a', 'b', 'c'])

    def test_create_table_header(self):
        rows = [['one', 'two', 'three']]
        rows.extend(self.rows)

        table = journalism.Table.from_rows(rows, self.column_types)

        self.assertEqual(len(table), 3)

        self.assertEqual(type(table['one']), journalism.IntColumn)
        self.assertEqual(type(table['two']), journalism.IntColumn)
        self.assertEqual(type(table['three']), journalism.TextColumn)

        self.assertEqual(table['one'], [1, 2, None])
        self.assertEqual(table['two'], [2, 3, 4])
        self.assertEqual(table['three'], ['a', 'b', 'c'])
