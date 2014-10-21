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


class AbstractNutritionR(SNISIReport):

    class Meta:
        app_label = 'snisi_nutrition'
        abstract = True


class NutritionR(AbstractNutritionR):

    REPORTING_TYPE = PERIODICAL_SOURCE
    RECEIPT_FORMAT = "{period}-NUT/{rand}"
    UNIQUE_TOGETHER = ('period', 'entity')

    class Meta:
        app_label = 'snisi_nutrition'
        verbose_name = _("Nutrition Report")
        verbose_name_plural = _("Nutrition Reports")

    urenam_report = models.ForeignKeyField(
        'URENAMNutritionR', null=True, blank=True, related_name='nutritionr')
    urenas_report = models.ForeignKeyField(
        'URENASNutritionR', null=True, blank=True, related_name='nutritionr')
    ureni_report = models.ForeignKeyField(
        'URENINutritionR', null=True, blank=True, related_name='nutritionr')


receiver(pre_save, sender=NutritionR)(pre_save_report)
receiver(post_save, sender=NutritionR)(post_save_report)

reversion.register(NutritionR)


class AggNutritionR(AbstractNutritionR,
                    PeriodicAggregatedReportInterface, SNISIReport):

    REPORTING_TYPE = PERIODICAL_AGGREGATED
    RECEIPT_FORMAT = "{period}-NUTa/{rand}"
    INDIVIDUAL_CLS = NutritionR
    UNIQUE_TOGETHER = [('period', 'entity')]

    class Meta:
        app_label = 'snisi_nutrition'
        verbose_name = _("Aggregated Nutrition Report")
        verbose_name_plural = _("Aggregated Nutrition Reports")

    urenam_report = models.ForeignKeyField(
        'AggURENAMNutritionR', null=True, blank=True,
        related_name='agg_nutritionr')
    urenas_report = models.ForeignKeyField(
        'AggURENASNutritionR', null=True, blank=True,
        related_name='agg_nutritionr')
    ureni_report = models.ForeignKeyField(
        'AggURENINutritionR', null=True, blank=True,
        related_name='agg_nutritionr')

    indiv_sources = models.ManyToManyField(
        INDIVIDUAL_CLS,
        verbose_name=_(u"Primary. Sources"),
        blank=True, null=True,
        related_name='source_agg_%(class)s_reports')

    @classmethod
    def update_instance_with_indiv(cls, report, instance):

        cls.update_instance_with_indiv_meta(report, instance)

    @classmethod
    def update_instance_with_agg(cls, report, instance):

        cls.update_instance_with_agg_meta(report, instance)


receiver(pre_save, sender=AggNutritionR)(pre_save_report)
receiver(post_save, sender=AggNutritionR)(post_save_report)

reversion.register(AggNutritionR)
