#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

from snisi_malaria.indicators.common import MalariaIndicator
from snisi_core.indicators import ReportDataMixin


# u5_total_consultation_all_causes = models.PositiveIntegerField(_("Total Consultation All Causes"))
# u5_total_suspected_malaria_cases = models.PositiveIntegerField(_("Total Suspected Malaria Cases"))
# u5_total_simple_malaria_cases = models.PositiveIntegerField(_("Total Simple Malaria Cases"))
# u5_total_severe_malaria_cases = models.PositiveIntegerField(_("Total Severe Malaria Cases"))
# u5_total_tested_malaria_cases = models.PositiveIntegerField(_("Total Tested Malaria Cases"))
# u5_total_confirmed_malaria_cases = models.PositiveIntegerField(_("Total Confirmed Malaria Cases"))
# u5_total_treated_malaria_cases = models.PositiveIntegerField(_("Total Treated Malaria Cases"))
# u5_total_inpatient_all_causes = models.PositiveIntegerField(_("Total Inpatient All Causes"))
# u5_total_malaria_inpatient = models.PositiveIntegerField(_("Total Malaria Inpatient"))
# u5_total_death_all_causes = models.PositiveIntegerField(_("Total Death All Causes"))
# u5_total_malaria_death = models.PositiveIntegerField(_("Total Malaria Death"))
# u5_total_distributed_bednets = models.PositiveIntegerField(_("Total Distributed Bednets"))

# o5_total_consultation_all_causes = models.PositiveIntegerField(_("Total Consultation All Causes"))
# o5_total_suspected_malaria_cases = models.PositiveIntegerField(_("Total Suspected Malaria Cases"))
# o5_total_simple_malaria_cases = models.PositiveIntegerField(_("Total Simple Malaria Cases"))
# o5_total_severe_malaria_cases = models.PositiveIntegerField(_("Total Severe Malaria Cases"))
# o5_total_tested_malaria_cases = models.PositiveIntegerField(_("Total Tested Malaria Cases"))
# o5_total_confirmed_malaria_cases = models.PositiveIntegerField(_("Total Confirmed Malaria Cases"))
# o5_total_treated_malaria_cases = models.PositiveIntegerField(_("Total Treated Malaria Cases"))
# o5_total_inpatient_all_causes = models.PositiveIntegerField(_("Total Inpatient All Causes"))
# o5_total_malaria_inpatient = models.PositiveIntegerField(_("Total Malaria Inpatient"))
# o5_total_death_all_causes = models.PositiveIntegerField(_("Total Death All Causes"))
# o5_total_malaria_death = models.PositiveIntegerField(_("Total Malaria Death"))

# pw_total_consultation_all_causes = models.PositiveIntegerField(_("Total Consultation All Causes"))
# pw_total_suspected_malaria_cases = models.PositiveIntegerField(_("Total Suspected Malaria Cases"))
# pw_total_severe_malaria_cases = models.PositiveIntegerField(_("Total Severe Malaria Cases"))
# pw_total_tested_malaria_cases = models.PositiveIntegerField(_("Total Tested Malaria Cases"))
# pw_total_confirmed_malaria_cases = models.PositiveIntegerField(_("Total Confirmed Malaria Cases"))
# pw_total_treated_malaria_cases = models.PositiveIntegerField(_("Total Treated Malaria Cases"))
# pw_total_inpatient_all_causes = models.PositiveIntegerField(_("Total Inpatient All Causes"))
# pw_total_malaria_inpatient = models.PositiveIntegerField(_("Total Malaria Inpatient"))
# pw_total_death_all_causes = models.PositiveIntegerField(_("Total Death All Causes"))
# pw_total_malaria_death = models.PositiveIntegerField(_("Total Malaria Death"))
# pw_total_distributed_bednets = models.PositiveIntegerField(_("Total Distributed Bednets"))
# pw_total_anc1 = models.PositiveIntegerField(_("Total ANC1 Visits"))
# pw_total_sp1 = models.PositiveIntegerField(_("Total SP1 given"))
# pw_total_sp2 = models.PositiveIntegerField(_("Total SP2 given"))

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
