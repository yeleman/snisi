#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

# from snisi_malaria.models import MalariaR
# from snisi_malaria.indicators.common import MalariaIndicator #, gen_shortcut
# from snisi_malaria.indicators.section1 import NumberOfHealthUnitsReporting
# from snisi_core.indicators import IndicatorTable

# class PourcentageStructuresRuptureStockCTADistrict(IndicatorTable):
#     """ Tableau: Pourcentage de structures avec Rupture de stock de CTA dans

#         le district """

#     name = "Tableau 17"
#     title = " "
#     caption = ("Pourcentage de structures sans Rupture de stock de CTA dans "
#                "le district"
#     rendering_type = 'table'
#     add_percentage = True

#     INDICATORS = [
#         gen_shortcut('u5_total_distributed_bednets',
#                      "Nombre MILD distribuées aux enfants de moins de 5 ans"),
#         gen_shortcut('pw_total_distributed_bednets',
#                      "Nombre de MILD distribuées aux femmes enceintes"),
#     ]

#     def period_is_valid(self, period):
#         return True

#     @reference
#     @indicator(0)
#     @label("Nombre total de structures dans le district")
#     def total_structures_in_the_district(self, period):
#         if self.entity.type.slug == 'cscom':
#             return 1
#         else:
#             return self.entity.get_descendants()\
#                               .filter(type__slug='cscom').count()

#     @indicator(1, 'total_structures_in_the_district')
#     @label("Structures sans rupture de stock en CTA Nourrisson - Enfant")
#     def stockout_act_children(self, period):
#         nb_act_children = nb_stockout(self.entity, period, 'act_children')
#         return nb_act_children

#     @indicator(2, 'total_structures_in_the_district')
#     @label("Structures sans rupture de stock en CTA Adolescent")
#     def stockout_act_youth(self, period):
#         nb_act_youth = nb_stockout(self.entity, period, 'act_youth')
#         return nb_act_youth

#     @indicator(3, 'total_structures_in_the_district')
#     @label("Structures sans rupture de stock en CTA Adulte")
#     def stockout_act_adult(self, period):
#         nb_act_adult = nb_stockout(self.entity, period, 'act_adult')
#         return nb_act_adult


# class EvolutionPourcentageStructuresRuptureStockCTA(IndicatorTable):
#     """ Graphe: Evolution du pourcentage de Structures avec rupture de stock en

#         CTA """

#     name = "Figure 27"
#     title = " "
#     caption = "Evolution du pourcentage de Structures sans rupture de " \
#               "stock en CTA (Nourrisson-Enfant, Adolescent, Adulte"
#     type = 'graph'
#     graph_type = 'spline'

#     default_options = {'with_percentage': True, \
#                        'with_reference': False, \
#                        'with_data': False,
#                        'only_percent': True}

#     def period_is_valid(self, period):
#         return MalariaReport.validated.filter(entity=self.entity, \
#                                               period=period).count() > 0

#     @reference
#     @indicator(0)
#     def total_structures_in_the_district(self, period):
#         return self.entity.get_descendants()\
#                               .filter(type__slug='cscom').count()

#     @indicator(1, 'total_structures_in_the_district')
#     @label("CTA Nourrisson - Enfant")
#     def stockout_act_children(self, period):
#         nb_act_children = nb_stockout(self.entity, period, 'act_children')
#         return nb_act_children

#     @indicator(2, 'total_structures_in_the_district')
#     @label("CTA Adolescent")
#     def stockout_act_youth(self, period):
#         nb_act_youth = nb_stockout(self.entity, period, 'act_youth')
#         return nb_act_youth

#     @indicator(3, 'total_structures_in_the_district')
#     @label("CTA Adulte")
#     def stockout_act_adult(self, period):
#         nb_act_adult = nb_stockout(self.entity, period, 'act_adult')
#         return nb_act_adult

# WIDGETS = [PourcentageStructuresRuptureStockCTADistrict,
#            EvolutionPourcentageStructuresRuptureStockCTA]
WIDGETS = []
TITLE = "Gestion de stock de CTA"
