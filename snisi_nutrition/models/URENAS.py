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


class AbstractURENASNutritionR(SNISIReport):

    class Meta:
        app_label = 'snisi_nutrition'
        abstract = True

    # 6-59 months
    u59_total_start_m = models.PositiveIntegerField(
        _("[6-59m] Start of Month Male"))
    u59_total_start_f = models.PositiveIntegerField(
        _("[6-59m] Start of Month Female"))

    u59_new_cases = models.PositiveIntegerField(
        _("[6-59m] New Cases"))
    u59_returned = models.PositiveIntegerField(
        _("[6-59m] Returned"))
    u59_total_in_m = models.PositiveIntegerField(
        _("[6-59m] Total Admitted Male"))
    u59_total_in_f = models.PositiveIntegerField(
        _("[6-59m] Total Admitted Female"))
    u59_transferred = models.PositiveIntegerField(
        _("[6-59m] Transferred from URENI"))

    u59_healed = models.PositiveIntegerField(
        _("[6-59m] Healed"))
    u59_deceased = models.PositiveIntegerField(
        _("[6-59m] Deceased"))
    u59_abandon = models.PositiveIntegerField(
        _("[6-59m] Abandon"))
    u59_total_out_m = models.PositiveIntegerField(
        _("[6-59m] Total Out Male"))
    u59_total_out_f = models.PositiveIntegerField(
        _("[6-59m] Total Out Female"))

    u59_referred = models.PositiveIntegerField(
        _("[6-59m] Referred"))

    u59_total_end_m = models.PositiveIntegerField(
        _("[6-59m] End of Month Male"))
    u59_total_end_f = models.PositiveIntegerField(
        _("[6-59m] End of Month Female"))

    # Pregnant & Breast Feeding Women
    o59_total_start_m = models.PositiveIntegerField(
        _("[59m+] Start of Month Male"))
    o59_total_start_f = models.PositiveIntegerField(
        _("[59m+] Start of Month Female"))

    o59_new_cases = models.PositiveIntegerField(
        _("[59m+] New Cases"))
    o59_returned = models.PositiveIntegerField(
        _("[59m+] Returned"))
    o59_total_in_m = models.PositiveIntegerField(
        _("[59m+] Total Admitted Male"))
    o59_total_in_f = models.PositiveIntegerField(
        _("[59m+] Total Admitted Female"))
    o59_transferred = models.PositiveIntegerField(
        _("[59m+] Transferred from URENI"))

    o59_healed = models.PositiveIntegerField(
        _("[59m+] Healed"))
    o59_deceased = models.PositiveIntegerField(
        _("[59m+] Deceased"))
    o59_abandon = models.PositiveIntegerField(
        _("[59m+] Abandon"))
    o59_total_out_m = models.PositiveIntegerField(
        _("[59m+] Total Out Male"))
    o59_total_out_f = models.PositiveIntegerField(
        _("[59m+] Total Out Female"))

    o59_referred = models.PositiveIntegerField(
        _("[59m+] Referred"))

    o59_total_end_m = models.PositiveIntegerField(
        _("[59m+] End of Month Male"))
    o59_total_end_f = models.PositiveIntegerField(
        _("[59m+] End of Month Female"))

    def age_sum_for(self, age, fields):
        return sum([getattr(self, '{}_{}'.format(age, field))
                    for field in fields])

    # 6-59 months
    @property
    def u59_total_start(self):
        return self.age_sum_for('u59', ['total_start_m', 'total_start_f'])

    @property
    def u59_total_in(self):
        return self.age_sum_for('u59', ['total_in_m', 'total_in_f'])

    @property
    def u59_grand_total_in(self):
        return self.age_sum_for('u59', ['total_in', 'transferred'])

    @property
    def u59_not_responding(self):
        return 0

    @property
    def u59_total_out(self):
        return self.age_sum_for('u59', ['total_out_m', 'total_out_f'])

    @property
    def u59_grand_total_out(self):
        return self.age_sum_for('u59', ['total_out', 'referred'])

    @property
    def u59_total_end(self):
        return self.age_sum_for('u59', ['total_end_m', 'total_end_f'])

    # Over 59 months
    @property
    def o59_total_start(self):
        return self.age_sum_for('o59', ['total_start_m', 'total_start_f'])

    @property
    def o59_total_in(self):
        return self.age_sum_for('o59', ['total_in_m', 'total_in_f'])

    @property
    def o59_grand_total_in(self):
        return self.age_sum_for('o59', ['total_in', 'transferred'])

    @property
    def o59_not_responding(self):
        return 0

    @property
    def o59_total_out(self):
        return self.age_sum_for('o59', ['total_out_m', 'total_out_f'])

    @property
    def o59_grand_total_out(self):
        return self.age_sum_for('o59', ['total_out', 'referred'])

    @property
    def o59_total_end(self):
        return self.age_sum_for('o59', ['total_end_m', 'total_end_f'])


class URENASNutritionR(AbstractURENASNutritionR):

    REPORTING_TYPE = PERIODICAL_SOURCE
    RECEIPT_FORMAT = "{period__year_short}{period__month}NAS-{dow}/{rand}"
    UNIQUE_TOGETHER = ('period', 'entity')

    class Meta:
        app_label = 'snisi_nutrition'
        verbose_name = _("URENAS Report")
        verbose_name_plural = _("URENAS Reports")


receiver(pre_save, sender=URENASNutritionR)(pre_save_report)
receiver(post_save, sender=URENASNutritionR)(post_save_report)

reversion.register(URENASNutritionR)


class AggURENASNutritionR(AbstractURENASNutritionR,
                          PeriodicAggregatedReportInterface, SNISIReport):

    REPORTING_TYPE = PERIODICAL_AGGREGATED
    RECEIPT_FORMAT = "{period__year_short}{period__month}NASa-{dow}/{rand}"
    INDIVIDUAL_CLS = URENASNutritionR
    UNIQUE_TOGETHER = [('period', 'entity')]

    class Meta:
        app_label = 'snisi_nutrition'
        verbose_name = _("Aggregated URENAS Report")
        verbose_name_plural = _("Aggregated URENAS Reports")

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


receiver(pre_save, sender=AggURENASNutritionR)(pre_save_report)
receiver(post_save, sender=AggURENASNutritionR)(post_save_report)

reversion.register(AggURENASNutritionR)
