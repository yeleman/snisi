#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging
import datetime

from py3compat import implements_to_string
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _, ugettext
from django.utils.dateformat import format as date_format

from snisi_tools.misc import class_str, import_path

logger = logging.getLogger(__name__)
ONE_SECOND_DELTA = datetime.timedelta(days=0, seconds=1)
ONE_MINUTE_DELTA = datetime.timedelta(days=0, minutes=1)
ONE_MICROSECOND_DELTA = datetime.timedelta(microseconds=1)
ONE_WEEK_DELTA = datetime.timedelta(days=7)


def normalize_date(target, as_aware=True):
    if isinstance(target, datetime.date):
        target = datetime.datetime(*target.timetuple()[:6])
    target_is_aware = timezone.is_aware(target)
    if as_aware and target_is_aware:
        return target
    elif as_aware and not target_is_aware:
        # make foreign object aware (assume UTC)
        return timezone.make_aware(target, timezone.utc)
    else:
        # make foreign object naive
        return timezone.make_naive(target, timezone.utc)


def next_month(year, month):
    """ next year and month as int from year and month """
    if month < 12:
        return (year, month + 1)
    else:
        return (year + 1, 1)


class PeriodsQuerySet(models.QuerySet):

    def days(self):
        return self.filter(period_type=Period.DAY)

    def weeks(self):
        return self.filter(period_type=Period.WEEK)

    def months(self):
        return self.filter(period_type=Period.MONTH)

    def quarters(self):
        return self.filter(period_type=Period.QUARTER)

    def semesters(self):
        return self.filter(period_type=Period.SEMESTER)

    def years(self):
        return self.filter(period_type=Period.YEAR)

    def custom(self):
        return self.exclude(period_type__in=Period.PERIOD_TYPES.keys())


