"""Unit tests for StatisticsTable."""
import unittest
from collections import OrderedDict

import mock

from erfgoedbot import statistics_table


class TestIsNumber(unittest.TestCase):

    """Test the is_number method."""

    def test_is_number_empty_string_fail(self):
        s = ''
        result = statistics_table.is_number(s)
        self.assertEqual(result, False)

    def test_is_number_none_fail(self):
        s = None
        result = statistics_table.is_number(s)
        self.assertEqual(result, False)

    def test_is_number_random_string_fail(self):
        s = 'random_string'
        result = statistics_table.is_number(s)
        self.assertEqual(result, False)

    def test_is_number_valid_int_succeed(self):
        s = '123'
        result = statistics_table.is_number(s)
        self.assertEqual(result, True)

    def test_is_number_valid_float_succeed(self):
        s = '123.456'
        result = statistics_table.is_number(s)
        self.assertEqual(result, True)

    def test_is_number_valid_negative_float_succeed(self):
        s = '-123.456'
        result = statistics_table.is_number(s)
        self.assertEqual(result, True)

    def test_is_number_nan_succeed(self):
        # NaN is a unique string
        s = 'NaN'
        result = statistics_table.is_number(s)
        self.assertEqual(result, True)


class TestStatisticsTableInit(unittest.TestCase):

    """Test the StatisticsTable.__init__ method."""

    def test_statistics_table_init_empty(self):
        st = statistics_table.StatisticsTable({}, [])
        self.assertEqual(st.columns, {})
        self.assertEqual(st.totals, {})
        self.assertEqual(st.rows, [])

    def test_statistics_table_init_basic(self):
        cols = OrderedDict([
            ('a', 'A'),
            ('b', 'B'),
            ('c', None)
        ])
        st = statistics_table.StatisticsTable(cols, ['a'])
        self.assertEqual(st.columns, cols)
        self.assertEqual(st.totals, {'a': 0})
        self.assertEqual(st.rows, [])

    def test_statistics_table_init_list(self):
        cols = ['a', ('b', 'B'), 'c']
        expected = OrderedDict([
            ('a', None),
            ('b', 'B'),
            ('c', None)
        ])
        st = statistics_table.StatisticsTable(cols, [])
        self.assertEqual(st.columns, expected)
        self.assertEqual(st.totals, {})
        self.assertEqual(st.rows, [])

    def test_statistics_table_init_tuple(self):
        cols = ('a', ('b', 'B'), 'c')
        expected = OrderedDict([
            ('a', None),
            ('b', 'B'),
            ('c', None)
        ])
        st = statistics_table.StatisticsTable(cols, [])
        self.assertEqual(st.columns, expected)
        self.assertEqual(st.totals, {})
        self.assertEqual(st.rows, [])


