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
from snisi_reprohealth import PROJECT_BRAND
from snisi_reprohealth.models.PFActivities import PFActivitiesR
from snisi_core.models.Reporting import ReportClass

logger = logging.getLogger(__name__)
reportcls_pf = ReportClass.get_or_none(slug='msi_pf_monthly_routine')
validating_role = Role.get_or_none('charge_sis')


def create_pf_report(provider, expected_reporting, completed_on,
                     integrity_checker, data_source):

    return create_monthly_routine_report(
        provider=provider,
        expected_reporting=expected_reporting,
        completed_on=completed_on,
        integrity_checker=integrity_checker,
        data_source=data_source,
        reportcls=PFActivitiesR,
        project_brand=PROJECT_BRAND)


class PFActivitiesRIntegrityChecker(RoutineIntegrityInterface,
                                    ReportIntegrityChecker):

    report_class = reportcls_pf
    validating_role = validating_role

    def check_pf_data(self, **options):
        # ### Provided Services
        # (new_clients + previous_clients) = (under25_visits + over25_visits)
        new_and_old_clients = self.get('new_clients') \
            + self.get('previous_clients')
        under_and_over_25 = self.get('under25_visits') \
            + self.get('over25_visits')
        if new_and_old_clients != under_and_over_25:
            self.add_error(_("Number of new + old clients ({noc}) "
                             "must equals number "
                             "of Under25 + Over25 ({uo25}).")
                           .format(noc=new_and_old_clients,
                                   uo25=under_and_over_25),
                           field='under25_visits')

        # = (tubal_ligations + short_term_method_visits
        #   + long_term_method_visits
        #    + implant_removal + iud_removal)
        all_services = sum([self.get(f) for f in ('tubal_ligations',
                                                  'short_term_method_visits',
                                                  'long_term_method_visits',
                                                  'implant_removal',
                                                  'iud_removal')])
        if new_and_old_clients != all_services:
            self.add_error(_("Number of new + old clients ({noc}) "
                             "must equals sum "
                             "of provided services ({alls}).")
                           .format(noc=new_and_old_clients,
                                   alls=all_services),
                           field='tubal_ligations')

        # very_first_visits <= new_clients
        if self.get('very_first_visits') > self.get('new_clients'):
            self.add_error(_("Number of first visits ({fv}) can't be more "
                             "than new clients ({nc}).")
                           .format(fv=self.get('very_first_visits'),
                                   nc=self.get('new_clients')),
                           field='very_first_visits')

        # long_term_method_visits = (intrauterine_devices + implants)
        iud_implants = self.get('intrauterine_devices') + self.get('implants')
        if self.get('long_term_method_visits') != iud_implants:
            self.add_error(_("Number of long-term visits ({ltv}) "
                             "must equals number "
                             "of IDU + Implants ({iudi}).")
                           .format(ltv=self.get('intrauterine_devices'),
                                   iudi=iud_implants),
                           field='long_term_method_visits')

        # ### Financial
        for field in PFActivitiesR.financial_fields(False):
            qty = self.get("{}_qty".format(field))
            price = self.get("{}_price".format(field))
            amount = qty * price
            revenue = self.get("{}_revenue".format(field))
            if amount < revenue:
                self.add_error(_("{f}: Amount ({a}) lower than "
                                 "Revenue ({r}).")
                               .format(f=PFActivitiesR.label_for_field(field),
                                       a=amount,
                                       r=revenue),
                               field="{}_revenue".format(field))

        # ### Stocks
        for field in PFActivitiesR.stocks_fields(False):

            consumed = self.get("{}_used".format(field)) \
                + self.get("{}_lost".format(field))
            available = self.get("{}_initial".format(field)) \
                + self.get("{}_received".format(field))

            if consumed > available:
                self.add_error(_("{f}: Used + Lost ({c}) higher than "
                                 "Initial + Received ({a}).")
                               .format(f=PFActivitiesR.label_for_field(field),
                                       c=consumed,
                                       a=available),
                               field="{}_used".format(field))

        # ### Cross-form checks
        # quantities from financial and stocks equals provided
        for field in PFActivitiesR.financial_fields(False):
            provided_qty = self.get(field)
            financial_qty = self.get("{}_qty".format(field))

            if provided_qty != financial_qty:
                self.add_error(_("{f}: Provided Quantity ({pq}) different "
                                 "from Financial Quantity ({fq}).")
                               .format(f=PFActivitiesR.label_for_field(field),
                                       pq=provided_qty,
                                       fq=financial_qty),
                               field="{}_qty".format(field))

            # stocks don't have all fields
            if field not in PFActivitiesR.stocks_fields(False):
                continue

            stock_qty = self.get("{}_used".format(field))
            if provided_qty != stock_qty:
                self.add_error(_("{f}: Provided Quantity ({pq}) different "
                                 "from Stocks Quantity ({sq}).")
                               .format(f=PFActivitiesR.label_for_field(field),
                                       pq=provided_qty,
                                       sq=stock_qty),
                               field="{}_used".format(field))

    def _check_completeness(self, **options):
        for field in PFActivitiesR.data_fields():
            if not self.has(field) and not field.endswith('_observation'):
                self.add_missing(_("Missing data for {f}").format(f=field),
                                 blocking=True, field=field)

    def _check(self, **options):
        self.check_pf_data(**options)
        self.chk_period_is_not_future(**options)
        self.chk_entity_exists(**options)
        self.chk_expected_arrival(**options)
        self.chk_provider_permission(**options)
