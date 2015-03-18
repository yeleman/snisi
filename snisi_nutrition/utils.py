#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging
from collections import OrderedDict

from snisi_core.indicators import Indicator
from snisi_core.models.Reporting import ExpectedReporting, ReportClass
from snisi_core.models.Periods import MonthPeriod
from snisi_core.models.Entities import Entity
from snisi_nutrition.models.URENI import AggURENINutritionR, URENINutritionR
from snisi_nutrition.models.URENAS import AggURENASNutritionR, URENASNutritionR
from snisi_nutrition.models.URENAM import AggURENAMNutritionR, URENAMNutritionR
from snisi_nutrition.models.Stocks import AggNutritionStocksR, NutritionStocksR
from snisi_nutrition.models.Monthly import AggNutritionR, NutritionR
from snisi_nutrition.models.Caseload import ExpectedCaseload

logger = logging.getLogger(__name__)
report_classes = [
    ReportClass.get_or_none("nutrition_monthly_routine"),
    ReportClass.get_or_none("nutrition_monthly_routine_aggregated")]
sort_by_name = lambda x: x.name


def compute_sum_value(entity, periods, field, sub_report=None):

    rcls = NutritionR if entity.type.slug == 'health_center' else AggNutritionR
    reports = rcls.objects.filter(
        entity=entity, period__in=periods)

    def get(sub_report, field):
        if sub_report is None:
            return sum([getattr(r, field, 0) for r in reports])
        return sum([getattr(getattr(r, '{}_report'.format(sub_report)),
                            field, 0) for r in reports])

    return get(sub_report, field)


def generate_sum_data_for(entity, periods):

    is_hc = False

    if entity.type.slug == 'health_center':
        is_hc = True
        rcls = NutritionR
        urenamrcls = URENAMNutritionR
        urenasrcls = URENASNutritionR
        urenircls = URENINutritionR
        stocksrcls = NutritionStocksR
    else:
        urenamrcls = AggURENAMNutritionR
        urenasrcls = AggURENASNutritionR
        urenircls = AggURENINutritionR
        stocksrcls = AggNutritionStocksR

    rcls = NutritionR if entity.type.slug == 'health_center' else AggNutritionR
    reports = rcls.objects.filter(
        entity=entity, period__in=periods)

    def get(sub_report, field):
        if sub_report is None:
            return sum([getattr(r, field, 0) for r in reports])
        return sum([getattr(getattr(r, '{}_report'.format(sub_report)),
                            field, 0) for r in reports])

    def recalc_rate(data, field_name):
        x = field_name.rsplit('_', 2)
        if len(x) <= 2:
            prefix = ''
            fname = x[0]
        else:
            prefix = '{}_'.format(x[0])
            fname = x[1]
        total_out = data['{}total_out'.format(prefix)]
        not_responding = data['{}not_responding'.format(prefix)]
        out_base = total_out - not_responding
        try:
            return data['{}{}'.format(prefix, fname)] / out_base
        except ZeroDivisionError:
            return 0

    d = {'ureni_report': {},
         'urenas_report': {},
         'urenam_report': {},
         'stocks_report': {},
         'entity': {'slug': entity.slug, 'name': entity.name}}

    if not is_hc or entity.has_ureni:
        for field in urenircls.all_uren_fields():
            d['ureni_report'][field] = get('ureni', field)
        # recalc rates as it's not a sum
        for field in urenircls.all_uren_fields():
            if field.endswith('_rate'):
                d['ureni_report'][field] = recalc_rate(d['ureni_report'],
                                                       field)

    if not is_hc or entity.has_urenas:
        for field in urenasrcls.all_uren_fields():
            d['urenas_report'][field] = get('urenas', field)
        # recalc rates as it's not a sum
        for field in urenasrcls.all_uren_fields():
            if field.endswith('_rate'):
                d['urenas_report'][field] = recalc_rate(d['urenas_report'],
                                                        field)

    if not is_hc or entity.has_urenam:
        for field in urenamrcls.all_uren_fields():
            d['urenam_report'][field] = get('urenam', field)
        # recalc rates as it's not a sum
        for field in urenamrcls.all_uren_fields():
            if field.endswith('_rate'):
                d['urenam_report'][field] = recalc_rate(d['urenam_report'],
                                                        field)

    for field in stocksrcls.data_fields():
        d['stocks_report'][field] = get('stocks', field)

    for field in rcls.all_uren_fields():
        d[field] = get(None, field)

    return d