@implements_to_string
class Period(models.Model):
    ''' Represents a Period of time. Base class ; should not be used directly.

    Use DayPeriod, MonthPeriod, etc instead.
    Provides easy way to find/create period for reporting.

    p = MonthPeriod.find_create_from(2011, 3)
    p.following() '''

    class Meta:
        app_label = 'snisi_core'
        unique_together = ('start_on', 'end_on', 'period_type')
        verbose_name = _("Period")
        verbose_name_plural = _("Periods")

    DAY = 'day'
    WEEK = 'week'
    MONTH = 'month'
    QUARTER = 'quarter'
    SEMESTER = 'semester'
    YEAR = 'year'
    CUSTOM = 'custom'

    PERIOD_TYPES = {
        DAY: _("Day"),
        WEEK: _("Week"),
        MONTH: _("Month"),
        QUARTER: _("Quarter"),
        SEMESTER: _("Semester"),
        YEAR: _("Year"),
        CUSTOM: _("Custom"),
    }

    identifier = models.CharField(max_length=200, primary_key=True)
    start_on = models.DateTimeField(_("Start On"))
    end_on = models.DateTimeField(_("End On"))
    period_type = models.CharField(max_length=100,
                                   choices=PERIOD_TYPES.items(),
                                   default=CUSTOM,
                                   verbose_name=_("Type"))

    objects = PeriodsQuerySet.as_manager()
    types = PeriodsQuerySet.as_manager()
    django = models.Manager()

    @property
    def id(self):
        return self.identifier

    def __lt__(self, other):
        try:
            return self.end_on < self.normalize_date(other.start_on)
        except:
            return NotImplemented

    def __le__(self, other):
        try:
            return self.end_on <= self.normalize_date(other.end_on)
        except:
            return NotImplemented

    def __eq__(self, other):
        try:
            return self.pid == other.pid
        except:
            return NotImplemented

    def __ne__(self, other):
        try:
            return self.start_on != self.normalize_date(other.start_on) \
                or self.end_on != self.normalize_date(other.end_on)
        except:
            return NotImplemented

    def __gt__(self, other):
        try:
            return self.start_on > self.normalize_date(other.end_on)
        except:
            return NotImplemented

    def __ge__(self, other):
        try:
            return self.start_on >= self.normalize_date(other.start_on)
        except:
            return NotImplemented

    def duration(self):
        return self.end_on - self.start_on

    def is_over(self, now=None):
        if now is None:
            now = timezone.now()
        now = normalize_date(now)
        return now > self.end_on

    def is_ahead(self, now=None):
        if now is None:
            now = timezone.now()
        now = normalize_date(now)
        return now < self.start_on

    def contains(self, obj):
        if not isinstance(obj, datetime.datetime):
            obj = datetime.datetime(obj.year, obj.month, obj.day) \
                          .replace(tzinfo=timezone.utc)
        nobj = self.normalize_date(obj)
        return nobj >= self.start_on and nobj <= self.end_on

    def normalize_date(self, obj):
        return normalize_date(obj, as_aware=self.is_aware())

    def is_aware(self):
        s = timezone.is_aware(self.start_on)
        e = timezone.is_aware(self.end_on)
        if not s == e:
            raise TypeError("Period boundaries can't mix naive and TZ aware")
        return s and e

    def is_naive(self):
        return not self.is_aware()

    def list_of_subs(self, cls):
        if cls == self.__class__:
            return [self]
        d = []
        n = cls.find_create_by_date(self.start_on, dont_create=True)
        while n.start_on <= self.end_on:
            d.append(n)
            n = cls.find_create_by_date(
                n.start_on + datetime.timedelta(cls.delta()), dont_create=True)
        return d

    def cast(self, cls):
        self.__class__ = cls

    @property
    def days(self):
        return self.list_of_subs(DayPeriod)

    @property
    def weeks(self):
        return self.list_of_subs(WeekPeriod)

    @property
    def months(self):
        return self.list_of_subs(MonthPeriod)

    @property
    def quarters_(self):
        return self.list_of_subs(QuarterPeriod)

    @property
    def years(self):
        return self.list_of_subs(YearPeriod)

    @classmethod
    def type(cls):
        ''' default type for period creation '''
        return cls.CUSTOM

    @classmethod
    def delta(self):
        ''' datetime.timedelta() length of a period. 1 = one day. '''
        return 1.0 // 24

    @property
    def pid(self):
        ''' A locale safe identifier of the period '''
        return self.middle().strftime('%s')

    def middle(self):
        ''' datetime.datetime at half of the period duration '''
        return self.start_on + ((self.end_on - self.start_on) // 2)

    def __str__(self):
        return self.casted().name()

    def name(self):
        try:
            cls = eval("{}Period".format(self.period_type.title()))
            return cls.objects.get(id=self.id).name()
        except:
            # TRANSLATORS: Django date format for Generic .name()
            return date_format(self.middle(), ugettext("c"))

    def strid(self):
        return self.middle().strftime('%s')

    def full_name(self):
        return self.name()

    def following(self):
        ''' returns next period in time '''
        return self.casted().find_create_by_date(
            self.middle() + datetime.timedelta(self.casted().delta()))

    def previous(self):
        ''' returns next period in time '''
        return self.casted().find_create_by_date(
            self.middle() - datetime.timedelta(self.casted().delta()))

    @classmethod
    def all_from(cls, first_period, last_period=None):
        periods = []
        if last_period is None:
            last_period = cls.current()
        p = first_period
        while p <= last_period:
            periods.append(p)
            p = p.following()
        return periods

    @classmethod
    def boundaries(cls, date_obj):
        ''' start and end dates of a period from a datetime.date. '''
        start = date_obj - datetime.timedelta(cls.delta() // 2)
        end = start + cls.delta()
        return (start, end)

    def includes(self, date_obj):
        ''' check if provided value is within this Period's scope

        date_obj can be:
         * datetime.datetime instance
         * datetime.date instance
         * integer (year) '''

        date_obj = self.normalize_date(date_obj)
        if isinstance(date_obj, datetime.date):
            date_obj = datetime.datetime(date_obj.year,
                                         date_obj.month,
                                         date_obj.day, 12, 0) \
                .replace(tzinfo=timezone.utc)
        if isinstance(date_obj, datetime.datetime):
            return self.normalize_date(self.start_on) \
                < self.normalize_date(date_obj) \
                and self.normalize_date(self.end_on) \
                > self.normalize_date(date_obj)
        elif isinstance(date_obj, int):
            pass
        return False
        # not sure what to do??
        raise ValueError("Can not understand datetime.date object.")

    @classmethod
    def find_create_from(cls, year, month=None, day=None,
                         week=None, hour=None, minute=None, second=None,
                         dont_create=False,
                         is_iso=False, is_precise=False):

        if not week and not month:
            # assume year search
            sy = datetime.datetime(year, 1, 1, 0, 0, tzinfo=timezone.utc)
            ey = sy.replace(year=year + 1) - ONE_MICROSECOND_DELTA
            try:
                period = cls.objects.filter(start_on__lte=sy,
                                            end_on__gte=ey)[0]
            except IndexError:
                period = cls.find_create_with(sy, ey)
            return period

        if week:
            return cls.find_create_by_weeknum(year=year,
                                              weeknum=week, is_iso=is_iso)

        month = month if month else 1
        day = day if day else 1
        hour = hour if hour else 0
        minute = minute if minute else 0
        second = second if second else 0

        date_obj = datetime.datetime(year, month, day, hour, minute, second,
                                     tzinfo=timezone.utc)
        if not is_precise:
            date_obj += datetime.timedelta(days=cls.delta() // 2)

        period = cls.find_create_by_date(date_obj, dont_create)

        return period

    @classmethod
    def find_create_by_date(cls, date_obj, dont_create=False):
        ''' creates a period to fit the provided date in '''
        if not isinstance(date_obj, datetime.datetime):
            date_obj = datetime.datetime.fromtimestamp(
                float(date_obj.strftime('%s')))
            date_obj = datetime.datetime(date_obj.year, date_obj.month,
                                         date_obj.day,
                                         date_obj.hour,
                                         date_obj.minute, 1,
                                         tzinfo=timezone.utc)

        date_obj = normalize_date(date_obj, as_aware=True)
        try:
            period = [period for period in cls.objects.all()
                      if period.start_on <= date_obj
                      and period.end_on >= date_obj][0]
        except IndexError:
            try:
                period = cls.find_create_with(*cls.boundaries(date_obj))
            except:
                return None
            if dont_create:
                return period
            period.save()
        return period

    @classmethod
    def find_create_with(cls, start_on, end_on, period_type=None):
        ''' creates a period with defined start and end dates '''
        start_on = normalize_date(start_on, as_aware=True)
        end_on = normalize_date(end_on, as_aware=True)
        if not period_type:
            period_type = cls.type()
        try:
            period = cls.objects.get(start_on=start_on,
                                     end_on=end_on, period_type=period_type)
        except cls.DoesNotExist:
            period = cls(start_on=start_on, end_on=end_on,
                         period_type=period_type)
            period.save()
        return period

    @classmethod
    def find_create_by_weeknum(cls, year, weeknum, is_iso=False):

        # version 1
        # sw, ew = week_from_weeknum(year, week, is_iso=is_iso)
        # period = cls.find_create_with(sw, ew)
        # return period

        # version 2
        # soy = date(year, 1, 1)
        # d = soy + datetime.timedelta(WeekPeriod.delta() * weeknum)
        # return cls.find_create_by_date(d)

        sy = datetime.datetime(year, 1, 1, 0, 0, tzinfo=timezone.utc)
        # ey = datetime.datetime(year, 12, 31, 23, 59)
        ONE_WEEK = WeekPeriod.delta()

        # retrieve start of year day
        sy_dow = sy.isoweekday() if is_iso else sy.weekday()

        # find first real week (first Mon/Sun)
        if sy_dow != 0:
            sy = sy + datetime.timedelta(ONE_WEEK - sy_dow)

        # if we want first week, it's from Jan 1st to next Mon/Sun
        if weeknum == 0:
            start_week = sy
            end_week = start_week + datetime.timedelta(ONE_WEEK - sy_dow) \
                - ONE_SECOND_DELTA
        else:
            weeknum -= 1  # cause we've set start as first real week
            start_week = sy + datetime.timedelta(ONE_WEEK * weeknum)
            end_week = start_week + datetime.timedelta(ONE_WEEK) \
                - ONE_SECOND_DELTA

        period = cls.find_create_with(start_week, end_week)
        return period

    @classmethod
    def find_create_by_quarter(cls, year, quarter):
        return YearPeriod.find_create_from(year, dont_create=True) \
                         .quarters_[quarter - 1]

    @classmethod
    def current(cls, dont_create=False):
        return cls.find_create_by_date(date_obj=datetime.date.today(),
                                       dont_create=dont_create)

    @classmethod
    def from_url_str(cls, period_str):

        year = indice = sub_indice = prefix = None

        def fail():
            raise ValueError(u"Incorrect period.")

        if not len(period_str):
            fail()

        if period_str.lower()[0] in ('q', 'w'):
            prefix = period_str.lower()[0]
            period_str = period_str[1:]

        parts = period_str.split('-')
        if not len(parts) in (1, 2, 3):
            fail()

        try:
            year = int(parts.pop())
            if len(parts):
                indice = int(parts.pop())

            if len(parts):
                sub_indice = int(parts.pop())

        except ValueError:
            fail()

        """
        FORMATS:

        YEAR:       2013                            [0-9]{4}
        MONTH:      01-2013                         [0-9]{2}-[0-9]{4}
        QUARTER:    Q1-2013                         Q[1-3]-[0-9]{4}
        WEEK:       W1-2013                         W[0-9]{1,2}-[0-9]{4}
        DAY:        01-01-2013                      [0-9]{2}-[0-9]{2}-[0-9]{4}
        """

        if sub_indice is not None:
            period = DayPeriod.find_create_from(year, indice, sub_indice)

        elif prefix == 'w':
            period = WeekPeriod.find_create_by_weeknum(year, indice)

        elif prefix == 'q':
            period = QuarterPeriod.find_create_by_quarter(year, indice)

        elif indice is not None:
            period = MonthPeriod.find_create_from(year, month=indice)

        else:
            period = YearPeriod.find_create_from(year)
        return period

    def get_day_periods(self):
        days = [DayPeriod.find_create_by_date(self.start_on)]
        while True:
            day = days[-1].following()
            if day.end_on <= self.end_on:
                days.append(day)
            else:
                break
        return days

    def save(self, *args, **kwargs):
        # update pk so it reflects the period data.
        # we want to make sure any FK remains attached to the correct
        # period despite mass creation/deletion of periods.
        self.identifier = '{cls}_{start_on}_{end_on}'.format(
            cls=class_str(self),
            start_on=self.start_on.strftime('%s'),
            end_on=self.end_on.strftime('%s'))
        return super(Period, self).save(*args, **kwargs)

    def casted(self):
        try:
            cls = import_path(self.identifier.rsplit('_', 2)[0])
        except (IndexError, AttributeError, ImportError):
            cls = self.__class__
        return cls.objects.get(identifier=self.identifier)


class SpecificTypeManager(models.Manager):
    SPECIFIC_TYPE = Period.CUSTOM

    def get_queryset(self):
        return super(SpecificTypeManager, self) \
            .get_queryset().filter(period_type=self.SPECIFIC_TYPE)


class DayManager(SpecificTypeManager):
    SPECIFIC_TYPE = Period.DAY


class WeekManager(SpecificTypeManager):
    SPECIFIC_TYPE = Period.WEEK


class MonthManager(SpecificTypeManager):
    SPECIFIC_TYPE = Period.MONTH


class QuarterManager(SpecificTypeManager):
    SPECIFIC_TYPE = Period.QUARTER


class SemesterManager(SpecificTypeManager):
    SPECIFIC_TYPE = Period.SEMESTER


class YearManager(SpecificTypeManager):
    SPECIFIC_TYPE = Period.YEAR


class DayPeriod(Period):

    class Meta:
        proxy = True
        app_label = 'snisi_core'
        verbose_name = _("Period")
        verbose_name_plural = _("Periods")

    objects = DayManager()

    @classmethod
    def type(cls):
        return cls.DAY

    def name(self):
        # Translators: Django's date format for DayPeriod.name()
        return date_format(self.middle(), ugettext("m/d/Y"))

    def full_name(self):
        # Translators: Django's date format for DayPeriod.full_name()
        return date_format(self.middle(), ugettext("F d Y"))

    @classmethod
    def delta(self):
        return 1

    @classmethod
    def boundaries(cls, date_obj):
        date_obj = normalize_date(date_obj, as_aware=True)

        start = date_obj.replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + datetime.timedelta(cls.delta()) - ONE_MICROSECOND_DELTA
        return (start, end)

    def strid(self):
        return self.middle().strftime('%d-%m-%Y')


class WeekPeriod(Period):

    class Meta:
        proxy = True
        app_label = 'snisi_core'
        verbose_name = _("Period")
        verbose_name_plural = _("Periods")

    objects = WeekManager()

    @classmethod
    def type(cls):
        return cls.WEEK

    @property
    def pid(self):
        return'W{}'.format(self.middle().strftime('%W-%Y'))

    def name(self):
        # Translators: Django's date format for WeekPeriod.name()
        return date_format(self.middle(), ugettext("W/Y"))

    def full_name(self):
        # Translators: Week Full name representation: weeknum, start and end
        return ugettext("Week %(weeknum)s (%(start)s to %(end)s)".format(
            weeknum=date_format(self.middle(), ugettext("W")),
            start=date_format(self.start_on, ugettext("d")),
            end=date_format(self.end_on, ugettext("d F Y"))))

    @classmethod
    def delta(self):
        return 7

    @classmethod
    def boundaries(cls, date_obj):
        date_obj = normalize_date(date_obj, as_aware=True)

        start = date_obj - datetime.timedelta(date_obj.weekday())
        start = start.replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + datetime.timedelta(cls.delta()) - ONE_MICROSECOND_DELTA
        return (start, end)

    def strid(self):
        return self.middle().strftime('W%W-%Y')


class MonthPeriod(Period):

    class Meta:
        proxy = True
        app_label = 'snisi_core'
        verbose_name = _("Period")
        verbose_name_plural = _("Periods")

    objects = MonthManager()

    @classmethod
    def type(cls):
        return cls.MONTH

    @property
    def pid(self):
        return self.middle().strftime('%m%Y')

    def name(self):
        # Translators: Django's date template format for MonthPeriod.name()
        return date_format(self.middle(), ugettext("F Y"))

    def full_name(self):
        # Translators: Django's date tmpl format for MonthPeriod.full_name()
        return date_format(self.middle(), ugettext("F Y"))

    @classmethod
    def delta(self):
        return 31

    @classmethod
    def boundaries(cls, date_obj):
        date_obj = normalize_date(date_obj, as_aware=True)

        nyear, nmonth = next_month(date_obj.year, date_obj.month)

        start = date_obj.replace(day=1, hour=0, minute=0,
                                 second=0, microsecond=0)
        end = start.replace(year=nyear, month=nmonth) \
            - ONE_MICROSECOND_DELTA
        return (start, end)

    def strid(self):
        return self.middle().strftime('%m-%Y')


class QuarterPeriod(Period):

    class Meta:
        proxy = True
        app_label = 'snisi_core'
        verbose_name = _("Period")
        verbose_name_plural = _("Periods")

    objects = QuarterManager()

    @classmethod
    def type(cls):
        return cls.QUARTER

    @property
    def quarter(self):
        m = self.middle().month
        if m in (1, 2, 3):
            return 1
        elif m in (4, 5, 6):
            return 2
        elif m in (7, 8, 9):
            return 3
        else:
            return 4

    @property
    def pid(self):
        return 'Q{:d}.{}'.format((self.quarter, self.middle().strftime('%Y')))

    def name(self):
        # Translators: django date format for accomp Quarter in Quarter.name()
        drepr = date_format(self.middle(), ugettext("Y"))
        # Translators: Quarter.name() repr using Quarter number and other
        return ugettext("Q%(quarter)s.%(year)s").format(
            year=drepr,
            quarter=self.quarter)

    def full_name(self):
        def ordinal(value):
            try:
                value = int(value)
            except ValueError:
                return value

            if value % 100 // 10 != 1:
                if value % 10 == 1:
                    # Translators: suffix for 1st
                    ordval = "{:d}{}".format((value, ugettext("st")))
                elif value % 10 == 2:
                    # Translators: suffix for 2nd
                    ordval = "{:d}{}".format((value, ugettext("nd")))
                elif value % 10 == 3:
                    # Translators: suffix for 3rd
                    ordval = "{:d}{}".format((value, ugettext("rd")))
                else:
                    # Translators: suffix for 4th
                    ordval = "{:d}{}".format((value, ugettext("th")))
            else:
                # Translators: suffix for 5th
                ordval = "{:d}{}".format((value, ugettext("th")))

            return ordval

        # Translators: Django's date format for QuarterPeriod.full_name()
        return ("%(ordinal_quarter)s Quarter %(year)s "
                "(%(start)s to %(end)s)").format(
            ordinal_quarter=ordinal(self.quarter),
            year=date_format(self.middle(), ugettext("Y")),
            start=date_format(self.start_on, ugettext("F")),
            end=date_format(self.end_on, ugettext("F Y")))

    @classmethod
    def delta(self):
        return 93

    @classmethod
    def boundaries(cls, date_obj):

        date_obj = normalize_date(date_obj, as_aware=True)

        clean_start = date_obj.replace(month=1, day=1, hour=0, minute=0,
                                       second=0, microsecond=0)
        clean_end = clean_start - ONE_MICROSECOND_DELTA
        clean_end = clean_end.replace(year=date_obj.year)

        if date_obj.month in (1, 2, 3):
            start = clean_start.replace(month=1)
            end = start.replace(month=4) - ONE_MICROSECOND_DELTA
        elif date_obj.month in (4, 5, 6):
            start = clean_start.replace(month=4)
            end = start.replace(month=7) - ONE_MICROSECOND_DELTA
        elif date_obj.month in (7, 8, 9):
            start = clean_start.replace(month=7)
            end = start.replace(month=10) - ONE_MICROSECOND_DELTA
        else:
            start = clean_start.replace(month=10)
            end = clean_end

        return (start, end)

    def strid(self):
        return 'Q{}-{}'.format(str(self.quarter).zfill(2),
                               self.middle().strftime('%Y'))


class YearPeriod(Period):

    class Meta:
        proxy = True
        app_label = 'snisi_core'
        verbose_name = _("Period")
        verbose_name_plural = _("Periods")

    objects = YearManager()

    @classmethod
    def type(cls):
        return cls.YEAR

    def name(self):
        # Translators: Django's date format for YearPeriod.name()
        return date_format(self.middle(), ugettext("F"))

    def full_name(self):
        return self.name()

    @classmethod
    def delta(self):
        return 365

    @classmethod
    def boundaries(cls, date_obj):
        date_obj = normalize_date(date_obj, as_aware=True)

        start = date_obj.replace(month=0, day=0, hour=0, minute=0,
                                 second=0, microsecond=0)
        end = start.replace(year=date_obj.year + 1) - ONE_MICROSECOND_DELTA
        return (start, end)

    def strid(self):
        return self.middle().strftime('%Y')


class FixedDaysPeriod(Period):

    class Meta:
        proxy = True
        app_label = 'snisi_core'
        verbose_name = _("Fixed Days Period")
        verbose_name_plural = _("Fixed Days Periods")

    def nb_days(self):
        return self.duration().days

    def name(self):
        # Translators: Django's date template format for MonthPeriod.name()
        return date_format(self.middle(), ugettext("{sd}-{ed} F Y").format(
            sd=self.start_on.day, ed=self.end_on.day))

    def full_name(self):
        # Translators: Django's date tmpl format for MonthPeriod.full_name()
        return date_format(self.middle(), ugettext("{sd} to {ed} F Y").format(
            sd=self.start_on.day, ed=self.end_on.day))

    def strid(self):
        return self.middle().strftime('[{sd}-{ed}}]-%m-%Y').format(
            sd=self.start_on.day, ed=self.end_on.day)
