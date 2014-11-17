#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging
import datetime

from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from snisi_core.models.Periods import MonthPeriod
from snisi_core.models.Projects import Cluster
from snisi_epidemiology.models import (EpidemiologyR,
                                       AggEpidemiologyR,
                                       EpidemiologyAlertR)
from snisi_web.utils import entity_periods_context
from snisi_core.indicators import IndicatorTable, is_ref, ref_is
from snisi_core.indicators import Indicator, gen_report_indicator
from snisi_epidemiology.models import EpiWeekPeriod

logger = logging.getLogger(__name__)


class EpidemiologyIndicator(Indicator):
    INDIVIDUAL_CLS = EpidemiologyR
    AGGREGATED_CLS = AggEpidemiologyR

    def is_hc(self):
        ''' whether at HealthCenter/Source level or not (above) '''
        return self.entity.type.slug == 'health_center'

    def should_yesno(self):
        return self.is_hc()

    def sum_on_hc(self, field):
        return sum(self.all_hc_values(field))

    def all_hc_values(self, field):
        return [getattr(r, field, None)
                for r in self.report.indiv_sources.all()]

gen_shortcut = lambda field, label=None: gen_report_indicator(
    field, name=label, report_cls=EpidemiologyR,
    base_indicator_cls=EpidemiologyIndicator)


class Summary(IndicatorTable):

    name = "Tableau 1"
    title = ""
    caption = ("Cas suspects et décès suspects des "
               "Maladies à Déclaration Obligatoire")
    rendering_type = 'table'

    INDICATORS = [
        is_ref(gen_shortcut('ebola_case')),
        ref_is(0)(gen_shortcut('ebola_death')),
        is_ref(gen_shortcut('acute_flaccid_paralysis_case')),
        ref_is(2)(gen_shortcut('acute_flaccid_paralysis_death')),
        is_ref(gen_shortcut('influenza_a_h1n1_case')),
        ref_is(4)(gen_shortcut('influenza_a_h1n1_death')),
        is_ref(gen_shortcut('cholera_case')),
        ref_is(6)(gen_shortcut('cholera_death')),
        is_ref(gen_shortcut('red_diarrhea_case')),
        ref_is(8)(gen_shortcut('red_diarrhea_death')),
        is_ref(gen_shortcut('measles_case')),
        ref_is(10)(gen_shortcut('measles_death')),
        is_ref(gen_shortcut('yellow_fever_case')),
        ref_is(12)(gen_shortcut('yellow_fever_death')),
        is_ref(gen_shortcut('neonatal_tetanus_case')),
        ref_is(14)(gen_shortcut('neonatal_tetanus_death')),
        is_ref(gen_shortcut('meningitis_case')),
        ref_is(16)(gen_shortcut('meningitis_death')),
        is_ref(gen_shortcut('rabies_case')),
        ref_is(18)(gen_shortcut('rabies_death')),
        is_ref(gen_shortcut('acute_measles_diarrhea_case')),
        ref_is(20)(gen_shortcut('acute_measles_diarrhea_death')),
        is_ref(gen_shortcut('other_notifiable_disease_case')),
        ref_is(22)(gen_shortcut('other_notifiable_disease_death')),
    ]


def nb_cases_for(periods, report_cls, field='cases'):
    return sum(
        [getattr(r, 'nb_{}_total'.format(field))()
         for r in report_cls.objects.filter(
            period__start_on__gte=periods[0].start_on,
            period__end_on__lte=periods[-1].end_on)])


@login_required
def indicators(request,
               entity_slug=None,
               perioda_str=None,
               periodb_str=None,
               **kwargs):
    context = {}

    cluster = Cluster.get_or_none('epidemiology_routine')
    context.update(entity_periods_context(
        request=request,
        root=request.user.location,
        cluster=cluster,
        view_name='epidemio_indicators',
        entity_slug=entity_slug,
        report_cls=EpidemiologyR,
        period_cls=MonthPeriod,
        must_be_in_cluster=False,
        full_lineage=['country', 'health_region',
                      'health_district', 'health_center']))

    summary_widget = Summary(periods=context['periods'],
                             entity=context['entity'])
    context.update({'summary_widget': summary_widget})

    return render(request,
                  kwargs.get('template_name',
                             'epidemiology/indicators.html'),
                  context)


@login_required
def dashboard(request, **kwargs):
    context = {}

    # # TODO: in this context we should use only Epidemiology not Agg

    # context.update({
    #     'current_period': MonthPeriod.current(),
    #     'periods': EpiWeekPeriod.all_from(
    #         EpiWeekPeriod.find_create_by_date(
    #             timezone.now() - datetime.timedelta(days=60)))
    # })

    # # if there has been NO case at all, do nothing
    # nb_cases_previous_months = nb_cases_for(context['periods'],
    #                                         AggEpidemiologyR)
    # nb_cases_this_month = nb_cases_for([MonthPeriod.current()],
    #                                    AggEpidemiologyR)
    # nb_cases_total = sum([nb_cases_previous_months, nb_cases_this_month])

    # all_quiet = nb_cases_total == 0
    # context.update({'nb_cases_previous_months': nb_cases_previous_months,
    #                 'nb_cases_this_month': nb_cases_this_month,
    #                 'nb_cases_total': nb_cases_total,
    #                 'all_quiet': all_quiet})

    # # if there is at least one case, add warning
    # weeks = []
    # if not all_quiet:
    #     for period in reversed(context['periods']):
    #         data = {field: {'cases': 0,
    #                         'deaths': 0,
    #                         'reports': []}
    #                 for field in AggEpidemiologyR.disease_fields()}
    #         # data = {field: 0 for field in EpidemiologyR.disease_fields()}
    #         # data_located = {field: []
    #         #                 for field in EpidemiologyR.disease_fields()}
    #         for report in AggEpidemiologyR.objects.filter(period=period):
    #             for field in data.keys():
    #                 cases = getattr(report, "{}_case".format(field), 0)
    #                 deaths = getattr(report, "{}_death".format(field), 0)
    #                 if cases:
    #                     data[field]['cases'] += cases
    #                     data[field]['deaths'] += deaths
    #                     data[field]['reports'].append(report)
    #         weeks.append((period, data))
    # context.update({'weeks': weeks})

    amonth_ago = datetime.date.today() - datetime.timedelta(days=30)

    alerts = EpidemiologyAlertR.objects.filter(
        date__gte=amonth_ago).order_by('-date')
    context.update({
        'alerts': alerts,
        'nb_cases_this_month': sum([a.cases_total for a in alerts.all()]),
    })

    return render(request,
                  kwargs.get('template_name',
                             'epidemiology/dashboard_alerts.html'),
                  context)
