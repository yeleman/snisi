#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging
import datetime

from django.conf import settings
from django.utils import timezone

from snisi_core.models.Providers import Provider
# from snisi_core.models.Roles import Role
from snisi_core.models.Entities import HealthEntity
from snisi_core.models.Periods import MonthPeriod
from snisi_core.models.Reporting import (ExpectedReporting, ReportClass)
from snisi_malaria.models import MalariaR
from snisi_malaria.integrity import (MalariaRSourceReportChecker,
                                     create_report, PROJECT_BRAND)
from snisi_tools.sms import send_sms
from snisi_sms.reply import SMSReply

logger = logging.getLogger(__name__)
reportcls = ReportClass.objects.get(slug='malaria_monthly_routine')


def malaria_handler(message):
    if message.content.lower().startswith('palu '):
        if message.content.lower().startswith('palu passwd'):
            return malaria_passwd(message)
        elif message.content.lower().strip() == 'palu aide':
            return malaria_help(message, True)
        elif message.content.lower().startswith('palu aide'):
            return malaria_help(message)
        else:
            return malaria_report(message)

    return False

KEYWORDS = {
    'palu': malaria_handler,
}


def malaria_help(message, nousername=False):

    try:
        hotline = settings.HOTLINE_NUMBER
    except:
        hotline = '65731076'

    if nousername:
        kw1, kw2 = message.content.strip().lower().split()
        username = None
    else:
        kw1, kw2, uusername = message.content.strip().lower().split()
        try:
            username = uusername.split(':')[1]
        except:
            username = None

    provider = None
    if username:
        try:
            provider = Provider.objects.get(username=username)
        except Provider.DoesNotExist:
            pass

    if not provider:

        provider = Provider.from_phone_number(identity=message.identity)

    if not provider:
        text_message = ("[DEMANDE AIDE] Non identifié: {}"
                        .format(message.identity))
    else:
        text_message = "[DEMANDE AIDE] {provider}".format(
            provider=provider.name())

    send_sms(hotline, text_message)
    return True


def malaria_passwd(message):
    error_start = "Impossible de changer votre mot de passe. "
    try:
        kw1, kw2, username, old_password, new_password = \
            message.content.strip().lower().split()
    except ValueError:
        message.respond(error_start + "Le format du SMS est incorrect.")
        return True

    try:
        provider = Provider.active.get(username=username)
    except Provider.DoesNotExist:
        message.respond(error_start + "Ce nom d'utilisateur ({}) "
                                      "n'existe pas.".format(username))
        return True

    if not provider.check_password(old_password):
        message.respond(error_start + "Votre ancien mot de passe "
                                      "est incorrect.")
        return True

    try:
        provider.set_password(new_password)
        provider.save()
    except:
        message.respond(error_start + "Essayez un autre nouveau "
                                      "mot de passe.")
        return True

    message.respond("Votre mot de passe a été changé et est "
                    "effectif immédiatement. Merci.")

    return True


