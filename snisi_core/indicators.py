#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging
import copy
import numpy
import uuid
from functools import wraps

from py3compat import text_type, implements_to_string
from snisi_core.models.Reporting import SNISIReport, ExpectedReporting
from snisi_tools.misc import class_str

logger = logging.getLogger(__name__)


def humanize_value(data, is_expected=True, is_missing=False,
                   is_ratio=False, is_yesno=False, should_yesno=False,
                   float_precision=2):
    float_fmt = "{0:." + text_type(float_precision) + "f}"
    zero_end = '.' + ''.zfill(float_precision)

    if not is_expected:
        return "n/a"
    if is_missing:
        return "-"
    t = type(data)
    v = data
    if t is int or t is long:
        v = data
    if t is float:
        v = float_fmt.format(data)
        if v.endswith(zero_end):
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

    GOOD = 'indicator-good'
    WARNING = 'indicator-warning'
    BAD = 'indicator-bad'
    BLANK = 'indicator-blank'

    SNISI_INDICATOR = True
    INDIVIDUAL_CLS = SNISIReport
    AGGREGATED_CLS = SNISIReport

    name = None

    # Fixed Data Reports
    fixed_period = None
    fixed_entity = None

    # data represent a ratio (percentage)
    is_ratio = False

    # include to the list of-geo-friendly incicators ?
    is_geo_friendly = False
    geo_section = None

    # data can be represented as Y/N value
    is_yesno = False

    # whether indicator has a meta value for CSS
    raise_class = False

    # precision of float for values
    float_precision = 2

    CLONABLE_PROPS = [
        'is_ratio', 'is_yesno', 'raise_class', 'get_class',
        'is_geo_friendly', 'geo_section']

    def __init__(self, period=None, entity=None, expected=None):

        self._data = None
        self._computed = False
        self._is_not_expected = False
        self._is_missing = False

        self._period = self.fixed_period or period
        self._entity = self.fixed_entity or entity
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

    def get_fake(self, adict):
        ind = FakeIndicator(adict)
        for prop in self.CLONABLE_PROPS:
            setattr(ind, prop, getattr(self, prop))
        return ind

    def get_class(self):
        if self.is_missing or not self.is_expected:
            return ""
        return self._get_class()

    def _get_class(self):
        return ""

    def get_numerator(self):
        return None

    def get_denominator(self):
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
        if self.is_ratio:
            num = self.get_numerator()
            denom = self.get_denominator()
            if num is None or denom is None:
                raise DataIsMissing
            try:
                return num / denom
            except ZeroDivisionError:
                return 0

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
        except (DataIsMissing, AttributeError):
            self._data = None
            self._is_missing = True
        except ZeroDivisionError:
            self._data = 0
        except Exception as e:
            logger.error(e)
            logger.exception(e)
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
                              should_yesno=self.should_yesno(),
                              float_precision=self.float_precision)

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
    report_sub_field = None

    def _compute(self):
        if self.report_sub_field:
            return getattr(getattr(self.report, self.report_field),
                           self.report_sub_field)
        return getattr(self.report, self.report_field)


class FakeIndicator(dict):

    is_missing = False
    is_expected = True

    @property
    def data(self):
        return self['data']

    @property
    def human(self):
        return self['human']


class IndicatorTableMixin(object):

    def get_total_for_ratio(self, line_index):
        entity = self.entities[0]
        numerators = []
        denominators = []

        for period in self.periods:
            indic = self.INDICATORS[line_index](entity=entity, period=period)
            try:
                n = indic.get_numerator()
                if n is not None:
                    numerators.append(n)

                d = indic.get_denominator()
                if d is not None:
                    denominators.append(d)
            except (DataNotExpected, DataIsMissing):
                pass
        try:
            d = sum(numerators) / sum(denominators)
        except ZeroDivisionError:
            d = 0
        except Exception as e:
            logger.exception(e)
            d = None
        return FakeIndicator({
            'human': humanize_value(None if d is None else d * 100,
                                    is_ratio=True),
            'data': d
        })

    def get_total_for(self, line_index):
        if self.INDICATORS[line_index].is_ratio:
            return self.get_total_for_ratio(line_index)

        d = sum([self.data_for(line_index, col).data
                 for col in range(0, self.nb_cols() - 1)
                 if not self.data_for(line_index, col).is_missing
                 and self.data_for(line_index, col).is_expected])
        return self.data_for(line_index, col).get_fake({
            'human': humanize_value(d),
            'data': d
        })

    def rotate_labels(self):
        if self.rotate_many_labels:
            return self.nb_lines() > self.max_nonrotated_labels
        return False


