#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import re
import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext
from django.utils.dateformat import format as date_format
from django.utils import timezone

from snisi_core.models.Periods import MonthPeriod, ONE_MICROSECOND_DELTA
from snisi_tools.datetime import normalize_date


class FixedMonthFirstWeekManager(models.Manager):
    def get_queryset(self):
        return super(FixedMonthFirstWeekManager, self) \
            .get_queryset().filter(period_type=FixedMonthFirstWeek.FWP)


class FixedMonthSecondWeekManager(models.Manager):
    def get_queryset(self):
        return super(FixedMonthSecondWeekManager, self) \
            .get_queryset().filter(period_type=FixedMonthSecondWeek.FWP)


class FixedMonthThirdWeekManager(models.Manager):
    def get_queryset(self):
        return super(FixedMonthThirdWeekManager, self) \
            .get_queryset().filter(period_type=FixedMonthThirdWeek.FWP)


class FixedMonthFourthWeekManager(models.Manager):
    def get_queryset(self):
        return super(FixedMonthFourthWeekManager, self) \
            .get_queryset().filter(period_type=FixedMonthFourthWeek.FWP)


class FixedMonthFifthWeekManager(models.Manager):
    def get_queryset(self):
        return super(FixedMonthFifthWeekManager, self) \
            .get_queryset().filter(period_type=FixedMonthFifthWeek.FWP)


class FixedMonthFirstWeek(MonthPeriod):

    FWP = 'fixed_month_first_week'
    FIXED_WEEK_NUM = 1

    class Meta:
        proxy = True
        app_label = 'snisi_core'
        verbose_name = _("Monthly Reporting Period")
        verbose_name_plural = _("Monthly Reporting Periods")

    objects = FixedMonthFirstWeekManager()

    @classmethod
    def from_url_str(cls, period_str):
        return FixedMonthWeek.from_url_str(period_str)

    @classmethod
    def type(cls):
        return cls.FWP

    @property
    def pid(self):
        return self.middle().strftime('FM1W%m%Y')

    def name(self):
        # Translators: Django's date template format for MonthPeriod.name()
        return date_format(self.middle(), ugettext("1-7 F Y"))

    def full_name(self):
        # Translators: Django's date tmpl format for MonthPeriod.full_name()
        return date_format(self.middle(), ugettext("1st to 7th F Y"))

    @classmethod
    def delta(self):
        return 31

    @classmethod
    def boundaries(cls, date_obj):
        date_obj = normalize_date(date_obj, as_aware=True)
        start = date_obj.replace(day=1, hour=0, minute=0,
                                 second=0, microsecond=0)
        end = start.replace(day=8) - ONE_MICROSECOND_DELTA
        return (start, end)

    def strid(self):
        return self.pid
        return self.middle().strftime('[1-7]-%m-%Y')


class FixedMonthSecondWeek(MonthPeriod):

    FWP = 'fixed_month_second_week'
    FIXED_WEEK_NUM = 2

    class Meta:
        proxy = True
        app_label = 'snisi_core'
        verbose_name = _("Monthly Reporting Period")
        verbose_name_plural = _("Monthly Reporting Periods")

    objects = FixedMonthSecondWeekManager()

    @classmethod
    def from_url_str(cls, period_str):
        return FixedMonthWeek.from_url_str(period_str)

    @classmethod
    def type(cls):
        return cls.FWP

    @property
    def pid(self):
        return self.middle().strftime('FM2W%m%Y')

    def name(self):
        # Translators: Django's date template format for MonthPeriod.name()
        return date_format(self.middle(), ugettext("8-14 F Y"))

    def full_name(self):
        # Translators: Django's date tmpl format for MonthPeriod.full_name()
        return date_format(self.middle(), ugettext("8th to 14th F Y"))

    @classmethod
    def delta(self):
        return 31

    @classmethod
    def boundaries(cls, date_obj):
        date_obj = normalize_date(date_obj, as_aware=True)
        start = date_obj.replace(day=8, hour=0, minute=0,
                                 second=0, microsecond=0)
        end = start.replace(day=15) - ONE_MICROSECOND_DELTA
        return (start, end)

    def strid(self):
        return self.pid
        return self.middle().strftime('[8-14]-%m-%Y')


class FixedMonthThirdWeek(MonthPeriod):

    FWP = 'fixed_month_third_week'
    FIXED_WEEK_NUM = 3

    class Meta:
        proxy = True
        app_label = 'snisi_core'
        verbose_name = _("Monthly Reporting Period")
        verbose_name_plural = _("Monthly Reporting Periods")

    objects = FixedMonthThirdWeekManager()

    @classmethod
    def from_url_str(cls, period_str):
        return FixedMonthWeek.from_url_str(period_str)

    @classmethod
    def type(cls):
        return cls.FWP

    @property
    def pid(self):
        return self.middle().strftime('FM3W%m%Y')

    def name(self):
        # Translators: Django's date template format for MonthPeriod.name()
        return date_format(self.middle(), ugettext("15-21 F Y"))

    def full_name(self):
        # Translators: Django's date tmpl format for MonthPeriod.full_name()
        return date_format(self.middle(), ugettext("15th to 21th F Y"))

    @classmethod
    def delta(self):
        return 31

    @classmethod
    def boundaries(cls, date_obj):
        date_obj = normalize_date(date_obj, as_aware=True)
        start = date_obj.replace(day=15, hour=0, minute=0,
                                 second=0, microsecond=0)
        end = start.replace(day=22) - ONE_MICROSECOND_DELTA
        return (start, end)

    def strid(self):
        return self.pid
        return self.middle().strftime('[15-21]-%m-%Y')


