#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import, division,
                        print_function)
import logging

from py3compat import text_type
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from snisi_core.xls_import import (ExcelForm, ExcelFormField)
from snisi_tools import type_converters
from snisi_tools.misc import class_str
from snisi_epidemiology import get_domain
from snisi_epidemiology.integrity import (
    EpidemiologyRIntegrityChecker,
    EpidemiologyRDistrictIntegrityChecker, create_epid_report)
from snisi_epidemiology.models import EpidemiologyR

logger = logging.getLogger(__name__)


class EpidemiologyExcelForm(EpidemiologyRIntegrityChecker, ExcelForm):

    domain = get_domain()

    DAY_MAP = range(1, 31)
    MONTH_MAP = range(1, 13)
    YEAR_MAP = range(2014, 2022)

    _mapping = {'0.1': {
        'hc': ExcelFormField('C3', text_type, _("Health Center")),
        'day': ExcelFormField('C4', type_converters.NormalizedIntChoiceList,
                              _("Day"), cast_args=DAY_MAP),
        'month': ExcelFormField('E4', type_converters.NormalizedIntChoiceList,
                                _("Month"), cast_args=MONTH_MAP),
        'year': ExcelFormField('G4', type_converters.NormalizedIntChoiceList,
                               _("Year"), cast_args=YEAR_MAP),
        'ebola_case': ExcelFormField(
            'D7', int,
            EpidemiologyR._meta.get_field('ebola_case').verbose_name),
        'ebola_death': ExcelFormField(
            'F7', int,
            EpidemiologyR._meta.get_field('ebola_death').verbose_name),
        'acute_flaccid_paralysis_case': ExcelFormField(
            'D8', int,
            EpidemiologyR._meta.get_field(
                'acute_flaccid_paralysis_case').verbose_name),
        'acute_flaccid_paralysis_death': ExcelFormField(
            'F8', int,
            EpidemiologyR._meta.get_field(
                'acute_flaccid_paralysis_death').verbose_name),
        'influenza_a_h1n1_case': ExcelFormField(
            'D9', int,
            EpidemiologyR._meta.get_field(
                'influenza_a_h1n1_case').verbose_name),
        'influenza_a_h1n1_death': ExcelFormField(
            'F9', int,
            EpidemiologyR._meta.get_field(
                'influenza_a_h1n1_death').verbose_name),
        'cholera_case': ExcelFormField(
            'D10', int,
            EpidemiologyR._meta.get_field('cholera_case').verbose_name),
        'cholera_death': ExcelFormField(
            'F10', int,
            EpidemiologyR._meta.get_field('cholera_death').verbose_name),
        'red_diarrhea_case': ExcelFormField(
            'D11', int,
            EpidemiologyR._meta.get_field('red_diarrhea_case').verbose_name),
        'red_diarrhea_death': ExcelFormField(
            'F11', int,
            EpidemiologyR._meta.get_field('red_diarrhea_death').verbose_name),
        'measles_case': ExcelFormField(
            'D12', int,
            EpidemiologyR._meta.get_field('measles_case').verbose_name),
        'measles_death': ExcelFormField(
            'F12', int,
            EpidemiologyR._meta.get_field('measles_death').verbose_name),
        'yellow_fever_case': ExcelFormField(
            'D13', int,
            EpidemiologyR._meta.get_field('yellow_fever_case').verbose_name),
        'yellow_fever_death': ExcelFormField(
            'F13', int,
            EpidemiologyR._meta.get_field('yellow_fever_death').verbose_name),
        'neonatal_tetanus_case': ExcelFormField(
            'D14', int,
            EpidemiologyR._meta.get_field(
                'neonatal_tetanus_case').verbose_name),
        'neonatal_tetanus_death': ExcelFormField(
            'F14', int,
            EpidemiologyR._meta.get_field(
                'neonatal_tetanus_death').verbose_name),
        'meningitis_case': ExcelFormField(
            'D15', int,
            EpidemiologyR._meta.get_field('meningitis_case').verbose_name),
        'meningitis_death': ExcelFormField(
            'F15', int,
            EpidemiologyR._meta.get_field('meningitis_death').verbose_name),
        'rabies_case': ExcelFormField(
            'D16', int,
            EpidemiologyR._meta.get_field('rabies_case').verbose_name),
        'rabies_death': ExcelFormField(
            'F16', int,
            EpidemiologyR._meta.get_field('rabies_death').verbose_name),
        'acute_measles_diarrhea_case': ExcelFormField(
            'D17', int,
            EpidemiologyR._meta.get_field(
                'acute_measles_diarrhea_case').verbose_name),
        'acute_measles_diarrhea_death': ExcelFormField(
            'F17', int,
            EpidemiologyR._meta.get_field(
                'acute_measles_diarrhea_death').verbose_name),
        'other_notifiable_disease_case': ExcelFormField(
            'D18', int,
            EpidemiologyR._meta.get_field(
                'other_notifiable_disease_case').verbose_name),
        'other_notifiable_disease_death': ExcelFormField(
            'F18', int,
            EpidemiologyR._meta.get_field(
                'other_notifiable_disease_death').verbose_name),
        }
    }

    def create_report(self, provider):
        expected_reporting = self.get('expected_reporting')

        return create_epid_report(provider=provider,
                                  expected_reporting=expected_reporting,
                                  completed_on=timezone.now(),
                                  integrity_checker=self,
                                  data_source=self.filepath)