class IndicatorTable(IndicatorTableMixin):

    INDICATORS = []
    add_percentage = False  # add % columns for each period
    is_percentage = False  # values are ratios and should be formatted as %
    add_total = False  # add a total column
    as_percentage = False  # only renders percentages
    multiple_axis = False
    on_descendants = False

    graph_type = 'column'
    rendering_type = 'table'
    graph_stacking = False
    is_entity_indicator = False
    use_advanced_rendering = False

    rotate_many_labels = True
    max_nonrotated_labels = 4

    def __init__(self, entity, periods, **kwargs):
        self.entity = entity
        self.periods = periods

        for key, value in kwargs.items():
            setattr(self, key, value)

        self._entities = self.get_descendants()
        self._data = {}
        self._computed = False

        if not len(self.INDICATORS):
            self.INDICATORS = self.build_indicators()

    def get_descendants(self):
        return [self.entity]

    @property
    def entities(self):
        if self.on_descendants:
            return self.descendants
        else:
            return [self.entity]

    def build_indicators(self):
        return []

    @property
    def descendants(self):
        return self._entities

    @property
    def show_as_percentage(self):
        return self.as_percentage or self.is_percentage

    def compute(self):
        line_index = 0
        for indicator_idx, indicator_cls in enumerate(self.INDICATORS):

            for entity in self.entities:
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
            return len(self.INDICATORS) * len(self.entities)
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

    # def get_total_for(self, line_index):
    #     if self.INDICATORS[line_index].is_ratio:
    #         return self.get_total_for_ratio(line_index)

    #     d = sum([self.data_for(line_index, col).data
    #              for col in range(0, self.nb_cols() - 1)
    #              if not self.data_for(line_index, col).is_missing
    #              and self.data_for(line_index, col).is_expected])
    #     return self.data_for(line_index, col).get_fake({
    #         'human': humanize_value(d),
    #         'data': d
    #     })

    # def get_total_for_ratio(self, line_index):
    #     entity = self.entities[0]
    #     numerators = []
    #     denominators = []

    #     for period in self.periods:
    #         indic = self.INDICATORS[line_index](entity=entity, period=period)
    #         try:
    #             n = indic.get_numerator()
    #             if n is not None:
    #                 numerators.append(n)

    #             d = indic.get_denominator()
    #             if d is not None:
    #                 denominators.append(d)
    #         except (DataNotExpected, DataIsMissing):
    #             pass
    #     try:
    #         d = sum(numerators) / sum(denominators)
    #     except ZeroDivisionError:
    #         d = 0
    #     except Exception as e:
    #         logger.exception(e)
    #         d = None
    #     return FakeIndicator({
    #         'human': humanize_value(None if d is None else d * 100,
    #                                 is_ratio=True),
    #         'data': d
    #     })

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
        # indic_ref_index = getattr(indic, '_reference_index', 0)
        if is_reference:
            return line_index

        ref_index = line_index - len(self.entities)
        if ref_index < 0:
            ref_index = 0
        return ref_index

    def get_percentage_value_for(self, line_index, column_index,
                                 as_human=False):
        numerator = self.data_for(line_index, column_index).data
        denominator = self.data_for(
            self.get_reference_line_for(line_index), column_index).data
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
                line_index = int(numpy.floor(line_index / len(self.entities)))
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

    def em_lines(self):
        return [index for index, indic in enumerate(self.INDICATORS)
                if getattr(indic, '_is_em', False)]

    def get_line_label_as_indic_for(self, line_index):
        return FakeIndicator({
            'data': self.get_line_label_for(line_index),
            'human': self.get_line_label_for(line_index)})

    def render_line(self,
                    line_index,
                    as_human=False,
                    with_labels=False,
                    as_period_tuple=False,
                    as_indic=False):
        cols = []
        if with_labels:
            if as_indic:
                cols.append(self.get_line_label_as_indic_for(line_index))
            else:
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

            # period_tuple is used for graphs so we can loop
            # on series with dated values
            if as_period_tuple:
                cols.append((self.get_period_for(column_index), data))
            elif as_indic:
                cols.append(indic)
            else:
                cols.append(data)

            # add percentage columns is requested
            if self.add_percentage:
                if not self.add_total or \
                        not column_index == self.total_col_index():
                    if indic.is_missing or not indic.is_expected:
                        cols.append(None)
                    else:
                        cols.append(
                            self.get_percentage_value_for(
                                line_index, column_index, as_human=as_human))

        return cols

    def render(self, as_human=False, with_labels=False, as_indic=False):
        lines = []
        for line_index in range(0, self.nb_lines()):
            lines.append(self.render_line(line_index,
                                          as_human=as_human,
                                          as_indic=as_indic,
                                          with_labels=with_labels))
        return lines

    def render_with_labels(self, as_human=False):
        return self.render(with_labels=True, as_human=as_human)

    def render_with_labels_human(self, as_human=True):
        return self.render(as_human=as_human, with_labels=True)

    def render_with_labels_raw(self):
        return self.render(as_human=False, with_labels=True, as_indic=True)

    def last_period(self):
        try:
            return self.periods[-1]
        except IndexError:
            return None

    def render_for_graph(self):
        return [
            {'label': self.get_line_label_for(idx),
             'data': self.render_line(idx, as_period_tuple=True),
             'yAxis': getattr(
                self.INDICATORS[self.fixed_line_index(idx)], '_yaxis', 0)}
            for idx in range(0, self.nb_lines())
            if not getattr(
                self.INDICATORS[self.fixed_line_index(idx)],
                '_is_hidden', False)]


