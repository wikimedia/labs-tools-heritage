#!/usr/bin/python
# -*- coding: utf-8  -*-
"""Create a wikitext formated statistics table."""
from __future__ import unicode_literals

from collections import OrderedDict

import common as common


class StatisticsTable(object):
    """A table intended to be outputted as wikitext."""

    def __init__(self, title_columns, numeric):
        """
        Initialise the Table by defining its columns.

        Numeric columns are sorted differently and summed across all rows.
        Entries in numeric which do not appear in tile_columns are summed
        but not displayed.

        @param title_columns: OrderedDict of {label: title} for each column.
            If title is set to None, the label is reused as a title. Can also
            be provided as a list [label_1, (label_2, title_2), label_3] where
            missing titles are interpreted as None.
        @param numeric: list of columns (labels) which should be treated as
            numeric.
        """
        # convert more compact notations to OrderedDict
        if isinstance(title_columns, (list, tuple)):
            title_columns = OrderedDict(
                [(k[0], k[1]) if isinstance(k, tuple) else (k, None)
                 for k in title_columns])

        self.columns = title_columns
        self.totals = dict.fromkeys(numeric, 0)
        self.rows = []

    def add_row(self, row_cols, num_cols=None, empty=None):
        """
        Add row to the table and increment totals.

        Only add to totals if the corresponding entry is a number. None
        or missing values are replaced by a standard string.

        @param row_cols: dict of column labels and their values
        @param num_cols: dict of column labels and their values for numeric
            entries when the normal entry cannot be used for summation.
        @param empty: string to use when an entry is None.
        """
        num_cols = num_cols or {}
        empty = empty or '---'

        # handle missing and None values
        for col in self.columns:
            if row_cols.get(col) is None:  # 0 is allowed
                row_cols[col] = empty
        self.rows.append(row_cols)

        for col in self.totals.keys():
            if col in num_cols:  # num_cols.get(col) misses 0
                self.totals[col] += num_cols.get(col)
            elif is_number(row_cols.get(col)):
                self.totals[col] += row_cols.get(col)

    def add_wikitext_row(self, wikitext):
        """
        Add a pre-formatted row to the table.

        The provided text must include the initial "|-". The wikitext is not
        validated. No entry will be added to the sum.

        param wikitext: the wikitext for a single row.
        """
        if not isinstance(wikitext, (str, unicode)):
            raise ValueError('wikitext must be a (unicode) string')
        self.rows.append(wikitext.rstrip('\n'))

    def get_header_row(self):
        """Get a header row using appropriate titles, as wikitext."""
        titles = OrderedDict()
        for col, title in self.columns.iteritems():
            if title is None:
                title = col
            titles.update({title: col in self.totals})
        return common.table_header_row(titles)

    def get_summation_row(self):
        """Get a row summing all numeric columns, as wikitext."""
        summed_columns = {}
        for num, col in enumerate(self.columns.keys()):
            if col in self.totals:
                summed_columns[num] = self.totals.get(col)
        return common.table_bottom_row(len(self.columns), summed_columns)

    def get_sum(self, column=None):
        """
        Get the summation of a given column.

        @param column: the column to return. If non is specified all the sums
            are returned as a dict.
        """
        if column:
            return self.totals.get(column)
        else:
            return self.totals

    def to_wikitext(self, add_summation=True, inline=False):
        """
        Output the table as wikitext.

        @param add_summation: Whether to add a summation row at the end.
        @param inline: whether to output each row on one line as oposed to one
            line per cell. Note that this has no effect on the header and
            summation rows.
        """
        delimiter = '\n'
        if inline:
            delimiter = '|'
        text = self.get_header_row()
        for row in self.rows:
            if not isinstance(row, dict):
                text += row
            else:
                text += '|-\n'
                text += delimiter.join([
                    '| {} '.format(row.get(col))
                    for col in self.columns.keys()])
            text += '\n'
        if add_summation:
            text += self.get_summation_row()
        else:
            text += '|}\n'
        return text


def is_number(value):
    """
    Check if the given value is a number.

    @param value: The value to check
    @type value: str, or int
    @return bool
    """
    try:
        float(value)
        return True
    except (ValueError, TypeError):
        return False

# @todo: move common.table_header_row and common.table_bottom_row here