class EpidemiologyDistrictExcelForm(
        EpidemiologyRDistrictIntegrityChecker, ExcelForm):

    DAY_MAP = range(1, 31)
    MONTH_MAP = range(1, 13)
    YEAR_MAP = range(2014, 2022)

    _mapping = {'0.1': {
        'hc': ExcelFormField('C3', text_type, _("Health Center")),
        'day': ExcelFormField('C4', type_converters.NormalizedIntChoiceList,
                              _("Day"), cast_args=DAY_MAP),
        'month': ExcelFormField('E4', type_converters.NormalizedIntChoiceList,
                                _("Month"), cast_args=MONTH_MAP),
        'year': ExcelFormField('G4', type_converters.NormalizedIntChoiceList,
                               _("Year"), cast_args=YEAR_MAP),

        # line 1
        'snisi_code_1': ExcelFormField('A9', text_type, _("Health Center")),
        'ebola_case_1': ExcelFormField(
            'D9', int,
            EpidemiologyR._meta.get_field('ebola_case').verbose_name),
        'ebola_death_1': ExcelFormField(
            'D10', int,
            EpidemiologyR._meta.get_field('ebola_death').verbose_name),
        'acute_flaccid_paralysis_case_1': ExcelFormField(
            'E9', int,
            EpidemiologyR._meta.get_field(
                'acute_flaccid_paralysis_case').verbose_name),
        'acute_flaccid_paralysis_death_1': ExcelFormField(
            'E10', int,
            EpidemiologyR._meta.get_field(
                'acute_flaccid_paralysis_death').verbose_name),
        'influenza_a_h1n1_case_1': ExcelFormField(
            'F9', int,
            EpidemiologyR._meta.get_field(
                'influenza_a_h1n1_case').verbose_name),
        'influenza_a_h1n1_death_1': ExcelFormField(
            'F10', int,
            EpidemiologyR._meta.get_field(
                'influenza_a_h1n1_death').verbose_name),
        'cholera_case_1': ExcelFormField(
            'G9', int,
            EpidemiologyR._meta.get_field('cholera_case').verbose_name),
        'cholera_death_1': ExcelFormField(
            'G10', int,
            EpidemiologyR._meta.get_field('cholera_death').verbose_name),
        'red_diarrhea_case_1': ExcelFormField(
            'H9', int,
            EpidemiologyR._meta.get_field('red_diarrhea_case').verbose_name),
        'red_diarrhea_death_1': ExcelFormField(
            'H10', int,
            EpidemiologyR._meta.get_field('red_diarrhea_death').verbose_name),
        'measles_case_1': ExcelFormField(
            'I9', int,
            EpidemiologyR._meta.get_field('measles_case').verbose_name),
        'measles_death_1': ExcelFormField(
            'I10', int,
            EpidemiologyR._meta.get_field('measles_death').verbose_name),
        'yellow_fever_case_1': ExcelFormField(
            'J9', int,
            EpidemiologyR._meta.get_field('yellow_fever_case').verbose_name),
        'yellow_fever_death_1': ExcelFormField(
            'J10', int,
            EpidemiologyR._meta.get_field('yellow_fever_death').verbose_name),
        'neonatal_tetanus_case_1': ExcelFormField(
            'K9', int,
            EpidemiologyR._meta.get_field(
                'neonatal_tetanus_case').verbose_name),
        'neonatal_tetanus_death_1': ExcelFormField(
            'K10', int,
            EpidemiologyR._meta.get_field(
                'neonatal_tetanus_death').verbose_name),
        'meningitis_case_1': ExcelFormField(
            'L9', int,
            EpidemiologyR._meta.get_field('meningitis_case').verbose_name),
        'meningitis_death_1': ExcelFormField(
            'L10', int,
            EpidemiologyR._meta.get_field('meningitis_death').verbose_name),
        'rabies_case_1': ExcelFormField(
            'M9', int,
            EpidemiologyR._meta.get_field('rabies_case').verbose_name),
        'rabies_death_1': ExcelFormField(
            'M10', int,
            EpidemiologyR._meta.get_field('rabies_death').verbose_name),
        'acute_measles_diarrhea_case_1': ExcelFormField(
            'N9', int,
            EpidemiologyR._meta.get_field(
                'acute_measles_diarrhea_case').verbose_name),
        'acute_measles_diarrhea_death_1': ExcelFormField(
            'N10', int,
            EpidemiologyR._meta.get_field(
                'acute_measles_diarrhea_death').verbose_name),
        'other_notifiable_disease_case_1': ExcelFormField(
            'O9', int,
            EpidemiologyR._meta.get_field(
                'other_notifiable_disease_case').verbose_name),
        'other_notifiable_disease_death_1': ExcelFormField(
            'O10', int,
            EpidemiologyR._meta.get_field(
                'other_notifiable_disease_death').verbose_name),

        # line 2
        'snisi_code_2': ExcelFormField('A9', text_type, _("Health Center")),
        'ebola_case_2': ExcelFormField(
            'D9', int,
            EpidemiologyR._meta.get_field('ebola_case').verbose_name),
        'ebola_death_2': ExcelFormField(
            'D10', int,
            EpidemiologyR._meta.get_field('ebola_death').verbose_name),
        'acute_flaccid_paralysis_case_2': ExcelFormField(
            'E9', int,
            EpidemiologyR._meta.get_field(
                'acute_flaccid_paralysis_case').verbose_name),
        'acute_flaccid_paralysis_death_2': ExcelFormField(
            'E10', int,
            EpidemiologyR._meta.get_field(
                'acute_flaccid_paralysis_death').verbose_name),
        'influenza_a_h1n1_case_2': ExcelFormField(
            'F9', int,
            EpidemiologyR._meta.get_field(
                'influenza_a_h1n1_case').verbose_name),
        'influenza_a_h1n1_death_2': ExcelFormField(
            'F10', int,
            EpidemiologyR._meta.get_field(
                'influenza_a_h1n1_death').verbose_name),
        'cholera_case_2': ExcelFormField(
            'G9', int,
            EpidemiologyR._meta.get_field('cholera_case').verbose_name),
        'cholera_death_2': ExcelFormField(
            'G10', int,
            EpidemiologyR._meta.get_field('cholera_death').verbose_name),
        'red_diarrhea_case_2': ExcelFormField(
            'H9', int,
            EpidemiologyR._meta.get_field('red_diarrhea_case').verbose_name),
        'red_diarrhea_death_2': ExcelFormField(
            'H10', int,
            EpidemiologyR._meta.get_field('red_diarrhea_death').verbose_name),
        'measles_case_2': ExcelFormField(
            'I9', int,
            EpidemiologyR._meta.get_field('measles_case').verbose_name),
        'measles_death_2': ExcelFormField(
            'I10', int,
            EpidemiologyR._meta.get_field('measles_death').verbose_name),
        'yellow_fever_case_2': ExcelFormField(
            'J9', int,
            EpidemiologyR._meta.get_field('yellow_fever_case').verbose_name),
        'yellow_fever_death_2': ExcelFormField(
            'J10', int,
            EpidemiologyR._meta.get_field('yellow_fever_death').verbose_name),
        'neonatal_tetanus_case_2': ExcelFormField(
            'K9', int,
            EpidemiologyR._meta.get_field(
                'neonatal_tetanus_case').verbose_name),
        'neonatal_tetanus_death_2': ExcelFormField(
            'K10', int,
            EpidemiologyR._meta.get_field(
                'neonatal_tetanus_death').verbose_name),
        'meningitis_case_2': ExcelFormField(
            'L9', int,
            EpidemiologyR._meta.get_field('meningitis_case').verbose_name),
        'meningitis_death_2': ExcelFormField(
            'L10', int,
            EpidemiologyR._meta.get_field('meningitis_death').verbose_name),
        'rabies_case_2': ExcelFormField(
            'M9', int,
            EpidemiologyR._meta.get_field('rabies_case').verbose_name),
        'rabies_death_2': ExcelFormField(
            'M10', int,
            EpidemiologyR._meta.get_field('rabies_death').verbose_name),
        'acute_measles_diarrhea_case_2': ExcelFormField(
            'N9', int,
            EpidemiologyR._meta.get_field(
                'acute_measles_diarrhea_case').verbose_name),
        'acute_measles_diarrhea_death_2': ExcelFormField(
            'N10', int,
            EpidemiologyR._meta.get_field(
                'acute_measles_diarrhea_death').verbose_name),
        'other_notifiable_disease_case_2': ExcelFormField(
            'O9', int,
            EpidemiologyR._meta.get_field(
                'other_notifiable_disease_case').verbose_name),
        'other_notifiable_disease_death_2': ExcelFormField(
            'O10', int,
            EpidemiologyR._meta.get_field(
                'other_notifiable_disease_death').verbose_name),

        # line 3
        'snisi_code_3': ExcelFormField('A9', text_type, _("Health Center")),
        'ebola_case_3': ExcelFormField(
            'D9', int,
            EpidemiologyR._meta.get_field('ebola_case').verbose_name),
        'ebola_death_3': ExcelFormField(
            'D10', int,
            EpidemiologyR._meta.get_field('ebola_death').verbose_name),
        'acute_flaccid_paralysis_case_3': ExcelFormField(
            'E9', int,
            EpidemiologyR._meta.get_field(
                'acute_flaccid_paralysis_case').verbose_name),
        'acute_flaccid_paralysis_death_3': ExcelFormField(
            'E10', int,
            EpidemiologyR._meta.get_field(
                'acute_flaccid_paralysis_death').verbose_name),
        'influenza_a_h1n1_case_3': ExcelFormField(
            'F9', int,
            EpidemiologyR._meta.get_field(
                'influenza_a_h1n1_case').verbose_name),
        'influenza_a_h1n1_death_3': ExcelFormField(
            'F10', int,
            EpidemiologyR._meta.get_field(
                'influenza_a_h1n1_death').verbose_name),
        'cholera_case_3': ExcelFormField(
            'G9', int,
            EpidemiologyR._meta.get_field('cholera_case').verbose_name),
        'cholera_death_3': ExcelFormField(
            'G10', int,
            EpidemiologyR._meta.get_field('cholera_death').verbose_name),
        'red_diarrhea_case_3': ExcelFormField(
            'H9', int,
            EpidemiologyR._meta.get_field('red_diarrhea_case').verbose_name),
        'red_diarrhea_death_3': ExcelFormField(
            'H10', int,
            EpidemiologyR._meta.get_field('red_diarrhea_death').verbose_name),
        'measles_case_3': ExcelFormField(
            'I9', int,
            EpidemiologyR._meta.get_field('measles_case').verbose_name),
        'measles_death_3': ExcelFormField(
            'I10', int,
            EpidemiologyR._meta.get_field('measles_death').verbose_name),
        'yellow_fever_case_3': ExcelFormField(
            'J9', int,
            EpidemiologyR._meta.get_field('yellow_fever_case').verbose_name),
        'yellow_fever_death_3': ExcelFormField(
            'J10', int,
            EpidemiologyR._meta.get_field('yellow_fever_death').verbose_name),
        'neonatal_tetanus_case_3': ExcelFormField(
            'K9', int,
            EpidemiologyR._meta.get_field(
                'neonatal_tetanus_case').verbose_name),
        'neonatal_tetanus_death_3': ExcelFormField(
            'K10', int,
            EpidemiologyR._meta.get_field(
                'neonatal_tetanus_death').verbose_name),
        'meningitis_case_3': ExcelFormField(
            'L9', int,
            EpidemiologyR._meta.get_field('meningitis_case').verbose_name),
        'meningitis_death_3': ExcelFormField(
            'L10', int,
            EpidemiologyR._meta.get_field('meningitis_death').verbose_name),
        'rabies_case_3': ExcelFormField(
            'M9', int,
            EpidemiologyR._meta.get_field('rabies_case').verbose_name),
        'rabies_death_3': ExcelFormField(
            'M10', int,
            EpidemiologyR._meta.get_field('rabies_death').verbose_name),
        'acute_measles_diarrhea_case_3': ExcelFormField(
            'N9', int,
            EpidemiologyR._meta.get_field(
                'acute_measles_diarrhea_case').verbose_name),
        'acute_measles_diarrhea_death_3': ExcelFormField(
            'N10', int,
            EpidemiologyR._meta.get_field(
                'acute_measles_diarrhea_death').verbose_name),
        'other_notifiable_disease_case_3': ExcelFormField(
            'O9', int,
            EpidemiologyR._meta.get_field(
                'other_notifiable_disease_case').verbose_name),
        'other_notifiable_disease_death_3': ExcelFormField(
            'O10', int,
            EpidemiologyR._meta.get_field(
                'other_notifiable_disease_death').verbose_name),

        # line 4
        'snisi_code_4': ExcelFormField('A9', text_type, _("Health Center")),
        'ebola_case_4': ExcelFormField(
            'D9', int,
            EpidemiologyR._meta.get_field('ebola_case').verbose_name),
        'ebola_death_4': ExcelFormField(
            'D10', int,
            EpidemiologyR._meta.get_field('ebola_death').verbose_name),
        'acute_flaccid_paralysis_case_4': ExcelFormField(
            'E9', int,
            EpidemiologyR._meta.get_field(
                'acute_flaccid_paralysis_case').verbose_name),
        'acute_flaccid_paralysis_death_4': ExcelFormField(
            'E10', int,
            EpidemiologyR._meta.get_field(
                'acute_flaccid_paralysis_death').verbose_name),
        'influenza_a_h1n1_case_4': ExcelFormField(
            'F9', int,
            EpidemiologyR._meta.get_field(
                'influenza_a_h1n1_case').verbose_name),
        'influenza_a_h1n1_death_4': ExcelFormField(
            'F10', int,
            EpidemiologyR._meta.get_field(
                'influenza_a_h1n1_death').verbose_name),
        'cholera_case_4': ExcelFormField(
            'G9', int,
            EpidemiologyR._meta.get_field('cholera_case').verbose_name),
        'cholera_death_4': ExcelFormField(
            'G10', int,
            EpidemiologyR._meta.get_field('cholera_death').verbose_name),
        'red_diarrhea_case_4': ExcelFormField(
            'H9', int,
            EpidemiologyR._meta.get_field('red_diarrhea_case').verbose_name),
        'red_diarrhea_death_4': ExcelFormField(
            'H10', int,
            EpidemiologyR._meta.get_field('red_diarrhea_death').verbose_name),
        'measles_case_4': ExcelFormField(
            'I9', int,
            EpidemiologyR._meta.get_field('measles_case').verbose_name),
        'measles_death_4': ExcelFormField(
            'I10', int,
            EpidemiologyR._meta.get_field('measles_death').verbose_name),
        'yellow_fever_case_4': ExcelFormField(
            'J9', int,
            EpidemiologyR._meta.get_field('yellow_fever_case').verbose_name),
        'yellow_fever_death_4': ExcelFormField(
            'J10', int,
            EpidemiologyR._meta.get_field('yellow_fever_death').verbose_name),
        'neonatal_tetanus_case_4': ExcelFormField(
            'K9', int,
            EpidemiologyR._meta.get_field(
                'neonatal_tetanus_case').verbose_name),
        'neonatal_tetanus_death_4': ExcelFormField(
            'K10', int,
            EpidemiologyR._meta.get_field(
                'neonatal_tetanus_death').verbose_name),
        'meningitis_case_4': ExcelFormField(
            'L9', int,
            EpidemiologyR._meta.get_field('meningitis_case').verbose_name),
        'meningitis_death_4': ExcelFormField(
            'L10', int,
            EpidemiologyR._meta.get_field('meningitis_death').verbose_name),
        'rabies_case_4': ExcelFormField(
            'M9', int,
            EpidemiologyR._meta.get_field('rabies_case').verbose_name),
        'rabies_death_4': ExcelFormField(
            'M10', int,
            EpidemiologyR._meta.get_field('rabies_death').verbose_name),
        'acute_measles_diarrhea_case_4': ExcelFormField(
            'N9', int,
            EpidemiologyR._meta.get_field(
                'acute_measles_diarrhea_case').verbose_name),
        'acute_measles_diarrhea_death_4': ExcelFormField(
            'N10', int,
            EpidemiologyR._meta.get_field(
                'acute_measles_diarrhea_death').verbose_name),
        'other_notifiable_disease_case_4': ExcelFormField(
            'O9', int,
            EpidemiologyR._meta.get_field(
                'other_notifiable_disease_case').verbose_name),
        'other_notifiable_disease_death_4': ExcelFormField(
            'O10', int,
            EpidemiologyR._meta.get_field(
                'other_notifiable_disease_death').verbose_name),

        # line 5
        'snisi_code_5': ExcelFormField('A9', text_type, _("Health Center")),
        'ebola_case_5': ExcelFormField(
            'D9', int,
            EpidemiologyR._meta.get_field('ebola_case').verbose_name),
        'ebola_death_5': ExcelFormField(
            'D10', int,
            EpidemiologyR._meta.get_field('ebola_death').verbose_name),
        'acute_flaccid_paralysis_case_5': ExcelFormField(
            'E9', int,
            EpidemiologyR._meta.get_field(
                'acute_flaccid_paralysis_case').verbose_name),
        'acute_flaccid_paralysis_death_5': ExcelFormField(
            'E10', int,
            EpidemiologyR._meta.get_field(
                'acute_flaccid_paralysis_death').verbose_name),
        'influenza_a_h1n1_case_5': ExcelFormField(
            'F9', int,
            EpidemiologyR._meta.get_field(
                'influenza_a_h1n1_case').verbose_name),
        'influenza_a_h1n1_death_5': ExcelFormField(
            'F10', int,
            EpidemiologyR._meta.get_field(
                'influenza_a_h1n1_death').verbose_name),
        'cholera_case_5': ExcelFormField(
            'G9', int,
            EpidemiologyR._meta.get_field('cholera_case').verbose_name),
        'cholera_death_5': ExcelFormField(
            'G10', int,
            EpidemiologyR._meta.get_field('cholera_death').verbose_name),
        'red_diarrhea_case_5': ExcelFormField(
            'H9', int,
            EpidemiologyR._meta.get_field('red_diarrhea_case').verbose_name),
        'red_diarrhea_death_5': ExcelFormField(
            'H10', int,
            EpidemiologyR._meta.get_field('red_diarrhea_death').verbose_name),
        'measles_case_5': ExcelFormField(
            'I9', int,
            EpidemiologyR._meta.get_field('measles_case').verbose_name),
        'measles_death_5': ExcelFormField(
            'I10', int,
            EpidemiologyR._meta.get_field('measles_death').verbose_name),
        'yellow_fever_case_5': ExcelFormField(
            'J9', int,
            EpidemiologyR._meta.get_field('yellow_fever_case').verbose_name),
        'yellow_fever_death_5': ExcelFormField(
            'J10', int,
            EpidemiologyR._meta.get_field('yellow_fever_death').verbose_name),
        'neonatal_tetanus_case_5': ExcelFormField(
            'K9', int,
            EpidemiologyR._meta.get_field(
                'neonatal_tetanus_case').verbose_name),
        'neonatal_tetanus_death_5': ExcelFormField(
            'K10', int,
            EpidemiologyR._meta.get_field(
                'neonatal_tetanus_death').verbose_name),
        'meningitis_case_5': ExcelFormField(
            'L9', int,
            EpidemiologyR._meta.get_field('meningitis_case').verbose_name),
        'meningitis_death_5': ExcelFormField(
            'L10', int,
            EpidemiologyR._meta.get_field('meningitis_death').verbose_name),
        'rabies_case_5': ExcelFormField(
            'M9', int,
            EpidemiologyR._meta.get_field('rabies_case').verbose_name),
        'rabies_death_5': ExcelFormField(
            'M10', int,
            EpidemiologyR._meta.get_field('rabies_death').verbose_name),
        'acute_measles_diarrhea_case_5': ExcelFormField(
            'N9', int,
            EpidemiologyR._meta.get_field(
                'acute_measles_diarrhea_case').verbose_name),
        'acute_measles_diarrhea_death_5': ExcelFormField(
            'N10', int,
            EpidemiologyR._meta.get_field(
                'acute_measles_diarrhea_death').verbose_name),
        'other_notifiable_disease_case_5': ExcelFormField(
            'O9', int,
            EpidemiologyR._meta.get_field(
                'other_notifiable_disease_case').verbose_name),
        'other_notifiable_disease_death_5': ExcelFormField(
            'O10', int,
            EpidemiologyR._meta.get_field(
                'other_notifiable_disease_death').verbose_name),

        # line 6
        'snisi_code_6': ExcelFormField('A9', text_type, _("Health Center")),
        'ebola_case_6': ExcelFormField(
            'D9', int,
            EpidemiologyR._meta.get_field('ebola_case').verbose_name),
        'ebola_death_6': ExcelFormField(
            'D10', int,
            EpidemiologyR._meta.get_field('ebola_death').verbose_name),
        'acute_flaccid_paralysis_case_6': ExcelFormField(
            'E9', int,
            EpidemiologyR._meta.get_field(
                'acute_flaccid_paralysis_case').verbose_name),
        'acute_flaccid_paralysis_death_6': ExcelFormField(
            'E10', int,
            EpidemiologyR._meta.get_field(
                'acute_flaccid_paralysis_death').verbose_name),
        'influenza_a_h1n1_case_6': ExcelFormField(
            'F9', int,
            EpidemiologyR._meta.get_field(
                'influenza_a_h1n1_case').verbose_name),
        'influenza_a_h1n1_death_6': ExcelFormField(
            'F10', int,
            EpidemiologyR._meta.get_field(
                'influenza_a_h1n1_death').verbose_name),
        'cholera_case_6': ExcelFormField(
            'G9', int,
            EpidemiologyR._meta.get_field('cholera_case').verbose_name),
        'cholera_death_6': ExcelFormField(
            'G10', int,
            EpidemiologyR._meta.get_field('cholera_death').verbose_name),
        'red_diarrhea_case_6': ExcelFormField(
            'H9', int,
            EpidemiologyR._meta.get_field('red_diarrhea_case').verbose_name),
        'red_diarrhea_death_6': ExcelFormField(
            'H10', int,
            EpidemiologyR._meta.get_field('red_diarrhea_death').verbose_name),
        'measles_case_6': ExcelFormField(
            'I9', int,
            EpidemiologyR._meta.get_field('measles_case').verbose_name),
        'measles_death_6': ExcelFormField(
            'I10', int,
            EpidemiologyR._meta.get_field('measles_death').verbose_name),
        'yellow_fever_case_6': ExcelFormField(
            'J9', int,
            EpidemiologyR._meta.get_field('yellow_fever_case').verbose_name),
        'yellow_fever_death_6': ExcelFormField(
            'J10', int,
            EpidemiologyR._meta.get_field('yellow_fever_death').verbose_name),
        'neonatal_tetanus_case_6': ExcelFormField(
            'K9', int,
            EpidemiologyR._meta.get_field(
                'neonatal_tetanus_case').verbose_name),
        'neonatal_tetanus_death_6': ExcelFormField(
            'K10', int,
            EpidemiologyR._meta.get_field(
                'neonatal_tetanus_death').verbose_name),
        'meningitis_case_6': ExcelFormField(
            'L9', int,
            EpidemiologyR._meta.get_field('meningitis_case').verbose_name),
        'meningitis_death_6': ExcelFormField(
            'L10', int,
            EpidemiologyR._meta.get_field('meningitis_death').verbose_name),
        'rabies_case_6': ExcelFormField(
            'M9', int,
            EpidemiologyR._meta.get_field('rabies_case').verbose_name),
        'rabies_death_6': ExcelFormField(
            'M10', int,
            EpidemiologyR._meta.get_field('rabies_death').verbose_name),
        'acute_measles_diarrhea_case_6': ExcelFormField(
            'N9', int,
            EpidemiologyR._meta.get_field(
                'acute_measles_diarrhea_case').verbose_name),
        'acute_measles_diarrhea_death_6': ExcelFormField(
            'N10', int,
            EpidemiologyR._meta.get_field(
                'acute_measles_diarrhea_death').verbose_name),
        'other_notifiable_disease_case_6': ExcelFormField(
            'O9', int,
            EpidemiologyR._meta.get_field(
                'other_notifiable_disease_case').verbose_name),
        'other_notifiable_disease_death_6': ExcelFormField(
            'O10', int,
            EpidemiologyR._meta.get_field(
                'other_notifiable_disease_death').verbose_name),

        # line 7
        'snisi_code_7': ExcelFormField('A9', text_type, _("Health Center")),
        'ebola_case_7': ExcelFormField(
            'D9', int,
            EpidemiologyR._meta.get_field('ebola_case').verbose_name),
        'ebola_death_7': ExcelFormField(
            'D10', int,
            EpidemiologyR._meta.get_field('ebola_death').verbose_name),
        'acute_flaccid_paralysis_case_7': ExcelFormField(
            'E9', int,
            EpidemiologyR._meta.get_field(
                'acute_flaccid_paralysis_case').verbose_name),
        'acute_flaccid_paralysis_death_7': ExcelFormField(
            'E10', int,
            EpidemiologyR._meta.get_field(
                'acute_flaccid_paralysis_death').verbose_name),
        'influenza_a_h1n1_case_7': ExcelFormField(
            'F9', int,
            EpidemiologyR._meta.get_field(
                'influenza_a_h1n1_case').verbose_name),
        'influenza_a_h1n1_death_7': ExcelFormField(
            'F10', int,
            EpidemiologyR._meta.get_field(
                'influenza_a_h1n1_death').verbose_name),
        'cholera_case_7': ExcelFormField(
            'G9', int,
            EpidemiologyR._meta.get_field('cholera_case').verbose_name),
        'cholera_death_7': ExcelFormField(
            'G10', int,
            EpidemiologyR._meta.get_field('cholera_death').verbose_name),
        'red_diarrhea_case_7': ExcelFormField(
            'H9', int,
            EpidemiologyR._meta.get_field('red_diarrhea_case').verbose_name),
        'red_diarrhea_death_7': ExcelFormField(
            'H10', int,
            EpidemiologyR._meta.get_field('red_diarrhea_death').verbose_name),
        'measles_case_7': ExcelFormField(
            'I9', int,
            EpidemiologyR._meta.get_field('measles_case').verbose_name),
        'measles_death_7': ExcelFormField(
            'I10', int,
            EpidemiologyR._meta.get_field('measles_death').verbose_name),
        'yellow_fever_case_7': ExcelFormField(
            'J9', int,
            EpidemiologyR._meta.get_field('yellow_fever_case').verbose_name),
        'yellow_fever_death_7': ExcelFormField(
            'J10', int,
            EpidemiologyR._meta.get_field('yellow_fever_death').verbose_name),
        'neonatal_tetanus_case_7': ExcelFormField(
            'K9', int,
            EpidemiologyR._meta.get_field(
                'neonatal_tetanus_case').verbose_name),
        'neonatal_tetanus_death_7': ExcelFormField(
            'K10', int,
            EpidemiologyR._meta.get_field(
                'neonatal_tetanus_death').verbose_name),
        'meningitis_case_7': ExcelFormField(
            'L9', int,
            EpidemiologyR._meta.get_field('meningitis_case').verbose_name),
        'meningitis_death_7': ExcelFormField(
            'L10', int,
            EpidemiologyR._meta.get_field('meningitis_death').verbose_name),
        'rabies_case_7': ExcelFormField(
            'M9', int,
            EpidemiologyR._meta.get_field('rabies_case').verbose_name),
        'rabies_death_7': ExcelFormField(
            'M10', int,
            EpidemiologyR._meta.get_field('rabies_death').verbose_name),
        'acute_measles_diarrhea_case_7': ExcelFormField(
            'N9', int,
            EpidemiologyR._meta.get_field(
                'acute_measles_diarrhea_case').verbose_name),
        'acute_measles_diarrhea_death_7': ExcelFormField(
            'N10', int,
            EpidemiologyR._meta.get_field(
                'acute_measles_diarrhea_death').verbose_name),
        'other_notifiable_disease_case_7': ExcelFormField(
            'O9', int,
            EpidemiologyR._meta.get_field(
                'other_notifiable_disease_case').verbose_name),
        'other_notifiable_disease_death_7': ExcelFormField(
            'O10', int,
            EpidemiologyR._meta.get_field(
                'other_notifiable_disease_death').verbose_name),

        # line 8
        'snisi_code_8': ExcelFormField('A9', text_type, _("Health Center")),
        'ebola_case_8': ExcelFormField(
            'D9', int,
            EpidemiologyR._meta.get_field('ebola_case').verbose_name),
        'ebola_death_8': ExcelFormField(
            'D10', int,
            EpidemiologyR._meta.get_field('ebola_death').verbose_name),
        'acute_flaccid_paralysis_case_8': ExcelFormField(
            'E9', int,
            EpidemiologyR._meta.get_field(
                'acute_flaccid_paralysis_case').verbose_name),
        'acute_flaccid_paralysis_death_8': ExcelFormField(
            'E10', int,
            EpidemiologyR._meta.get_field(
                'acute_flaccid_paralysis_death').verbose_name),
        'influenza_a_h1n1_case_8': ExcelFormField(
            'F9', int,
            EpidemiologyR._meta.get_field(
                'influenza_a_h1n1_case').verbose_name),
        'influenza_a_h1n1_death_8': ExcelFormField(
            'F10', int,
            EpidemiologyR._meta.get_field(
                'influenza_a_h1n1_death').verbose_name),
        'cholera_case_8': ExcelFormField(
            'G9', int,
            EpidemiologyR._meta.get_field('cholera_case').verbose_name),
        'cholera_death_8': ExcelFormField(
            'G10', int,
            EpidemiologyR._meta.get_field('cholera_death').verbose_name),
        'red_diarrhea_case_8': ExcelFormField(
            'H9', int,
            EpidemiologyR._meta.get_field('red_diarrhea_case').verbose_name),
        'red_diarrhea_death_8': ExcelFormField(
            'H10', int,
            EpidemiologyR._meta.get_field('red_diarrhea_death').verbose_name),
        'measles_case_8': ExcelFormField(
            'I9', int,
            EpidemiologyR._meta.get_field('measles_case').verbose_name),
        'measles_death_8': ExcelFormField(
            'I10', int,
            EpidemiologyR._meta.get_field('measles_death').verbose_name),
        'yellow_fever_case_8': ExcelFormField(
            'J9', int,
            EpidemiologyR._meta.get_field('yellow_fever_case').verbose_name),
        'yellow_fever_death_8': ExcelFormField(
            'J10', int,
            EpidemiologyR._meta.get_field('yellow_fever_death').verbose_name),
        'neonatal_tetanus_case_8': ExcelFormField(
            'K9', int,
            EpidemiologyR._meta.get_field(
                'neonatal_tetanus_case').verbose_name),
        'neonatal_tetanus_death_8': ExcelFormField(
            'K10', int,
            EpidemiologyR._meta.get_field(
                'neonatal_tetanus_death').verbose_name),
        'meningitis_case_8': ExcelFormField(
            'L9', int,
            EpidemiologyR._meta.get_field('meningitis_case').verbose_name),
        'meningitis_death_8': ExcelFormField(
            'L10', int,
            EpidemiologyR._meta.get_field('meningitis_death').verbose_name),
        'rabies_case_8': ExcelFormField(
            'M9', int,
            EpidemiologyR._meta.get_field('rabies_case').verbose_name),
        'rabies_death_8': ExcelFormField(
            'M10', int,
            EpidemiologyR._meta.get_field('rabies_death').verbose_name),
        'acute_measles_diarrhea_case_8': ExcelFormField(
            'N9', int,
            EpidemiologyR._meta.get_field(
                'acute_measles_diarrhea_case').verbose_name),
        'acute_measles_diarrhea_death_8': ExcelFormField(
            'N10', int,
            EpidemiologyR._meta.get_field(
                'acute_measles_diarrhea_death').verbose_name),
        'other_notifiable_disease_case_8': ExcelFormField(
            'O9', int,
            EpidemiologyR._meta.get_field(
                'other_notifiable_disease_case').verbose_name),
        'other_notifiable_disease_death_8': ExcelFormField(
            'O10', int,
            EpidemiologyR._meta.get_field(
                'other_notifiable_disease_death').verbose_name),

        # line 9
        'snisi_code_9': ExcelFormField('A9', text_type, _("Health Center")),
        'ebola_case_9': ExcelFormField(
            'D9', int,
            EpidemiologyR._meta.get_field('ebola_case').verbose_name),
        'ebola_death_9': ExcelFormField(
            'D10', int,
            EpidemiologyR._meta.get_field('ebola_death').verbose_name),
        'acute_flaccid_paralysis_case_9': ExcelFormField(
            'E9', int,
            EpidemiologyR._meta.get_field(
                'acute_flaccid_paralysis_case').verbose_name),
        'acute_flaccid_paralysis_death_9': ExcelFormField(
            'E10', int,
            EpidemiologyR._meta.get_field(
                'acute_flaccid_paralysis_death').verbose_name),
        'influenza_a_h1n1_case_9': ExcelFormField(
            'F9', int,
            EpidemiologyR._meta.get_field(
                'influenza_a_h1n1_case').verbose_name),
        'influenza_a_h1n1_death_9': ExcelFormField(
            'F10', int,
            EpidemiologyR._meta.get_field(
                'influenza_a_h1n1_death').verbose_name),
        'cholera_case_9': ExcelFormField(
            'G9', int,
            EpidemiologyR._meta.get_field('cholera_case').verbose_name),
        'cholera_death_9': ExcelFormField(
            'G10', int,
            EpidemiologyR._meta.get_field('cholera_death').verbose_name),
        'red_diarrhea_case_9': ExcelFormField(
            'H9', int,
            EpidemiologyR._meta.get_field('red_diarrhea_case').verbose_name),
        'red_diarrhea_death_9': ExcelFormField(
            'H10', int,
            EpidemiologyR._meta.get_field('red_diarrhea_death').verbose_name),
        'measles_case_9': ExcelFormField(
            'I9', int,
            EpidemiologyR._meta.get_field('measles_case').verbose_name),
        'measles_death_9': ExcelFormField(
            'I10', int,
            EpidemiologyR._meta.get_field('measles_death').verbose_name),
        'yellow_fever_case_9': ExcelFormField(
            'J9', int,
            EpidemiologyR._meta.get_field('yellow_fever_case').verbose_name),
        'yellow_fever_death_9': ExcelFormField(
            'J10', int,
            EpidemiologyR._meta.get_field('yellow_fever_death').verbose_name),
        'neonatal_tetanus_case_9': ExcelFormField(
            'K9', int,
            EpidemiologyR._meta.get_field(
                'neonatal_tetanus_case').verbose_name),
        'neonatal_tetanus_death_9': ExcelFormField(
            'K10', int,
            EpidemiologyR._meta.get_field(
                'neonatal_tetanus_death').verbose_name),
        'meningitis_case_9': ExcelFormField(
            'L9', int,
            EpidemiologyR._meta.get_field('meningitis_case').verbose_name),
        'meningitis_death_9': ExcelFormField(
            'L10', int,
            EpidemiologyR._meta.get_field('meningitis_death').verbose_name),
        'rabies_case_9': ExcelFormField(
            'M9', int,
            EpidemiologyR._meta.get_field('rabies_case').verbose_name),
        'rabies_death_9': ExcelFormField(
            'M10', int,
            EpidemiologyR._meta.get_field('rabies_death').verbose_name),
        'acute_measles_diarrhea_case_9': ExcelFormField(
            'N9', int,
            EpidemiologyR._meta.get_field(
                'acute_measles_diarrhea_case').verbose_name),
        'acute_measles_diarrhea_death_9': ExcelFormField(
            'N10', int,
            EpidemiologyR._meta.get_field(
                'acute_measles_diarrhea_death').verbose_name),
        'other_notifiable_disease_case_9': ExcelFormField(
            'O9', int,
            EpidemiologyR._meta.get_field(
                'other_notifiable_disease_case').verbose_name),
        'other_notifiable_disease_death_9': ExcelFormField(
            'O10', int,
            EpidemiologyR._meta.get_field(
                'other_notifiable_disease_death').verbose_name),

        # line 10
        'snisi_code_10': ExcelFormField('A9', text_type, _("Health Center")),
        'ebola_case_10': ExcelFormField(
            'D9', int,
            EpidemiologyR._meta.get_field('ebola_case').verbose_name),
        'ebola_death_10': ExcelFormField(
            'D10', int,
            EpidemiologyR._meta.get_field('ebola_death').verbose_name),
        'acute_flaccid_paralysis_case_10': ExcelFormField(
            'E9', int,
            EpidemiologyR._meta.get_field(
                'acute_flaccid_paralysis_case').verbose_name),
        'acute_flaccid_paralysis_death_10': ExcelFormField(
            'E10', int,
            EpidemiologyR._meta.get_field(
                'acute_flaccid_paralysis_death').verbose_name),
        'influenza_a_h1n1_case_10': ExcelFormField(
            'F9', int,
            EpidemiologyR._meta.get_field(
                'influenza_a_h1n1_case').verbose_name),
        'influenza_a_h1n1_death_10': ExcelFormField(
            'F10', int,
            EpidemiologyR._meta.get_field(
                'influenza_a_h1n1_death').verbose_name),
        'cholera_case_10': ExcelFormField(
            'G9', int,
            EpidemiologyR._meta.get_field('cholera_case').verbose_name),
        'cholera_death_10': ExcelFormField(
            'G10', int,
            EpidemiologyR._meta.get_field('cholera_death').verbose_name),
        'red_diarrhea_case_10': ExcelFormField(
            'H9', int,
            EpidemiologyR._meta.get_field('red_diarrhea_case').verbose_name),
        'red_diarrhea_death_10': ExcelFormField(
            'H10', int,
            EpidemiologyR._meta.get_field('red_diarrhea_death').verbose_name),
        'measles_case_10': ExcelFormField(
            'I9', int,
            EpidemiologyR._meta.get_field('measles_case').verbose_name),
        'measles_death_10': ExcelFormField(
            'I10', int,
            EpidemiologyR._meta.get_field('measles_death').verbose_name),
        'yellow_fever_case_10': ExcelFormField(
            'J9', int,
            EpidemiologyR._meta.get_field('yellow_fever_case').verbose_name),
        'yellow_fever_death_10': ExcelFormField(
            'J10', int,
            EpidemiologyR._meta.get_field('yellow_fever_death').verbose_name),
        'neonatal_tetanus_case_10': ExcelFormField(
            'K9', int,
            EpidemiologyR._meta.get_field(
                'neonatal_tetanus_case').verbose_name),
        'neonatal_tetanus_death_10': ExcelFormField(
            'K10', int,
            EpidemiologyR._meta.get_field(
                'neonatal_tetanus_death').verbose_name),
        'meningitis_case_10': ExcelFormField(
            'L9', int,
            EpidemiologyR._meta.get_field('meningitis_case').verbose_name),
        'meningitis_death_10': ExcelFormField(
            'L10', int,
            EpidemiologyR._meta.get_field('meningitis_death').verbose_name),
        'rabies_case_10': ExcelFormField(
            'M9', int,
            EpidemiologyR._meta.get_field('rabies_case').verbose_name),
        'rabies_death_10': ExcelFormField(
            'M10', int,
            EpidemiologyR._meta.get_field('rabies_death').verbose_name),
        'acute_measles_diarrhea_case_10': ExcelFormField(
            'N9', int,
            EpidemiologyR._meta.get_field(
                'acute_measles_diarrhea_case').verbose_name),
        'acute_measles_diarrhea_death_10': ExcelFormField(
            'N10', int,
            EpidemiologyR._meta.get_field(
                'acute_measles_diarrhea_death').verbose_name),
        'other_notifiable_disease_case_10': ExcelFormField(
            'O9', int,
            EpidemiologyR._meta.get_field(
                'other_notifiable_disease_case').verbose_name),
        'other_notifiable_disease_death_10': ExcelFormField(
            'O10', int,
            EpidemiologyR._meta.get_field(
                'other_notifiable_disease_death').verbose_name),

        # line 11
        'snisi_code_11': ExcelFormField('A9', text_type, _("Health Center")),
        'ebola_case_11': ExcelFormField(
            'D9', int,
            EpidemiologyR._meta.get_field('ebola_case').verbose_name),
        'ebola_death_11': ExcelFormField(
            'D10', int,
            EpidemiologyR._meta.get_field('ebola_death').verbose_name),
        'acute_flaccid_paralysis_case_11': ExcelFormField(
            'E9', int,
            EpidemiologyR._meta.get_field(
                'acute_flaccid_paralysis_case').verbose_name),
        'acute_flaccid_paralysis_death_11': ExcelFormField(
            'E10', int,
            EpidemiologyR._meta.get_field(
                'acute_flaccid_paralysis_death').verbose_name),
        'influenza_a_h1n1_case_11': ExcelFormField(
            'F9', int,
            EpidemiologyR._meta.get_field(
                'influenza_a_h1n1_case').verbose_name),
        'influenza_a_h1n1_death_11': ExcelFormField(
            'F10', int,
            EpidemiologyR._meta.get_field(
                'influenza_a_h1n1_death').verbose_name),
        'cholera_case_11': ExcelFormField(
            'G9', int,
            EpidemiologyR._meta.get_field('cholera_case').verbose_name),
        'cholera_death_11': ExcelFormField(
            'G10', int,
            EpidemiologyR._meta.get_field('cholera_death').verbose_name),
        'red_diarrhea_case_11': ExcelFormField(
            'H9', int,
            EpidemiologyR._meta.get_field('red_diarrhea_case').verbose_name),
        'red_diarrhea_death_11': ExcelFormField(
            'H10', int,
            EpidemiologyR._meta.get_field('red_diarrhea_death').verbose_name),
        'measles_case_11': ExcelFormField(
            'I9', int,
            EpidemiologyR._meta.get_field('measles_case').verbose_name),
        'measles_death_11': ExcelFormField(
            'I10', int,
            EpidemiologyR._meta.get_field('measles_death').verbose_name),
        'yellow_fever_case_11': ExcelFormField(
            'J9', int,
            EpidemiologyR._meta.get_field('yellow_fever_case').verbose_name),
        'yellow_fever_death_11': ExcelFormField(
            'J10', int,
            EpidemiologyR._meta.get_field('yellow_fever_death').verbose_name),
        'neonatal_tetanus_case_11': ExcelFormField(
            'K9', int,
            EpidemiologyR._meta.get_field(
                'neonatal_tetanus_case').verbose_name),
        'neonatal_tetanus_death_11': ExcelFormField(
            'K10', int,
            EpidemiologyR._meta.get_field(
                'neonatal_tetanus_death').verbose_name),
        'meningitis_case_11': ExcelFormField(
            'L9', int,
            EpidemiologyR._meta.get_field('meningitis_case').verbose_name),
        'meningitis_death_11': ExcelFormField(
            'L10', int,
            EpidemiologyR._meta.get_field('meningitis_death').verbose_name),
        'rabies_case_11': ExcelFormField(
            'M9', int,
            EpidemiologyR._meta.get_field('rabies_case').verbose_name),
        'rabies_death_11': ExcelFormField(
            'M10', int,
            EpidemiologyR._meta.get_field('rabies_death').verbose_name),
        'acute_measles_diarrhea_case_11': ExcelFormField(
            'N9', int,
            EpidemiologyR._meta.get_field(
                'acute_measles_diarrhea_case').verbose_name),
        'acute_measles_diarrhea_death_11': ExcelFormField(
            'N10', int,
            EpidemiologyR._meta.get_field(
                'acute_measles_diarrhea_death').verbose_name),
        'other_notifiable_disease_case_11': ExcelFormField(
            'O9', int,
            EpidemiologyR._meta.get_field(
                'other_notifiable_disease_case').verbose_name),
        'other_notifiable_disease_death_11': ExcelFormField(
            'O10', int,
            EpidemiologyR._meta.get_field(
                'other_notifiable_disease_death').verbose_name),

        # line 12
        'snisi_code_12': ExcelFormField('A9', text_type, _("Health Center")),
        'ebola_case_12': ExcelFormField(
            'D9', int,
            EpidemiologyR._meta.get_field('ebola_case').verbose_name),
        'ebola_death_12': ExcelFormField(
            'D10', int,
            EpidemiologyR._meta.get_field('ebola_death').verbose_name),
        'acute_flaccid_paralysis_case_12': ExcelFormField(
            'E9', int,
            EpidemiologyR._meta.get_field(
                'acute_flaccid_paralysis_case').verbose_name),
        'acute_flaccid_paralysis_death_12': ExcelFormField(
            'E10', int,
            EpidemiologyR._meta.get_field(
                'acute_flaccid_paralysis_death').verbose_name),
        'influenza_a_h1n1_case_12': ExcelFormField(
            'F9', int,
            EpidemiologyR._meta.get_field(
                'influenza_a_h1n1_case').verbose_name),
        'influenza_a_h1n1_death_12': ExcelFormField(
            'F10', int,
            EpidemiologyR._meta.get_field(
                'influenza_a_h1n1_death').verbose_name),
        'cholera_case_12': ExcelFormField(
            'G9', int,
            EpidemiologyR._meta.get_field('cholera_case').verbose_name),
        'cholera_death_12': ExcelFormField(
            'G10', int,
            EpidemiologyR._meta.get_field('cholera_death').verbose_name),
        'red_diarrhea_case_12': ExcelFormField(
            'H9', int,
            EpidemiologyR._meta.get_field('red_diarrhea_case').verbose_name),
        'red_diarrhea_death_12': ExcelFormField(
            'H10', int,
            EpidemiologyR._meta.get_field('red_diarrhea_death').verbose_name),
        'measles_case_12': ExcelFormField(
            'I9', int,
            EpidemiologyR._meta.get_field('measles_case').verbose_name),
        'measles_death_12': ExcelFormField(
            'I10', int,
            EpidemiologyR._meta.get_field('measles_death').verbose_name),
        'yellow_fever_case_12': ExcelFormField(
            'J9', int,
            EpidemiologyR._meta.get_field('yellow_fever_case').verbose_name),
        'yellow_fever_death_12': ExcelFormField(
            'J10', int,
            EpidemiologyR._meta.get_field('yellow_fever_death').verbose_name),
        'neonatal_tetanus_case_12': ExcelFormField(
            'K9', int,
            EpidemiologyR._meta.get_field(
                'neonatal_tetanus_case').verbose_name),
        'neonatal_tetanus_death_12': ExcelFormField(
            'K10', int,
            EpidemiologyR._meta.get_field(
                'neonatal_tetanus_death').verbose_name),
        'meningitis_case_12': ExcelFormField(
            'L9', int,
            EpidemiologyR._meta.get_field('meningitis_case').verbose_name),
        'meningitis_death_12': ExcelFormField(
            'L10', int,
            EpidemiologyR._meta.get_field('meningitis_death').verbose_name),
        'rabies_case_12': ExcelFormField(
            'M9', int,
            EpidemiologyR._meta.get_field('rabies_case').verbose_name),
        'rabies_death_12': ExcelFormField(
            'M10', int,
            EpidemiologyR._meta.get_field('rabies_death').verbose_name),
        'acute_measles_diarrhea_case_12': ExcelFormField(
            'N9', int,
            EpidemiologyR._meta.get_field(
                'acute_measles_diarrhea_case').verbose_name),
        'acute_measles_diarrhea_death_12': ExcelFormField(
            'N10', int,
            EpidemiologyR._meta.get_field(
                'acute_measles_diarrhea_death').verbose_name),
        'other_notifiable_disease_case_12': ExcelFormField(
            'O9', int,
            EpidemiologyR._meta.get_field(
                'other_notifiable_disease_case').verbose_name),
        'other_notifiable_disease_death_12': ExcelFormField(
            'O10', int,
            EpidemiologyR._meta.get_field(
                'other_notifiable_disease_death').verbose_name),

        # line 13
        'snisi_code_13': ExcelFormField('A9', text_type, _("Health Center")),
        'ebola_case_13': ExcelFormField(
            'D9', int,
            EpidemiologyR._meta.get_field('ebola_case').verbose_name),
        'ebola_death_13': ExcelFormField(
            'D10', int,
            EpidemiologyR._meta.get_field('ebola_death').verbose_name),
        'acute_flaccid_paralysis_case_13': ExcelFormField(
            'E9', int,
            EpidemiologyR._meta.get_field(
                'acute_flaccid_paralysis_case').verbose_name),
        'acute_flaccid_paralysis_death_13': ExcelFormField(
            'E10', int,
            EpidemiologyR._meta.get_field(
                'acute_flaccid_paralysis_death').verbose_name),
        'influenza_a_h1n1_case_13': ExcelFormField(
            'F9', int,
            EpidemiologyR._meta.get_field(
                'influenza_a_h1n1_case').verbose_name),
        'influenza_a_h1n1_death_13': ExcelFormField(
            'F10', int,
            EpidemiologyR._meta.get_field(
                'influenza_a_h1n1_death').verbose_name),
        'cholera_case_13': ExcelFormField(
            'G9', int,
            EpidemiologyR._meta.get_field('cholera_case').verbose_name),
        'cholera_death_13': ExcelFormField(
            'G10', int,
            EpidemiologyR._meta.get_field('cholera_death').verbose_name),
        'red_diarrhea_case_13': ExcelFormField(
            'H9', int,
            EpidemiologyR._meta.get_field('red_diarrhea_case').verbose_name),
        'red_diarrhea_death_13': ExcelFormField(
            'H10', int,
            EpidemiologyR._meta.get_field('red_diarrhea_death').verbose_name),
        'measles_case_13': ExcelFormField(
            'I9', int,
            EpidemiologyR._meta.get_field('measles_case').verbose_name),
        'measles_death_13': ExcelFormField(
            'I10', int,
            EpidemiologyR._meta.get_field('measles_death').verbose_name),
        'yellow_fever_case_13': ExcelFormField(
            'J9', int,
            EpidemiologyR._meta.get_field('yellow_fever_case').verbose_name),
        'yellow_fever_death_13': ExcelFormField(
            'J10', int,
            EpidemiologyR._meta.get_field('yellow_fever_death').verbose_name),
        'neonatal_tetanus_case_13': ExcelFormField(
            'K9', int,
            EpidemiologyR._meta.get_field(
                'neonatal_tetanus_case').verbose_name),
        'neonatal_tetanus_death_13': ExcelFormField(
            'K10', int,
            EpidemiologyR._meta.get_field(
                'neonatal_tetanus_death').verbose_name),
        'meningitis_case_13': ExcelFormField(
            'L9', int,
            EpidemiologyR._meta.get_field('meningitis_case').verbose_name),
        'meningitis_death_13': ExcelFormField(
            'L10', int,
            EpidemiologyR._meta.get_field('meningitis_death').verbose_name),
        'rabies_case_13': ExcelFormField(
            'M9', int,
            EpidemiologyR._meta.get_field('rabies_case').verbose_name),
        'rabies_death_13': ExcelFormField(
            'M10', int,
            EpidemiologyR._meta.get_field('rabies_death').verbose_name),
        'acute_measles_diarrhea_case_13': ExcelFormField(
            'N9', int,
            EpidemiologyR._meta.get_field(
                'acute_measles_diarrhea_case').verbose_name),
        'acute_measles_diarrhea_death_13': ExcelFormField(
            'N10', int,
            EpidemiologyR._meta.get_field(
                'acute_measles_diarrhea_death').verbose_name),
        'other_notifiable_disease_case_13': ExcelFormField(
            'O9', int,
            EpidemiologyR._meta.get_field(
                'other_notifiable_disease_case').verbose_name),
        'other_notifiable_disease_death_13': ExcelFormField(
            'O10', int,
            EpidemiologyR._meta.get_field(
                'other_notifiable_disease_death').verbose_name),

        # line 14
        'snisi_code_14': ExcelFormField('A9', text_type, _("Health Center")),
        'ebola_case_14': ExcelFormField(
            'D9', int,
            EpidemiologyR._meta.get_field('ebola_case').verbose_name),
        'ebola_death_14': ExcelFormField(
            'D10', int,
            EpidemiologyR._meta.get_field('ebola_death').verbose_name),
        'acute_flaccid_paralysis_case_14': ExcelFormField(
            'E9', int,
            EpidemiologyR._meta.get_field(
                'acute_flaccid_paralysis_case').verbose_name),
        'acute_flaccid_paralysis_death_14': ExcelFormField(
            'E10', int,
            EpidemiologyR._meta.get_field(
                'acute_flaccid_paralysis_death').verbose_name),
        'influenza_a_h1n1_case_14': ExcelFormField(
            'F9', int,
            EpidemiologyR._meta.get_field(
                'influenza_a_h1n1_case').verbose_name),
        'influenza_a_h1n1_death_14': ExcelFormField(
            'F10', int,
            EpidemiologyR._meta.get_field(
                'influenza_a_h1n1_death').verbose_name),
        'cholera_case_14': ExcelFormField(
            'G9', int,
            EpidemiologyR._meta.get_field('cholera_case').verbose_name),
        'cholera_death_14': ExcelFormField(
            'G10', int,
            EpidemiologyR._meta.get_field('cholera_death').verbose_name),
        'red_diarrhea_case_14': ExcelFormField(
            'H9', int,
            EpidemiologyR._meta.get_field('red_diarrhea_case').verbose_name),
        'red_diarrhea_death_14': ExcelFormField(
            'H10', int,
            EpidemiologyR._meta.get_field('red_diarrhea_death').verbose_name),
        'measles_case_14': ExcelFormField(
            'I9', int,
            EpidemiologyR._meta.get_field('measles_case').verbose_name),
        'measles_death_14': ExcelFormField(
            'I10', int,
            EpidemiologyR._meta.get_field('measles_death').verbose_name),
        'yellow_fever_case_14': ExcelFormField(
            'J9', int,
            EpidemiologyR._meta.get_field('yellow_fever_case').verbose_name),
        'yellow_fever_death_14': ExcelFormField(
            'J10', int,
            EpidemiologyR._meta.get_field('yellow_fever_death').verbose_name),
        'neonatal_tetanus_case_14': ExcelFormField(
            'K9', int,
            EpidemiologyR._meta.get_field(
                'neonatal_tetanus_case').verbose_name),
        'neonatal_tetanus_death_14': ExcelFormField(
            'K10', int,
            EpidemiologyR._meta.get_field(
                'neonatal_tetanus_death').verbose_name),
        'meningitis_case_14': ExcelFormField(
            'L9', int,
            EpidemiologyR._meta.get_field('meningitis_case').verbose_name),
        'meningitis_death_14': ExcelFormField(
            'L10', int,
            EpidemiologyR._meta.get_field('meningitis_death').verbose_name),
        'rabies_case_14': ExcelFormField(
            'M9', int,
            EpidemiologyR._meta.get_field('rabies_case').verbose_name),
        'rabies_death_14': ExcelFormField(
            'M10', int,
            EpidemiologyR._meta.get_field('rabies_death').verbose_name),
        'acute_measles_diarrhea_case_14': ExcelFormField(
            'N9', int,
            EpidemiologyR._meta.get_field(
                'acute_measles_diarrhea_case').verbose_name),
        'acute_measles_diarrhea_death_14': ExcelFormField(
            'N10', int,
            EpidemiologyR._meta.get_field(
                'acute_measles_diarrhea_death').verbose_name),
        'other_notifiable_disease_case_14': ExcelFormField(
            'O9', int,
            EpidemiologyR._meta.get_field(
                'other_notifiable_disease_case').verbose_name),
        'other_notifiable_disease_death_14': ExcelFormField(
            'O10', int,
            EpidemiologyR._meta.get_field(
                'other_notifiable_disease_death').verbose_name),

        # line 15
        'snisi_code_15': ExcelFormField('A9', text_type, _("Health Center")),
        'ebola_case_15': ExcelFormField(
            'D9', int,
            EpidemiologyR._meta.get_field('ebola_case').verbose_name),
        'ebola_death_15': ExcelFormField(
            'D10', int,
            EpidemiologyR._meta.get_field('ebola_death').verbose_name),
        'acute_flaccid_paralysis_case_15': ExcelFormField(
            'E9', int,
            EpidemiologyR._meta.get_field(
                'acute_flaccid_paralysis_case').verbose_name),
        'acute_flaccid_paralysis_death_15': ExcelFormField(
            'E10', int,
            EpidemiologyR._meta.get_field(
                'acute_flaccid_paralysis_death').verbose_name),
        'influenza_a_h1n1_case_15': ExcelFormField(
            'F9', int,
            EpidemiologyR._meta.get_field(
                'influenza_a_h1n1_case').verbose_name),
        'influenza_a_h1n1_death_15': ExcelFormField(
            'F10', int,
            EpidemiologyR._meta.get_field(
                'influenza_a_h1n1_death').verbose_name),
        'cholera_case_15': ExcelFormField(
            'G9', int,
            EpidemiologyR._meta.get_field('cholera_case').verbose_name),
        'cholera_death_15': ExcelFormField(
            'G10', int,
            EpidemiologyR._meta.get_field('cholera_death').verbose_name),
        'red_diarrhea_case_15': ExcelFormField(
            'H9', int,
            EpidemiologyR._meta.get_field('red_diarrhea_case').verbose_name),
        'red_diarrhea_death_15': ExcelFormField(
            'H10', int,
            EpidemiologyR._meta.get_field('red_diarrhea_death').verbose_name),
        'measles_case_15': ExcelFormField(
            'I9', int,
            EpidemiologyR._meta.get_field('measles_case').verbose_name),
        'measles_death_15': ExcelFormField(
            'I10', int,
            EpidemiologyR._meta.get_field('measles_death').verbose_name),
        'yellow_fever_case_15': ExcelFormField(
            'J9', int,
            EpidemiologyR._meta.get_field('yellow_fever_case').verbose_name),
        'yellow_fever_death_15': ExcelFormField(
            'J10', int,
            EpidemiologyR._meta.get_field('yellow_fever_death').verbose_name),
        'neonatal_tetanus_case_15': ExcelFormField(
            'K9', int,
            EpidemiologyR._meta.get_field(
                'neonatal_tetanus_case').verbose_name),
        'neonatal_tetanus_death_15': ExcelFormField(
            'K10', int,
            EpidemiologyR._meta.get_field(
                'neonatal_tetanus_death').verbose_name),
        'meningitis_case_15': ExcelFormField(
            'L9', int,
            EpidemiologyR._meta.get_field('meningitis_case').verbose_name),
        'meningitis_death_15': ExcelFormField(
            'L10', int,
            EpidemiologyR._meta.get_field('meningitis_death').verbose_name),
        'rabies_case_15': ExcelFormField(
            'M9', int,
            EpidemiologyR._meta.get_field('rabies_case').verbose_name),
        'rabies_death_15': ExcelFormField(
            'M10', int,
            EpidemiologyR._meta.get_field('rabies_death').verbose_name),
        'acute_measles_diarrhea_case_15': ExcelFormField(
            'N9', int,
            EpidemiologyR._meta.get_field(
                'acute_measles_diarrhea_case').verbose_name),
        'acute_measles_diarrhea_death_15': ExcelFormField(
            'N10', int,
            EpidemiologyR._meta.get_field(
                'acute_measles_diarrhea_death').verbose_name),
        'other_notifiable_disease_case_15': ExcelFormField(
            'O9', int,
            EpidemiologyR._meta.get_field(
                'other_notifiable_disease_case').verbose_name),
        'other_notifiable_disease_death_15': ExcelFormField(
            'O10', int,
            EpidemiologyR._meta.get_field(
                'other_notifiable_disease_death').verbose_name),

        # line 16
        'snisi_code_16': ExcelFormField('A9', text_type, _("Health Center")),
        'ebola_case_16': ExcelFormField(
            'D9', int,
            EpidemiologyR._meta.get_field('ebola_case').verbose_name),
        'ebola_death_16': ExcelFormField(
            'D10', int,
            EpidemiologyR._meta.get_field('ebola_death').verbose_name),
        'acute_flaccid_paralysis_case_16': ExcelFormField(
            'E9', int,
            EpidemiologyR._meta.get_field(
                'acute_flaccid_paralysis_case').verbose_name),
        'acute_flaccid_paralysis_death_16': ExcelFormField(
            'E10', int,
            EpidemiologyR._meta.get_field(
                'acute_flaccid_paralysis_death').verbose_name),
        'influenza_a_h1n1_case_16': ExcelFormField(
            'F9', int,
            EpidemiologyR._meta.get_field(
                'influenza_a_h1n1_case').verbose_name),
        'influenza_a_h1n1_death_16': ExcelFormField(
            'F10', int,
            EpidemiologyR._meta.get_field(
                'influenza_a_h1n1_death').verbose_name),
        'cholera_case_16': ExcelFormField(
            'G9', int,
            EpidemiologyR._meta.get_field('cholera_case').verbose_name),
        'cholera_death_16': ExcelFormField(
            'G10', int,
            EpidemiologyR._meta.get_field('cholera_death').verbose_name),
        'red_diarrhea_case_16': ExcelFormField(
            'H9', int,
            EpidemiologyR._meta.get_field('red_diarrhea_case').verbose_name),
        'red_diarrhea_death_16': ExcelFormField(
            'H10', int,
            EpidemiologyR._meta.get_field('red_diarrhea_death').verbose_name),
        'measles_case_16': ExcelFormField(
            'I9', int,
            EpidemiologyR._meta.get_field('measles_case').verbose_name),
        'measles_death_16': ExcelFormField(
            'I10', int,
            EpidemiologyR._meta.get_field('measles_death').verbose_name),
        'yellow_fever_case_16': ExcelFormField(
            'J9', int,
            EpidemiologyR._meta.get_field('yellow_fever_case').verbose_name),
        'yellow_fever_death_16': ExcelFormField(
            'J10', int,
            EpidemiologyR._meta.get_field('yellow_fever_death').verbose_name),
        'neonatal_tetanus_case_16': ExcelFormField(
            'K9', int,
            EpidemiologyR._meta.get_field(
                'neonatal_tetanus_case').verbose_name),
        'neonatal_tetanus_death_16': ExcelFormField(
            'K10', int,
            EpidemiologyR._meta.get_field(
                'neonatal_tetanus_death').verbose_name),
        'meningitis_case_16': ExcelFormField(
            'L9', int,
            EpidemiologyR._meta.get_field('meningitis_case').verbose_name),
        'meningitis_death_16': ExcelFormField(
            'L10', int,
            EpidemiologyR._meta.get_field('meningitis_death').verbose_name),
        'rabies_case_16': ExcelFormField(
            'M9', int,
            EpidemiologyR._meta.get_field('rabies_case').verbose_name),
        'rabies_death_16': ExcelFormField(
            'M10', int,
            EpidemiologyR._meta.get_field('rabies_death').verbose_name),
        'acute_measles_diarrhea_case_16': ExcelFormField(
            'N9', int,
            EpidemiologyR._meta.get_field(
                'acute_measles_diarrhea_case').verbose_name),
        'acute_measles_diarrhea_death_16': ExcelFormField(
            'N10', int,
            EpidemiologyR._meta.get_field(
                'acute_measles_diarrhea_death').verbose_name),
        'other_notifiable_disease_case_16': ExcelFormField(
            'O9', int,
            EpidemiologyR._meta.get_field(
                'other_notifiable_disease_case').verbose_name),
        'other_notifiable_disease_death_16': ExcelFormField(
            'O10', int,
            EpidemiologyR._meta.get_field(
                'other_notifiable_disease_death').verbose_name),

        # line 17
        'snisi_code_17': ExcelFormField('A9', text_type, _("Health Center")),
        'ebola_case_17': ExcelFormField(
            'D9', int,
            EpidemiologyR._meta.get_field('ebola_case').verbose_name),
        'ebola_death_17': ExcelFormField(
            'D10', int,
            EpidemiologyR._meta.get_field('ebola_death').verbose_name),
        'acute_flaccid_paralysis_case_17': ExcelFormField(
            'E9', int,
            EpidemiologyR._meta.get_field(
                'acute_flaccid_paralysis_case').verbose_name),
        'acute_flaccid_paralysis_death_17': ExcelFormField(
            'E10', int,
            EpidemiologyR._meta.get_field(
                'acute_flaccid_paralysis_death').verbose_name),
        'influenza_a_h1n1_case_17': ExcelFormField(
            'F9', int,
            EpidemiologyR._meta.get_field(
                'influenza_a_h1n1_case').verbose_name),
        'influenza_a_h1n1_death_17': ExcelFormField(
            'F10', int,
            EpidemiologyR._meta.get_field(
                'influenza_a_h1n1_death').verbose_name),
        'cholera_case_17': ExcelFormField(
            'G9', int,
            EpidemiologyR._meta.get_field('cholera_case').verbose_name),
        'cholera_death_17': ExcelFormField(
            'G10', int,
            EpidemiologyR._meta.get_field('cholera_death').verbose_name),
        'red_diarrhea_case_17': ExcelFormField(
            'H9', int,
            EpidemiologyR._meta.get_field('red_diarrhea_case').verbose_name),
        'red_diarrhea_death_17': ExcelFormField(
            'H10', int,
            EpidemiologyR._meta.get_field('red_diarrhea_death').verbose_name),
        'measles_case_17': ExcelFormField(
            'I9', int,
            EpidemiologyR._meta.get_field('measles_case').verbose_name),
        'measles_death_17': ExcelFormField(
            'I10', int,
            EpidemiologyR._meta.get_field('measles_death').verbose_name),
        'yellow_fever_case_17': ExcelFormField(
            'J9', int,
            EpidemiologyR._meta.get_field('yellow_fever_case').verbose_name),
        'yellow_fever_death_17': ExcelFormField(
            'J10', int,
            EpidemiologyR._meta.get_field('yellow_fever_death').verbose_name),
        'neonatal_tetanus_case_17': ExcelFormField(
            'K9', int,
            EpidemiologyR._meta.get_field(
                'neonatal_tetanus_case').verbose_name),
        'neonatal_tetanus_death_17': ExcelFormField(
            'K10', int,
            EpidemiologyR._meta.get_field(
                'neonatal_tetanus_death').verbose_name),
        'meningitis_case_17': ExcelFormField(
            'L9', int,
            EpidemiologyR._meta.get_field('meningitis_case').verbose_name),
        'meningitis_death_17': ExcelFormField(
            'L10', int,
            EpidemiologyR._meta.get_field('meningitis_death').verbose_name),
        'rabies_case_17': ExcelFormField(
            'M9', int,
            EpidemiologyR._meta.get_field('rabies_case').verbose_name),
        'rabies_death_17': ExcelFormField(
            'M10', int,
            EpidemiologyR._meta.get_field('rabies_death').verbose_name),
        'acute_measles_diarrhea_case_17': ExcelFormField(
            'N9', int,
            EpidemiologyR._meta.get_field(
                'acute_measles_diarrhea_case').verbose_name),
        'acute_measles_diarrhea_death_17': ExcelFormField(
            'N10', int,
            EpidemiologyR._meta.get_field(
                'acute_measles_diarrhea_death').verbose_name),
        'other_notifiable_disease_case_17': ExcelFormField(
            'O9', int,
            EpidemiologyR._meta.get_field(
                'other_notifiable_disease_case').verbose_name),
        'other_notifiable_disease_death_17': ExcelFormField(
            'O10', int,
            EpidemiologyR._meta.get_field(
                'other_notifiable_disease_death').verbose_name),

        # line 18
        'snisi_code_18': ExcelFormField('A9', text_type, _("Health Center")),
        'ebola_case_18': ExcelFormField(
            'D9', int,
            EpidemiologyR._meta.get_field('ebola_case').verbose_name),
        'ebola_death_18': ExcelFormField(
            'D10', int,
            EpidemiologyR._meta.get_field('ebola_death').verbose_name),
        'acute_flaccid_paralysis_case_18': ExcelFormField(
            'E9', int,
            EpidemiologyR._meta.get_field(
                'acute_flaccid_paralysis_case').verbose_name),
        'acute_flaccid_paralysis_death_18': ExcelFormField(
            'E10', int,
            EpidemiologyR._meta.get_field(
                'acute_flaccid_paralysis_death').verbose_name),
        'influenza_a_h1n1_case_18': ExcelFormField(
            'F9', int,
            EpidemiologyR._meta.get_field(
                'influenza_a_h1n1_case').verbose_name),
        'influenza_a_h1n1_death_18': ExcelFormField(
            'F10', int,
            EpidemiologyR._meta.get_field(
                'influenza_a_h1n1_death').verbose_name),
        'cholera_case_18': ExcelFormField(
            'G9', int,
            EpidemiologyR._meta.get_field('cholera_case').verbose_name),
        'cholera_death_18': ExcelFormField(
            'G10', int,
            EpidemiologyR._meta.get_field('cholera_death').verbose_name),
        'red_diarrhea_case_18': ExcelFormField(
            'H9', int,
            EpidemiologyR._meta.get_field('red_diarrhea_case').verbose_name),
        'red_diarrhea_death_18': ExcelFormField(
            'H10', int,
            EpidemiologyR._meta.get_field('red_diarrhea_death').verbose_name),
        'measles_case_18': ExcelFormField(
            'I9', int,
            EpidemiologyR._meta.get_field('measles_case').verbose_name),
        'measles_death_18': ExcelFormField(
            'I10', int,
            EpidemiologyR._meta.get_field('measles_death').verbose_name),
        'yellow_fever_case_18': ExcelFormField(
            'J9', int,
            EpidemiologyR._meta.get_field('yellow_fever_case').verbose_name),
        'yellow_fever_death_18': ExcelFormField(
            'J10', int,
            EpidemiologyR._meta.get_field('yellow_fever_death').verbose_name),
        'neonatal_tetanus_case_18': ExcelFormField(
            'K9', int,
            EpidemiologyR._meta.get_field(
                'neonatal_tetanus_case').verbose_name),
        'neonatal_tetanus_death_18': ExcelFormField(
            'K10', int,
            EpidemiologyR._meta.get_field(
                'neonatal_tetanus_death').verbose_name),
        'meningitis_case_18': ExcelFormField(
            'L9', int,
            EpidemiologyR._meta.get_field('meningitis_case').verbose_name),
        'meningitis_death_18': ExcelFormField(
            'L10', int,
            EpidemiologyR._meta.get_field('meningitis_death').verbose_name),
        'rabies_case_18': ExcelFormField(
            'M9', int,
            EpidemiologyR._meta.get_field('rabies_case').verbose_name),
        'rabies_death_18': ExcelFormField(
            'M10', int,
            EpidemiologyR._meta.get_field('rabies_death').verbose_name),
        'acute_measles_diarrhea_case_18': ExcelFormField(
            'N9', int,
            EpidemiologyR._meta.get_field(
                'acute_measles_diarrhea_case').verbose_name),
        'acute_measles_diarrhea_death_18': ExcelFormField(
            'N10', int,
            EpidemiologyR._meta.get_field(
                'acute_measles_diarrhea_death').verbose_name),
        'other_notifiable_disease_case_18': ExcelFormField(
            'O9', int,
            EpidemiologyR._meta.get_field(
                'other_notifiable_disease_case').verbose_name),
        'other_notifiable_disease_death_18': ExcelFormField(
            'O10', int,
            EpidemiologyR._meta.get_field(
                'other_notifiable_disease_death').verbose_name),

        # line 19
        'snisi_code_19': ExcelFormField('A9', text_type, _("Health Center")),
        'ebola_case_19': ExcelFormField(
            'D9', int,
            EpidemiologyR._meta.get_field('ebola_case').verbose_name),
        'ebola_death_19': ExcelFormField(
            'D10', int,
            EpidemiologyR._meta.get_field('ebola_death').verbose_name),
        'acute_flaccid_paralysis_case_19': ExcelFormField(
            'E9', int,
            EpidemiologyR._meta.get_field(
                'acute_flaccid_paralysis_case').verbose_name),
        'acute_flaccid_paralysis_death_19': ExcelFormField(
            'E10', int,
            EpidemiologyR._meta.get_field(
                'acute_flaccid_paralysis_death').verbose_name),
        'influenza_a_h1n1_case_19': ExcelFormField(
            'F9', int,
            EpidemiologyR._meta.get_field(
                'influenza_a_h1n1_case').verbose_name),
        'influenza_a_h1n1_death_19': ExcelFormField(
            'F10', int,
            EpidemiologyR._meta.get_field(
                'influenza_a_h1n1_death').verbose_name),
        'cholera_case_19': ExcelFormField(
            'G9', int,
            EpidemiologyR._meta.get_field('cholera_case').verbose_name),
        'cholera_death_19': ExcelFormField(
            'G10', int,
            EpidemiologyR._meta.get_field('cholera_death').verbose_name),
        'red_diarrhea_case_19': ExcelFormField(
            'H9', int,
            EpidemiologyR._meta.get_field('red_diarrhea_case').verbose_name),
        'red_diarrhea_death_19': ExcelFormField(
            'H10', int,
            EpidemiologyR._meta.get_field('red_diarrhea_death').verbose_name),
        'measles_case_19': ExcelFormField(
            'I9', int,
            EpidemiologyR._meta.get_field('measles_case').verbose_name),
        'measles_death_19': ExcelFormField(
            'I10', int,
            EpidemiologyR._meta.get_field('measles_death').verbose_name),
        'yellow_fever_case_19': ExcelFormField(
            'J9', int,
            EpidemiologyR._meta.get_field('yellow_fever_case').verbose_name),
        'yellow_fever_death_19': ExcelFormField(
            'J10', int,
            EpidemiologyR._meta.get_field('yellow_fever_death').verbose_name),
        'neonatal_tetanus_case_19': ExcelFormField(
            'K9', int,
            EpidemiologyR._meta.get_field(
                'neonatal_tetanus_case').verbose_name),
        'neonatal_tetanus_death_19': ExcelFormField(
            'K10', int,
            EpidemiologyR._meta.get_field(
                'neonatal_tetanus_death').verbose_name),
        'meningitis_case_19': ExcelFormField(
            'L9', int,
            EpidemiologyR._meta.get_field('meningitis_case').verbose_name),
        'meningitis_death_19': ExcelFormField(
            'L10', int,
            EpidemiologyR._meta.get_field('meningitis_death').verbose_name),
        'rabies_case_19': ExcelFormField(
            'M9', int,
            EpidemiologyR._meta.get_field('rabies_case').verbose_name),
        'rabies_death_19': ExcelFormField(
            'M10', int,
            EpidemiologyR._meta.get_field('rabies_death').verbose_name),
        'acute_measles_diarrhea_case_19': ExcelFormField(
            'N9', int,
            EpidemiologyR._meta.get_field(
                'acute_measles_diarrhea_case').verbose_name),
        'acute_measles_diarrhea_death_19': ExcelFormField(
            'N10', int,
            EpidemiologyR._meta.get_field(
                'acute_measles_diarrhea_death').verbose_name),
        'other_notifiable_disease_case_19': ExcelFormField(
            'O9', int,
            EpidemiologyR._meta.get_field(
                'other_notifiable_disease_case').verbose_name),
        'other_notifiable_disease_death_19': ExcelFormField(
            'O10', int,
            EpidemiologyR._meta.get_field(
                'other_notifiable_disease_death').verbose_name),

        # line 20
        'snisi_code_20': ExcelFormField('A9', text_type, _("Health Center")),
        'ebola_case_20': ExcelFormField(
            'D9', int,
            EpidemiologyR._meta.get_field('ebola_case').verbose_name),
        'ebola_death_20': ExcelFormField(
            'D10', int,
            EpidemiologyR._meta.get_field('ebola_death').verbose_name),
        'acute_flaccid_paralysis_case_20': ExcelFormField(
            'E9', int,
            EpidemiologyR._meta.get_field(
                'acute_flaccid_paralysis_case').verbose_name),
        'acute_flaccid_paralysis_death_20': ExcelFormField(
            'E10', int,
            EpidemiologyR._meta.get_field(
                'acute_flaccid_paralysis_death').verbose_name),
        'influenza_a_h1n1_case_20': ExcelFormField(
            'F9', int,
            EpidemiologyR._meta.get_field(
                'influenza_a_h1n1_case').verbose_name),
        'influenza_a_h1n1_death_20': ExcelFormField(
            'F10', int,
            EpidemiologyR._meta.get_field(
                'influenza_a_h1n1_death').verbose_name),
        'cholera_case_20': ExcelFormField(
            'G9', int,
            EpidemiologyR._meta.get_field('cholera_case').verbose_name),
        'cholera_death_20': ExcelFormField(
            'G10', int,
            EpidemiologyR._meta.get_field('cholera_death').verbose_name),
        'red_diarrhea_case_20': ExcelFormField(
            'H9', int,
            EpidemiologyR._meta.get_field('red_diarrhea_case').verbose_name),
        'red_diarrhea_death_20': ExcelFormField(
            'H10', int,
            EpidemiologyR._meta.get_field('red_diarrhea_death').verbose_name),
        'measles_case_20': ExcelFormField(
            'I9', int,
            EpidemiologyR._meta.get_field('measles_case').verbose_name),
        'measles_death_20': ExcelFormField(
            'I10', int,
            EpidemiologyR._meta.get_field('measles_death').verbose_name),
        'yellow_fever_case_20': ExcelFormField(
            'J9', int,
            EpidemiologyR._meta.get_field('yellow_fever_case').verbose_name),
        'yellow_fever_death_20': ExcelFormField(
            'J10', int,
            EpidemiologyR._meta.get_field('yellow_fever_death').verbose_name),
        'neonatal_tetanus_case_20': ExcelFormField(
            'K9', int,
            EpidemiologyR._meta.get_field(
                'neonatal_tetanus_case').verbose_name),
        'neonatal_tetanus_death_20': ExcelFormField(
            'K10', int,
            EpidemiologyR._meta.get_field(
                'neonatal_tetanus_death').verbose_name),
        'meningitis_case_20': ExcelFormField(
            'L9', int,
            EpidemiologyR._meta.get_field('meningitis_case').verbose_name),
        'meningitis_death_20': ExcelFormField(
            'L10', int,
            EpidemiologyR._meta.get_field('meningitis_death').verbose_name),
        'rabies_case_20': ExcelFormField(
            'M9', int,
            EpidemiologyR._meta.get_field('rabies_case').verbose_name),
        'rabies_death_20': ExcelFormField(
            'M10', int,
            EpidemiologyR._meta.get_field('rabies_death').verbose_name),
        'acute_measles_diarrhea_case_20': ExcelFormField(
            'N9', int,
            EpidemiologyR._meta.get_field(
                'acute_measles_diarrhea_case').verbose_name),
        'acute_measles_diarrhea_death_20': ExcelFormField(
            'N10', int,
            EpidemiologyR._meta.get_field(
                'acute_measles_diarrhea_death').verbose_name),
        'other_notifiable_disease_case_20': ExcelFormField(
            'O9', int,
            EpidemiologyR._meta.get_field(
                'other_notifiable_disease_case').verbose_name),
        'other_notifiable_disease_death_20': ExcelFormField(
            'O10', int,
            EpidemiologyR._meta.get_field(
                'other_notifiable_disease_death').verbose_name),

        # line 21
        'snisi_code_21': ExcelFormField('A9', text_type, _("Health Center")),
        'ebola_case_21': ExcelFormField(
            'D9', int,
            EpidemiologyR._meta.get_field('ebola_case').verbose_name),
        'ebola_death_21': ExcelFormField(
            'D10', int,
            EpidemiologyR._meta.get_field('ebola_death').verbose_name),
        'acute_flaccid_paralysis_case_21': ExcelFormField(
            'E9', int,
            EpidemiologyR._meta.get_field(
                'acute_flaccid_paralysis_case').verbose_name),
        'acute_flaccid_paralysis_death_21': ExcelFormField(
            'E10', int,
            EpidemiologyR._meta.get_field(
                'acute_flaccid_paralysis_death').verbose_name),
        'influenza_a_h1n1_case_21': ExcelFormField(
            'F9', int,
            EpidemiologyR._meta.get_field(
                'influenza_a_h1n1_case').verbose_name),
        'influenza_a_h1n1_death_21': ExcelFormField(
            'F10', int,
            EpidemiologyR._meta.get_field(
                'influenza_a_h1n1_death').verbose_name),
        'cholera_case_21': ExcelFormField(
            'G9', int,
            EpidemiologyR._meta.get_field('cholera_case').verbose_name),
        'cholera_death_21': ExcelFormField(
            'G10', int,
            EpidemiologyR._meta.get_field('cholera_death').verbose_name),
        'red_diarrhea_case_21': ExcelFormField(
            'H9', int,
            EpidemiologyR._meta.get_field('red_diarrhea_case').verbose_name),
        'red_diarrhea_death_21': ExcelFormField(
            'H10', int,
            EpidemiologyR._meta.get_field('red_diarrhea_death').verbose_name),
        'measles_case_21': ExcelFormField(
            'I9', int,
            EpidemiologyR._meta.get_field('measles_case').verbose_name),
        'measles_death_21': ExcelFormField(
            'I10', int,
            EpidemiologyR._meta.get_field('measles_death').verbose_name),
        'yellow_fever_case_21': ExcelFormField(
            'J9', int,
            EpidemiologyR._meta.get_field('yellow_fever_case').verbose_name),
        'yellow_fever_death_21': ExcelFormField(
            'J10', int,
            EpidemiologyR._meta.get_field('yellow_fever_death').verbose_name),
        'neonatal_tetanus_case_21': ExcelFormField(
            'K9', int,
            EpidemiologyR._meta.get_field(
                'neonatal_tetanus_case').verbose_name),
        'neonatal_tetanus_death_21': ExcelFormField(
            'K10', int,
            EpidemiologyR._meta.get_field(
                'neonatal_tetanus_death').verbose_name),
        'meningitis_case_21': ExcelFormField(
            'L9', int,
            EpidemiologyR._meta.get_field('meningitis_case').verbose_name),
        'meningitis_death_21': ExcelFormField(
            'L10', int,
            EpidemiologyR._meta.get_field('meningitis_death').verbose_name),
        'rabies_case_21': ExcelFormField(
            'M9', int,
            EpidemiologyR._meta.get_field('rabies_case').verbose_name),
        'rabies_death_21': ExcelFormField(
            'M10', int,
            EpidemiologyR._meta.get_field('rabies_death').verbose_name),
        'acute_measles_diarrhea_case_21': ExcelFormField(
            'N9', int,
            EpidemiologyR._meta.get_field(
                'acute_measles_diarrhea_case').verbose_name),
        'acute_measles_diarrhea_death_21': ExcelFormField(
            'N10', int,
            EpidemiologyR._meta.get_field(
                'acute_measles_diarrhea_death').verbose_name),
        'other_notifiable_disease_case_21': ExcelFormField(
            'O9', int,
            EpidemiologyR._meta.get_field(
                'other_notifiable_disease_case').verbose_name),
        'other_notifiable_disease_death_21': ExcelFormField(
            'O10', int,
            EpidemiologyR._meta.get_field(
                'other_notifiable_disease_death').verbose_name),

        # line 22
        'snisi_code_22': ExcelFormField('A9', text_type, _("Health Center")),
        'ebola_case_22': ExcelFormField(
            'D9', int,
            EpidemiologyR._meta.get_field('ebola_case').verbose_name),
        'ebola_death_22': ExcelFormField(
            'D10', int,
            EpidemiologyR._meta.get_field('ebola_death').verbose_name),
        'acute_flaccid_paralysis_case_22': ExcelFormField(
            'E9', int,
            EpidemiologyR._meta.get_field(
                'acute_flaccid_paralysis_case').verbose_name),
        'acute_flaccid_paralysis_death_22': ExcelFormField(
            'E10', int,
            EpidemiologyR._meta.get_field(
                'acute_flaccid_paralysis_death').verbose_name),
        'influenza_a_h1n1_case_22': ExcelFormField(
            'F9', int,
            EpidemiologyR._meta.get_field(
                'influenza_a_h1n1_case').verbose_name),
        'influenza_a_h1n1_death_22': ExcelFormField(
            'F10', int,
            EpidemiologyR._meta.get_field(
                'influenza_a_h1n1_death').verbose_name),
        'cholera_case_22': ExcelFormField(
            'G9', int,
            EpidemiologyR._meta.get_field('cholera_case').verbose_name),
        'cholera_death_22': ExcelFormField(
            'G10', int,
            EpidemiologyR._meta.get_field('cholera_death').verbose_name),
        'red_diarrhea_case_22': ExcelFormField(
            'H9', int,
            EpidemiologyR._meta.get_field('red_diarrhea_case').verbose_name),
        'red_diarrhea_death_22': ExcelFormField(
            'H10', int,
            EpidemiologyR._meta.get_field('red_diarrhea_death').verbose_name),
        'measles_case_22': ExcelFormField(
            'I9', int,
            EpidemiologyR._meta.get_field('measles_case').verbose_name),
        'measles_death_22': ExcelFormField(
            'I10', int,
            EpidemiologyR._meta.get_field('measles_death').verbose_name),
        'yellow_fever_case_22': ExcelFormField(
            'J9', int,
            EpidemiologyR._meta.get_field('yellow_fever_case').verbose_name),
        'yellow_fever_death_22': ExcelFormField(
            'J10', int,
            EpidemiologyR._meta.get_field('yellow_fever_death').verbose_name),
        'neonatal_tetanus_case_22': ExcelFormField(
            'K9', int,
            EpidemiologyR._meta.get_field(
                'neonatal_tetanus_case').verbose_name),
        'neonatal_tetanus_death_22': ExcelFormField(
            'K10', int,
            EpidemiologyR._meta.get_field(
                'neonatal_tetanus_death').verbose_name),
        'meningitis_case_22': ExcelFormField(
            'L9', int,
            EpidemiologyR._meta.get_field('meningitis_case').verbose_name),
        'meningitis_death_22': ExcelFormField(
            'L10', int,
            EpidemiologyR._meta.get_field('meningitis_death').verbose_name),
        'rabies_case_22': ExcelFormField(
            'M9', int,
            EpidemiologyR._meta.get_field('rabies_case').verbose_name),
        'rabies_death_22': ExcelFormField(
            'M10', int,
            EpidemiologyR._meta.get_field('rabies_death').verbose_name),
        'acute_measles_diarrhea_case_22': ExcelFormField(
            'N9', int,
            EpidemiologyR._meta.get_field(
                'acute_measles_diarrhea_case').verbose_name),
        'acute_measles_diarrhea_death_22': ExcelFormField(
            'N10', int,
            EpidemiologyR._meta.get_field(
                'acute_measles_diarrhea_death').verbose_name),
        'other_notifiable_disease_case_22': ExcelFormField(
            'O9', int,
            EpidemiologyR._meta.get_field(
                'other_notifiable_disease_case').verbose_name),
        'other_notifiable_disease_death_22': ExcelFormField(
            'O10', int,
            EpidemiologyR._meta.get_field(
                'other_notifiable_disease_death').verbose_name),

        # line 23
        'snisi_code_23': ExcelFormField('A9', text_type, _("Health Center")),
        'ebola_case_23': ExcelFormField(
            'D9', int,
            EpidemiologyR._meta.get_field('ebola_case').verbose_name),
        'ebola_death_23': ExcelFormField(
            'D10', int,
            EpidemiologyR._meta.get_field('ebola_death').verbose_name),
        'acute_flaccid_paralysis_case_23': ExcelFormField(
            'E9', int,
            EpidemiologyR._meta.get_field(
                'acute_flaccid_paralysis_case').verbose_name),
        'acute_flaccid_paralysis_death_23': ExcelFormField(
            'E10', int,
            EpidemiologyR._meta.get_field(
                'acute_flaccid_paralysis_death').verbose_name),
        'influenza_a_h1n1_case_23': ExcelFormField(
            'F9', int,
            EpidemiologyR._meta.get_field(
                'influenza_a_h1n1_case').verbose_name),
        'influenza_a_h1n1_death_23': ExcelFormField(
            'F10', int,
            EpidemiologyR._meta.get_field(
                'influenza_a_h1n1_death').verbose_name),
        'cholera_case_23': ExcelFormField(
            'G9', int,
            EpidemiologyR._meta.get_field('cholera_case').verbose_name),
        'cholera_death_23': ExcelFormField(
            'G10', int,
            EpidemiologyR._meta.get_field('cholera_death').verbose_name),
        'red_diarrhea_case_23': ExcelFormField(
            'H9', int,
            EpidemiologyR._meta.get_field('red_diarrhea_case').verbose_name),
        'red_diarrhea_death_23': ExcelFormField(
            'H10', int,
            EpidemiologyR._meta.get_field('red_diarrhea_death').verbose_name),
        'measles_case_23': ExcelFormField(
            'I9', int,
            EpidemiologyR._meta.get_field('measles_case').verbose_name),
        'measles_death_23': ExcelFormField(
            'I10', int,
            EpidemiologyR._meta.get_field('measles_death').verbose_name),
        'yellow_fever_case_23': ExcelFormField(
            'J9', int,
            EpidemiologyR._meta.get_field('yellow_fever_case').verbose_name),
        'yellow_fever_death_23': ExcelFormField(
            'J10', int,
            EpidemiologyR._meta.get_field('yellow_fever_death').verbose_name),
        'neonatal_tetanus_case_23': ExcelFormField(
            'K9', int,
            EpidemiologyR._meta.get_field(
                'neonatal_tetanus_case').verbose_name),
        'neonatal_tetanus_death_23': ExcelFormField(
            'K10', int,
            EpidemiologyR._meta.get_field(
                'neonatal_tetanus_death').verbose_name),
        'meningitis_case_23': ExcelFormField(
            'L9', int,
            EpidemiologyR._meta.get_field('meningitis_case').verbose_name),
        'meningitis_death_23': ExcelFormField(
            'L10', int,
            EpidemiologyR._meta.get_field('meningitis_death').verbose_name),
        'rabies_case_23': ExcelFormField(
            'M9', int,
            EpidemiologyR._meta.get_field('rabies_case').verbose_name),
        'rabies_death_23': ExcelFormField(
            'M10', int,
            EpidemiologyR._meta.get_field('rabies_death').verbose_name),
        'acute_measles_diarrhea_case_23': ExcelFormField(
            'N9', int,
            EpidemiologyR._meta.get_field(
                'acute_measles_diarrhea_case').verbose_name),
        'acute_measles_diarrhea_death_23': ExcelFormField(
            'N10', int,
            EpidemiologyR._meta.get_field(
                'acute_measles_diarrhea_death').verbose_name),
        'other_notifiable_disease_case_23': ExcelFormField(
            'O9', int,
            EpidemiologyR._meta.get_field(
                'other_notifiable_disease_case').verbose_name),
        'other_notifiable_disease_death_23': ExcelFormField(
            'O10', int,
            EpidemiologyR._meta.get_field(
                'other_notifiable_disease_death').verbose_name),

        # line 24
        'snisi_code_24': ExcelFormField('A9', text_type, _("Health Center")),
        'ebola_case_24': ExcelFormField(
            'D9', int,
            EpidemiologyR._meta.get_field('ebola_case').verbose_name),
        'ebola_death_24': ExcelFormField(
            'D10', int,
            EpidemiologyR._meta.get_field('ebola_death').verbose_name),
        'acute_flaccid_paralysis_case_24': ExcelFormField(
            'E9', int,
            EpidemiologyR._meta.get_field(
                'acute_flaccid_paralysis_case').verbose_name),
        'acute_flaccid_paralysis_death_24': ExcelFormField(
            'E10', int,
            EpidemiologyR._meta.get_field(
                'acute_flaccid_paralysis_death').verbose_name),
        'influenza_a_h1n1_case_24': ExcelFormField(
            'F9', int,
            EpidemiologyR._meta.get_field(
                'influenza_a_h1n1_case').verbose_name),
        'influenza_a_h1n1_death_24': ExcelFormField(
            'F10', int,
            EpidemiologyR._meta.get_field(
                'influenza_a_h1n1_death').verbose_name),
        'cholera_case_24': ExcelFormField(
            'G9', int,
            EpidemiologyR._meta.get_field('cholera_case').verbose_name),
        'cholera_death_24': ExcelFormField(
            'G10', int,
            EpidemiologyR._meta.get_field('cholera_death').verbose_name),
        'red_diarrhea_case_24': ExcelFormField(
            'H9', int,
            EpidemiologyR._meta.get_field('red_diarrhea_case').verbose_name),
        'red_diarrhea_death_24': ExcelFormField(
            'H10', int,
            EpidemiologyR._meta.get_field('red_diarrhea_death').verbose_name),
        'measles_case_24': ExcelFormField(
            'I9', int,
            EpidemiologyR._meta.get_field('measles_case').verbose_name),
        'measles_death_24': ExcelFormField(
            'I10', int,
            EpidemiologyR._meta.get_field('measles_death').verbose_name),
        'yellow_fever_case_24': ExcelFormField(
            'J9', int,
            EpidemiologyR._meta.get_field('yellow_fever_case').verbose_name),
        'yellow_fever_death_24': ExcelFormField(
            'J10', int,
            EpidemiologyR._meta.get_field('yellow_fever_death').verbose_name),
        'neonatal_tetanus_case_24': ExcelFormField(
            'K9', int,
            EpidemiologyR._meta.get_field(
                'neonatal_tetanus_case').verbose_name),
        'neonatal_tetanus_death_24': ExcelFormField(
            'K10', int,
            EpidemiologyR._meta.get_field(
                'neonatal_tetanus_death').verbose_name),
        'meningitis_case_24': ExcelFormField(
            'L9', int,
            EpidemiologyR._meta.get_field('meningitis_case').verbose_name),
        'meningitis_death_24': ExcelFormField(
            'L10', int,
            EpidemiologyR._meta.get_field('meningitis_death').verbose_name),
        'rabies_case_24': ExcelFormField(
            'M9', int,
            EpidemiologyR._meta.get_field('rabies_case').verbose_name),
        'rabies_death_24': ExcelFormField(
            'M10', int,
            EpidemiologyR._meta.get_field('rabies_death').verbose_name),
        'acute_measles_diarrhea_case_24': ExcelFormField(
            'N9', int,
            EpidemiologyR._meta.get_field(
                'acute_measles_diarrhea_case').verbose_name),
        'acute_measles_diarrhea_death_24': ExcelFormField(
            'N10', int,
            EpidemiologyR._meta.get_field(
                'acute_measles_diarrhea_death').verbose_name),
        'other_notifiable_disease_case_24': ExcelFormField(
            'O9', int,
            EpidemiologyR._meta.get_field(
                'other_notifiable_disease_case').verbose_name),
        'other_notifiable_disease_death_24': ExcelFormField(
            'O10', int,
            EpidemiologyR._meta.get_field(
                'other_notifiable_disease_death').verbose_name),

        # line 25
        'snisi_code_25': ExcelFormField('A9', text_type, _("Health Center")),
        'ebola_case_25': ExcelFormField(
            'D9', int,
            EpidemiologyR._meta.get_field('ebola_case').verbose_name),
        'ebola_death_25': ExcelFormField(
            'D10', int,
            EpidemiologyR._meta.get_field('ebola_death').verbose_name),
        'acute_flaccid_paralysis_case_25': ExcelFormField(
            'E9', int,
            EpidemiologyR._meta.get_field(
                'acute_flaccid_paralysis_case').verbose_name),
        'acute_flaccid_paralysis_death_25': ExcelFormField(
            'E10', int,
            EpidemiologyR._meta.get_field(
                'acute_flaccid_paralysis_death').verbose_name),
        'influenza_a_h1n1_case_25': ExcelFormField(
            'F9', int,
            EpidemiologyR._meta.get_field(
                'influenza_a_h1n1_case').verbose_name),
        'influenza_a_h1n1_death_25': ExcelFormField(
            'F10', int,
            EpidemiologyR._meta.get_field(
                'influenza_a_h1n1_death').verbose_name),
        'cholera_case_25': ExcelFormField(
            'G9', int,
            EpidemiologyR._meta.get_field('cholera_case').verbose_name),
        'cholera_death_25': ExcelFormField(
            'G10', int,
            EpidemiologyR._meta.get_field('cholera_death').verbose_name),
        'red_diarrhea_case_25': ExcelFormField(
            'H9', int,
            EpidemiologyR._meta.get_field('red_diarrhea_case').verbose_name),
        'red_diarrhea_death_25': ExcelFormField(
            'H10', int,
            EpidemiologyR._meta.get_field('red_diarrhea_death').verbose_name),
        'measles_case_25': ExcelFormField(
            'I9', int,
            EpidemiologyR._meta.get_field('measles_case').verbose_name),
        'measles_death_25': ExcelFormField(
            'I10', int,
            EpidemiologyR._meta.get_field('measles_death').verbose_name),
        'yellow_fever_case_25': ExcelFormField(
            'J9', int,
            EpidemiologyR._meta.get_field('yellow_fever_case').verbose_name),
        'yellow_fever_death_25': ExcelFormField(
            'J10', int,
            EpidemiologyR._meta.get_field('yellow_fever_death').verbose_name),
        'neonatal_tetanus_case_25': ExcelFormField(
            'K9', int,
            EpidemiologyR._meta.get_field(
                'neonatal_tetanus_case').verbose_name),
        'neonatal_tetanus_death_25': ExcelFormField(
            'K10', int,
            EpidemiologyR._meta.get_field(
                'neonatal_tetanus_death').verbose_name),
        'meningitis_case_25': ExcelFormField(
            'L9', int,
            EpidemiologyR._meta.get_field('meningitis_case').verbose_name),
        'meningitis_death_25': ExcelFormField(
            'L10', int,
            EpidemiologyR._meta.get_field('meningitis_death').verbose_name),
        'rabies_case_25': ExcelFormField(
            'M9', int,
            EpidemiologyR._meta.get_field('rabies_case').verbose_name),
        'rabies_death_25': ExcelFormField(
            'M10', int,
            EpidemiologyR._meta.get_field('rabies_death').verbose_name),
        'acute_measles_diarrhea_case_25': ExcelFormField(
            'N9', int,
            EpidemiologyR._meta.get_field(
                'acute_measles_diarrhea_case').verbose_name),
        'acute_measles_diarrhea_death_25': ExcelFormField(
            'N10', int,
            EpidemiologyR._meta.get_field(
                'acute_measles_diarrhea_death').verbose_name),
        'other_notifiable_disease_case_25': ExcelFormField(
            'O9', int,
            EpidemiologyR._meta.get_field(
                'other_notifiable_disease_case').verbose_name),
        'other_notifiable_disease_death_25': ExcelFormField(
            'O10', int,
            EpidemiologyR._meta.get_field(
                'other_notifiable_disease_death').verbose_name),

        # line 26
        'snisi_code_26': ExcelFormField('A9', text_type, _("Health Center")),
        'ebola_case_26': ExcelFormField(
            'D9', int,
            EpidemiologyR._meta.get_field('ebola_case').verbose_name),
        'ebola_death_26': ExcelFormField(
            'D10', int,
            EpidemiologyR._meta.get_field('ebola_death').verbose_name),
        'acute_flaccid_paralysis_case_26': ExcelFormField(
            'E9', int,
            EpidemiologyR._meta.get_field(
                'acute_flaccid_paralysis_case').verbose_name),
        'acute_flaccid_paralysis_death_26': ExcelFormField(
            'E10', int,
            EpidemiologyR._meta.get_field(
                'acute_flaccid_paralysis_death').verbose_name),
        'influenza_a_h1n1_case_26': ExcelFormField(
            'F9', int,
            EpidemiologyR._meta.get_field(
                'influenza_a_h1n1_case').verbose_name),
        'influenza_a_h1n1_death_26': ExcelFormField(
            'F10', int,
            EpidemiologyR._meta.get_field(
                'influenza_a_h1n1_death').verbose_name),
        'cholera_case_26': ExcelFormField(
            'G9', int,
            EpidemiologyR._meta.get_field('cholera_case').verbose_name),
        'cholera_death_26': ExcelFormField(
            'G10', int,
            EpidemiologyR._meta.get_field('cholera_death').verbose_name),
        'red_diarrhea_case_26': ExcelFormField(
            'H9', int,
            EpidemiologyR._meta.get_field('red_diarrhea_case').verbose_name),
        'red_diarrhea_death_26': ExcelFormField(
            'H10', int,
            EpidemiologyR._meta.get_field('red_diarrhea_death').verbose_name),
        'measles_case_26': ExcelFormField(
            'I9', int,
            EpidemiologyR._meta.get_field('measles_case').verbose_name),
        'measles_death_26': ExcelFormField(
            'I10', int,
            EpidemiologyR._meta.get_field('measles_death').verbose_name),
        'yellow_fever_case_26': ExcelFormField(
            'J9', int,
            EpidemiologyR._meta.get_field('yellow_fever_case').verbose_name),
        'yellow_fever_death_26': ExcelFormField(
            'J10', int,
            EpidemiologyR._meta.get_field('yellow_fever_death').verbose_name),
        'neonatal_tetanus_case_26': ExcelFormField(
            'K9', int,
            EpidemiologyR._meta.get_field(
                'neonatal_tetanus_case').verbose_name),
        'neonatal_tetanus_death_26': ExcelFormField(
            'K10', int,
            EpidemiologyR._meta.get_field(
                'neonatal_tetanus_death').verbose_name),
        'meningitis_case_26': ExcelFormField(
            'L9', int,
            EpidemiologyR._meta.get_field('meningitis_case').verbose_name),
        'meningitis_death_26': ExcelFormField(
            'L10', int,
            EpidemiologyR._meta.get_field('meningitis_death').verbose_name),
        'rabies_case_26': ExcelFormField(
            'M9', int,
            EpidemiologyR._meta.get_field('rabies_case').verbose_name),
        'rabies_death_26': ExcelFormField(
            'M10', int,
            EpidemiologyR._meta.get_field('rabies_death').verbose_name),
        'acute_measles_diarrhea_case_26': ExcelFormField(
            'N9', int,
            EpidemiologyR._meta.get_field(
                'acute_measles_diarrhea_case').verbose_name),
        'acute_measles_diarrhea_death_26': ExcelFormField(
            'N10', int,
            EpidemiologyR._meta.get_field(
                'acute_measles_diarrhea_death').verbose_name),
        'other_notifiable_disease_case_26': ExcelFormField(
            'O9', int,
            EpidemiologyR._meta.get_field(
                'other_notifiable_disease_case').verbose_name),
        'other_notifiable_disease_death_26': ExcelFormField(
            'O10', int,
            EpidemiologyR._meta.get_field(
                'other_notifiable_disease_death').verbose_name),

        # line 27
        'snisi_code_27': ExcelFormField('A9', text_type, _("Health Center")),
        'ebola_case_27': ExcelFormField(
            'D9', int,
            EpidemiologyR._meta.get_field('ebola_case').verbose_name),
        'ebola_death_27': ExcelFormField(
            'D10', int,
            EpidemiologyR._meta.get_field('ebola_death').verbose_name),
        'acute_flaccid_paralysis_case_27': ExcelFormField(
            'E9', int,
            EpidemiologyR._meta.get_field(
                'acute_flaccid_paralysis_case').verbose_name),
        'acute_flaccid_paralysis_death_27': ExcelFormField(
            'E10', int,
            EpidemiologyR._meta.get_field(
                'acute_flaccid_paralysis_death').verbose_name),
        'influenza_a_h1n1_case_27': ExcelFormField(
            'F9', int,
            EpidemiologyR._meta.get_field(
                'influenza_a_h1n1_case').verbose_name),
        'influenza_a_h1n1_death_27': ExcelFormField(
            'F10', int,
            EpidemiologyR._meta.get_field(
                'influenza_a_h1n1_death').verbose_name),
        'cholera_case_27': ExcelFormField(
            'G9', int,
            EpidemiologyR._meta.get_field('cholera_case').verbose_name),
        'cholera_death_27': ExcelFormField(
            'G10', int,
            EpidemiologyR._meta.get_field('cholera_death').verbose_name),
        'red_diarrhea_case_27': ExcelFormField(
            'H9', int,
            EpidemiologyR._meta.get_field('red_diarrhea_case').verbose_name),
        'red_diarrhea_death_27': ExcelFormField(
            'H10', int,
            EpidemiologyR._meta.get_field('red_diarrhea_death').verbose_name),
        'measles_case_27': ExcelFormField(
            'I9', int,
            EpidemiologyR._meta.get_field('measles_case').verbose_name),
        'measles_death_27': ExcelFormField(
            'I10', int,
            EpidemiologyR._meta.get_field('measles_death').verbose_name),
        'yellow_fever_case_27': ExcelFormField(
            'J9', int,
            EpidemiologyR._meta.get_field('yellow_fever_case').verbose_name),
        'yellow_fever_death_27': ExcelFormField(
            'J10', int,
            EpidemiologyR._meta.get_field('yellow_fever_death').verbose_name),
        'neonatal_tetanus_case_27': ExcelFormField(
            'K9', int,
            EpidemiologyR._meta.get_field(
                'neonatal_tetanus_case').verbose_name),
        'neonatal_tetanus_death_27': ExcelFormField(
            'K10', int,
            EpidemiologyR._meta.get_field(
                'neonatal_tetanus_death').verbose_name),
        'meningitis_case_27': ExcelFormField(
            'L9', int,
            EpidemiologyR._meta.get_field('meningitis_case').verbose_name),
        'meningitis_death_27': ExcelFormField(
            'L10', int,
            EpidemiologyR._meta.get_field('meningitis_death').verbose_name),
        'rabies_case_27': ExcelFormField(
            'M9', int,
            EpidemiologyR._meta.get_field('rabies_case').verbose_name),
        'rabies_death_27': ExcelFormField(
            'M10', int,
            EpidemiologyR._meta.get_field('rabies_death').verbose_name),
        'acute_measles_diarrhea_case_27': ExcelFormField(
            'N9', int,
            EpidemiologyR._meta.get_field(
                'acute_measles_diarrhea_case').verbose_name),
        'acute_measles_diarrhea_death_27': ExcelFormField(
            'N10', int,
            EpidemiologyR._meta.get_field(
                'acute_measles_diarrhea_death').verbose_name),
        'other_notifiable_disease_case_27': ExcelFormField(
            'O9', int,
            EpidemiologyR._meta.get_field(
                'other_notifiable_disease_case').verbose_name),
        'other_notifiable_disease_death_27': ExcelFormField(
            'O10', int,
            EpidemiologyR._meta.get_field(
                'other_notifiable_disease_death').verbose_name),

        # line 28
        'snisi_code_28': ExcelFormField('A9', text_type, _("Health Center")),
        'ebola_case_28': ExcelFormField(
            'D9', int,
            EpidemiologyR._meta.get_field('ebola_case').verbose_name),
        'ebola_death_28': ExcelFormField(
            'D10', int,
            EpidemiologyR._meta.get_field('ebola_death').verbose_name),
        'acute_flaccid_paralysis_case_28': ExcelFormField(
            'E9', int,
            EpidemiologyR._meta.get_field(
                'acute_flaccid_paralysis_case').verbose_name),
        'acute_flaccid_paralysis_death_28': ExcelFormField(
            'E10', int,
            EpidemiologyR._meta.get_field(
                'acute_flaccid_paralysis_death').verbose_name),
        'influenza_a_h1n1_case_28': ExcelFormField(
            'F9', int,
            EpidemiologyR._meta.get_field(
                'influenza_a_h1n1_case').verbose_name),
        'influenza_a_h1n1_death_28': ExcelFormField(
            'F10', int,
            EpidemiologyR._meta.get_field(
                'influenza_a_h1n1_death').verbose_name),
        'cholera_case_28': ExcelFormField(
            'G9', int,
            EpidemiologyR._meta.get_field('cholera_case').verbose_name),
        'cholera_death_28': ExcelFormField(
            'G10', int,
            EpidemiologyR._meta.get_field('cholera_death').verbose_name),
        'red_diarrhea_case_28': ExcelFormField(
            'H9', int,
            EpidemiologyR._meta.get_field('red_diarrhea_case').verbose_name),
        'red_diarrhea_death_28': ExcelFormField(
            'H10', int,
            EpidemiologyR._meta.get_field('red_diarrhea_death').verbose_name),
        'measles_case_28': ExcelFormField(
            'I9', int,
            EpidemiologyR._meta.get_field('measles_case').verbose_name),
        'measles_death_28': ExcelFormField(
            'I10', int,
            EpidemiologyR._meta.get_field('measles_death').verbose_name),
        'yellow_fever_case_28': ExcelFormField(
            'J9', int,
            EpidemiologyR._meta.get_field('yellow_fever_case').verbose_name),
        'yellow_fever_death_28': ExcelFormField(
            'J10', int,
            EpidemiologyR._meta.get_field('yellow_fever_death').verbose_name),
        'neonatal_tetanus_case_28': ExcelFormField(
            'K9', int,
            EpidemiologyR._meta.get_field(
                'neonatal_tetanus_case').verbose_name),
        'neonatal_tetanus_death_28': ExcelFormField(
            'K10', int,
            EpidemiologyR._meta.get_field(
                'neonatal_tetanus_death').verbose_name),
        'meningitis_case_28': ExcelFormField(
            'L9', int,
            EpidemiologyR._meta.get_field('meningitis_case').verbose_name),
        'meningitis_death_28': ExcelFormField(
            'L10', int,
            EpidemiologyR._meta.get_field('meningitis_death').verbose_name),
        'rabies_case_28': ExcelFormField(
            'M9', int,
            EpidemiologyR._meta.get_field('rabies_case').verbose_name),
        'rabies_death_28': ExcelFormField(
            'M10', int,
            EpidemiologyR._meta.get_field('rabies_death').verbose_name),
        'acute_measles_diarrhea_case_28': ExcelFormField(
            'N9', int,
            EpidemiologyR._meta.get_field(
                'acute_measles_diarrhea_case').verbose_name),
        'acute_measles_diarrhea_death_28': ExcelFormField(
            'N10', int,
            EpidemiologyR._meta.get_field(
                'acute_measles_diarrhea_death').verbose_name),
        'other_notifiable_disease_case_28': ExcelFormField(
            'O9', int,
            EpidemiologyR._meta.get_field(
                'other_notifiable_disease_case').verbose_name),
        'other_notifiable_disease_death_28': ExcelFormField(
            'O10', int,
            EpidemiologyR._meta.get_field(
                'other_notifiable_disease_death').verbose_name),

        # line 29
        'snisi_code_29': ExcelFormField('A9', text_type, _("Health Center")),
        'ebola_case_29': ExcelFormField(
            'D9', int,
            EpidemiologyR._meta.get_field('ebola_case').verbose_name),
        'ebola_death_29': ExcelFormField(
            'D10', int,
            EpidemiologyR._meta.get_field('ebola_death').verbose_name),
        'acute_flaccid_paralysis_case_29': ExcelFormField(
            'E9', int,
            EpidemiologyR._meta.get_field(
                'acute_flaccid_paralysis_case').verbose_name),
        'acute_flaccid_paralysis_death_29': ExcelFormField(
            'E10', int,
            EpidemiologyR._meta.get_field(
                'acute_flaccid_paralysis_death').verbose_name),
        'influenza_a_h1n1_case_29': ExcelFormField(
            'F9', int,
            EpidemiologyR._meta.get_field(
                'influenza_a_h1n1_case').verbose_name),
        'influenza_a_h1n1_death_29': ExcelFormField(
            'F10', int,
            EpidemiologyR._meta.get_field(
                'influenza_a_h1n1_death').verbose_name),
        'cholera_case_29': ExcelFormField(
            'G9', int,
            EpidemiologyR._meta.get_field('cholera_case').verbose_name),
        'cholera_death_29': ExcelFormField(
            'G10', int,
            EpidemiologyR._meta.get_field('cholera_death').verbose_name),
        'red_diarrhea_case_29': ExcelFormField(
            'H9', int,
            EpidemiologyR._meta.get_field('red_diarrhea_case').verbose_name),
        'red_diarrhea_death_29': ExcelFormField(
            'H10', int,
            EpidemiologyR._meta.get_field('red_diarrhea_death').verbose_name),
        'measles_case_29': ExcelFormField(
            'I9', int,
            EpidemiologyR._meta.get_field('measles_case').verbose_name),
        'measles_death_29': ExcelFormField(
            'I10', int,
            EpidemiologyR._meta.get_field('measles_death').verbose_name),
        'yellow_fever_case_29': ExcelFormField(
            'J9', int,
            EpidemiologyR._meta.get_field('yellow_fever_case').verbose_name),
        'yellow_fever_death_29': ExcelFormField(
            'J10', int,
            EpidemiologyR._meta.get_field('yellow_fever_death').verbose_name),
        'neonatal_tetanus_case_29': ExcelFormField(
            'K9', int,
            EpidemiologyR._meta.get_field(
                'neonatal_tetanus_case').verbose_name),
        'neonatal_tetanus_death_29': ExcelFormField(
            'K10', int,
            EpidemiologyR._meta.get_field(
                'neonatal_tetanus_death').verbose_name),
        'meningitis_case_29': ExcelFormField(
            'L9', int,
            EpidemiologyR._meta.get_field('meningitis_case').verbose_name),
        'meningitis_death_29': ExcelFormField(
            'L10', int,
            EpidemiologyR._meta.get_field('meningitis_death').verbose_name),
        'rabies_case_29': ExcelFormField(
            'M9', int,
            EpidemiologyR._meta.get_field('rabies_case').verbose_name),
        'rabies_death_29': ExcelFormField(
            'M10', int,
            EpidemiologyR._meta.get_field('rabies_death').verbose_name),
        'acute_measles_diarrhea_case_29': ExcelFormField(
            'N9', int,
            EpidemiologyR._meta.get_field(
                'acute_measles_diarrhea_case').verbose_name),
        'acute_measles_diarrhea_death_29': ExcelFormField(
            'N10', int,
            EpidemiologyR._meta.get_field(
                'acute_measles_diarrhea_death').verbose_name),
        'other_notifiable_disease_case_29': ExcelFormField(
            'O9', int,
            EpidemiologyR._meta.get_field(
                'other_notifiable_disease_case').verbose_name),
        'other_notifiable_disease_death_29': ExcelFormField(
            'O10', int,
            EpidemiologyR._meta.get_field(
                'other_notifiable_disease_death').verbose_name),

        # line 30
        'snisi_code_30': ExcelFormField('A9', text_type, _("Health Center")),
        'ebola_case_30': ExcelFormField(
            'D9', int,
            EpidemiologyR._meta.get_field('ebola_case').verbose_name),
        'ebola_death_30': ExcelFormField(
            'D10', int,
            EpidemiologyR._meta.get_field('ebola_death').verbose_name),
        'acute_flaccid_paralysis_case_30': ExcelFormField(
            'E9', int,
            EpidemiologyR._meta.get_field(
                'acute_flaccid_paralysis_case').verbose_name),
        'acute_flaccid_paralysis_death_30': ExcelFormField(
            'E10', int,
            EpidemiologyR._meta.get_field(
                'acute_flaccid_paralysis_death').verbose_name),
        'influenza_a_h1n1_case_30': ExcelFormField(
            'F9', int,
            EpidemiologyR._meta.get_field(
                'influenza_a_h1n1_case').verbose_name),
        'influenza_a_h1n1_death_30': ExcelFormField(
            'F10', int,
            EpidemiologyR._meta.get_field(
                'influenza_a_h1n1_death').verbose_name),
        'cholera_case_30': ExcelFormField(
            'G9', int,
            EpidemiologyR._meta.get_field('cholera_case').verbose_name),
        'cholera_death_30': ExcelFormField(
            'G10', int,
            EpidemiologyR._meta.get_field('cholera_death').verbose_name),
        'red_diarrhea_case_30': ExcelFormField(
            'H9', int,
            EpidemiologyR._meta.get_field('red_diarrhea_case').verbose_name),
        'red_diarrhea_death_30': ExcelFormField(
            'H10', int,
            EpidemiologyR._meta.get_field('red_diarrhea_death').verbose_name),
        'measles_case_30': ExcelFormField(
            'I9', int,
            EpidemiologyR._meta.get_field('measles_case').verbose_name),
        'measles_death_30': ExcelFormField(
            'I10', int,
            EpidemiologyR._meta.get_field('measles_death').verbose_name),
        'yellow_fever_case_30': ExcelFormField(
            'J9', int,
            EpidemiologyR._meta.get_field('yellow_fever_case').verbose_name),
        'yellow_fever_death_30': ExcelFormField(
            'J10', int,
            EpidemiologyR._meta.get_field('yellow_fever_death').verbose_name),
        'neonatal_tetanus_case_30': ExcelFormField(
            'K9', int,
            EpidemiologyR._meta.get_field(
                'neonatal_tetanus_case').verbose_name),
        'neonatal_tetanus_death_30': ExcelFormField(
            'K10', int,
            EpidemiologyR._meta.get_field(
                'neonatal_tetanus_death').verbose_name),
        'meningitis_case_30': ExcelFormField(
            'L9', int,
            EpidemiologyR._meta.get_field('meningitis_case').verbose_name),
        'meningitis_death_30': ExcelFormField(
            'L10', int,
            EpidemiologyR._meta.get_field('meningitis_death').verbose_name),
        'rabies_case_30': ExcelFormField(
            'M9', int,
            EpidemiologyR._meta.get_field('rabies_case').verbose_name),
        'rabies_death_30': ExcelFormField(
            'M10', int,
            EpidemiologyR._meta.get_field('rabies_death').verbose_name),
        'acute_measles_diarrhea_case_30': ExcelFormField(
            'N9', int,
            EpidemiologyR._meta.get_field(
                'acute_measles_diarrhea_case').verbose_name),
        'acute_measles_diarrhea_death_30': ExcelFormField(
            'N10', int,
            EpidemiologyR._meta.get_field(
                'acute_measles_diarrhea_death').verbose_name),
        'other_notifiable_disease_case_30': ExcelFormField(
            'O9', int,
            EpidemiologyR._meta.get_field(
                'other_notifiable_disease_case').verbose_name),
        'other_notifiable_disease_death_30': ExcelFormField(
            'O10', int,
            EpidemiologyR._meta.get_field(
                'other_notifiable_disease_death').verbose_name),

        # line 31
        'snisi_code_31': ExcelFormField('A9', text_type, _("Health Center")),
        'ebola_case_31': ExcelFormField(
            'D9', int,
            EpidemiologyR._meta.get_field('ebola_case').verbose_name),
        'ebola_death_31': ExcelFormField(
            'D10', int,
            EpidemiologyR._meta.get_field('ebola_death').verbose_name),
        'acute_flaccid_paralysis_case_31': ExcelFormField(
            'E9', int,
            EpidemiologyR._meta.get_field(
                'acute_flaccid_paralysis_case').verbose_name),
        'acute_flaccid_paralysis_death_31': ExcelFormField(
            'E10', int,
            EpidemiologyR._meta.get_field(
                'acute_flaccid_paralysis_death').verbose_name),
        'influenza_a_h1n1_case_31': ExcelFormField(
            'F9', int,
            EpidemiologyR._meta.get_field(
                'influenza_a_h1n1_case').verbose_name),
        'influenza_a_h1n1_death_31': ExcelFormField(
            'F10', int,
            EpidemiologyR._meta.get_field(
                'influenza_a_h1n1_death').verbose_name),
        'cholera_case_31': ExcelFormField(
            'G9', int,
            EpidemiologyR._meta.get_field('cholera_case').verbose_name),
        'cholera_death_31': ExcelFormField(
            'G10', int,
            EpidemiologyR._meta.get_field('cholera_death').verbose_name),
        'red_diarrhea_case_31': ExcelFormField(
            'H9', int,
            EpidemiologyR._meta.get_field('red_diarrhea_case').verbose_name),
        'red_diarrhea_death_31': ExcelFormField(
            'H10', int,
            EpidemiologyR._meta.get_field('red_diarrhea_death').verbose_name),
        'measles_case_31': ExcelFormField(
            'I9', int,
            EpidemiologyR._meta.get_field('measles_case').verbose_name),
        'measles_death_31': ExcelFormField(
            'I10', int,
            EpidemiologyR._meta.get_field('measles_death').verbose_name),
        'yellow_fever_case_31': ExcelFormField(
            'J9', int,
            EpidemiologyR._meta.get_field('yellow_fever_case').verbose_name),
        'yellow_fever_death_31': ExcelFormField(
            'J10', int,
            EpidemiologyR._meta.get_field('yellow_fever_death').verbose_name),
        'neonatal_tetanus_case_31': ExcelFormField(
            'K9', int,
            EpidemiologyR._meta.get_field(
                'neonatal_tetanus_case').verbose_name),
        'neonatal_tetanus_death_31': ExcelFormField(
            'K10', int,
            EpidemiologyR._meta.get_field(
                'neonatal_tetanus_death').verbose_name),
        'meningitis_case_31': ExcelFormField(
            'L9', int,
            EpidemiologyR._meta.get_field('meningitis_case').verbose_name),
        'meningitis_death_31': ExcelFormField(
            'L10', int,
            EpidemiologyR._meta.get_field('meningitis_death').verbose_name),
        'rabies_case_31': ExcelFormField(
            'M9', int,
            EpidemiologyR._meta.get_field('rabies_case').verbose_name),
        'rabies_death_31': ExcelFormField(
            'M10', int,
            EpidemiologyR._meta.get_field('rabies_death').verbose_name),
        'acute_measles_diarrhea_case_31': ExcelFormField(
            'N9', int,
            EpidemiologyR._meta.get_field(
                'acute_measles_diarrhea_case').verbose_name),
        'acute_measles_diarrhea_death_31': ExcelFormField(
            'N10', int,
            EpidemiologyR._meta.get_field(
                'acute_measles_diarrhea_death').verbose_name),
        'other_notifiable_disease_case_31': ExcelFormField(
            'O9', int,
            EpidemiologyR._meta.get_field(
                'other_notifiable_disease_case').verbose_name),
        'other_notifiable_disease_death_31': ExcelFormField(
            'O10', int,
            EpidemiologyR._meta.get_field(
                'other_notifiable_disease_death').verbose_name),

        # line 32
        'snisi_code_32': ExcelFormField('A9', text_type, _("Health Center")),
        'ebola_case_32': ExcelFormField(
            'D9', int,
            EpidemiologyR._meta.get_field('ebola_case').verbose_name),
        'ebola_death_32': ExcelFormField(
            'D10', int,
            EpidemiologyR._meta.get_field('ebola_death').verbose_name),
        'acute_flaccid_paralysis_case_32': ExcelFormField(
            'E9', int,
            EpidemiologyR._meta.get_field(
                'acute_flaccid_paralysis_case').verbose_name),
        'acute_flaccid_paralysis_death_32': ExcelFormField(
            'E10', int,
            EpidemiologyR._meta.get_field(
                'acute_flaccid_paralysis_death').verbose_name),
        'influenza_a_h1n1_case_32': ExcelFormField(
            'F9', int,
            EpidemiologyR._meta.get_field(
                'influenza_a_h1n1_case').verbose_name),
        'influenza_a_h1n1_death_32': ExcelFormField(
            'F10', int,
            EpidemiologyR._meta.get_field(
                'influenza_a_h1n1_death').verbose_name),
        'cholera_case_32': ExcelFormField(
            'G9', int,
            EpidemiologyR._meta.get_field('cholera_case').verbose_name),
        'cholera_death_32': ExcelFormField(
            'G10', int,
            EpidemiologyR._meta.get_field('cholera_death').verbose_name),
        'red_diarrhea_case_32': ExcelFormField(
            'H9', int,
            EpidemiologyR._meta.get_field('red_diarrhea_case').verbose_name),
        'red_diarrhea_death_32': ExcelFormField(
            'H10', int,
            EpidemiologyR._meta.get_field('red_diarrhea_death').verbose_name),
        'measles_case_32': ExcelFormField(
            'I9', int,
            EpidemiologyR._meta.get_field('measles_case').verbose_name),
        'measles_death_32': ExcelFormField(
            'I10', int,
            EpidemiologyR._meta.get_field('measles_death').verbose_name),
        'yellow_fever_case_32': ExcelFormField(
            'J9', int,
            EpidemiologyR._meta.get_field('yellow_fever_case').verbose_name),
        'yellow_fever_death_32': ExcelFormField(
            'J10', int,
            EpidemiologyR._meta.get_field('yellow_fever_death').verbose_name),
        'neonatal_tetanus_case_32': ExcelFormField(
            'K9', int,
            EpidemiologyR._meta.get_field(
                'neonatal_tetanus_case').verbose_name),
        'neonatal_tetanus_death_32': ExcelFormField(
            'K10', int,
            EpidemiologyR._meta.get_field(
                'neonatal_tetanus_death').verbose_name),
        'meningitis_case_32': ExcelFormField(
            'L9', int,
            EpidemiologyR._meta.get_field('meningitis_case').verbose_name),
        'meningitis_death_32': ExcelFormField(
            'L10', int,
            EpidemiologyR._meta.get_field('meningitis_death').verbose_name),
        'rabies_case_32': ExcelFormField(
            'M9', int,
            EpidemiologyR._meta.get_field('rabies_case').verbose_name),
        'rabies_death_32': ExcelFormField(
            'M10', int,
            EpidemiologyR._meta.get_field('rabies_death').verbose_name),
        'acute_measles_diarrhea_case_32': ExcelFormField(
            'N9', int,
            EpidemiologyR._meta.get_field(
                'acute_measles_diarrhea_case').verbose_name),
        'acute_measles_diarrhea_death_32': ExcelFormField(
            'N10', int,
            EpidemiologyR._meta.get_field(
                'acute_measles_diarrhea_death').verbose_name),
        'other_notifiable_disease_case_32': ExcelFormField(
            'O9', int,
            EpidemiologyR._meta.get_field(
                'other_notifiable_disease_case').verbose_name),
        'other_notifiable_disease_death_32': ExcelFormField(
            'O10', int,
            EpidemiologyR._meta.get_field(
                'other_notifiable_disease_death').verbose_name),

        # line 33
        'snisi_code_33': ExcelFormField('A9', text_type, _("Health Center")),
        'ebola_case_33': ExcelFormField(
            'D9', int,
            EpidemiologyR._meta.get_field('ebola_case').verbose_name),
        'ebola_death_33': ExcelFormField(
            'D10', int,
            EpidemiologyR._meta.get_field('ebola_death').verbose_name),
        'acute_flaccid_paralysis_case_33': ExcelFormField(
            'E9', int,
            EpidemiologyR._meta.get_field(
                'acute_flaccid_paralysis_case').verbose_name),
        'acute_flaccid_paralysis_death_33': ExcelFormField(
            'E10', int,
            EpidemiologyR._meta.get_field(
                'acute_flaccid_paralysis_death').verbose_name),
        'influenza_a_h1n1_case_33': ExcelFormField(
            'F9', int,
            EpidemiologyR._meta.get_field(
                'influenza_a_h1n1_case').verbose_name),
        'influenza_a_h1n1_death_33': ExcelFormField(
            'F10', int,
            EpidemiologyR._meta.get_field(
                'influenza_a_h1n1_death').verbose_name),
        'cholera_case_33': ExcelFormField(
            'G9', int,
            EpidemiologyR._meta.get_field('cholera_case').verbose_name),
        'cholera_death_33': ExcelFormField(
            'G10', int,
            EpidemiologyR._meta.get_field('cholera_death').verbose_name),
        'red_diarrhea_case_33': ExcelFormField(
            'H9', int,
            EpidemiologyR._meta.get_field('red_diarrhea_case').verbose_name),
        'red_diarrhea_death_33': ExcelFormField(
            'H10', int,
            EpidemiologyR._meta.get_field('red_diarrhea_death').verbose_name),
        'measles_case_33': ExcelFormField(
            'I9', int,
            EpidemiologyR._meta.get_field('measles_case').verbose_name),
        'measles_death_33': ExcelFormField(
            'I10', int,
            EpidemiologyR._meta.get_field('measles_death').verbose_name),
        'yellow_fever_case_33': ExcelFormField(
            'J9', int,
            EpidemiologyR._meta.get_field('yellow_fever_case').verbose_name),
        'yellow_fever_death_33': ExcelFormField(
            'J10', int,
            EpidemiologyR._meta.get_field('yellow_fever_death').verbose_name),
        'neonatal_tetanus_case_33': ExcelFormField(
            'K9', int,
            EpidemiologyR._meta.get_field(
                'neonatal_tetanus_case').verbose_name),
        'neonatal_tetanus_death_33': ExcelFormField(
            'K10', int,
            EpidemiologyR._meta.get_field(
                'neonatal_tetanus_death').verbose_name),
        'meningitis_case_33': ExcelFormField(
            'L9', int,
            EpidemiologyR._meta.get_field('meningitis_case').verbose_name),
        'meningitis_death_33': ExcelFormField(
            'L10', int,
            EpidemiologyR._meta.get_field('meningitis_death').verbose_name),
        'rabies_case_33': ExcelFormField(
            'M9', int,
            EpidemiologyR._meta.get_field('rabies_case').verbose_name),
        'rabies_death_33': ExcelFormField(
            'M10', int,
            EpidemiologyR._meta.get_field('rabies_death').verbose_name),
        'acute_measles_diarrhea_case_33': ExcelFormField(
            'N9', int,
            EpidemiologyR._meta.get_field(
                'acute_measles_diarrhea_case').verbose_name),
        'acute_measles_diarrhea_death_33': ExcelFormField(
            'N10', int,
            EpidemiologyR._meta.get_field(
                'acute_measles_diarrhea_death').verbose_name),
        'other_notifiable_disease_case_33': ExcelFormField(
            'O9', int,
            EpidemiologyR._meta.get_field(
                'other_notifiable_disease_case').verbose_name),
        'other_notifiable_disease_death_33': ExcelFormField(
            'O10', int,
            EpidemiologyR._meta.get_field(
                'other_notifiable_disease_death').verbose_name),

        # line 34
        'snisi_code_34': ExcelFormField('A9', text_type, _("Health Center")),
        'ebola_case_34': ExcelFormField(
            'D9', int,
            EpidemiologyR._meta.get_field('ebola_case').verbose_name),
        'ebola_death_34': ExcelFormField(
            'D10', int,
            EpidemiologyR._meta.get_field('ebola_death').verbose_name),
        'acute_flaccid_paralysis_case_34': ExcelFormField(
            'E9', int,
            EpidemiologyR._meta.get_field(
                'acute_flaccid_paralysis_case').verbose_name),
        'acute_flaccid_paralysis_death_34': ExcelFormField(
            'E10', int,
            EpidemiologyR._meta.get_field(
                'acute_flaccid_paralysis_death').verbose_name),
        'influenza_a_h1n1_case_34': ExcelFormField(
            'F9', int,
            EpidemiologyR._meta.get_field(
                'influenza_a_h1n1_case').verbose_name),
        'influenza_a_h1n1_death_34': ExcelFormField(
            'F10', int,
            EpidemiologyR._meta.get_field(
                'influenza_a_h1n1_death').verbose_name),
        'cholera_case_34': ExcelFormField(
            'G9', int,
            EpidemiologyR._meta.get_field('cholera_case').verbose_name),
        'cholera_death_34': ExcelFormField(
            'G10', int,
            EpidemiologyR._meta.get_field('cholera_death').verbose_name),
        'red_diarrhea_case_34': ExcelFormField(
            'H9', int,
            EpidemiologyR._meta.get_field('red_diarrhea_case').verbose_name),
        'red_diarrhea_death_34': ExcelFormField(
            'H10', int,
            EpidemiologyR._meta.get_field('red_diarrhea_death').verbose_name),
        'measles_case_34': ExcelFormField(
            'I9', int,
            EpidemiologyR._meta.get_field('measles_case').verbose_name),
        'measles_death_34': ExcelFormField(
            'I10', int,
            EpidemiologyR._meta.get_field('measles_death').verbose_name),
        'yellow_fever_case_34': ExcelFormField(
            'J9', int,
            EpidemiologyR._meta.get_field('yellow_fever_case').verbose_name),
        'yellow_fever_death_34': ExcelFormField(
            'J10', int,
            EpidemiologyR._meta.get_field('yellow_fever_death').verbose_name),
        'neonatal_tetanus_case_34': ExcelFormField(
            'K9', int,
            EpidemiologyR._meta.get_field(
                'neonatal_tetanus_case').verbose_name),
        'neonatal_tetanus_death_34': ExcelFormField(
            'K10', int,
            EpidemiologyR._meta.get_field(
                'neonatal_tetanus_death').verbose_name),
        'meningitis_case_34': ExcelFormField(
            'L9', int,
            EpidemiologyR._meta.get_field('meningitis_case').verbose_name),
        'meningitis_death_34': ExcelFormField(
            'L10', int,
            EpidemiologyR._meta.get_field('meningitis_death').verbose_name),
        'rabies_case_34': ExcelFormField(
            'M9', int,
            EpidemiologyR._meta.get_field('rabies_case').verbose_name),
        'rabies_death_34': ExcelFormField(
            'M10', int,
            EpidemiologyR._meta.get_field('rabies_death').verbose_name),
        'acute_measles_diarrhea_case_34': ExcelFormField(
            'N9', int,
            EpidemiologyR._meta.get_field(
                'acute_measles_diarrhea_case').verbose_name),
        'acute_measles_diarrhea_death_34': ExcelFormField(
            'N10', int,
            EpidemiologyR._meta.get_field(
                'acute_measles_diarrhea_death').verbose_name),
        'other_notifiable_disease_case_34': ExcelFormField(
            'O9', int,
            EpidemiologyR._meta.get_field(
                'other_notifiable_disease_case').verbose_name),
        'other_notifiable_disease_death_34': ExcelFormField(
            'O10', int,
            EpidemiologyR._meta.get_field(
                'other_notifiable_disease_death').verbose_name),

        # line 35
        'snisi_code_35': ExcelFormField('A9', text_type, _("Health Center")),
        'ebola_case_35': ExcelFormField(
            'D9', int,
            EpidemiologyR._meta.get_field('ebola_case').verbose_name),
        'ebola_death_35': ExcelFormField(
            'D10', int,
            EpidemiologyR._meta.get_field('ebola_death').verbose_name),
        'acute_flaccid_paralysis_case_35': ExcelFormField(
            'E9', int,
            EpidemiologyR._meta.get_field(
                'acute_flaccid_paralysis_case').verbose_name),
        'acute_flaccid_paralysis_death_35': ExcelFormField(
            'E10', int,
            EpidemiologyR._meta.get_field(
                'acute_flaccid_paralysis_death').verbose_name),
        'influenza_a_h1n1_case_35': ExcelFormField(
            'F9', int,
            EpidemiologyR._meta.get_field(
                'influenza_a_h1n1_case').verbose_name),
        'influenza_a_h1n1_death_35': ExcelFormField(
            'F10', int,
            EpidemiologyR._meta.get_field(
                'influenza_a_h1n1_death').verbose_name),
        'cholera_case_35': ExcelFormField(
            'G9', int,
            EpidemiologyR._meta.get_field('cholera_case').verbose_name),
        'cholera_death_35': ExcelFormField(
            'G10', int,
            EpidemiologyR._meta.get_field('cholera_death').verbose_name),
        'red_diarrhea_case_35': ExcelFormField(
            'H9', int,
            EpidemiologyR._meta.get_field('red_diarrhea_case').verbose_name),
        'red_diarrhea_death_35': ExcelFormField(
            'H10', int,
            EpidemiologyR._meta.get_field('red_diarrhea_death').verbose_name),
        'measles_case_35': ExcelFormField(
            'I9', int,
            EpidemiologyR._meta.get_field('measles_case').verbose_name),
        'measles_death_35': ExcelFormField(
            'I10', int,
            EpidemiologyR._meta.get_field('measles_death').verbose_name),
        'yellow_fever_case_35': ExcelFormField(
            'J9', int,
            EpidemiologyR._meta.get_field('yellow_fever_case').verbose_name),
        'yellow_fever_death_35': ExcelFormField(
            'J10', int,
            EpidemiologyR._meta.get_field('yellow_fever_death').verbose_name),
        'neonatal_tetanus_case_35': ExcelFormField(
            'K9', int,
            EpidemiologyR._meta.get_field(
                'neonatal_tetanus_case').verbose_name),
        'neonatal_tetanus_death_35': ExcelFormField(
            'K10', int,
            EpidemiologyR._meta.get_field(
                'neonatal_tetanus_death').verbose_name),
        'meningitis_case_35': ExcelFormField(
            'L9', int,
            EpidemiologyR._meta.get_field('meningitis_case').verbose_name),
        'meningitis_death_35': ExcelFormField(
            'L10', int,
            EpidemiologyR._meta.get_field('meningitis_death').verbose_name),
        'rabies_case_35': ExcelFormField(
            'M9', int,
            EpidemiologyR._meta.get_field('rabies_case').verbose_name),
        'rabies_death_35': ExcelFormField(
            'M10', int,
            EpidemiologyR._meta.get_field('rabies_death').verbose_name),
        'acute_measles_diarrhea_case_35': ExcelFormField(
            'N9', int,
            EpidemiologyR._meta.get_field(
                'acute_measles_diarrhea_case').verbose_name),
        'acute_measles_diarrhea_death_35': ExcelFormField(
            'N10', int,
            EpidemiologyR._meta.get_field(
                'acute_measles_diarrhea_death').verbose_name),
        'other_notifiable_disease_case_35': ExcelFormField(
            'O9', int,
            EpidemiologyR._meta.get_field(
                'other_notifiable_disease_case').verbose_name),
        'other_notifiable_disease_death_35': ExcelFormField(
            'O10', int,
            EpidemiologyR._meta.get_field(
                'other_notifiable_disease_death').verbose_name),

        # line 36
        'snisi_code_36': ExcelFormField('A9', text_type, _("Health Center")),
        'ebola_case_36': ExcelFormField(
            'D9', int,
            EpidemiologyR._meta.get_field('ebola_case').verbose_name),
        'ebola_death_36': ExcelFormField(
            'D10', int,
            EpidemiologyR._meta.get_field('ebola_death').verbose_name),
        'acute_flaccid_paralysis_case_36': ExcelFormField(
            'E9', int,
            EpidemiologyR._meta.get_field(
                'acute_flaccid_paralysis_case').verbose_name),
        'acute_flaccid_paralysis_death_36': ExcelFormField(
            'E10', int,
            EpidemiologyR._meta.get_field(
                'acute_flaccid_paralysis_death').verbose_name),
        'influenza_a_h1n1_case_36': ExcelFormField(
            'F9', int,
            EpidemiologyR._meta.get_field(
                'influenza_a_h1n1_case').verbose_name),
        'influenza_a_h1n1_death_36': ExcelFormField(
            'F10', int,
            EpidemiologyR._meta.get_field(
                'influenza_a_h1n1_death').verbose_name),
        'cholera_case_36': ExcelFormField(
            'G9', int,
            EpidemiologyR._meta.get_field('cholera_case').verbose_name),
        'cholera_death_36': ExcelFormField(
            'G10', int,
            EpidemiologyR._meta.get_field('cholera_death').verbose_name),
        'red_diarrhea_case_36': ExcelFormField(
            'H9', int,
            EpidemiologyR._meta.get_field('red_diarrhea_case').verbose_name),
        'red_diarrhea_death_36': ExcelFormField(
            'H10', int,
            EpidemiologyR._meta.get_field('red_diarrhea_death').verbose_name),
        'measles_case_36': ExcelFormField(
            'I9', int,
            EpidemiologyR._meta.get_field('measles_case').verbose_name),
        'measles_death_36': ExcelFormField(
            'I10', int,
            EpidemiologyR._meta.get_field('measles_death').verbose_name),
        'yellow_fever_case_36': ExcelFormField(
            'J9', int,
            EpidemiologyR._meta.get_field('yellow_fever_case').verbose_name),
        'yellow_fever_death_36': ExcelFormField(
            'J10', int,
            EpidemiologyR._meta.get_field('yellow_fever_death').verbose_name),
        'neonatal_tetanus_case_36': ExcelFormField(
            'K9', int,
            EpidemiologyR._meta.get_field(
                'neonatal_tetanus_case').verbose_name),
        'neonatal_tetanus_death_36': ExcelFormField(
            'K10', int,
            EpidemiologyR._meta.get_field(
                'neonatal_tetanus_death').verbose_name),
        'meningitis_case_36': ExcelFormField(
            'L9', int,
            EpidemiologyR._meta.get_field('meningitis_case').verbose_name),
        'meningitis_death_36': ExcelFormField(
            'L10', int,
            EpidemiologyR._meta.get_field('meningitis_death').verbose_name),
        'rabies_case_36': ExcelFormField(
            'M9', int,
            EpidemiologyR._meta.get_field('rabies_case').verbose_name),
        'rabies_death_36': ExcelFormField(
            'M10', int,
            EpidemiologyR._meta.get_field('rabies_death').verbose_name),
        'acute_measles_diarrhea_case_36': ExcelFormField(
            'N9', int,
            EpidemiologyR._meta.get_field(
                'acute_measles_diarrhea_case').verbose_name),
        'acute_measles_diarrhea_death_36': ExcelFormField(
            'N10', int,
            EpidemiologyR._meta.get_field(
                'acute_measles_diarrhea_death').verbose_name),
        'other_notifiable_disease_case_36': ExcelFormField(
            'O9', int,
            EpidemiologyR._meta.get_field(
                'other_notifiable_disease_case').verbose_name),
        'other_notifiable_disease_death_36': ExcelFormField(
            'O10', int,
            EpidemiologyR._meta.get_field(
                'other_notifiable_disease_death').verbose_name),

        # line 37
        'snisi_code_37': ExcelFormField('A9', text_type, _("Health Center")),
        'ebola_case_37': ExcelFormField(
            'D9', int,
            EpidemiologyR._meta.get_field('ebola_case').verbose_name),
        'ebola_death_37': ExcelFormField(
            'D10', int,
            EpidemiologyR._meta.get_field('ebola_death').verbose_name),
        'acute_flaccid_paralysis_case_37': ExcelFormField(
            'E9', int,
            EpidemiologyR._meta.get_field(
                'acute_flaccid_paralysis_case').verbose_name),
        'acute_flaccid_paralysis_death_37': ExcelFormField(
            'E10', int,
            EpidemiologyR._meta.get_field(
                'acute_flaccid_paralysis_death').verbose_name),
        'influenza_a_h1n1_case_37': ExcelFormField(
            'F9', int,
            EpidemiologyR._meta.get_field(
                'influenza_a_h1n1_case').verbose_name),
        'influenza_a_h1n1_death_37': ExcelFormField(
            'F10', int,
            EpidemiologyR._meta.get_field(
                'influenza_a_h1n1_death').verbose_name),
        'cholera_case_37': ExcelFormField(
            'G9', int,
            EpidemiologyR._meta.get_field('cholera_case').verbose_name),
        'cholera_death_37': ExcelFormField(
            'G10', int,
            EpidemiologyR._meta.get_field('cholera_death').verbose_name),
        'red_diarrhea_case_37': ExcelFormField(
            'H9', int,
            EpidemiologyR._meta.get_field('red_diarrhea_case').verbose_name),
        'red_diarrhea_death_37': ExcelFormField(
            'H10', int,
            EpidemiologyR._meta.get_field('red_diarrhea_death').verbose_name),
        'measles_case_37': ExcelFormField(
            'I9', int,
            EpidemiologyR._meta.get_field('measles_case').verbose_name),
        'measles_death_37': ExcelFormField(
            'I10', int,
            EpidemiologyR._meta.get_field('measles_death').verbose_name),
        'yellow_fever_case_37': ExcelFormField(
            'J9', int,
            EpidemiologyR._meta.get_field('yellow_fever_case').verbose_name),
        'yellow_fever_death_37': ExcelFormField(
            'J10', int,
            EpidemiologyR._meta.get_field('yellow_fever_death').verbose_name),
        'neonatal_tetanus_case_37': ExcelFormField(
            'K9', int,
            EpidemiologyR._meta.get_field(
                'neonatal_tetanus_case').verbose_name),
        'neonatal_tetanus_death_37': ExcelFormField(
            'K10', int,
            EpidemiologyR._meta.get_field(
                'neonatal_tetanus_death').verbose_name),
        'meningitis_case_37': ExcelFormField(
            'L9', int,
            EpidemiologyR._meta.get_field('meningitis_case').verbose_name),
        'meningitis_death_37': ExcelFormField(
            'L10', int,
            EpidemiologyR._meta.get_field('meningitis_death').verbose_name),
        'rabies_case_37': ExcelFormField(
            'M9', int,
            EpidemiologyR._meta.get_field('rabies_case').verbose_name),
        'rabies_death_37': ExcelFormField(
            'M10', int,
            EpidemiologyR._meta.get_field('rabies_death').verbose_name),
        'acute_measles_diarrhea_case_37': ExcelFormField(
            'N9', int,
            EpidemiologyR._meta.get_field(
                'acute_measles_diarrhea_case').verbose_name),
        'acute_measles_diarrhea_death_37': ExcelFormField(
            'N10', int,
            EpidemiologyR._meta.get_field(
                'acute_measles_diarrhea_death').verbose_name),
        'other_notifiable_disease_case_37': ExcelFormField(
            'O9', int,
            EpidemiologyR._meta.get_field(
                'other_notifiable_disease_case').verbose_name),
        'other_notifiable_disease_death_37': ExcelFormField(
            'O10', int,
            EpidemiologyR._meta.get_field(
                'other_notifiable_disease_death').verbose_name),

        # line 38
        'snisi_code_38': ExcelFormField('A9', text_type, _("Health Center")),
        'ebola_case_38': ExcelFormField(
            'D9', int,
            EpidemiologyR._meta.get_field('ebola_case').verbose_name),
        'ebola_death_38': ExcelFormField(
            'D10', int,
            EpidemiologyR._meta.get_field('ebola_death').verbose_name),
        'acute_flaccid_paralysis_case_38': ExcelFormField(
            'E9', int,
            EpidemiologyR._meta.get_field(
                'acute_flaccid_paralysis_case').verbose_name),
        'acute_flaccid_paralysis_death_38': ExcelFormField(
            'E10', int,
            EpidemiologyR._meta.get_field(
                'acute_flaccid_paralysis_death').verbose_name),
        'influenza_a_h1n1_case_38': ExcelFormField(
            'F9', int,
            EpidemiologyR._meta.get_field(
                'influenza_a_h1n1_case').verbose_name),
        'influenza_a_h1n1_death_38': ExcelFormField(
            'F10', int,
            EpidemiologyR._meta.get_field(
                'influenza_a_h1n1_death').verbose_name),
        'cholera_case_38': ExcelFormField(
            'G9', int,
            EpidemiologyR._meta.get_field('cholera_case').verbose_name),
        'cholera_death_38': ExcelFormField(
            'G10', int,
            EpidemiologyR._meta.get_field('cholera_death').verbose_name),
        'red_diarrhea_case_38': ExcelFormField(
            'H9', int,
            EpidemiologyR._meta.get_field('red_diarrhea_case').verbose_name),
        'red_diarrhea_death_38': ExcelFormField(
            'H10', int,
            EpidemiologyR._meta.get_field('red_diarrhea_death').verbose_name),
        'measles_case_38': ExcelFormField(
            'I9', int,
            EpidemiologyR._meta.get_field('measles_case').verbose_name),
        'measles_death_38': ExcelFormField(
            'I10', int,
            EpidemiologyR._meta.get_field('measles_death').verbose_name),
        'yellow_fever_case_38': ExcelFormField(
            'J9', int,
            EpidemiologyR._meta.get_field('yellow_fever_case').verbose_name),
        'yellow_fever_death_38': ExcelFormField(
            'J10', int,
            EpidemiologyR._meta.get_field('yellow_fever_death').verbose_name),
        'neonatal_tetanus_case_38': ExcelFormField(
            'K9', int,
            EpidemiologyR._meta.get_field(
                'neonatal_tetanus_case').verbose_name),
        'neonatal_tetanus_death_38': ExcelFormField(
            'K10', int,
            EpidemiologyR._meta.get_field(
                'neonatal_tetanus_death').verbose_name),
        'meningitis_case_38': ExcelFormField(
            'L9', int,
            EpidemiologyR._meta.get_field('meningitis_case').verbose_name),
        'meningitis_death_38': ExcelFormField(
            'L10', int,
            EpidemiologyR._meta.get_field('meningitis_death').verbose_name),
        'rabies_case_38': ExcelFormField(
            'M9', int,
            EpidemiologyR._meta.get_field('rabies_case').verbose_name),
        'rabies_death_38': ExcelFormField(
            'M10', int,
            EpidemiologyR._meta.get_field('rabies_death').verbose_name),
        'acute_measles_diarrhea_case_38': ExcelFormField(
            'N9', int,
            EpidemiologyR._meta.get_field(
                'acute_measles_diarrhea_case').verbose_name),
        'acute_measles_diarrhea_death_38': ExcelFormField(
            'N10', int,
            EpidemiologyR._meta.get_field(
                'acute_measles_diarrhea_death').verbose_name),
        'other_notifiable_disease_case_38': ExcelFormField(
            'O9', int,
            EpidemiologyR._meta.get_field(
                'other_notifiable_disease_case').verbose_name),
        'other_notifiable_disease_death_38': ExcelFormField(
            'O10', int,
            EpidemiologyR._meta.get_field(
                'other_notifiable_disease_death').verbose_name),

        # line 39
        'snisi_code_39': ExcelFormField('A9', text_type, _("Health Center")),
        'ebola_case_39': ExcelFormField(
            'D9', int,
            EpidemiologyR._meta.get_field('ebola_case').verbose_name),
        'ebola_death_39': ExcelFormField(
            'D10', int,
            EpidemiologyR._meta.get_field('ebola_death').verbose_name),
        'acute_flaccid_paralysis_case_39': ExcelFormField(
            'E9', int,
            EpidemiologyR._meta.get_field(
                'acute_flaccid_paralysis_case').verbose_name),
        'acute_flaccid_paralysis_death_39': ExcelFormField(
            'E10', int,
            EpidemiologyR._meta.get_field(
                'acute_flaccid_paralysis_death').verbose_name),
        'influenza_a_h1n1_case_39': ExcelFormField(
            'F9', int,
            EpidemiologyR._meta.get_field(
                'influenza_a_h1n1_case').verbose_name),
        'influenza_a_h1n1_death_39': ExcelFormField(
            'F10', int,
            EpidemiologyR._meta.get_field(
                'influenza_a_h1n1_death').verbose_name),
        'cholera_case_39': ExcelFormField(
            'G9', int,
            EpidemiologyR._meta.get_field('cholera_case').verbose_name),
        'cholera_death_39': ExcelFormField(
            'G10', int,
            EpidemiologyR._meta.get_field('cholera_death').verbose_name),
        'red_diarrhea_case_39': ExcelFormField(
            'H9', int,
            EpidemiologyR._meta.get_field('red_diarrhea_case').verbose_name),
        'red_diarrhea_death_39': ExcelFormField(
            'H10', int,
            EpidemiologyR._meta.get_field('red_diarrhea_death').verbose_name),
        'measles_case_39': ExcelFormField(
            'I9', int,
            EpidemiologyR._meta.get_field('measles_case').verbose_name),
        'measles_death_39': ExcelFormField(
            'I10', int,
            EpidemiologyR._meta.get_field('measles_death').verbose_name),
        'yellow_fever_case_39': ExcelFormField(
            'J9', int,
            EpidemiologyR._meta.get_field('yellow_fever_case').verbose_name),
        'yellow_fever_death_39': ExcelFormField(
            'J10', int,
            EpidemiologyR._meta.get_field('yellow_fever_death').verbose_name),
        'neonatal_tetanus_case_39': ExcelFormField(
            'K9', int,
            EpidemiologyR._meta.get_field(
                'neonatal_tetanus_case').verbose_name),
        'neonatal_tetanus_death_39': ExcelFormField(
            'K10', int,
            EpidemiologyR._meta.get_field(
                'neonatal_tetanus_death').verbose_name),
        'meningitis_case_39': ExcelFormField(
            'L9', int,
            EpidemiologyR._meta.get_field('meningitis_case').verbose_name),
        'meningitis_death_39': ExcelFormField(
            'L10', int,
            EpidemiologyR._meta.get_field('meningitis_death').verbose_name),
        'rabies_case_39': ExcelFormField(
            'M9', int,
            EpidemiologyR._meta.get_field('rabies_case').verbose_name),
        'rabies_death_39': ExcelFormField(
            'M10', int,
            EpidemiologyR._meta.get_field('rabies_death').verbose_name),
        'acute_measles_diarrhea_case_39': ExcelFormField(
            'N9', int,
            EpidemiologyR._meta.get_field(
                'acute_measles_diarrhea_case').verbose_name),
        'acute_measles_diarrhea_death_39': ExcelFormField(
            'N10', int,
            EpidemiologyR._meta.get_field(
                'acute_measles_diarrhea_death').verbose_name),
        'other_notifiable_disease_case_39': ExcelFormField(
            'O9', int,
            EpidemiologyR._meta.get_field(
                'other_notifiable_disease_case').verbose_name),
        'other_notifiable_disease_death_39': ExcelFormField(
            'O10', int,
            EpidemiologyR._meta.get_field(
                'other_notifiable_disease_death').verbose_name),

        # line 40
        'snisi_code_40': ExcelFormField('A9', text_type, _("Health Center")),
        'ebola_case_40': ExcelFormField(
            'D9', int,
            EpidemiologyR._meta.get_field('ebola_case').verbose_name),
        'ebola_death_40': ExcelFormField(
            'D10', int,
            EpidemiologyR._meta.get_field('ebola_death').verbose_name),
        'acute_flaccid_paralysis_case_40': ExcelFormField(
            'E9', int,
            EpidemiologyR._meta.get_field(
                'acute_flaccid_paralysis_case').verbose_name),
        'acute_flaccid_paralysis_death_40': ExcelFormField(
            'E10', int,
            EpidemiologyR._meta.get_field(
                'acute_flaccid_paralysis_death').verbose_name),
        'influenza_a_h1n1_case_40': ExcelFormField(
            'F9', int,
            EpidemiologyR._meta.get_field(
                'influenza_a_h1n1_case').verbose_name),
        'influenza_a_h1n1_death_40': ExcelFormField(
            'F10', int,
            EpidemiologyR._meta.get_field(
                'influenza_a_h1n1_death').verbose_name),
        'cholera_case_40': ExcelFormField(
            'G9', int,
            EpidemiologyR._meta.get_field('cholera_case').verbose_name),
        'cholera_death_40': ExcelFormField(
            'G10', int,
            EpidemiologyR._meta.get_field('cholera_death').verbose_name),
        'red_diarrhea_case_40': ExcelFormField(
            'H9', int,
            EpidemiologyR._meta.get_field('red_diarrhea_case').verbose_name),
        'red_diarrhea_death_40': ExcelFormField(
            'H10', int,
            EpidemiologyR._meta.get_field('red_diarrhea_death').verbose_name),
        'measles_case_40': ExcelFormField(
            'I9', int,
            EpidemiologyR._meta.get_field('measles_case').verbose_name),
        'measles_death_40': ExcelFormField(
            'I10', int,
            EpidemiologyR._meta.get_field('measles_death').verbose_name),
        'yellow_fever_case_40': ExcelFormField(
            'J9', int,
            EpidemiologyR._meta.get_field('yellow_fever_case').verbose_name),
        'yellow_fever_death_40': ExcelFormField(
            'J10', int,
            EpidemiologyR._meta.get_field('yellow_fever_death').verbose_name),
        'neonatal_tetanus_case_40': ExcelFormField(
            'K9', int,
            EpidemiologyR._meta.get_field(
                'neonatal_tetanus_case').verbose_name),
        'neonatal_tetanus_death_40': ExcelFormField(
            'K10', int,
            EpidemiologyR._meta.get_field(
                'neonatal_tetanus_death').verbose_name),
        'meningitis_case_40': ExcelFormField(
            'L9', int,
            EpidemiologyR._meta.get_field('meningitis_case').verbose_name),
        'meningitis_death_40': ExcelFormField(
            'L10', int,
            EpidemiologyR._meta.get_field('meningitis_death').verbose_name),
        'rabies_case_40': ExcelFormField(
            'M9', int,
            EpidemiologyR._meta.get_field('rabies_case').verbose_name),
        'rabies_death_40': ExcelFormField(
            'M10', int,
            EpidemiologyR._meta.get_field('rabies_death').verbose_name),
        'acute_measles_diarrhea_case_40': ExcelFormField(
            'N9', int,
            EpidemiologyR._meta.get_field(
                'acute_measles_diarrhea_case').verbose_name),
        'acute_measles_diarrhea_death_40': ExcelFormField(
            'N10', int,
            EpidemiologyR._meta.get_field(
                'acute_measles_diarrhea_death').verbose_name),
        'other_notifiable_disease_case_40': ExcelFormField(
            'O9', int,
            EpidemiologyR._meta.get_field(
                'other_notifiable_disease_case').verbose_name),
        'other_notifiable_disease_death_40': ExcelFormField(
            'O10', int,
            EpidemiologyR._meta.get_field(
                'other_notifiable_disease_death').verbose_name),

        }
    }

    def create_report(self, provider):
        # expected_reporting = self.get('expected_reporting')

        reports = []
        msgs = []

        # for expected_reporting in self.expected_reportings:
        for zrow, entity in enumerate(self.entities):
            # skip the district if present
            if entity.slug == self.get('entity').slug:
                continue
            row = zrow + 1
            expected_reporting = self.expected_reportings[zrow]
            checker = EpidemiologyRIntegrityChecker()
            checker.set('entity', entity)
            checker.set('period', self.get('period'))
            checker.set('submit_time', self.get('submit_time'))
            checker.set('hc', self.get('entity').slug)
            checker.set('day', self.get('day'))
            checker.set('month', self.get('month'))
            checker.set('year', self.get('year'))
            checker.set('submitter', self.get('submitter'))
            for field in EpidemiologyR.data_fields():
                checker.set(field, self.get('{}_{}'.format(field, row)))
            checker.check()
            if not checker.is_valid():
                report = None
                msg = checker.errors.pop().render(short=False)
                msgs.append(msg)
            else:
                report, msg = create_epid_report(
                    provider=provider,
                    expected_reporting=expected_reporting,
                    completed_on=timezone.now(),
                    integrity_checker=checker,
                    data_source=self.filepath)
                reports.append(report)
                msgs.append(msg)
        return reports[-1], "\n".join(msgs)

EXPORTED_FORMS = [
    (class_str(EpidemiologyExcelForm), "Routine Hebdomadaire SMIR"),
    (class_str(EpidemiologyDistrictExcelForm),
     "Routine Hebdomadaire SMIR (District)")
]
