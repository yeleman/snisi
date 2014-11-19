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
from snisi_tools.misc import class_str
from snisi_nutrition.integrity import (NutritionRIntegrityChecker,
                                       create_nut_report)

from snisi_nutrition.models import (URENAM, URENAS, URENI)

logger = logging.getLogger(__name__)


class NutritionExcelForm(NutritionRIntegrityChecker, ExcelForm):

    STOCKS = "INTRANTS"
    URENAMURENAS = "URENAM-URENAS"
    URENI = "URENI"

    MONTH_MAP = range(1, 13)
    YEAR_MAP = range(2014, 2021)

    _mapping = {'0.1': {
        'hc': ExcelFormField(
            'B5', text_type, _("Health Center"), sheet=STOCKS),
        'month': ExcelFormField(
            'F3', type_converters.NormalizedIntChoiceList,
            _("Month"), cast_args=MONTH_MAP, sheet=STOCKS),
        'year': ExcelFormField(
            'F4', type_converters.NormalizedIntChoiceList,
            _("Year"), cast_args=YEAR_MAP, sheet=STOCKS),
        }

        # URENAM-URENAS
        # URENAM
        'u23o6_total_start_m': ExcelFormField(
            "C15", int,
            URENAM._meta.get_field(
                'u23o6_total_start_m').verbose_name, sheet.URENAMURENAS)
        'u23o6_total_start_f': ExcelFormField(
            "D15", int,
            URENAM._meta.get_field(
                'u23o6_total_start_f').verbose_name, sheet.URENAMURENAS)
        'u23o6_new_cases': ExcelFormField(
            "E15", int,
            URENAM._meta.get_field(
                'u23o6_new_cases').verbose_name, sheet.URENAMURENAS)
        'u23o6_returned': ExcelFormField(
            "H15", int,
            URENAM._meta.get_field(
                'u23o6_returned').verbose_name, sheet.URENAMURENAS)
        'u23o6_total_in_m': ExcelFormField(
            "L15", int,
            URENAM._meta.get_field(
                'u23o6_total_in_m').verbose_name, sheet.URENAMURENAS)
        'u23o6_total_in_f': ExcelFormField(
            "M15", int,
            URENAM._meta.get_field(
                'u23o6_total_in_f').verbose_name, sheet.URENAMURENAS)
        'u23o6_healed': ExcelFormField(
            "B30", int,
            URENAM._meta.get_field(
                'u23o6_healed').verbose_name, sheet.URENAMURENAS)
        'u23o6_deceased': ExcelFormField(
            "D30", int,
            URENAM._meta.get_field(
                'u23o6_deceased').verbose_name, sheet.URENAMURENAS)
        'u23o6_abandon': ExcelFormField(
            "F30", int,
            URENAM._meta.get_field(
                'u23o6_abandon').verbose_name, sheet.URENAMURENAS)
        'u23o6_not_responding': ExcelFormField(
            "H30", int,
            URENAM._meta.get_field(
                'u23o6_not_responding').verbose_name, sheet.URENAMURENAS)
        'u23o6_total_out_m': ExcelFormField(
            "K30", int,
            URENAM._meta.get_field(
                'u23o6_total_out_m').verbose_name, sheet.URENAMURENAS)
        'u23o6_total_out_f': ExcelFormField(
            "L30", int,
            URENAM._meta.get_field(
                'u23o6_total_out_f').verbose_name, sheet.URENAMURENAS)
        'u23o6_referred': ExcelFormField(
            "M30", int,
            URENAM._meta.get_field(
                'u23o6_referred').verbose_name, sheet.URENAMURENAS)
        'u23o6_total_end_m': ExcelFormField(
            "Q30", int,
            URENAM._meta.get_field(
                'u23o6_total_end_m').verbose_name, sheet.URENAMURENAS)
        'u23o6_total_end_f': ExcelFormField(
            "R30", int,
            URENAM._meta.get_field(
                'u23o6_total_end_f').verbose_name, sheet.URENAMURENAS)
        'u59o23_total_start_m': ExcelFormField(
            "C16", int,
            URENAM._meta.get_field(
                'u59o23_total_start_m').verbose_name, sheet.URENAMURENAS)
        'u59o23_total_start_f': ExcelFormField(
            "D16", int,
            URENAM._meta.get_field(
                'u59o23_total_start_f').verbose_name, sheet.URENAMURENAS)
        'u59o23_new_cases': ExcelFormField(
            "E16", int,
            URENAM._meta.get_field(
                'u59o23_new_cases').verbose_name, sheet.URENAMURENAS)
        'u59o23_returned': ExcelFormField(
            "H16", int,
            URENAM._meta.get_field(
                'u59o23_returned').verbose_name, sheet.URENAMURENAS)
        'u59o23_total_in_m': ExcelFormField(
            "L16", int,
            URENAM._meta.get_field(
                'u59o23_total_in_m').verbose_name, sheet.URENAMURENAS)
        'u59o23_total_in_f': ExcelFormField(
            "M16", int,
            URENAM._meta.get_field(
                'u59o23_total_in_f').verbose_name, sheet.URENAMURENAS)
        'u59o23_healed': ExcelFormField(
            "B31", int,
            URENAM._meta.get_field(
                'u59o23_healed').verbose_name, sheet.URENAMURENAS)
        'u59o23_deceased': ExcelFormField(
            "D31", int,
            URENAM._meta.get_field(
                'u59o23_deceased').verbose_name, sheet.URENAMURENAS)
        'u59o23_abandon': ExcelFormField(
            "F31", int,
            URENAM._meta.get_field(
                'u59o23_abandon').verbose_name, sheet.URENAMURENAS)
        'u59o23_not_responding': ExcelFormField(
            "H31", int,
            URENAM._meta.get_field(
                'u59o23_not_responding').verbose_name, sheet.URENAMURENAS)
        'u59o23_total_out_m': ExcelFormField(
            "K31", int,
            URENAM._meta.get_field(
                'u59o23_total_out_m').verbose_name, sheet.URENAMURENAS)
        'u59o23_total_out_f': ExcelFormField(
            "L31", int,
            URENAM._meta.get_field(
                'u59o23_total_out_f').verbose_name, sheet.URENAMURENAS)
        'u59o23_referred': ExcelFormField(
            "M31", int,
            URENAM._meta.get_field(
                'u59o23_referred').verbose_name, sheet.URENAMURENAS)
        'u59o23_total_end_m': ExcelFormField(
            "Q31", int,
            URENAM._meta.get_field(
                'u59o23_total_end_m').verbose_name, sheet.URENAMURENAS)
        'u59o23_total_end_f': ExcelFormField(
            "R31", int,
            URENAM._meta.get_field(
                'u59o23_total_end_f').verbose_name, sheet.URENAMURENAS)
        'o59_total_start_m': ExcelFormField(
            "C17", int,
            URENAM._meta.get_field(
                'o59_total_start_m').verbose_name, sheet.URENAMURENAS)
        'o59_total_start_f': ExcelFormField(
            "D17", int,
            URENAM._meta.get_field(
                'o59_total_start_f').verbose_name, sheet.URENAMURENAS)
        'o59_new_cases': ExcelFormField(
            "E17", int,
            URENAM._meta.get_field(
                'o59_new_cases').verbose_name, sheet.URENAMURENAS)
        'o59_returned': ExcelFormField(
            "H17", int,
            URENAM._meta.get_field(
                'o59_returned').verbose_name, sheet.URENAMURENAS)
        'o59_total_in_m': ExcelFormField(
            "L17", int,
            URENAM._meta.get_field(
                'o59_total_in_m').verbose_name, sheet.URENAMURENAS)
        'o59_total_in_f': ExcelFormField(
            "M17", int,
            URENAM._meta.get_field(
                'o59_total_in_f').verbose_name, sheet.URENAMURENAS)
        'o59_healed': ExcelFormField(
            "B32", int,
            URENAM._meta.get_field(
                'o59_healed').verbose_name, sheet.URENAMURENAS)
        'o59_deceased': ExcelFormField(
            "D32", int,
            URENAM._meta.get_field(
                'o59_deceased').verbose_name, sheet.URENAMURENAS)
        'o59_abandon': ExcelFormField(
            "F32", int,
            URENAM._meta.get_field(
                'o59_abandon').verbose_name, sheet.URENAMURENAS)
        'o59_not_responding': ExcelFormField(
            "H32", int,
            URENAM._meta.get_field(
                'o59_not_responding').verbose_name, sheet.URENAMURENAS)
        'o59_total_out_m': ExcelFormField(
            "K32", int,
            URENAM._meta.get_field(
                'o59_total_out_m').verbose_name, sheet.URENAMURENAS)
        'o59_total_out_f': ExcelFormField(
            "L32", int,
            URENAM._meta.get_field(
                'o59_total_out_f').verbose_name, sheet.URENAMURENAS)
        'o59_referred': ExcelFormField(
            "M32", int,
            URENAM._meta.get_field(
                'o59_referred').verbose_name, sheet.URENAMURENAS)
        'o59_total_end_m': ExcelFormField(
            "Q32", int,
            URENAM._meta.get_field(
                'o59_total_end_m').verbose_name, sheet.URENAMURENAS)
        'o59_total_end_f': ExcelFormField(
            "R32", int,
            URENAM._meta.get_field(
                'o59_total_end_f').verbose_name, sheet.URENAMURENAS)
        'pw_total_start_f': ExcelFormField(
            "D18", int,
            URENAM._meta.get_field(
                'pw_total_start_f').verbose_name, sheet.URENAMURENAS)
        'pw_new_cases': ExcelFormField(
            "E18", int,
            URENAM._meta.get_field(
                'pw_new_cases').verbose_name, sheet.URENAMURENAS)
        'pw_returned': ExcelFormField(
            "H18", int,
            URENAM._meta.get_field(
                'pw_returned').verbose_name, sheet.URENAMURENAS)
        'pw_total_in_f': ExcelFormField(
            "M18", int,
            URENAM._meta.get_field(
                'pw_total_in_f').verbose_name, sheet.URENAMURENAS)
        'pw_healed': ExcelFormField(
            "B33", int,
            URENAM._meta.get_field(
                'pw_healed').verbose_name, sheet.URENAMURENAS)
        'pw_deceased': ExcelFormField(
            "D33", int,
            URENAM._meta.get_field(
                'pw_deceased').verbose_name, sheet.URENAMURENAS)
        'pw_abandon': ExcelFormField(
            "F33", int,
            URENAM._meta.get_field(
                'pw_abandon').verbose_name, sheet.URENAMURENAS)
        'pw_not_responding': ExcelFormField(
            "H33", int,
            URENAM._meta.get_field(
                'pw_not_responding').verbose_name, sheet.URENAMURENAS)
        'pw_total_out_f': ExcelFormField(
            "L33", int,
            URENAM._meta.get_field(
                'pw_total_out_f').verbose_name, sheet.URENAMURENAS)
        'pw_referred': ExcelFormField(
            "M33", int,
            URENAM._meta.get_field(
                'pw_referred').verbose_name, sheet.URENAMURENAS)
        'pw_total_end_f': ExcelFormField(
            "R33", int,
            URENAM._meta.get_field(
                'pw_total_end_f').verbose_name, sheet.URENAMURENAS)
        'exsam_total_start_m': ExcelFormField(
            "", int,
            URENAM._meta.get_field(
                'exsam_total_start_m').verbose_name, sheet.URENAMURENAS)
        'exsam_total_start_f': ExcelFormField(
            "", int,
            URENAM._meta.get_field(
                'exsam_total_start_f').verbose_name, sheet.URENAMURENAS)
        'exsam_total_out_m': ExcelFormField(
            "", int,
            URENAM._meta.get_field(
                'exsam_total_out_m').verbose_name, sheet.URENAMURENAS)
        'exsam_total_out_f': ExcelFormField(
            "", int,
            URENAM._meta.get_field(
                'exsam_total_out_f').verbose_name, sheet.URENAMURENAS)
        'exsam_referred': ExcelFormField(
            "", int,
            URENAM._meta.get_field(
                'exsam_referred').verbose_name, sheet.URENAMURENAS)
        'exsam_total_end_m': ExcelFormField(
            "", int,
            URENAM._meta.get_field(
                'exsam_total_end_m').verbose_name, sheet.URENAMURENAS)
        'exsam_total_end_f': ExcelFormField(
            "", int,
            URENAM._meta.get_field(
                'exsam_total_end_f').verbose_name, sheet.URENAMURENAS)
        # URENAS
        'u59o6_total_start_m': ExcelFormField(
            "C11", int,
            URENAS._meta.get_field(
                'u59o6_total_start_m').verbose_name, sheet.URENAMURENAS)
        'u59o6_total_start_f': ExcelFormField(
            "D11", int,
            URENAS._meta.get_field(
                'u59o6_total_start_f').verbose_name, sheet.URENAMURENAS)
        'u59o6_new_cases': ExcelFormField(
            "E11", int,
            URENAS._meta.get_field(
                'u59o6_new_cases').verbose_name, sheet.URENAMURENAS)
        'u59o6_returned': ExcelFormField(
            "H11", int,
            URENAS._meta.get_field(
                'u59o6_returned').verbose_name, sheet.URENAMURENAS)
        'u59o6_total_in_m': ExcelFormField(
            "L11", int,
            URENAS._meta.get_field(
                'u59o6_total_in_m').verbose_name, sheet.URENAMURENAS)
        'u59o6_total_in_f': ExcelFormField(
            "M11", int,
            URENAS._meta.get_field(
                'u59o6_total_in_f').verbose_name, sheet.URENAMURENAS)
        'u59o6_transferred': ExcelFormField(
            "N11", int,
            URENAS._meta.get_field(
                'u59o6_transferred').verbose_name, sheet.URENAMURENAS)
        'u59o6_healed': ExcelFormField(
            "B26", int,
            URENAS._meta.get_field(
                'u59o6_healed').verbose_name, sheet.URENAMURENAS)
        'u59o6_deceased': ExcelFormField(
            "D26", int,
            URENAS._meta.get_field(
                'u59o6_deceased').verbose_name, sheet.URENAMURENAS)
        'u59o6_abandon': ExcelFormField(
            "F26", int,
            URENAS._meta.get_field(
                'u59o6_abandon').verbose_name, sheet.URENAMURENAS)
        'u59o6_not_responding': ExcelFormField(
            "H26", int,
            URENAS._meta.get_field(
                'u59o6_not_responding').verbose_name, sheet.URENAMURENAS)
        'u59o6_total_out_m': ExcelFormField(
            "K26", int,
            URENAS._meta.get_field(
                'u59o6_total_out_m').verbose_name, sheet.URENAMURENAS)
        'u59o6_total_out_f': ExcelFormField(
            "L26", int,
            URENAS._meta.get_field(
                'u59o6_total_out_f').verbose_name, sheet.URENAMURENAS)
        'u59o6_referred': ExcelFormField(
            "M26", int,
            URENAS._meta.get_field(
                'u59o6_referred').verbose_name, sheet.URENAMURENAS)
        'u59o6_total_end_m': ExcelFormField(
            "Q26", int,
            URENAS._meta.get_field(
                'u59o6_total_end_m').verbose_name, sheet.URENAMURENAS)
        'u59o6_total_end_f': ExcelFormField(
            "R26", int,
            URENAS._meta.get_field(
                'u59o6_total_end_f').verbose_name, sheet.URENAMURENAS)
        'o59_total_start_m': ExcelFormField(
            "C12", int,
            URENAS._meta.get_field(
                'o59_total_start_m').verbose_name, sheet.URENAMURENAS)
        'o59_total_start_f': ExcelFormField(
            "D12", int,
            URENAS._meta.get_field(
                'o59_total_start_f').verbose_name, sheet.URENAMURENAS)
        'o59_new_cases': ExcelFormField(
            "E12", int,
            URENAS._meta.get_field(
                'o59_new_cases').verbose_name, sheet.URENAMURENAS)
        'o59_returned': ExcelFormField(
            "H12", int,
            URENAS._meta.get_field(
                'o59_returned').verbose_name, sheet.URENAMURENAS)
        'o59_total_in_m': ExcelFormField(
            "L12", int,
            URENAS._meta.get_field(
                'o59_total_in_m').verbose_name, sheet.URENAMURENAS)
        'o59_total_in_f': ExcelFormField(
            "M12", int,
            URENAS._meta.get_field(
                'o59_total_in_f').verbose_name, sheet.URENAMURENAS)
        'o59_transferred': ExcelFormField(
            "N12", int,
            URENAS._meta.get_field(
                'o59_transferred').verbose_name, sheet.URENAMURENAS)
        'o59_healed': ExcelFormField(
            "B27", int,
            URENAS._meta.get_field(
                'o59_healed').verbose_name, sheet.URENAMURENAS)
        'o59_deceased': ExcelFormField(
            "D27", int,
            URENAS._meta.get_field(
                'o59_deceased').verbose_name, sheet.URENAMURENAS)
        'o59_abandon': ExcelFormField(
            "F27", int,
            URENAS._meta.get_field(
                'o59_abandon').verbose_name, sheet.URENAMURENAS)
        'o59_not_responding': ExcelFormField(
            "H27", int,
            URENAS._meta.get_field(
                'o59_not_responding').verbose_name, sheet.URENAMURENAS)
        'o59_total_out_m': ExcelFormField(
            "K27", int,
            URENAS._meta.get_field(
                'o59_total_out_m').verbose_name, sheet.URENAMURENAS)
        'o59_total_out_f': ExcelFormField(
            "L27", int,
            URENAS._meta.get_field(
                'o59_total_out_f').verbose_name, sheet.URENAMURENAS)
        'o59_referred': ExcelFormField(
            "M27", int,
            URENAS._meta.get_field(
                'o59_referred').verbose_name, sheet.URENAMURENAS)
        'o59_total_end_m': ExcelFormField(
            "Q27", int,
            URENAS._meta.get_field(
                'o59_total_end_m').verbose_name, sheet.URENAMURENAS)
        'o59_total_end_f': ExcelFormField(
            "R27", int,
            URENAS._meta.get_field(
                'o59_total_end_f').verbose_name, sheet.URENAMURENAS)
        # URENI
        'u6_total_start_m': ExcelFormField(
            "C11", int,
            URENI._meta.get_field(
                'u6_total_start_m').verbose_name, sheet=URENI)
        'u6_total_start_f': ExcelFormField(
            "D11", int,
            URENI._meta.get_field(
                'u6_total_start_f').verbose_name, sheet=URENI)
        'u6_new_cases': ExcelFormField(
            "E11", int,
            URENI._meta.get_field(
                'u6_new_cases').verbose_name, sheet=URENI)
        'u6_returned': ExcelFormField(
            "H11", int,
            URENI._meta.get_field(
                'u6_returned').verbose_name, sheet=URENI)
        'u6_total_in_m': ExcelFormField(
            "L11", int,
            URENI._meta.get_field(
                'u6_total_in_m').verbose_name, sheet=URENI)
        'u6_total_in_f': ExcelFormField(
            "M11", int,
            URENI._meta.get_field(
                'u6_total_in_f').verbose_name, sheet=URENI)
        'u6_transferred': ExcelFormField(
            "N11", int,
            URENI._meta.get_field(
                'u6_transferred').verbose_name, sheet=URENI)
        'u6_healed': ExcelFormField(
            "B20", int,
            URENI._meta.get_field(
                'u6_healed').verbose_name, sheet=URENI)
        'u6_deceased': ExcelFormField(
            "D20", int,
            URENI._meta.get_field(
                'u6_deceased').verbose_name, sheet=URENI)
        'u6_abandon': ExcelFormField(
            "F20", int,
            URENI._meta.get_field(
                'u6_abandon').verbose_name, sheet=URENI)
        'u6_not_responding': ExcelFormField(
            "H20", int,
            URENI._meta.get_field(
                'u6_not_responding').verbose_name, sheet=URENI)
        'u6_total_out_m': ExcelFormField(
            "K20", int,
            URENI._meta.get_field(
                'u6_total_out_m').verbose_name, sheet=URENI)
        'u6_total_out_f': ExcelFormField(
            "L20", int,
            URENI._meta.get_field(
                'u6_total_out_f').verbose_name, sheet=URENI)
        'u6_referred': ExcelFormField(
            "M20", int,
            URENI._meta.get_field(
                'u6_referred').verbose_name, sheet=URENI)
        'u6_total_end_m': ExcelFormField(
            "Q20", int,
            URENI._meta.get_field(
                'u6_total_end_m').verbose_name, sheet=URENI)
        'u6_total_end_f': ExcelFormField(
            "R20", int,
            URENI._meta.get_field(
                'u6_total_end_f').verbose_name, sheet=URENI)
        'u59o6_total_start_m': ExcelFormField(
            "C12", int,
            URENI._meta.get_field(
                'u59o6_total_start_m').verbose_name, sheet=URENI)
        'u59o6_total_start_f': ExcelFormField(
            "D12", int,
            URENI._meta.get_field(
                'u59o6_total_start_f').verbose_name, sheet=URENI)
        'u59o6_new_cases': ExcelFormField(
            "E12", int,
            URENI._meta.get_field(
                'u59o6_new_cases').verbose_name, sheet=URENI)
        'u59o6_returned': ExcelFormField(
            "H12", int,
            URENI._meta.get_field(
                'u59o6_returned').verbose_name, sheet=URENI)
        'u59o6_total_in_m': ExcelFormField(
            "L12", int,
            URENI._meta.get_field(
                'u59o6_total_in_m').verbose_name, sheet=URENI)
        'u59o6_total_in_f': ExcelFormField(
            "M12", int,
            URENI._meta.get_field(
                'u59o6_total_in_f').verbose_name, sheet=URENI)
        'u59o6_transferred': ExcelFormField(
            "N12", int,
            URENI._meta.get_field(
                'u59o6_transferred').verbose_name, sheet=URENI)
        'u59o6_healed': ExcelFormField(
            "B21", int,
            URENI._meta.get_field(
                'u59o6_healed').verbose_name, sheet=URENI)
        'u59o6_deceased': ExcelFormField(
            "D21", int,
            URENI._meta.get_field(
                'u59o6_deceased').verbose_name, sheet=URENI)
        'u59o6_abandon': ExcelFormField(
            "F21", int,
            URENI._meta.get_field(
                'u59o6_abandon').verbose_name, sheet=URENI)
        'u59o6_not_responding': ExcelFormField(
            "H21", int,
            URENI._meta.get_field(
                'u59o6_not_responding').verbose_name, sheet=URENI)
        'u59o6_total_out_m': ExcelFormField(
            "K21", int,
            URENI._meta.get_field(
                'u59o6_total_out_m').verbose_name, sheet=URENI)
        'u59o6_total_out_f': ExcelFormField(
            "L21", int,
            URENI._meta.get_field(
                'u59o6_total_out_f').verbose_name, sheet=URENI)
        'u59o6_referred': ExcelFormField(
            "M21", int,
            URENI._meta.get_field(
                'u59o6_referred').verbose_name, sheet=URENI)
        'u59o6_total_end_m': ExcelFormField(
            "Q21", int,
            URENI._meta.get_field(
                'u59o6_total_end_m').verbose_name, sheet=URENI)
        'u59o6_total_end_f': ExcelFormField(
            "R21", int,
            URENI._meta.get_field(
                'u59o6_total_end_f').verbose_name, sheet=URENI)
        'o59_total_start_m': ExcelFormField(
            "C13", int,
            URENI._meta.get_field(
                'o59_total_start_m').verbose_name, sheet=URENI)
        'o59_total_start_f': ExcelFormField(
            "D13", int,
            URENI._meta.get_field(
                'o59_total_start_f').verbose_name, sheet=URENI)
        'o59_new_cases': ExcelFormField(
            "E13", int,
            URENI._meta.get_field(
                'o59_new_cases').verbose_name, sheet=URENI)
        'o59_returned': ExcelFormField(
            "H13", int,
            URENI._meta.get_field(
                'o59_returned').verbose_name, sheet=URENI)
        'o59_total_in_m': ExcelFormField(
            "L13", int,
            URENI._meta.get_field(
                'o59_total_in_m').verbose_name, sheet=URENI)
        'o59_total_in_f': ExcelFormField(
            "M13", int,
            URENI._meta.get_field(
                'o59_total_in_f').verbose_name, sheet=URENI)
        'o59_transferred': ExcelFormField(
            "N13", int,
            URENI._meta.get_field(
                'o59_transferred').verbose_name, sheet=URENI)
        'o59_healed': ExcelFormField(
            "B22", int,
            URENI._meta.get_field(
                'o59_healed').verbose_name, sheet=URENI)
        'o59_deceased': ExcelFormField(
            "D22", int,
            URENI._meta.get_field(
                'o59_deceased').verbose_name, sheet=URENI)
        'o59_abandon': ExcelFormField(
            "F22", int,
            URENI._meta.get_field(
                'o59_abandon').verbose_name, sheet=URENI)
        'o59_not_responding': ExcelFormField(
            "H22", int,
            URENI._meta.get_field(
                'o59_not_responding').verbose_name, sheet=URENI)
        'o59_total_out_m': ExcelFormField(
            "K22", int,
            URENI._meta.get_field(
                'o59_total_out_m').verbose_name, sheet=URENI)
        'o59_total_out_f': ExcelFormField(
            "L22", int,
            URENI._meta.get_field(
                'o59_total_out_f').verbose_name, sheet=URENI)
        'o59_referred': ExcelFormField(
            "M22", int,
            URENI._meta.get_field(
                'o59_referred').verbose_name, sheet=URENI)
        'o59_total_end_m': ExcelFormField(
            "Q22", int,
            URENI._meta.get_field(
                'o59_total_end_m').verbose_name, sheet=URENI)
        'o59_total_end_f': ExcelFormField(
            "R22", int,
            URENI._meta.get_field(
                'o59_total_end_f').verbose_name, sheet=URENI)

        # Stocts
        'plumpy_nut_initial': ExcelFormField(
            "D8", int,
            Stocks._meta.get_field(
                'plumpy_nut_initial').verbose_name, sheet=STOCKS)
        'plumpy_nut_received': ExcelFormField(
            "F8", int,
            Stocks._meta.get_field(
                'plumpy_nut_received').verbose_name, sheet=STOCKS)
        'plumpy_nut_used': ExcelFormField(
            "H8", int,
            Stocks._meta.get_field(
                'plumpy_nut_used').verbose_name, sheet=STOCKS)
        'plumpy_nut_lost': ExcelFormField(
            "J8", int,
            Stocks._meta.get_field(
                'plumpy_nut_lost').verbose_name, sheet=STOCKS)
        'milk_f75_initial': ExcelFormField(
            "D9", int,
            Stocks._meta.get_field(
                'milk_f75_initial').verbose_name, sheet=STOCKS)
        'milk_f75_received': ExcelFormField(
            "F9", int,
            Stocks._meta.get_field(
                'milk_f75_received').verbose_name, sheet=STOCKS)
        'milk_f75_used': ExcelFormField(
            "H9", int,
            Stocks._meta.get_field(
                'milk_f75_used').verbose_name, sheet=STOCKS)
        'milk_f75_lost': ExcelFormField(
            "J9", int,
            Stocks._meta.get_field(
                'milk_f75_lost').verbose_name, sheet=STOCKS)
        'milk_f100_initial': ExcelFormField(
            "D10", int,
            Stocks._meta.get_field(
                'milk_f100_initial').verbose_name, sheet=STOCKS)
        'milk_f100_received': ExcelFormField(
            "F10", int,
            Stocks._meta.get_field(
                'milk_f100_received').verbose_name, sheet=STOCKS)
        'milk_f100_used': ExcelFormField(
            "H10", int,
            Stocks._meta.get_field(
                'milk_f100_used').verbose_name, sheet=STOCKS)
        'milk_f100_lost': ExcelFormField(
            "J10", int,
            Stocks._meta.get_field(
                'milk_f100_lost').verbose_name, sheet=STOCKS)
        'resomal_initial': ExcelFormField(
            "D11", int,
            Stocks._meta.get_field(
                'resomal_initial').verbose_name, sheet=STOCKS)
        'resomal_received': ExcelFormField(
            "F11", int,
            Stocks._meta.get_field(
                'resomal_received').verbose_name, sheet=STOCKS)
        'resomal_used': ExcelFormField(
            "H11", int,
            Stocks._meta.get_field(
                'resomal_used').verbose_name, sheet=STOCKS)
        'resomal_lost': ExcelFormField(
            "J11", int,
            Stocks._meta.get_field(
                'resomal_lost').verbose_name, sheet=STOCKS)
        'plumpy_sup_initial': ExcelFormField(
            "D12", int,
            Stocks._meta.get_field(
                'plumpy_sup_initial').verbose_name, sheet=STOCKS)
        'plumpy_sup_received': ExcelFormField(
            "F12", int,
            Stocks._meta.get_field(
                'plumpy_sup_received').verbose_name, sheet=STOCKS)
        'plumpy_sup_used': ExcelFormField(
            "H12", int,
            Stocks._meta.get_field(
                'plumpy_sup_used').verbose_name, sheet=STOCKS)
        'plumpy_sup_lost': ExcelFormField(
            "J12", int,
            Stocks._meta.get_field(
                'plumpy_sup_lost').verbose_name, sheet=STOCKS)
        'supercereal_initial': ExcelFormField(
            "D13", int,
            Stocks._meta.get_field(
                'supercereal_initial').verbose_name, sheet=STOCKS)
        'supercereal_received': ExcelFormField(
            "F13", int,
            Stocks._meta.get_field(
                'supercereal_received').verbose_name, sheet=STOCKS)
        'supercereal_used': ExcelFormField(
            "H13", int,
            Stocks._meta.get_field(
                'supercereal_used').verbose_name, sheet=STOCKS)
        'supercereal_lost': ExcelFormField(
            "J13", int,
            Stocks._meta.get_field(
                'supercereal_lost').verbose_name, sheet=STOCKS)
        'supercereal_plus_initial': ExcelFormField(
            "D14", int,
            Stocks._meta.get_field(
                'supercereal_plus_initial').verbose_name, sheet=STOCKS)
        'supercereal_plus_received': ExcelFormField(
            "F14", int,
            Stocks._meta.get_field(
                'supercereal_plus_received').verbose_name, sheet=STOCKS)
        'supercereal_plus_used': ExcelFormField(
            "H14", int,
            Stocks._meta.get_field(
                'supercereal_plus_used').verbose_name, sheet=STOCKS)
        'supercereal_plus_lost': ExcelFormField(
            "J14", int,
            Stocks._meta.get_field(
                'supercereal_plus_lost').verbose_name, sheet=STOCKS)
        'oil_initial': ExcelFormField(
            "D15", int,
            Stocks._meta.get_field(
                'oil_initial').verbose_name, sheet=STOCKS)
        'oil_received': ExcelFormField(
            "F15", int,
            Stocks._meta.get_field(
                'oil_received').verbose_name, sheet=STOCKS)
        'oil_used': ExcelFormField(
            "H15", int,
            Stocks._meta.get_field(
                'oil_used').verbose_name, sheet=STOCKS)
        'oil_lost': ExcelFormField(
            "J15", int,
            Stocks._meta.get_field(
                'oil_lost').verbose_name, sheet=STOCKS)
        'amoxycilline_125_vials_initial': ExcelFormField(
            "D16", int,
            Stocks._meta.get_field(
                'amoxycilline_125_vials_initial').verbose_name, sheet=STOCKS)
        'amoxycilline_125_vials_received': ExcelFormField(
            "F16", int,
            Stocks._meta.get_field(
                'amoxycilline_125_vials_received').verbose_name, sheet=STOCKS)
        'amoxycilline_125_vials_used': ExcelFormField(
            "H16", int,
            Stocks._meta.get_field(
                'amoxycilline_125_vials_used').verbose_name, sheet=STOCKS)
        'amoxycilline_125_vials_lost': ExcelFormField(
            "J16", int,
            Stocks._meta.get_field(
                'amoxycilline_125_vials_lost').verbose_name, sheet=STOCKS)
        'amoxycilline_250_caps_initial': ExcelFormField(
            "D17", int,
            Stocks._meta.get_field(
                'amoxycilline_250_caps_initial').verbose_name, sheet=STOCKS)
        'amoxycilline_250_caps_received': ExcelFormField(
            "F17", int,
            Stocks._meta.get_field(
                'amoxycilline_250_caps_received').verbose_name, sheet=STOCKS)
        'amoxycilline_250_caps_used': ExcelFormField(
            "H17", int,
            Stocks._meta.get_field(
                'amoxycilline_250_caps_used').verbose_name, sheet=STOCKS)
        'amoxycilline_250_caps_lost': ExcelFormField(
            "J17", int,
            Stocks._meta.get_field(
                'amoxycilline_250_caps_lost').verbose_name, sheet=STOCKS)
        'albendazole_400_initial': ExcelFormField(
            "D18", int,
            Stocks._meta.get_field(
                'albendazole_400_initial').verbose_name, sheet=STOCKS)
        'albendazole_400_received': ExcelFormField(
            "F18", int,
            Stocks._meta.get_field(
                'albendazole_400_received').verbose_name, sheet=STOCKS)
        'albendazole_400_used': ExcelFormField(
            "H18", int,
            Stocks._meta.get_field(
                'albendazole_400_used').verbose_name, sheet=STOCKS)
        'albendazole_400_lost': ExcelFormField(
            "J18", int,
            Stocks._meta.get_field(
                'albendazole_400_lost').verbose_name, sheet=STOCKS)
        'vita_100_injectable_initial': ExcelFormField(
            "D19", int,
            Stocks._meta.get_field(
                'vita_100_injectable_initial').verbose_name, sheet=STOCKS)
        'vita_100_injectable_received': ExcelFormField(
            "F19", int,
            Stocks._meta.get_field(
                'vita_100_injectable_received').verbose_name, sheet=STOCKS)
        'vita_100_injectable_used': ExcelFormField(
            "H19", int,
            Stocks._meta.get_field(
                'vita_100_injectable_used').verbose_name, sheet=STOCKS)
        'vita_100_injectable_lost': ExcelFormField(
            "J19", int,
            Stocks._meta.get_field(
                'vita_100_injectable_lost').verbose_name, sheet=STOCKS)
        'vita_200_injectable_initial': ExcelFormField(
            "D20", int,
            Stocks._meta.get_field(
                'vita_200_injectable_initial').verbose_name, sheet=STOCKS)
        'vita_200_injectable_received': ExcelFormField(
            "F20", int,
            Stocks._meta.get_field(
                'vita_200_injectable_received').verbose_name, sheet=STOCKS)
        'vita_200_injectable_used': ExcelFormField(
            "H20", int,
            Stocks._meta.get_field(
                'vita_200_injectable_used').verbose_name, sheet=STOCKS)
        'vita_200_injectable_lost': ExcelFormField(
            "J20", int,
            Stocks._meta.get_field(
                'vita_200_injectable_lost').verbose_name, sheet=STOCKS)
        'iron_folic_acid_initial': ExcelFormField(
            "21", int,
            Stocks._meta.get_field(
                'iron_folic_acid_initial').verbose_name, sheet=STOCKS)
        'iron_folic_acid_received': ExcelFormField(
            "21", int,
            Stocks._meta.get_field(
                'iron_folic_acid_received').verbose_name, sheet=STOCKS)
        'iron_folic_acid_used': ExcelFormField(
            "21", int,
            Stocks._meta.get_field(
                'iron_folic_acid_used').verbose_name, sheet=STOCKS)
        'iron_folic_acid_lost': ExcelFormField(
            "21", int,
            Stocks._meta.get_field(
                'iron_folic_acid_lost').verbose_name, sheet=STOCKS)

    }

    def create_report(self, provider):

        expected_reporting = self.get('expected_reporting')

        return create_nut_report(provider=provider,
                                 expected_reporting=expected_reporting,
                                 completed_on=timezone.now(),
                                 integrity_checker=self,
                                 data_source=self.filepath)

EXPORTED_FORMS = [
    (class_str(NutritionExcelForm), "Routine Mensuelle Nutrition")
]
