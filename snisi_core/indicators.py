#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
from functools import wraps
import copy
import numpy

from py3compat import text_type, implements_to_string
from snisi_core.models.Reporting import SNISIReport, ExpectedReporting
from snisi_tools.misc import class_str

def humanize_value(data, is_expected=True, is_missing=False,
                   is_ratio=False, is_yesno=False, should_yesno=False):
    if not is_expected:
        return "n/a"
    if is_missing:
        return "-"
    t = type(data)
    v = data
    if t is int:
        v = data
    if t is float or t is long:
        v = "{0:.2f}".format(data)
        if v.endswith('.00'):
            v = int(float(v))
    if is_yesno and should_yesno:
        v = "OUI" if bool(v) else "NON"
    if is_ratio and not (is_yesno and should_yesno):
        v = "{}%".format(v)
    return text_type(v)


class DataNotExpected(Exception):
    ''' No data for request but none was expected '''
    pass


class DataIsMissing(Exception):
    ''' Data was expected but not received '''
    pass


@implements_to_string
class Indicator(object):

    SNISI_INDICATOR = True
    INDIVIDUAL_CLS = SNISIReport
    AGGREGATED_CLS = SNISIReport

    name = None

    # data represent a ratio (percentage)
    is_ratio = False

    # include to the list of-geo-friendly incicators ?
    is_geo_friendly = False
    geo_section = None

    # data can be represented as Y/N value
    is_yesno = False

    def __init__(self, period=None, entity=None, expected=None):

        self._data = None
        self._computed = False
        self._is_not_expected = False
        self._is_missing = False

        self._period = period
        self._entity = entity
        if expected is None:
            self._expected = self.get_expected_reporting()
        else:
            self._expected = expected

    def get_expected_reporting(self):
        qs = ExpectedReporting.objects.filter(period=self.period,
                                              entity=self.entity)
        if self.entity.type.slug in ('health_center', 'vfq'):
            qsi = qs.filter(report_class__cls=class_str(self.INDIVIDUAL_CLS))
            if qsi.count() == 1:
                return qsi.get()
        qsa = qs.filter(report_class__cls=class_str(self.AGGREGATED_CLS))
        if qsa.count() == 1:
            return qsa.get()
        return None

    @classmethod
    def clone_from(cls, indicator_instance):
        return cls(period=indicator_instance.period,
                   entity=indicator_instance.entity,
                   expected=indicator_instance.expected)

    @classmethod
    def spec(cls):
        return {'slug': cls.__name__,
                'name': cls.name,
                'is_ratio': cls.is_ratio,
                'is_geo_friendly': cls.is_geo_friendly,
                'is_yesno': cls.is_yesno,
                'geo_section': cls.geo_section}

    @property
    def report(self):
        r = self.expected.arrived_report()
        if r is None:
            raise DataIsMissing
        return r

    @property
    def reports(self):
        return self.expected.arrived_reports.all()

    @property
    def period(self):
        return self._period

    @property
    def entity(self):
        return self._entity

    @property
    def is_expected(self):
        if not self.computed:
            self.compute()
        return not self._is_not_expected

    @property
    def is_missing(self):
        if not self.computed:
            self.compute()
        return self._is_missing

    @property
    def expected(self):
        if self._expected is None:
            raise DataNotExpected
        return self._expected

    def reset(self):
        self._computed = False
        return self.compute()

    def _compute(self):
        # overwrite. this returns the final value
        pass

    @classmethod
    def to_percentage(cls, value):
        return value * 100

    def compute(self):
        try:
            self.expected
            # self.report
            self._data = self._compute()
            if self.is_ratio:
                self._data = self.to_percentage(self._data)
        except DataNotExpected:
            self._data = None
            self._is_not_expected = True
        except DataIsMissing:
            self._data = None
            self._is_missing = True
        except Exception as e:
            import traceback
            print(e)
            print("".join(traceback.format_exc()))

            raise e

        self._computed = True
        return self._data

    @property
    def computed(self):
        return self._computed

    @property
    def data(self):
        if self.computed:
            return self._data
        return self.compute()

    @property
    def human(self):
        return humanize_value(self.data,
                              is_expected=self.is_expected,
                              is_missing=self.is_missing,
                              is_ratio=self.is_ratio,
                              is_yesno=self.is_yesno,
                              should_yesno=self.should_yesno())

    def divide(self, numerator, denominator):
        try:
            return numerator / denominator
        except ZeroDivisionError:
            return 0

    def __str__(self):
        return "{name}/{entity}/{period}".format(
            name=self.name,
            entity=self.entity,
            period=self.period)


