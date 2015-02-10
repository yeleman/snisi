#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging
import datetime
import reversion
import traceback

from django.utils.translation import ugettext as _

from snisi_core.integrity import (ReportIntegrityChecker,
                                  create_period_routine_report,
                                  RoutineIntegrityInterface)
from snisi_core.models.Notifications import Notification
from snisi_core.models.Groups import Group
from snisi_core.models.Entities import Entity
from snisi_core.models.Reporting import ExpectedReporting, SNISIReport
from snisi_core.models.Roles import Role
from snisi_core.models.Reporting import ReportClass
from snisi_epidemiology import PROJECT_BRAND, get_domain
from snisi_epidemiology.models import (EpidemiologyR, EpiWeekPeriod,
                                       EpiWeekDistrictValidationPeriod,
                                       EpidemiologyAlertR)

logger = logging.getLogger(__name__)
reportcls_epidemio_alert = ReportClass.get_or_none('epidemio_alert')
reportcls_epidemio = ReportClass.get_or_none('epidemio_weekly_routine')
reportcls_epidemio_agg = ReportClass.get_or_none(
    'epidemio_weekly_routine_aggregated')
validating_role = Role.get_or_none('charge_sis')


def create_epid_report(provider, expected_reporting, completed_on,
                       integrity_checker, data_source,
                       reportcls=EpidemiologyR):

    validation_period = EpiWeekDistrictValidationPeriod.find_create_by_date(
        expected_reporting.period.middle())

    return create_period_routine_report(
        provider=provider,
        expected_reporting=expected_reporting,
        completed_on=completed_on,
        data_source=data_source,
        integrity_checker=integrity_checker,
        reportcls=reportcls,
        project_brand=PROJECT_BRAND,
        validation_period=validation_period,
        validating_entity=expected_reporting.entity.get_health_district(),
        validating_role=validating_role)


class EpidemiologyRIntegrityChecker(RoutineIntegrityInterface,
                                    ReportIntegrityChecker):
    DOMAIN = get_domain()
    report_class = reportcls_epidemio
    validating_role = validating_role
    period_class = EpiWeekPeriod

    def check_epid_data(self):
        list_fields = ['ebola',
                       'acute_flaccid_paralysis',
                       'influenza_a_h1n1',
                       'cholera',
                       'red_diarrhea',
                       'measles',
                       'yellow_fever',
                       'neonatal_tetanus',
                       'meningitis',
                       'rabies',
                       'acute_measles_diarrhea',
                       'other_notifiable_disease']

        if self.period_class == EpiWeekPeriod and \
                self.get('reporting_date').weekday() != 4:
            self.add_error("Fin de semaine doit être un vendredi et non un {}."
                           .format(self.get('reporting_date').strftime("%A")),
                           field="year")

        for field in list_fields:
            nb_case = self.get("{}_case".format(field))
            nb_death = self.get("{}_death".format(field))
            if nb_case < nb_death:
                self.add_error(
                    _("{field_name}: ({case}) number case "
                      "lower than ({death}) number death")
                    .format(field_name=field, case=nb_case, death=nb_death),
                    field="{}".format(field))

    def _check_completeness(self, **options):
        local_fields = ['year', 'month', 'day', 'hc',
                        'submit_time', 'submitter']

        for field in local_fields + EpidemiologyR.data_fields():
            if not self.has(field):
                self.add_missing(_("Missing data for {f}").format(f=field),
                                 blocking=True, field=field)

    def _check(self, **options):
        try:
            reporting_date = datetime.datetime(self.get('year'),
                                               self.get('month'),
                                               self.get('day'),
                                               14, 0, 0)
        except:
            self.add_error("Date incorrecte.", blocking=True)
        else:
            self.set('reporting_date', reporting_date)

        period = self.period_class.find_create_by_date(
            reporting_date - datetime.timedelta(days=3))
        self.set('period', period)

        self.check_epid_data()
        self.chk_period_is_not_future()
        self.chk_entity_exists()
        self.chk_expected_arrival()
        self.chk_provider_permission()


