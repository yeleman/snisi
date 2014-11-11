#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging
import datetime
from collections import OrderedDict

from django.utils import timezone

from snisi_core.models.Providers import Provider
from snisi_core.models.Entities import Entity
from snisi_core.models.Periods import MonthPeriod
from snisi_core.models.Reporting import (ExpectedReporting, ReportClass)
from snisi_nutrition import PROJECT_BRAND
from snisi_nutrition.integrity import (
    create_nut_weekly_report,
    NutritionRIntegrityChecker, create_nut_report,
    URENAMNutritionRIntegrityChecker,
    URENASNutritionRIntegrityChecker,
    URENINutritionRIntegrityChecker,
    StocksNutritionRIntegrityChecker)
from snisi_sms.reply import SMSReply

logger = logging.getLogger(__name__)
reportcls_nut = ReportClass.get_or_none(slug='nutrition_monthly_routine')


def nut_handler(message):
    if message.content.lower().startswith('nut '):
        return NUT_HANDLERS.get(
            message.content.lower().split(' ', 2)[1])(message)

    return False

KEYWORDS = {
    'nut': nut_handler,
}


def weekly_report(message):

    """
        nut w username password month year

            <all fields> (see args_names)
    """

    reply = SMSReply(message, PROJECT_BRAND)

    # create variables from text messages.
    try:
        args_names = ['kw', 'w', 'username', 'password',
                      'thursday',
                      'mam_screening', 'sam_screening', 'samc_screening',
                      'mam_cases', 'mam_deaths',
                      'sam_cases', 'sam_deaths',
                      'samc_cases', 'samc_deaths']

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
            if key in ('kw', 'w'):
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
        hc = Entity.get_or_none(provider.location.slug)
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

    entity = checker.get('entity')

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

    report, text_message = create_nut_weekly_report(
        provider=provider,
        expected_reporting=expected_reporting,
        completed_on=timezone.now(),
        integrity_checker=checker,
        data_source=message.content)

    if report:
        return reply.success(text_message)
    else:
        return reply.error(text_message)


