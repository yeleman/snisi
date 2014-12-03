#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging
import datetime

import reversion
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from snisi_core.models.common import pre_save_report, post_save_report
from snisi_core.models.Reporting import (SNISIReport,
                                         PeriodicAggregatedReportInterface,
                                         PERIODICAL_SOURCE,
                                         PERIODICAL_AGGREGATED)
from snisi_core.models.Periods import (WeekPeriod, ONE_WEEK_DELTA,
                                       ONE_MICROSECOND_DELTA,
                                       SpecificTypeManager,
                                       normalize_date)

logger = logging.getLogger(__name__)


class NutWeekManager(SpecificTypeManager):
    SPECIFIC_TYPE = 'nut_week'


class NutWeekPeriod(WeekPeriod):

    class Meta:
        proxy = True
        verbose_name = _("Week Period")
        verbose_name_plural = _("Week Periods")

    objects = NutWeekManager()

    @classmethod
    def type(cls):
        return 'nut_week'

    @property
    def pid(self):
        return'nW{}'.format(self.middle().strftime('%W-%Y'))

    @classmethod
    def boundaries(cls, date_obj):
        date_obj = normalize_date(date_obj, as_aware=True)

        monday = date_obj - datetime.timedelta(date_obj.weekday())
        monday = monday.replace(hour=0, minute=0, second=0, microsecond=0)

        friday_morning_dt = datetime.timedelta(days=4, minutes=0)
        friday_morning = monday + friday_morning_dt
        is_next_week = not date_obj < friday_morning

        if not is_next_week:
            start = friday_morning - ONE_WEEK_DELTA
        else:
            start = friday_morning
        end = start + datetime.timedelta(cls.delta()) - ONE_MICROSECOND_DELTA
        return (start, end)

    def strid(self):
        return self.middle().strftime('nW%W-%Y')


class NutWeekReportingManager(models.Manager):
    def get_queryset(self):
        return super(NutWeekReportingManager, self) \
            .get_queryset().filter(period_type='nut_week_reporting_period')


class NutWeekReportingPeriod(WeekPeriod):

    class Meta:
        proxy = True
        verbose_name = _("Week Reporting Period")
        verbose_name_plural = _("Week Reporting Periods")

    objects = NutWeekReportingManager()

    @classmethod
    def type(cls):
        return 'nut_week_reporting_period'

    @property
    def pid(self):
        return'nWRP{}'.format(self.middle().strftime('%W-%Y'))

    @classmethod
    def boundaries(cls, date_obj):
        nut_week = NutWeekPeriod.find_create_by_date(
            date_obj, dont_create=True)
        start = nut_week.end_on + ONE_MICROSECOND_DELTA
        end = start + datetime.timedelta(days=1)
        return start, end

    def strid(self):
        return self.middle().strftime('nWRP%W-%Y')


class NutWeekExtendedReportingManager(models.Manager):
    def get_queryset(self):
        return super(NutWeekExtendedReportingManager, self) \
            .get_queryset().filter(
                period_type='nut_week_extended_reporting_period')


class NutWeekExtendedReportingPeriod(WeekPeriod):

    class Meta:
        proxy = True
        verbose_name = _("Week Reporting Period")
        verbose_name_plural = _("Week Reporting Periods")

    objects = NutWeekExtendedReportingManager()

    @classmethod
    def type(cls):
        return 'nut_week_extended_reporting_period'

    @property
    def pid(self):
        return'nWERP{}'.format(self.middle().strftime('%W-%Y'))

    @classmethod
    def boundaries(cls, date_obj):
        nut_week = NutWeekReportingPeriod.find_create_by_date(
            date_obj, dont_create=True)
        start = nut_week.end_on + ONE_MICROSECOND_DELTA
        end = start + datetime.timedelta(days=2)
        return start, end

    def strid(self):
        return self.middle().strftime('nWERP%W-%Y')


class NutWeekDistrictValidationManager(models.Manager):
    def get_queryset(self):
        return super(NutWeekDistrictValidationManager, self) \
            .get_queryset().filter(period_type='nut_week_district_validation')


