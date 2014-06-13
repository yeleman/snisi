#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import StringIO


def default_xls_export(report):
    return StringIO.StringIO()


def xls_get_cell_repr(outSheet, colIndex, rowIndex):
    """ HACK: Extract the internal xlwt cell representation. """
    row = outSheet._Worksheet__rows.get(rowIndex)
    if not row:
        return None
    cell = row._Row__cells.get(colIndex)
    return cell


def xls_update_value_only(outSheet, col, row, value):
    """ Change cell value without changing formatting. """
    previousCell = xls_get_cell_repr(outSheet, col, row)
    outSheet.write(row, col, value)
    if previousCell:
        newCell = xls_get_cell_repr(outSheet, col, row)
        if newCell:
            newCell.xf_idx = previousCell.xf_idx
