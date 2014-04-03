#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

# from snisi_core.models.Periods import MonthPeriod
# from snisi_core.models.ReportingPeriods import (
#     DefaultMonthlyReportingPeriod,
#     DefaultMonthlyExtendedReportingPeriod)
# from snisi_core.models.Reporting import ExpectedReporting, ReportClass
# from snisi_core.models.Roles import Role
from snisi_core.models.Projects import Domain

DOMAIN_SLUG = 'malaria'


def get_domain():
    return Domain.get_or_none(DOMAIN_SLUG)


# def expected_period_for(project, entity, adate):
#     return MonthPeriod.find_create_by_date(adate)


# def reporting_period_for(project, entity, adate):
#     return DefaultMonthlyReportingPeriod.find_create_by_date(adate)


# def extended_reporting_period_for(project, entity, adate):
#     return DefaultMonthlyExtendedReportingPeriod.find_create_by_date(adate)


# def reportclass_for(project, entity, adate):
#     source_reportclass = ReportClass.objects.get(slug='malaria_monthly_routine')
#     agg_reportclass = ReportClass.objects.get(slug='malaria_monthly_routine_aggregated')
#     if entity.type.slug == 'health_center':
#         return source_reportclass
#     else:
#         return agg_reportclass


# def reporting_role_for(project, entity, adate):
#     dtc = Role.objects.get(slug='dtc')
#     charge_sis = Role.objects.get(slug='charge_sis')
#     if entity.type.slug == 'health_center':
#         return dtc
#     else:
#         return charge_sis


# def within_period_for(project, entity, adate):
#     return False


# def within_entity_for(project, entity, adate):
#     return False


# def amount_expected_for(project, entity, adate):
#     return ExpectedReporting.EXPECTED_SINGLE