class FixedMonthFourthWeek(MonthPeriod):

    FWP = 'fixed_month_fourth_week'
    FIXED_WEEK_NUM = 4

    class Meta:
        proxy = True
        app_label = 'snisi_core'
        verbose_name = _("Monthly Reporting Period")
        verbose_name_plural = _("Monthly Reporting Periods")

    objects = FixedMonthFourthWeekManager()

    @classmethod
    def from_url_str(cls, period_str):
        return FixedMonthWeek.from_url_str(period_str)

    @classmethod
    def type(cls):
        return cls.FWP

    @property
    def pid(self):
        return self.middle().strftime('FM4W%m%Y')

    def name(self):
        # Translators: Django's date template format for MonthPeriod.name()
        return date_format(self.middle(), ugettext("22-28 F Y"))

    def full_name(self):
        # Translators: Django's date tmpl format for MonthPeriod.full_name()
        return date_format(self.middle(), ugettext("22th to 28th F Y"))

    @classmethod
    def delta(self):
        return 31

    @classmethod
    def boundaries(cls, date_obj):
        date_obj = normalize_date(date_obj, as_aware=True)
        start = date_obj.replace(day=22, hour=0, minute=0,
                                 second=0, microsecond=0)
        end = start.replace(day=28, hour=23, minute=59,
                            second=59, microsecond=59)
        return (start, end)

    def strid(self):
        return self.pid
        return self.middle().strftime('[22-28]-%m-%Y')


class FixedMonthFifthWeek(MonthPeriod):

    FWP = 'fixed_month_fifth_week'
    FIXED_WEEK_NUM = 5

    class Meta:
        proxy = True
        app_label = 'snisi_core'
        verbose_name = _("Fifth Monthly Reporting Period")
        verbose_name_plural = _("Monthly Reporting Periods")

    objects = FixedMonthFifthWeekManager()

    @classmethod
    def from_url_str(cls, period_str):
        return FixedMonthWeek.from_url_str(period_str)

    @classmethod
    def type(cls):
        return cls.FWP

    @property
    def pid(self):
        return self.middle().strftime('FM5W%m%Y')

    def name(self):
        # Translators: Django's date template format for MonthPeriod.name()
        return date_format(self.middle(), ugettext("29+ F Y"))

    def full_name(self):
        # Translators: Django's date tmpl format for MonthPeriod.full_name()
        return date_format(self.middle(), ugettext("29th + F Y"))

    @classmethod
    def delta(self):
        return 31

    @classmethod
    def boundaries(cls, date_obj):
        date_obj = normalize_date(date_obj, as_aware=True)
        start = date_obj.replace(day=29, hour=0, minute=0,
                                 second=0, microsecond=0)
        end = MonthPeriod.find_create_by_date(date_obj,
                                              dont_create=True).following() \
                         .start_on - ONE_MICROSECOND_DELTA
        return (start, end)

    def strid(self):
        return self.pid
        return self.middle().strftime('[29+]-%m-%Y')


class FixedMonthWeek(object):

    week_classes = [
        FixedMonthFirstWeek,
        FixedMonthSecondWeek,
        FixedMonthThirdWeek,
        FixedMonthFourthWeek,
        FixedMonthFifthWeek
    ]

    @classmethod
    def from_url_str(cls, period_str):
        if not re.match(r'^FM[1-5]W[0-9]{2}[0-9]{4}$', period_str):
            raise ValueError("Not a FixedMonthWeek")

        pcls = cls.week_classes[int(period_str[2]) - 1]
        month = int(period_str[4:6])
        year = int(period_str[-4:])
        return pcls.find_create_from(year=year, month=month)

    @classmethod
    def get_fxp_class(cls, at=None):
        if at is None:
            at = timezone.now()
        day = at.day
        if day <= 7:
            ccls = FixedMonthFirstWeek
        elif day <= 14:
            ccls = FixedMonthSecondWeek
        elif day <= 21:
            ccls = FixedMonthThirdWeek
        elif day <= 28:
            ccls = FixedMonthFourthWeek
        else:
            ccls = FixedMonthFifthWeek
        return ccls

    @classmethod
    def find_create_by_date(cls, date_obj, dont_create=False):
        return cls.get_fxp_class(at=date_obj) \
            .find_create_by_date(date_obj=date_obj, dont_create=dont_create)

    @classmethod
    def current(cls, at=None):
        if at is None:
            at = timezone.now()
        return cls.get_fxp_class(at=at) \
            .find_create_from(year=at.year, month=at.month)

    @classmethod
    def all_from(cls, first_period, last_period=None):
        l = []
        p = first_period
        while p <= last_period:
            l.append(p)
            p = cls.find_create_by_date(p.end_on + datetime.timedelta(days=1))
        return l

    @classmethod
    def previous_week(cls, reference):
        idx = cls.week_classes.index(reference.__class__)
        if idx == 0:
            ncls = cls.week_classes[-1]
            nmonth = MonthPeriod.find_create_by_date(reference.middle())
            at = nmonth.previous().middle()
        else:
            ncls = cls.week_classes[idx - 1]
            at = reference.middle()
        return ncls.find_create_by_date(at)

    @classmethod
    def following_week(cls, reference):
        idx = cls.week_classes.index(reference.__class__)
        if idx == len(cls.week_classes) - 1:
            ncls = cls.week_classes[0]
            nmonth = MonthPeriod.find_create_by_date(reference.middle())
            at = nmonth.next().middle()
        else:
            ncls = cls.week_classes[idx + 1]
            at = reference.middle()
        return ncls.find_create_by_date(at)
