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
from snisi_core.models.Reporting import (PeriodicAggregatedReportInterface,
                                         PERIODICAL_SOURCE,
                                         PERIODICAL_AGGREGATED,
                                         SNISIReport)
from snisi_nutrition.models.Common import AbstractURENutritionR

logger = logging.getLogger(__name__)


class AbstractURENASNutritionR(AbstractURENutritionR):

    class Meta:
        app_label = 'snisi_nutrition'
        abstract = True

    IS_URENAS = True

    # 6-59 months
    u59o6_total_start_m = models.PositiveIntegerField(
        _("[6-59m] Start of Month Male"))
    u59o6_total_start_f = models.PositiveIntegerField(
        _("[6-59m] Start of Month Female"))

    u59o6_new_cases = models.PositiveIntegerField(
        _("[6-59m] New Cases"))
    u59o6_returned = models.PositiveIntegerField(
        _("[6-59m] Returned"))
    u59o6_total_in_m = models.PositiveIntegerField(
        _("[6-59m] Total Admitted Male"))
    u59o6_total_in_f = models.PositiveIntegerField(
        _("[6-59m] Total Admitted Female"))
    u59o6_transferred = models.PositiveIntegerField(
        _("[6-59m] Transferred from URENI"))

    u59o6_healed = models.PositiveIntegerField(
        _("[6-59m] Healed"))
    u59o6_deceased = models.PositiveIntegerField(
        _("[6-59m] Deceased"))
    u59o6_abandon = models.PositiveIntegerField(
        _("[6-59m] Abandon"))
    u59o6_not_responding = models.PositiveIntegerField(
        _("[6-59m] Not Responding"))
    u59o6_total_out_m = models.PositiveIntegerField(
        _("[6-59m] Total Out Male"))
    u59o6_total_out_f = models.PositiveIntegerField(
        _("[6-59m] Total Out Female"))

    u59o6_referred = models.PositiveIntegerField(
        _("[6-59m] Referred"))

    u59o6_total_end_m = models.PositiveIntegerField(
        _("[6-59m] End of Month Male"))
    u59o6_total_end_f = models.PositiveIntegerField(
        _("[6-59m] End of Month Female"))

    # Over 59 months
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
    o59_not_responding = models.PositiveIntegerField(
        _("[59m+] Not Responding"))
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

    # 6-59 months
    @property
    def u59o6_total_start(self):
        return self.age_sum_for('u59o6', ['total_start_m', 'total_start_f'])

    @property
    def u59o6_total_in(self):
        return self.age_sum_for('u59o6', ['total_in_m', 'total_in_f'])

    @property
    def u59o6_grand_total_in(self):
        return self.age_sum_for('u59o6', ['total_in', 'transferred'])

    @property
    def u59o6_total_out(self):
        return self.age_sum_for('u59o6', ['total_out_m', 'total_out_f'])

    @property
    def u59o6_grand_total_out(self):
        return self.age_sum_for('u59o6', ['total_out', 'referred'])

    @property
    def u59o6_total_end(self):
        return self.age_sum_for('u59o6', ['total_end_m', 'total_end_f'])

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
    def o59_total_out(self):
        return self.age_sum_for('o59', ['total_out_m', 'total_out_f'])

    @property
    def o59_grand_total_out(self):
        return self.age_sum_for('o59', ['total_out', 'referred'])

    @property
    def o59_total_end(self):
        return self.age_sum_for('o59', ['total_end_m', 'total_end_f'])

    @classmethod
    def age_groups(cls):
        return ['u59o6', 'o59']

    @classmethod
    def comp_age_groups(cls):
        return ['u59o6']


class URENASNutritionR(AbstractURENASNutritionR):

    REPORTING_TYPE = PERIODICAL_SOURCE
    RECEIPT_FORMAT = "{period__year_short}{period__month}" \
                     "NAS-{dow}/{entity__slug}-{rand}"
    UNIQUE_TOGETHER = [('period', 'entity')]

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
    RECEIPT_FORMAT = "{period__year_short}{period__month}" \
                     "NASa-{dow}/{entity__slug}-{rand}"
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

    direct_indiv_sources = models.ManyToManyField(
        INDIVIDUAL_CLS,
        verbose_name=_("Primary. Sources (direct)"),
        blank=True, null=True,
        related_name='direct_source_agg_%(class)s_reports')

    @classmethod
    def create_from(cls, period, entity, created_by,
                    indiv_sources=None, agg_sources=None):

        if indiv_sources is None:
            if entity.type.slug in ('health_center', 'health_district'):
                indiv_sources = cls.INDIVIDUAL_CLS.objects.filter(
                    period__start_on__gte=period.start_on,
                    period__end_on__lte=period.end_on) \
                    .filter(entity__in=entity.get_health_centers())
            else:
                indiv_sources = []

        if agg_sources is None and not len(indiv_sources):
            agg_sources = cls.objects.filter(
                period__start_on__gte=period.start_on,
                period__end_on__lte=period.end_on) \
                .filter(entity__in=entity.get_natural_children(
                    skip_slugs=['health_area']))

        return super(cls, cls).create_from(
            period=period,
            entity=entity,
            created_by=created_by,
            indiv_sources=indiv_sources,
            agg_sources=agg_sources)

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