def generate_sum_data_table_for(entity, periods):

    sl = ['health_area', 'region', 'cercle', 'commune', 'vfq']
    entities = set([
        Entity.get_or_none(exp['entity'])
        for exp in ExpectedReporting.objects.filter(
            period__in=periods, report_class__in=report_classes,
            entity__slug__in=[
                e.slug for e in
                entity.casted().get_natural_children(sl)]).values('entity')])

    data = {
        centity.slug: generate_sum_data_for(entity=centity, periods=periods)
        for centity in entities
    }

    data.update(generate_sum_data_for(entity=entity, periods=periods))

    return data


def generate_entity_period_matrix(entity, period, months_data=None):
    # TOTAL sum of all periods
    is_total = isinstance(period, list)

    if is_total:
        periods = period
        rcls = NutritionR if entity.type.slug == 'health_center' \
            else AggNutritionR
        reports = rcls.objects.filter(entity=entity, period__in=periods)
        expecteds = ExpectedReporting.objects.filter(
            entity=entity, period__in=period, report_class__in=report_classes)
        expected = {}
        report = {}
    else:
        reports = []
        expecteds = ExpectedReporting.objects.filter(
            entity=entity, period=period, report_class__in=report_classes)
        try:
            expected = expecteds.get()
            report = expected.arrived_report()
        except ExpectedReporting.DoesNotExist:
            expected = None
            report = None

    def get(r, sub_report, field):
        if r is None:
            return 0

        if not is_total:
            if sub_report is None:
                return getattr(r, field, 0) or 0
            return getattr(getattr(r, '{}_report'.format(sub_report)),
                           field, 0) or 0

        if sub_report is None:
            return sum([getattr(report, field, 0) or 0 for report in reports])
        return sum([getattr(getattr(report, '{}_report'.format(sub_report)),
                            field, 0) or 0 for report in reports])

    def pc(a, b):
        try:
            return a / b
        except ZeroDivisionError:
            return 0

    def rpc(data, field):
        return pc(data["{}__num".format(field)],
                  data["{}__denum".format(field)])

    def gc(value, slug):
        blank = Indicator.BLANK
        good = Indicator.GOOD
        warning = Indicator.WARNING
        bad = Indicator.BAD
        if slug == 'caseload':
            return blank if value >= 0.5 else bad
        elif slug == 'healed':
            return good if value >= 0.75 else bad
        elif slug == 'deceased':
            return good if value < 0.10 else bad
        elif slug == 'abandon':
            return good if value < 0.15 else bad
        elif slug == 'ureni':
            return good if value >= 0.10 and value <= 0.20 else bad
        elif slug == 'urenas':
            return good if value >= 0.80 and value <= 0.90 else bad
        return ''

    if not expecteds.count() or (not is_total and expected is None):
        return {'expected': None}

    def perf_indic_denum(report, prefix, field):
        if report is None:
            return 0
        if is_total:
            return sum([data.get('{}{}_rate__denum'.format(prefix, field), 0)
                        for data in months_data.values()])

        if 'sam_ureni_' in prefix:
            report = report.ureni_report
            prefix = prefix.replace('sam_ureni_comp_', '') \
                .replace('sam_ureni_', '')

        if 'sam_urenas_' in prefix:
            report = report.ureni_report
            prefix = prefix.replace('sam_urenas_comp_', '') \
                .replace('sam_urenas_', '')

        tof = '{}total_out'.format(prefix) \
            if prefix is not None else 'total_out'
        nof = '{}not_responding'.format(prefix) \
            if prefix is not None else 'not_responding'

        if isinstance(report, dict):
            dtof = report.get(tof, 0)
            dnof = report.get(nof, 0)
        else:
            dtof = getattr(report, tof, 0)
            dnof = getattr(report, nof, 0)
        return dtof - dnof

    def perf_indic_num(report, prefix, field):
        if report is None:
            return 0

        if is_total:
            return sum([data.get('{}{}_rate__num'.format(prefix, field), 0)
                        for data in months_data.values()])

        if 'sam_ureni_' in prefix:
            report = report.ureni_report
            prefix = prefix.replace('sam_ureni_comp_', '') \
                .replace('sam_ureni_', '')

        if 'sam_urenas_' in prefix:
            report = report.ureni_report
            prefix = prefix.replace('sam_urenas_comp_', '') \
                .replace('sam_urenas_', '')

        f = '{}{}'.format(prefix, field) \
            if prefix != 'all' else '{}'.format(field)
        if isinstance(report, dict):
            d = data.get(f)
        else:
            d = getattr(report, f)
        return d

    data = {
        'expected': expected,
        'report': report,
        'nb_expected': get(report, None, 'nb_source_reports_expected'),
        'nb_arrived': get(report, None, 'nb_source_reports_arrived'),
    }
    data['ureni_nb_expected'] = get(report, 'ureni',
                                    'nb_source_reports_expected')
    data['ureni_nb_arrived'] = get(report, 'ureni',
                                   'nb_source_reports_arrived')

    data['ureni_completion_rate__num'] = data['ureni_nb_arrived']
    data['ureni_completion_rate__denum'] = data['ureni_nb_expected']

    data['ureni_completion_rate'] = rpc(data, 'ureni_completion_rate')
    # data['ureni_nb_arrived'], data['ureni_nb_expected'])

    data['urenas_nb_expected'] = get(report, 'urenas',
                                     'nb_source_reports_expected')
    data['urenas_nb_arrived'] = get(report, 'urenas',
                                    'nb_source_reports_arrived')

    data['urenas_completion_rate__num'] = data['urenas_nb_arrived']
    data['urenas_completion_rate__denum'] = data['urenas_nb_expected']
    data['urenas_completion_rate'] = rpc(data, 'urenas_completion_rate')

    data['urenam_nb_expected'] = get(report, 'urenam',
                                     'nb_source_reports_expected')
    data['urenam_nb_arrived'] = get(report, 'urenam',
                                    'nb_source_reports_arrived')

    data['urenam_completion_rate__num'] = data['urenam_nb_arrived']
    data['urenam_completion_rate__denum'] = data['urenam_nb_expected']
    data['urenam_completion_rate'] = rpc(data, 'urenam_completion_rate')

    data['sam_comp_new_cases'] = get(report, None, 'sam_comp_new_cases')
    data['sam_comp_caseload_expected'] = get_caseload_expected_for(
        period=period, entity=entity, uren='sam')

    data['sam_comp_caseload_treated_rate__num'] = data['sam_comp_new_cases']
    data['sam_comp_caseload_treated_rate__denum'] = \
        data['sam_comp_caseload_expected']
    data['sam_comp_caseload_treated_rate'] = rpc(
        data, 'sam_comp_caseload_treated_rate')
    data['sam_comp_caseload_treated_rate_class'] = gc(
        data['sam_comp_caseload_treated_rate'], 'caseload')

    # ureni only
    data['sam_ureni_comp_healed'] = get(report, 'ureni', 'comp_healed')
    data['sam_ureni_comp_abandon'] = get(report, 'ureni', 'comp_abandon')
    data['sam_ureni_comp_deceased'] = get(report, 'ureni', 'comp_deceased')
    data['sam_ureni_comp_out_base'] = get(report, 'ureni', 'sam_comp_out_base')

    data['sam_ureni_comp_healed_rate__num'] = \
        perf_indic_num(report, 'sam_ureni_comp_', 'healed')
    data['sam_ureni_comp_healed_rate__denum'] = \
        perf_indic_denum(report, 'sam_ureni_comp_', 'healed')
    data['sam_ureni_comp_healed_rate'] = rpc(
        data, 'sam_ureni_comp_healed_rate')
    data['sam_ureni_comp_healed_rate_class'] = gc(
        data['sam_ureni_comp_healed_rate'], 'healed')

    data['sam_ureni_comp_abandon_rate__num'] = \
        perf_indic_num(report, 'sam_ureni_comp_', 'abandon')
    data['sam_ureni_comp_abandon_rate__denum'] = \
        perf_indic_denum(report, 'sam_ureni_comp_', 'abandon')
    data['sam_ureni_comp_abandon_rate'] = rpc(
        data, 'sam_ureni_comp_abandon_rate')
    data['sam_ureni_comp_abandon_rate_class'] = gc(
        data['sam_ureni_comp_abandon_rate'], 'abandon')

    data['sam_ureni_comp_deceased_rate__num'] = \
        perf_indic_num(report, 'sam_ureni_comp_', 'deceased')
    data['sam_ureni_comp_deceased_rate__denum'] = \
        perf_indic_denum(report, 'sam_ureni_comp_', 'deceased')
    data['sam_ureni_comp_deceased_rate'] = rpc(
        data, 'sam_ureni_comp_deceased_rate')
    data['sam_ureni_comp_deceased_rate_class'] = gc(
        data['sam_ureni_comp_deceased_rate'], 'deceased')
    ####

    # ureni only
    data['sam_urenas_comp_healed'] = get(report, 'urenas', 'comp_healed')
    data['sam_urenas_comp_abandon'] = get(report, 'urenas', 'comp_abandon')
    data['sam_urenas_comp_deceased'] = get(report, 'urenas', 'comp_deceased')
    data['sam_urenas_comp_out_base'] = get(report, 'urenas',
                                           'sam_comp_out_base')

    data['sam_urenas_comp_healed_rate__num'] = \
        perf_indic_num(report, 'sam_urenas_comp_', 'healed')
    data['sam_urenas_comp_healed_rate__denum'] = \
        perf_indic_denum(report, 'sam_urenas_comp_', 'healed')
    data['sam_urenas_comp_healed_rate'] = rpc(
        data, 'sam_urenas_comp_healed_rate')
    data['sam_urenas_comp_healed_rate_class'] = gc(
        data['sam_urenas_comp_healed_rate'], 'healed')

    data['sam_urenas_comp_abandon_rate__num'] = \
        perf_indic_num(report, 'sam_urenas_comp_', 'abandon')
    data['sam_urenas_comp_abandon_rate__denum'] = \
        perf_indic_denum(report, 'sam_urenas_comp_', 'abandon')
    data['sam_urenas_comp_abandon_rate'] = rpc(
        data, 'sam_urenas_comp_abandon_rate')
    data['sam_urenas_comp_abandon_rate_class'] = gc(
        data['sam_urenas_comp_abandon_rate'], 'abandon')

    data['sam_urenas_comp_deceased_rate__num'] = \
        perf_indic_num(report, 'sam_urenas_comp_', 'deceased')
    data['sam_urenas_comp_deceased_rate__denum'] = \
        perf_indic_denum(report, 'sam_urenas_comp_', 'deceased')
    data['sam_urenas_comp_deceased_rate'] = rpc(
        data, 'sam_urenas_comp_deceased_rate')
    data['sam_urenas_comp_deceased_rate_class'] = gc(
        data['sam_urenas_comp_deceased_rate'], 'deceased')
    ####

    data['sam_ureni_comp_new_cases'] = get(report, 'ureni', 'comp_new_cases')
    data['sam_urenas_comp_new_cases'] = get(report, 'urenas', 'comp_new_cases')
    data['sam_comp_new_cases'] = get(report, None, 'sam_comp_new_cases')

    data['sam_ureni_comp_new_cases_rate__num'] = \
        data['sam_ureni_comp_new_cases']
    data['sam_ureni_comp_new_cases_rate__denum'] = \
        data['sam_comp_new_cases']
    data['sam_ureni_comp_new_cases_rate'] = rpc(
        data, 'sam_ureni_comp_new_cases_rate')
    data['sam_ureni_comp_new_cases_rate_class'] = gc(
        data['sam_ureni_comp_new_cases_rate'], 'ureni')

    data['sam_urenas_comp_new_cases_rate__num'] = \
        data['sam_urenas_comp_new_cases']
    data['sam_urenas_comp_new_cases_rate__denum'] = \
        data['sam_comp_new_cases']
    data['sam_urenas_comp_new_cases_rate'] = rpc(
        data, 'sam_urenas_comp_new_cases_rate')
    data['sam_urenas_comp_new_cases_rate_class'] = gc(
        data['sam_urenas_comp_new_cases_rate'], 'urenas')

    data['sam_comp_healed'] = get(report, None, 'sam_comp_healed')
    data['sam_comp_abandon'] = get(report, None, 'sam_comp_abandon')
    data['sam_comp_deceased'] = get(report, None, 'sam_comp_deceased')
    data['sam_comp_out_base'] = get(report, None, 'sam_comp_out_base')

    data['sam_comp_healed_rate__num'] = \
        perf_indic_num(report, 'sam_comp_', 'healed')
    data['sam_comp_healed_rate__denum'] = \
        perf_indic_denum(report, 'sam_comp_', 'healed')
    data['sam_comp_healed_rate'] = rpc(data, 'sam_comp_healed_rate')
    data['sam_comp_healed_rate_class'] = gc(
        data['sam_comp_healed_rate'], 'healed')

    data['sam_comp_abandon_rate__num'] = \
        perf_indic_num(report, 'sam_comp_', 'abandon')
    data['sam_comp_abandon_rate__denum'] = \
        perf_indic_denum(report, 'sam_comp_', 'abandon')
    data['sam_comp_abandon_rate'] = rpc(data, 'sam_comp_abandon_rate')
    data['sam_comp_abandon_rate_class'] = gc(
        data['sam_comp_abandon_rate'], 'abandon')

    data['sam_comp_deceased_rate__num'] = \
        perf_indic_num(report, 'sam_comp_', 'deceased')
    data['sam_comp_deceased_rate__denum'] = \
        perf_indic_denum(report, 'sam_comp_', 'deceased')
    data['sam_comp_deceased_rate'] = rpc(data, 'sam_comp_deceased_rate')
    data['sam_comp_deceased_rate_class'] = gc(
        data['sam_comp_deceased_rate'], 'deceased')

    data['mam_comp_new_cases'] = get(report, None, 'mam_comp_new_cases')

    data['mam_comp_caseload_expected'] = get_caseload_expected_for(
        period=period, entity=entity, uren='mam')
    data['mam_comp_caseload_treated_rate__num'] = data['mam_comp_new_cases']
    data['mam_comp_caseload_treated_rate__denum'] = \
        data['mam_comp_caseload_expected']
    data['mam_comp_caseload_treated_rate'] = rpc(
        data, 'mam_comp_caseload_treated_rate')
    data['mam_comp_caseload_treated_rate_class'] = gc(
        data['mam_comp_caseload_treated_rate'], 'caseload')

    data['mam_comp_healed'] = get(report, None, 'mam_comp_healed')
    data['mam_comp_abandon'] = get(report, None, 'mam_comp_abandon')
    data['mam_comp_deceased'] = get(report, None, 'mam_comp_deceased')
    data['mam_comp_out_base'] = get(report, None, 'mam_comp_out_base')

    data['mam_comp_healed_rate__num'] = \
        perf_indic_num(report, 'mam_comp_', 'healed')
    data['mam_comp_healed_rate__denum'] = \
        perf_indic_denum(report, 'mam_comp_', 'healed')
    data['mam_comp_healed_rate'] = rpc(data, 'mam_comp_healed_rate')
    data['mam_comp_healed_rate_class'] = gc(
        data['mam_comp_healed_rate'], 'healed')

    data['mam_comp_abandon_rate__num'] = \
        perf_indic_num(report, 'mam_comp_', 'abandon')
    data['mam_comp_abandon_rate__denum'] = \
        perf_indic_denum(report, 'mam_comp_', 'abandon')
    data['mam_comp_abandon_rate'] = rpc(data, 'mam_comp_abandon_rate')
    data['mam_comp_abandon_rate_class'] = gc(
        data['mam_comp_abandon_rate'], 'abandon')

    data['mam_comp_deceased_rate__num'] = \
        perf_indic_num(report, 'mam_comp_', 'deceased')
    data['mam_comp_deceased_rate__denum'] = \
        perf_indic_denum(report, 'mam_comp_', 'deceased')
    data['mam_comp_deceased_rate'] = rpc(data, 'mam_comp_deceased_rate')
    data['mam_comp_deceased_rate_class'] = gc(
        data['mam_comp_deceased_rate'], 'deceased')

    return data


