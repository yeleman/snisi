#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

import reversion
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from django.utils.translation import ugettext_lazy as _, ugettext

from snisi_core.models.common import pre_save_report, post_save_report
from snisi_core.models.Reporting import (SNISIReport,
                                         PeriodicAggregatedReportInterface,
                                         ExpectedReporting,
                                         PERIODICAL_SOURCE, PERIODICAL_AGGREGATED)

class FinancialRIface(models.Model):

    class Meta:
        abstract = True

    intrauterine_devices_qty = models.PositiveIntegerField()
    intrauterine_devices_price = models.PositiveIntegerField()
    intrauterine_devices_revenue = models.PositiveIntegerField()

    implants_qty = models.PositiveIntegerField()
    implants_price = models.PositiveIntegerField()
    implants_revenue = models.PositiveIntegerField()

    injections_qty = models.PositiveIntegerField()
    injections_price = models.PositiveIntegerField()
    injections_revenue = models.PositiveIntegerField()

    pills_qty = models.PositiveIntegerField()
    pills_price = models.PositiveIntegerField()
    pills_revenue = models.PositiveIntegerField()

    male_condoms_qty = models.PositiveIntegerField()
    male_condoms_price = models.PositiveIntegerField()
    male_condoms_revenue = models.PositiveIntegerField()

    female_condoms_qty = models.PositiveIntegerField()
    female_condoms_price = models.PositiveIntegerField()
    female_condoms_revenue = models.PositiveIntegerField()

    hiv_tests_qty = models.PositiveIntegerField()
    hiv_tests_price = models.PositiveIntegerField()
    hiv_tests_revenue = models.PositiveIntegerField()

    iud_removal_qty = models.PositiveIntegerField()
    iud_removal_price = models.PositiveIntegerField()
    iud_removal_revenue = models.PositiveIntegerField()

    implant_removal_qty = models.PositiveIntegerField()
    implant_removal_price = models.PositiveIntegerField()
    implant_removal_revenue = models.PositiveIntegerField()

    def fill_blank(self, **kwargs):
        for field in self.data_fields():
            setattr(self, field, 0)


class FinancialR(FinancialRIface, SNISIReport):

    REPORTING_TYPE = PERIODICAL_SOURCE
    RECEIPT_FORMAT = None  # using custom generate_receipt
    UNIQUE_TOGETHER = [('period', 'entity')]
    INTEGRITY_CHECKER = 'snisi_reprohealth.integrity.FinancialRIntegrityChecker'

    class Meta:
        app_label = 'snisi_reprohealth'
        verbose_name = _("Fianancial Report")
        verbose_name_plural = _("Fianancial Reports")


receiver(pre_save, sender=FinancialR)(pre_save_report)
receiver(post_save, sender=FinancialR)(post_save_report)

reversion.register(FinancialR, follow=['snisireport_ptr'])


class AggFinancialR(FinancialRIface,
                    PeriodicAggregatedReportInterface, SNISIReport):

    REPORTING_TYPE = PERIODICAL_AGGREGATED
    INDIVIDUAL_CLS = FinancialR
    RECEIPT_FORMAT =  None  # using custom generate_receipt
    UNIQUE_TOGETHER = [('period', 'entity'),]

    class Meta:
        app_label = 'snisi_reprohealth'
        verbose_name = _("Aggregated Financial Report")
        verbose_name_plural = _("Aggregated Financial Reports")

    # all source reports (CSCOM)
    indiv_sources = models.ManyToManyField(INDIVIDUAL_CLS,
        verbose_name=_("Primary. Sources (all)"),
        blank=True, null=True,
        related_name='source_agg_%(class)s_reports',
        symmetrical=False)

    direct_indiv_sources = models.ManyToManyField(INDIVIDUAL_CLS,
        verbose_name=_("Primary. Sources (direct)"),
        blank=True, null=True,
        related_name='direct_source_agg_%(class)s_reports',
        symmetrical=False)

receiver(pre_save, sender=AggFinancialR)(pre_save_report)
receiver(post_save, sender=AggFinancialR)(post_save_report)

reversion.register(AggFinancialR, follow=['snisireport_ptr'])
