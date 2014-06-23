#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

from py3compat import text_type

from django.utils.translation import ugettext as _


class ReportingDataException(Exception):

    level = 'unknown'
    field = None
    message = None
    short_message = None
    extras = {}

    def __init__(self, message, field=None, short_message=None, extras={}):
        if field:
            self.field = field
        if message:
            self.message = message
        if short_message:
            self.short_message = message
        if len(extras.keys()):
            self.extras.update(extras)

        super(ReportingDataException, self).__init__(message or short_message)

    def add_extras(self, extras):
        self.extras.update(extras)

    def render(self, short=False):
        if short and self.short_message:
            return self.short
        return self.message


class ReportingDataWarning(ReportingDataException):
    level = 'warning'


class ReportingDataError(ReportingDataException):
    level = 'error'


class ReportingDataMissing(ReportingDataException):
    level = 'error'


class ReportingDataHolder(object):

    def __init__(self):
        self.fields = []
        self._data = {}
        self._feedbacks = []
        self._raised = None

    @property
    def data(self):
        return self._data

    def to_dict(self):
        return self.data

    def feed(self, **kwargs):
        self._data.update(kwargs)

    def set(self, key, value):
        self._data.update({key: value})

    def get(self, key, default=None, silent=False):
        if not key in self.data.keys():
            self.add_missing(_("Missing Data for {}").format(key),
                             blocking=not silent,
                             field=key)
        return self.data.get(key, default)

    def has(self, key, test_value=True):
        return key in self.data.keys() and \
            (self.data.get(key) is not None or not test_value)

    def add_warning(self, warning, **kwargs):
        if isinstance(warning, text_type):
            warning = ReportingDataWarning(warning, **kwargs)
        self._feedbacks.append(warning)

    def add_error(self, error, blocking=False, **kwargs):
        if isinstance(error, text_type):
            error = ReportingDataError(error, **kwargs)
        self._feedbacks.append(error)
        if blocking:
            raise error

    def add_missing(self, missing, blocking=False, **kwargs):
        if isinstance(missing, text_type):
            missing = ReportingDataMissing(missing, **kwargs)
        self._feedbacks.append(missing)
        if blocking:
            raise missing

    def _read(self):
        # override if you need to read data from a stream or anything.
        # useful for Excel Forms.
        pass

    def read(self):
        self._read()

    def _check(self, **options):
        # overrride to add checks here
        pass

    def _check_completeness(self, **options):
        # overrride to add completeness checks here
        pass

    def check_completeness(self, **options):
        try:
            self._check_completeness(**options)
        except ReportingDataException as raised:
            self._raised = raised
            if not raised in self._feedbacks:
                self._feedbacks.append(raised)

    def check(self, **options):
        try:
            self._read(**options)
            self._check_completeness(**options)
            self._check(**options)
        except ReportingDataException as raised:
            self._raised = raised
            if not raised in self._feedbacks:
                self._feedbacks.append(raised)

    def is_valid(self):
        return not len([1 for e in self.feedbacks if e.level == 'error'])

    def is_complete(self, *args, **kwargs):
        return not len([1 for e in self.feedbacks
                        if isinstance(e, ReportingDataMissing)])

    @property
    def raised(self):
        return self._raised

    @property
    def errors(self):
        return [self.raised] + [error for error in self._feedbacks
                                if isinstance(error, ReportingDataError)]

    @property
    def warnings(self):
        return [error for error in self._feedbacks
            if isinstance(error, ReportingDataWarning)]

    @property
    def missings(self):
        return [error for error in self._feedbacks
            if isinstance(error, ReportingDataMissing)]

    @property
    def feedbacks(self):
        return ([self.raised] if self.raised else []) \
            + [f for f in self._feedbacks if not f == self.raised]

    def render_feedbacks(self, sep="\n"):
        return sep.join([f.render() for f in self.feedbacks])


class ReportIntegrityChecker(ReportingDataHolder):
    pass


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
