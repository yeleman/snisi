#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
from collections import OrderedDict

from snisi_malaria.indicators.common import MalariaIndicator, gen_shortcut, gen_shortcut_agg
from snisi_core.indicators import IndicatorTable, is_ref, ref_is, hide
from snisi_core.models.Reporting import ExpectedReporting
from snisi_malaria.indicators.section2a_all import (
    TousCasPaludismeNotifies,
    ProportionsPaludismeConsultationsTTC)
from snisi_core.models.Projects import Cluster
from snisi_malaria.indicators.map import (TotalTestedMalariaCases,
                                          TotalConfirmedMalariaCases,
                                          HealthUnitsWithoutACTChildrenStockout,
                                          HealthUnitsWithoutACTYouthStockout,
                                          HealthUnitsWithoutACTAdultStockout,
                                          HealthUnitsWithoutBednetStockout,
                                          HealthUnitsWithoutRDTStockout,
                                          HealthUnitsWithoutSPStockout)


class Tableau1(TousCasPaludismeNotifies):
    name = "Tableau 1"
    title = "Tout âge confondu"
    caption = ("Total consultation, cas suspects, cas testés, cas confirmés, "
               "paludisme grave et paludisme simple")



class Figure1(ProportionsPaludismeConsultationsTTC):

    name = "Figure 1"
    title = ""
    caption = ("Pourcentage de cas suspects de paludisme parmi le total "
               "consultations (tout âge confondu)")
    rendering_type = 'graph'
    graph_type = 'spline'
    as_percentage = True


class CasSuspectsTestes(TotalTestedMalariaCases):
    name = ("% de cas suspects testés")


class CasTestesConfirmes(TotalConfirmedMalariaCases):
    name = ("% de cas confirmés")


class Figure2(IndicatorTable):

    name = "Figure 2"
    title = ""
    caption = ("Pourcentage de cas suspects testés et pourcentage de "
               "cas confirmés (Tout âge confondu)")
    rendering_type = 'graph'
    as_percentage = True
    graph_type = 'spline'

    INDICATORS = [
        hide(is_ref(gen_shortcut('total_suspected_malaria_cases', "-"))),
        ref_is(0)(gen_shortcut('total_tested_malaria_cases',
                               "% de cas suspects testés")),
        ref_is(1)(gen_shortcut('total_confirmed_malaria_cases',
                               "% de cas testés confirmés")),
    ]


class Figure3(IndicatorTable):

    name = "Figure 3"
    title = ""
    caption = ("Nombre d’hospitalisation toutes causes confondues et "
               "nombre d’hospitalisation  pour paludisme "
               "chez les moins de 5 ans")
    rendering_type = 'graph'
    graph_type = 'spline'

    dual_axis = {
        'default': {'label': "Nbre hospitalisations TCC"},
        'opposite': {'label': "Nbre hospitalisations pour paludisme"}
        }

    INDICATORS = [
        gen_shortcut('u5_total_inpatient_all_causes',
                     "Nbre hospitalisations toutes causes contondues (TCC) (<5ans)"),
        gen_shortcut('u5_total_malaria_inpatient',
                     "Nbre hospitalisations pour paludisme grave (<5ans)"),
    ]


# class Figure4(IndicatorTable):
#     name = "Figure 4"
#     title = ""
#     caption = ("Nombre de cas de paludisme grave et nombre de décès pour"
#                "paludisme chez les moins de 5 ans")
#     rendering_type = 'graph'
#     graph_type = 'spline'

#     dual_axis = {
#         'default': {'label': "Nbre hospitalisations TCC"},
#         'opposite': {'label': "Nbre hospitalisations pour paludisme"}
#         }

#     INDICATORS = [
#         gen_shortcut('u5_total_severe_malaria_cases',
#                      "Cas de paludisme grave"),
#         gen_shortcut('u5_total_malaria_death',
#                      "Cas de décès"),
#     ]


class Figure5(IndicatorTable):
    name = "Figure 5"
    title = ""
    caption = ("Nombre de cas de paludisme grave et nombre de décès pour "
               "paludisme chez les moins de 5 ans")
    rendering_type = 'graph'
    graph_type = 'spline'

    dual_axis = {
        'default': {'label': "Nbre de cas graves"},
        'opposite': {'label': "Nbre de décès"}
    }

    INDICATORS = [
        gen_shortcut('u5_total_severe_malaria_cases',
                     "Nbre de cas de paludisme grave chez < 5 ans"),
        gen_shortcut('u5_total_malaria_death',
                     "Nbre de cas décès chez < 5 ans"),
    ]