class ReportDataMixin(object):
    """ shortcut for indicators which straighly reflects a field in model """
    report_field = None

    def _compute(self):
        return getattr(self.report, self.report_field)


class FakeIndicator(dict):

    @property
    def data(self):
        return self['data']

    @property
    def human(self):
        return self['human']



class IndicatorTable:

    INDICATORS = []
    add_percentage = False # add % columns for each period
    add_total = False # add a total column
    as_percentage = False # only renders percentages
    multiple_axis = False
    on_descendants = False

    graph_type = 'column'
    rendering_type = 'table'

    def __init__(self, entity, periods, **kwargs):
        self.entity = entity
        self.periods = periods

        for key, value in kwargs.items():
            setattr(self, key, value)

        self._entities = self.get_descendants()
        self._data = {}
        self._computed = False

    def get_descendants(self):
        return [self.entity]

    def compute(self):
        line_index = 0
        for indicator_idx, indicator_cls in enumerate(self.INDICATORS):

            for entity in self._entities:
                line_sum = 0
                for period_idx, period in enumerate(self.periods):
                    indicator = indicator_cls(entity=entity,
                                              period=period)
                    # indicator.data
                    try:
                        line_sum += indicator.data
                    except:
                        pass
                    self._data[(line_index, period_idx)] = indicator

                line_index += 1

        self._computed = True
        return self._data

    @property
    def computed(self):
        return self._computed

    @property
    def data(self):
        if self.computed:
            return self._data
        return self.compute()

    def nb_lines(self):
        if self.on_descendants:
            return len(self.INDICATORS) * len(self._entities)
        return len(self.INDICATORS)

    def nb_cols(self):
        return len(self.periods) + (1 if self.add_total else 0)

    def main_labels(self):
        l = []
        for p in self.periods:
            l.append(text_type(p))
        if self.add_total:
            l.append("TOTAL")
        return l

    def get_line(self, line_index):
        line_index = self.fixed_line_index(line_index)
        return self.INDICATORS[line_index]

    def get_total_for(self, line_index):
        d = sum([self.data_for(line_index, col).data for col in range(0, self.nb_cols() -1) if not self.data_for(line_index, col).is_missing and self.data_for(line_index, col).is_expected])
        return FakeIndicator({
            'human': humanize_value(d),
            'data': d
        })

    def data_for(self, line_index, column_index):
        if self.add_total and column_index == self.total_col_index():
            return self.get_total_for(line_index)
        return self.data[(line_index, column_index)]

    def get_reference_line_for(self, line_index):
        if not self.on_descendants:
            if getattr(self.get_line(line_index), '_is_reference', False):
                return line_index
            return getattr(self.get_line(line_index), '_reference_index', 0)

        fixed = self.fixed_line_index(line_index)
        indic = self.INDICATORS[fixed]
        is_reference = getattr(indic, '_is_reference', False)
        indic_ref_index = getattr(indic, '_reference_index', 0)
        if is_reference:
            return line_index

        ref_index = line_index - len(self._entities)
        if ref_index < 0:
            ref_index = 0
        return ref_index

    def get_percentage_value_for(self, line_index, column_index, as_human=False):
        numerator = self.data_for(line_index, column_index).data
        denominator = self.data_for(self.get_reference_line_for(line_index), column_index).data
        try:
            d = (numerator / denominator) * 100
        except:
            d = 0
        if not as_human:
            return d
        return humanize_value(d,
                              is_expected=True,
                              is_missing=False,
                              is_ratio=True,
                              is_yesno=False,
                              should_yesno=False)

    def has_sub_labels(self):
        return self.add_percentage

    def sub_labels(self):
        if not self.has_sub_labels():
            return None
        l = []
        for p in self.periods:
            l.append("Nbre")
            l.append("%")
        if self.add_total:
            l.append("Nbre")
        return l

    def fixed_line_index(self, line_index):
        if self.on_descendants:
            try:
                line_index = int(numpy.floor(line_index / len(self._entities)))
            except:
                line_index = 0
        if line_index < 0:
            line_index = 0
        return line_index

    def get_line_label_for(self, line_index):
        if self.on_descendants:
            data = self.data_for(line_index, 0)
            return "{} - {}".format(data.name, data.entity)
        else:
            return getattr(self.INDICATORS[line_index], 'name')

    def get_period_for(self, column_index):
        return self.periods[column_index]

    def total_col_index(self):
        return self.nb_cols() - 1

    def render_line(self,
                    line_index,
                    as_human=False,
                    with_labels=False,
                    as_period_tuple=False):
        cols = []
        if with_labels:
            cols.append(self.get_line_label_for(line_index))
        for column_index in range(0, self.nb_cols()):
            indic = self.data_for(line_index, column_index)

            # graphs might want only percentage value
            if self.as_percentage:
                if indic.is_missing or not indic.is_expected:
                    data = None
                else:
                    data = self.get_percentage_value_for(line_index,
                                                         column_index,
                                                         as_human=as_human)
            else:
                data = getattr(indic, 'human' if as_human else 'data')

            # period_tuple is used for graphs so we can loop on series with dated values
            if as_period_tuple:
                cols.append((self.get_period_for(column_index), data))
            else:
                cols.append(data)

            # add percentage columns is requested
            if self.add_percentage:
                if not self.add_total or not column_index == self.total_col_index():
                    if indic.is_missing or not indic.is_expected:
                        cols.append(None)
                    else:
                        cols.append(self.get_percentage_value_for(line_index,
                                                                  column_index,
                                                                  as_human=as_human))

        return cols

    def render(self, as_human=False, with_labels=False):
        lines = []
        for line_index in range(0, self.nb_lines()):
            lines.append(self.render_line(line_index,
                                          as_human=as_human,
                                          with_labels=with_labels))
        return lines

    def render_with_labels(self, as_human=False):
        return self.render(with_labels=True, as_human=as_human)

    def render_with_labels_human(self, as_human=True):
        return self.render(as_human=as_human, with_labels=True)

    def last_period(self):
        try:
            return self.periods[-1]
        except IndexError:
            return None

    def render_for_graph(self):
        return [
            {'label': self.get_line_label_for(idx),
             'data': self.render_line(idx, as_period_tuple=True)}
                for idx in range(0, self.nb_lines())
                if not getattr(self.INDICATORS[self.fixed_line_index(idx)], '_is_hidden', False)]


def ref_is(index=0):
    """ decorator setting the percentage denominator of an indicator.

        index is the index of the line in the table  """
    def outer_wrapper(func, *args, **kwargs):
        func._is_reference = False
        func._reference_index = index

        @wraps(func)
        def wrapper(self, *args, **kwargs):
            return func(*args, **kwargs)
        return func
    return outer_wrapper

def is_ref(func):
    """ decorator marking indicator a reference (percent will always be 1) """
    func._is_reference = True

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        return func(*args, **kwargs)
    return func


def hide(func):
    """ decorator marking indicator a reference (percent will always be 1) """
    func._is_hidden = True

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        return func(*args, **kwargs)
    return func


def gen_report_indicator(field,
                         name=None,
                         report_cls=None,
                         base_indicator_cls=Indicator):

    class GenericReportIndicator(ReportDataMixin, base_indicator_cls):
        pass


    cls = copy.copy(GenericReportIndicator)
    cls.report_field = field
    cls.name = name if name else report_cls.field_name(field) if report_cls is not None else None
    return cls
