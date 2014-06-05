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
from snisi_reprohealth import PROJECT_BRAND
from snisi_reprohealth.integrity import (
    ProvidedServicesRIntegrityChecker, create_services_report,
    FinancialRIntegrityChecker, create_financial_report,
    ContraceptiveStockRIntegrityChecker, create_stock_report)
from snisi_sms.reply import SMSReply

logger = logging.getLogger(__name__)
reportcls_services = ReportClass.get_or_none(slug='msi_services_monthly_routine')
reportcls_financial = ReportClass.get_or_none(slug='msi_financial_monthly_routine')
reportcls_stocks = ReportClass.get_or_none(slug='msi_stocks_monthly_routine')


def msi_handler(message):
    if message.content.lower().startswith('msi '):
        if message.content.lower().startswith('msi services'):
            return msi_services(message)
        elif message.content.lower().startswith('msi financial'):
            return msi_financial(message)
        elif message.content.lower().startswith('msi stocks'):
            return msi_stocks(message)

    return False

KEYWORDS = {
    'msi': msi_handler,
}


def msi_services(message):

    """
        msi services username password month year
            tubal_ligations intrauterine_devices injections pills
            male_condoms female_condoms emergency_controls implants
            new_clients previous_clients under25_visits over25_visits
            very_first_visits short_term_method_visits long_term_method_visits
            hiv_counseling_clients hiv_tests hiv_positive_results
            implant_removals iud_removal
    """

    reply = SMSReply(message, PROJECT_BRAND)

    # create variables from text messages.
    try:
        args_names = ['kw1', 'kw2', 'username', 'password', 'month', 'year',
                      'tubal_ligations', 'intrauterine_devices', 'injections',
                      'pills', 'male_condoms', 'female_condoms',
                      'emergency_controls', 'implants', 'new_clients',
                      'previous_clients', 'under25_visits', 'over25_visits',
                      'very_first_visits', 'short_term_method_visits',
                      'long_term_method_visits', 'hiv_counseling_clients',
                      'hiv_tests', 'hiv_positive_results',
                      'implant_removals', 'iud_removal']
        args_values = message.content.strip().lower().split()
        arguments = dict(zip(args_names, args_values))
    except ValueError:
        # failure to split means we proabably lack a data or more
        # we can't process it.
        return reply.error("Le format du SMS est incorrect.")

    # convert form-data to int or bool respectively
    try:
        for key, value in arguments.items():
            if key in ('kw1', 'kw2'):
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
        return reply.error("Ce nom d'utilisateur "
                           "({}) n'existe pas.".format(arguments['username']))

    if not provider.check_password(arguments['password']):
        return reply.error("Votre mot de passe est incorrect.")

    # now we have well formed and authenticated data.
    # let's check for business-logic errors.
    checker = ProvidedServicesRIntegrityChecker()

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
        report_class=reportcls_services,
        period=period,
        within_period=False,
        entity=entity,
        within_entity=False,
        amount_expected=ExpectedReporting.EXPECTED_SINGLE)

    # should have already been checked in checker.
    if expected_reporting is None:
        logger.error("Expected reporting not found: "
                     "cls:{cls} - period:{period} - entity:{entity}".format(
                        cls=reportcls_services, period=period, entity=entity))
        return reply.error("Aucun rapport de routine attendu à "
                           "{entity} pour {period}".format(
                                entity=entity, period=period))

    report, text_message = create_services_report(
        provider=provider,
        expected_reporting=expected_reporting,
        completed_on=timezone.now(),
        integrity_checker=checker,
        data_source=message.content)

    if report:
        return reply.success(text_message)
    else:
        return reply.error(text_message)


