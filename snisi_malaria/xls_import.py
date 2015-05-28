#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging

# import reversion
from py3compat import text_type
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from snisi_core.models.Periods import MonthPeriod
from snisi_core.xls_import import (ExcelForm, ExcelFormField)
from snisi_tools import type_converters
from snisi_tools.misc import class_str
from snisi_malaria import get_domain
from snisi_malaria.models import MalariaR, EpidemioMalariaR
from snisi_malaria.integrity import (MalariaRSourceReportChecker,
                                     EpidemioMalariaRIntegrityChecker,
                                     create_report, create_epidemio_report)

logger = logging.getLogger(__name__)

YN_MAP = {'oui': MalariaR.YES, 'non': MalariaR.NO}
MONTH_MAP = range(1, 13)
YEAR_MAP = range(2010, 2021)
DAY_MAP = range(1, 32)

base_map = {'0.4': {
    'region': ExcelFormField('B2', text_type, _("Region")),
    'district': ExcelFormField('B3', text_type, _("Health District")),
    'hc': ExcelFormField('B4', text_type, _("Health Center")),
    'month': ExcelFormField('D3', type_converters.NormalizedIntChoiceList,
                            _("Month"), cast_args=MONTH_MAP),
    'year': ExcelFormField('G3', type_converters.NormalizedIntChoiceList,
                           _("Year"), cast_args=YEAR_MAP),

    'u5_total_consultation_all_causes':
    ExcelFormField(
        'C7', int,
        MalariaR._meta.get_field(
            'u5_total_consultation_all_causes').verbose_name),
    'o5_total_consultation_all_causes':
    ExcelFormField(
        'E7', int,
        MalariaR._meta.get_field(
            'o5_total_consultation_all_causes').verbose_name),
    'pw_total_consultation_all_causes':
    ExcelFormField(
        'G7', int,
        MalariaR._meta.get_field(
            'pw_total_consultation_all_causes').verbose_name),
    'u5_total_suspected_malaria_cases':
    ExcelFormField(
        'C8', int,
        MalariaR._meta.get_field(
            'u5_total_suspected_malaria_cases').verbose_name),
    'o5_total_suspected_malaria_cases':
    ExcelFormField(
        'E8', int,
        MalariaR._meta.get_field(
            'o5_total_suspected_malaria_cases').verbose_name),
    'pw_total_suspected_malaria_cases':
    ExcelFormField(
        'G8', int,
        MalariaR._meta.get_field(
            'pw_total_suspected_malaria_cases').verbose_name),
    'u5_total_tested_malaria_cases':
    ExcelFormField(
        'C9', int,
        MalariaR._meta.get_field(
            'u5_total_tested_malaria_cases').verbose_name),
    'o5_total_tested_malaria_cases':
    ExcelFormField(
        'E9', int,
        MalariaR._meta.get_field(
            'o5_total_tested_malaria_cases').verbose_name),
    'pw_total_tested_malaria_cases':
    ExcelFormField(
        'G9', int,
        MalariaR._meta.get_field(
            'pw_total_tested_malaria_cases').verbose_name),
    'u5_total_confirmed_malaria_cases':
    ExcelFormField(
        'C10', int,
        MalariaR._meta.get_field(
            'u5_total_confirmed_malaria_cases').verbose_name),
    'o5_total_confirmed_malaria_cases':
    ExcelFormField(
        'E10', int,
        MalariaR._meta.get_field(
            'o5_total_confirmed_malaria_cases').verbose_name),
    'pw_total_confirmed_malaria_cases':
    ExcelFormField(
        'G10', int,
        MalariaR._meta.get_field(
            'pw_total_confirmed_malaria_cases').verbose_name),
    'u5_total_simple_malaria_cases':
    ExcelFormField(
        'C11', int,
        MalariaR._meta.get_field(
            'u5_total_simple_malaria_cases').verbose_name),
    'o5_total_simple_malaria_cases':
    ExcelFormField(
        'E11', int,
        MalariaR._meta.get_field(
            'o5_total_simple_malaria_cases').verbose_name),
    'u5_total_severe_malaria_cases':
    ExcelFormField(
        'C12', int,
        MalariaR._meta.get_field(
            'u5_total_severe_malaria_cases').verbose_name),
    'o5_total_severe_malaria_cases':
    ExcelFormField(
        'E12', int,
        MalariaR._meta.get_field(
            'o5_total_severe_malaria_cases').verbose_name),
    'pw_total_severe_malaria_cases':
    ExcelFormField(
        'G12', int,
        MalariaR._meta.get_field(
            'pw_total_severe_malaria_cases').verbose_name),
    'u5_total_treated_malaria_cases':
    ExcelFormField(
        'C13', int,
        MalariaR._meta.get_field(
            'u5_total_treated_malaria_cases').verbose_name),
    'o5_total_treated_malaria_cases':
    ExcelFormField(
        'E13', int,
        MalariaR._meta.get_field(
            'o5_total_treated_malaria_cases').verbose_name),
    'pw_total_treated_malaria_cases':
    ExcelFormField(
        'G13', int,
        MalariaR._meta.get_field(
            'pw_total_treated_malaria_cases').verbose_name),
    'u5_total_inpatient_all_causes':
    ExcelFormField(
        'C17', int,
        MalariaR._meta.get_field(
            'u5_total_inpatient_all_causes').verbose_name),
    'o5_total_inpatient_all_causes':
    ExcelFormField(
        'E17', int,
        MalariaR._meta.get_field(
            'o5_total_inpatient_all_causes').verbose_name),
    'pw_total_inpatient_all_causes':
    ExcelFormField(
        'G17', int,
        MalariaR._meta.get_field(
            'pw_total_inpatient_all_causes').verbose_name),
    'u5_total_malaria_inpatient':
    ExcelFormField(
        'C18', int,
        MalariaR._meta.get_field(
            'u5_total_malaria_inpatient').verbose_name),
    'o5_total_malaria_inpatient':
    ExcelFormField(
        'E18', int,
        MalariaR._meta.get_field(
            'o5_total_malaria_inpatient').verbose_name),
    'pw_total_malaria_inpatient':
    ExcelFormField(
        'G18', int,
        MalariaR._meta.get_field(
            'pw_total_malaria_inpatient').verbose_name),
    'u5_total_death_all_causes':
    ExcelFormField(
        'C22', int,
        MalariaR._meta.get_field(
            'u5_total_death_all_causes').verbose_name),
    'o5_total_death_all_causes':
    ExcelFormField(
        'E22', int,
        MalariaR._meta.get_field(
            'o5_total_death_all_causes').verbose_name),
    'pw_total_death_all_causes':
    ExcelFormField(
        'G22', int,
        MalariaR._meta.get_field(
            'pw_total_death_all_causes').verbose_name),
    'u5_total_malaria_death':
    ExcelFormField(
        'C23', int,
        MalariaR._meta.get_field(
            'u5_total_malaria_death').verbose_name),
    'o5_total_malaria_death':
    ExcelFormField(
        'E23', int,
        MalariaR._meta.get_field(
            'o5_total_malaria_death').verbose_name),
    'pw_total_malaria_death':
    ExcelFormField(
        'G23', int,
        MalariaR._meta.get_field(
            'pw_total_malaria_death').verbose_name),
    'u5_total_distributed_bednets':
    ExcelFormField(
        'C27', int,
        MalariaR._meta.get_field(
            'u5_total_distributed_bednets').verbose_name),
    'pw_total_distributed_bednets':
    ExcelFormField(
        'E27', int,
        MalariaR._meta.get_field(
            'pw_total_distributed_bednets').verbose_name),
    'pw_total_anc1': ExcelFormField(
        'M22', int,
        MalariaR._meta.get_field(
            'pw_total_anc1').verbose_name),
    'pw_total_sp1': ExcelFormField(
        'M23', int,
        MalariaR._meta.get_field(
            'pw_total_sp1').verbose_name),
    'pw_total_sp2': ExcelFormField(
        'M24', int,
        MalariaR._meta.get_field(
            'pw_total_sp2').verbose_name),
    'stockout_act_children': ExcelFormField(
        'M5', type_converters.NormalizedChoiceList,
        MalariaR._meta.get_field(
            'stockout_act_children').verbose_name,
        cast_args=YN_MAP),
    'stockout_act_youth':
    ExcelFormField(
        'M6', type_converters.NormalizedChoiceList,
        MalariaR._meta.get_field(
            'stockout_act_youth').verbose_name,
        cast_args=YN_MAP),
    'stockout_act_adult':
    ExcelFormField(
        'M7', type_converters.NormalizedChoiceList,
        MalariaR._meta.get_field(
            'stockout_act_adult').verbose_name,
        cast_args=YN_MAP),
    'stockout_artemether':
    ExcelFormField(
        'M11', type_converters.NormalizedChoiceList,
        MalariaR._meta.get_field(
            'stockout_artemether').verbose_name,
        cast_args=YN_MAP),
    'stockout_quinine':
    ExcelFormField(
        'M12', type_converters.NormalizedChoiceList,
        MalariaR._meta.get_field(
            'stockout_quinine').verbose_name,
        cast_args=YN_MAP),
    'stockout_serum':
    ExcelFormField(
        'M13', type_converters.NormalizedChoiceList,
        MalariaR._meta.get_field(
            'stockout_serum').verbose_name,
        cast_args=YN_MAP),
    'stockout_bednet':
    ExcelFormField(
        'M16', type_converters.NormalizedChoiceList,
        MalariaR._meta.get_field(
            'stockout_bednet').verbose_name,
        cast_args=YN_MAP),
    'stockout_rdt': ExcelFormField(
        'M17', type_converters.NormalizedChoiceList,
        MalariaR._meta.get_field(
            'stockout_rdt').verbose_name,
        cast_args=YN_MAP),
    'stockout_sp': ExcelFormField(
        'M18', type_converters.NormalizedChoiceList,
        MalariaR._meta.get_field(
            'stockout_sp').verbose_name,
        cast_args=YN_MAP),
    'fillin_day': ExcelFormField(
        'K28', type_converters.NormalizedIntChoiceList,
        _("Filling Day"), cast_args=DAY_MAP),
    'fillin_month': ExcelFormField(
        'L28', type_converters.NormalizedIntChoiceList,
        _("Filling Month"), cast_args=MONTH_MAP),
    'fillin_year': ExcelFormField(
        'M28', type_converters.NormalizedIntChoiceList,
        _("Filling Year"), cast_args=YEAR_MAP),
    'author': ExcelFormField(
        'L26', text_type, _("Author Name")),
    }
}

