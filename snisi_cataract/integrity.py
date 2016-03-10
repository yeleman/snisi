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
from snisi_cataract import models as cat_models
from snisi_cataract.models import CATSurgeryR, CATMissionR
from snisi_core.models.Reporting import (ReportClass, ExpectedReporting,
                                         ExpectedValidation)
from snisi_core.integrity import ReportIntegrityChecker
from snisi_tools.datetime import parse_date_string
from snisi_cataract import PROJECT_BRAND, get_domain

logger = logging.getLogger(__name__)
reportcls_mission = ReportClass.objects.get(slug='cat_mission')
validating_role = Role.objects.get(slug='charge_sis')


class CATMissionStartChecker(ReportIntegrityChecker):

    DOMAIN = get_domain()

    def _check_completeness(self, **options):
        fields = ['district', 'submitter', 'submit_time', 'started_on',
                  'operator_type', 'strategy']

        for field in fields:
            if not self.has(field):
                try:
                    fname = CATSurgeryR.field_name(field)
                except:
                    fname = field
                self.add_missing(_("Missing data for {}").format(fname),
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
                or self.get('submitter').role.slug
                not in ('tt_tso', 'tt_opt', 'tt_amo',
                        'tt_surgeon', 'charge_sis')):
            self.add_error("Vous n'êtes pas autorisé à créer un rapport de "
                           "mission pour ce district: {}".format(entity),
                           blocking=True, field='submitter')

        # expected reporting defines if report is expeted or not
        expected_reporting = ExpectedReporting.get_or_none(
            report_class__slug='cat_mission',
            period=period,
            within_period=True,
            entity=entity,
            within_entity=False)

        self.set('expected_reporting', expected_reporting)

        # should have already been checked in checker.
        if expected_reporting is None:
            self.add_error("Aucune mission cataracte attendue à {} pour "
                           "la période de {}".format(entity, period),
                           blocking=True)

        if expected_reporting.completion_status \
                == ExpectedReporting.COMPLETION_COMPLETE:
            self.add_error("Aucune mission cataracte attendue à {} pour "
                           "la période de {}".format(entity, period),
                           blocking=True)

        # no creation if exist open
        open_missions = CATMissionR.objects.filter(
            entity=entity,
            created_by=self.get('submitter'),
            ).exclude(completion_status=CATMissionR.COMPLETE)

        if open_missions.count():
            self.add_error("Vous avez déjà une mission en cours à {}. "
                           "Cloturez la d'abord.".format(entity, period),
                           blocking=True)

        # started_on must be <= today
        today = datetime.date.today()
        started_on = parse_date_string(self.get('started_on'), as_date=True)
        if started_on is None:
            self.add_error("La date de démarrage est incorrecte: "
                           "{}.".format(self.get('started_on')),
                           blocking=True, field='started_on')
        if started_on > today:
            self.add_error("La date de démarrage est dans "
                           "le futur: {}.".format(started_on),
                           blocking=True, field='started_on')

        if started_on < today - datetime.timedelta(days=21):
            self.add_error("La date de démarrage est trop "
                           "ancienne: {}.".format(started_on),
                           blocking=True, field='started_on')

        self.set('clean_started_on', started_on)

        # operator type
        operator_type = {
            'amo': cat_models.AMO,
            'tso': cat_models.TSO,
            'opt': cat_models.OPT,
            'surgeon': cat_models.SURGEON,
        }.get(self.get('operator_type').lower())
        if operator_type not in cat_models.OPERATOR_TYPES.keys():
            self.add_error("Profil agent innatendu: "
                           "{}.".format(self.get('operator_type')),
                           blocking=True, field='operator')
        self.set('clean_operator_type', operator_type)

        # strategy
        strategy = {
            'fixed': cat_models.FIXED,
            'mobile': cat_models.MOBILE,
            'advanced': cat_models.ADVANCED
        }.get(self.get('strategy').lower())
        if strategy not in cat_models.STRATEGIES.keys():
            self.add_error("Strategie innatendue: "
                           "{}.".format(self.get('strategy')),
                           blocking=True, field='strategy')
        self.set('clean_strategy', strategy)


def create_mission_report(provider, expected_reporting, completed_on,
                          integrity_checker, data_source):

    report = CATMissionR.start(
        period=expected_reporting.period,
        entity=expected_reporting.entity,
        created_by=provider,
        completion_status=CATMissionR.INCOMPLETE,
        arrival_status=CATMissionR.ON_TIME,
        validation_status=CATMissionR.NOT_VALIDATED)
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

    # acknowledge report
    expected_reporting.acknowledge_report(report)

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
            text="Une mission cataracte de {district} a été créée "
                 "par {author}. No reçu: #{receipt}."
                 .format(district=report.entity.display_full_name(),
                         author=report.operator,
                         receipt=report.receipt)
            )

    return report, ("Le rapport de mission cataracte au départ de {district} "
                    "a été enregistré. "
                    "Le No de reçu est #{receipt}."
                    .format(district=report.entity.display_full_name(),
                            receipt=report.receipt))


