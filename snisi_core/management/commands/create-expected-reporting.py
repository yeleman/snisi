#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging
import datetime

from django.core.management.base import BaseCommand
from django.utils import timezone
from optparse import make_option

from snisi_core.models.Projects import Domain
from snisi_tools.misc import import_path

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
        make_option('-d',
                    help='Date to build the report for. Optional '
                         '(defaults to now()). Can be `previous` '
                         'for previous period based on now.',
                    action='store',
                    default='',
                    dest='date'),
        make_option('-t',
                    help='Period Type: DayPeriod, WeekPeriod, MonthPeriod..',
                    action='store',
                    dest='period_type'),
    )

    def handle(self, *args, **options):

        period_type = options.get('period_type')
        period_cls = import_path('snisi_core.models.{}'
                                 .format(period_type), failsafe=True)
        if period_cls is None:
            logger.error("Invalid period-type {}".format(period_type))
            return

        date_str = options.get('date', '')
        try:
            if len(date_str) and date_str.lower() not in ('auto', 'previous'):
                new_date = datetime.datetime(*[int(e) for e in date_str.lower().split('-')]) \
                                   .replace(tzinfo=timezone.utc)
            else:
                new_date = timezone.now()
        except:
            new_date = None

        if new_date is None:
            logger.error("Invalid date string {}".format(date_str))
            return

        period = period_cls.find_create_by_date(new_date)

        if date_str.lower() == 'previous':
            period = period.previous()

        logger.info("Period: {} from {}".format(period, new_date))

        for domain in Domain.active.all():
            logger.info(domain)

            create_expected_for = domain.import_from(
                'expected.create_expected_for')
            if create_expected_for is None:
                logger.info("\t Skipping domain {}".format(domain))
                continue

            logger.info("Creating expected reportings for {}/{}"
                        .format(domain, period))

            created_list = create_expected_for(period)
            logger.info("Created {} expected reportings for {}/{}"
                        .format(len(created_list), domain, period))
