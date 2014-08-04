#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging
import datetime

from django.utils import timezone

from snisi_core.models.Providers import Provider
from snisi_core.models.Reporting import (ExpectedReporting, ReportClass)
from snisi_epidemiology import PROJECT_BRAND
from snisi_epidemiology.models import EpiWeekPeriod
from snisi_epidemiology.integrity import (EpidemiologyRIntegrityChecker,
                                          create_epid_report)
from snisi_sms.reply import SMSReply

logger = logging.getLogger(__name__)
reportcls_epi = ReportClass.get_or_none(slug='epidemio_weekly_routine')


def epidemiology_handler(message):
    if message.content.lower().startswith('mado '):
        return epidemio(message)

    return False

KEYWORDS = {
    'mado': epidemiology_handler,
}


def epidemio(message):

    reply = SMSReply(message, PROJECT_BRAND)

    try:
        args_names = ['kw', 'username', 'password', 'date',
                      'ebola_case',
                      'ebola_death',
                      'acute_flaccid_paralysis_case',
                      'acute_flaccid_paralysis_death',
                      'influenza_a_h1n1_case',
                      'influenza_a_h1n1_death',
                      'cholera_case',
                      'cholera_death',
                      'red_diarrhea_case',
                      'red_diarrhea_death',
                      'measles_case',
                      'measles_death',
                      'yellow_fever_case',
                      'yellow_fever_death',
                      'neonatal_tetanus_case',
                      'neonatal_tetanus_death',
                      'meningitis_case',
                      'meningitis_death',
                      'rabies_case',
                      'rabies_death',
                      'acute_measles_diarrhea_case',
                      'acute_measles_diarrhea_death',
                      'other_notifiable_disease_case',
                      'other_notifiable_disease_death']

        args_values = message.content.strip().lower().split()
        arguments = dict(zip(args_names, args_values))
        assert len(args_values) == len(args_names)
    except (ValueError, AssertionError):
        # failure to split means we proabably lack a data or more
        # we can't process it.
        return reply.error("Le format du SMS est incorrect.")

    # convert form-data to int or bool respectively
    try:
        for key, value in arguments.items():

            if key in ('kw',):
                continue
            elif key in ('username', 'password'):
                arguments[key] = value.strip()
            elif key in ('date', ):
                day, month, year = value.split("/")
                arguments['year'] = int(year)
                arguments['month'] = int(month)
                arguments['day'] = int(day)
                arguments.pop(key)
            else:
                arguments[key] = int(value)
    except:
        logger.warning("Unable to convert/cast SMS data: {}"
                       .format(message.content))
        # failure to convert means non-numeric value which we can't process.
        return reply.error("Les données sont malformées.")

    # check credentials
    try:
        provider = Provider.active.get(username=arguments['username'])
    except Provider.DoesNotExist:
        return reply.error("Ce nom d'utilisateur ({}) n'existe pas."
                           .format(arguments['username']))
    if not provider.check_password(arguments['password']):
        return reply.error("Votre mot de passe est incorrect.")

    # try:
    #     arguments['reporting_date'] = datetime.date(arguments.get('year'),
    #                                                 arguments.get('month'),
    #                                                 arguments.get('day'))
    # except:
    #     return reply.error("Les données sont malformées (date).")

    checker = EpidemiologyRIntegrityChecker()

    for key, value in arguments.items():
        checker.set(key, value)

    try:
        hc = provider.location
    except:
        hc = None

    logger.debug("HC: {}".format(hc))

    checker.set('entity', hc)
    checker.set('hc', getattr(hc, 'slug', None))
    checker.set('submit_time', message.event_on)
    checker.set('author', provider.name())
    checker.set('submitter', provider)

    # test the data
    checker.check()
    if not checker.is_valid():
        return reply.error(checker.errors.pop().render(short=True))

    # build requirements for report
    # period = EpiWeekPeriod.find_create_by_date(checker.get('submit_time'))
    period = checker.get('period')
    entity = checker.get('entity')

    # expected reporting defines if report is expeted or not
    expected_reporting = ExpectedReporting.get_or_none(
        report_class=reportcls_epi,
        period=period,
        within_period=False,
        entity=entity,
        within_entity=False,
        amount_expected=ExpectedReporting.EXPECTED_SINGLE)

    # should have already been checked in checker.
    if expected_reporting is None:
        logger.error("Expected reporting not found: "
                     "cls:{cls} - period:{period} - entity:{entity}"
                     .format(cls=reportcls_epi, period=period, entity=entity))
        return reply.error("Aucun rapport de routine attendu à "
                           "{entity} pour {period}"
                           .format(entity=entity, period=period))

    report, text_message = create_epid_report(
        provider=provider,
        expected_reporting=expected_reporting,
        completed_on=timezone.now(),
        integrity_checker=checker,
        data_source=message.content)

    if report:
        return reply.success(text_message)
    else:
        return reply.error(text_message)