class CATSurgeryChecker(ReportIntegrityChecker):

    DOMAIN = get_domain()

    def _check_completeness(self, **options):
        fields = ['surgery_date', 'gender', 'eye', 'age', 'number']

        local_fields = ['location', 'submitter', 'submit_time']

        for field in fields + local_fields:
            if not self.has(field):
                try:
                    fname = CATSurgeryR.field_name(field)
                except:
                    fname = field
                self.add_missing(_("Missing data for {}").format(fname),
                                 blocking=True, field=field)

    def check_data(self, **options):

        # number checking
        field = 'number'
        try:
            self.set(field, int(self.get(field)))
            assert self.get(field) > 0
            assert self.get(field) < 500
        except:
            self.add_error(
                "Le numéro `{}` n'est pas correct."
                .format(self.get(field)),
                blocking=True, field=field)

        # gender matching
        gender_matrix = {
            'm': cat_models.MALE,
            'f': cat_models.FEMALE,
        }
        field = 'gender'
        if self.get(field) not in gender_matrix.keys():
            self.add_error(
                "Le sexe `{}` n'est pas compréhensible."
                .format(self.get(field)),
                blocking=True, field=field)
        self.set(field, gender_matrix.get(self.get(field)))

        # eye matching
        eye_matrix = {
            'right': cat_models.RIGHT,
            'left': cat_models.LEFT
        }
        field = 'eye'
        if self.get(field) not in eye_matrix.keys():
            self.add_error(
                "L'oeil `{}` n'est pas un compréhensible."
                .format(self.get(field)),
                blocking=True, field=field)
        self.set(field, eye_matrix.get(self.get(field)))

        # age setting
        field = 'age'
        try:
            age = int(self.get(field))
            assert age >= 5
            assert age <= 95
            self.set(field, age)
        except:
            self.add_error(
                "L'age `{}` n'est pas compréhensible.".format(self.get(field)),
                blocking=True, field=field)

        # surgery_date is a date
        self.set('surgery_date', parse_date_string(self.get('surgery_date'),
                                                   as_date=True))
        if not isinstance(self.get('surgery_date'), datetime.date):
            self.add_error("La date de chirurgie n'est pas "
                           "compréhensible: {}"
                           .format(self.get('surgery_date')),
                           blocking=True, field='surgery_date')

        today = datetime.date.today()

        # surgery_date <= today
        if not self.get('surgery_date') <= today:
            self.add_error("La date de chirurgie est "
                           "dans le futur: {}"
                           .format(self.get('surgery_date')),
                           blocking=True, field='surgery_date')

    def _check(self, **options):

        period = MonthPeriod.find_create_by_date(self.get('submit_time'))
        self.set('period', period)

        self.check_data(**options)

        if options.get('fixed'):
            district = Entity.get_or_none(self.get('location'),
                                          type_slug='health_district')

            if district is None:
                self.add_error("Impossible de retrouver le district "
                               "correspondant à {}".format(district),
                               field='location', blocking=True)

            # check auth for user at district
            user_district = self.get('submitter') \
                .location.get_health_district()
            if (user_district is None
                    or not user_district == district
                    or self.get('submitter').role.slug
                    not in ('tt_tso', 'tt_opt', 'tt_amo',
                            'tt_surgeon', 'charge_sis')):
                self.add_error("Vous n'êtes pas autorisé à créer un rapport "
                               "de chirurgie pour ce district: {}"
                               .format(district),
                               blocking=True, field='submitter')

            self.set('clean_location', district)

            missionR = CATMissionR.get_or_create_fixed_for(
                entity=district,
                period=self.get('period'),
                provider=self.get('submitter'))
        else:
            # Entity for Village
            health_area = Entity.get_or_none(self.get('location'),
                                             type_slug='health_area')
            if health_area is None:
                self.add_error("Aucune aire ne correspond "
                               "au code {}".format(self.get('location')),
                               field='location', blocking=True)
            self.set('health_area', health_area)

            # Entity for district
            district = health_area.get_health_district()
            if district is None:
                self.add_error("Impossible de retrouver le district "
                               "correspondant à l'aire {}".format(health_area),
                               field='district', blocking=True)
            self.set('district', district)

            # tt_surgeon has permission everywhere
            submitter = self.get('submitter')
            if not (submitter.role.slug == 'tt_surgeon'
                    and submitter.location.is_central):

                # check auth for user at district
                user_district = self.get('submitter') \
                    .location.get_health_district()
                if (user_district is None
                        or not user_district == district
                        or self.get('submitter').role.slug
                        not in ('tt_tso', 'tt_opt', 'tt_amo',
                                'tt_surgeon', 'charge_sis')):
                    self.add_error("Vous n'êtes pas autorisé à créer un rapport "
                                   "de chirurgie pour cette aire: {}"
                                   .format(health_area),
                                   blocking=True, field='submitter')

            self.set('clean_location', health_area)

            # No ExpectedReporting for CATSurgeryR ; open missionR instead
            open_missions = CATMissionR.objects.filter(
                entity=district,
                created_by=self.get('submitter'),
                ).exclude(completion_status=CATMissionR.COMPLETE)

            if not open_missions.count():
                self.add_error("Aucune mission cataracte en cours pour vous. "
                               "Commencez par envoyer le formulaire de "
                               "début de mission.", blocking=True)

            if open_missions.count() > 1:
                self.add_error("Vous avez plusieurs missions ouvertes. "
                               "Merci de contacter ANTIM.", blocking=True)

            missionR = open_missions[0]

        # set mission for use in create_report
        self.set('missionR', missionR)

        # surgery_date => mission.started_on
        if not self.get('surgery_date') >= missionR.started_on:
            self.add_error("La date de chirurgie est antérieure au "
                           "début de la mission: {} vs {}"
                           .format(self.get('surgery_date'),
                                   missionR.started_on),
                           blocking=True, field='surgery_date')

        existing = CATSurgeryR.existing_for(
            mission=missionR,
            surgery_date=self.get('surgery_date'),
            gender=self.get('gender'),
            eye=self.get('eye'),
            age=self.get('age'),
            number=self.get('number'))
        if existing:
            self.add_error("Rapport de chirurgie existant pour {details}. "
                           "Identifiant : {ident}"
                           .format(details=existing.verbose_features,
                                   ident=existing.surgery_ident),
                           blocking=True, field='surgery_date')


