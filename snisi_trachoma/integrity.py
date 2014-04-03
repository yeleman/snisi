#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging
import traceback
import datetime

import reversion
from django.utils.translation import ugettext as _

from snisi_core.models.common import get_temp_receipt
from snisi_core.models.Providers import Provider
from snisi_core.models.Entities import Entity
from snisi_core.models.Roles import Role
from snisi_core.models.Periods import MonthPeriod, FixedDaysPeriod
from snisi_core.models.Notifications import Notification
from snisi_trachoma.models import (TTBacklogVillageR,
                                   TTBacklogMissionR)
from snisi_core.models.Reporting import ReportClass, ExpectedReporting, ExpectedValidation
from snisi_core.integrity import ReportIntegrityChecker
from snisi_tools.datetime import parse_date_string
from snisi_trachoma import PROJECT_BRAND

logger = logging.getLogger(__name__)
reportcls_visit = ReportClass.objects.get(slug='ttbacklog_visit')
reportcls_mission = ReportClass.objects.get(slug='ttbacklog_mission')
validating_role = Role.objects.get(slug='charge_sis')


class TTBacklogMissionStartChecker(ReportIntegrityChecker):

    def _check_completeness(self, **options):
        fields = ['district', 'submitter', 'submit_time', 'started_on',
                  'operator_type', 'strategy']

        for field in fields:
            if not self.has(field):
                try:
                    fname = TTBacklogVillageR.field_name(field)
                except:
                    fname = field
                self.add_missing(_("Données manquantes pour {}").format(fname),
                                 blocking=True, field=field)

    def _check(self, **options):
        # period
        period = MonthPeriod.find_create_by_date(self.get('submit_time'))
        self.set('clean_period', period)

        # entity (district)
        entity = Entity.get_or_none(self.get('district'),
                                    type_slug='health_district')
        if entity is None:
            self.add_error("Aucun District ne correspond "
                           "au code {}".format(self.get('district')),
                           field='district', blocking=True)
        self.set('clean_entity', entity)

        # check auth for user at district
        user_district = self.get('submitter').location.get_health_district()
        if (user_district is None
            or not user_district == entity
            or not self.get('submitter').role.slug in ('tt_tso', 'tt_opt',
                                                       'tt_amo', 'charge_sis')):
            self.add_error("Vous n'êtes pas autorisé à créer un rapport de "
                           "mission pour ce district: {}".format(entity),
                           blocking=True, field='submitter')

        # expected reporting defines if report is expeted or not
        expected_reporting = ExpectedReporting.get_or_none(
            report_class__slug='ttbacklog_mission',
            period=period,
            within_period=True,
            entity=entity,
            within_entity=False)

        self.set('expected_reporting', expected_reporting)

        # should have already been checked in checker.
        if expected_reporting is None:
            self.add_error("Aucune mission TT Backlog attendue à {} pour "
                           "la période de {}".format(entity, period),
                           blocking=True)

        if expected_reporting.completion_status == ExpectedReporting.COMPLETION_COMPLETE:
            self.add_error("Aucune mission TT Backlog attendue à {} pour "
                           "la période de {}".format(entity, period),
                           blocking=True)

        # no creation if exist open
        open_missions = TTBacklogMissionR.objects.filter(
            entity=entity,
            created_by=self.get('submitter'),
            ).exclude(completion_status=TTBacklogMissionR.COMPLETE)

        if open_missions.count():
            self.add_error("Vous avez déjà une mission en cours à {}. "
                           "Cloturez la d'abord.".format(entity, period),
                           blocking=True)

        # started_on must be <= today
        today = datetime.date.today()
        started_on = parse_date_string(self.get('started_on'))
        if started_on is None:
            self.add_error("La date de démarrage est incorrecte: "
                           "{}.".format(self.get('started_on')),
                           blocking=True, field='started_on')
        if started_on.date() > today:
            self.add_error("La date de démarrage est dans "
                           "le futur: {}.".format(started_on),
                           blocking=True, field='started_on')
        self.set('clean_started_on', started_on)

        # operator type
        operator_type = {
            'amo': TTBacklogMissionR.AMO,
            'tso': TTBacklogMissionR.TSO,
            'opt': TTBacklogMissionR.OPT
        }.get(self.get('operator_type').lower())
        if operator_type not in TTBacklogMissionR.OPERATOR_TYPES.keys():
            self.add_error("Profil agent innatendu: "
                           "{}.".format(self.get('operator_type')),
                           blocking=True, field='operator')
        self.set('clean_operator_type', operator_type)

        # strategy
        strategy = {
            'fixed': TTBacklogMissionR.FIXED,
            'mobile':TTBacklogMissionR.MOBILE,
            'advanced': TTBacklogMissionR.ADVANCED
        }.get(self.get('strategy').lower())
        if strategy not in TTBacklogMissionR.STRATEGIES.keys():
            self.add_error("Strategie innatendue: "
                           "{}.".format(self.get('strategy')),
                           blocking=True, field='strategy')
        self.set('clean_strategy', strategy)