def ref_is(index=0):
    """ decorator setting the percentage denominator of an indicator.

        index is the index of the line in the table  """
    def outer_wrapper(func, *args, **kwargs):
        nfunc = type(str('{}_{}'.format(func.__name__, uuid.uuid4().hex)),
                     func.__bases__, dict(func.__dict__))
        nfunc._is_reference = False
        nfunc._reference_index = index

        @wraps(nfunc)
        def wrapper(self, *args, **kwargs):
            return nfunc(*args, **kwargs)
        return nfunc
    return outer_wrapper


def yAxis(index=0):
    """ decorator setting the Highcharts yAxis of an indicator.

        index is the index of the line in the table's multiple_index array  """
    def outer_wrapper(func, *args, **kwargs):
        nfunc = type(str('{}_{}'.format(func.__name__, uuid.uuid4().hex)),
                     func.__bases__, dict(func.__dict__))
        # nfunc._is_specified_yaxis = False
        nfunc._yaxis = index

        @wraps(nfunc)
        def wrapper(self, *args, **kwargs):
            return nfunc(*args, **kwargs)
        return nfunc
    return outer_wrapper


def is_ref(func):
    """ decorator marking indicator a reference (percent will always be 1) """
    nfunc = type(str('{}_{}'.format(func.__name__, uuid.uuid4().hex)),
                 func.__bases__, dict(func.__dict__))
    nfunc._is_reference = True

    @wraps(nfunc)
    def wrapper(self, *args, **kwargs):
        return nfunc(*args, **kwargs)
    return nfunc


def hide(func):
    """ decorator marking indicator a reference (percent will always be 1) """
    nfunc = type(str('{}_{}'.format(func.__name__, uuid.uuid4().hex)),
                 func.__bases__, dict(func.__dict__))
    nfunc._is_hidden = True

    @wraps(nfunc)
    def wrapper(self, *args, **kwargs):
        return nfunc(*args, **kwargs)
    return nfunc


def em(func):
    """ decorator marking indicator a to be emphased (bold?) """
    nfunc = type(str('{}_{}'.format(func.__name__, uuid.uuid4().hex)),
                 func.__bases__, dict(func.__dict__))
    nfunc._is_em = True

    @wraps(nfunc)
    def wrapper(self, *args, **kwargs):
        return nfunc(*args, **kwargs)
    return nfunc


def gen_report_indicator(field,
                         name=None,
                         report_cls=None,
                         base_indicator_cls=Indicator):

    class GenericReportIndicator(ReportDataMixin, base_indicator_cls):
        pass

    cls = copy.copy(GenericReportIndicator)
    cls.report_field = field
    cls.name = name if name is not None else report_cls.field_name(field) \
        if report_cls is not None else None
    return cls


