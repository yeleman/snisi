#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

from snisi_malaria.models import MalariaR
from snisi_malaria.indicators.common import MalariaIndicator
from snisi_core.indicators import IndicatorTable, is_ref, ref_is, hide


class NbSourceReportsExpected(MalariaIndicator):
    name = "Nombre de rapports attendus"

    def _compute(self):
        if self.is_hc():
            return 1 if self._expected else 0
        return getattr(self.report, 'nb_source_reports_expected', 0)


class NbSourceReportsArrived(MalariaIndicator):
    name = "Nombre de rapports reçus"

    def _compute(self):
        if self.is_hc():
            return 1 if self._expected.satisfied else 0
        return getattr(self.report, 'nb_source_reports_arrived', 0)


class NbSourceReportsArrivedOnTime(MalariaIndicator):
    name = "Nombre de rapports reçus à temps"

    def _compute(self):
        if self.is_hc():
            if self._expected.satisfied:
                return 1 if self.report.arrival_status == MalariaR.ON_TIME \
                    else 0
            else:
                return 0
        return getattr(self.report, 'nb_source_reports_arrived_on_time', 0)


class TableauPromptitudeRapportage(IndicatorTable):

    name = "Tableau 1"
    title = ""
    caption = ("Pourcentage de structures ayant transmis leurs formulaires "
               "de collecte dans les délais prévus")
    rendering_type = 'table'

    INDICATORS = [
        is_ref(NbSourceReportsExpected),
        ref_is(0)(NbSourceReportsArrived),
        ref_is(0)(NbSourceReportsArrivedOnTime),
    ]


class FigurePromptitudeRapportage(IndicatorTable):

    name = "Figure 1"
    title = ""
    caption = ("Évolution de la promptitude de la notification")
    rendering_type = 'graph'
    graph_type = 'spline'
    as_percentage = True

    INDICATORS = [
        hide(is_ref(NbSourceReportsExpected)),
        ref_is(0)(NbSourceReportsArrived),
        ref_is(0)(NbSourceReportsArrivedOnTime),
    ]


WIDGETS = [
    TableauPromptitudeRapportage,
    FigurePromptitudeRapportage
]
TITLE = "Identification de la structure ayant notifié les données"
