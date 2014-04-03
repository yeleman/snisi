#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

from py3compat import text_type

from django.utils.translation import ugettext as _


class ReportingDataException(Exception):

    level = 'unknown'
    field = None
    message = None
    short_message = None
    extras = {}

    def __init__(self, message, field=None, short_message=None, extras={}):
        if field:
            self.field = field
        if message:
            self.message = message
        if short_message:
            self.short_message = message
        if len(extras.keys()):
            self.extras.update(extras)

        super(ReportingDataException, self).__init__(message or short_message)

    def add_extras(self, extras):
        self.extras.update(extras)

    def render(self, short=False):
        if short and self.short_message:
            return self.short
        return self.message


class ReportingDataWarning(ReportingDataException):
    level = 'warning'


class ReportingDataError(ReportingDataException):
    level = 'error'


class ReportingDataMissing(ReportingDataException):
    level = 'error'


class ReportingDataHolder(object):

    def __init__(self):
        self.fields = []
        self._data = {}
        self._feedbacks = []
        self._raised = None

    @property
    def data(self):
        return self._data

    def to_dict(self):
        return self.data

    def feed(self, **kwargs):
        self._data.update(kwargs)

    def set(self, key, value):
        self._data.update({key: value})

    def get(self, key, default=None, silent=False):
        if not key in self.data.keys():
            self.add_missing(_("Missing Data for {}").format(key),
                             blocking=not silent,
                             field=key)
        return self.data.get(key, default)

    def has(self, key, test_value=True):
        return key in self.data.keys() and \
            (self.data.get(key) is not None or not test_value)

    def add_warning(self, warning, **kwargs):
        if isinstance(warning, text_type):
            warning = ReportingDataWarning(warning, **kwargs)
        self._feedbacks.append(warning)

    def add_error(self, error, blocking=False, **kwargs):
        if isinstance(error, text_type):
            error = ReportingDataError(error, **kwargs)
        self._feedbacks.append(error)
        if blocking:
            raise error

    def add_missing(self, missing, blocking=False, **kwargs):
        if isinstance(missing, text_type):
            missing = ReportingDataMissing(missing, **kwargs)
        self._feedbacks.append(missing)
        if blocking:
            raise missing

    def _read(self):
        # override if you need to read data from a stream or anything.
        # useful for Excel Forms.
        pass

    def read(self):
        self._read()

    def _check(self, **options):
        # overrride to add checks here
        pass

    def _check_completeness(self, **options):
        # overrride to add completeness checks here
        pass

    def check_completeness(self, **options):
        try:
            self._check_completeness(**options)
        except ReportingDataException as raised:
            self._raised = raised
            if not raised in self._feedbacks:
                self._feedbacks.append(raised)

    def check(self, **options):
        try:
            self._read(**options)
            self._check_completeness(**options)
            self._check(**options)
        except ReportingDataException as raised:
            self._raised = raised
            if not raised in self._feedbacks:
                self._feedbacks.append(raised)

    def is_valid(self):
        return not len([1 for e in self.feedbacks if e.level == 'error'])

    def is_complete(self, *args, **kwargs):
        return not len([1 for e in self.feedbacks
                        if isinstance(e, ReportingDataMissing)])

    @property
    def raised(self):
        return self._raised

    @property
    def errors(self):
        return [self.raised] + [error for error in self._feedbacks
                                if isinstance(error, ReportingDataError)]

    @property
    def warnings(self):
        return [error for error in self._feedbacks
            if isinstance(error, ReportingDataWarning)]

    @property
    def missings(self):
        return [error for error in self._feedbacks
            if isinstance(error, ReportingDataMissing)]

    @property
    def feedbacks(self):
        return ([self.raised] if self.raised else []) \
            + [f for f in self._feedbacks if not f == self.raised]

    def render_feedbacks(self, sep="\n"):
        return sep.join([f.render() for f in self.feedbacks])


class ReportIntegrityChecker(ReportingDataHolder):
    pass