class Figure6(IndicatorTable):
    name = "Figure 6"
    title = ""
    caption = ("Proportion de décès pour paludisme parmi le total décès "
               "toutes causes confondues chez les moins de 5 ans")
    rendering_type = 'graph'
    graph_type = 'spline'
    as_percentage = True

    INDICATORS = [
        hide(is_ref(gen_shortcut('u5_total_death_all_causes'))),
        ref_is(0)(gen_shortcut('u5_total_malaria_death',
                               "% décès pour paludisme chez "
                               "les moins de 5 ans"))
    ]


class Figure7(IndicatorTable):
    name = "Figure 7"
    title = "Tout âge confondu"
    caption = ("Nombre des cas de paludisme simple et Nombre de cas de "
               "paludisme simple traités par CTA (Tout âge confondu)")
    rendering_type = 'graph'
    graph_type = 'column'

    INDICATORS = [
        gen_shortcut('total_simple_malaria_cases',
                     "Nbre de cas de paludisme simple"),
        gen_shortcut('total_treated_malaria_cases',
                     "Nbre de cas de paludisme simples traités par CTA"),
    ]


class Figure8(IndicatorTable):
    name = "Figure 8"
    title = "Les moins de 5 ans"
    caption = ("Nombre des cas de paludisme simple et Nombre de cas de "
               "paludisme simple traités par CTA (chez les moins de 5 ans)")
    rendering_type = 'graph'
    graph_type = 'column'

    INDICATORS = [
        gen_shortcut('u5_total_simple_malaria_cases',
                     "Nbre de cas de paludisme simple"),
        gen_shortcut('u5_total_treated_malaria_cases',
                     "Nbre de cas de paludisme simples traités par CTA"),
    ]


class FECPNMILD(MalariaIndicator):
    name = ("% MILD")
    def _compute(self):
        return self.divide(self.report.pw_total_distributed_bednets,
                           self.report.pw_total_anc1)


class Figure9(IndicatorTable):
    """ MILD:
            Numérateur : Total femmes enceintes ayant  reçu une MILD;
            Dénominateur : total femmes enceintes vue en CNP (CPN total)
    """
    name = "Figure 9"
    title = ""
    caption = ("Pourcentage de femmes enceintes vues en CPN "
               "ayant reçu une MILD")
    rendering_type = 'graph'
    graph_type = 'spline'

    INDICATORS = [
        FECPNMILD
    ]


class PercentTPI2(MalariaIndicator):
    name = ("% TPI2")
    def _compute(self):
        return self.divide(self.report.pw_total_sp2,
                           self.report.pw_total_anc1)

class PercentTPI3(MalariaIndicator):
    name = ("% TPI3")
    def _compute(self):
        return self.divide(self.report.pw_total_sp3,
                           self.report.pw_total_anc1)

class Figure10(IndicatorTable):
    """ TPI2 :
        Numérateur : Total femmes enceintes ayant  reçu une SP2 ;
         Dénominateur : total femmes enceintes vue en CNP (CPN Total)

        TPI3 :
        Numérateur : Total femmes enceintes ayant  reçu une SP3 ;
         Dénominateur : total femmes enceintes vue en CNP (CPN Total)
    """
    name = "Figure 10"
    title = ""
    caption = ("Pourcentage de femmes enceintes vues en CPN ayant "
               "reçu un TPI2 ou TPI3")
    rendering_type = 'graph'
    graph_type = 'spline'

    INDICATORS = [
        PercentTPI2,
        # PercentTPI3
    ]


class StockoutActAdult(HealthUnitsWithoutACTAdultStockout):
    name = ("% CTA Adulte")
    is_geo_friendly = False
    is_yesno = False


class StockoutActChildren(HealthUnitsWithoutACTChildrenStockout):
    name = ("% CTA Nourrisson Enfant")
    is_geo_friendly = False
    is_yesno = False


class StockoutActYouth(HealthUnitsWithoutACTYouthStockout):
    name = ("% CTA Adolescent")
    is_geo_friendly = False
    is_yesno = False


class Figure11(IndicatorTable):
    """ structures sans rupture (par type de CTA)
            Numérateur : Nombre de centres sans ruptures de stocks (pour le type de CTA)
            Dénominateur : Nombre total de centres couverts
    """
    name = "Figure 11"
    title = ""
    caption = ("Pourcentage de structures sans rupture de stock en CTA")
    rendering_type = 'graph'
    graph_type = 'spline'

    INDICATORS = [
        StockoutActAdult,
        StockoutActChildren,
        StockoutActYouth
    ]