def create_surgery_report(provider, expected_reporting, completed_on,
                          integrity_checker, data_source):

    report = CATSurgeryR.start(
        period=integrity_checker.get('missionR').period,
        entity=integrity_checker.get('clean_location'),
        created_by=provider,
        completion_status=CATSurgeryR.COMPLETE,
        completed_on=completed_on,
        integrity_status=CATSurgeryR.CORRECT,
        arrival_status=CATSurgeryR.ON_TIME,
        validation_status=CATSurgeryR.NOT_VALIDATED)
    report.surgery_ident = report.get_unused_ident()

    # fill the report from SMS data
    report.location = integrity_checker.get('clean_location')
    for field in ('surgery_date', 'gender', 'eye', 'age', 'number'):
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
    integrity_checker.get('missionR').add_surgery(report)

    # No individual validation on CATSurgeryR.
    # Validation is handled Mission-wise once it is over.
    return report, ("Chirurgie cataracte ({gender}/{age}a/{eye}) "
                    "enregistrée. Identifiant : {ident}."
                    .format(ident=report.surgery_ident,
                            gender=report.verbose_short_gender,
                            age=report.age,
                            eye=report.verbose_eye))


class CATSurgeryResultChecker(ReportIntegrityChecker):

    DOMAIN = get_domain()

    def _check_completeness(self, **options):
        fields = ['result_date', 'surgery_ident', 'visual_acuity']

        local_fields = ['submitter', 'submit_time']

        for field in fields + local_fields:
            if not self.has(field):
                try:
                    fname = CATSurgeryR.field_name(field)
                except:
                    fname = field
                self.add_missing(_("Missing data for {}").format(fname),
                                 blocking=True, field=field)

    def check_data(self, **options):

        # ID matching
        field = 'surgery_ident'
        surgery_report = CATSurgeryR.get_by_ident(self.get(field))
        if surgery_report is None:
            self.add_error(
                "L'identifiant de chirurgie `{}` est incorrect."
                .format(self.get(field)),
                blocking=True, field=field)
        elif surgery_report.has_result():
            self.add_error(
                "La résultat de la chirurgie pour `{}` a déjà été transmis."
                .format(self.get(field).upper()),
                blocking=True, field=field)
        else:
            # ident is correct
            self.set('surgery_report', surgery_report)

        # visual_acuity validation
        field = 'visual_acuity'
        if self.get(field) == '<1':
            visual_acuity = 0
        else:
            try:
                visual_acuity = int(self.get(field))
                assert visual_acuity >= 0
                assert visual_acuity <= 10
                self.set(field, visual_acuity)
            except:
                self.add_error(
                    "L'acuité visuelle `{}` n'est pas valide."
                    .format(self.get(field)),
                    blocking=True, field=field)

        # result_date is a date
        self.set('result_date', parse_date_string(self.get('result_date'),
                                                  as_date=True))
        if not isinstance(self.get('result_date'), datetime.date):
            self.add_error("La date de chirurgie n'est pas "
                           "compréhensible: {}"
                           .format(self.get('result_date')),
                           blocking=True, field='result_date')

        today = datetime.date.today()

        # result_date <= today
        if not self.get('result_date') <= today:
            self.add_error("La date de chirurgie est dans le futur: {}"
                           .format(self.get('result_date')),
                           blocking=True, field='result_date')

    def _check(self, **options):

        self.check_data(**options)

        # user must has rights on surgery_report district
        district = self.get('surgery_report').location.get_health_district()

        # tt_surgeon has permission everywhere
        submitter = self.get('submitter')
        if not (submitter.role.slug == 'tt_surgeon'
                and submitter.location.is_central):

            # check auth for user at district
            user_district = self.get('submitter') \
                .location.get_health_district()
            if (user_district is None
                    or not user_district == district
                    or self.get('submitter').role.slug
                    not in ('tt_tso', 'tt_opt', 'tt_amo',
                            'tt_surgeon', 'charge_sis')):
                self.add_error("Vous n'êtes pas autorisé à "
                               "envoyer de résultat "
                               "chirurgie pour ce district: {}"
                               .format(user_district),
                               blocking=True, field='submitter')

        # result_date => surgery_date
        if not self.get('result_date') >= \
                self.get('surgery_report').surgery_date:
            self.add_error("La date du résultat est antérieure "
                           "à la date de la chirurgie: {}"
                           .format(self.get('result_date')),
                           blocking=True, field='result_date')


