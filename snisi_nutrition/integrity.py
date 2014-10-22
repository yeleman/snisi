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
from snisi_nutrition import PROJECT_BRAND
from snisi_nutrition.models.Monthly import NutritionR
from snisi_nutrition.models.URENAM import URENAMNutritionR
from snisi_nutrition.models.URENAS import URENASNutritionR
from snisi_nutrition.models.URENI import URENINutritionR
from snisi_nutrition.models.Weekly import WeeklyNutritionR
from snisi_nutrition.models.Stocks import NutritionStocksR
from snisi_core.models.Reporting import ReportClass

logger = logging.getLogger(__name__)
reportcls_weekly = ReportClass.get_or_none(slug='nutrition_weekly_routine')
reportcls_monthly = ReportClass.get_or_none(slug='nutrition_monthly_routine')
reportcls_urenam = ReportClass.get_or_none(slug='nut_urenam_monthly_routine')
reportcls_urenas = ReportClass.get_or_none(slug='nut_urenas_monthly_routine')
reportcls_ureni = ReportClass.get_or_none(slug='nut_ureni_monthly_routine')
reportcls_stocks = ReportClass.get_or_none(slug='nut_stocks_monthly_routine')
validating_role = Role.get_or_none('charge_sis')


def create_nut_report(provider, expected_reporting, completed_on,
                      integrity_checker, data_source):

    return create_monthly_routine_report(
        provider=provider,
        expected_reporting=expected_reporting,
        completed_on=completed_on,
        integrity_checker=integrity_checker,
        data_source=data_source,
        reportcls=NutritionR,
        project_brand=PROJECT_BRAND)


class NutritionRIntegrityChecker(RoutineIntegrityInterface,
                                 ReportIntegrityChecker):

    report_class = reportcls_monthly
    validating_role = validating_role

    def check_pf_data(self, **options):
        pass

    def _check_completeness(self, **options):
        for field in NutritionR.data_fields():
            if not self.has(field):
                self.add_missing(_("Missing data for {f}").format(f=field),
                                 blocking=True, field=field)

    def _check(self, **options):
        self.check_pf_data(**options)
        self.chk_period_is_not_future(**options)
        self.chk_entity_exists(**options)
        self.chk_expected_arrival(**options)
        self.chk_provider_permission(**options)


class URENAMNutritionRIntegrityChecker(RoutineIntegrityInterface,
                                       ReportIntegrityChecker):

    report_class = reportcls_urenam
    validating_role = validating_role

    # - MAM/MAS checks (pour chaque tranche d’age)
    #     calculations:
    #         non_respondant = 0
    #         if MAM:
    #             transfered = 0
    #         total_start = total_start_m + total_start_f
    #         total_in = total_in_m + total_in_f
    #         grand_total_in = total_in + transfered
    #         total_out = total_out_m + total_out_f
    #         grand_total_out = total_out + referred
    #         total_end = total_end_m + total_end_f

    #     # Admisssion (nouveau cas + readmission) = Total dam (M + F)
    #     - total_in = new + returning

    #     # Sorties
    #     total_out = healed + deceased + abandoned (+ non_respondant)

    #     # sorties no more than avail
    #     total_out <= total_start + grand_total_in

    #     # Total fin de mois
    #     total_end = total_start + grand_total_in - grand_total_out

    # - URENI checks (pour chaque tranche d’age)
    #     calculations:
    #         grand_total_in = total_in + reffered
    #         grand_total_out = total_out + transferred

    # - Intrants Checks (pour chaque produit)
    #     (debut + reçu) >= (utilisé + perdu)

    def check_urenam_data(self, **options):
        pass

    def _check_completeness(self, **options):
        for field in URENAMNutritionR.data_fields():
            if not self.has(field):
                self.add_missing(_("Missing data for {f}").format(f=field),
                                 blocking=True, field=field)

    def _check(self, **options):
        self.check_urenam_data(**options)
        self.chk_period_is_not_future(**options)
        self.chk_entity_exists(**options)
        self.chk_expected_arrival(**options)
        self.chk_provider_permission(**options)


