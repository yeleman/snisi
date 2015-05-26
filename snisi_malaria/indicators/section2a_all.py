#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

from snisi_malaria.indicators.common import gen_shortcut
from snisi_core.indicators import IndicatorTable, is_ref, ref_is, hide
from snisi_malaria.indicators.section2a import TITLE as TITLE_2A


class TousCasPaludismeNotifies(IndicatorTable):
    """Tableau: Nombre de cas de paludisme (tout âge confondu) notifiés """

    name = "Tableau 3"
    title = "Tout âge confondu"
    caption = "Nombre de cas de paludisme (tout âge confondu) notifiés"
    rendering_type = 'table'
    add_percentage = True
    add_total = True

    INDICATORS = [
        is_ref(gen_shortcut(
            'total_consultation_all_causes',
            "Total consultation toutes causes confondues (TCC)")),
        ref_is(0)(gen_shortcut(
            'total_suspected_malaria_cases',
            "Nombre de cas de paludisme (tous suspectés) "
            "parmi le total consultation")),
        ref_is(1)(gen_shortcut(
            'total_tested_malaria_cases',
            "Total des cas suspects testés (GE et/ou TDR)")),
        ref_is(2)(gen_shortcut(
            'total_confirmed_malaria_cases',
            "Nombre de cas suspects testés qui sont confirmés par GE ou TDR")),
        ref_is(3)(gen_shortcut('total_simple_malaria_cases', ". Cas simples")),
        ref_is(3)(gen_shortcut('total_severe_malaria_cases', ". Cas graves")),
    ]


class ProportionsPaludismeConsultationsTTC(IndicatorTable):
    """Graphe: Proportion des cas de paludisme par rapport aux consultations

        toutes causes confondues """

    name = "Figure 3"
    title = ""
    caption = ("Proportion des cas suspects de paludisme par rapport aux "
               "consultations toutes causes confondues")
    rendering_type = 'graph'
    as_percentage = True

    INDICATORS = [
        hide(is_ref(gen_shortcut(
            'total_consultation_all_causes',
            "Total consultation toutes causes confondues (TCC)"))),
        ref_is(0)(gen_shortcut(
            'total_suspected_malaria_cases',
            "Pourcentage de consultations pour Paludisme "
            "(Tous cas suspectés)")),
    ]


class NbreCasSuspectesTestesConfirmesALL(IndicatorTable):
    """ Graphe: Nombre de cas de paludisme (cas suspects, cas testés, cas

        confirmés) tout âge confondu. """

    name = "Figure 4"
    caption = ("Nombre de cas de paludisme (cas suspects, "
               "cas testés, cas confirmés) tout âge confondu.")
    rendering_type = 'graph'
    graph_type = 'column'

    INDICATORS = [
        is_ref(gen_shortcut('total_suspected_malaria_cases', "Cas suspects")),
        ref_is(0)(gen_shortcut('total_tested_malaria_cases', "Cas testés")),
        ref_is(0)(gen_shortcut('total_confirmed_malaria_cases',
                               "Cas confirmés")),
    ]


class CasSimplesGravesALL(IndicatorTable):
    """ Graphe: Nombre de cas de paludisme (cas suspects, cas testés, cas

        confirmés) tout âge confondu. """

    name = "Figure 5"
    caption = ("Nombre de cas de paludisme par mois  (cas confirmés, "
               "cas simples, cas graves) tout âge confondu.")
    rendering_type = 'graph'
    graph_type = 'column'

    INDICATORS = [
        gen_shortcut('total_confirmed_malaria_cases', "Cas confirmés"),
        ref_is(0)(gen_shortcut('total_simple_malaria_cases', "Cas simples")),
        ref_is(0)(gen_shortcut('total_severe_malaria_cases', "Cas graves")),
    ]


WIDGETS = [TousCasPaludismeNotifies,
           ProportionsPaludismeConsultationsTTC,
           NbreCasSuspectesTestesConfirmesALL,
           CasSimplesGravesALL]
TITLE = "{} / Tout âge confondu".format(TITLE_2A)