def create_mission_report(provider, expected_reporting, completed_on,
                          integrity_checker, data_source):

    report = TTBacklogMissionR.start(
        period=expected_reporting.period,
        entity=expected_reporting.entity,
        created_by=provider,
        completion_status=TTBacklogMissionR.INCOMPLETE,
        arrival_status=TTBacklogMissionR.ON_TIME,
        validation_status=TTBacklogMissionR.NOT_VALIDATED)
    report.receipt = get_temp_receipt(report)[:10]

    # fill the report from SMS data
    report.started_on = integrity_checker.get('clean_started_on')
    report.operator = provider
    report.operator_type = integrity_checker.get('clean_operator_type')
    report.strategy = integrity_checker.get('clean_strategy')

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

    # No ExpectedReporting for VisitR. We rely on MissionR.

    # Warn Disctrict people that mission started
    for recipient in Provider.get_at(integrity_checker.get('clean_entity'),
                                     role_slug='charge_sis'):

        if recipient == provider:
            continue

        Notification.create(
            provider=recipient,
            deliver=Notification.TODAY,
            expirate_on=report.started_on + datetime.timedelta(days=3),
            category=PROJECT_BRAND,
            text="Une mission TT de {district} a été créée par {author}. "
                 "No reçu: #{receipt}.".format(
                    district=report.entity.display_full_name(),
                    author=report.operator,
                    receipt=report.receipt)
            )

    return report, ("Le rapport de mission TT au départ de {district} "
                    "a été enregistré. "
                    "Le No de reçu est #{receipt}.".format(
                     district=report.entity.display_full_name(),
                     receipt=report.receipt))