def generate_entity_periods_matrix(entity, periods):
    data = {
        'entity': {'slug': entity.slug, 'name': entity.name},
        'periods': OrderedDict([
            (period, generate_entity_period_matrix(entity, period))
            for period in sorted(periods, key=lambda x: x.start_on)
        ])
    }
    data['periods']["TOTAL"] = \
        generate_entity_period_matrix(entity, periods, data['periods'])
    return data


def generate_entities_periods_matrix(entity, periods):
    return OrderedDict([
        (centity.slug,  generate_entity_periods_matrix(centity, periods))
        for centity in sorted(entity.get_health_children(), key=sort_by_name)
    ] + [
        (entity.slug, generate_entity_periods_matrix(entity, periods))
    ])


def get_caseload_completion_for(period, entity, uren):
    periods = MonthPeriod.all_from(
        MonthPeriod.find_create_from(period.middle().year, 1, 1), period)
    field = '{}_comp_new_cases'.format(uren)
    return compute_sum_value(entity=entity, periods=periods, field=field)


def get_caseload_expected_for(period, entity, uren):
    if isinstance(period, list):
        period = period[-1]
    return getattr(ExpectedCaseload.get_or_none_from(
        year=period.start_on.year,
        entity_slug=entity.slug), 'u59o6_{}'.format(uren), 0)
