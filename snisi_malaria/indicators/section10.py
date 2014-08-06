#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

from snisi_malaria.indicators.common import gen_shortcut
from snisi_core.indicators import IndicatorTable, is_ref, ref_is, hide


class CasConfirmes(IndicatorTable):
    """ """

    name = "Tableau 21"
    title = " "
    caption = ("Pourcentage de cas de paludisme confirmés chez les moins "
               "de 5 ans et tout âge confond")
    rendering_type = 'table'

    add_percentage = True

    INDICATORS = [
        is_ref(gen_shortcut(
            'u5_total_tested_malaria_cases',
            "Total des cas suspects testés chez les moins de 5 ans")),
        ref_is(0)(gen_shortcut(
            'u5_total_confirmed_malaria_cases',
            "Total des cas confirmés chez les moins de 5 ans")),
        is_ref(gen_shortcut(
            'total_tested_malaria_cases',
            "Total des cas suspects testés chez Tout âge confond")),
        ref_is(2)(gen_shortcut(
            'total_confirmed_malaria_cases',
            "Total des cas confirmés chez Tout âge confond")),
    ]


class GrapheConfirmes(IndicatorTable):
    """ Graphe: Pourcentage de cas de paludisme confirmés chez les moins de 5

        ans et tout âge confondu """

    name = "Figure 31"
    caption = ("Pourcentage de cas de paludisme confirmés chez les moins "
               "de 5 ans et tout âge confond")
    graph_type = 'spline'
    rendering_type = "graph"
    as_percentage = True

    INDICATORS = [
        hide(is_ref(gen_shortcut(
            'u5_total_tested_malaria_cases',
            "Total des cas suspects testés chez les moins de 5 ans"))),
        ref_is(0)(gen_shortcut(
            'u5_total_confirmed_malaria_cases',
            "Total des cas confirmés chez les moins de 5 ans")),
        hide(is_ref(gen_shortcut(
            'total_tested_malaria_cases',
            "Total des cas suspects testés chez Tout âge confond"))),
        ref_is(2)(gen_shortcut(
            'total_confirmed_malaria_cases',
            "Total des cas confirmés chez Tout âge confond")),
    ]


class NbreHospitalisationDeces(IndicatorTable):
    """ Tableau: Données sur l'hospitalisation et le decès pour paludisme chez

        les moins de 5 ans """

    name = "Tableau 22"
    title = ("Nombre d'hospitalisation et décès pour paludisme chez les "
             "moins 5 ans")
    caption = ("Nombre d'hospitalisation et décès pour paludisme chez les "
               "moins 5 ans")
    rendering_type = 'table'

    INDICATORS = [
        gen_shortcut('u5_total_malaria_inpatient',
                     "Hospitalisations pour paludisme"),
        gen_shortcut('u5_total_malaria_death',
                     "Décès pour paludisme"),
    ]


class GrapheNbreHospitalisationDeces(NbreHospitalisationDeces):
    """ Graphe: Données sur l'hospitalisation et le decès pour paludisme chez

        les moins de 5 ans """

    name = "Figure 32"
    title = " "
    caption = ("Nombre d'hospitalisation et décès pour paludisme chez les"
               "moins de 5 ans")
    rendering_type = 'graph'
    graph_type = 'spline'


class DecesPaluToutCauses(IndicatorTable):
    """ Tableau: Données de décès pour paludisme et toutes causes chez les

        moins de 5 ans """

    name = "Tableau 23"
    title = " "
    caption = "Pourcentage de décès pour paludisme et pourcentage de décès " \
              "toutes causes chez les moins de 5 ans"
    rendering_type = 'table'

    add_percentage = True

    INDICATORS = [
        is_ref(gen_shortcut(
            'u5_total_consultation_all_causes',
            "Total consultation chez les moins de 5 ans")),
        ref_is(0)(gen_shortcut(
            'u5_total_death_all_causes',
            "Décès toutes causes confondues chez les moins de 5 ans")),
        ref_is(1)(gen_shortcut(
            'u5_total_malaria_death',
            "Décès pour paludisme chez les moins de 5 ans")),
        is_ref(gen_shortcut(
            'o5_total_consultation_all_causes',
            "Total consultation chez les 5 ans et plus")),
        ref_is(3)(gen_shortcut(
            'o5_total_death_all_causes',
            "Décès toutes causes confondues chez les 5 ans et plus")),
        ref_is(4)(gen_shortcut(
            'o5_total_malaria_death',
            "Décès pour paludisme chez les 5 ans et plus")),
    ]