class TestStatisticsTableAddRow(unittest.TestCase):

    """Test the StatisticsTable.add_row method."""

    def setUp(self):
        self.st = statistics_table.StatisticsTable({}, [])
        self.st.columns = OrderedDict([
            ('a', 'A'),
            ('b', 'B')
        ])
        self.st.totals = {'a': 0}
        self.st.rows = []

    def test_statistics_table_add_row_first(self):
        row = {'a': 5, 'b': 'foo'}
        self.st.add_row(row)
        self.assertEqual(self.st.totals, {'a': 5})
        self.assertEqual(self.st.rows, [row])

    def test_statistics_table_add_row_later(self):
        row_1 = {'a': 5, 'b': 'foo'}
        self.st.rows = [row_1]
        self.st.totals = {'a': 5}

        row_2 = {'a': 10, 'b': 'bar'}
        self.st.add_row(row_2)
        self.assertEqual(self.st.totals, {'a': 15})
        self.assertEqual(self.st.rows, [row_1, row_2])

    def test_statistics_table_add_row_nan(self):
        self.st.columns.update({'c': 'C'})
        self.st.totals.update({'c': 0})

        row = {'a': '---', 'b': 'foo', 'c': 1}
        self.st.add_row(row)
        self.assertEqual(self.st.totals, {'a': 0, 'c': 1})
        self.assertEqual(self.st.rows, [row])

    def test_statistics_table_add_row_number_in_text(self):
        row = {'a': 5, 'b': 10}
        self.st.add_row(row)
        self.assertEqual(self.st.totals, {'a': 5})
        self.assertEqual(self.st.rows, [row])

    def test_statistics_table_add_row_number_override_entry(self):
        self.st.totals.update({'b': 0})
        row = {'a': 5, 'b': 10}
        num_cols = {'a': 8}
        self.st.add_row(row, num_cols)
        self.assertEqual(self.st.totals, {'a': 8, 'b': 10})
        self.assertEqual(self.st.rows, [row])

    def test_statistics_table_add_row_number_override_entry_with_zero(self):
        self.st.totals.update({'b': 8})
        row = {'a': 5, 'b': 10}
        num_cols = {'b': 0}
        self.st.add_row(row, num_cols)
        self.assertEqual(self.st.totals, {'a': 5, 'b': 8})
        self.assertEqual(self.st.rows, [row])

    def test_statistics_table_add_row_numeric_not_in_columns(self):
        self.st.totals.update({'c': 0})  # no c in self.st.columns

        row = {'a': '---', 'b': 'foo'}
        num_row = {'c': 1}
        self.st.add_row(row, num_row)
        self.assertEqual(self.st.totals, {'a': 0, 'c': 1})
        self.assertEqual(self.st.rows, [row])

    def test_statistics_table_add_row_missing_value(self):
        row = {'a': 5}
        expected = {'a': 5, 'b': '---'}
        self.st.add_row(row)
        self.assertEqual(self.st.totals, {'a': 5})
        self.assertEqual(self.st.rows, [expected])

    def test_statistics_table_add_row_none_value(self):
        row = {'a': 5, 'b': None}
        expected = {'a': 5, 'b': '---'}
        self.st.add_row(row)
        self.assertEqual(self.st.totals, {'a': 5})
        self.assertEqual(self.st.rows, [expected])

    def test_statistics_table_add_row_override_none_value(self):
        row = {'a': 5, 'b': None}
        expected = {'a': 5, 'b': 'foo'}
        self.st.add_row(row, empty='foo')
        self.assertEqual(self.st.totals, {'a': 5})
        self.assertEqual(self.st.rows, [expected])

    def test_statistics_table_add_row_numeric_not_in_column(self):
        self.st.totals.update({'c': 0})

        row = {'a': '---', 'b': 'foo'}
        num_row = {'c': 1}
        self.st.add_row(row, num_row)
        self.assertEqual(self.st.totals, {'a': 0, 'c': 1})
        self.assertEqual(self.st.rows, [row])


class TestStatisticsTableAddWikitextRow(unittest.TestCase):

    """Test the StatisticsTable.add_wikitext_row method."""

    def setUp(self):
        self.st = statistics_table.StatisticsTable({}, [])
        self.st.columns = OrderedDict([
            ('a', 'A'),
            ('b', 'B')
        ])
        self.st.totals = {'a': 5}
        self.row_1 = {'a': 5, 'b': 'foo'}
        self.st.rows = [self.row_1]

    def test_statistics_table_add_wikitext_row(self):
        row = '|-\n|some wikitext'
        self.st.add_wikitext_row(row)
        self.assertEqual(self.st.totals, {'a': 5})
        self.assertEqual(self.st.rows, [self.row_1, row])

    def test_statistics_table_add_row_trim_trailing_newline(self):
        row = '|-\n|some wikitext\n'
        expected = '|-\n|some wikitext'
        self.st.add_wikitext_row(row)
        self.assertEqual(self.st.totals, {'a': 5})
        self.assertEqual(self.st.rows, [self.row_1, expected])

    def test_statistics_table_add_row_non_wikitext(self):
        with self.assertRaises(ValueError):
            self.st.add_wikitext_row({'a': 5})


class TestStatisticsTableGetHeaderRow(unittest.TestCase):

    """Test the StatisticsTable.get_header_row method."""

    def setUp(self):
        self.st = statistics_table.StatisticsTable({}, [])
        self.st.columns = OrderedDict([
            ('a', 'A'),
            ('b', 'B')
        ])
        self.st.totals = {'b': 10}

        patcher = mock.patch(
            'erfgoedbot.statistics_table.common.table_header_row')
        self.mock_table_header_row = patcher.start()
        self.mock_table_header_row.return_value = 'header_row'
        self.addCleanup(patcher.stop)

    def test_statistics_table_get_header_row(self):
        expected_call = OrderedDict([
            ('A', False),
            ('B', True)
        ])
        result = self.st.get_header_row()
        self.mock_table_header_row.assert_called_once_with(expected_call)
        self.assertEqual(result, 'header_row')

    def test_statistics_table_get_header_row_reuse_label(self):
        self.st.columns.update({'c': None})
        expected_call = OrderedDict([
            ('A', False),
            ('B', True),
            ('c', False)
        ])
        result = self.st.get_header_row()
        self.mock_table_header_row.assert_called_once_with(expected_call)
        self.assertEqual(result, 'header_row')

    # something with inline


