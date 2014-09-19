#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging
import datetime

from django.utils import timezone

from snisi_core.models.Providers import Provider
# from snisi_core.models.Roles import Role
from snisi_core.models.Entities import Entity
from snisi_core.models.Periods import MonthPeriod
from snisi_core.models.Reporting import (ExpectedReporting, ReportClass)
from snisi_nutrition import PROJECT_BRAND
from snisi_nutrition.integrity import (
    NutritionRIntegrityChecker, create_nut_report)
from snisi_sms.reply import SMSReply

logger = logging.getLogger(__name__)
reportcls_nut = ReportClass.get_or_none(slug='nutrition_monthly_routine')


def nut_handler(message):
    if message.content.lower().startswith('nut '):
        return nutrition(message)

    return False

KEYWORDS = {
    'nut': nut_handler,
}


def nutrition(message):

    """
        nut username password month year

            <all fields> (see args_names)
    """

    reply = SMSReply(message, PROJECT_BRAND)

    # create variables from text messages.
    try:
        args_names = ['kw', 'username', 'password', 'month', 'year']

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

    # now we have well formed and authenticated data.
    # let's check for business-logic errors.
    checker = NutritionRIntegrityChecker()

    # feed data holder with sms provided data
    for key, value in arguments.items():
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

    entity = Entity.get_or_none(checker.get('hc'))

    # expected reporting defines if report is expeted or not
    expected_reporting = ExpectedReporting.get_or_none(
        report_class=reportcls_nut,
        period=period,
        within_period=False,
        entity=entity,
        within_entity=False,
        amount_expected=ExpectedReporting.EXPECTED_SINGLE)

    # should have already been checked in checker.
    if expected_reporting is None:
        logger.error("Expected reporting not found: "
                     "cls:{cls} - period:{period} - entity:{entity}"
                     .format(cls=reportcls_nut, period=period, entity=entity))
        return reply.error("Aucun rapport de routine attendu à "
                           "{entity} pour {period}"
                           .format(entity=entity, period=period))

    report, text_message = create_nut_report(
        provider=provider,
        expected_reporting=expected_reporting,
        completed_on=timezone.now(),
        integrity_checker=checker,
        data_source=message.content)

    if report:
        return reply.success(text_message)
    else:
        return reply.error(text_message)
