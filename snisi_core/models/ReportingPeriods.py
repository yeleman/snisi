#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import datetime
import logging

from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext
from django.utils.dateformat import format as date_format

from snisi_core.models.Periods import (MonthPeriod,
                                       ONE_MICROSECOND_DELTA, ONE_MINUTE_DELTA)
from snisi_core.models.FixedWeekPeriods import (FixedMonthFirstWeek,
                                                FixedMonthSecondWeek,
                                                FixedMonthThirdWeek,
                                                FixedMonthFourthWeek,
                                                FixedMonthFifthWeek)
from snisi_tools.datetime import normalize_date

logger = logging.getLogger(__name__)


class MonthlyReportingManager(models.Manager):
    def get_queryset(self):
        return super(MonthlyReportingManager, self).get_queryset().filter(
            period_type=DefaultMonthlyReportingPeriod.DMRP)


class DefaultMonthlyReportingPeriod(MonthPeriod):

    DMRP = 'monthly_reporting'

    class Meta:
        proxy = True
        app_label = 'snisi_core'
        verbose_name = _("Monthly Reporting Period")
        verbose_name_plural = _("Monthly Reporting Periods")

    objects = MonthlyReportingManager()

    @classmethod
    def type(cls):
        return cls.DMRP

    @property
    def pid(self):
        return self.middle().strftime('MRP%m%Y')

    def name(self):
        # Translators: Django's date template format for MonthPeriod.name()
        return date_format(self.middle(), ugettext("1-5 F Y"))

    def full_name(self):
        # Translators: Django's date tmpl format for MonthPeriod.full_name()
        return date_format(self.middle(), ugettext("1st to 5th F Y"))

    @classmethod
    def delta(self):
        return 31

    @classmethod
    def boundaries(cls, date_obj):
        date_obj = normalize_date(date_obj, as_aware=True)
        start = date_obj.replace(day=1, hour=0, minute=0,
                                 second=0, microsecond=0)
        end = start.replace(day=6) - ONE_MICROSECOND_DELTA
        return (start, end)

    def strid(self):
        return self.middle().strftime('[1-5]-%m-%Y')


class MonthlyExtendedReportingManager(models.Manager):
    def get_queryset(self):
        return super(MonthlyExtendedReportingManager, self) \
            .get_queryset().filter(
                period_type=DefaultMonthlyExtendedReportingPeriod.DMERP)


class DefaultMonthlyExtendedReportingPeriod(MonthPeriod):

    DMERP = 'monthly_extended_reporting'

    class Meta:
        proxy = True
        app_label = 'snisi_core'
        verbose_name = _("Monthly Extended Reporting Period")
        verbose_name_plural = _("Monthly Extended Reporting Periods")

    objects = MonthlyExtendedReportingManager()

    @classmethod
    def type(cls):
        return cls.DMERP

    @property
    def pid(self):
        return self.middle().strftime('MERP%m%Y')

    def name(self):
        # Translators: Django's date template format for MonthPeriod.name()
        return date_format(self.middle(), ugettext("6-10 F Y"))

    def full_name(self):
        # Translators: Django's date tmpl format for MonthPeriod.full_name()
        return date_format(self.middle(), ugettext("6th to 10th F Y"))

    @classmethod
    def delta(self):
        return 31

    @classmethod
    def boundaries(cls, date_obj):
        date_obj = normalize_date(date_obj, as_aware=True)
        start = date_obj.replace(day=6, hour=0, minute=0,
                                 second=0, microsecond=0)
        end = start.replace(day=11) - ONE_MICROSECOND_DELTA
        return (start, end)

    def strid(self):
        return self.middle().strftime('[6-10]-%m-%Y')


class FixedMonthFirstWeekReportingManager(models.Manager):
    def get_queryset(self):
        return super(FixedMonthFirstWeekReportingManager, self) \
            .get_queryset().filter(
                period_type=FixedMonthFirstWeekReportingPeriod.FWP)


