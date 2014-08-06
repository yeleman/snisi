#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

import reversion
from py3compat import implements_to_string
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from django.utils.translation import ugettext_lazy as _, ugettext

from snisi_core.models.common import pre_save_report, post_save_report
from snisi_core.models.Reporting import (SNISIReport,
                                         PeriodicAggregatedReportInterface,
                                         PERIODICAL_SOURCE,
                                         PERIODICAL_AGGREGATED)


class AbstractBednetR(SNISIReport):

    RECEIPT_FORMAT = "{period}-BDN/{rand}"

    class Meta:
        app_label = 'snisi_bednets'
        abstract = True

    initial_mild = models.IntegerField(_("Initial"))
    received_mild = models.IntegerField(_("Received"))

    distributed_mild = models.IntegerField(_("Distributed"))
    remaining_mild = models.IntegerField(_("Left"))

    difference_mild = models.IntegerField(_("Difference"))

    def add_data(self, initial_mild,
                 received_mild,
                 distributed_mild,
                 remaining_mild,
                 difference_mild):
        self.initial_mild = initial_mild
        self.received_mild = received_mild
        self.distributed_mild = distributed_mild
        self.remaining_mild = remaining_mild
        self.difference_mild = difference_mild

    def __str__(self):
        return ugettext("{cscom} / {period} / {receipt}").format(
            cscom=self.entity.display_full_name(),
            period=self.period,
            receipt=self.receipt)

    def fill_blank(self):
        for field in self.to_dict().keys():
            setattr(self, field, 0)


@implements_to_string
class BednetR(AbstractBednetR):

    REPORTING_TYPE = PERIODICAL_SOURCE

    class Meta:
        app_label = 'snisi_bednets'
        verbose_name = _("MILD Report")
        verbose_name_plural = _("MILD Reports")

receiver(pre_save, sender=BednetR)(pre_save_report)
receiver(post_save, sender=BednetR)(post_save_report)

reversion.register(BednetR)


@implements_to_string
class AggBednetR(PeriodicAggregatedReportInterface, AbstractBednetR):

    REPORTING_TYPE = PERIODICAL_AGGREGATED
    INDIVIDUAL_CLS = BednetR
    UNIQUE_TOGETHER = [('period', 'entity')]

    class Meta:
        app_label = 'snisi_bednets'
        verbose_name = _("Aggregated MILD Report")
        verbose_name_plural = _("Aggregated MILD Reports")

    indiv_sources = models.ManyToManyField(
        INDIVIDUAL_CLS,
        verbose_name=_(u"Primary. Sources"),
        blank=True, null=True,
        related_name='source_agg_%(class)s_reports')

receiver(pre_save, sender=AggBednetR)(pre_save_report)
receiver(post_save, sender=AggBednetR)(post_save_report)

reversion.register(AggBednetR)