class TestStatisticsTableGetSummationRow(unittest.TestCase):

    """Test the StatisticsTable.get_summation_row method."""

    def setUp(self):
        self.st = statistics_table.StatisticsTable({}, [])
        self.st.columns = OrderedDict([
            ('a', 'A'),
            ('b', 'B')
        ])
        self.st.totals = {'b': 10}

        patcher = mock.patch(
            'erfgoedbot.statistics_table.common.table_bottom_row')
        self.mock_table_bottom_row = patcher.start()
        self.mock_table_bottom_row.return_value = 'bottom_row'
        self.addCleanup(patcher.stop)

    def test_statistics_table_get_summation_row(self):
        result = self.st.get_summation_row()
        self.mock_table_bottom_row.assert_called_once_with(2, {1: 10})
        self.assertEqual(result, 'bottom_row')

    # something with inline


class TestStatisticsTableGetSum(unittest.TestCase):

    """Test the StatisticsTable.get_sum method."""

    def setUp(self):
        self.st = statistics_table.StatisticsTable({}, [])
        self.st.totals = {'a': 5, 'b': 10}

    def test_statistics_table_get_sum_all(self):
        result = self.st.get_sum()
        self.assertEqual(result, {'a': 5, 'b': 10})

    def test_statistics_table_get_sum_single(self):
        result = self.st.get_sum('b')
        self.assertEqual(result, 10)


class TestStatisticsTableToWikitext(unittest.TestCase):

    """Test the StatisticsTable.to_wikitext method."""

    def setUp(self):
        self.st = statistics_table.StatisticsTable({}, [])
        self.st.columns = OrderedDict([
            ('a', 'A'),
            ('b', 'B'),
            ('c', 'C')
        ])
        self.st.totals = {'a': 5, 'c': 10}
        self.st.rows = [
            {'a': 1, 'b': 'foo', 'c': 2},
            {'a': 3, 'b': 'bar', 'c': 4}
        ]

        patcher = mock.patch(
            'erfgoedbot.statistics_table.StatisticsTable.get_header_row')
        self.mock_table_header_row = patcher.start()
        self.mock_table_header_row.return_value = 'header_row'
        self.addCleanup(patcher.stop)

        patcher = mock.patch(
            'erfgoedbot.statistics_table.StatisticsTable.get_summation_row')
        self.mock_table_bottom_row = patcher.start()
        self.mock_table_bottom_row.return_value = 'summation_row'
        self.addCleanup(patcher.stop)

    def test_statistics_table_to_wikitext_defaults(self):
        expected = (
            'header_row'
            '|-\n'
            '| 1 \n| foo \n| 2 \n'
            '|-\n'
            '| 3 \n| bar \n| 4 \n'
            'summation_row'
        )
        result = self.st.to_wikitext()
        self.mock_table_header_row.assert_called_once_with()
        self.mock_table_bottom_row.assert_called_once_with()
        self.assertEqual(result, expected)

    def test_statistics_table_to_wikitext_no_summation(self):
        expected = (
            'header_row'
            '|-\n'
            '| 1 \n| foo \n| 2 \n'
            '|-\n'
            '| 3 \n| bar \n| 4 \n'
            '|}\n'
        )
        result = self.st.to_wikitext(add_summation=False)
        self.mock_table_header_row.assert_called_once_with()
        self.mock_table_bottom_row.assert_not_called()
        self.assertEqual(result, expected)

    def test_statistics_table_to_wikitext_inline(self):
        expected = (
            'header_row'
            '|-\n'
            '| 1 || foo || 2 \n'
            '|-\n'
            '| 3 || bar || 4 \n'
            'summation_row'
        )
        result = self.st.to_wikitext(inline=True)
        self.mock_table_header_row.assert_called_once_with()
        self.mock_table_bottom_row.assert_called_once_with()
        self.assertEqual(result, expected)

    def test_statistics_table_to_wikitext_wikitext_row(self):
        self.st.rows = [
            {'a': 1, 'b': 'foo', 'c': 2},
            '|-\n|some wikitext',
            {'a': 3, 'b': 'bar', 'c': 4}
        ]
        expected = (
            'header_row'
            '|-\n'
            '| 1 \n| foo \n| 2 \n'
            '|-\n'
            '|some wikitext\n'
            '|-\n'
            '| 3 \n| bar \n| 4 \n'
            'summation_row'
        )
        result = self.st.to_wikitext()
        self.mock_table_header_row.assert_called_once_with()
        self.mock_table_bottom_row.assert_called_once_with()
        self.assertEqual(result, expected)