class FixedMonthFirstWeekReportingPeriod(MonthPeriod):

    FWP = 'fixed_month_first_week_reporting_period'

    class Meta:
        proxy = True
        app_label = 'snisi_core'
        verbose_name = _("Monthly Reporting Period")
        verbose_name_plural = _("Monthly Reporting Periods")

    objects = FixedMonthFirstWeekReportingManager()

    @classmethod
    def type(cls):
        return cls.FWP

    @property
    def pid(self):
        return self.middle().strftime('FM1WRP%m%Y')

    def name(self):
        # Translators: Django's date tmpl format for MonthPeriod.name()
        return ugettext("W1/RP {}").format(date_format(
            self.middle(), ugettext("F Y")))

    def full_name(self):
        # Translators: Django's date tmpl format for MonthPeriod.full_name()
        return ugettext("W1/RP {}").format(date_format(
            self.middle(), ugettext("F Y")))

    @classmethod
    def delta(self):
        return 31

    @classmethod
    def boundaries(cls, date_obj):
        fw = FixedMonthFirstWeek.find_create_by_date(
            date_obj, dont_create=True)
        start = fw.end_on + ONE_MINUTE_DELTA
        end = start + datetime.timedelta(days=2) - ONE_MICROSECOND_DELTA
        return (start, end)

    def strid(self):
        return "[W1/RP]-{}".format(self.middle().strftime('%m-%Y'))


class FixedMonthSecondWeekReportingManager(models.Manager):
    def get_queryset(self):
        return super(FixedMonthSecondWeekReportingManager, self) \
            .get_queryset().filter(
                period_type=FixedMonthSecondWeekReportingPeriod.FWP)


class FixedMonthSecondWeekReportingPeriod(MonthPeriod):

    FWP = 'fixed_month_second_week_reporting_period'

    class Meta:
        proxy = True
        app_label = 'snisi_core'
        verbose_name = _("Monthly Reporting Period")
        verbose_name_plural = _("Monthly Reporting Periods")

    objects = FixedMonthSecondWeekReportingManager()

    @classmethod
    def type(cls):
        return cls.FWP

    @property
    def pid(self):
        return self.middle().strftime('FM2WRP%m%Y')

    def name(self):
        # Translators: Django's date tmpl format for MonthPeriod.name()
        return ugettext("W2/RP {}").format(date_format(
            self.middle(), ugettext("F Y")))

    def full_name(self):
        # Translators: Django's date tmpl format for MonthPeriod.full_name()
        return ugettext("W2/RP {}").format(date_format(
            self.middle(), ugettext("F Y")))

    @classmethod
    def delta(self):
        return 31

    @classmethod
    def boundaries(cls, date_obj):
        fw = FixedMonthSecondWeek.find_create_by_date(
            date_obj, dont_create=True)
        start = fw.end_on + ONE_MINUTE_DELTA
        end = start + datetime.timedelta(days=2) - ONE_MICROSECOND_DELTA
        return (start, end)

    def strid(self):
        return "[W2/RP]-{}".format(self.middle().strftime('%m-%Y'))


class FixedMonthThirdWeekReportingManager(models.Manager):
    def get_queryset(self):
        return super(FixedMonthThirdWeekReportingManager, self) \
            .get_queryset().filter(
                period_type=FixedMonthThirdWeekReportingPeriod.FWP)


class FixedMonthThirdWeekReportingPeriod(MonthPeriod):

    FWP = 'fixed_month_third_week_reporting_period'

    class Meta:
        proxy = True
        app_label = 'snisi_core'
        verbose_name = _("Monthly Reporting Period")
        verbose_name_plural = _("Monthly Reporting Periods")

    objects = FixedMonthThirdWeekReportingManager()

    @classmethod
    def type(cls):
        return cls.FWP

    @property
    def pid(self):
        return self.middle().strftime('FM3WRP%m%Y')

    def name(self):
        # Translators: Django's date tmpl format for MonthPeriod.name()
        return ugettext("W3/RP {}").format(date_format(
            self.middle(), ugettext("F Y")))

    def full_name(self):
        # Translators: Django's date tmpl format for MonthPeriod.full_name()
        return ugettext("W3/RP {}").format(date_format(
            self.middle(), ugettext("F Y")))

    @classmethod
    def delta(self):
        return 31

    @classmethod
    def boundaries(cls, date_obj):
        fw = FixedMonthThirdWeek.find_create_by_date(
            date_obj, dont_create=True)
        start = fw.end_on + ONE_MINUTE_DELTA
        end = start + datetime.timedelta(days=2) - ONE_MICROSECOND_DELTA
        return (start, end)

    def strid(self):
        return "[W3/RP]-{}".format(self.middle().strftime('%m-%Y'))