def malaria_report(message):

    reply = SMSReply(message, PROJECT_BRAND)

    # create variables from text messages.
    try:
        args_names = ['kw1', 'username', 'password', 'month', 'year',
                      'u5_total_consultation_all_causes',
                      'u5_total_suspected_malaria_cases',
                      'u5_total_simple_malaria_cases',
                      'u5_total_severe_malaria_cases',
                      'u5_total_tested_malaria_cases',
                      'u5_total_confirmed_malaria_cases',
                      'u5_total_treated_malaria_cases',
                      'u5_total_inpatient_all_causes',
                      'u5_total_malaria_inpatient',
                      'u5_total_death_all_causes',
                      'u5_total_malaria_death',
                      'u5_total_distributed_bednets',
                      'o5_total_consultation_all_causes',
                      'o5_total_suspected_malaria_cases',
                      'o5_total_simple_malaria_cases',
                      'o5_total_severe_malaria_cases',
                      'o5_total_tested_malaria_cases',
                      'o5_total_confirmed_malaria_cases',
                      'o5_total_treated_malaria_cases',
                      'o5_total_inpatient_all_causes',
                      'o5_total_malaria_inpatient',
                      'o5_total_death_all_causes',
                      'o5_total_malaria_death',
                      'pw_total_consultation_all_causes',
                      'pw_total_suspected_malaria_cases',
                      'pw_total_severe_malaria_cases',
                      'pw_total_tested_malaria_cases',
                      'pw_total_confirmed_malaria_cases',
                      'pw_total_treated_malaria_cases',
                      'pw_total_inpatient_all_causes',
                      'pw_total_malaria_inpatient',
                      'pw_total_death_all_causes',
                      'pw_total_malaria_death',
                      'pw_total_distributed_bednets',
                      'pw_total_anc1',
                      'pw_total_sp1',
                      'pw_total_sp2',
                      'stockout_act_children',
                      'stockout_act_youth', 'stockout_act_adult',
                      'stockout_artemether', 'stockout_quinine',
                      'stockout_serum',
                      'stockout_bednet', 'stockout_rdt', 'stockout_sp']
        args_values = message.content.strip().lower().split()
        arguments = dict(zip(args_names, args_values))
    except ValueError:
        # failure to split means we proabably lack a data or more
        # we can't process it.
        return reply.error("Le format du SMS est incorrect.")

    # convert form-data to int or bool respectively
    try:
        for key, value in arguments.items():
            if key.split('_')[0] in ('u5', 'o5', 'pw', 'month', 'year'):
                arguments[key] = int(value)
            if key.split('_')[0] == 'stockout':
                arguments[key] = MalariaR.YES if bool(int(value)) \
                    else MalariaR.NO
    except:
        logger.warning("Unable to convert SMS data to int: {}"
                       .format(message.content))
        # failure to convert means non-numeric value which we can't process.
        return reply.error("Les données sont malformées.")

    # check credentials
    try:
        provider = Provider.active.get(username=arguments['username'])
    except Provider.DoesNotExist:
        return reply.error("Ce nom d'utilisateur "
                           "({}) n'existe pas.".format(arguments['username']))

    if not provider.check_password(arguments['password']):
        return reply.error("Votre mot de passe est incorrect.")

    # now we have well formed and authenticated data.
    # let's check for business-logic errors.
    checker = MalariaRSourceReportChecker()

    # feed data holder with sms provided data
    for key, value in arguments.items():
        if key.split('_')[0] in ('u5', 'o5', 'pw',
                                 'stockout', 'year', 'month'):
            checker.set(key, value)

    # harmonized meta-data
    try:
        hc = provider.location
    except:
        hc = None
    checker.set('entity', hc)
    checker.set('hc', getattr(hc, 'slug', None))
    today = datetime.date.today()
    checker.set('fillin_day', today.day)
    checker.set('fillin_month', today.month)
    checker.set('fillin_year', today.year)
    checker.set('submit_time', message.event_on)
    checker.set('author', provider.name())
    checker.set('submitter', provider)

    # test the data
    checker.check()
    if not checker.is_valid():
        return reply.error(checker.errors.pop().render(short=True))

    # build requirements for report
    period = MonthPeriod.find_create_from(year=checker.get('year'),
                                          month=checker.get('month'))

    entity = HealthEntity.objects.get(slug=checker.get('hc'),
                                      type__slug='health_center')

    # expected reporting defines if report is expeted or not
    expected_reporting = ExpectedReporting.get_or_none(
        report_class=reportcls,
        period=period,
        within_period=False,
        entity=entity,
        within_entity=False,
        amount_expected=ExpectedReporting.EXPECTED_SINGLE)

    # should have already been checked in checker.
    if expected_reporting is None:
        logger.error("Expected reporting not found: "
                     "cls:{cls} - period:{period} - entity:{entity}"
                     .format(cls=reportcls, period=period, entity=entity))
        return reply.error("Aucun rapport de routine attendu à "
                           "{entity} pour {period}"
                           .format(entity=entity, period=period))

    report, text_message = create_report(provider=provider,
                                         expected_reporting=expected_reporting,
                                         completed_on=timezone.now(),
                                         integrity_checker=checker,
                                         data_source=message.content,)

    if report:
        return reply.success(text_message)
    else:
        return reply.error(text_message)
