#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging

from django.utils import timezone

from snisi_sms.reply import SMSReply
from snisi_core.models.Providers import Provider
from snisi_trachoma import PROJECT_BRAND
from snisi_trachoma.integrity import (TTBacklogMissionStartChecker,
                                      TTBacklogMissionEndChecker,
                                      TTBacklogVisitChecker,
                                      create_mission_report,
                                      create_visit_report,
                                      close_mission_report)

logger = logging.getLogger(__name__)


def trachoma_handler(message):
    if message.content.lower().startswith('tt '):
        if message.content.lower().startswith('tt start'):
            return trachoma_start_mission(message)
        elif message.content.lower().startswith('tt visit'):
            return trachoma_visit_village(message)
        elif message.content.lower().startswith('tt end'):
            return trachoma_end_mission(message)
        else:
            return False

    return False

KEYWORDS = {
    'tt': trachoma_handler,
}


def check_create_provider(username, password, reply):
    try:
        provider = Provider.active.get(username=username)
    except Provider.DoesNotExist:
        reply.error("Ce nom d'utilisateur ({}) n'existe pas.".format(username))
        return None

    if not provider.role.slug in ('tt_tso', 'tt_opt', 'tt_amo'):
        reply.error("Votre rôle ne vous permet pas de créer "
                    "des rapports BacklogTT")
        return None

    if not provider.check_password(password):
        reply.error("Votre mot de passe est incorrect.")
        return None

    return provider


def trachoma_start_mission(message, **kwargs):
    reply = SMSReply(message, PROJECT_BRAND)
    try:
        args_names = ['kw1', 'kw2', 'username', 'password',
                      'district', 'started_on', 'operator_type', 'strategy']
        args_values = message.content.strip().lower().split()
        arguments = dict(zip(args_names, args_values))
    except ValueError:
        # failure to split means w e proabably lack a data or more
        # we can't process it.
        return reply.error("Le format du SMS est incorrect.")

    # check credentials
    provider = check_create_provider(arguments['username'],
                                     arguments['password'], reply)
    if provider is None:
        return True

    checker = TTBacklogMissionStartChecker()

    # feed data holder with sms provided data
    for key, value in arguments.items():
        checker.set(key, value)

    checker.set('submit_time', message.event_on)
    checker.set('submitter', provider)

    # test the data (existing report, values)
    checker.check()
    if not checker.is_valid():
        return reply.error(checker.feedbacks.pop().render(short=True))

    report, text_message = create_mission_report(
        provider=provider,
        expected_reporting=checker.get('expected_reporting'),
        completed_on=None,
        integrity_checker=checker,
        data_source=message.content)

    if report:
        return reply.success(text_message)
    else:
        return reply.error(text_message)


def trachoma_visit_village(message, **kwargs):
    reply = SMSReply(message, PROJECT_BRAND)
    try:
        args_names = ['kw1', 'kw2', 'username', 'password', 'location',
                      'consultation_male', 'consultation_female',
                      'surgery_male', 'surgery_female',
                      'refusal_male', 'refusal_female',
                      'recidivism_male', 'recidivism_female',
                      'community_assistance',
                      'arrived_on', 'left_on']
        args_values = message.content.strip().lower().split()
        arguments = dict(zip(args_names, args_values))
    except ValueError:
        # failure to split means we proabably lack a data or more
        # we can't process it.
        return reply.error("Le format du SMS est incorrect.")

    # check credentials
    provider = check_create_provider(arguments['username'],
                                     arguments['password'], reply)
    if provider is None:
        return True

    # Visit depends on an ExpectedReporting AND an open MissionR from which
    # the expected period is set.
    checker = TTBacklogVisitChecker()

    # feed data holder with sms provided data
    for key, value in arguments.items():
        checker.set(key, value)

    checker.set('submit_time', message.event_on)
    checker.set('submitter', provider)

    # test the data (existing report, values)
    checker.check()
    if not checker.is_valid():
        return reply.error(checker.feedbacks.pop().render(short=True))

    report, text_message = create_visit_report(
        provider=provider,
        expected_reporting=None,
        completed_on=timezone.now(),
        integrity_checker=checker,
        data_source=message.content)

    if report:
        return reply.success(text_message)
    else:
        return reply.error(text_message)


def trachoma_end_mission(message, **kwargs):
    reply = SMSReply(message, PROJECT_BRAND)
    try:
        args_names = ['kw1', 'kw2', 'username', 'password',
                      'district', 'ended_on']
        args_values = message.content.strip().lower().split()
        arguments = dict(zip(args_names, args_values))
    except ValueError:
        # failure to split means we proabably lack a data or more
        # we can't process it.
        return reply.error("Le format du SMS est incorrect.")

    # check credentials
    provider = check_create_provider(arguments['username'],
                                     arguments['password'], reply)
    if provider is None:
        return True

    checker = TTBacklogMissionEndChecker()

    # feed data holder with sms provided data
    for key, value in arguments.items():
        checker.set(key, value)

    checker.set('submit_time', message.event_on)
    checker.set('submitter', provider)

    # test the data (existing report, values)
    checker.check()
    if not checker.is_valid():
        return reply.error(checker.feedbacks.pop().render(short=True))

    report, text_message = close_mission_report(
        provider=provider,
        expected_reporting=checker.get('expected_reporting'),
        completed_on=timezone.now(),
        integrity_checker=checker,
        data_source=message.content)

    if report:
        return reply.success(text_message)
    else:
        return reply.error(text_message)