class FixedMonthFourthWeekReportingManager(models.Manager):
    def get_queryset(self):
        return super(FixedMonthFourthWeekReportingManager, self) \
            .get_queryset().filter(
                period_type=FixedMonthFourthWeekReportingPeriod.FWP)


class FixedMonthFourthWeekReportingPeriod(MonthPeriod):

    FWP = 'fixed_month_fourth_week_reporting_period'

    class Meta:
        proxy = True
        app_label = 'snisi_core'
        verbose_name = _("Monthly Reporting Period")
        verbose_name_plural = _("Monthly Reporting Periods")

    objects = FixedMonthFourthWeekReportingManager()

    @classmethod
    def type(cls):
        return cls.FWP

    @property
    def pid(self):
        return self.middle().strftime('FM4WRP%m%Y')

    def name(self):
        # Translators: Django's date tmpl format for MonthPeriod.name()
        return ugettext("W4/RP {}").format(date_format(
            self.middle(), ugettext("F Y")))

    def full_name(self):
        # Translators: Django's date tmpl format for MonthPeriod.full_name()
        return ugettext("W4/RP {}").format(date_format(
            self.middle(), ugettext("F Y")))

    @classmethod
    def delta(self):
        return 31

    @classmethod
    def boundaries(cls, date_obj):
        fw = FixedMonthFourthWeek.find_create_by_date(
            date_obj, dont_create=True)
        start = fw.end_on + ONE_MINUTE_DELTA
        end = start + datetime.timedelta(days=2) - ONE_MICROSECOND_DELTA
        return (start, end)

    def strid(self):
        return "[W4/RP]-{}".format(self.middle().strftime('%m-%Y'))


class FixedMonthFifthWeekReportingManager(models.Manager):
    def get_queryset(self):
        return super(FixedMonthFifthWeekReportingManager, self) \
            .get_queryset().filter(
                period_type=FixedMonthFifthWeekReportingPeriod.FWP)


class FixedMonthFifthWeekReportingPeriod(MonthPeriod):

    FWP = 'fixed_month_fifth_week_reporting_period'

    class Meta:
        proxy = True
        app_label = 'snisi_core'
        verbose_name = _("Monthly Reporting Period")
        verbose_name_plural = _("Monthly Reporting Periods")

    objects = FixedMonthFifthWeekReportingManager()

    @classmethod
    def type(cls):
        return cls.FWP

    @property
    def pid(self):
        return self.middle().strftime('FM5WRP%m%Y')

    def name(self):
        # Translators: Django's date tmpl format for MonthPeriod.name()
        return ugettext("W5/RP {}").format(date_format(
            self.middle(), ugettext("F Y")))

    def full_name(self):
        # Translators: Django's date tmpl format for MonthPeriod.full_name()
        return ugettext("W5/RP {}").format(date_format(
            self.middle(), ugettext("F Y")))

    @classmethod
    def delta(self):
        return 31

    @classmethod
    def boundaries(cls, date_obj):
        fw = FixedMonthFifthWeek.find_create_by_date(
            date_obj, dont_create=True)
        start = fw.end_on + ONE_MINUTE_DELTA
        end = start + datetime.timedelta(days=2) - ONE_MICROSECOND_DELTA
        return (start, end)

    def strid(self):
        return "[W5/RP]-{}".format(self.middle().strftime('%m-%Y'))


class FixedMonthFirstWeekExtendedReportingManager(models.Manager):
    def get_queryset(self):
        return super(FixedMonthFirstWeekExtendedReportingManager, self) \
            .get_queryset().filter(
                period_type=FixedMonthFirstWeekExtendedReportingPeriod.FWP)


