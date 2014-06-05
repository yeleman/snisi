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
                                         PERIODICAL_SOURCE, PERIODICAL_AGGREGATED)

class ProvidedServicesRIface(models.Model):

    class Meta:
        abstract = True

    # CAP-providing services
    tubal_ligations = models.PositiveIntegerField(
        verbose_name=_("Tubal Ligations"))
    intrauterine_devices = models.PositiveIntegerField(
        verbose_name=_("IUD"))
    injections = models.PositiveIntegerField(
        verbose_name=_("Injections"))
    pills = models.PositiveIntegerField(
        verbose_name=_("Pills"))
    male_condoms = models.PositiveIntegerField(
        verbose_name=_("Male condoms"))
    female_condoms = models.PositiveIntegerField(
        verbose_name=_("Female condoms"))
    emergency_controls = models.PositiveIntegerField(
        verbose_name=_("Emergency controls"))
    implants = models.PositiveIntegerField(
        verbose_name=_("Implants"))

    # Clients related services
    new_clients = models.PositiveIntegerField(
        verbose_name=_("New Clients"))
    previous_clients = models.PositiveIntegerField(
        verbose_name=_("Previous Clients"))
    under25_visits = models.PositiveIntegerField(
        verbose_name=_("Visits from under 25yo."))
    over25_visits = models.PositiveIntegerField(
        verbose_name=_("Visits from over 25yo."))
    very_first_visits = models.PositiveIntegerField(
        verbose_name=_("Clients visiting for the first time."))
    short_term_method_visits = models.PositiveIntegerField(
        verbose_name=_("Short-term methods related visits"))
    long_term_method_visits = models.PositiveIntegerField(
        verbose_name=_("Long-term methods related visits"))
    hiv_counseling_clients = models.PositiveIntegerField(
        verbose_name=_("HIV Counseiling"))
    hiv_tests = models.PositiveIntegerField(
        verbose_name=_("HIV Tests"))
    hiv_positive_results = models.PositiveIntegerField(
        verbose_name=_("HIV+ results"))

    # non-CAP providing services
    implant_removals = models.PositiveIntegerField(
        verbose_name=_("Implant removals"))
    iud_removal = models.PositiveIntegerField(
        verbose_name=_("IUD removals"))

    def fill_blank(self, **kwargs):
        for field in self.data_fields():
            setattr(self, field, 0)


class ProvidedServicesR(ProvidedServicesRIface, SNISIReport):

    REPORTING_TYPE = PERIODICAL_SOURCE
    RECEIPT_FORMAT = None  # using custom generate_receipt
    UNIQUE_TOGETHER = [('period', 'entity')]
    INTEGRITY_CHECKER = 'snisi_reprohealth.integrity.ProvidedServicesRIntegrityChecker'

    class Meta:
        app_label = 'snisi_reprohealth'
        verbose_name = _("Provided Services Report")
        verbose_name_plural = _("Provided Services Reports")


receiver(pre_save, sender=ProvidedServicesR)(pre_save_report)
receiver(post_save, sender=ProvidedServicesR)(post_save_report)

reversion.register(ProvidedServicesR, follow=['snisireport_ptr'])


class AggProvidedServicesR(ProvidedServicesRIface,
                           PeriodicAggregatedReportInterface, SNISIReport):

    REPORTING_TYPE = PERIODICAL_AGGREGATED
    INDIVIDUAL_CLS = ProvidedServicesR
    RECEIPT_FORMAT =  None  # using custom generate_receipt
    UNIQUE_TOGETHER = [('period', 'entity'),]

    class Meta:
        app_label = 'snisi_reprohealth'
        verbose_name = _("Aggregated Provided Services Report")
        verbose_name_plural = _("Aggregated Provided Services Reports")

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

receiver(pre_save, sender=AggProvidedServicesR)(pre_save_report)
receiver(post_save, sender=AggProvidedServicesR)(post_save_report)

reversion.register(AggProvidedServicesR, follow=['snisireport_ptr'])