class EpidemiologyRDistrictIntegrityChecker(RoutineIntegrityInterface,
                                            ReportIntegrityChecker):
    DOMAIN = get_domain()
    report_class = reportcls_epidemio_agg
    validating_role = validating_role
    period_class = EpiWeekPeriod
    entities = []
    expected_reportings = []
    entity_type = 'health_district'

    def check_epid_data(self):

        if self.period_class == EpiWeekPeriod and \
                self.get('reporting_date').weekday() != 4:
            self.add_error("Fin de semaine doit être un vendredi et non un {}."
                           .format(self.get('reporting_date').strftime("%A")),
                           field="year")

        for row in range(1, 41):
            hc_field = 'snisi_code_{}'.format(row)
            has_hc = self.has(hc_field)
            # if HC field is blank, the whole line should be ignored
            if not has_hc:
                continue

            # retrieve actual HC and check existence
            entity_field = 'entity_{}'.format(row)
            if not self.has(entity_field) or not self.get(entity_field):
                entity = Entity.get_or_none(self.get(hc_field, '').upper(),
                                            type_slug='health_center')
                self.set(entity_field, entity)

            if self.get(entity_field) is None \
                    or not isinstance(self.get(entity_field), Entity):
                self.add_error("Aucun CSCOM ne correspond au code {}"
                               .format(self.get(hc_field)),
                               field=hc_field, blocking=True)

            # add this entity to list of found in document.
            # used later to check expecteds
            self.entities.append(self.get(entity_field))

            for field in EpidemiologyR.DISEASE_NAMES.keys():
                nb_case = self.get("{}_case_{}".format(field, row))
                nb_death = self.get("{}_death_{}".format(field, row))
                if nb_case < nb_death:
                    self.add_error(
                        _("{field_name} ({hc}): ({case}) number case "
                          "lower than ({death}) number death")
                        .format(field_name=field, hc=self.get(entity_field),
                                case=nb_case, death=nb_death),
                        field="{}".format(field))

    def chk_expected_arrivals(self, **options):
        period = self.get('period')

        for entity in self.entities:
            # expected reporting defines if report is expeted or not
            expected_reporting = ExpectedReporting.get_or_none(
                report_class=reportcls_epidemio,
                period=period,
                within_period=False,
                entity=entity,
                within_entity=False,
                amount_expected=ExpectedReporting.EXPECTED_SINGLE)

            self.expected_reportings.append(expected_reporting)

            if expected_reporting is None:
                self.add_error("Aucun rapport de routine SMIR attendu à "
                               "{entity} pour {period}"
                               .format(entity=entity, period=period),
                               blocking=True)

            # Following checks only applies to incoming new reports.
            # reports being edited already exists and should have
            # arrived in time.
            if options.get('is_edition'):
                return

            if expected_reporting.satisfied:
                self.add_error("Le rapport de routine attendu à "
                               "{entity} pour {period} est déjà arrivé"
                               .format(entity=entity, period=period),
                               blocking=True)

            # check if the report arrived in time or not.
            if expected_reporting.reporting_period.contains(
                    self.get('submit_time')):
                arrival_status = SNISIReport.ON_TIME
            elif expected_reporting.extended_reporting_period and \
                expected_reporting.extended_reporting_period.contains(
                    self.get('submit_time')):
                arrival_status = SNISIReport.LATE
            else:
                # arrived while not in a reporting period
                if self.get('submit_time') \
                        < expected_reporting.reporting_period.start_on:
                    text = ("La période de collecte pour {period} "
                            "n'a pas encore commencée. Rapport refusé.")
                else:
                    # arrived too late. We can't accept the report.
                    text = ("La période de collecte pour {period} "
                            "est terminée. Rapport refusé.")
                self.add_error(text
                               .format(period=expected_reporting.period),
                               blocking=True, field='period')
            self.set('arrival_status', arrival_status)

    def _check_completeness(self, **options):
        local_fields = ['year', 'month', 'day', 'hc',
                        'submit_time', 'submitter']

        for field in local_fields:
            if not self.has(field):
                self.add_missing(_("Missing data for {f}").format(f=field),
                                 blocking=True, field=field)

        for row in range(1, 41):
            hc_field = 'snisi_code_{}'.format(row)
            has_hc = self.has(hc_field)
            has_any_value = sum([int(self.has('{}_{}'.format(field, row)))
                                 for field in EpidemiologyR.data_fields()])
            if has_any_value and not has_hc:
                self.add_missing(
                    _("Missing data for {f}/{row}")
                    .format(f=hc_field, row=row),
                    blocking=True, field=hc_field)

    def _check(self, **options):
        try:
            reporting_date = datetime.datetime(self.get('year'),
                                               self.get('month'),
                                               self.get('day'),
                                               14, 0, 0)
        except:
            self.add_error("Date incorrecte.", blocking=True)
        else:
            self.set('reporting_date', reporting_date)

        period = self.period_class.find_create_by_date(
            reporting_date - datetime.timedelta(days=3))
        self.set('period', period)

        self.check_epid_data()
        self.chk_period_is_not_future()
        self.chk_entity_exists()
        self.chk_expected_arrival()
        self.chk_expected_arrivals()
        self.chk_provider_permission(allow_district=True)


