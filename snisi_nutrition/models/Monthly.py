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

from snisi_core.models.common import (pre_save_report, post_save_report,
                                      create_periodic_agg_report_from)
from snisi_core.models.Reporting import (SNISIReport,
                                         PeriodicAggregatedReportInterface,
                                         PERIODICAL_SOURCE,
                                         PERIODICAL_AGGREGATED)
from snisi_nutrition.xls_export import nutrition_monthly_as_xls

logger = logging.getLogger(__name__)


class AbstractNutritionR(SNISIReport):

    class Meta:
        app_label = 'snisi_nutrition'
        abstract = True

    def total_for(self, field):
        return sum([
            getattr(report, 'total_for', lambda x: 0)(field)
            for report in (self.urenam_report,
                           self.urenas_report,
                           self.ureni_report)
            ])

    @property
    def total_start(self):
        return self.total_for('total_start')

    @property
    def total_start_m(self):
        return self.total_for('total_start_m')

    @property
    def total_start_f(self):
        return self.total_for('total_start_f')

    @property
    def new_cases(self):
        return self.total_for('new_cases')

    @property
    def returned(self):
        return self.total_for('returned')

    @property
    def total_in_m(self):
        return self.total_for('total_in_m')

    @property
    def total_in_f(self):
        return self.total_for('total_in_f')

    @property
    def transferred(self):
        return self.total_for('transferred')

    @property
    def grand_total_in(self):
        return self.total_for('grand_total_in')

    @property
    def healed(self):
        return self.total_for('healed')

    @property
    def deceased(self):
        return self.total_for('deceased')

    @property
    def abandon(self):
        return self.total_for('abandon')

    @property
    def not_responding(self):
        return self.total_for('not_responding')

    @property
    def total_out(self):
        return self.total_for('total_out')

    @property
    def total_out_m(self):
        return self.total_for('total_out_m')

    @property
    def total_out_f(self):
        return self.total_for('total_out_f')

    @property
    def referred(self):
        return self.total_for('referred')

    @property
    def grand_total_out(self):
        return self.total_for('grand_total_out')

    @property
    def total_end(self):
        return self.total_for('total_end')

    @property
    def total_end_m(self):
        return self.total_for('total_end_m')

    @property
    def total_end_f(self):
        return self.total_for('total_end_f')

    @property
    def total_out_resp(self):
        return self.total_out - self.not_responding

    @property
    def healed_rate(self):
        try:
            return self.healed / self.total_out_resp
        except ZeroDivisionError:
            return 0

    @property
    def deceased_rate(self):
        try:
            return self.deceased / self.total_out_resp
        except ZeroDivisionError:
            return 0

    @property
    def abandon_rate(self):
        try:
            return self.abandon / self.total_out_resp
        except ZeroDivisionError:
            return 0

    def as_xls(self):
        file_name = "NUT_{entity}.{month}.{year}.xls" \
                    .format(entity=self.entity.slug,
                            month=self.period.middle().month,
                            year=self.period.middle().year)
        return file_name, nutrition_monthly_as_xls(self)


class NutritionR(AbstractNutritionR):

    REPORTING_TYPE = PERIODICAL_SOURCE
    RECEIPT_FORMAT = "{period}-NUT/{rand}"
    UNIQUE_TOGETHER = [('period', 'entity')]

    class Meta:
        app_label = 'snisi_nutrition'
        verbose_name = _("Nutrition Report")
        verbose_name_plural = _("Nutrition Reports")

    urenam_report = models.ForeignKey(
        'URENAMNutritionR', null=True, blank=True, related_name='nutritionr')
    urenas_report = models.ForeignKey(
        'URENASNutritionR', null=True, blank=True, related_name='nutritionr')
    ureni_report = models.ForeignKey(
        'URENINutritionR', null=True, blank=True, related_name='nutritionr')
    stocks_report = models.ForeignKey(
        'NutritionStocksR', null=True, blank=True, related_name='nutritionr')


