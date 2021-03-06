#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import datetime

import iso8601
from django.utils import timezone


def datetime_from_iso(aniso):
    if aniso is None:
        return None
    return iso8601.parse_date(aniso)


def datetime_to_iso(adate):
    return adate.isoformat()


def parse_date_string(adatestr, as_date=False):
    def _cast(d, as_date):
        if type(d) == datetime.datetime:
            return d.date() if as_date else d.replace(tzinfo=timezone.utc)
        if as_date:
            return d
        return datetime.datetime(
            *d.timetuple()[:3]).replace(tzinfo=timezone.utc)
    if isinstance(adatestr, (datetime.date, datetime.datetime)):
        return _cast(adatestr, as_date)
    try:
        return _cast(iso8601.parse_date(adatestr), as_date)
    except:
        return None


def normalize_date(adate, as_aware=True):
    adate_is_aware = timezone.is_aware(adate)
    if as_aware and adate_is_aware:
        return adate
    elif as_aware and not adate_is_aware:
        # make foreign object aware (assume UTC)
        return timezone.make_aware(adate, timezone.utc)
    else:
        # make foreign object naive
        return timezone.make_naive(adate, timezone.utc)


def DEBUG_change_system_date(new_date, I_KNOW=False):
    if not I_KNOW:
        return

    import sys
    import subprocess

    if new_date is None:
        if sys.platform == 'darwin':
            cmd = ("sudo ntpdate -u $(sudo systemsetup "
                   "-getnetworktimeserver|awk '{print $4}')")
        else:
            cmd = "sudo ntpdate-debian"
    else:
        cmd = "sudo date {}".format(new_date.strftime('%m%d%H%M%Y'))
    subprocess.call([cmd], shell=True)


def to_timestamp(dt):
    """
    Return a timestamp for the given datetime object.
    """
    if dt is not None:
        return (dt - datetime.datetime(1970, 1, 1)
                .replace(tzinfo=timezone.utc)).total_seconds()


def to_jstimestamp(adate):
    if adate is not None:
        return int(to_timestamp(adate)) * 1000


def get_periods_str(periods):
    if not len(periods):
        return

    start = periods[0]
    end = periods[-1]

    if start == end:
        return start.strid()

    if start.middle().year == end.middle().year:
        if start.middle().month == 1 and end.middle().month == 12:
            return "{}".format(start.middle().year)
        else:
            return "{}-{} {}".format(start.middle().month,
                                     end.middle().month,
                                     start.middle().year)

    return "{} - {}".format(start.strid(), end.strid())
