#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging
import os

from django.core.management.base import BaseCommand
from optparse import make_option
from django.utils import timezone
from django.conf import settings
from rtfw import Renderer

from snisi_core.models.Periods import MonthPeriod
from snisi_core.models.Projects import Cluster
from snisi_malaria.rtf_export import (health_region_report,
                                      health_district_report)
from snisi_tools.path import mkdir_p

logger = logging.getLogger(__name__)


def generate_report(year, quarter_num, entity):

    fail = (None, None)

    quarter_month_matrix = {
        '1': 1,
        '2': 4,
        '3': 7,
        '4': 10
    }
    if not quarter_num in quarter_month_matrix.keys():
        logger.error("Incorrect quarter {}".format(quarter_num))
        return fail
    try:
        year = int(year)
        if year > timezone.now().year:
            raise ValueError("Year in the future")
    except:
        logger.error("Incorrect quarter {}".format(quarter_num))
        return fail

    start_period = MonthPeriod.find_create_from(
        year=year,
        month=quarter_month_matrix.get(quarter_num),
        dont_create=True)
    periods = [start_period]
    for _ in range(1, 3):
        periods.append(periods[-1].following())
    end_period = periods[-1]

    if end_period.end_on > timezone.now():
        logger.error("Quarter in the future")
        return fail

    # check that Entity was part of Cluster at that time
    if entity.participations.get(cluster__slug='malaria_monthly_routine') \
                            .modified_on > end_period.start_on:
        logger.debug("{} was not part of Cluster".format(entity))
        return fail

    quarter = "T{}-{}".format(quarter_num, year)

    doc_creator = {
        'health_center': None,
        'health_district': health_district_report,
        'health_region': health_region_report,
    }.get(entity.type.slug)

    if doc_creator is None:
        return fail

    filename = ("{entity.slug}-{entity.name}_{quarter}.rtf"
                .format(entity=entity, quarter=quarter))

    document = doc_creator(entity=entity,
                           periods=periods,
                           quarter_num=quarter_num,
                           year=year)

    return document, filename


class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
        make_option('-y',
                    help='Year',
                    action='store',
                    dest='year'),
        make_option('-q',
                    help='Quarter',
                    action='store',
                    dest='quarter_num'),
    )


    def handle(self, *args, **options):

        # set/create the destination folder
        report_folder = os.path.join(settings.FILES_REPOSITORY,
                                     "malaria",
                                     "quarter_reports")
        mkdir_p(report_folder)

        # inputs
        year = options.get('year')
        quarter_num = options.get('quarter_num')

        logger.info("Exporting quarter reports for Q{}-{} to {}"
                    .format(quarter_num, year, report_folder))

        cluster = Cluster.get_or_none("malaria_monthly_routine")

        for entity in cluster.members():
            logger.info(entity)

            doc, filename = generate_report(year, quarter_num, entity)
            if doc and filename:
                filepath = os.path.join(report_folder, filename)
                with open(filepath, 'w') as f:
                    Renderer().Write(doc, f)
                logger.info("\tCreated {}".format(filepath))
            else:
                logger.info("\tNo document for {}".format(entity))