class TTBacklogVisitChecker(ReportIntegrityChecker):

    def _check_completeness(self, **options):
        fields = ['consultation_male', 'consultation_female',
                  'surgery_male', 'surgery_female',
                  'refusal_male', 'refusal_female',
                  'recidivism_male', 'recidivism_female']

        local_fields = ['location', 'submitter', 'submit_time']

        for field in fields + local_fields:
            if not self.has(field):
                try:
                    fname = TTBacklogVillageR.field_name(field)
                except:
                    fname = field
                self.add_missing(_("Données manquantes pour {}").format(fname),
                                 blocking=True, field=field)

    def check_data(self, **options):

        genders = ('male', 'female')

        # convert data to int
        number_fields = ['consultation_male', 'consultation_female',
                         'surgery_male', 'surgery_female',
                         'refusal_male', 'refusal_female',
                         'recidivism_male', 'recidivism_female']
        for field in number_fields:
            try:
                self.set(field, int(self.get(field)))
            except:
                self.add_error(
                    "La valeur de {} n'est pas un entier.".format(field),
                    blocking=True, field=field)

        error_tmpl = ("Le nombre de {f1} ({f1n}) ne peut pas être supérieur "
                      "au nombre de {f2} ({f2n})")

        # consultés >= opérés + refus
        for gender in genders:
            sf = 'surgery_{}'.format(gender)
            rf = 'refusal_{}'.format(gender)
            cf = 'consultation_{}'.format(gender)
            cname = TTBacklogVillageR.field_name(cf)
            surgery_refusal = self.get(sf) + self.get(rf)
            if surgery_refusal > self.get(cf):
                srname = "{} + {}".format(
                    TTBacklogVillageR.field_name(sf),
                    TTBacklogVillageR.field_name(rf))
                self.add_error(error_tmpl.format(f1=srname,
                                                 f1n=surgery_refusal,
                                                 f2=cname,
                                                 f2n=self.get(cf)),
                               field=sf, blocking=True)

        # operés <= consultés
        for gender in genders:
            sf = 'surgery_{}'.format(gender)
            cf = 'consultation_{}'.format(gender)
            cname = TTBacklogVillageR.field_name(cf)
            if self.get(sf) > self.get(cf):
                rname = TTBacklogVillageR.field_name(sf)
                self.add_error(error_tmpl.format(f1=rname,
                                                 f1n=self.get(sf),
                                                 f2=cname,
                                                 f2n=self.get(cf)),
                               field=sf, blocking=True)

        # refus <= consultés
        for gender in genders:
            rf = 'refusal_{}'.format(gender)
            cf = 'consultation_{}'.format(gender)
            cname = TTBacklogVillageR.field_name(cf)
            if self.get(rf) > self.get(cf):
                rname = TTBacklogVillageR.field_name(rf)
                self.add_error(error_tmpl.format(f1=rname,
                                                 f1n=self.get(rf),
                                                 f2=cname,
                                                 f2n=self.get(cf)),
                               field=rf, blocking=True)

        # recidives <= opérés
        for gender in genders:
            rf = 'recidivism_{}'.format(gender)
            sf = 'surgery_{}'.format(gender)
            cname = TTBacklogVillageR.field_name(sf)
            if self.get(rf) > self.get(sf):
                rname = TTBacklogVillageR.field_name(rf)
                self.add_error(error_tmpl.format(f1=rname,
                                                 f1n=self.get(rf),
                                                 f2=cname,
                                                 f2n=self.get(sf)),
                               field=rf, blocking=True)

        # community_assistance
        if self.get('community_assistance'):
            self.set('community_assistance', True)

        # arrived_on is a date
        self.set('arrived_on', parse_date_string(self.get('arrived_on')))
        if not isinstance(self.get('arrived_on'), datetime.date):
            self.add_error("La date d'arrivée au village est "
                           "incompréhensible: {}".format(self.get('arrived_on')),
                           blocking=True, field='arrived_on')

        # left_on is a date
        self.set('left_on', parse_date_string(self.get('left_on')))
        if not isinstance(self.get('left_on'), datetime.date):
            self.add_error("La date de départ du village est "
                           "incompréhensible: {}".format(self.get('left_on')),
                           blocking=True, field='left_on')

        today = datetime.date.today()

        # arrived_on <= today
        if not self.get('arrived_on').date() <= today:
            self.add_error("La date d'arrivée au village est "
                           "dans le futur: {}".format(self.get('arrived_on')),
                           blocking=True, field='arrived_on')

        # left_on <= today
        if not self.get('left_on').date() <= today:
            self.add_error("La date de départ du village est "
                           "dans le futur: {}".format(self.get('left_on')),
                           blocking=True, field='left_on')

        # arrived_on <= left_on
        if not self.get('arrived_on') <= self.get('left_on'):
            self.add_error("La date de départ du village est "
                           "postérieure à la date d'arrivée {}"
                           .format(self.get('left_on')),
                           blocking=True, field='left_on')

    def _check(self, **options):

        self.check_data(**options)

        # Entity for Village
        village = Entity.get_or_none(self.get('location'), type_slug='vfq')
        if village is None:
            self.add_error("Aucun village ne correspond "
                           "au code {}".format(self.get('location')),
                           field='location', blocking=True)
        self.set('clean_village', village)

        # Entity for district
        district = village.get_health_district()
        if district is None:
            self.add_error("Impossible de retrouver le district correspondant "
                           "au village {}".format(village),
                           field='district', blocking=True)
        self.set('clean_district', district)

        # check auth for user at district
        user_district = self.get('submitter').location.get_health_district()
        if (user_district is None
            or not user_district == district
            or not self.get('submitter').role.slug in ('tt_tso', 'tt_opt',
                                                       'tt_amo', 'charge_sis')):
            self.add_error("Vous n'êtes pas autorisé à créer un rapport de "
                           "visite pour ce village: {}".format(village),
                           blocking=True, field='submitter')

        # No ExpectedReporting for VisitR ; open missionR instead
        open_missions = TTBacklogMissionR.objects.filter(
            entity=district,
            created_by=self.get('submitter'),
            ).exclude(completion_status=TTBacklogMissionR.COMPLETE)

        if not open_missions.count():
            self.add_error("Aucune mission TT en cours pour vous. "
                           "Commencez par envoyer le formulaire de "
                           "début de mission.", blocking=True)

        if open_missions.count() > 1:
            self.add_error("Vous avez plusieurs missions ouvertes. "
                           "Merci de contacter ANTIM.", blocking=True)

        # only one visit per village
        if open_missions[0].village_reports.filter(location__slug=village.slug):
            self.add_error("Cette mission possède déjà un rapport de "
                           "visite TT pour le village {}.".format(village),
                           blocking=True, field='location')
        missionR = open_missions[0]

        # set mission for use in create_report
        self.set('missionR', missionR)

        # arrived_on => mission.started_on
        if not self.get('arrived_on').date() >= missionR.started_on:
            self.add_error("La date d'arrivée au village est antérieure au "
                           "début de la mission: {}".format(self.get('arrived_on')),
                           blocking=True, field='arrived_on')


