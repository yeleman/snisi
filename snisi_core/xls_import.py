#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import re
import logging

import xlrd
from py3compat import text_type

from snisi_core.integrity import ReportingDataHolder
from snisi_tools import type_converters

logger = logging.getLogger(__name__)


class ExcelFormField(object):
    """ A field in an Excel form represented by its coordinates """

    def __init__(self, coord, type=None, name=None,
                 sheet=None,
                 cast_args=None, attr=None, *args, **kwargs):
        self.coord = coord
        self.type = type
        self.name = name
        self.sheet = sheet
        self.attr = attr
        self.cast_args = cast_args
        self.args = args
        self.kwargs = kwargs

    def display_name(self):
        if self.name:
            return self.name
        return self.coord

    def convert_data(self, value):
        """ converted data from type property """
        if not self.type:
            return value
        if self.cast_args:
            return self.type(value, self.cast_args)
        else:
            return self.type(value)


class ExcelForm(ReportingDataHolder):

    """ A Form in an Excel File """

    _mapping = {None: {}}
    version = None
    domain = None

    def __init__(self, filepath, sheet=None, version=None):

        super(ExcelForm, self).__init__()

        if version:
            self.version = version

        self.filepath = filepath
        self.sheet = sheet
        self.book = None

    def _read(self, sheet=None):
        """ parses all fields in mapping and stores converted data """

        if not sheet:
            sheet = self.sheet

        try:
            self.book = xlrd.open_workbook(self.filepath)
            if isinstance(sheet, text_type):
                self.ws = self.book.sheet_by_name(sheet)
            elif isinstance(sheet, int):
                self.ws = self.book.sheets()[sheet]
            else:
                self.ws = self.book.sheets()[0]
        except Exception as e:
            logger.warning("Unable to read Excel Uploaded file {path}. "
                           "Raised {e}".format(path=self.filepath, e=e))
            self.add_error("Impossible d'ouvrir le masque de saisie. "
                           "Le fichier est corrompu ou a été modifié.")
            return

        for field_id, field in self.mapping().items():
            self.map_field(field, field_id)

    def mapping(self):
        """ dict mapping of the current version """
        if self.version:
            return self._mapping[self.version]
        else:
            return self._mapping[self._mapping.keys()[0]]

    def data_for_coord(self, coord, sheet=None):
        """ raw data from Excel coordinates """
        if sheet is None:
            ws = self.ws
        else:
            ws = self.book.sheet_by_name(sheet)
        XLS_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        letter, line = re.match(r'([a-zA-Z]+)([0-9]+)', coord).groups()
        try:
            row = int(line) - 1
            column = XLS_LETTERS.index(letter.upper())
            return ws.row_values(row)[column]
        except:
            self.add_missing("Aucune donnée pour le champ “{coord}”"
                             .format(coord=coord), blocking=True, field=coord)
            return None

    def field_name(self, variable):
        """ name of field from slug """
        return self.mapping()[variable].display_name()

    def map_field(self, field, variable):
        """ retrieve and store data from excel to mapping for field+slug """
        # raw data
        fdata = self.data_for_coord(field.coord, field.sheet)
        try:
            self.set(variable, field.convert_data(fdata))
        except ValueError as e:
            # field is blank
            if len(type_converters.clean_str(fdata)) == 0:
                self.set(variable, None)
            else:
                self.value_error(fdata, field, variable, e)

    def value_error(self, data, field, variable, exception):
        """ adds an error if data is not valid """
        self.add_error("“{data}” n'est pas une valeur correcte "
                       "pour le champ “{field}”"
                       .format(data=data, field=field.display_name()))

    @classmethod
    def get_domain(cls):
        return cls.domain
