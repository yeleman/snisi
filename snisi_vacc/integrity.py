#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging

from django.utils.translation import ugettext as _

from snisi_core.integrity import (ReportIntegrityChecker,
                                  create_monthly_routine_report,
                                  RoutineIntegrityInterface)

from snisi_core.models.Roles import Role
from snisi_vacc import PROJECT_BRAND
from snisi_vacc.models import VaccCovR
from snisi_core.models.Reporting import ReportClass

logger = logging.getLogger(__name__)
reportcls_pev = ReportClass.get_or_none(slug='major_vaccine_monthly')
validating_role = Role.get_or_none('charge_sis')


def create_pev_report(provider, expected_reporting, completed_on,
                      integrity_checker, data_source):

    return create_monthly_routine_report(
        provider=provider,
        expected_reporting=expected_reporting,
        completed_on=completed_on,
        integrity_checker=integrity_checker,
        data_source=data_source,
        reportcls=VaccCovR,
        project_brand=PROJECT_BRAND)


class VaccCovRIntegrityChecker(RoutineIntegrityInterface,
                               ReportIntegrityChecker):

    report_class = reportcls_pev
    validating_role = validating_role

    def _check_completeness(self, **options):
        for field in VaccCovR.data_fields():
            if not self.has(field):
                self.add_missing(_("Missing data for {f}").format(f=field),
                                 blocking=True, field=field)

    def _check(self, **options):
        self.chk_period_is_not_future()
        self.chk_entity_exists()
        self.chk_expected_arrival()
        self.chk_provider_permission()