def create_visit_report(provider, expected_reporting, completed_on,
                        integrity_checker, data_source):

    report = TTBacklogVillageR.start(
        period=integrity_checker.get('missionR').period,
        entity=integrity_checker.get('clean_village'),
        created_by=provider,
        completion_status=TTBacklogVillageR.COMPLETE,
        completed_on=completed_on,
        integrity_status=TTBacklogVillageR.CORRECT,
        arrival_status=TTBacklogVillageR.ON_TIME,
        validation_status=TTBacklogVillageR.NOT_VALIDATED)

    # fill the report from SMS data
    report.location = integrity_checker.get('clean_village')
    for field_part in ('consultation', 'surgery', 'refusal', 'recidivism'):
        for gender in ('male', 'female'):
            field = '{}_{}'.format(field_part, gender)
            setattr(report, field, integrity_checker.get(field))

    for field in ('community_assistance', 'arrived_on', 'left_on'):
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
    # no expected reporting to acknowledge.

    # Add this report to MissionR
    integrity_checker.get('missionR').add_village(report)

    # No individual validation on VisitR.
    # Validation is handled Mission-wise once it is over.

    # Add alert to validation Entity?
    for recipient in Provider.get_at(integrity_checker.get('clean_district'),
                                     role_slug='charge_sis'):

        if recipient == provider:
            continue

        Notification.create(
            provider=recipient,
            deliver=Notification.TODAY,
            expirate_on=report.left_on + datetime.timedelta(days=3),
            category=PROJECT_BRAND,
            text="La mission TT de {mission_author} a fini la visite de "
                 " {village}. No reçu: #{receipt}.".format(
                    village=report.location.display_full_name(),
                    mission_author=integrity_checker.get('missionR').operator,
                    receipt=report.receipt)
            )

    return report, ("Le rapport de visite TT pour {village} "
                    "a été enregistré. "
                    "Le No de reçu est #{receipt}.".format(
                     village=report.entity.display_full_name(),
                     receipt=report.receipt))