class GrapheDecesPaluToutCauses(IndicatorTable):
    """ Graphe: Pourcentage de décès pour paludisme et toutes causes chez les

        moins de 5 ans """

    name = "Figure 33"
    title = " "
    caption = ("Pourcentage de décès pour paludisme et pourcentage de décès "
               "toutes causes chez les moins de 5 ans")
    graph_type = 'spline'
    rendering_type = 'graph'

    as_percentage = True

    INDICATORS = [
        hide(is_ref(gen_shortcut(
            'u5_total_death_all_causes',
            "Décès toutes causes confondues chez les moins de 5 ans"))),
        ref_is(0)(gen_shortcut(
            'u5_total_malaria_death',
            "Pourcentage décès pour paludisme chez les moins de 5 ans")),
        hide(is_ref(gen_shortcut(
            'o5_total_death_all_causes',
            "Décès toutes causes confondues chez les 5 ans et plus"))),
        ref_is(2)(gen_shortcut(
            'o5_total_malaria_death',
            "Pourcentage décès pour paludisme chez les 5 ans et plus")),
    ]


class CasTestesConfirmes(IndicatorTable):
    """ Tableau: Pourcentage de cas de suspect testés et pourcentage de cas de

        paludisme confirmés parmi les cas testés """

    name = "Tableau 25"
    title = " "
    caption = ("Pourcentage de cas suspect testés et pourcentage de cas de "
               "paludisme confirmés parmi les cas testés")
    rendering_type = 'table'

    add_percentage = True

    INDICATORS = [
        is_ref(gen_shortcut('total_suspected_malaria_cases',
                            "Total des cas suspects")),
        ref_is(0)(gen_shortcut('total_tested_malaria_cases',
                               "Total des cas suspects testés")),
        ref_is(1)(gen_shortcut('total_confirmed_malaria_cases',
                               "Cas confirmés")),
    ]


class GrapheCasTestesConfirmes(IndicatorTable):
    """ Graphe: Nombre de femmes enceintes reçues en CPN1 et Nombre de

        MILD distribuées aux femmes enceintes"""

    name = "Figure 35"
    title = " "
    caption = ("Pourcentage de cas suspect testés et pourcentage de cas de "
               "paludisme confirmés parmi les cas testés")
    graph_type = 'spline'
    rendering_type = 'graph'
    as_percentage = True

    INDICATORS = [
        hide(is_ref(gen_shortcut('total_suspected_malaria_cases',
                                 "Total des cas suspects"))),
        ref_is(0)(gen_shortcut('total_tested_malaria_cases',
                               "Total des cas suspects testés")),
        ref_is(1)(gen_shortcut('total_confirmed_malaria_cases',
                               "Cas confirmés")),
    ]


class NbreConsultationCasSuspect(IndicatorTable):
    """ Tableau: Pourcentage de cas de suspect testés et pourcentage de cas de

        paludisme confirmés parmi les cas testés """

    name = "Tableau 26"
    title = " "
    caption = ("Nombre de consultation toutes causes confondues et nombre de "
               "cas suspects de paludisme")
    rendering_type = 'table'

    INDICATORS = [
        gen_shortcut('total_consultation_all_causes',
                     "Total consultation(toutes causes)"),
        gen_shortcut('total_tested_malaria_cases',
                     "Cas suspects de paludisme"),
    ]


class GrapheNbreConsultationCasSuspect(NbreConsultationCasSuspect):
    """ Graphe: Nombre de femmes enceintes reçues en CPN1 et Nombre de

        MILD distribuées aux femmes enceintes"""

    name = "Figure 36"
    title = " "
    caption = ("Nombre de consultation toutes causes confondues et nombre de "
               "cas suspects de paludisme")
    graph_type = 'spline'
    rendering_type = 'graph'


WIDGETS = [CasConfirmes, GrapheConfirmes, NbreHospitalisationDeces,
           GrapheNbreHospitalisationDeces, DecesPaluToutCauses,
           GrapheDecesPaluToutCauses,
           # DecesPalu, GrapheDecesPalu,
           CasTestesConfirmes,
           GrapheCasTestesConfirmes,
           NbreConsultationCasSuspect,
           GrapheNbreConsultationCasSuspect]
TITLE = "Données de surveillance"
