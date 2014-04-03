#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext
from django.utils.dateformat import format as date_format

from snisi_core.models.Periods import MonthPeriod, ONE_MICROSECOND_DELTA
from snisi_tools.datetime import normalize_date


class DistrictValidationManager(models.Manager):
    def get_query_set(self):
        return super(DistrictValidationManager, self) \
            .get_query_set().filter(period_type=DefaultDistrictValidationPeriod.DVP)


class DefaultDistrictValidationPeriod(MonthPeriod):

    DVP = 'distrit_validation'

    class Meta:
        proxy = True
        app_label = 'snisi_core'
        verbose_name = _("District Validation Period")
        verbose_name_plural = _("District Validation Periods")

    objects = DistrictValidationManager()

    @classmethod
    def type(cls):
        return cls.DVP

    @property
    def pid(self):
        return self.middle().strftime('DVP%m%Y')

    def name(self):
        # Translators: Django's date template format for MonthPeriod.name()
        return date_format(self.middle(), ugettext("1-15 F Y"))

    def full_name(self):
        # Translators: Django's date template format for MonthPeriod.full_name()
        return date_format(self.middle(), ugettext("1st to 15th F Y"))

    @classmethod
    def delta(self):
        return 31

    @classmethod
    def boundaries(cls, date_obj):
        date_obj = normalize_date(date_obj, as_aware=True)
        start = date_obj.replace(day=1, hour=0, minute=0,
                                 second=0, microsecond=0)
        end = start.replace(day=16) - ONE_MICROSECOND_DELTA
        return (start, end)

    def strid(self):
        return self.middle().strftime('[1-15]-%m-%Y')


class RegionValidationManager(models.Manager):
    def get_query_set(self):
        return super(RegionValidationManager, self) \
            .get_query_set().filter(period_type=DefaultRegionValidationPeriod.RVP)


class DefaultRegionValidationPeriod(MonthPeriod):

    RVP = 'region_validation'

    class Meta:
        proxy = True
        app_label = 'snisi_core'
        verbose_name = _("Region Validation Period")
        verbose_name_plural = _("Region Validation Periods")

    objects = RegionValidationManager()

    @classmethod
    def type(cls):
        return cls.RVP

    @property
    def pid(self):
        return self.middle().strftime('RVP%m%Y')

    def name(self):
        # Translators: Django's date template format for MonthPeriod.name()
        return date_format(self.middle(), ugettext("15-25 F Y"))

    def full_name(self):
        # Translators: Django's date template format for MonthPeriod.full_name()
        return date_format(self.middle(), ugettext("15th to 25th F Y"))

    @classmethod
    def delta(self):
        return 31

    @classmethod
    def boundaries(cls, date_obj):
        date_obj = normalize_date(date_obj, as_aware=True)
        start = date_obj.replace(day=16, hour=0, minute=0,
                                 second=0, microsecond=0)
        end = start.replace(day=26) - ONE_MICROSECOND_DELTA
        return (start, end)

    def strid(self):
        return self.middle().strftime('[16-25]-%m-%Y')


class NationalValidationManager(models.Manager):
    def get_query_set(self):
        return super(NationalValidationManager, self) \
            .get_query_set().filter(period_type=DefaultNationalValidationPeriod.NVP)


class DefaultNationalValidationPeriod(MonthPeriod):

    NVP = 'national_validation'

    class Meta:
        proxy = True
        app_label = 'snisi_core'
        verbose_name = _("National Validation Period")
        verbose_name_plural = _("National Validation Periods")

    objects = NationalValidationManager()

    @classmethod
    def type(cls):
        return cls.NVP

    @property
    def pid(self):
        return self.middle().strftime('NVP%m%Y')

    def name(self):
        # Translators: Django's date template format for MonthPeriod.name()
        return date_format(self.middle(), ugettext("26-27 F Y"))

    def full_name(self):
        # Translators: Django's date template format for MonthPeriod.full_name()
        return date_format(self.middle(), ugettext("26th to 27th F Y"))

    @classmethod
    def delta(self):
        return 31

    @classmethod
    def boundaries(cls, date_obj):
        date_obj = normalize_date(date_obj, as_aware=True)
        start = date_obj.replace(day=26, hour=0, minute=0,
                                 second=0, microsecond=0)
        end = start.replace(day=28) - ONE_MICROSECOND_DELTA
        return (start, end)

    def strid(self):
        return self.middle().strftime('[26-28]-%m-%Y')