receiver(pre_save, sender=NutritionR)(pre_save_report)
receiver(post_save, sender=NutritionR)(post_save_report)

reversion.register(NutritionR)


class AggNutritionR(AbstractNutritionR,
                    PeriodicAggregatedReportInterface, SNISIReport):

    REPORTING_TYPE = PERIODICAL_AGGREGATED
    RECEIPT_FORMAT = "{period}-NUTa/{rand}"
    INDIVIDUAL_CLS = NutritionR
    UNIQUE_TOGETHER = [('period', 'entity')]

    class Meta:
        app_label = 'snisi_nutrition'
        verbose_name = _("Aggregated Nutrition Report")
        verbose_name_plural = _("Aggregated Nutrition Reports")

    urenam_report = models.ForeignKey(
        'AggURENAMNutritionR', null=True, blank=True,
        related_name='agg_nutritionr')
    urenas_report = models.ForeignKey(
        'AggURENASNutritionR', null=True, blank=True,
        related_name='agg_nutritionr')
    ureni_report = models.ForeignKey(
        'AggURENINutritionR', null=True, blank=True,
        related_name='agg_nutritionr')
    stocks_report = models.ForeignKey(
        'AggNutritionStocksR', null=True, blank=True,
        related_name='agg_nutritionr')

    indiv_sources = models.ManyToManyField(
        INDIVIDUAL_CLS,
        verbose_name=_(u"Primary. Sources"),
        blank=True, null=True,
        related_name='source_agg_%(class)s_reports')

    def fill_blank(self):
        # no fields to set data on
        return

    @classmethod
    def update_instance_with_indiv(cls, report, instance):
        # no data update
        cls.update_instance_with_indiv_meta(report, instance)

    @classmethod
    def update_instance_with_agg(cls, report, instance):
        # no data update
        cls.update_instance_with_agg_meta(report, instance)

    @classmethod
    def create_from(cls, period, entity, created_by,
                    indiv_sources=None, agg_sources=None):
        # AggNutritionR is specific in that it only holds UREN/STOCKS reports
        # for an entity/period and does not carry data.

        from snisi_nutrition.models.URENAM import AggURENAMNutritionR
        from snisi_nutrition.models.URENAS import AggURENASNutritionR
        from snisi_nutrition.models.URENI import AggURENINutritionR
        from snisi_nutrition.models.Stocks import AggNutritionStocksR

        def gr(cls):
            try:
                return cls.objects.get(period=period, entity=entity)
            except:
                return None

        stocks_report = gr(AggNutritionStocksR)
        tocopy_fields = ['created_by', 'created_on',
                         'completion_status', 'completed_on',
                         'integrity_status', 'arrival_status',
                         'validation_status', 'validated_on',
                         'validated_by', 'auto_validated']

        # create blank report with data from stock report
        report = create_periodic_agg_report_from(
            cls, period=period, entity=entity,
            created_by=created_by, indiv_cls=cls.INDIVIDUAL_CLS,
            indiv_sources=indiv_sources,
            agg_sources=agg_sources)

        # copy status fields from stocks
        for field in tocopy_fields:
            setattr(report, getattr(stocks_report, field))

        if entity.has_urenam:
            report.urenam_report = gr(AggURENAMNutritionR)
        if entity.has_urenas:
            report.urenas_report = gr(AggURENASNutritionR)
        if entity.has_ureni:
            report.ureni_report = gr(AggURENINutritionR)
        report.stocks_report = stocks_report

        with reversion.create_revision():
            report.save()
            reversion.set_user(created_by)

        return report

    @classmethod
    def start_aggreagted(cls, *args, **kwargs):
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


receiver(pre_save, sender=AggNutritionR)(pre_save_report)
receiver(post_save, sender=AggNutritionR)(post_save_report)

reversion.register(AggNutritionR)