class HealthUnitsWithoutBednet(HealthUnitsWithoutBednetStockout):
    name = ("% MILD")


class HealthUnitsWithoutRDTS(HealthUnitsWithoutRDTStockout):
    name = ("% TDR")


class HealthUnitsWithoutSP(HealthUnitsWithoutSPStockout):
    name = ("% SP")


class Figure12(IndicatorTable):
    """ structures sans rupture (par type de produit)
            Numérateur : Nombre de centres sans ruptures de stocks (pour le produit)
            Dénominateur : Nombre total de centres couverts
    """
    name = "Figure 12"
    title = ""
    caption = ("Pourcentage de structures sans rupture de stock en SP, TDR et MILD")
    rendering_type = 'graph'
    graph_type = 'spline'

    INDICATORS = [
        HealthUnitsWithoutBednet,
        HealthUnitsWithoutRDTS,
        HealthUnitsWithoutSP,
    ]


class SMSSourceReportsExpected(MalariaIndicator):
    name = "Nb. de rapports attendus (SMS)"
    def _compute(self):
        descendants = [e.slug for e in self.entity.casted().get_descendants()]
        sms_members = Cluster.get_or_none("malaria_monthly_routine_sms").members()
        all_exp = ExpectedReporting.objects.filter(
            report_class__slug='malaria_monthly_routine', period=self.period)

        return len([1 for e in all_exp
                    if e.entity.casted() in sms_members and e.entity.slug in descendants])


class SMSSourceReportsArrivedInTime(MalariaIndicator):
    name = "Nb. de rapports reçus à temps (SMS)"
    def _compute(self):
        sms_members = Cluster.get_or_none("malaria_monthly_routine_sms").members()
        return len([1 for r in self.report.indiv_sources.all()
                    if r.entity.casted() in sms_members and r.arrival_status == r.ON_TIME])


class SMSSourceReportsArrived(MalariaIndicator):
    name = "Nb. de rapports reçus (SMS)"
    def _compute(self):
        sms_members = Cluster.get_or_none("malaria_monthly_routine_sms").members()
        return len([1 for r in self.report.indiv_sources.all()
                    if r.entity.casted() in sms_members])


class Figure13(IndicatorTable):
    """  de structures:
            Numérateur : nombre de centres ayant transmis leurs rapports dans
                         les délais requis (le 5 du mois suivant)
            Dénominateur : total centres couverts dans la région
    """
    name = "Figure 13"
    title = ""
    caption = ("Pourcentage de structures ayant transmis leurs données "
               "à temps (promptitude) ")
    rendering_type = 'graph'
    as_percentage = True
    graph_type = 'spline'

    INDICATORS = [
        hide(is_ref(gen_shortcut_agg('nb_source_reports_expected'))),
        ref_is(0)(gen_shortcut_agg('nb_source_reports_arrived_on_time',
                                   "Nb. de rapports reçus à temps.")),
        hide(is_ref(SMSSourceReportsExpected)),
        ref_is(2)(SMSSourceReportsArrivedInTime)
    ]


class Figure14(IndicatorTable):
    """  de structures:
        Numérateur : nombre de centres ayant transmis leurs rapports
        (y compris après les délais requis)
        Dénominateur : total centres couverts dans la région
    """
    name = "Figure 14"
    title = ""
    caption = ("Pourcentage de structures ayant transmis "
               "leurs données (complétude)")

    rendering_type = 'graph'
    as_percentage = True
    graph_type = 'spline'

    INDICATORS = [
        hide(is_ref(gen_shortcut_agg('nb_source_reports_expected'))),
        ref_is(0)(gen_shortcut_agg('nb_source_reports_arrived',
                                   "Nb. de rapports reçus.")),
        hide(is_ref(SMSSourceReportsExpected)),
        ref_is(2)(SMSSourceReportsArrived)
    ]

WIDGET_DICT = OrderedDict([
    ('Tableau1', Tableau1),
    ('Figure1', Figure1),
    ('Figure2', Figure2),
    ('Figure3', Figure3),
    ('Figure5', Figure5),
    ('Figure6', Figure6),
    ('Figure7', Figure7),
    ('Figure8', Figure8),
    ('Figure9', Figure9),
    ('Figure10', Figure10),
    ('Figure11', Figure11),
    ('Figure12', Figure12),
    ('Figure13', Figure13),
    ('Figure14', Figure14),
])
