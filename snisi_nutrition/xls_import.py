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

logger = logging.getLogger(__name__)


class NutritionExcelForm(NutritionRIntegrityChecker, ExcelForm):

    MONTH_MAP = range(1, 13)
    YEAR_MAP = range(2014, 2021)

    _mapping = {'0.1': {
        'hc': ExcelFormField(
            'C2', text_type, _("Health Center")),
        'month': ExcelFormField(
            'C3', type_converters.NormalizedIntChoiceList,
            _("Month"), cast_args=MONTH_MAP),
        'year': ExcelFormField(
            'E3', type_converters.NormalizedIntChoiceList,
            _("Year"), cast_args=YEAR_MAP),
        }
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
