#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging
import datetime
from collections import OrderedDict

import numpy as np
from django.utils import timezone
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from snisi_core.models.Entities import Entity
from snisi_core.models.Periods import MonthPeriod
from snisi_web.decorators import user_role_within
from snisi_nutrition.models.Monthly import NutritionR
from snisi_nutrition.models.Stocks import NutritionStocksR
from snisi_nutrition.models.Weekly import NutWeekPeriod, WeeklyNutritionR
from snisi_nutrition.indicators.small import (
    TableauPromptitudeRapportage,
    FigurePromptitudeRapportage,
    WeekTableauPromptitudeRapportage,
    WeekFigurePromptitudeRapportage)

logger = logging.getLogger(__name__)


@login_required
@user_role_within(['snisi_admin'])
def dashboard(request, **kwargs):

    now = timezone.now()
    last_period = MonthPeriod.current().previous() if now.day < 26 else None
    if now.day < 10:
        last_period = last_period.previous()
    periods = MonthPeriod.all_from(
        MonthPeriod.from_url_str("11-2014"), last_period)
    entity = request.user.location.casted()

    fwp = NutWeekPeriod.find_create_by_date(datetime.datetime(2014, 12, 1))
    lwp = NutWeekPeriod.find_create_by_date(datetime.datetime(2015, 6, 26))
    wperiods = NutWeekPeriod.all_from(fwp, lwp)

    imatrix = OrderedDict([
        ('promptitude', TableauPromptitudeRapportage),
        ('promptitude_graph', FigurePromptitudeRapportage),
        ('w_promptitude', WeekTableauPromptitudeRapportage),
        ('w_promptitude_graph', WeekFigurePromptitudeRapportage),
    ])

    gp = lambda s: wperiods if s.startswith('w_') else periods

    sm_indics = {slug: icls(entity=entity, periods=gp(slug))
                 for slug, icls in imatrix.items()}

    def pc(a, b):
        try:
            return b / a
        except ZeroDivisionError:
            return 0

    mopti = Entity.get_or_none("SSH3")
    nb_hc = len(mopti.get_health_centers())
    nb_months = len(periods)
    nb_exp = nb_hc * nb_months
    nb_received = NutritionR.objects.all().count()
    nb_received_it = NutritionR.objects.filter(
        arrival_status=NutritionR.ON_TIME).count()
    # nb_stock = len([1 for r in NutritionStocksR.objects.all()
    #                 if r.has_stockout()])
    nb_stock_thera = len([1 for r in NutritionStocksR.objects.all()
                          if r.has_therapeutic_stockout()])
    nb_stock_drug = len([1 for r in NutritionStocksR.objects.all()
                         if r.has_drug_stockout()])

    nb_weeks = len(wperiods)
    nb_expw = nb_hc * nb_weeks
    nb_receivedw = WeeklyNutritionR.objects.all().count()
    nb_received_itw = WeeklyNutritionR.objects.filter(
        arrival_status=WeeklyNutritionR.ON_TIME).count()

    ds_received = [(ds.name,
                    pc(len(ds.get_health_centers()) * nb_months,
                       NutritionR.objects.filter(
                        entity__slug__in=[hc.slug
                                          for hc in ds.get_health_centers()])
                       .count()))
                   for ds in mopti.get_health_districts()]

    ds_auto_val = [(ds.name,
                    pc(len(ds.get_health_centers()) * nb_months,
                       NutritionR.objects.filter(
                        entity__slug__in=[hc.slug
                                          for hc in ds.get_health_centers()],
                        auto_validated=False)
                       .count()))
                   for ds in mopti.get_health_districts()]

    nb_hc_100 = len([hc for hc in mopti.get_health_centers()
                     if NutritionR.objects.filter(entity__slug=hc.slug)
                                  .count() == nb_months])

    overall_table = OrderedDict([
        ("Nombre de centres", nb_hc),
        ("Nombre de mois", nb_months),
        ("Nombre de rapports attendus", nb_exp),
        ("Nombre de rapports reçus", nb_received),
        ("Taux de complétude moyen", pc(nb_exp, nb_received)),
        ("Nombre de rapports reçus à temps", nb_received_it),
        ("Taux de promptitude moyen", pc(nb_exp, nb_received_it)),

        ("Nombre de semaines", nb_weeks),
        ("Nombre de rapports hebdo attendus", nb_expw),
        ("Nombre de rapports hebdo reçus", nb_receivedw),
        ("Taux de complétude hebdo moyen", pc(nb_expw, nb_receivedw)),
        ("Nombre de rapports hebdo reçus à temps", nb_received_itw),
        ("Taux de promptitude hebdo moyen", pc(nb_expw, nb_received_itw)),

        ("Nombre de rapports avec de mauvais indicateurs de performances", 0),
        ("Pourcentage de mauvais indicateurs de performances", 0),
        ("Classement du rapportage (complétude) par DS", "-"),
    ])
    for idx, dsdd in enumerate(sorted(ds_received,
                                      key=lambda x: x[1], reverse=True)):
        overall_table.update({
            "nº {} – DS de {}".format(idx + 1, dsdd[0]): dsdd[1]})

    overall_table.update({"Taux de rapports validés par les districts": "-"})
    for idx, dsdd in enumerate(sorted(ds_auto_val,
                                      key=lambda x: x[1], reverse=True)):
        overall_table.update({
            "nº {} – DS de {}".format(idx + 1, dsdd[0]): dsdd[1]})

    overall_table.update({
        "Pourcentage de CSCOM avec complétude 100%": pc(nb_hc, nb_hc_100)})

    overall_table.update({
        "Pourcentage de rapport mensuel avec au moins une "
        "rupture d'intrant thérapeutique": pc(nb_exp, nb_stock_thera)})
    overall_table.update({
        "Pourcentage de rapport mensuel avec au moins une "
        "rupture de médicament": pc(nb_exp, nb_stock_drug)})

    context = {
        'periods': periods,
        'entity': entity,
        'indicators': sm_indics,
        'overall_table': overall_table,
    }
    return render(request, kwargs.get('template_name',
                  'nutrition/small_indicators.html'), context)
