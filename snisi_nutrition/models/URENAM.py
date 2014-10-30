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
                                         PERIODICAL_AGGREGATED)
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
    pw_total_start_m = models.PositiveIntegerField(
        _("[PW/BF] Start of Month Male"))
    pw_total_start_f = models.PositiveIntegerField(
        _("[PW/BF] Start of Month Female"))

    pw_new_cases = models.PositiveIntegerField(
        _("[PW/BF] New Cases"))
    pw_returned = models.PositiveIntegerField(
        _("[PW/BF] Returned"))
    pw_total_in_m = models.PositiveIntegerField(
        _("[PW/BF] Total Admitted Male"))
    pw_total_in_f = models.PositiveIntegerField(
        _("[PW/BF] Total Admitted Female"))

    pw_healed = models.PositiveIntegerField(
        _("[PW/BF] Healed"))
    pw_deceased = models.PositiveIntegerField(
        _("[PW/BF] Deceased"))
    pw_abandon = models.PositiveIntegerField(
        _("[PW/BF] Abandon"))
    pw_total_out_m = models.PositiveIntegerField(
        _("[PW/BF] Total Out Male"))
    pw_total_out_f = models.PositiveIntegerField(
        _("[PW/BF] Total Out Female"))

    pw_referred = models.PositiveIntegerField(
        _("[PW/BF] Referred"))

    pw_total_end_m = models.PositiveIntegerField(
        _("[PW/BF] End of Month Male"))
    pw_total_end_f = models.PositiveIntegerField(
        _("[PW/BF] End of Month Female"))

    # Former SAM
    exsam_total_start_m = models.PositiveIntegerField(
        _("[Ex-SAM] Start of Month Male"))
    exsam_total_start_f = models.PositiveIntegerField(
        _("[Ex-SAM] Start of Month Female"))

    exsam_total_out_m = models.PositiveIntegerField(
        _("[Ex-SAM] Total Out Male"))
    exsam_total_out_f = models.PositiveIntegerField(
        _("[Ex-SAM] Total Out Female"))

    exsam_referred = models.PositiveIntegerField(
        _("[Ex-SAM] Referred"))

    exsam_total_end_m = models.PositiveIntegerField(
        _("[Ex-SAM] End of Month Male"))
    exsam_total_end_f = models.PositiveIntegerField(
        _("[Ex-SAM] End of Month Female"))

    @classmethod
    def age_groups(cls):
        return ['u23o6', 'u59o23', 'o59', 'pw', 'exsam']

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
    def u23o6_not_responding(self):
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
    def u59o23_not_responding(self):
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
    def o59_not_responding(self):
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

    # Pregnant & Breast Feeding Women
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
    def pw_not_responding(self):
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
    def exsam_transferred(self):
        # URENAM can't receive transfers
        return 0

    @property
    def exsam_grand_total_in(self):
        return self.age_sum_for('exsam', ['total_in', 'transferred'])

    @property
    def exsam_total_out(self):
        return self.age_sum_for('exsam', ['total_out_m', 'total_out_f'])

    @property
    def exsam_grand_total_out(self):
        return self.age_sum_for('exsam', ['total_out', 'referred'])

    @property
    def exsam_total_end(self):
        return self.age_sum_for('exsam', ['total_end_m', 'total_end_f'])


class URENAMNutritionR(AbstractURENAMNutritionR):

    REPORTING_TYPE = PERIODICAL_SOURCE
    RECEIPT_FORMAT = "{period__year_short}{period__month}NAM-{dow}/{rand}"
    UNIQUE_TOGETHER = ('period', 'entity')

    class Meta:
        app_label = 'snisi_nutrition'
        verbose_name = _("URENAM Report")
        verbose_name_plural = _("URENAM Reports")


receiver(pre_save, sender=URENAMNutritionR)(pre_save_report)
receiver(post_save, sender=URENAMNutritionR)(post_save_report)

reversion.register(URENAMNutritionR)


class AggURENAMNutritionR(AbstractURENAMNutritionR,
                          PeriodicAggregatedReportInterface):

    REPORTING_TYPE = PERIODICAL_AGGREGATED
    RECEIPT_FORMAT = "{period__year_short}{period__month}NAMa-{dow}/{rand}"
    INDIVIDUAL_CLS = URENAMNutritionR
    UNIQUE_TOGETHER = [('period', 'entity')]

    class Meta:
        app_label = 'snisi_nutrition'
        verbose_name = _("Aggregated URENAM Report")
        verbose_name_plural = _("Aggregated URENAM Reports")

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


receiver(pre_save, sender=AggURENAMNutritionR)(pre_save_report)
receiver(post_save, sender=AggURENAMNutritionR)(post_save_report)

reversion.register(AggURENAMNutritionR)
