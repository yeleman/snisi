#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

from snisi_malaria.indicators.common import MalariaIndicator
from snisi_core.indicators import ReportDataMixin


class U5TotalSimpleMalariaCases(ReportDataMixin, MalariaIndicator):
    name = "Nombre de cas simple chez les moins de 5 ans"
    report_field = 'u5_total_simple_malaria_cases'


class U5TotalTreatedMalariaCases(ReportDataMixin, MalariaIndicator):
    name = "Cas simple traités par CTA chez les moins de 5 ans"
    report_field = 'u5_total_treated_malaria_cases'


class O5TotalSimpleMalariaCases(ReportDataMixin, MalariaIndicator):
    name = "Cas simple traités par CTA chez les 5 ans et plus"
    report_field = 'o5_total_simple_malaria_cases'


class O5TotalTreatedMalariaCases(ReportDataMixin, MalariaIndicator):
    name = "Cas simple traités par CTA chez les 5 ans et plus"
    report_field = 'o5_total_treated_malaria_cases'


class PWTotalANC1(ReportDataMixin, MalariaIndicator):
    name = "Femmes enceintes reçues en CPN"
    report_field = 'pw_total_anc1'


class PWTotalDistributedBednets(ReportDataMixin, MalariaIndicator):
    name = "Total des moustiquaires distribues aux femmes enceintes"
    report_field = 'pw_total_distributed_bednets'


class PWTotalANC2(ReportDataMixin, MalariaIndicator):
    name = "Femmes enceintes ayant reçu la SP2"
    report_field = 'pw_total_sp2'