class NutWeekDistrictValidationPeriod(WeekPeriod):

    class Meta:
        proxy = True
        verbose_name = _("Week District Validation Period")
        verbose_name_plural = _("Week District Validation Periods")

    objects = NutWeekDistrictValidationManager()

    @classmethod
    def type(cls):
        return 'nut_week_district_validation'

    @property
    def pid(self):
        return'nWDVP{}'.format(self.middle().strftime('%W-%Y'))

    @classmethod
    def boundaries(cls, date_obj):
        nut_week = NutWeekPeriod.find_create_by_date(
            date_obj, dont_create=True)
        start = nut_week.end_on + ONE_MICROSECOND_DELTA
        end = start + datetime.timedelta(days=4)
        return start, end

    def strid(self):
        return self.middle().strftime('nWVP%W-%Y')


class NutWeekRegionValidationManager(models.Manager):
    def get_queryset(self):
        return super(NutWeekRegionValidationManager, self) \
            .get_queryset().filter(period_type='nut_week_region_validation')


class NutWeekRegionValidationPeriod(WeekPeriod):

    class Meta:
        proxy = True
        verbose_name = _("Week Region Validation Period")
        verbose_name_plural = _("Week Region Validation Periods")

    objects = NutWeekRegionValidationManager()

    @classmethod
    def type(cls):
        return 'nut_week_region_validation'

    @property
    def pid(self):
        return'nWRVP{}'.format(self.middle().strftime('%W-%Y'))

    @classmethod
    def boundaries(cls, date_obj):
        district_val_period = NutWeekDistrictValidationPeriod \
            .find_create_by_date(date_obj, dont_create=True)
        start = district_val_period.end_on + ONE_MICROSECOND_DELTA
        end = start + datetime.timedelta(days=1)
        return start, end

    def strid(self):
        return self.middle().strftime('nWRVP%W-%Y')


class AbstractWeeklyNutritionR(SNISIReport):

    class Meta:
        app_label = 'snisi_nutrition'
        abstract = True

    urenam_screening = models.IntegerField(_("MAM Screening"))
    urenam_cases = models.IntegerField(_("MAM Cases"))
    urenam_deaths = models.IntegerField(_("MAM Deaths"))

    urenas_screening = models.IntegerField(_("SAM Screening"))
    urenas_cases = models.IntegerField(_("SAM Cases"))
    urenas_deaths = models.IntegerField(_("SAM Deaths"))

    ureni_screening = models.IntegerField(_("SAM+ Screening"))
    ureni_cases = models.IntegerField(_("SAM+ Cases"))
    ureni_deaths = models.IntegerField(_("SAM+ Deaths"))

    def screening_fields(self):
        return [field for field in self.data_fields()
                if field.endswith('screening')]

    def cases_fields(self):
        return [field for field in self.data_fields()
                if field.endswith('cases')]

    def deaths_fields(self):
        return [field for field in self.data_fields()
                if field.endswith('deaths')]

    def total_screening(self):
        return sum([getattr(self, field, 0)
                    for field in self.screening_fields()])

    def total_cases(self):
        return sum([getattr(self, field, 0)
                    for field in self.cases_fields()])

    def total_deaths(self):
        return sum([getattr(self, field, 0)
                    for field in self.deaths_fields()])


class WeeklyNutritionR(AbstractWeeklyNutritionR):

    REPORTING_TYPE = PERIODICAL_SOURCE
    RECEIPT_FORMAT = "{period}-WNUT/{id}-{rand}"
    UNIQUE_TOGETHER = [('period', 'entity')]

    class Meta:
        app_label = 'snisi_nutrition'
        verbose_name = _("Weekly Nutrition Report")
        verbose_name_plural = _("Weekly Nutrition Reports")


receiver(pre_save, sender=WeeklyNutritionR)(pre_save_report)
receiver(post_save, sender=WeeklyNutritionR)(post_save_report)

reversion.register(WeeklyNutritionR)


class AggWeeklyNutritionR(PeriodicAggregatedReportInterface, SNISIReport):

    REPORTING_TYPE = PERIODICAL_AGGREGATED
    RECEIPT_FORMAT = "{period}-WNUTa/{id}-{rand}"
    INDIVIDUAL_CLS = WeeklyNutritionR
    UNIQUE_TOGETHER = [('period', 'entity')]

    class Meta:
        app_label = 'snisi_nutrition'
        verbose_name = _("Aggregated Weekly Nutrition Report")
        verbose_name_plural = _("Aggregated Weekly Nutrition Reports")

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


receiver(pre_save, sender=AggWeeklyNutritionR)(pre_save_report)
receiver(post_save, sender=AggWeeklyNutritionR)(post_save_report)

reversion.register(AggWeeklyNutritionR)
