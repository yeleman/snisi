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


class AbstractURENAMNutritionR(AbstractURENutritionR):

    class Meta:
        app_label = 'snisi_nutrition'
        abstract = True

    IS_URENAM = True

    # 6-23 months
    u23o6_total_start_m = models.PositiveIntegerField(
        _("[6-23m] Start of Month Male"))
    u23o6_total_start_f = models.PositiveIntegerField(
        _("[6-23m] Start of Month Female"))

    u23o6_new_cases = models.PositiveIntegerField(
        _("[6-23m] New Cases"))
    u23o6_returned = models.PositiveIntegerField(
        _("[6-23m] Returned"))
    u23o6_total_in_m = models.PositiveIntegerField(
        _("[6-23m] Total Admitted Male"))
    u23o6_total_in_f = models.PositiveIntegerField(
        _("[6-23m] Total Admitted Female"))

    u23o6_healed = models.PositiveIntegerField(
        _("[6-23m] Healed"))
    u23o6_deceased = models.PositiveIntegerField(
        _("[6-23m] Deceased"))
    u23o6_abandon = models.PositiveIntegerField(
        _("[6-23m] Abandon"))

    u23o6_not_responding = models.PositiveIntegerField(
        _("[6-23m] Not Responding"))

    u23o6_total_out_m = models.PositiveIntegerField(
        _("[6-23m] Total Out Male"))
    u23o6_total_out_f = models.PositiveIntegerField(
        _("[6-23m] Total Out Female"))

    u23o6_referred = models.PositiveIntegerField(
        _("[6-23m] Referred"))

    u23o6_total_end_m = models.PositiveIntegerField(
        _("[6-23m] End of Month Male"))
    u23o6_total_end_f = models.PositiveIntegerField(
        _("[6-23m] End of Month Female"))

    # 23-59 months
    u59o23_total_start_m = models.PositiveIntegerField(
        _("[23-59m] Start of Month Male"))
    u59o23_total_start_f = models.PositiveIntegerField(
        _("[23-59m] Start of Month Female"))

    u59o23_new_cases = models.PositiveIntegerField(
        _("[23-59m] New Cases"))
    u59o23_returned = models.PositiveIntegerField(
        _("[23-59m] Returned"))
    u59o23_total_in_m = models.PositiveIntegerField(
        _("[23-59m] Total Admitted Male"))
    u59o23_total_in_f = models.PositiveIntegerField(
        _("[23-59m] Total Admitted Female"))

    u59o23_healed = models.PositiveIntegerField(
        _("[23-59m] Healed"))
    u59o23_deceased = models.PositiveIntegerField(
        _("[23-59m] Deceased"))
    u59o23_abandon = models.PositiveIntegerField(
        _("[23-59m] Abandon"))
    u59o23_not_responding = models.PositiveIntegerField(
        _("[23-59m] Not Responding"))
    u59o23_total_out_m = models.PositiveIntegerField(
        _("[23-59m] Total Out Male"))
    u59o23_total_out_f = models.PositiveIntegerField(
        _("[23-59m] Total Out Female"))

    u59o23_referred = models.PositiveIntegerField(
        _("[23-59m] Referred"))

    u59o23_total_end_m = models.PositiveIntegerField(
        _("[23-59m] End of Month Male"))
    u59o23_total_end_f = models.PositiveIntegerField(
        _("[23-59m] End of Month Female"))

    # 59+ months
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

    # Pregnant & Breast Feeding Women
    pw_total_start_f = models.PositiveIntegerField(
        _("[PW/BF] Start of Month Female"))

    pw_new_cases = models.PositiveIntegerField(
        _("[PW/BF] New Cases"))
    pw_returned = models.PositiveIntegerField(
        _("[PW/BF] Returned"))
    pw_total_in_f = models.PositiveIntegerField(
        _("[PW/BF] Total Admitted Female"))

    pw_healed = models.PositiveIntegerField(
        _("[PW/BF] Healed"))
    pw_deceased = models.PositiveIntegerField(
        _("[PW/BF] Deceased"))
    pw_abandon = models.PositiveIntegerField(
        _("[PW/BF] Abandon"))
    pw_not_responding = models.PositiveIntegerField(
        _("[PW/BF] Not Responding"))
    pw_total_out_f = models.PositiveIntegerField(
        _("[PW/BF] Total Out Female"))

    pw_referred = models.PositiveIntegerField(
        _("[PW/BF] Referred"))

    pw_total_end_f = models.PositiveIntegerField(
        _("[PW/BF] End of Month Female"))

    # Former SAM
    exsam_total_start_m = models.PositiveIntegerField(
        _("[Ex-SAM] Start of Month Male"))
    exsam_total_start_f = models.PositiveIntegerField(
        _("[Ex-SAM] Start of Month Female"))

    exsam_grand_total_in = models.PositiveIntegerField(
        _("[Ex-SAM] Grand Total In"))

    exsam_grand_total_out = models.PositiveIntegerField(
        _("[Ex-SAM] Grand Total Out"))

    exsam_total_end_m = models.PositiveIntegerField(
        _("[Ex-SAM] End of Month Male"))
    exsam_total_end_f = models.PositiveIntegerField(
        _("[Ex-SAM] End of Month Female"))

    @classmethod
    def age_groups(cls):
        return ['u23o6', 'u59o23', 'o59', 'pw', 'exsam']

    @classmethod
    def comp_age_groups(cls):
        return ['u23o6', 'u59o23']

    # 6-23 months
    @property
    def u23o6_total_start(self):
        return self.age_sum_for('u23o6', ['total_start_m', 'total_start_f'])

    @property
    def u23o6_total_in(self):
        return self.age_sum_for('u23o6', ['total_in_m', 'total_in_f'])

    @property
    def u23o6_transferred(self):
        # URENAM can't receive transfers
        return 0

    @property
    def u23o6_grand_total_in(self):
        return self.age_sum_for('u23o6', ['total_in', 'transferred'])

    @property
    def u23o6_total_out(self):
        return self.age_sum_for('u23o6', ['total_out_m', 'total_out_f'])

    @property
    def u23o6_grand_total_out(self):
        return self.age_sum_for('u23o6', ['total_out', 'referred'])

    @property
    def u23o6_total_end(self):
        return self.age_sum_for('u23o6', ['total_end_m', 'total_end_f'])

    @property
    def u23o6_healed_rate(self):
        return self.performance_indicator_for('u23o6', 'healed')

    @property
    def u23o6_deceased_rate(self):
        return self.performance_indicator_for('u23o6', 'deceased')

    @property
    def u23o6_abandon_rate(self):
        return self.performance_indicator_for('u23o6', 'abandon')

    # 23-59 months
    @property
    def u59o23_total_start(self):
        return self.age_sum_for('u59o23', ['total_start_m', 'total_start_f'])

    @property
    def u59o23_total_in(self):
        return self.age_sum_for('u59o23', ['total_in_m', 'total_in_f'])

    @property
    def u59o23_transferred(self):
        # URENAM can't receive transfers
        return 0

    @property
    def u59o23_grand_total_in(self):
        return self.age_sum_for('u59o23', ['total_in', 'transferred'])

    @property
    def u59o23_total_out(self):
        return self.age_sum_for('u59o23', ['total_out_m', 'total_out_f'])

    @property
    def u59o23_grand_total_out(self):
        return self.age_sum_for('u59o23', ['total_out', 'referred'])

    @property
    def u59o23_total_end(self):
        return self.age_sum_for('u59o23', ['total_end_m', 'total_end_f'])

    @property
    def u59o23_healed_rate(self):
        return self.performance_indicator_for('u59o23', 'healed')

    @property
    def u59o23_deceased_rate(self):
        return self.performance_indicator_for('u59o23', 'deceased')

    @property
    def u59o23_abandon_rate(self):
        return self.performance_indicator_for('u59o23', 'abandon')

    # 59+ months
    @property
    def o59_total_start(self):
        return self.age_sum_for('o59', ['total_start_m', 'total_start_f'])

    @property
    def o59_total_in(self):
        return self.age_sum_for('o59', ['total_in_m', 'total_in_f'])

    @property
    def o59_transferred(self):
        # URENAM can't receive transfers
        return 0

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

    @property
    def o59_healed_rate(self):
        return self.performance_indicator_for('o59', 'healed')

    @property
    def o59_deceased_rate(self):
        return self.performance_indicator_for('o59', 'deceased')

    @property
    def o59_abandon_rate(self):
        return self.performance_indicator_for('o59', 'abandon')

    # Pregnant & Breast Feeding Women
    @property
    def pw_total_start_m(self):
        return 0

    @property
    def pw_total_in_m(self):
        return 0

    @property
    def pw_total_out_m(self):
        return 0

    @property
    def pw_total_end_m(self):
        return 0

    @property
    def pw_total_start(self):
        return self.age_sum_for('pw', ['total_start_m', 'total_start_f'])

    @property
    def pw_total_in(self):
        return self.age_sum_for('pw', ['total_in_m', 'total_in_f'])

    @property
    def pw_transferred(self):
        # URENAM can't receive transfers
        return 0

    @property
    def pw_grand_total_in(self):
        return self.age_sum_for('pw', ['total_in', 'transferred'])

    @property
    def pw_total_out(self):
        return self.age_sum_for('pw', ['total_out_m', 'total_out_f'])

    @property
    def pw_grand_total_out(self):
        return self.age_sum_for('pw', ['total_out', 'referred'])

    @property
    def pw_total_end(self):
        return self.age_sum_for('pw', ['total_end_m', 'total_end_f'])

    @property
    def pw_healed_rate(self):
        return self.performance_indicator_for('pw', 'healed')

    @property
    def pw_deceased_rate(self):
        return self.performance_indicator_for('pw', 'deceased')

    @property
    def pw_abandon_rate(self):
        return self.performance_indicator_for('pw', 'abandon')

    # Former SAM
    @property
    def exsam_new_cases(self):
        return 0

    @property
    def exsam_returned(self):
        return 0

    @property
    def exsam_total_in_m(self):
        return 0

    @property
    def exsam_total_in_f(self):
        return 0

    @property
    def exsam_healed(self):
        return 0

    @property
    def exsam_deceased(self):
        return 0

    @property
    def exsam_abandon(self):
        return 0

    @property
    def exsam_not_responding(self):
        return 0

    @property
    def exsam_total_start(self):
        return self.age_sum_for('exsam', ['total_start_m', 'total_start_f'])

    @property
    def exsam_total_in(self):
        return self.age_sum_for('exsam', ['total_in_m', 'total_in_f'])

    @property
    def exsam_referred(self):
        return 0

    @property
    def exsam_transferred(self):
        # URENAM can't receive transfers
        return 0

    @property
    def exsam_total_out_m(self):
        return 0

    @property
    def exsam_total_out_f(self):
        return 0

    @property
    def exsam_total_end(self):
        return self.age_sum_for('exsam', ['total_end_m', 'total_end_f'])

    @property
    def exsam_healed_rate(self):
        return self.performance_indicator_for('exsam', 'healed')

    @property
    def exsam_deceased_rate(self):
        return self.performance_indicator_for('exsam', 'deceased')

    @property
    def exsam_abandon_rate(self):
        return self.performance_indicator_for('exsam', 'abandon')

    def fill_blank(self):
        for field in self.data_fields():
            setattr(self, field, 0)


