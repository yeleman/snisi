#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)


class Options(dict, object):
    """ dict-like object allowing direct member access to its keys/values_list

        Example:
        adict = Options(name='madou', prof='student')
        a.name => 'madou'
        a.prof => 'student'
        a.age => None """

    def __init__(self, **kwargs):
        dict.__init__(self, **kwargs)

    def __getattribute__(self, name):
        # short-circuit object's internal members
        if name.startswith('_') or name in ('update'):
            return super(Options, self).__getattribute__(name)
        try:
            return self[name]
        except:
            return None

    def update(self, dic):
        # duplicate dict functionality
        for k, v in dic.items():
            setattr(self, k, v)


from snisi_core.models.Roles import Role
from snisi_core.models.Entities import (EntityType, Entity,
                                        HealthEntity, AdministrativeEntity)
from snisi_core.models.Periods import (Period, DayPeriod, WeekPeriod,
                                       MonthPeriod, QuarterPeriod, YearPeriod)
from snisi_core.models.Providers import Provider
from snisi_core.models.Numbers import PhoneNumber, PhoneNumberType
from snisi_core.models.Reporting import (SNISIReport, ReportClass,
                                         ExpectedReporting, ExpectedValidation)
from snisi_core.models.ValidationPeriods import DefaultDistrictValidationPeriod
from snisi_core.models.SMSMessages import SMSMessage
from snisi_core.models.Notifications import Notification

from snisi_core.models.Projects import Domain, Cluster, Participation
from snisi_core.models.Groups import SNISIGroup

from snisi_core.models.ReportingPeriods import (DefaultMonthlyReportingPeriod,
                                                DefaultMonthlyExtendedReportingPeriod)
from snisi_core.models.ValidationPeriods import (DefaultDistrictValidationPeriod,
                                                 DefaultRegionValidationPeriod,
                                                 DefaultNationalValidationPeriod)
