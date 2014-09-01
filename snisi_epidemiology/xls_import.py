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
from snisi_epidemiology.integrity import (EpidemiologyRIntegrityChecker,
                                          create_epid_report)
from snisi_epidemiology.models import EpidemiologyR

logger = logging.getLogger(__name__)


class EpidemiologyExcelForm(EpidemiologyRIntegrityChecker, ExcelForm):

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

EXPORTED_FORMS = [
    (class_str(EpidemiologyExcelForm), "Routine Hebdomadaire SMIR")
]
