#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging

from snisi_core.models.Reporting import ExpectedReporting, ReportClass
from snisi_core.models.Entities import Entity
from snisi_nutrition.models.URENI import AggURENINutritionR, URENINutritionR
from snisi_nutrition.models.URENAS import AggURENASNutritionR, URENASNutritionR
from snisi_nutrition.models.URENAM import AggURENAMNutritionR, URENAMNutritionR
from snisi_nutrition.models.Stocks import AggNutritionStocksR, NutritionStocksR
from snisi_nutrition.models.Monthly import AggNutritionR, NutritionR

logger = logging.getLogger(__name__)


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
    report_classes = [
        ReportClass.get_or_none("nutrition_monthly_routine"),
        ReportClass.get_or_none("nutrition_monthly_routine_aggregated")]
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
