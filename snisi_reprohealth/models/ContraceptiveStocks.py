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

class ContraceptiveStockRIface(models.Model):

    class Meta:
        abstract = True

    intrauterine_devices_initial = models.PositiveIntegerField(
        verbose_name=_("IUD: Initial Quantity"))
    intrauterine_devices_used = models.PositiveIntegerField(
        verbose_name=_("IUD: Quantity Used"))
    intrauterine_devices_received = models.PositiveIntegerField(
        verbose_name=_("IUD: Quantity Received"))

    implants_initial = models.PositiveIntegerField(
        verbose_name=_("Implants: Initial Quantity"))
    implants_used = models.PositiveIntegerField(
        verbose_name=_("Implants: Quantity Used"))
    implants_received = models.PositiveIntegerField(
        verbose_name=_("Implants: Quantity Received"))

    injections_initial = models.PositiveIntegerField(
        verbose_name=_("Injections: Initial Quantity"))
    injections_used = models.PositiveIntegerField(
        verbose_name=_("Injections: Quantity Used"))
    injections_received = models.PositiveIntegerField(
        verbose_name=_("Injections: Quantity Received"))

    pills_initial = models.PositiveIntegerField(
        verbose_name=_("Pills: Initial Quantity"))
    pills_used = models.PositiveIntegerField(
        verbose_name=_("Pills: Quantity Used"))
    pills_received = models.PositiveIntegerField(
        verbose_name=_("Pills: Quantity Received"))

    male_condoms_initial = models.PositiveIntegerField(
        verbose_name=_("Male Condoms: Initial Quantity"))
    male_condoms_used = models.PositiveIntegerField(
        verbose_name=_("Male Condoms: Quantity Used"))
    male_condoms_received = models.PositiveIntegerField(
        verbose_name=_("Male Condoms: Quantity Received"))

    female_condoms_initial = models.PositiveIntegerField(
        verbose_name=_("Female Condoms: Initial Quantity"))
    female_condoms_used = models.PositiveIntegerField(
        verbose_name=_("Female Condoms: Quantity Used"))
    female_condoms_received = models.PositiveIntegerField(
        verbose_name=_("Female Condoms: Quantity Received"))

    hiv_tests_initial = models.PositiveIntegerField(
        verbose_name=_("HIV Tests: Initial Quantity"))
    hiv_tests_used = models.PositiveIntegerField(
        verbose_name=_("HIV Tests: Quantity Used"))
    hiv_tests_received = models.PositiveIntegerField(
        verbose_name=_("HIV Tests: Quantity Received"))

    def fill_blank(self, **kwargs):
        for field in self.data_fields():
            if not field.endswith('_observation'):
                setattr(self, field, 0)


class ContraceptiveStockR(ContraceptiveStockRIface, SNISIReport):

    REPORTING_TYPE = PERIODICAL_SOURCE
    RECEIPT_FORMAT = None  # using custom generate_receipt
    UNIQUE_TOGETHER = [('period', 'entity')]
    INTEGRITY_CHECKER = 'snisi_reprohealth.integrity.ContraceptiveStockRIntegrityChecker'

    class Meta:
        app_label = 'snisi_reprohealth'
        verbose_name = _("Contaceptive Stocks Report")
        verbose_name_plural = _("Contaceptive Stocks Reports")

    intrauterine_devices_observation = models.CharField(
        max_length=500, null=True, blank=True)

    implants_observation = models.CharField(
        max_length=500, null=True, blank=True)

    injections_observation = models.CharField(
        max_length=500, null=True, blank=True)

    pills_observation = models.CharField(
        max_length=500, null=True, blank=True)

    male_condoms_observation = models.CharField(
        max_length=500, null=True, blank=True)

    female_condoms_observation = models.CharField(
        max_length=500, null=True, blank=True)

    hiv_tests_observation = models.CharField(
        max_length=500, null=True, blank=True)


receiver(pre_save, sender=ContraceptiveStockR)(pre_save_report)
receiver(post_save, sender=ContraceptiveStockR)(post_save_report)

reversion.register(ContraceptiveStockR, follow=['snisireport_ptr'])


class AggContraceptiveStockR(ContraceptiveStockRIface,
                             PeriodicAggregatedReportInterface, SNISIReport):

    REPORTING_TYPE = PERIODICAL_AGGREGATED
    INDIVIDUAL_CLS = ContraceptiveStockR
    RECEIPT_FORMAT =  None  # using custom generate_receipt
    UNIQUE_TOGETHER = [('period', 'entity'),]

    class Meta:
        app_label = 'snisi_reprohealth'
        verbose_name = _("Aggregated Contaceptive Stocks Report")
        verbose_name_plural = _("Aggregated Contaceptive Stocks Reports")

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

receiver(pre_save, sender=AggContraceptiveStockR)(pre_save_report)
receiver(post_save, sender=AggContraceptiveStockR)(post_save_report)

reversion.register(AggContraceptiveStockR, follow=['snisireport_ptr'])