def monthly_report(message):

    """
        nut username password month year

            <all fields> (see args_names)
    """

    reply = SMSReply(message, PROJECT_BRAND)

    # create variables from text messages.
    try:
        args_names = [
            'kw', 'kw2', 'username', 'password', 'month', 'year',
            'urenam_data', 'urenas_data', 'ureni_data', 'stocks_data']

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
            if key in ('kw', 'kw2', 'urenam_data',
                       'urenas_data', 'ureni_data', 'stocks_data'):
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

    # URENAM
    urenam_names = [
        'u23o6_total_start_m',
        'u23o6_total_start_f',
        'u23o6_new_cases',
        'u23o6_returned',
        'u23o6_total_in_m',
        'u23o6_total_in_f',
        'u23o6_healed',
        'u23o6_deceased',
        'u23o6_abandon',
        'u23o6_not_responding',
        'u23o6_total_out_m',
        'u23o6_total_out_f',
        'u23o6_referred',
        'u23o6_total_end_m',
        'u23o6_total_end_f',
        'u59o23_total_start_m',
        'u59o23_total_start_f',
        'u59o23_new_cases',
        'u59o23_returned',
        'u59o23_total_in_m',
        'u59o23_total_in_f',
        'u59o23_healed',
        'u59o23_deceased',
        'u59o23_abandon',
        'u59o23_not_responding',
        'u59o23_total_out_m',
        'u59o23_total_out_f',
        'u59o23_referred',
        'u59o23_total_end_m',
        'u59o23_total_end_f',
        'o59_total_start_m',
        'o59_total_start_f',
        'o59_new_cases',
        'o59_returned',
        'o59_total_in_m',
        'o59_total_in_f',
        'o59_healed',
        'o59_deceased',
        'o59_abandon',
        'o59_not_responding',
        'o59_total_out_m',
        'o59_total_out_f',
        'o59_referred',
        'o59_total_end_m',
        'o59_total_end_f',
        'pw_total_start_f',
        'pw_new_cases',
        'pw_returned',
        'pw_total_in_f',
        'pw_healed',
        'pw_deceased',
        'pw_abandon',
        'pw_not_responding',
        'pw_total_out_f',
        'pw_referred',
        'pw_total_end_f',
        'exsam_total_start_m',
        'exsam_total_start_f',
        'exsam_total_out_m',
        'exsam_total_out_f',
        'exsam_referred',
        'exsam_total_end_m',
        'exsam_total_end_f',
    ]

    # URENAS
    urenas_names = [
        'u59o6_total_start_m',
        'u59o6_total_start_f',
        'u59o6_new_cases',
        'u59o6_returned',
        'u59o6_total_in_m',
        'u59o6_total_in_f',
        'u59o6_transferred',
        'u59o6_healed',
        'u59o6_deceased',
        'u59o6_abandon',
        'u59o6_not_responding',
        'u59o6_total_out_m',
        'u59o6_total_out_f',
        'u59o6_referred',
        'u59o6_total_end_m',
        'u59o6_total_end_f',
        'o59_total_start_m',
        'o59_total_start_f',
        'o59_new_cases',
        'o59_returned',
        'o59_total_in_m',
        'o59_total_in_f',
        'o59_transferred',
        'o59_healed',
        'o59_deceased',
        'o59_abandon',
        'o59_not_responding',
        'o59_total_out_m',
        'o59_total_out_f',
        'o59_referred',
        'o59_total_end_m',
        'o59_total_end_f',
    ]

    # URENI
    ureni_names = [
        'u6_total_start_m',
        'u6_total_start_f',
        'u6_new_cases',
        'u6_returned',
        'u6_total_in_m',
        'u6_total_in_f',
        'u6_referred',
        'u6_healed',
        'u6_deceased',
        'u6_abandon',
        'u6_not_responding',
        'u6_total_out_m',
        'u6_total_out_f',
        'u6_transferred',
        'u6_total_end_m',
        'u6_total_end_f',
        'u59o6_total_start_m',
        'u59o6_total_start_f',
        'u59o6_new_cases',
        'u59o6_returned',
        'u59o6_total_in_m',
        'u59o6_total_in_f',
        'u59o6_referred',
        'u59o6_healed',
        'u59o6_deceased',
        'u59o6_abandon',
        'u59o6_not_responding',
        'u59o6_total_out_m',
        'u59o6_total_out_f',
        'u59o6_transferred',
        'u59o6_total_end_m',
        'u59o6_total_end_f',
        'o59_total_start_m',
        'o59_total_start_f',
        'o59_new_cases',
        'o59_returned',
        'o59_total_in_m',
        'o59_total_in_f',
        'o59_referred',
        'o59_healed',
        'o59_deceased',
        'o59_abandon',
        'o59_not_responding',
        'o59_total_out_m',
        'o59_total_out_f',
        'o59_transferred',
        'o59_total_end_m',
        'o59_total_end_f',
    ]

    # STOCKS
    stocks_names = [
        'plumpy_nut_initial',
        'plumpy_nut_received',
        'plumpy_nut_used',
        'plumpy_nut_lost',
        'milk_f75_initial',
        'milk_f75_received',
        'milk_f75_used',
        'milk_f75_lost',
        'milk_f100_initial',
        'milk_f100_received',
        'milk_f100_used',
        'milk_f100_lost',
        'resomal_initial',
        'resomal_received',
        'resomal_used',
        'resomal_lost',
        'plumpy_sup_initial',
        'plumpy_sup_received',
        'plumpy_sup_used',
        'plumpy_sup_lost',
        'supercereal_initial',
        'supercereal_received',
        'supercereal_used',
        'supercereal_lost',
        'supercereal_plus_initial',
        'supercereal_plus_received',
        'supercereal_plus_used',
        'supercereal_plus_lost',
        'oil_initial',
        'oil_received',
        'oil_used',
        'oil_lost',
        'amoxycilline_125_vials_initial',
        'amoxycilline_125_vials_received',
        'amoxycilline_125_vials_used',
        'amoxycilline_125_vials_lost',
        'amoxycilline_250_caps_initial',
        'amoxycilline_250_caps_received',
        'amoxycilline_250_caps_used',
        'amoxycilline_250_caps_lost',
        'albendazole_400_initial',
        'albendazole_400_received',
        'albendazole_400_used',
        'albendazole_400_lost',
        'vita_100_injectable_initial',
        'vita_100_injectable_received',
        'vita_100_injectable_used',
        'vita_100_injectable_lost',
        'vita_200_injectable_initial',
        'vita_200_injectable_received',
        'vita_200_injectable_used',
        'vita_200_injectable_lost',
        'iron_folic_acid_initial',
        'iron_folic_acid_received',
        'iron_folic_acid_used',
        'iron_folic_acid_lost',
    ]

    # now we have well formed and authenticated data.
    # let's check for business-logic errors.
    checker = NutritionRIntegrityChecker()

    # feed data holder with sms provided data
    for key, value in arguments.items():
        checker.set(key, value)

    # harmonized meta-data
    try:
        hc = Entity.get_or_none(provider.location.slug)
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

    # ensure we have a expecteds and all
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

    def prepare_checker_with(master_checker, uren_checker, uren,
                             sms_part, args_names):

        master_fields = ['month', 'year', 'username',
                         'entity', 'hc', 'fillin_day', 'fillin_month',
                         'fillin_year', 'submit_time', 'author', 'submitter']

        for field in master_fields:
            uren_checker.set(field, checker.get(field))

        # create variables from text messages.
        try:
            args_values = sms_part.strip().lower().split("-")
            arguments = dict(zip(args_names, args_values))
            assert len(args_values) == len(args_names)
        except (ValueError, AssertionError):
            # failure to split means we proabably lack a data or more
            # we can't process it.
            return "[{}] Le format du SMS est incorrect.".format(uren)

        # convert form-data to int or bool respectively
        try:
            for key, value in arguments.items():
                arguments[key] = int(value)
        except:
            logger.warning("Unable to convert/cast SMS data: {}"
                           .format(sms_part))
            # failure to convert means non-numeric value
            # which we can't process.
            return "Les données sont malformées."

        # feed data holder with sms provided data
        for key, value in arguments.items():
            uren_checker.set(key, value)

        # check data
        uren_checker.check(has_ureni=entity.has_ureni)

        if not uren_checker.is_valid():
            return uren_checker.errors.pop().render(short=True)

    # check data individually for sub reports
    integrity_map = OrderedDict([
        ('urenam', URENAMNutritionRIntegrityChecker),
        ('urenas', URENASNutritionRIntegrityChecker),
        ('ureni', URENINutritionRIntegrityChecker),
        ('stocks', StocksNutritionRIntegrityChecker),
    ])

    args_names_map = OrderedDict([
        ('urenam', urenam_names),
        ('urenas', urenas_names),
        ('ureni', ureni_names),
        ('stocks', stocks_names),
    ])

    sr_checkers = {}

    for sr, sr_cls in integrity_map.items():
        if sr == 'stocks' or getattr(entity, 'has_{}'.format(sr), False):
            logger.debug("checking {}".format(sr))
            sri = sr_cls()
            error = prepare_checker_with(
                master_checker=checker,
                uren_checker=sri,
                uren=sr,
                sms_part=arguments.get('{}_data'.format(sr)),
                args_names=args_names_map.get(sr))
            if error is not None:
                return reply.error(error)
            else:
                sr_checkers[sr] = sri

    # all sub reports have been checked. we can safely create reports
    logger.debug("ALL UREN AND STOCKS CHECKS PERFORMED. CREATING REPORT")

    report, text_message = create_nut_report(
        provider=provider,
        expected_reporting=expected_reporting,
        completed_on=timezone.now(),
        integrity_checker=checker,
        data_source=message.content,
        subreport_checkers=sr_checkers)

    if report:
        return reply.success(text_message)
    else:
        return reply.error(text_message)

NUT_HANDLERS = {
    'w': weekly_report,
    'm': monthly_report,
}