class URENAMNutritionR(AbstractURENAMNutritionR):

    REPORTING_TYPE = PERIODICAL_SOURCE
    RECEIPT_FORMAT = "{period__year_short}{period__month}" \
                     "NAM-{dow}/{entity__slug}-{rand}"
    UNIQUE_TOGETHER = [('period', 'entity')]

    class Meta:
        app_label = 'snisi_nutrition'
        verbose_name = _("URENAM Report")
        verbose_name_plural = _("URENAM Reports")


receiver(pre_save, sender=URENAMNutritionR)(pre_save_report)
receiver(post_save, sender=URENAMNutritionR)(post_save_report)

reversion.register(URENAMNutritionR)


class AggURENAMNutritionR(AbstractURENAMNutritionR,
                          PeriodicAggregatedReportInterface, SNISIReport):

    REPORTING_TYPE = PERIODICAL_AGGREGATED
    RECEIPT_FORMAT = "{period__year_short}{period__month}" \
                     "NAMa-{dow}/{entity__slug}-{rand}"
    INDIVIDUAL_CLS = URENAMNutritionR
    UNIQUE_TOGETHER = [('period', 'entity')]

    class Meta:
        app_label = 'snisi_nutrition'
        verbose_name = _("Aggregated URENAM Report")
        verbose_name_plural = _("Aggregated URENAM Reports")

    indiv_sources = models.ManyToManyField(
        INDIVIDUAL_CLS,
        verbose_name=_(u"Primary. Sources"),
        blank=True,
        related_name='source_agg_%(class)s_reports')

    direct_indiv_sources = models.ManyToManyField(
        INDIVIDUAL_CLS,
        verbose_name=_("Primary. Sources (direct)"),
        blank=True,
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
        for field in cls.data_fields():
            setattr(report, field,
                    getattr(report, field, 0) + getattr(instance, field, 0))

    @classmethod
    def update_instance_with_agg(cls, report, instance):
        for field in cls.data_fields():
            setattr(report, field,
                    getattr(report, field, 0) + getattr(instance, field, 0))


receiver(pre_save, sender=AggURENAMNutritionR)(pre_save_report)
receiver(post_save, sender=AggURENAMNutritionR)(post_save_report)

reversion.register(AggURENAMNutritionR)