def msi_financial(message):

    """
        msi financial username password month year
            intrauterine_devices_qty
            intrauterine_devices_price
            intrauterine_devices_revenue
            implants_qty
            implants_price
            implants_revenue
            injections_qty
            injections_price
            injections_revenue
            pills_qty
            pills_price
            pills_revenue
            male_condoms_qty
            male_condoms_price
            male_condoms_revenue
            female_condoms_qty
            female_condoms_price
            female_condoms_revenue
            hiv_tests_qty
            hiv_tests_price
            hiv_tests_revenue
            iud_removal_qty
            iud_removal_price
            iud_removal_revenue
            implant_removal_qty
            implant_removal_price
            implant_removal_revenue
    """

    reply = SMSReply(message, PROJECT_BRAND)

    # create variables from text messages.
    try:
        args_names = ['kw1', 'kw2', 'username', 'password', 'month', 'year',
                      'intrauterine_devices_qty',
                      'intrauterine_devices_price',
                      'intrauterine_devices_revenue',
                      'implants_qty',
                      'implants_price',
                      'implants_revenue',
                      'injections_qty',
                      'injections_price',
                      'injections_revenue',
                      'pills_qty',
                      'pills_price',
                      'pills_revenue',
                      'male_condoms_qty',
                      'male_condoms_price',
                      'male_condoms_revenue',
                      'female_condoms_qty',
                      'female_condoms_price',
                      'female_condoms_revenue',
                      'hiv_tests_qty',
                      'hiv_tests_price',
                      'hiv_tests_revenue',
                      'iud_removal_qty',
                      'iud_removal_price',
                      'iud_removal_revenue',
                      'implant_removal_qty',
                      'implant_removal_price',
                      'implant_removal_revenue']
        args_values = message.content.strip().lower().split()
        arguments = dict(zip(args_names, args_values))
    except ValueError:
        # failure to split means we proabably lack a data or more
        # we can't process it.
        return reply.error("Le format du SMS est incorrect.")

    # convert form-data to int or bool respectively
    try:
        for key, value in arguments.items():
            if key in ('kw1', 'kw2'):
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
        return reply.error("Ce nom d'utilisateur "
                           "({}) n'existe pas.".format(arguments['username']))

    if not provider.check_password(arguments['password']):
        return reply.error("Votre mot de passe est incorrect.")

    # now we have well formed and authenticated data.
    # let's check for business-logic errors.
    checker = FinancialRIntegrityChecker()

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
        report_class=reportcls_financial,
        period=period,
        within_period=False,
        entity=entity,
        within_entity=False,
        amount_expected=ExpectedReporting.EXPECTED_SINGLE)

    # should have already been checked in checker.
    if expected_reporting is None:
        logger.error("Expected reporting not found: "
                     "cls:{cls} - period:{period} - entity:{entity}".format(
                        cls=reportcls_financial, period=period, entity=entity))
        return reply.error("Aucun rapport de routine attendu à "
                           "{entity} pour {period}".format(
                                entity=entity, period=period))

    report, text_message = create_financial_report(
        provider=provider,
        expected_reporting=expected_reporting,
        completed_on=timezone.now(),
        integrity_checker=checker,
        data_source=message.content)

    if report:
        return reply.success(text_message)
    else:
        return reply.error(text_message)


def msi_stocks(message):

    """
        msi stocks username password month year
            intrauterine_devices_initial
            intrauterine_devices_used
            intrauterine_devices_received
            implants_initial
            implants_used
            implants_received
            injections_initial
            injections_used
            injections_received
            pills_initial
            pills_used
            pills_received
            male_condoms_initial
            male_condoms_used
            male_condoms_received
            female_condoms_initial
            female_condoms_used
            female_condoms_received
            hiv_tests_initial
            hiv_tests_used
            hiv_tests_received
            intrauterine_devices_observation
            implants_observation
            injections_observation
            pills_observation
            male_condoms_observation
            female_condoms_observation
            hiv_tests_observation

            *_observation has spaces replaced by #
            *_observation are optional. - if not set.
    """

    reply = SMSReply(message, PROJECT_BRAND)

    # create variables from text messages.
    try:
        args_names = ['kw1', 'kw2', 'username', 'password', 'month', 'year',
                      'intrauterine_devices_qty',
                      'intrauterine_devices_price',
                      'intrauterine_devices_revenue',
                      'implants_qty',
                      'implants_price',
                      'implants_revenue',
                      'injections_qty',
                      'injections_price',
                      'injections_revenue',
                      'pills_qty',
                      'pills_price',
                      'pills_revenue',
                      'male_condoms_qty',
                      'male_condoms_price',
                      'male_condoms_revenue',
                      'female_condoms_qty',
                      'female_condoms_price',
                      'female_condoms_revenue',
                      'hiv_tests_qty',
                      'hiv_tests_price',
                      'hiv_tests_revenue',
                      'iud_removal_qty',
                      'iud_removal_price',
                      'iud_removal_revenue',
                      'implant_removal_qty',
                      'implant_removal_price',
                      'implant_removal_revenue']
        args_values = message.content.strip().lower().split()
        arguments = dict(zip(args_names, args_values))
    except ValueError:
        # failure to split means we proabably lack a data or more
        # we can't process it.
        return reply.error("Le format du SMS est incorrect.")

    # convert form-data to int or bool respectively
    try:
        for key, value in arguments.items():
            if key in ('kw1', 'kw2'):
                continue
            elif key in ('username', 'password'):
                arguments[key] = value.strip()
            elif key.endswith('_observation'):
                if value.strip() == '-':
                    arguments[key] = None
                else:
                    arguments[key] = value.replace('#', ' ')
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
        return reply.error("Ce nom d'utilisateur "
                           "({}) n'existe pas.".format(arguments['username']))

    if not provider.check_password(arguments['password']):
        return reply.error("Votre mot de passe est incorrect.")

    # now we have well formed and authenticated data.
    # let's check for business-logic errors.
    checker = ContraceptiveStockRIntegrityChecker()

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
        report_class=reportcls_stocks,
        period=period,
        within_period=False,
        entity=entity,
        within_entity=False,
        amount_expected=ExpectedReporting.EXPECTED_SINGLE)

    # should have already been checked in checker.
    if expected_reporting is None:
        logger.error("Expected reporting not found: "
                     "cls:{cls} - period:{period} - entity:{entity}".format(
                        cls=reportcls_stocks, period=period, entity=entity))
        return reply.error("Aucun rapport de routine attendu à "
                           "{entity} pour {period}".format(
                                entity=entity, period=period))

    report, text_message = create_stock_report(
        provider=provider,
        expected_reporting=expected_reporting,
        completed_on=timezone.now(),
        integrity_checker=checker,
        data_source=message.content)

    if report:
        return reply.success(text_message)
    else:
        return reply.error(text_message)