class FixedMonthFirstWeekExtendedReportingPeriod(MonthPeriod):

    FWP = 'fixed_month_first_week_extended_reporting_period'

    class Meta:
        proxy = True
        app_label = 'snisi_core'
        verbose_name = _("Monthly Extended Reporting Period")
        verbose_name_plural = _("Monthly ExtendedReporting Periods")

    objects = FixedMonthFirstWeekExtendedReportingManager()

    @classmethod
    def type(cls):
        return cls.FWP

    @property
    def pid(self):
        return self.middle().strftime('FM1WERP%m%Y')

    def name(self):
        # Translators: Django's date tmpl format for MonthPeriod.name()
        return ugettext("W1/ERP {}").format(date_format(
            self.middle(), ugettext("F Y")))

    def full_name(self):
        # Translators: Django's date tmpl format for MonthPeriod.full_name()
        return ugettext("W1/ERP {}").format(date_format(
            self.middle(), ugettext("F Y")))

    @classmethod
    def delta(self):
        return 31

    @classmethod
    def boundaries(cls, date_obj):
        fw = FixedMonthFirstWeekReportingPeriod.find_create_by_date(
            date_obj, dont_create=True)
        start = fw.end_on + ONE_MINUTE_DELTA
        end = start + datetime.timedelta(days=3) - ONE_MICROSECOND_DELTA
        return (start, end)

    def strid(self):
        return "[W1/ERP]-{}".format(self.middle().strftime('%m-%Y'))


class FixedMonthSecondWeekExtendedReportingManager(models.Manager):
    def get_queryset(self):
        return super(FixedMonthSecondWeekExtendedReportingManager, self) \
            .get_queryset().filter(
                period_type=FixedMonthSecondWeekExtendedReportingPeriod.FWP)


class FixedMonthSecondWeekExtendedReportingPeriod(MonthPeriod):

    FWP = 'fixed_month_second_week_extended_reporting_period'

    class Meta:
        proxy = True
        app_label = 'snisi_core'
        verbose_name = _("Monthly Extended Reporting Period")
        verbose_name_plural = _("Monthly ExtendedReporting Periods")

    objects = FixedMonthSecondWeekExtendedReportingManager()

    @classmethod
    def type(cls):
        return cls.FWP

    @property
    def pid(self):
        return self.middle().strftime('FM2WERP%m%Y')

    def name(self):
        # Translators: Django's date tmpl format for MonthPeriod.name()
        return ugettext("W2/ERP {}").format(date_format(
            self.middle(), ugettext("F Y")))

    def full_name(self):
        # Translators: Django's date tmpl format for MonthPeriod.full_name()
        return ugettext("W2/ERP {}").format(date_format(
            self.middle(), ugettext("F Y")))

    @classmethod
    def delta(self):
        return 31

    @classmethod
    def boundaries(cls, date_obj):
        fw = FixedMonthSecondWeekReportingPeriod.find_create_by_date(
            date_obj, dont_create=True)
        start = fw.end_on + ONE_MINUTE_DELTA
        end = start + datetime.timedelta(days=3) - ONE_MICROSECOND_DELTA
        return (start, end)

    def strid(self):
        return "[W2/ERP]-{}".format(self.middle().strftime('%m-%Y'))


class FixedMonthThirdWeekExtendedReportingManager(models.Manager):
    def get_queryset(self):
        return super(FixedMonthThirdWeekExtendedReportingManager, self) \
            .get_queryset().filter(
                period_type=FixedMonthThirdWeekExtendedReportingPeriod.FWP)


class FixedMonthThirdWeekExtendedReportingPeriod(MonthPeriod):

    FWP = 'fixed_month_third_week_extended_reporting_period'

    class Meta:
        proxy = True
        app_label = 'snisi_core'
        verbose_name = _("Monthly Extended Reporting Period")
        verbose_name_plural = _("Monthly ExtendedReporting Periods")

    objects = FixedMonthThirdWeekExtendedReportingManager()

    @classmethod
    def type(cls):
        return cls.FWP

    @property
    def pid(self):
        return self.middle().strftime('FM3WERP%m%Y')

    def name(self):
        # Translators: Django's date tmpl format for MonthPeriod.name()
        return ugettext("W3/ERP {}").format(date_format(
            self.middle(), ugettext("F Y")))

    def full_name(self):
        # Translators: Django's date tmpl format for MonthPeriod.full_name()
        return ugettext("W3/ERP {}").format(date_format(
            self.middle(), ugettext("F Y")))

    @classmethod
    def delta(self):
        return 31

    @classmethod
    def boundaries(cls, date_obj):
        fw = FixedMonthThirdWeekReportingPeriod.find_create_by_date(
            date_obj, dont_create=True)
        start = fw.end_on + ONE_MINUTE_DELTA
        end = start + datetime.timedelta(days=3) - ONE_MICROSECOND_DELTA
        return (start, end)

    def strid(self):
        return "[W3/ERP]-{}".format(self.middle().strftime('%m-%Y'))