base_map['0.5'] = base_map['0.4']
base_map['0.5'].update({
    'pw_total_simple_malaria_cases':
    ExcelFormField(
        'G11', int,
        MalariaR._meta.get_field(
            'pw_total_simple_malaria_cases').verbose_name)})


class MalariaExcelForm(MalariaRSourceReportChecker, ExcelForm):

    domain = get_domain()
    period_class = MonthPeriod

    """ Mapping between MalariaReport & Excel Monthly Malaria Routine File """

    YN_MAP = YN_MAP
    MONTH_MAP = MONTH_MAP
    YEAR_MAP = YEAR_MAP
    DAY_MAP = DAY_MAP

    _mapping = base_map

    def create_report(self, provider):

        expected_reporting = self.get('expected_reporting')

        # return report, text_message (success or failure)
        return create_report(provider=provider,
                             expected_reporting=expected_reporting,
                             completed_on=timezone.now(),
                             integrity_checker=self,
                             data_source=self.filepath)


class EpidemioMalariaRForm(EpidemioMalariaRIntegrityChecker, ExcelForm):

    MONTH_MAP = range(1, 13)
    WEEK_MAP = range(1, 6)
    YEAR_MAP = range(2011, 2025)

    _mapping = {'0.1': {
        'region': ExcelFormField('B3', text_type, _("Region")),
        'district': ExcelFormField('B4', text_type, _('Health District')),
        'hc': ExcelFormField('B5', text_type, _("Health Center")),
        'month': ExcelFormField(
            'F4', type_converters.NormalizedIntChoiceList,
            _("Month"), cast_args=MONTH_MAP),
        'year': ExcelFormField(
            'I4', type_converters.NormalizedIntChoiceList,
            _("Year"), cast_args=YEAR_MAP),
        'week': ExcelFormField(
            'G6', type_converters.NormalizedIntChoiceList,
            _("Week"), cast_args=WEEK_MAP),

        'd1_u5_total_consultation_all_causes': ExcelFormField(
            'C10', int,
            EpidemioMalariaR._meta.get_field(
                'u5_total_consultation_all_causes').verbose_name),
        'd1_u5_total_suspected_malaria_cases': ExcelFormField(
            'C13', int,
            EpidemioMalariaR._meta.get_field(
                'u5_total_suspected_malaria_cases').verbose_name),
        'd1_u5_total_rdt_tested_malaria_cases': ExcelFormField(
            'C16', int,
            EpidemioMalariaR._meta.get_field(
                'u5_total_rdt_tested_malaria_cases').verbose_name),
        'd1_u5_total_rdt_confirmed_malaria_cases': ExcelFormField(
            'C19', int,
            EpidemioMalariaR._meta.get_field(
                'u5_total_rdt_confirmed_malaria_cases').verbose_name),
        'd1_u5_total_rdt_pfalciparum_malaria_cases': ExcelFormField(
            'C22', int,
            EpidemioMalariaR._meta.get_field(
                'u5_total_rdt_pfalciparum_malaria_cases').verbose_name),
        'd1_u5_total_ts_tested_malaria_cases': ExcelFormField(
            'C25', int,
            EpidemioMalariaR._meta.get_field(
                'u5_total_ts_tested_malaria_cases').verbose_name),
        'd1_u5_total_ts_confirmed_malaria_cases': ExcelFormField(
            'C28', int,
            EpidemioMalariaR._meta.get_field(
                'u5_total_ts_confirmed_malaria_cases').verbose_name),
        'd1_u5_total_ts_pfalciparum_malaria_cases': ExcelFormField(
            'C31', int,
            EpidemioMalariaR._meta.get_field(
                'u5_total_ts_pfalciparum_malaria_cases').verbose_name),
        'd1_u5_total_simple_malaria_cases': ExcelFormField(
            'C34', int,
            EpidemioMalariaR._meta.get_field(
                'u5_total_simple_malaria_cases').verbose_name),
        'd1_u5_total_severe_malaria_cases': ExcelFormField(
            'C37', int,
            EpidemioMalariaR._meta.get_field(
                'u5_total_severe_malaria_cases').verbose_name),
        'd1_u5_total_malaria_death': ExcelFormField(
            'C40', int,
            EpidemioMalariaR._meta.get_field(
                'u5_total_malaria_death').verbose_name),
        'd1_u5_total_death_all_causes': ExcelFormField(
            'C43', int,
            EpidemioMalariaR._meta.get_field(
                'u5_total_death_all_causes').verbose_name),

        'd1_o5_total_consultation_all_causes': ExcelFormField(
            'C11', int,
            EpidemioMalariaR._meta.get_field(
                'o5_total_consultation_all_causes').verbose_name),
        'd1_o5_total_suspected_malaria_cases': ExcelFormField(
            'C14', int,
            EpidemioMalariaR._meta.get_field(
                'o5_total_suspected_malaria_cases').verbose_name),
        'd1_o5_total_rdt_tested_malaria_cases': ExcelFormField(
            'C17', int,
            EpidemioMalariaR._meta.get_field(
                'o5_total_rdt_tested_malaria_cases').verbose_name),
        'd1_o5_total_rdt_confirmed_malaria_cases': ExcelFormField(
            'C20', int,
            EpidemioMalariaR._meta.get_field(
                'o5_total_rdt_confirmed_malaria_cases').verbose_name),
        'd1_o5_total_rdt_pfalciparum_malaria_cases': ExcelFormField(
            'C23', int,
            EpidemioMalariaR._meta.get_field(
                'o5_total_rdt_pfalciparum_malaria_cases').verbose_name),
        'd1_o5_total_ts_tested_malaria_cases': ExcelFormField(
            'C26', int,
            EpidemioMalariaR._meta.get_field(
                'o5_total_ts_tested_malaria_cases').verbose_name),
        'd1_o5_total_ts_confirmed_malaria_cases': ExcelFormField(
            'C29', int,
            EpidemioMalariaR._meta.get_field(
                'o5_total_ts_confirmed_malaria_cases').verbose_name),
        'd1_o5_total_ts_pfalciparum_malaria_cases': ExcelFormField(
            'C32', int,
            EpidemioMalariaR._meta.get_field(
                'o5_total_ts_pfalciparum_malaria_cases').verbose_name),
        'd1_o5_total_simple_malaria_cases': ExcelFormField(
            'C35', int,
            EpidemioMalariaR._meta.get_field(
                'o5_total_simple_malaria_cases').verbose_name),
        'd1_o5_total_severe_malaria_cases': ExcelFormField(
            'C38', int,
            EpidemioMalariaR._meta.get_field(
                'o5_total_severe_malaria_cases').verbose_name),
        'd1_o5_total_malaria_death': ExcelFormField(
            'C41', int,
            EpidemioMalariaR._meta.get_field(
                'o5_total_malaria_death').verbose_name),
        'd1_o5_total_death_all_causes': ExcelFormField(
            'C34', int,
            EpidemioMalariaR._meta.get_field(
                'o5_total_death_all_causes').verbose_name),

        'd1_pw_total_consultation_all_causes': ExcelFormField(
            'C12', int,
            EpidemioMalariaR._meta.get_field(
                'pw_total_consultation_all_causes').verbose_name),
        'd1_pw_total_suspected_malaria_cases': ExcelFormField(
            'C15', int,
            EpidemioMalariaR._meta.get_field(
                'pw_total_suspected_malaria_cases').verbose_name),
        'd1_pw_total_rdt_tested_malaria_cases': ExcelFormField(
            'C18', int,
            EpidemioMalariaR._meta.get_field(
                'pw_total_rdt_tested_malaria_cases').verbose_name),
        'd1_pw_total_rdt_confirmed_malaria_cases': ExcelFormField(
            'C21', int,
            EpidemioMalariaR._meta.get_field(
                'pw_total_rdt_confirmed_malaria_cases').verbose_name),
        'd1_pw_total_rdt_pfalciparum_malaria_cases': ExcelFormField(
            'C24', int,
            EpidemioMalariaR._meta.get_field(
                'pw_total_rdt_pfalciparum_malaria_cases').verbose_name),
        'd1_pw_total_ts_tested_malaria_cases': ExcelFormField(
            'C27', int,
            EpidemioMalariaR._meta.get_field(
                'pw_total_ts_tested_malaria_cases').verbose_name),
        'd1_pw_total_ts_confirmed_malaria_cases': ExcelFormField(
            'C30', int,
            EpidemioMalariaR._meta.get_field(
                'pw_total_ts_confirmed_malaria_cases').verbose_name),
        'd1_pw_total_ts_pfalciparum_malaria_cases': ExcelFormField(
            'C33', int,
            EpidemioMalariaR._meta.get_field(
                'pw_total_ts_pfalciparum_malaria_cases').verbose_name),
        'd1_pw_total_simple_malaria_cases': ExcelFormField(
            'C36', int,
            EpidemioMalariaR._meta.get_field(
                'pw_total_simple_malaria_cases').verbose_name),
        'd1_pw_total_severe_malaria_cases': ExcelFormField(
            'C39', int,
            EpidemioMalariaR._meta.get_field(
                'pw_total_severe_malaria_cases').verbose_name),
        'd1_pw_total_malaria_death': ExcelFormField(
            'C42', int,
            EpidemioMalariaR._meta.get_field(
                'pw_total_malaria_death').verbose_name),
        'd1_pw_total_death_all_causes': ExcelFormField(
            'C45', int,
            EpidemioMalariaR._meta.get_field(
                'pw_total_death_all_causes').verbose_name),

        'd2_u5_total_consultation_all_causes': ExcelFormField(
            'D10', int,
            EpidemioMalariaR._meta.get_field(
                'u5_total_consultation_all_causes').verbose_name),
        'd2_u5_total_suspected_malaria_cases': ExcelFormField(
            'D13', int,
            EpidemioMalariaR._meta.get_field(
                'u5_total_suspected_malaria_cases').verbose_name),
        'd2_u5_total_rdt_tested_malaria_cases': ExcelFormField(
            'D16', int,
            EpidemioMalariaR._meta.get_field(
                'u5_total_rdt_tested_malaria_cases').verbose_name),
        'd2_u5_total_rdt_confirmed_malaria_cases': ExcelFormField(
            'D19', int,
            EpidemioMalariaR._meta.get_field(
                'u5_total_rdt_confirmed_malaria_cases').verbose_name),
        'd2_u5_total_rdt_pfalciparum_malaria_cases': ExcelFormField(
            'D22', int,
            EpidemioMalariaR._meta.get_field(
                'u5_total_rdt_pfalciparum_malaria_cases').verbose_name),
        'd2_u5_total_ts_tested_malaria_cases': ExcelFormField(
            'D25', int,
            EpidemioMalariaR._meta.get_field(
                'u5_total_ts_tested_malaria_cases').verbose_name),
        'd2_u5_total_ts_confirmed_malaria_cases': ExcelFormField(
            'D28', int,
            EpidemioMalariaR._meta.get_field(
                'u5_total_ts_confirmed_malaria_cases').verbose_name),
        'd2_u5_total_ts_pfalciparum_malaria_cases': ExcelFormField(
            'D31', int,
            EpidemioMalariaR._meta.get_field(
                'u5_total_ts_pfalciparum_malaria_cases').verbose_name),
        'd2_u5_total_simple_malaria_cases': ExcelFormField(
            'D34', int,
            EpidemioMalariaR._meta.get_field(
                'u5_total_simple_malaria_cases').verbose_name),
        'd2_u5_total_severe_malaria_cases': ExcelFormField(
            'D37', int,
            EpidemioMalariaR._meta.get_field(
                'u5_total_severe_malaria_cases').verbose_name),
        'd2_u5_total_malaria_death': ExcelFormField(
            'D40', int,
            EpidemioMalariaR._meta.get_field(
                'u5_total_malaria_death').verbose_name),
        'd2_u5_total_death_all_causes': ExcelFormField(
            'D43', int,
            EpidemioMalariaR._meta.get_field(
                'u5_total_death_all_causes').verbose_name),

        'd2_o5_total_consultation_all_causes': ExcelFormField(
            'D11', int,
            EpidemioMalariaR._meta.get_field(
                'o5_total_consultation_all_causes').verbose_name),
        'd2_o5_total_suspected_malaria_cases': ExcelFormField(
            'D14', int,
            EpidemioMalariaR._meta.get_field(
                'o5_total_suspected_malaria_cases').verbose_name),
        'd2_o5_total_rdt_tested_malaria_cases': ExcelFormField(
            'D17', int,
            EpidemioMalariaR._meta.get_field(
                'o5_total_rdt_tested_malaria_cases').verbose_name),
        'd2_o5_total_rdt_confirmed_malaria_cases': ExcelFormField(
            'D20', int,
            EpidemioMalariaR._meta.get_field(
                'o5_total_rdt_confirmed_malaria_cases').verbose_name),
        'd2_o5_total_rdt_pfalciparum_malaria_cases': ExcelFormField(
            'D23', int,
            EpidemioMalariaR._meta.get_field(
                'o5_total_rdt_pfalciparum_malaria_cases').verbose_name),
        'd2_o5_total_ts_tested_malaria_cases': ExcelFormField(
            'D26', int,
            EpidemioMalariaR._meta.get_field(
                'o5_total_ts_tested_malaria_cases').verbose_name),
        'd2_o5_total_ts_confirmed_malaria_cases': ExcelFormField(
            'D29', int,
            EpidemioMalariaR._meta.get_field(
                'o5_total_ts_confirmed_malaria_cases').verbose_name),
        'd2_o5_total_ts_pfalciparum_malaria_cases': ExcelFormField(
            'D32', int,
            EpidemioMalariaR._meta.get_field(
                'o5_total_ts_pfalciparum_malaria_cases').verbose_name),
        'd2_o5_total_simple_malaria_cases': ExcelFormField(
            'D35', int,
            EpidemioMalariaR._meta.get_field(
                'o5_total_simple_malaria_cases').verbose_name),
        'd2_o5_total_severe_malaria_cases': ExcelFormField(
            'D38', int,
            EpidemioMalariaR._meta.get_field(
                'o5_total_severe_malaria_cases').verbose_name),
        'd2_o5_total_malaria_death': ExcelFormField(
            'D41', int,
            EpidemioMalariaR._meta.get_field(
                'o5_total_malaria_death').verbose_name),
        'd2_o5_total_death_all_causes': ExcelFormField(
            'D34', int,
            EpidemioMalariaR._meta.get_field(
                'o5_total_death_all_causes').verbose_name),

        'd2_pw_total_consultation_all_causes': ExcelFormField(
            'D12', int,
            EpidemioMalariaR._meta.get_field(
                'pw_total_consultation_all_causes').verbose_name),
        'd2_pw_total_suspected_malaria_cases': ExcelFormField(
            'D15', int,
            EpidemioMalariaR._meta.get_field(
                'pw_total_suspected_malaria_cases').verbose_name),
        'd2_pw_total_rdt_tested_malaria_cases': ExcelFormField(
            'D18', int,
            EpidemioMalariaR._meta.get_field(
                'pw_total_rdt_tested_malaria_cases').verbose_name),
        'd2_pw_total_rdt_confirmed_malaria_cases': ExcelFormField(
            'D21', int,
            EpidemioMalariaR._meta.get_field(
                'pw_total_rdt_confirmed_malaria_cases').verbose_name),
        'd2_pw_total_rdt_pfalciparum_malaria_cases': ExcelFormField(
            'D24', int,
            EpidemioMalariaR._meta.get_field(
                'pw_total_rdt_pfalciparum_malaria_cases').verbose_name),
        'd2_pw_total_ts_tested_malaria_cases': ExcelFormField(
            'D27', int,
            EpidemioMalariaR._meta.get_field(
                'pw_total_ts_tested_malaria_cases').verbose_name),
        'd2_pw_total_ts_confirmed_malaria_cases': ExcelFormField(
            'D30', int,
            EpidemioMalariaR._meta.get_field(
                'pw_total_ts_confirmed_malaria_cases').verbose_name),
        'd2_pw_total_ts_pfalciparum_malaria_cases': ExcelFormField(
            'D33', int,
            EpidemioMalariaR._meta.get_field(
                'pw_total_ts_pfalciparum_malaria_cases').verbose_name),
        'd2_pw_total_simple_malaria_cases': ExcelFormField(
            'D36', int,
            EpidemioMalariaR._meta.get_field(
                'pw_total_simple_malaria_cases').verbose_name),
        'd2_pw_total_severe_malaria_cases': ExcelFormField(
            'D39', int,
            EpidemioMalariaR._meta.get_field(
                'pw_total_severe_malaria_cases').verbose_name),
        'd2_pw_total_malaria_death': ExcelFormField(
            'D42', int,
            EpidemioMalariaR._meta.get_field(
                'pw_total_malaria_death').verbose_name),
        'd2_pw_total_death_all_causes': ExcelFormField(
            'D45', int,
            EpidemioMalariaR._meta.get_field(
                'pw_total_death_all_causes').verbose_name),

        'd3_u5_total_consultation_all_causes': ExcelFormField(
            'E10', int,
            EpidemioMalariaR._meta.get_field(
                'u5_total_consultation_all_causes').verbose_name),
        'd3_u5_total_suspected_malaria_cases': ExcelFormField(
            'E13', int,
            EpidemioMalariaR._meta.get_field(
                'u5_total_suspected_malaria_cases').verbose_name),
        'd3_u5_total_rdt_tested_malaria_cases': ExcelFormField(
            'E16', int,
            EpidemioMalariaR._meta.get_field(
                'u5_total_rdt_tested_malaria_cases').verbose_name),
        'd3_u5_total_rdt_confirmed_malaria_cases': ExcelFormField(
            'E19', int,
            EpidemioMalariaR._meta.get_field(
                'u5_total_rdt_confirmed_malaria_cases').verbose_name),
        'd3_u5_total_rdt_pfalciparum_malaria_cases': ExcelFormField(
            'E22', int,
            EpidemioMalariaR._meta.get_field(
                'u5_total_rdt_pfalciparum_malaria_cases').verbose_name),
        'd3_u5_total_ts_tested_malaria_cases': ExcelFormField(
            'E25', int,
            EpidemioMalariaR._meta.get_field(
                'u5_total_ts_tested_malaria_cases').verbose_name),
        'd3_u5_total_ts_confirmed_malaria_cases': ExcelFormField(
            'E28', int,
            EpidemioMalariaR._meta.get_field(
                'u5_total_ts_confirmed_malaria_cases').verbose_name),
        'd3_u5_total_ts_pfalciparum_malaria_cases': ExcelFormField(
            'E31', int,
            EpidemioMalariaR._meta.get_field(
                'u5_total_ts_pfalciparum_malaria_cases').verbose_name),
        'd3_u5_total_simple_malaria_cases': ExcelFormField(
            'E34', int,
            EpidemioMalariaR._meta.get_field(
                'u5_total_simple_malaria_cases').verbose_name),
        'd3_u5_total_severe_malaria_cases': ExcelFormField(
            'E37', int,
            EpidemioMalariaR._meta.get_field(
                'u5_total_severe_malaria_cases').verbose_name),
        'd3_u5_total_malaria_death': ExcelFormField(
            'E40', int,
            EpidemioMalariaR._meta.get_field(
                'u5_total_malaria_death').verbose_name),
        'd3_u5_total_death_all_causes': ExcelFormField(
            'E43', int,
            EpidemioMalariaR._meta.get_field(
                'u5_total_death_all_causes').verbose_name),

        'd3_o5_total_consultation_all_causes': ExcelFormField(
            'E11', int,
            EpidemioMalariaR._meta.get_field(
                'o5_total_consultation_all_causes').verbose_name),
        'd3_o5_total_suspected_malaria_cases': ExcelFormField(
            'E14', int,
            EpidemioMalariaR._meta.get_field(
                'o5_total_suspected_malaria_cases').verbose_name),
        'd3_o5_total_rdt_tested_malaria_cases': ExcelFormField(
            'E17', int,
            EpidemioMalariaR._meta.get_field(
                'o5_total_rdt_tested_malaria_cases').verbose_name),
        'd3_o5_total_rdt_confirmed_malaria_cases': ExcelFormField(
            'E20', int,
            EpidemioMalariaR._meta.get_field(
                'o5_total_rdt_confirmed_malaria_cases').verbose_name),
        'd3_o5_total_rdt_pfalciparum_malaria_cases': ExcelFormField(
            'E23', int,
            EpidemioMalariaR._meta.get_field(
                'o5_total_rdt_pfalciparum_malaria_cases').verbose_name),
        'd3_o5_total_ts_tested_malaria_cases': ExcelFormField(
            'E26', int,
            EpidemioMalariaR._meta.get_field(
                'o5_total_ts_tested_malaria_cases').verbose_name),
        'd3_o5_total_ts_confirmed_malaria_cases': ExcelFormField(
            'E29', int,
            EpidemioMalariaR._meta.get_field(
                'o5_total_ts_confirmed_malaria_cases').verbose_name),
        'd3_o5_total_ts_pfalciparum_malaria_cases': ExcelFormField(
            'E32', int,
            EpidemioMalariaR._meta.get_field(
                'o5_total_ts_pfalciparum_malaria_cases').verbose_name),
        'd3_o5_total_simple_malaria_cases': ExcelFormField(
            'E35', int,
            EpidemioMalariaR._meta.get_field(
                'o5_total_simple_malaria_cases').verbose_name),
        'd3_o5_total_severe_malaria_cases': ExcelFormField(
            'E38', int,
            EpidemioMalariaR._meta.get_field(
                'o5_total_severe_malaria_cases').verbose_name),
        'd3_o5_total_malaria_death': ExcelFormField(
            'E41', int,
            EpidemioMalariaR._meta.get_field(
                'o5_total_malaria_death').verbose_name),
        'd3_o5_total_death_all_causes': ExcelFormField(
            'E34', int,
            EpidemioMalariaR._meta.get_field(
                'o5_total_death_all_causes').verbose_name),

        'd3_pw_total_consultation_all_causes': ExcelFormField(
            'E12', int,
            EpidemioMalariaR._meta.get_field(
                'pw_total_consultation_all_causes').verbose_name),
        'd3_pw_total_suspected_malaria_cases': ExcelFormField(
            'E15', int,
            EpidemioMalariaR._meta.get_field(
                'pw_total_suspected_malaria_cases').verbose_name),
        'd3_pw_total_rdt_tested_malaria_cases': ExcelFormField(
            'E18', int,
            EpidemioMalariaR._meta.get_field(
                'pw_total_rdt_tested_malaria_cases').verbose_name),
        'd3_pw_total_rdt_confirmed_malaria_cases': ExcelFormField(
            'E21', int,
            EpidemioMalariaR._meta.get_field(
                'pw_total_rdt_confirmed_malaria_cases').verbose_name),
        'd3_pw_total_rdt_pfalciparum_malaria_cases': ExcelFormField(
            'E24', int,
            EpidemioMalariaR._meta.get_field(
                'pw_total_rdt_pfalciparum_malaria_cases').verbose_name),
        'd3_pw_total_ts_tested_malaria_cases': ExcelFormField(
            'E27', int,
            EpidemioMalariaR._meta.get_field(
                'pw_total_ts_tested_malaria_cases').verbose_name),
        'd3_pw_total_ts_confirmed_malaria_cases': ExcelFormField(
            'E30', int,
            EpidemioMalariaR._meta.get_field(
                'pw_total_ts_confirmed_malaria_cases').verbose_name),
        'd3_pw_total_ts_pfalciparum_malaria_cases': ExcelFormField(
            'E33', int,
            EpidemioMalariaR._meta.get_field(
                'pw_total_ts_pfalciparum_malaria_cases').verbose_name),
        'd3_pw_total_simple_malaria_cases': ExcelFormField(
            'E36', int,
            EpidemioMalariaR._meta.get_field(
                'pw_total_simple_malaria_cases').verbose_name),
        'd3_pw_total_severe_malaria_cases': ExcelFormField(
            'E39', int,
            EpidemioMalariaR._meta.get_field(
                'pw_total_severe_malaria_cases').verbose_name),
        'd3_pw_total_malaria_death': ExcelFormField(
            'E42', int,
            EpidemioMalariaR._meta.get_field(
                'pw_total_malaria_death').verbose_name),
        'd3_pw_total_death_all_causes': ExcelFormField(
            'E45', int,
            EpidemioMalariaR._meta.get_field(
                'pw_total_death_all_causes').verbose_name),

        'd4_u5_total_consultation_all_causes': ExcelFormField(
            'F10', int,
            EpidemioMalariaR._meta.get_field(
                'u5_total_consultation_all_causes').verbose_name),
        'd4_u5_total_suspected_malaria_cases': ExcelFormField(
            'F13', int,
            EpidemioMalariaR._meta.get_field(
                'u5_total_suspected_malaria_cases').verbose_name),
        'd4_u5_total_rdt_tested_malaria_cases': ExcelFormField(
            'F16', int,
            EpidemioMalariaR._meta.get_field(
                'u5_total_rdt_tested_malaria_cases').verbose_name),
        'd4_u5_total_rdt_confirmed_malaria_cases': ExcelFormField(
            'F19', int,
            EpidemioMalariaR._meta.get_field(
                'u5_total_rdt_confirmed_malaria_cases').verbose_name),
        'd4_u5_total_rdt_pfalciparum_malaria_cases': ExcelFormField(
            'F22', int,
            EpidemioMalariaR._meta.get_field(
                'u5_total_rdt_pfalciparum_malaria_cases').verbose_name),
        'd4_u5_total_ts_tested_malaria_cases': ExcelFormField(
            'F25', int,
            EpidemioMalariaR._meta.get_field(
                'u5_total_ts_tested_malaria_cases').verbose_name),
        'd4_u5_total_ts_confirmed_malaria_cases': ExcelFormField(
            'F28', int,
            EpidemioMalariaR._meta.get_field(
                'u5_total_ts_confirmed_malaria_cases').verbose_name),
        'd4_u5_total_ts_pfalciparum_malaria_cases': ExcelFormField(
            'F31', int,
            EpidemioMalariaR._meta.get_field(
                'u5_total_ts_pfalciparum_malaria_cases').verbose_name),
        'd4_u5_total_simple_malaria_cases': ExcelFormField(
            'F34', int,
            EpidemioMalariaR._meta.get_field(
                'u5_total_simple_malaria_cases').verbose_name),
        'd4_u5_total_severe_malaria_cases': ExcelFormField(
            'F37', int,
            EpidemioMalariaR._meta.get_field(
                'u5_total_severe_malaria_cases').verbose_name),
        'd4_u5_total_malaria_death': ExcelFormField(
            'F40', int,
            EpidemioMalariaR._meta.get_field(
                'u5_total_malaria_death').verbose_name),
        'd4_u5_total_death_all_causes': ExcelFormField(
            'F43', int,
            EpidemioMalariaR._meta.get_field(
                'u5_total_death_all_causes').verbose_name),

        'd4_o5_total_consultation_all_causes': ExcelFormField(
            'F11', int,
            EpidemioMalariaR._meta.get_field(
                'o5_total_consultation_all_causes').verbose_name),
        'd4_o5_total_suspected_malaria_cases': ExcelFormField(
            'F14', int,
            EpidemioMalariaR._meta.get_field(
                'o5_total_suspected_malaria_cases').verbose_name),
        'd4_o5_total_rdt_tested_malaria_cases': ExcelFormField(
            'F17', int,
            EpidemioMalariaR._meta.get_field(
                'o5_total_rdt_tested_malaria_cases').verbose_name),
        'd4_o5_total_rdt_confirmed_malaria_cases': ExcelFormField(
            'F20', int,
            EpidemioMalariaR._meta.get_field(
                'o5_total_rdt_confirmed_malaria_cases').verbose_name),
        'd4_o5_total_rdt_pfalciparum_malaria_cases': ExcelFormField(
            'F23', int,
            EpidemioMalariaR._meta.get_field(
                'o5_total_rdt_pfalciparum_malaria_cases').verbose_name),
        'd4_o5_total_ts_tested_malaria_cases': ExcelFormField(
            'F26', int,
            EpidemioMalariaR._meta.get_field(
                'o5_total_ts_tested_malaria_cases').verbose_name),
        'd4_o5_total_ts_confirmed_malaria_cases': ExcelFormField(
            'F29', int,
            EpidemioMalariaR._meta.get_field(
                'o5_total_ts_confirmed_malaria_cases').verbose_name),
        'd4_o5_total_ts_pfalciparum_malaria_cases': ExcelFormField(
            'F32', int,
            EpidemioMalariaR._meta.get_field(
                'o5_total_ts_pfalciparum_malaria_cases').verbose_name),
        'd4_o5_total_simple_malaria_cases': ExcelFormField(
            'F35', int,
            EpidemioMalariaR._meta.get_field(
                'o5_total_simple_malaria_cases').verbose_name),
        'd4_o5_total_severe_malaria_cases': ExcelFormField(
            'F38', int,
            EpidemioMalariaR._meta.get_field(
                'o5_total_severe_malaria_cases').verbose_name),
        'd4_o5_total_malaria_death': ExcelFormField(
            'F41', int,
            EpidemioMalariaR._meta.get_field(
                'o5_total_malaria_death').verbose_name),
        'd4_o5_total_death_all_causes': ExcelFormField(
            'F34', int,
            EpidemioMalariaR._meta.get_field(
                'o5_total_death_all_causes').verbose_name),

        'd4_pw_total_consultation_all_causes': ExcelFormField(
            'F12', int,
            EpidemioMalariaR._meta.get_field(
                'pw_total_consultation_all_causes').verbose_name),
        'd4_pw_total_suspected_malaria_cases': ExcelFormField(
            'F15', int,
            EpidemioMalariaR._meta.get_field(
                'pw_total_suspected_malaria_cases').verbose_name),
        'd4_pw_total_rdt_tested_malaria_cases': ExcelFormField(
            'F18', int,
            EpidemioMalariaR._meta.get_field(
                'pw_total_rdt_tested_malaria_cases').verbose_name),
        'd4_pw_total_rdt_confirmed_malaria_cases': ExcelFormField(
            'F21', int,
            EpidemioMalariaR._meta.get_field(
                'pw_total_rdt_confirmed_malaria_cases').verbose_name),
        'd4_pw_total_rdt_pfalciparum_malaria_cases': ExcelFormField(
            'F24', int,
            EpidemioMalariaR._meta.get_field(
                'pw_total_rdt_pfalciparum_malaria_cases').verbose_name),
        'd4_pw_total_ts_tested_malaria_cases': ExcelFormField(
            'F27', int,
            EpidemioMalariaR._meta.get_field(
                'pw_total_ts_tested_malaria_cases').verbose_name),
        'd4_pw_total_ts_confirmed_malaria_cases': ExcelFormField(
            'F30', int,
            EpidemioMalariaR._meta.get_field(
                'pw_total_ts_confirmed_malaria_cases').verbose_name),
        'd4_pw_total_ts_pfalciparum_malaria_cases': ExcelFormField(
            'F33', int,
            EpidemioMalariaR._meta.get_field(
                'pw_total_ts_pfalciparum_malaria_cases').verbose_name),
        'd4_pw_total_simple_malaria_cases': ExcelFormField(
            'F36', int,
            EpidemioMalariaR._meta.get_field(
                'pw_total_simple_malaria_cases').verbose_name),
        'd4_pw_total_severe_malaria_cases': ExcelFormField(
            'F39', int,
            EpidemioMalariaR._meta.get_field(
                'pw_total_severe_malaria_cases').verbose_name),
        'd4_pw_total_malaria_death': ExcelFormField(
            'F42', int,
            EpidemioMalariaR._meta.get_field(
                'pw_total_malaria_death').verbose_name),
        'd4_pw_total_death_all_causes': ExcelFormField(
            'F45', int,
            EpidemioMalariaR._meta.get_field(
                'pw_total_death_all_causes').verbose_name),

        'd5_u5_total_consultation_all_causes': ExcelFormField(
            'G10', int,
            EpidemioMalariaR._meta.get_field(
                'u5_total_consultation_all_causes').verbose_name),
        'd5_u5_total_suspected_malaria_cases': ExcelFormField(
            'G13', int,
            EpidemioMalariaR._meta.get_field(
                'u5_total_suspected_malaria_cases').verbose_name),
        'd5_u5_total_rdt_tested_malaria_cases': ExcelFormField(
            'G16', int,
            EpidemioMalariaR._meta.get_field(
                'u5_total_rdt_tested_malaria_cases').verbose_name),
        'd5_u5_total_rdt_confirmed_malaria_cases': ExcelFormField(
            'G19', int,
            EpidemioMalariaR._meta.get_field(
                'u5_total_rdt_confirmed_malaria_cases').verbose_name),
        'd5_u5_total_rdt_pfalciparum_malaria_cases': ExcelFormField(
            'G22', int,
            EpidemioMalariaR._meta.get_field(
                'u5_total_rdt_pfalciparum_malaria_cases').verbose_name),
        'd5_u5_total_ts_tested_malaria_cases': ExcelFormField(
            'G25', int,
            EpidemioMalariaR._meta.get_field(
                'u5_total_ts_tested_malaria_cases').verbose_name),
        'd5_u5_total_ts_confirmed_malaria_cases': ExcelFormField(
            'G28', int,
            EpidemioMalariaR._meta.get_field(
                'u5_total_ts_confirmed_malaria_cases').verbose_name),
        'd5_u5_total_ts_pfalciparum_malaria_cases': ExcelFormField(
            'G31', int,
            EpidemioMalariaR._meta.get_field(
                'u5_total_ts_pfalciparum_malaria_cases').verbose_name),
        'd5_u5_total_simple_malaria_cases': ExcelFormField(
            'G34', int,
            EpidemioMalariaR._meta.get_field(
                'u5_total_simple_malaria_cases').verbose_name),
        'd5_u5_total_severe_malaria_cases': ExcelFormField(
            'G37', int,
            EpidemioMalariaR._meta.get_field(
                'u5_total_severe_malaria_cases').verbose_name),
        'd5_u5_total_malaria_death': ExcelFormField(
            'G40', int,
            EpidemioMalariaR._meta.get_field(
                'u5_total_malaria_death').verbose_name),
        'd5_u5_total_death_all_causes': ExcelFormField(
            'G43', int,
            EpidemioMalariaR._meta.get_field(
                'u5_total_death_all_causes').verbose_name),

        'd5_o5_total_consultation_all_causes': ExcelFormField(
            'G11', int,
            EpidemioMalariaR._meta.get_field(
                'o5_total_consultation_all_causes').verbose_name),
        'd5_o5_total_suspected_malaria_cases': ExcelFormField(
            'G14', int,
            EpidemioMalariaR._meta.get_field(
                'o5_total_suspected_malaria_cases').verbose_name),
        'd5_o5_total_rdt_tested_malaria_cases': ExcelFormField(
            'G17', int,
            EpidemioMalariaR._meta.get_field(
                'o5_total_rdt_tested_malaria_cases').verbose_name),
        'd5_o5_total_rdt_confirmed_malaria_cases': ExcelFormField(
            'G20', int,
            EpidemioMalariaR._meta.get_field(
                'o5_total_rdt_confirmed_malaria_cases').verbose_name),
        'd5_o5_total_rdt_pfalciparum_malaria_cases': ExcelFormField(
            'G23', int,
            EpidemioMalariaR._meta.get_field(
                'o5_total_rdt_pfalciparum_malaria_cases').verbose_name),
        'd5_o5_total_ts_tested_malaria_cases': ExcelFormField(
            'G26', int,
            EpidemioMalariaR._meta.get_field(
                'o5_total_ts_tested_malaria_cases').verbose_name),
        'd5_o5_total_ts_confirmed_malaria_cases': ExcelFormField(
            'G29', int,
            EpidemioMalariaR._meta.get_field(
                'o5_total_ts_confirmed_malaria_cases').verbose_name),
        'd5_o5_total_ts_pfalciparum_malaria_cases': ExcelFormField(
            'G32', int,
            EpidemioMalariaR._meta.get_field(
                'o5_total_ts_pfalciparum_malaria_cases').verbose_name),
        'd5_o5_total_simple_malaria_cases': ExcelFormField(
            'G35', int,
            EpidemioMalariaR._meta.get_field(
                'o5_total_simple_malaria_cases').verbose_name),
        'd5_o5_total_severe_malaria_cases': ExcelFormField(
            'G38', int,
            EpidemioMalariaR._meta.get_field(
                'o5_total_severe_malaria_cases').verbose_name),
        'd5_o5_total_malaria_death': ExcelFormField(
            'G41', int,
            EpidemioMalariaR._meta.get_field(
                'o5_total_malaria_death').verbose_name),
        'd5_o5_total_death_all_causes': ExcelFormField(
            'G34', int,
            EpidemioMalariaR._meta.get_field(
                'o5_total_death_all_causes').verbose_name),

        'd5_pw_total_consultation_all_causes': ExcelFormField(
            'G12', int,
            EpidemioMalariaR._meta.get_field(
                'pw_total_consultation_all_causes').verbose_name),
        'd5_pw_total_suspected_malaria_cases': ExcelFormField(
            'G15', int,
            EpidemioMalariaR._meta.get_field(
                'pw_total_suspected_malaria_cases').verbose_name),
        'd5_pw_total_rdt_tested_malaria_cases': ExcelFormField(
            'G18', int,
            EpidemioMalariaR._meta.get_field(
                'pw_total_rdt_tested_malaria_cases').verbose_name),
        'd5_pw_total_rdt_confirmed_malaria_cases': ExcelFormField(
            'G21', int,
            EpidemioMalariaR._meta.get_field(
                'pw_total_rdt_confirmed_malaria_cases').verbose_name),
        'd5_pw_total_rdt_pfalciparum_malaria_cases': ExcelFormField(
            'G24', int,
            EpidemioMalariaR._meta.get_field(
                'pw_total_rdt_pfalciparum_malaria_cases').verbose_name),
        'd5_pw_total_ts_tested_malaria_cases': ExcelFormField(
            'G27', int,
            EpidemioMalariaR._meta.get_field(
                'pw_total_ts_tested_malaria_cases').verbose_name),
        'd5_pw_total_ts_confirmed_malaria_cases': ExcelFormField(
            'G30', int,
            EpidemioMalariaR._meta.get_field(
                'pw_total_ts_confirmed_malaria_cases').verbose_name),
        'd5_pw_total_ts_pfalciparum_malaria_cases': ExcelFormField(
            'G33', int,
            EpidemioMalariaR._meta.get_field(
                'pw_total_ts_pfalciparum_malaria_cases').verbose_name),
        'd5_pw_total_simple_malaria_cases': ExcelFormField(
            'G36', int,
            EpidemioMalariaR._meta.get_field(
                'pw_total_simple_malaria_cases').verbose_name),
        'd5_pw_total_severe_malaria_cases': ExcelFormField(
            'G39', int,
            EpidemioMalariaR._meta.get_field(
                'pw_total_severe_malaria_cases').verbose_name),
        'd5_pw_total_malaria_death': ExcelFormField(
            'G42', int,
            EpidemioMalariaR._meta.get_field(
                'pw_total_malaria_death').verbose_name),
        'd5_pw_total_death_all_causes': ExcelFormField(
            'G45', int,
            EpidemioMalariaR._meta.get_field(
                'pw_total_death_all_causes').verbose_name),

        'd6_u5_total_consultation_all_causes': ExcelFormField(
            'H10', int,
            EpidemioMalariaR._meta.get_field(
                'u5_total_consultation_all_causes').verbose_name),
        'd6_u5_total_suspected_malaria_cases': ExcelFormField(
            'H13', int,
            EpidemioMalariaR._meta.get_field(
                'u5_total_suspected_malaria_cases').verbose_name),
        'd6_u5_total_rdt_tested_malaria_cases': ExcelFormField(
            'H16', int,
            EpidemioMalariaR._meta.get_field(
                'u5_total_rdt_tested_malaria_cases').verbose_name),
        'd6_u5_total_rdt_confirmed_malaria_cases': ExcelFormField(
            'H19', int,
            EpidemioMalariaR._meta.get_field(
                'u5_total_rdt_confirmed_malaria_cases').verbose_name),
        'd6_u5_total_rdt_pfalciparum_malaria_cases': ExcelFormField(
            'H22', int,
            EpidemioMalariaR._meta.get_field(
                'u5_total_rdt_pfalciparum_malaria_cases').verbose_name),
        'd6_u5_total_ts_tested_malaria_cases': ExcelFormField(
            'H25', int,
            EpidemioMalariaR._meta.get_field(
                'u5_total_ts_tested_malaria_cases').verbose_name),
        'd6_u5_total_ts_confirmed_malaria_cases': ExcelFormField(
            'H28', int,
            EpidemioMalariaR._meta.get_field(
                'u5_total_ts_confirmed_malaria_cases').verbose_name),
        'd6_u5_total_ts_pfalciparum_malaria_cases': ExcelFormField(
            'H31', int,
            EpidemioMalariaR._meta.get_field(
                'u5_total_ts_pfalciparum_malaria_cases').verbose_name),
        'd6_u5_total_simple_malaria_cases': ExcelFormField(
            'H34', int,
            EpidemioMalariaR._meta.get_field(
                'u5_total_simple_malaria_cases').verbose_name),
        'd6_u5_total_severe_malaria_cases': ExcelFormField(
            'H37', int,
            EpidemioMalariaR._meta.get_field(
                'u5_total_severe_malaria_cases').verbose_name),
        'd6_u5_total_malaria_death': ExcelFormField(
            'H40', int,
            EpidemioMalariaR._meta.get_field(
                'u5_total_malaria_death').verbose_name),
        'd6_u5_total_death_all_causes': ExcelFormField(
            'H43', int,
            EpidemioMalariaR._meta.get_field(
                'u5_total_death_all_causes').verbose_name),

        'd6_o5_total_consultation_all_causes': ExcelFormField(
            'H11', int,
            EpidemioMalariaR._meta.get_field(
                'o5_total_consultation_all_causes').verbose_name),
        'd6_o5_total_suspected_malaria_cases': ExcelFormField(
            'H14', int,
            EpidemioMalariaR._meta.get_field(
                'o5_total_suspected_malaria_cases').verbose_name),
        'd6_o5_total_rdt_tested_malaria_cases': ExcelFormField(
            'H17', int,
            EpidemioMalariaR._meta.get_field(
                'o5_total_rdt_tested_malaria_cases').verbose_name),
        'd6_o5_total_rdt_confirmed_malaria_cases': ExcelFormField(
            'H20', int,
            EpidemioMalariaR._meta.get_field(
                'o5_total_rdt_confirmed_malaria_cases').verbose_name),
        'd6_o5_total_rdt_pfalciparum_malaria_cases': ExcelFormField(
            'H23', int,
            EpidemioMalariaR._meta.get_field(
                'o5_total_rdt_pfalciparum_malaria_cases').verbose_name),
        'd6_o5_total_ts_tested_malaria_cases': ExcelFormField(
            'H26', int,
            EpidemioMalariaR._meta.get_field(
                'o5_total_ts_tested_malaria_cases').verbose_name),
        'd6_o5_total_ts_confirmed_malaria_cases': ExcelFormField(
            'H29', int,
            EpidemioMalariaR._meta.get_field(
                'o5_total_ts_confirmed_malaria_cases').verbose_name),
        'd6_o5_total_ts_pfalciparum_malaria_cases': ExcelFormField(
            'H32', int,
            EpidemioMalariaR._meta.get_field(
                'o5_total_ts_pfalciparum_malaria_cases').verbose_name),
        'd6_o5_total_simple_malaria_cases': ExcelFormField(
            'H35', int,
            EpidemioMalariaR._meta.get_field(
                'o5_total_simple_malaria_cases').verbose_name),
        'd6_o5_total_severe_malaria_cases': ExcelFormField(
            'H38', int,
            EpidemioMalariaR._meta.get_field(
                'o5_total_severe_malaria_cases').verbose_name),
        'd6_o5_total_malaria_death': ExcelFormField(
            'H41', int,
            EpidemioMalariaR._meta.get_field(
                'o5_total_malaria_death').verbose_name),
        'd6_o5_total_death_all_causes': ExcelFormField(
            'H34', int,
            EpidemioMalariaR._meta.get_field(
                'o5_total_death_all_causes').verbose_name),

        'd6_pw_total_consultation_all_causes': ExcelFormField(
            'H12', int,
            EpidemioMalariaR._meta.get_field(
                'pw_total_consultation_all_causes').verbose_name),
        'd6_pw_total_suspected_malaria_cases': ExcelFormField(
            'H15', int,
            EpidemioMalariaR._meta.get_field(
                'pw_total_suspected_malaria_cases').verbose_name),
        'd6_pw_total_rdt_tested_malaria_cases': ExcelFormField(
            'H18', int,
            EpidemioMalariaR._meta.get_field(
                'pw_total_rdt_tested_malaria_cases').verbose_name),
        'd6_pw_total_rdt_confirmed_malaria_cases': ExcelFormField(
            'H21', int,
            EpidemioMalariaR._meta.get_field(
                'pw_total_rdt_confirmed_malaria_cases').verbose_name),
        'd6_pw_total_rdt_pfalciparum_malaria_cases': ExcelFormField(
            'H24', int,
            EpidemioMalariaR._meta.get_field(
                'pw_total_rdt_pfalciparum_malaria_cases').verbose_name),
        'd6_pw_total_ts_tested_malaria_cases': ExcelFormField(
            'H27', int,
            EpidemioMalariaR._meta.get_field(
                'pw_total_ts_tested_malaria_cases').verbose_name),
        'd6_pw_total_ts_confirmed_malaria_cases': ExcelFormField(
            'H30', int,
            EpidemioMalariaR._meta.get_field(
                'pw_total_ts_confirmed_malaria_cases').verbose_name),
        'd6_pw_total_ts_pfalciparum_malaria_cases': ExcelFormField(
            'H33', int,
            EpidemioMalariaR._meta.get_field(
                'pw_total_ts_pfalciparum_malaria_cases').verbose_name),
        'd6_pw_total_simple_malaria_cases': ExcelFormField(
            'H36', int,
            EpidemioMalariaR._meta.get_field(
                'pw_total_simple_malaria_cases').verbose_name),
        'd6_pw_total_severe_malaria_cases': ExcelFormField(
            'H39', int,
            EpidemioMalariaR._meta.get_field(
                'pw_total_severe_malaria_cases').verbose_name),
        'd6_pw_total_malaria_death': ExcelFormField(
            'H42', int,
            EpidemioMalariaR._meta.get_field(
                'pw_total_malaria_death').verbose_name),
        'd6_pw_total_death_all_causes': ExcelFormField(
            'H45', int,
            EpidemioMalariaR._meta.get_field(
                'pw_total_death_all_causes').verbose_name),

        'd7_u5_total_consultation_all_causes': ExcelFormField(
            'I10', int,
            EpidemioMalariaR._meta.get_field(
                'u5_total_consultation_all_causes').verbose_name),
        'd7_u5_total_suspected_malaria_cases': ExcelFormField(
            'I13', int,
            EpidemioMalariaR._meta.get_field(
                'u5_total_suspected_malaria_cases').verbose_name),
        'd7_u5_total_rdt_tested_malaria_cases': ExcelFormField(
            'I16', int,
            EpidemioMalariaR._meta.get_field(
                'u5_total_rdt_tested_malaria_cases').verbose_name),
        'd7_u5_total_rdt_confirmed_malaria_cases': ExcelFormField(
            'I19', int,
            EpidemioMalariaR._meta.get_field(
                'u5_total_rdt_confirmed_malaria_cases').verbose_name),
        'd7_u5_total_rdt_pfalciparum_malaria_cases': ExcelFormField(
            'I22', int,
            EpidemioMalariaR._meta.get_field(
                'u5_total_rdt_pfalciparum_malaria_cases').verbose_name),
        'd7_u5_total_ts_tested_malaria_cases': ExcelFormField(
            'I25', int,
            EpidemioMalariaR._meta.get_field(
                'u5_total_ts_tested_malaria_cases').verbose_name),
        'd7_u5_total_ts_confirmed_malaria_cases': ExcelFormField(
            'I28', int,
            EpidemioMalariaR._meta.get_field(
                'u5_total_ts_confirmed_malaria_cases').verbose_name),
        'd7_u5_total_ts_pfalciparum_malaria_cases': ExcelFormField(
            'I31', int,
            EpidemioMalariaR._meta.get_field(
                'u5_total_ts_pfalciparum_malaria_cases').verbose_name),
        'd7_u5_total_simple_malaria_cases': ExcelFormField(
            'I34', int,
            EpidemioMalariaR._meta.get_field(
                'u5_total_simple_malaria_cases').verbose_name),
        'd7_u5_total_severe_malaria_cases': ExcelFormField(
            'I37', int,
            EpidemioMalariaR._meta.get_field(
                'u5_total_severe_malaria_cases').verbose_name),
        'd7_u5_total_malaria_death': ExcelFormField(
            'I40', int,
            EpidemioMalariaR._meta.get_field(
                'u5_total_malaria_death').verbose_name),
        'd7_u5_total_death_all_causes': ExcelFormField(
            'I43', int,
            EpidemioMalariaR._meta.get_field(
                'u5_total_death_all_causes').verbose_name),

        'd7_o5_total_consultation_all_causes': ExcelFormField(
            'I11', int,
            EpidemioMalariaR._meta.get_field(
                'o5_total_consultation_all_causes').verbose_name),
        'd7_o5_total_suspected_malaria_cases': ExcelFormField(
            'I14', int,
            EpidemioMalariaR._meta.get_field(
                'o5_total_suspected_malaria_cases').verbose_name),
        'd7_o5_total_rdt_tested_malaria_cases': ExcelFormField(
            'I17', int,
            EpidemioMalariaR._meta.get_field(
                'o5_total_rdt_tested_malaria_cases').verbose_name),
        'd7_o5_total_rdt_confirmed_malaria_cases': ExcelFormField(
            'I20', int,
            EpidemioMalariaR._meta.get_field(
                'o5_total_rdt_confirmed_malaria_cases').verbose_name),
        'd7_o5_total_rdt_pfalciparum_malaria_cases': ExcelFormField(
            'I23', int,
            EpidemioMalariaR._meta.get_field(
                'o5_total_rdt_pfalciparum_malaria_cases').verbose_name),
        'd7_o5_total_ts_tested_malaria_cases': ExcelFormField(
            'I26', int,
            EpidemioMalariaR._meta.get_field(
                'o5_total_ts_tested_malaria_cases').verbose_name),
        'd7_o5_total_ts_confirmed_malaria_cases': ExcelFormField(
            'I29', int,
            EpidemioMalariaR._meta.get_field(
                'o5_total_ts_confirmed_malaria_cases').verbose_name),
        'd7_o5_total_ts_pfalciparum_malaria_cases': ExcelFormField(
            'I32', int,
            EpidemioMalariaR._meta.get_field(
                'o5_total_ts_pfalciparum_malaria_cases').verbose_name),
        'd7_o5_total_simple_malaria_cases': ExcelFormField(
            'I35', int,
            EpidemioMalariaR._meta.get_field(
                'o5_total_simple_malaria_cases').verbose_name),
        'd7_o5_total_severe_malaria_cases': ExcelFormField(
            'I38', int,
            EpidemioMalariaR._meta.get_field(
                'o5_total_severe_malaria_cases').verbose_name),
        'd7_o5_total_malaria_death': ExcelFormField(
            'I41', int,
            EpidemioMalariaR._meta.get_field(
                'o5_total_malaria_death').verbose_name),
        'd7_o5_total_death_all_causes': ExcelFormField(
            'I34', int,
            EpidemioMalariaR._meta.get_field(
                'o5_total_death_all_causes').verbose_name),

        'd7_pw_total_consultation_all_causes': ExcelFormField(
            'I12', int,
            EpidemioMalariaR._meta.get_field(
                'pw_total_consultation_all_causes').verbose_name),
        'd7_pw_total_suspected_malaria_cases': ExcelFormField(
            'I15', int,
            EpidemioMalariaR._meta.get_field(
                'pw_total_suspected_malaria_cases').verbose_name),
        'd7_pw_total_rdt_tested_malaria_cases': ExcelFormField(
            'I18', int,
            EpidemioMalariaR._meta.get_field(
                'pw_total_rdt_tested_malaria_cases').verbose_name),
        'd7_pw_total_rdt_confirmed_malaria_cases': ExcelFormField(
            'I21', int,
            EpidemioMalariaR._meta.get_field(
                'pw_total_rdt_confirmed_malaria_cases').verbose_name),
        'd7_pw_total_rdt_pfalciparum_malaria_cases': ExcelFormField(
            'I24', int,
            EpidemioMalariaR._meta.get_field(
                'pw_total_rdt_pfalciparum_malaria_cases').verbose_name),
        'd7_pw_total_ts_tested_malaria_cases': ExcelFormField(
            'I27', int,
            EpidemioMalariaR._meta.get_field(
                'pw_total_ts_tested_malaria_cases').verbose_name),
        'd7_pw_total_ts_confirmed_malaria_cases': ExcelFormField(
            'I30', int,
            EpidemioMalariaR._meta.get_field(
                'pw_total_ts_confirmed_malaria_cases').verbose_name),
        'd7_pw_total_ts_pfalciparum_malaria_cases': ExcelFormField(
            'I33', int,
            EpidemioMalariaR._meta.get_field(
                'pw_total_ts_pfalciparum_malaria_cases').verbose_name),
        'd7_pw_total_simple_malaria_cases': ExcelFormField(
            'I36', int,
            EpidemioMalariaR._meta.get_field(
                'pw_total_simple_malaria_cases').verbose_name),
        'd7_pw_total_severe_malaria_cases': ExcelFormField(
            'I39', int,
            EpidemioMalariaR._meta.get_field(
                'pw_total_severe_malaria_cases').verbose_name),
        'd7_pw_total_malaria_death': ExcelFormField(
            'I42', int,
            EpidemioMalariaR._meta.get_field(
                'pw_total_malaria_death').verbose_name),
        'd7_pw_total_death_all_causes': ExcelFormField(
            'I45', int,
            EpidemioMalariaR._meta.get_field(
                'pw_total_death_all_causes').verbose_name),
        }
    }

    def create_report(self, provider):

        expected_reporting = self.get('expected_reporting')

        # return report, text_message (success or failure)
        return create_epidemio_report(provider=provider,
                                      expected_reporting=expected_reporting,
                                      completed_on=timezone.now(),
                                      integrity_checker=self,
                                      data_source=self.filepath)


EXPORTED_FORMS = [
    (class_str(MalariaExcelForm), "Routine Mensuelle Paludisme",
     {'version': '0.5'}),
    (class_str(MalariaExcelForm), "Routine Mensuelle Paludisme (ancien)",
     {'version': '0.4'}),
    (class_str(EpidemioMalariaRForm), "Épidémiologie hebdomadaire Paludisme")
]