def create_result_report(provider, expected_reporting, completed_on,
                         integrity_checker, data_source):

    report = integrity_checker.get('surgery_report')

    # fill the report from SMS data
    for field in ('result_date', 'visual_acuity'):
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

    # No individual validation on CATSurgeryR.
    # Validation is handled Mission-wise once it is over.

    return report, ("Le résultat de chirurgie cataracte {ident} "
                    "a été enregistré."
                    .format(ident=report.surgery_ident))


class CATMissionEndChecker(ReportIntegrityChecker):

    DOMAIN = get_domain()

    def _check_completeness(self, **options):
        for field in ['district', 'ended_on', 'submit_time', 'submitter']:
            if not self.has(field):
                self.add_missing(_("Missing data for {}").format(field),
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
            self.set('clean_ended_on',
                     parse_date_string(self.get('ended_on'), as_date=True))
        except:
            self.add_error("La date de fin de mission est incorrecte: "
                           "{}.".format(self.get('clean_ended_on')),
                           blocking=True)
        if self.get('clean_ended_on') > today:
            self.add_error("La date de fin de mission est dans "
                           "le futur: {}".format(self.get('clean_ended_on')),
                           blocking=True, field='ended_on')

        open_missions = CATMissionR.objects.filter(
            entity=entity,
            created_by=self.get('submitter'),
            ).exclude(completion_status=CATMissionR.COMPLETE)

        if not open_missions.count():
            self.add_error("Aucune mission cataracte en cours pour vous. "
                           "Commencez par envoyer le formulaire de "
                           "début de mission.", blocking=True)

        if open_missions.count() > 1:
            self.add_error("Vous avez plusieurs missions ouvertes. "
                           "Merci de contacter ANTIM.", blocking=True)

        missionR = open_missions.all()[0]
        self.set('missionR', missionR)

        if self.get('clean_ended_on') < missionR.started_on:
            self.add_error("La date de fin de mission {} est antérieure "
                           "à la date de début: {}"
                           .format(self.get('clean_ended_on'),
                                   missionR.started_on),
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
    report.integrity_status = CATMissionR.CORRECT
    report.completion_status = CATMissionR.COMPLETE
    report.completed_on = completed_on
    report.update_stats()

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
            text="La mission cataracte de {mission_author} est terminée. "
                 "No reçu: #{receipt}."
                 .format(mission_author=report.operator,
                         receipt=report.receipt)
            )

    return report, ("La de mission cataracte "
                    "a bien été cloturée. "
                    "Le No de reçu est #{receipt}."
                    .format(receipt=report.receipt))