class FixedMonthFourthWeekExtendedReportingManager(models.Manager):
    def get_queryset(self):
        return super(FixedMonthFourthWeekExtendedReportingManager, self) \
            .get_queryset().filter(
                period_type=FixedMonthFourthWeekExtendedReportingPeriod.FWP)


class FixedMonthFourthWeekExtendedReportingPeriod(MonthPeriod):

    FWP = 'fixed_month_fourth_week_extended_reporting_period'

    class Meta:
        proxy = True
        app_label = 'snisi_core'
        verbose_name = _("Monthly Extended Reporting Period")
        verbose_name_plural = _("Monthly ExtendedReporting Periods")

    objects = FixedMonthFourthWeekExtendedReportingManager()

    @classmethod
    def type(cls):
        return cls.FWP

    @property
    def pid(self):
        return self.middle().strftime('FM4WERP%m%Y')

    def name(self):
        # Translators: Django's date tmpl format for MonthPeriod.name()
        return ugettext("W4/ERP {}").format(date_format(
            self.middle(), ugettext("F Y")))

    def full_name(self):
        # Translators: Django's date tmpl format for MonthPeriod.full_name()
        return ugettext("W4/ERP {}").format(date_format(
            self.middle(), ugettext("F Y")))

    @classmethod
    def delta(self):
        return 31

    @classmethod
    def boundaries(cls, date_obj):
        fw = FixedMonthFourthWeekReportingPeriod.find_create_by_date(
            date_obj, dont_create=True)
        start = fw.end_on + ONE_MINUTE_DELTA
        end = start + datetime.timedelta(days=3) - ONE_MICROSECOND_DELTA
        return (start, end)

    def strid(self):
        return "[W4/ERP]-{}".format(self.middle().strftime('%m-%Y'))


class FixedMonthFifthWeekExtendedReportingManager(models.Manager):
    def get_queryset(self):
        return super(FixedMonthFifthWeekExtendedReportingManager, self) \
            .get_queryset().filter(
                period_type=FixedMonthFifthWeekExtendedReportingPeriod.FWP)


class FixedMonthFifthWeekExtendedReportingPeriod(MonthPeriod):

    FWP = 'fixed_month_fifth_week_extended_reporting_period'

    class Meta:
        proxy = True
        app_label = 'snisi_core'
        verbose_name = _("Monthly Extended Reporting Period")
        verbose_name_plural = _("Monthly ExtendedReporting Periods")

    objects = FixedMonthFifthWeekExtendedReportingManager()

    @classmethod
    def type(cls):
        return cls.FWP

    @property
    def pid(self):
        return self.middle().strftime('FM5WERP%m%Y')

    def name(self):
        # Translators: Django's date tmpl format for MonthPeriod.name()
        return ugettext("W5/ERP {}").format(date_format(
            self.middle(), ugettext("F Y")))

    def full_name(self):
        # Translators: Django's date tmpl format for MonthPeriod.full_name()
        return ugettext("W5/ERP {}").format(date_format(
            self.middle(), ugettext("F Y")))

    @classmethod
    def delta(self):
        return 31

    @classmethod
    def boundaries(cls, date_obj):
        fw = FixedMonthFifthWeekReportingPeriod.find_create_by_date(
            date_obj, dont_create=True)
        start = fw.end_on + ONE_MINUTE_DELTA
        end = start + datetime.timedelta(days=3) - ONE_MICROSECOND_DELTA
        return (start, end)

    def strid(self):
        return "[W5/ERP]-{}".format(self.middle().strftime('%m-%Y'))
