#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging

from py3compat import text_type
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from snisi_core.xls_import import (ExcelForm, ExcelFormField)
from snisi_tools import type_converters
from snisi_reprohealth import get_domain
from snisi_reprohealth.integrity import (PFActivitiesRIntegrityChecker,
                                         create_pf_report)
from snisi_reprohealth.models import PFActivitiesR

logger = logging.getLogger(__name__)


class PfactivitiesExcelForm(PFActivitiesRIntegrityChecker, ExcelForm):

    domain = get_domain()

    SERVICES = "Services"
    FINANCIAL = "Financier"
    STOCKS = "Stocks"

    MONTH_MAP = range(1, 13)
    YEAR_MAP = range(2014, 2021)

    _mapping = {'0.3': {
        'hc': ExcelFormField(
            'C2', text_type, _("Health Center"), sheet=SERVICES),
        'month': ExcelFormField(
            'C3', type_converters.NormalizedIntChoiceList,
            _("Month"), sheet=SERVICES, cast_args=MONTH_MAP),
        'year': ExcelFormField(
            'E3', type_converters.NormalizedIntChoiceList,
            _("Year"), sheet=SERVICES, cast_args=YEAR_MAP),
        'tubal_ligations': ExcelFormField(
            'C6', int,
            PFActivitiesR._meta.get_field(
                'tubal_ligations').verbose_name, sheet=SERVICES),
        'intrauterine_devices': ExcelFormField(
            'C7', int,
            PFActivitiesR._meta.get_field(
                'intrauterine_devices').verbose_name, sheet=SERVICES),
        'injections': ExcelFormField(
            'C8', int,
            PFActivitiesR._meta.get_field(
                'injections').verbose_name, sheet=SERVICES),
        'pills': ExcelFormField(
            'C9', int,
            PFActivitiesR._meta.get_field(
                'pills').verbose_name, sheet=SERVICES),
        'male_condoms': ExcelFormField(
            'C10', int,
            PFActivitiesR._meta.get_field(
                'male_condoms').verbose_name, sheet=SERVICES),
        'female_condoms': ExcelFormField(
            'C11', int,
            PFActivitiesR._meta.get_field(
                'female_condoms').verbose_name, sheet=SERVICES),
        'emergency_controls': ExcelFormField(
            'C12', int,
            PFActivitiesR._meta.get_field(
                'emergency_controls').verbose_name, sheet=SERVICES),
        'implants': ExcelFormField(
            'C13', int,
            PFActivitiesR._meta.get_field(
                'implants').verbose_name, sheet=SERVICES),
        'new_clients': ExcelFormField(
            'D16', int,
            PFActivitiesR._meta.get_field(
                'new_clients').verbose_name, sheet=SERVICES),
        'previous_clients': ExcelFormField(
            'D17', int,
            PFActivitiesR._meta.get_field(
                'previous_clients').verbose_name, sheet=SERVICES),
        'under25_visits': ExcelFormField(
            'D18', int,
            PFActivitiesR._meta.get_field(
                'under25_visits').verbose_name, sheet=SERVICES),
        'over25_visits': ExcelFormField(
            'D19', int,
            PFActivitiesR._meta.get_field(
                'over25_visits').verbose_name, sheet=SERVICES),
        'very_first_visits': ExcelFormField(
            'D20', int,
            PFActivitiesR._meta.get_field(
                'very_first_visits').verbose_name, sheet=SERVICES),
        'short_term_method_visits': ExcelFormField(
            'D21', int,
            PFActivitiesR._meta.get_field(
                'short_term_method_visits').verbose_name, sheet=SERVICES),
        'long_term_method_visits': ExcelFormField(
            'D22', int,
            PFActivitiesR._meta.get_field(
                'long_term_method_visits').verbose_name, sheet=SERVICES),
        'hiv_counseling_clients': ExcelFormField(
            'D23', int,
            PFActivitiesR._meta.get_field(
                'hiv_counseling_clients').verbose_name, sheet=SERVICES),
        'hiv_tests': ExcelFormField(
            'D24', int,
            PFActivitiesR._meta.get_field(
                'hiv_tests').verbose_name, sheet=SERVICES),
        'hiv_positive_results': ExcelFormField(
            'D25', int,
            PFActivitiesR._meta.get_field(
                'hiv_positive_results').verbose_name, sheet=SERVICES),
        'implant_removal': ExcelFormField(
            'D27', int,
            PFActivitiesR._meta.get_field(
                'implant_removal').verbose_name, sheet=SERVICES),
        'iud_removal': ExcelFormField(
            'D28', int,
            PFActivitiesR._meta.get_field(
                'iud_removal').verbose_name, sheet=SERVICES),
        'intrauterine_devices_qty': ExcelFormField(
            'B3', int,
            PFActivitiesR._meta.get_field(
                'intrauterine_devices_qty').verbose_name, sheet=FINANCIAL),
        'intrauterine_devices_price': ExcelFormField(
            'C3', int,
            PFActivitiesR._meta.get_field(
                'intrauterine_devices_price').verbose_name, sheet=FINANCIAL),
        'intrauterine_devices_revenue': ExcelFormField(
            'E3', int,
            PFActivitiesR._meta.get_field(
                'intrauterine_devices_revenue').verbose_name, sheet=FINANCIAL),
        'implants_qty': ExcelFormField(
            'B4', int,
            PFActivitiesR._meta.get_field(
                'implants_qty').verbose_name, sheet=FINANCIAL),
        'implants_price': ExcelFormField(
            'C4', int,
            PFActivitiesR._meta.get_field(
                'implants_price').verbose_name, sheet=FINANCIAL),
        'implants_revenue': ExcelFormField(
            'E4', int,
            PFActivitiesR._meta.get_field(
                'implants_revenue').verbose_name, sheet=FINANCIAL),
        'injections_qty': ExcelFormField(
            'B5', int,
            PFActivitiesR._meta.get_field(
                'injections_qty').verbose_name, sheet=FINANCIAL),
        'injections_price': ExcelFormField(
            'C5', int,
            PFActivitiesR._meta.get_field(
                'injections_price').verbose_name, sheet=FINANCIAL),
        'injections_revenue': ExcelFormField(
            'E5', int,
            PFActivitiesR._meta.get_field(
                'injections_revenue').verbose_name, sheet=FINANCIAL),
        'pills_qty': ExcelFormField(
            'B6', int,
            PFActivitiesR._meta.get_field(
                'pills_qty').verbose_name, sheet=FINANCIAL),
        'pills_price': ExcelFormField(
            'C6', int,
            PFActivitiesR._meta.get_field(
                'pills_price').verbose_name, sheet=FINANCIAL),
        'pills_revenue': ExcelFormField(
            'E6', int,
            PFActivitiesR._meta.get_field(
                'pills_revenue').verbose_name, sheet=FINANCIAL),
        'male_condoms_qty': ExcelFormField(
            'B7', int,
            PFActivitiesR._meta.get_field(
                'male_condoms_qty').verbose_name, sheet=FINANCIAL),
        'male_condoms_price': ExcelFormField(
            'C7', int,
            PFActivitiesR._meta.get_field(
                'male_condoms_price').verbose_name, sheet=FINANCIAL),
        'male_condoms_revenue': ExcelFormField(
            'E7', int,
            PFActivitiesR._meta.get_field(
                'male_condoms_revenue').verbose_name, sheet=FINANCIAL),
        'female_condoms_qty': ExcelFormField(
            'B8', int,
            PFActivitiesR._meta.get_field(
                'female_condoms_qty').verbose_name, sheet=FINANCIAL),
        'female_condoms_price': ExcelFormField(
            'C8', int,
            PFActivitiesR._meta.get_field(
                'female_condoms_price').verbose_name, sheet=FINANCIAL),
        'female_condoms_revenue': ExcelFormField(
            'E8', int,
            PFActivitiesR._meta.get_field(
                'female_condoms_revenue').verbose_name, sheet=FINANCIAL),
        'hiv_tests_qty': ExcelFormField(
            'B9', int,
            PFActivitiesR._meta.get_field(
                'hiv_tests_qty').verbose_name, sheet=FINANCIAL),
        'hiv_tests_price': ExcelFormField(
            'C9', int,
            PFActivitiesR._meta.get_field(
                'hiv_tests_price').verbose_name, sheet=FINANCIAL),
        'hiv_tests_revenue': ExcelFormField(
            'E9', int,
            PFActivitiesR._meta.get_field(
                'hiv_tests_revenue').verbose_name, sheet=FINANCIAL),
        'iud_removal_qty': ExcelFormField(
            'B10', int,
            PFActivitiesR._meta.get_field(
                'iud_removal_qty').verbose_name, sheet=FINANCIAL),
        'iud_removal_price': ExcelFormField(
            'C10', int,
            PFActivitiesR._meta.get_field(
                'iud_removal_price').verbose_name, sheet=FINANCIAL),
        'iud_removal_revenue': ExcelFormField(
            'E10', int,
            PFActivitiesR._meta.get_field(
                'iud_removal_revenue').verbose_name, sheet=FINANCIAL),
        'implant_removal_qty': ExcelFormField(
            'B11', int,
            PFActivitiesR._meta.get_field(
                'implant_removal_qty').verbose_name, sheet=FINANCIAL),
        'implant_removal_price': ExcelFormField(
            'C11', int,
            PFActivitiesR._meta.get_field(
                'implant_removal_price').verbose_name, sheet=FINANCIAL),
        'implant_removal_revenue': ExcelFormField(
            'E11', int,
            PFActivitiesR._meta.get_field(
                'implant_removal_revenue').verbose_name, sheet=FINANCIAL),
        'intrauterine_devices_initial': ExcelFormField(
            'B3', int,
            PFActivitiesR._meta.get_field(
                'intrauterine_devices_initial').verbose_name, sheet=STOCKS),
        'intrauterine_devices_used': ExcelFormField(
            'D3', int,
            PFActivitiesR._meta.get_field(
                'intrauterine_devices_used').verbose_name, sheet=STOCKS),
        'intrauterine_devices_lost': ExcelFormField(
            'E3', int,
            PFActivitiesR._meta.get_field(
                'intrauterine_devices_lost').verbose_name, sheet=STOCKS),
        'intrauterine_devices_received': ExcelFormField(
            'C3', int,
            PFActivitiesR._meta.get_field(
                'intrauterine_devices_received').verbose_name, sheet=STOCKS),
        'implants_initial': ExcelFormField(
            'B4', int,
            PFActivitiesR._meta.get_field(
                'implants_initial').verbose_name, sheet=STOCKS),
        'implants_used': ExcelFormField(
            'D4', int,
            PFActivitiesR._meta.get_field(
                'implants_used').verbose_name, sheet=STOCKS),
        'implants_lost': ExcelFormField(
            'E4', int,
            PFActivitiesR._meta.get_field(
                'implants_lost').verbose_name, sheet=STOCKS),
        'implants_received': ExcelFormField(
            'C4', int,
            PFActivitiesR._meta.get_field(
                'implants_received').verbose_name, sheet=STOCKS),
        'injections_initial': ExcelFormField(
            'B5', int,
            PFActivitiesR._meta.get_field(
                'injections_initial').verbose_name, sheet=STOCKS),
        'injections_used': ExcelFormField(
            'D5', int,
            PFActivitiesR._meta.get_field(
                'injections_used').verbose_name, sheet=STOCKS),
        'injections_lost': ExcelFormField(
            'E5', int,
            PFActivitiesR._meta.get_field(
                'injections_lost').verbose_name, sheet=STOCKS),
        'injections_received': ExcelFormField(
            'C5', int,
            PFActivitiesR._meta.get_field(
                'injections_received').verbose_name, sheet=STOCKS),
        'pills_initial': ExcelFormField(
            'B6', int,
            PFActivitiesR._meta.get_field(
                'pills_initial').verbose_name, sheet=STOCKS),
        'pills_used': ExcelFormField(
            'D6', int,
            PFActivitiesR._meta.get_field(
                'pills_used').verbose_name, sheet=STOCKS),
        'pills_lost': ExcelFormField(
            'E6', int,
            PFActivitiesR._meta.get_field(
                'pills_lost').verbose_name, sheet=STOCKS),
        'pills_received': ExcelFormField(
            'C6', int,
            PFActivitiesR._meta.get_field(
                'pills_received').verbose_name, sheet=STOCKS),
        'male_condoms_initial': ExcelFormField(
            'B7', int,
            PFActivitiesR._meta.get_field(
                'male_condoms_initial').verbose_name, sheet=STOCKS),
        'male_condoms_used': ExcelFormField(
            'D7', int,
            PFActivitiesR._meta.get_field(
                'male_condoms_used').verbose_name, sheet=STOCKS),
        'male_condoms_lost': ExcelFormField(
            'E7', int,
            PFActivitiesR._meta.get_field(
                'male_condoms_lost').verbose_name, sheet=STOCKS),
        'male_condoms_received': ExcelFormField(
            'C7', int,
            PFActivitiesR._meta.get_field(
                'male_condoms_received').verbose_name, sheet=STOCKS),
        'female_condoms_initial': ExcelFormField(
            'B8', int,
            PFActivitiesR._meta.get_field(
                'female_condoms_initial').verbose_name, sheet=STOCKS),
        'female_condoms_used': ExcelFormField(
            'D8', int,
            PFActivitiesR._meta.get_field(
                'female_condoms_used').verbose_name, sheet=STOCKS),
        'female_condoms_lost': ExcelFormField(
            'E8', int,
            PFActivitiesR._meta.get_field(
                'female_condoms_lost').verbose_name, sheet=STOCKS),
        'female_condoms_received': ExcelFormField(
            'C8', int,
            PFActivitiesR._meta.get_field(
                'female_condoms_received').verbose_name, sheet=STOCKS),
        'hiv_tests_initial': ExcelFormField(
            'B9', int,
            PFActivitiesR._meta.get_field(
                'hiv_tests_initial').verbose_name, sheet=STOCKS),
        'hiv_tests_used': ExcelFormField(
            'D9', int,
            PFActivitiesR._meta.get_field(
                'hiv_tests_used').verbose_name, sheet=STOCKS),
        'hiv_tests_lost': ExcelFormField(
            'E9', int,
            PFActivitiesR._meta.get_field(
                'hiv_tests_lost').verbose_name, sheet=STOCKS),
        'hiv_tests_received': ExcelFormField(
            'C9', int,
            PFActivitiesR._meta.get_field(
                'hiv_tests_received').verbose_name, sheet=STOCKS),
        'pregnancy_tests_initial': ExcelFormField(
            'B10', int,
            PFActivitiesR._meta.get_field(
                'pregnancy_tests_initial').verbose_name, sheet=STOCKS),
        'pregnancy_tests_used': ExcelFormField(
            'D10', int,
            PFActivitiesR._meta.get_field(
                'pregnancy_tests_used').verbose_name, sheet=STOCKS),
        'pregnancy_tests_lost': ExcelFormField(
            'E10', int,
            PFActivitiesR._meta.get_field(
                'pregnancy_tests_lost').verbose_name, sheet=STOCKS),
        'pregnancy_tests_received': ExcelFormField(
            'C10', int,
            PFActivitiesR._meta.get_field(
                'pregnancy_tests_received').verbose_name, sheet=STOCKS),
        }
    }

    def create_report(self, provider):

        expected_reporting = self.get('expected_reporting')

        return create_pf_report(provider=provider,
                                expected_reporting=expected_reporting,
                                completed_on=timezone.now(),
                                integrity_checker=self,
                                data_source=self.filepath)

EXPORTED_FORMS = {
    '4reprohealth_monthly_routine': {
        'label': "Routine Mensuelle PF/MSI",
        'class': PfactivitiesExcelForm
    }
}
