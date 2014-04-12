#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

from snisi_core.models.Entities import Entity
from snisi_core.models.Projects import Cluster
from snisi_core.indicators import IndicatorTable, is_ref, ref_is, hide
from snisi_malaria.indicators.section1 import (
    NbSourceReportsArrived, NbSourceReportsExpected)
from snisi_tools.caching import json_cache_from_cluster

cluster = Cluster.get_or_none("malaria_monthly_routine")


class TableauPromptitudeRapportage(IndicatorTable):

    name = "Tableau 1"
    title = ""
    caption = ("Pourcentage de structures ayant transmis leurs formulaires "
               "de collecte dans les délais prévus")
    rendering_type = 'table'
    on_descendants = True
    add_percentage = True

    def get_descendants(self):
        return [Entity.get_or_none(e['slug'])
                for e in json_cache_from_cluster(cluster).get(self.entity.slug)]

    INDICATORS = [
        is_ref(NbSourceReportsExpected),
        ref_is(0)(NbSourceReportsArrived),
    ]

class FigurePromptitudeRapportage(IndicatorTable):

    name = "Figure 1"
    title = ""
    caption = ("Évolution de la promptitude de la notification")
    rendering_type = 'graph'
    graph_type = 'spline'
    as_percentage = True
    on_descendants = True

    def get_descendants(self):
        return [Entity.get_or_none(e['slug'])
                for e in json_cache_from_cluster(cluster).get(self.entity.slug)]

    INDICATORS = [
        is_ref(NbSourceReportsExpected),
        ref_is(0)(NbSourceReportsArrived),
    ]


WIDGETS = [TableauPromptitudeRapportage,
           FigurePromptitudeRapportage
]
TITLE = "Données sur la complétude du rapportage"
