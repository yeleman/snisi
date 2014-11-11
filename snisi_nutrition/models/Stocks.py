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

from snisi_core.models.Entities import Entity
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

    INPUTS_LABELS = {
        'plumpy_nut': "Plumpy Nut",
        'milk_f75': "Milk F75",
        'milk_f100': "Milk F100",
        'resomal': "Resomal",
        'plumpy_sup': "Plumpy Sup",
        'supercereal': "Supercereal",
        'supercereal_plus': "Supercereal+",
        'oil': "Oil",
        'amoxycilline_125_vials': "Amoxycilline 125",
        'amoxycilline_250_caps': "Amoxycilline 250",
        'albendazole_400': "Albendazole",
        'vita_100_injectable': "Vitamin A 100",
        'vita_200_injectable': "Vitamin A 200",
        'iron_folic_acid': "Iron/Folic Acid"
    }

    @classmethod
    def input_str(cls, input_slug):
        return cls.INPUTS_LABELS.get(input_slug)

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

    # Amoxycilline 125mg Vials
    amoxycilline_125_vials_initial = models.IntegerField(
        _("Amoxycilline_125_Vials Initial"), default=0)
    amoxycilline_125_vials_received = models.IntegerField(
        _("Amoxycilline_125_Vials Received"), default=0)
    amoxycilline_125_vials_used = models.IntegerField(
        _("Amoxycilline_125_Vials Used"), default=0)
    amoxycilline_125_vials_lost = models.IntegerField(
        _("Amoxycilline_125_Vials Lost"), default=0)

    @property
    def amoxycilline_125_vials_balance(self):
        return self.balance_for('amoxycilline_125_vials')

    @property
    def amoxycilline_125_vials_stocked(self):
        return self.stocked_for('amoxycilline_125_vials')

    @property
    def amoxycilline_125_vials_consumed(self):
        return self.consumed_for('amoxycilline_125_vials')

    # Amoxycilline 250mg Caps
    amoxycilline_250_caps_initial = models.IntegerField(
        _("Amoxycilline_250_Caps Initial"), default=0)
    amoxycilline_250_caps_received = models.IntegerField(
        _("Amoxycilline_250_Caps Received"), default=0)
    amoxycilline_250_caps_used = models.IntegerField(
        _("Amoxycilline_250_Caps Used"), default=0)
    amoxycilline_250_caps_lost = models.IntegerField(
        _("Amoxycilline_250_Caps Lost"), default=0)

    @property
    def amoxycilline_250_caps_balance(self):
        return self.balance_for('amoxycilline_250_caps')

    @property
    def amoxycilline_250_caps_stocked(self):
        return self.stocked_for('amoxycilline_250_caps')

    @property
    def amoxycilline_250_caps_consumed(self):
        return self.consumed_for('amoxycilline_250_caps')

    # Albendazole 400mg
    albendazole_400_initial = models.IntegerField(
        _("Albendazole Initial"), default=0)
    albendazole_400_received = models.IntegerField(
        _("Albendazole Received"), default=0)
    albendazole_400_used = models.IntegerField(
        _("Albendazole Used"), default=0)
    albendazole_400_lost = models.IntegerField(
        _("Albendazole Lost"), default=0)

    @property
    def albendazole_400_balance(self):
        return self.balance_for('albendazole')

    @property
    def albendazole_400_stocked(self):
        return self.stocked_for('albendazole')

    @property
    def albendazole_400_consumed(self):
        return self.consumed_for('albendazole')

    # VitA 100K UI Injectable
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

    # VitA 200K UI Injectable
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

    @classmethod
    def consumed_for_dict(cls, data, field):
        return sum([data.get('{}_used'.format(field), 0),
                    data.get('{}_lost'.format(field), 0)])

    @classmethod
    def stocked_for_dict(cls, data, field):
        return sum([data.get('{}_initial'.format(field), 0),
                    data.get('{}_received'.format(field), 0)])

    @classmethod
    def balance_for_dict(cls, data, field):
        return cls.stocked_for_dict(data, field) \
            - cls.consumed_for_dict(data, field)

    @classmethod
    def inputs(cls, ureni_only=False):
        if ureni_only:
            return ['milk_f75', 'milk_f100', 'resomal']

        return ['plumpy_nut',
                'milk_f75',
                'milk_f100',
                'resomal',
                'plumpy_sup',
                'supercereal',
                'supercereal_plus',
                'oil',
                'amoxycilline_125_vials',
                'amoxycilline_250_caps',
                'albendazole_400',
                'vita_100_injectable',
                'vita_200_injectable',
                'iron_folic_acid']

    def line_data(self):
        e = Entity.get_or_none(self.entity.slug)
        lines = []
        for inp in self.inputs():
            if not e.has_ureni and inp in self.inputs(ureni_only=True):
                continue

            d = {'label': self.input_str(inp),
                 'unit': '-'}

            suffixes = ['initial', 'received', 'used', 'lost']
            auto_suffixes = ['balance', 'consumed', 'stocked']

            for suffix in auto_suffixes + suffixes:
                value = getattr(self, '{}_{}'.format(inp, suffix))
                if suffix in auto_suffixes:
                    full_slug = '{}_{}'.format(inp, suffix)
                else:
                    full_slug = 'stocks_{}_{}'.format(inp, suffix)
                d[suffix] = value
                d[suffix + '_full_slug'] = full_slug

            lines.append(d)
        return lines


class NutritionStocksR(AbstractNutritionStocksR):

    REPORTING_TYPE = PERIODICAL_SOURCE
    RECEIPT_FORMAT = "{period__year_short}{period__month}NUTST-{dow}/{rand}"
    UNIQUE_TOGETHER = [('period', 'entity')]

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
