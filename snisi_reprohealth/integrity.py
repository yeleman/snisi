#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging
import datetime
import traceback
import json

import reversion
from django.utils.translation import ugettext as _
from django.utils.timezone import utc

from snisi_core.integrity import ReportIntegrityChecker
from snisi_core.models.Providers import Provider
from snisi_core.models.Entities import HealthEntity, Entity
from snisi_core.models.Periods import MonthPeriod
from snisi_core.models.Notifications import Notification
from snisi_core.models.Roles import Role
from snisi_reprohealth import PROJECT_BRAND
from snisi_reprohealth.models.PFActivities import PFActivitiesR
from snisi_core.models.Reporting import (ReportClass, ExpectedReporting,
                                         ExpectedValidation, SNISIReport)
from snisi_core.models.ValidationPeriods import DefaultDistrictValidationPeriod

logger = logging.getLogger(__name__)
reportcls_pf = ReportClass.get_or_none(slug='msi_pf_monthly_routine')
validating_role = Role.get_or_none('charge_sis')


class RoutineIntegrityInterface(object):

    def chk_period_is_not_future(self):
        # Get period and Entity
        period = MonthPeriod.find_create_from(year=self.get('year'),
                                              month=self.get('month'))
        if period.is_ahead():
            self.add_error("La période indiquée ({period}) est dans "
                           "le futur".format(period=period),
                           blocking=True, field='month')

        self.set('period', period)

    def chk_entity_exists(self):
        entity = Entity.get_or_none(self.get('hc', '').upper(),
                                    type_slug='health_center')

        if entity is None:
            self.add_error("Aucun CSCOM ne correspond au code {}".format(self.get('hc')),
                           field='hc', blocking=True)

        self.set('entity', entity)

    def chk_expected_arrival(self):

        period = self.get('period')
        entity = self.get('entity')

        # expected reporting defines if report is expeted or not
        expected_reporting = ExpectedReporting.get_or_none(
            report_class=reportcls_pf,
            period=period,
            within_period=False,
            entity=entity,
            within_entity=False,
            amount_expected=ExpectedReporting.EXPECTED_SINGLE)

        self.set('expected_reporting', expected_reporting)

        if expected_reporting is None:
            self.add_error("Aucun rapport de routine attendu à "
                           "{entity} pour {period}".format(
                                entity=entity, period=period),
                           blocking=True)

        if expected_reporting.satisfied:
            self.add_error("Le rapport de routine attendu à "
                           "{entity} pour {period} est déjà arrivé"
                           .format(entity=entity, period=period),
                           blocking=True)

        # check if the report arrived in time or not.
        if expected_reporting.reporting_period.contains(self.get('submit_time')):
            arrival_status = SNISIReport.ON_TIME
        elif expected_reporting.extended_reporting_period.contains(self.get('submit_time')):
            arrival_status = SNISIReport.LATE
        else:
            # arrived while not in a reporting period
            if self.get('submit_time') < expected_reporting.reporting_period.start_on:
                text = ("La période de collecte pour {period} "
                        "n'a pas encore commencée. Rapport refusé.")
            else:
                # arrived too late. We can't accept the report.
                text = ("La période de collecte pour {period} "
                        "est terminée. Rapport refusé.")
            self.add_error(text.format(period=expected_reporting.period),
                                       blocking=True, field='period')
        self.set('arrival_status', arrival_status)

    def chk_provider_permission(self):
        # check permission to submit report.
        provider = self.get('submitter')
        entity = self.get('entity')

        # provider must be DTC or Charge_SIS
        # if DTC, he must be from very same Entity
        # if Charge_SIS, he must be from a district
        # and the district have the Entity as child HC
        if not provider.role.slug in ('dtc', 'charge_sis') \
            or (provider.role.slug == 'dtc' and not provider.location.slug == entity.slug) \
            or (provider.role.slug == 'charge_sis' and
                (not provider.location.type.slug == 'health_district'
                 or not entity in provider.location.get_health_centers())):
                self.add_error("Vous ne pouvez pas envoyer de rapport "
                               "de routine pour {entity}."
                               .format(entity=entity),
                               blocking=True, field='created_by')