def create_epialert_report(provider, expected_reporting, completed_on,
                           integrity_checker, data_source,
                           reportcls=EpidemiologyAlertR):

    report = reportcls.start(
        period=expected_reporting.period,
        entity=expected_reporting.entity,
        created_by=provider,
        completion_status=SNISIReport.COMPLETE,
        completed_on=completed_on,
        integrity_status=SNISIReport.CORRECT,
        arrival_status=integrity_checker.get('arrival_status'),
        validation_status=SNISIReport.VALIDATED)

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

    # no expected validation

    # send a notification to the SMIR Alert Response Group
    try:
        recipients = Group.get_or_none("smir_alert_response") \
            .members.all()
    except:
        recipients = []
    msg = ("{provider} ({contact}) vient d'envoyer une alerte pour {nb_cases} "
           "cas de {disease} ({nb_suspected} suspects, {nb_confirmed} "
           "confirmés, {nb_death} décès).").format(
        provider=provider.name(),
        contact=provider.primary_number(),
        nb_cases=report.cases_total,
        disease=report.disease_name,
        nb_suspected=report.suspected_cases,
        nb_confirmed=report.confirmed_cases,
        nb_death=report.deaths)
    expirate_on = integrity_checker.get('submit_time') + \
        datetime.timedelta(days=1)
    for recipient in recipients:

        if recipient == provider:
            continue

        Notification.create(
            provider=recipient,
            deliver=Notification.IMMEDIATELY,
            expirate_on=expirate_on,
            category=PROJECT_BRAND,
            text=msg)

    return report, ("L'alerte {disease} a bien été prise en compte "
                    "et notifiée. Le No de reçu est #{receipt}."
                    .format(disease=report.disease_name,
                            receipt=report.receipt))


class EpidemiologyAlertRIntegrityChecker(ReportIntegrityChecker):

    DOMAIN = get_domain()
    report_class = reportcls_epidemio_alert
    validating_role = validating_role

    def _check_completeness(self, **options):
        for field in EpidemiologyAlertR.data_fields():
            if not self.has(field):
                self.add_missing(_("Missing data for {f}").format(f=field),
                                 blocking=True, field=field)

    def chk_expected_arrival(self, **options):

        period = self.get('period')
        entity = self.get('entity')

        # expected reporting defines if report is expeted or not
        expected_reporting = ExpectedReporting.get_or_none(
            report_class=self.report_class,
            period=period,
            within_period=True,
            entity=entity,
            within_entity=False,
            amount_expected=ExpectedReporting.EXPECTED_ZEROPLUS)

        self.set('expected_reporting', expected_reporting)

        if expected_reporting is None:
            self.add_error("Aucun rapport d'alerte attendu à "
                           "{entity} pour {period}"
                           .format(entity=entity, period=period),
                           blocking=True)

        # Following checks only applies to incoming new reports.
        # reports being edited already exists and should
        # have arrived in time.
        if options.get('is_edition'):
            return

        if expected_reporting.satisfied:
            self.add_error("Plus de rapport d'alerte supplémentaire "
                           "attendu pour {period} à {entity}."
                           .format(entity=entity, period=period),
                           blocking=True)

        self.set('arrival_status', SNISIReport.ON_TIME)

    def _check(self, **options):

        options.update({'allow_district': True})

        # check if disease is in list
        if not self.get('disease') in EpidemiologyR.DISEASE_NAMES.keys():
            self.add_error(
                "Cette maladie `{disease}` n'est pas prise en charge."
                .format(disease=self.get('disease')),
                blocking=True, field='disease')

        self.chk_period_is_not_future(**options)
        self.chk_entity_exists(**options)
        self.chk_expected_arrival(**options)
        self.chk_provider_permission(**options)
