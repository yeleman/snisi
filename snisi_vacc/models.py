#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

import reversion
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from django.utils.translation import ugettext_lazy as _

from snisi_core.models.common import pre_save_report, post_save_report
from snisi_core.models.Reporting import (SNISIReport,
                                         PeriodicAggregatedReportInterface,
                                         PERIODICAL_SOURCE,
                                         PERIODICAL_AGGREGATED)


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

    @classmethod
    def create_aggregated(cls, period, entity, created_by, *args, **kwargs):
        agg_report = cls.start(period=period,
                               entity=entity,
                               created_by=created_by,
                               *args, **kwargs)

        sources = VaccCovR.validated.filter(period=period,
                                            entity__in=entity.get_children())

        if sources.count() == 0:
            agg_report.fill_blank()
            agg_report.save()

        for report in sources:
            for key, value in report.to_dict().items():
                pv = getattr(agg_report, key)
                if not pv:
                    nv = value
                else:
                    nv = pv + value
                setattr(agg_report, key, nv)
            agg_report.save()

        for report in sources:
            agg_report.sources.add(report)

        with reversion.create_revision():
            agg_report.save()
            reversion.set_user(created_by)

        return agg_report

receiver(pre_save, sender=VaccCovR)(pre_save_report)
receiver(post_save, sender=VaccCovR)(post_save_report)

reversion.register(VaccCovR, follow=['snisireport_ptr'])


class AggVaccCovR(VaccCovRIface,
                  PeriodicAggregatedReportInterface, SNISIReport):

    REPORTING_TYPE = PERIODICAL_AGGREGATED
    INDIVIDUAL_CLS = VaccCovR
    RECEIPT_FORMAT = "AMVC{id}/{entity__slug}-{day}"
    UNIQUE_TOGETHER = [('period', 'entity')]

    class Meta:
        app_label = 'snisi_vacc'
        verbose_name = _("Aggregated Major Vaccine Coverage Report")
        verbose_name_plural = _("Aggregated Major Vaccine Coverage Reports")

    # all source reports (CSCOM)
    indiv_sources = models.ManyToManyField(
        INDIVIDUAL_CLS,
        verbose_name=_("Primary. Sources (all)"),
        blank=True, null=True,
        related_name='source_agg_%(class)s_reports',
        symmetrical=False)

    direct_indiv_sources = models.ManyToManyField(
        INDIVIDUAL_CLS,
        verbose_name=_("Primary. Sources (direct)"),
        blank=True, null=True,
        related_name='direct_source_agg_%(class)s_reports',
        symmetrical=False)

    @classmethod
    def start_aggregated(cls, *args, **kwargs):
        rfdict = {}
        for field in ('completion_ok', 'integrity_ok',
                      'arrival_ok', 'auto_validate'):
            if field in kwargs:
                rfdict.update({field: kwargs.get(field)})
                del kwargs[field]
        report = cls.start_report(*args, **kwargs)
        report.fill_blank()

        # only agg
        if hasattr(report, 'set_reporting_status_fields'):
            report.set_reporting_status_fields(**rfdict)
        if hasattr(report, 'update_expected_reportings_number'):
            report.update_expected_reportings_number()
        return report

    @classmethod
    def create_from(cls, period, entity, created_by,
                    indiv_sources=None, agg_sources=None):
        if indiv_sources is None and entity.type.slug == 'health_district':
            indiv_sources = cls.INDIVIDUAL_CLS \
                               .objects \
                               .filter(period=period,
                                       entity__in=entity.get_health_centers())
        return super(AggVaccCovR, cls).create_from(period=period,
                                                   entity=entity,
                                                   created_by=created_by,
                                                   indiv_sources=indiv_sources,
                                                   agg_sources=agg_sources)

    @classmethod
    def update_instance_with_indiv(cls, report, instance):
        for field in instance.data_fields():
            setattr(report, field,
                    (getattr(report, field, 0) or 0)
                    + (getattr(instance, field, 0) or 0))

    @classmethod
    def update_instance_with_agg(cls, report, instance):
        for field in cls.data_fields():
            setattr(report, field,
                    (getattr(report, field, 0) or 0)
                    + (getattr(instance, field, 0) or 0))

receiver(pre_save, sender=AggVaccCovR)(pre_save_report)
receiver(post_save, sender=AggVaccCovR)(post_save_report)

reversion.register(AggVaccCovR, follow=['snisireport_ptr'])
