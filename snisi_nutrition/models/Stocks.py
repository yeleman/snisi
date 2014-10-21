#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging

import reversion
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from snisi_core.models.common import pre_save_report, post_save_report
from snisi_core.models.Reporting import (SNISIReport,
                                         PeriodicAggregatedReportInterface,
                                         PERIODICAL_SOURCE,
                                         PERIODICAL_AGGREGATED)

logger = logging.getLogger(__name__)


class AbstractNutritionStocksR(SNISIReport):

    class Meta:
        app_label = 'snisi_nutrition'
        abstract = True

    # Plumpy Nut
    plumpy_nut_initial = models.IntegerField(_("Plumpy Nut Initial"))
    plumpy_nut_received = models.IntegerField(_("Plumpy Nut Received"))
    plumpy_nut_used = models.IntegerField(_("Plumpy Nut Used"))
    plumpy_nut_lost = models.IntegerField(_("Plumpy Nut Lost"))

    @property
    def plumpy_nut_balance(self):
        return self.balance_for('plumpy_nut')

    @property
    def plumpy_nut_stocked(self):
        return self.stocked_for('plumpy_nut')

    @property
    def plumpy_nut_consumed(self):
        return self.consumed_for('plumpy_nut')

    # Plumpy_Sup
    plumpy_sup_initial = models.IntegerField(
        _("Plumpy_Sup Initial"), default=0)
    plumpy_sup_received = models.IntegerField(
        _("Plumpy_Sup Received"), default=0)
    plumpy_sup_used = models.IntegerField(
        _("Plumpy_Sup Used"), default=0)
    plumpy_sup_lost = models.IntegerField(
        _("Plumpy_Sup Lost"), default=0)

    @property
    def plumpy_sup_balance(self):
        return self.balance_for('plumpy_sup')

    @property
    def plumpy_sup_stocked(self):
        return self.stocked_for('plumpy_sup')

    @property
    def plumpy_sup_consumed(self):
        return self.consumed_for('plumpy_sup')

    # Supercereal
    supercereal_initial = models.IntegerField(
        _("Supercereal Initial"), default=0)
    supercereal_received = models.IntegerField(
        _("Supercereal Received"), default=0)
    supercereal_used = models.IntegerField(
        _("Supercereal Used"), default=0)
    supercereal_lost = models.IntegerField(
        _("Supercereal Lost"), default=0)

    @property
    def supercereal_balance(self):
        return self.balance_for('supercereal')

    @property
    def supercereal_stocked(self):
        return self.stocked_for('supercereal')

    @property
    def supercereal_consumed(self):
        return self.consumed_for('supercereal')

    # Supercereal_Plus
    supercereal_plus_initial = models.IntegerField(
        _("Supercereal_Plus Initial"), default=0)
    supercereal_plus_received = models.IntegerField(
        _("Supercereal_Plus Received"), default=0)
    supercereal_plus_used = models.IntegerField(
        _("Supercereal_Plus Used"), default=0)
    supercereal_plus_lost = models.IntegerField(
        _("Supercereal_Plus Lost"), default=0)

    @property
    def supercereal_plus_balance(self):
        return self.balance_for('supercereal_plus')

    @property
    def supercereal_plus_stocked(self):
        return self.stocked_for('supercereal_plus')

    @property
    def supercereal_plus_consumed(self):
        return self.consumed_for('supercereal_plus')

    # Milk_F75
    milk_f75_initial = models.IntegerField(
        _("Milk_F75 Initial"), default=0)
    milk_f75_received = models.IntegerField(
        _("Milk_F75 Received"), default=0)
    milk_f75_used = models.IntegerField(
        _("Milk_F75 Used"), default=0)
    milk_f75_lost = models.IntegerField(
        _("Milk_F75 Lost"), default=0)

    @property
    def milk_f75_balance(self):
        return self.balance_for('milk_f75')

    @property
    def milk_f75_stocked(self):
        return self.stocked_for('milk_f75')

    @property
    def milk_f75_consumed(self):
        return self.consumed_for('milk_f75')

    # Milk_F100
    milk_f100_initial = models.IntegerField(
        _("Milk_F100 Initial"), default=0)
    milk_f100_received = models.IntegerField(
        _("Milk_F100 Received"), default=0)
    milk_f100_used = models.IntegerField(
        _("Milk_F100 Used"), default=0)
    milk_f100_lost = models.IntegerField(
        _("Milk_F100 Lost"), default=0)

    @property
    def milk_f100_balance(self):
        return self.balance_for('milk_f100')

    @property
    def milk_f100_stocked(self):
        return self.stocked_for('milk_f100')

    @property
    def milk_f100_consumed(self):
        return self.consumed_for('milk_f100')

    # Resomal
    resomal_initial = models.IntegerField(
        _("Resomal Initial"), default=0)
    resomal_received = models.IntegerField(
        _("Resomal Received"), default=0)
    resomal_used = models.IntegerField(
        _("Resomal Used"), default=0)
    resomal_lost = models.IntegerField(
        _("Resomal Lost"), default=0)

    @property
    def resomal_balance(self):
        return self.balance_for('resomal')

    @property
    def resomal_stocked(self):
        return self.stocked_for('resomal')

    @property
    def resomal_consumed(self):
        return self.consumed_for('resomal')

    # Csb_Plus
    csb_plus_initial = models.IntegerField(
        _("Csb_Plus Initial"), default=0)
    csb_plus_received = models.IntegerField(
        _("Csb_Plus Received"), default=0)
    csb_plus_used = models.IntegerField(
        _("Csb_Plus Used"), default=0)
    csb_plus_lost = models.IntegerField(
        _("Csb_Plus Lost"), default=0)

    @property
    def csb_plus_balance(self):
        return self.balance_for('csb_plus')

    @property
    def csb_plus_stocked(self):
        return self.stocked_for('csb_plus')

    @property
    def csb_plus_consumed(self):
        return self.consumed_for('csb_plus')

    # Sugar
    sugar_initial = models.IntegerField(
        _("Sugar Initial"), default=0)
    sugar_received = models.IntegerField(
        _("Sugar Received"), default=0)
    sugar_used = models.IntegerField(
        _("Sugar Used"), default=0)
    sugar_lost = models.IntegerField(
        _("Sugar Lost"), default=0)

    @property
    def sugar_balance(self):
        return self.balance_for('sugar')

    @property
    def sugar_stocked(self):
        return self.stocked_for('sugar')

    @property
    def sugar_consumed(self):
        return self.consumed_for('sugar')

    # Oil
    oil_initial = models.IntegerField(
        _("Oil Initial"), default=0)
    oil_received = models.IntegerField(
        _("Oil Received"), default=0)
    oil_used = models.IntegerField(
        _("Oil Used"), default=0)
    oil_lost = models.IntegerField(
        _("Oil Lost"), default=0)

    @property
    def oil_balance(self):
        return self.balance_for('oil')

    @property
    def oil_stocked(self):
        return self.stocked_for('oil')

    @property
    def oil_consumed(self):
        return self.consumed_for('oil')

    # Cereals
    cereals_initial = models.IntegerField(
        _("Cereals Initial"), default=0)
    cereals_received = models.IntegerField(
        _("Cereals Received"), default=0)
    cereals_used = models.IntegerField(
        _("Cereals Used"), default=0)
    cereals_lost = models.IntegerField(
        _("Cereals Lost"), default=0)

    @property
    def cereals_balance(self):
        return self.balance_for('cereals')

    @property
    def cereals_stocked(self):
        return self.stocked_for('cereals')

    @property
    def cereals_consumed(self):
        return self.consumed_for('cereals')

    # Legumes
    legumes_initial = models.IntegerField(
        _("Legumes Initial"), default=0)
    legumes_received = models.IntegerField(
        _("Legumes Received"), default=0)
    legumes_used = models.IntegerField(
        _("Legumes Used"), default=0)
    legumes_lost = models.IntegerField(
        _("Legumes Lost"), default=0)

    @property
    def legumes_balance(self):
        return self.balance_for('legumes')

    @property
    def legumes_stocked(self):
        return self.stocked_for('legumes')

    @property
    def legumes_consumed(self):
        return self.consumed_for('legumes')

    # Amoxycilline_Vials
    amoxycilline_vials_initial = models.IntegerField(
        _("Amoxycilline_Vials Initial"), default=0)
    amoxycilline_vials_received = models.IntegerField(
        _("Amoxycilline_Vials Received"), default=0)
    amoxycilline_vials_used = models.IntegerField(
        _("Amoxycilline_Vials Used"), default=0)
    amoxycilline_vials_lost = models.IntegerField(
        _("Amoxycilline_Vials Lost"), default=0)

    @property
    def amoxycilline_vials_balance(self):
        return self.balance_for('amoxycilline_vials')

    @property
    def amoxycilline_vials_stocked(self):
        return self.stocked_for('amoxycilline_vials')

    @property
    def amoxycilline_vials_consumed(self):
        return self.consumed_for('amoxycilline_vials')

    # Amoxycilline_Caps
    amoxycilline_caps_initial = models.IntegerField(
        _("Amoxycilline_Caps Initial"), default=0)
    amoxycilline_caps_received = models.IntegerField(
        _("Amoxycilline_Caps Received"), default=0)
    amoxycilline_caps_used = models.IntegerField(
        _("Amoxycilline_Caps Used"), default=0)
    amoxycilline_caps_lost = models.IntegerField(
        _("Amoxycilline_Caps Lost"), default=0)

    @property
    def amoxycilline_caps_balance(self):
        return self.balance_for('amoxycilline_caps')

    @property
    def amoxycilline_caps_stocked(self):
        return self.stocked_for('amoxycilline_caps')

    @property
    def amoxycilline_caps_consumed(self):
        return self.consumed_for('amoxycilline_caps')

    # Ceftriaxone
    ceftriaxone_initial = models.IntegerField(
        _("Ceftriaxone Initial"), default=0)
    ceftriaxone_received = models.IntegerField(
        _("Ceftriaxone Received"), default=0)
    ceftriaxone_used = models.IntegerField(
        _("Ceftriaxone Used"), default=0)
    ceftriaxone_lost = models.IntegerField(
        _("Ceftriaxone Lost"), default=0)

    @property
    def ceftriaxone_balance(self):
        return self.balance_for('ceftriaxone')

    @property
    def ceftriaxone_stocked(self):
        return self.stocked_for('ceftriaxone')

    @property
    def ceftriaxone_consumed(self):
        return self.consumed_for('ceftriaxone')

    # Albendazole
    albendazole_initial = models.IntegerField(
        _("Albendazole Initial"), default=0)
    albendazole_received = models.IntegerField(
        _("Albendazole Received"), default=0)
    albendazole_used = models.IntegerField(
        _("Albendazole Used"), default=0)
    albendazole_lost = models.IntegerField(
        _("Albendazole Lost"), default=0)

    @property
    def albendazole_balance(self):
        return self.balance_for('albendazole')

    @property
    def albendazole_stocked(self):
        return self.stocked_for('albendazole')

    @property
    def albendazole_consumed(self):
        return self.consumed_for('albendazole')

    # Vita_100_Injectable
    vita_100_injectable_initial = models.IntegerField(
        _("Vita_100_Injectable Initial"), default=0)
    vita_100_injectable_received = models.IntegerField(
        _("Vita_100_Injectable Received"), default=0)
    vita_100_injectable_used = models.IntegerField(
        _("Vita_100_Injectable Used"), default=0)
    vita_100_injectable_lost = models.IntegerField(
        _("Vita_100_Injectable Lost"), default=0)

    @property
    def vita_100_injectable_balance(self):
        return self.balance_for('vita_100_injectable')

    @property
    def vita_100_injectable_stocked(self):
        return self.stocked_for('vita_100_injectable')

    @property
    def vita_100_injectable_consumed(self):
        return self.consumed_for('vita_100_injectable')

    # Vita_200_Injectable
    vita_200_injectable_initial = models.IntegerField(
        _("Vita_200_Injectable Initial"), default=0)
    vita_200_injectable_received = models.IntegerField(
        _("Vita_200_Injectable Received"), default=0)
    vita_200_injectable_used = models.IntegerField(
        _("Vita_200_Injectable Used"), default=0)
    vita_200_injectable_lost = models.IntegerField(
        _("Vita_200_Injectable Lost"), default=0)

    @property
    def vita_200_injectable_balance(self):
        return self.balance_for('vita_200_injectable')

    @property
    def vita_200_injectable_stocked(self):
        return self.stocked_for('vita_200_injectable')

    @property
    def vita_200_injectable_consumed(self):
        return self.consumed_for('vita_200_injectable')

    # Nystatine_Syrup
    nystatine_syrup_initial = models.IntegerField(
        _("Nystatine_Syrup Initial"), default=0)
    nystatine_syrup_received = models.IntegerField(
        _("Nystatine_Syrup Received"), default=0)
    nystatine_syrup_used = models.IntegerField(
        _("Nystatine_Syrup Used"), default=0)
    nystatine_syrup_lost = models.IntegerField(
        _("Nystatine_Syrup Lost"), default=0)

    @property
    def nystatine_syrup_balance(self):
        return self.balance_for('nystatine_syrup')

    @property
    def nystatine_syrup_stocked(self):
        return self.stocked_for('nystatine_syrup')

    @property
    def nystatine_syrup_consumed(self):
        return self.consumed_for('nystatine_syrup')

    # Nystatine_Tabs
    nystatine_tabs_initial = models.IntegerField(
        _("Nystatine_Tabs Initial"), default=0)
    nystatine_tabs_received = models.IntegerField(
        _("Nystatine_Tabs Received"), default=0)
    nystatine_tabs_used = models.IntegerField(
        _("Nystatine_Tabs Used"), default=0)
    nystatine_tabs_lost = models.IntegerField(
        _("Nystatine_Tabs Lost"), default=0)

    @property
    def nystatine_tabs_balance(self):
        return self.balance_for('nystatine_tabs')

    @property
    def nystatine_tabs_stocked(self):
        return self.stocked_for('nystatine_tabs')

    @property
    def nystatine_tabs_consumed(self):
        return self.consumed_for('nystatine_tabs')

    # Folic_Acid
    folic_acid_initial = models.IntegerField(
        _("Folic_Acid Initial"), default=0)
    folic_acid_received = models.IntegerField(
        _("Folic_Acid Received"), default=0)
    folic_acid_used = models.IntegerField(
        _("Folic_Acid Used"), default=0)
    folic_acid_lost = models.IntegerField(
        _("Folic_Acid Lost"), default=0)

    @property
    def folic_acid_balance(self):
        return self.balance_for('folic_acid')

    @property
    def folic_acid_stocked(self):
        return self.stocked_for('folic_acid')

    @property
    def folic_acid_consumed(self):
        return self.consumed_for('folic_acid')

    # Iron
    iron_initial = models.IntegerField(
        _("Iron Initial"), default=0)
    iron_received = models.IntegerField(
        _("Iron Received"), default=0)
    iron_used = models.IntegerField(
        _("Iron Used"), default=0)
    iron_lost = models.IntegerField(
        _("Iron Lost"), default=0)

    @property
    def iron_balance(self):
        return self.balance_for('iron')

    @property
    def iron_stocked(self):
        return self.stocked_for('iron')

    @property
    def iron_consumed(self):
        return self.consumed_for('iron')

    # Iron_Folic_Acid
    iron_folic_acid_initial = models.IntegerField(
        _("Iron_Folic_Acid Initial"), default=0)
    iron_folic_acid_received = models.IntegerField(
        _("Iron_Folic_Acid Received"), default=0)
    iron_folic_acid_used = models.IntegerField(
        _("Iron_Folic_Acid Used"), default=0)
    iron_folic_acid_lost = models.IntegerField(
        _("Iron_Folic_Acid Lost"), default=0)

    @property
    def iron_folic_acid_balance(self):
        return self.balance_for('iron_folic_acid')

    @property
    def iron_folic_acid_stocked(self):
        return self.stocked_for('iron_folic_acid')

    @property
    def iron_folic_acid_consumed(self):
        return self.consumed_for('iron_folic_acid')

    # subroutines
    def consumed_for(self, field):
        return sum([getattr(self, '{}_used'.format(field), 0),
                    getattr(self, '{}_lost'.format(field), 0)])

    def stocked_for(self, field):
        return sum([getattr(self, '{}_initial'.format(field), 0),
                    getattr(self, '{}_received'.format(field), 0)])

    def balance_for(self, field):
        return self.stocked_for(field) - self.consumed_for(field)


