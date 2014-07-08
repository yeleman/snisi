#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging

from datetime import date

from django.utils.translation import ugettext as _

from snisi_core.integrity import (ReportIntegrityChecker,
                                  create_monthly_routine_report,
                                  RoutineIntegrityInterface)
from snisi_core.models.Roles import Role
from snisi_core.models.Reporting import ReportClass
from snisi_epidemiology import PROJECT_BRAND
from snisi_epidemiology.models import EpidemiologyR

logger = logging.getLogger(__name__)
reportcls_epidemio = ReportClass.get_or_none(slug='')
validating_role = Role.get_or_none('charge_sis')


def create_epid_report(provider, expected_reporting, completed_on,
                       integrity_checker, data_source):

    # TODO: changer la periode en hebdomadaire.
    return create_monthly_routine_report(
        provider=provider,
        expected_reporting=expected_reporting,
        data_source=data_source,
        integrity_checker=integrity_checker,
        reportcls=EpidemiologyR,
        project_brand=PROJECT_BRAND)


class EpidemiologyRIntegrityChecker(RoutineIntegrityInterface,
                                    ReportIntegrityChecker):
    report_class = reportcls_epidemio
    validating_role = validating_role

    def check_epid_data(self):
        dict_fields = {'ebola': _('Ebola'),
                       'acute_flaccid_paralysis': _("AFP"),
                       'influenza_a_h1n1': _("Influenza A H1N1"),
                       'cholera': _("Cholera"),
                       'red_diarrhea': _("Red Diarrhea"),
                       'measles': _("Measles"),
                       'yellow_fever': _("Yellow Fever"),
                       'neonatal_tetanus': _("NNT"),
                       'meningitis': _("Meningitis"),
                       'rabies': _("Rabies"),
                       'acute_measles_diarrhea': _("Acute Measles Diarrhea"),
                       'other_notifiable_disease': _("Other Notifiable Diseases")}

        reporting_date = date(self.get('year'), self.get('month'), self.get('day'))
        if reporting_date.weekday() != 6:
            self.add_error("{} n'est pas un dimanche".format(reporting_date.strftime("%X")),
                            field="year")

        for field in dict_fields.keys():
            nb_case = self.get("{}_case".format(field))
            nb_death = self.get("{}_death".format(field))
            if nb_case < nb_death:
                self.add_error(_("{field}: ({case}) number case lower than ({death}) number death")
                               .format(field=dict_fields.get(field), case=nb_case, death=nb_death),
                               field="{}_case".format(field))



    def _check_completeness(self, **options):
        local_fields = ['year', 'month', 'day', 'hc', 'submit_time', 'submitter']

        for field in local_fields + EpidemiologyR.data_fields():
            if not self.has(field):
                self.add_missing(_("Missing data for {f}").format(f=field),
                                 blocking=True, field=field)

    def _check(self, **options):
        self.check_epid_data()
        self.chk_period_is_not_future()
        self.chk_entity_exists()
        self.chk_expected_arrival()
        self.chk_provider_permission()
