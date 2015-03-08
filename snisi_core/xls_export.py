#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import StringIO


ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


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


def xl_col_width(cm):
    """ xlwt width for a given width in centimeters """
    return int(2770 / 2.29 * cm)


def xl_set_col_width(sheet, col, cm):
    """ change column width """
    sheet.col(col).width = xl_col_width(cm)


def xl_row_height(cm):
    """ xlwt height for a given height in centimeters """
    return int(342 / 0.6 * cm)


def xl_set_row_height(sheet, row, cm):
    """ change row height """
    sheet.row(row).height = xl_row_height(cm)
    sheet.row(row).height_mismatch = True


class ColorMatcher(object):
    """
    the source is in : http://www.archivum.info/python-excel@googlegroups.
        com/2012-09/00014/Re-(pyxl)-Re-Background-with-any-rgb-value.html

    Prior to Excel 2007, Excel only had color
    indexes, and that's all that xlwt supports.  Maybe this will help,
    though.  It use a ColorMatcher that takes an RGB input and tries to
    return the closest matching Excel color index:
    """

    def __init__(self):
        self.reset()

    def reset(self):
        self.unused_colors = set(self.xlwt_colors)
        # Never use black.
        self.unused_colors.discard((0, 0, 0))

    # Culled from a table at http://www.mvps.org/dmcritchie/excel/colors.htm
    xlwt_colors = [
        (0, 0, 0), (255, 255, 255), (255, 0, 0), (0, 255, 0),
        (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255),
        (0, 0, 0), (255, 255, 255), (255, 0, 0), (0, 255, 0),
        (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255),
        (128, 0, 0), (0, 128, 0), (0, 0, 128), (128, 128, 0),
        (128, 0, 128), (0, 128, 128), (192, 192, 192),
        (128, 128, 128), (153, 153, 255), (153, 51, 102),
        (255, 255, 204), (204, 255, 255), (102, 0, 102),
        (255, 128, 128), (0, 102, 204), (204, 204, 255),
        (0, 0, 128), (255, 0, 255), (255, 255, 0), (0, 255, 255),
        (128, 0, 128), (128, 0, 0), (0, 128, 128), (0, 0, 255),
        (0, 204, 255), (204, 255, 255), (204, 255, 204),
        (255, 255, 153), (153, 204, 255), (255, 153, 204),
        (204, 153, 255), (255, 204, 153), (51, 102, 255),
        (51, 204, 204), (153, 204, 0), (255, 204, 0), (255, 153, 0),
        (255, 102, 0), (102, 102, 153), (150, 150, 150),
        (0, 51, 102), (51, 153, 102), (0, 51, 0), (51, 51, 0),
        (153, 51, 0), (153, 51, 102), (51, 51, 153), (51, 51, 51)
    ]

    @staticmethod
    def color_distance(rgb1, rgb2):
        # Adapted from Colour metric by Thiadmer Riemersma,
        # http://www.compuphase.com/cmetric.htm
        rmean = (rgb1[0] + rgb2[0]) / 2
        r = rgb1[0] - rgb2[0]
        g = rgb1[1] - rgb2[1]
        b = rgb1[2] - rgb2[2]
        return (((512 + rmean) * r * r) / 256) + 4 * g * g \
            + (((767 - rmean) * b * b) / 256)

    def match_color_index(self, color):
        """Takes an "R,G,B" string or wx.Color and returns a matching xlwt
        color.
        """
        if isinstance(color, int):
            return color
        if color:
            if isinstance(color, basestring):
                rgb = map(int, color.split(','))
            else:
                rgb = color.Get()
            distances = [self.color_distance(rgb, x) for x in self.xlwt_colors]
            result = distances.index(min(distances))
            self.unused_colors.discard(self.xlwt_colors[result])
            return result

    def get_unused_color(self):
        """Returns an xlwt color index that has not been previously returned by
        this instance.  Attempts to maximize the distance between the color and
        all previously used colors.
        """
        if not self.unused_colors:
            # If we somehow run out of colors, reset the color matcher.
            self.reset()
        used_colors = [c for c in self.xlwt_colors
                       if c not in self.unused_colors]
        result_color = max(self.unused_colors,
                           key=lambda c: min([self.color_distance(c, c2)
                                              for c2 in used_colors]))
        result_index = self.xlwt_colors.index(result_color)
        self.unused_colors.discard(result_color)
        return result_index