class TTBacklogMissionEndChecker(ReportIntegrityChecker):

    def _check_completeness(self, **options):
        for field in ['district', 'ended_on', 'submit_time', 'submitter']:
            if not self.has(field):
                self.add_missing(_("Données manquantes pour {}").format(field),
                                 blocking=True, field=field)

    def _check(self, **options):

        # district
        entity = Entity.get_or_none(self.get('district'),
                                    type_slug='health_district')
        if entity is None:
            self.add_error("Aucun District ne correspond "
                           "au code {}".format(self.get('district')),
                           field='district', blocking=True)
        self.set('clean_entity', entity)

        # started_on must be <= today
        today = datetime.date.today()
        try:
            self.set('clean_ended_on', parse_date_string(self.get('ended_on')))
        except:
            self.add_error("La date de fin de mission est incorrecte: "
                           "{}.".format(self.get('clean_ended_on')),
                           blocking=True)
        if self.get('clean_ended_on').date() > today:
            self.add_error("La date de fin de mission est dans "
                           "le futur: {}".format(self.get('clean_ended_on')),
                           blocking=True, field='ended_on')

        open_missions = TTBacklogMissionR.objects.filter(
            entity=entity,
            created_by=self.get('submitter'),
            ).exclude(completion_status=TTBacklogMissionR.COMPLETE)

        if not open_missions.count():
            self.add_error("Aucune mission TT en cours pour vous. "
                           "Commencez par envoyer le formulaire de "
                           "début de mission.", blocking=True)

        if open_missions.count() > 1:
            self.add_error("Vous avez plusieurs missions ouvertes. "
                           "Merci de contacter ANTIM.", blocking=True)

        missionR = open_missions.all()[0]
        self.set('missionR', missionR)

        if self.get('clean_ended_on').date() < missionR.started_on:
            self.add_error("La date de fin de mission est antérieure à la date "
                           "de début: {}".format(self.get('clean_ended_on')),
                           blocking=True, field='ended_on')

        expected_reporting = ExpectedReporting.get_or_none(
            report_class=reportcls_mission,
            period=missionR.period,
            entity=missionR.entity)
        self.set('expected_reporting', expected_reporting)


def close_mission_report(provider, expected_reporting, completed_on,
                         integrity_checker, data_source):

    report = integrity_checker.get('missionR')
    report.ended_on = integrity_checker.get('clean_ended_on')
    report.integrity_status = TTBacklogMissionR.CORRECT
    report.completion_status = TTBacklogMissionR.COMPLETE
    report.completed_on = completed_on

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
    today = datetime.date.today()
    validation_period = FixedDaysPeriod.find_create_with(
        start_on=today,
        end_on=today + datetime.timedelta(days=10))

    # VE is the district (CSCOM's parent)
    validating_entity = report.entity

    # created expected validation for district charge_sis
    ExpectedValidation.objects.create(
        report=report,
        validation_period=validation_period,
        validating_entity=validating_entity,
        validating_role=validating_role)

    # Add alert to validation Entity?
    for recipient in Provider.get_at(integrity_checker.get('clean_entity'),
                                     role_slug='charge_sis'):

        if recipient == provider:
            continue

        Notification.create(
            provider=recipient,
            deliver=Notification.TODAY,
            expirate_on=report.ended_on + datetime.timedelta(days=3),
            category=PROJECT_BRAND,
            text="La mission TT de {mission_author} est terminée. "
                 "No reçu: #{receipt}.".format(
                    mission_author=report.operator,
                    receipt=report.receipt)
            )

    return report, ("Le rapport de mission TT "
                    "a été enregistré. "
                    "Le No de reçu est #{receipt}.".format(
                     receipt=report.receipt))