class SummaryForEntitiesTable(IndicatorTableMixin):
    """ Special IndicatorTable adapatation for Graph over children's

        Not a complete drop-in replacement.
        Instead of looping through periods to display per-entity
        variation of data over time

        it loops through entities (health children is default)
        and displays a sum of data for the periods """

    name = None
    title = None
    caption = None
    rendering_type = 'graph'
    graph_type = 'column'
    is_entity_indicator = True
    INDICATORS = []

    def __init__(self, entity, periods, **kwargs):
        self.entity = entity
        self.periods = periods

        for key, value in kwargs.items():
            setattr(self, key, value)

        self._entities = self.get_descendants()
        self._data = {}
        self._computed = False

    # override plz
    def get_descendants(self):
        return sorted(self.entity.casted().get_health_children(),
                      key=lambda x: x.name)

    @property
    def entities(self):
        return self._entities

    def compute(self):
        for indicator_idx, indicator_cls in enumerate(self.INDICATORS):
            for entity_idx, entity in enumerate(self.entities):
                self._data[(indicator_idx, entity_idx)] = \
                    self.compute_data_for(
                        entity=entity, periods=self.periods,
                        indicator_cls=indicator_cls)

        self._computed = True
        return self._data

    def compute_data_for(cls, entity, periods, indicator_cls):
        return FakeIndicator({
            'data': cls.compute_sum_data_for(entity, periods, indicator_cls)})

    def compute_sum_data_for(cls, entity, periods, indicator_cls):
        if indicator_cls.is_ratio:
            return cls.compute_sum_data_for_ratio(
                entity, periods, indicator_cls).data * 100
        return sum([d for d in [
            indicator_cls(entity=entity, period=period).data
            for period in periods
        ] if d is not None])

    def compute_sum_data_for_ratio(cls, entity, periods, indicator_cls):
        entity = entity
        numerators = []
        denominators = []

        for period in periods:
            indic = indicator_cls(entity=entity, period=period)
            try:
                n = indic.get_numerator()
                if n is not None:
                    numerators.append(n)

                d = indic.get_denominator()
                if d is not None:
                    denominators.append(d)
            except (DataNotExpected, DataIsMissing):
                pass
        try:
            d = sum(numerators) / sum(denominators)
        except ZeroDivisionError:
            d = 0
        except Exception as e:
            logger.exception(e)
            d = None
        return FakeIndicator({
            'human': humanize_value(None if d is None else d * 100,
                                    is_ratio=True),
            'data': d
        })

    # def get_total_for(self, line_index):
    #     if self.INDICATORS[line_index].is_ratio:
    #         return self.get_total_for_ratio(line_index)

    #     d = sum([self.data_for(line_index, col).data
    #              for col in range(0, self.nb_cols() - 1)
    #              if not self.data_for(line_index, col).is_missing
    #              and self.data_for(line_index, col).is_expected])
    #     return self.data_for(line_index, col).get_fake({
    #         'human': humanize_value(d),
    #         'data': d
    #     })

    @property
    def computed(self):
        return self._computed

    @property
    def data(self):
        if self.computed:
            return self._data
        return self.compute()

    def data_for(self, lidx, cidx):
        return self.data[(lidx, cidx)]

    def nb_lines(self):
        return len(self.INDICATORS)

    def nb_cols(self):
        return len(self.entities)

    def get_column_label_for(self, idx):
        return self.entities[idx].name

    def get_column_for(self, idx):
        return self.entities[idx]

    def get_line_label_for(self, idx):
        return self.INDICATORS[idx].name

    def render_line(self, line_index):
        cols = []
        for column_index in range(0, self.nb_cols()):
            indic = self.data_for(line_index, column_index)
            data = getattr(indic, 'data')

            cols.append((self.get_column_for(column_index), data))
            # cols.append(data)

        return cols

    def render_for_graph(self):
        return [
            {'label': self.get_line_label_for(idx),
             'data': self.render_line(idx),
             'yAxis': getattr(self.INDICATORS[idx], '_yaxis', None)}
            for idx in range(0, self.nb_lines())
        ]

    @property
    def show_as_percentage(self):
        return self.is_percentage

    def last_period(self):
        try:
            return self.periods[-1]
        except IndexError:
            return None

    def rotate_labels(self):
        return True