def create_monthly_routine_report(
    provider, expected_reporting, completed_on,
    integrity_checker, data_source,
    reportcls, project_brand):

    report = reportcls.start(
        period=expected_reporting.period,
        entity=expected_reporting.entity,
        created_by=provider,
        completion_status=SNISIReport.COMPLETE,
        completed_on=completed_on,
        integrity_status=SNISIReport.CORRECT,
        arrival_status=integrity_checker.get('arrival_status'),
        validation_status=SNISIReport.NOT_VALIDATED)

    # fill the report from SMS data
    for field in report.data_fields():
        if integrity_checker.has(field):
            setattr(report, field, integrity_checker.get(field))
    try:
        with reversion.create_revision():
            report.save()
    except Exception as e:
        logger.error("Unable to save report to DB. Content: {} | Exp: {}"
                     .format(data_source, e))
        logger.debug("".join(traceback.format_exc()))
        return False, ("Une erreur technique s'est "
                       "produite. Réessayez plus tard et "
                       "contactez ANTIM si le problème persiste.")
    else:
        expected_reporting.acknowledge_report(report)

    # VP is District VP of next month
    validation_period = DefaultDistrictValidationPeriod.find_create_by_date(
        report.period.casted().following().middle())

    # VE is the district (CSCOM's parent)
    validating_entity = report.entity.get_health_district()

    # created expected validation for district charge_sis
    ExpectedValidation.objects.create(
        report=report,
        validation_period=validation_period,
        validating_entity=validating_entity,
        validating_role=validating_role)

    # Add alert to validation Entity?
    for recipient in Provider.active.filter(
        role=validating_role, location=validating_entity):

        if recipient == provider:
            continue

        Notification.create(
            provider=recipient,
            deliver=Notification.TODAY,
            expirate_on=validation_period.end_on,
            category=project_brand,
            text="L'Unité Sanitaire {hc} vient d'envoyer son rapport "
                 "{report_name} pour {period}. "
                 "No reçu: #{receipt}.".format(
                    report_name=reportcls._meta.verbose_name,
                    hc=report.entity.display_full_name(),
                    period=report.period,
                    receipt=report.receipt)
            )

    return report, ("Le rapport de {cscom} pour {period} "
                    "a été enregistré. "
                    "Le No de reçu est #{receipt}.".format(
                     cscom=report.entity.display_full_name(),
                     period=report.period,
                     receipt=report.receipt))


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

    def check_pf_data(self):
        #### Provided Services
        # (new_clients + previous_clients) = (under25_visits + over25_visits)
        new_and_old_clients = self.get('new_clients') + self.get('previous_clients')
        under_and_over_25 = self.get('under25_visits') + self.get('over25_visits')
        if new_and_old_clients != under_and_over_25:
            self.add_error(_("Number of new + old clients ({noc}) must equals number "
                             "of Under25 + Over25 ({uo25}).")
                           .format(noc=new_and_old_clients,
                                   uo25=under_and_over_25),
                           field='under25_visits')

        # = (tubal_ligations + short_term_method_visits + long_term_method_visits
        #    + implant_removal + iud_removal)
        all_services = sum([self.get(f) for f in ('tubal_ligations',
                                                  'short_term_method_visits',
                                                  'long_term_method_visits',
                                                  'implant_removal',
                                                  'iud_removal')])
        if new_and_old_clients != all_services:
            self.add_error(_("Number of new + old clients ({noc}) must equals sum "
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
            self.add_error(_("Number of long-term visits ({ltv}) must equals number "
                             "of IDU + Implants ({iudi}).")
                           .format(ltv=self.get('intrauterine_devices'),
                                   iudi=iud_implants),
                           field='long_term_method_visits')

        #### Financial
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

        #### Stocks
        for field in PFActivitiesR.stocks_fields(False):

            consumed = self.get("{}_used".format(field)) + self.get("{}_lost".format(field))
            available = self.get("{}_initial".format(field)) + self.get("{}_received".format(field))

            if consumed > available:
                self.add_error(_("{f}: Used + Lost ({c}) higher than "
                                 "Initial + Received ({a}).")
                               .format(f=PFActivitiesR.label_for_field(field),
                                       c=consumed,
                                       a=available),
                               field="{}_used".format(field))

        #### Cross-form checks
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
            if not field in PFActivitiesR.stocks_fields(False):
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
                self.add_missing(_("Données manquantes pour {f}").format(f=field),
                                 blocking=True, field=field)

    def _check(self, **options):
        self.check_pf_data()
        self.chk_period_is_not_future()
        self.chk_entity_exists()
        self.chk_expected_arrival()
        self.chk_provider_permission()