class NutritionStocksR(AbstractNutritionStocksR):

    REPORTING_TYPE = PERIODICAL_SOURCE
    RECEIPT_FORMAT = "{period__year_short}{period__month}NUTST-{dow}/{rand}"
    UNIQUE_TOGETHER = ('period', 'entity')

    class Meta:
        app_label = 'snisi_nutrition'
        verbose_name = _("Nutrition Inputs Report")
        verbose_name_plural = _("Nutrition Inputs Reports")


receiver(pre_save, sender=NutritionStocksR)(pre_save_report)
receiver(post_save, sender=NutritionStocksR)(post_save_report)

reversion.register(NutritionStocksR)


class AggNutritionStocksR(AbstractNutritionStocksR,
                          PeriodicAggregatedReportInterface, SNISIReport):

    REPORTING_TYPE = PERIODICAL_AGGREGATED
    RECEIPT_FORMAT = "{period__year_short}{period__month}NUTSTa-{dow}/{rand}"
    INDIVIDUAL_CLS = NutritionStocksR
    UNIQUE_TOGETHER = [('period', 'entity')]

    class Meta:
        app_label = 'snisi_nutrition'
        verbose_name = _("Aggregated Nutrition Inputs Report")
        verbose_name_plural = _("Aggregated Nutrition Inputs Reports")

    indiv_sources = models.ManyToManyField(
        INDIVIDUAL_CLS,
        verbose_name=_(u"Primary. Sources"),
        blank=True, null=True,
        related_name='source_agg_%(class)s_reports')

    @classmethod
    def update_instance_with_indiv(cls, report, instance):

        cls.update_instance_with_indiv_meta(report, instance)

        for field in cls.data_fields():
            setattr(report, field,
                    getattr(report, field, 0) + getattr(instance, field, 0))

    @classmethod
    def update_instance_with_agg(cls, report, instance):

        cls.update_instance_with_agg_meta(report, instance)

        for field in cls.data_fields():
            setattr(report, field,
                    getattr(report, field, 0) + getattr(instance, field, 0))


receiver(pre_save, sender=AggNutritionStocksR)(pre_save_report)
receiver(post_save, sender=AggNutritionStocksR)(post_save_report)

reversion.register(AggNutritionStocksR)
