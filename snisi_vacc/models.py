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


class VaccCovRIface(models.Model):

    class Meta:
        abstract = True

    bcg_coverage = models.FloatField(verbose_name=_("BCG Coverage"))
    polio3_coverage = models.FloatField(verbose_name=_("Penta3 Coverage"))
    measles_coverage = models.FloatField(verbose_name=_("Measles Coverage"))
    polio3_abandonment_rate = models.FloatField(
        verbose_name=_("Penta3 Abandonment Rate"))

    def fill_blank(self, **kwargs):
        for field in self.data_fields():
            setattr(self, field, 0)


class VaccCovR(VaccCovRIface, SNISIReport):

    REPORTING_TYPE = PERIODICAL_SOURCE
    RECEIPT_FORMAT = "MVC{id}/{entity__slug}-{day}"
    UNIQUE_TOGETHER = [('period', 'entity')]
    INTEGRITY_CHECKER = 'snisi_vacc.integrity.VaccCovRIntegrityChecker'

    class Meta:
        app_label = 'snisi_vacc'
        verbose_name = _("Provided Services Report")
        verbose_name_plural = _("Provided Services Reports")

receiver(pre_save, sender=VaccCovR)(pre_save_report)
receiver(post_save, sender=VaccCovR)(post_save_report)

reversion.register(VaccCovR, follow=['snisireport_ptr'])


class AggVaccCovR(VaccCovRIface,
                       PeriodicAggregatedReportInterface, SNISIReport):

    REPORTING_TYPE = PERIODICAL_AGGREGATED
    INDIVIDUAL_CLS = VaccCovR
    RECEIPT_FORMAT = "AMVC{id}/{entity__slug}-{day}"
    UNIQUE_TOGETHER = [('period', 'entity'),]

    class Meta:
        app_label = 'snisi_vacc'
        verbose_name = _("Aggregated Major Vaccine Coverage Report")
        verbose_name_plural = _("Aggregated Major Vaccine Coverage Reports")

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

receiver(pre_save, sender=AggVaccCovR)(pre_save_report)
receiver(post_save, sender=AggVaccCovR)(post_save_report)

reversion.register(AggVaccCovR, follow=['snisireport_ptr'])
