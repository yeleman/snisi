#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging
import datetime

from django.utils import timezone

from snisi_core.models.Providers import Provider
from snisi_nutrition import PROJECT_BRAND, ROUTINE_EXTENDED_REPORTING_END_DAY
from snisi_core.models.Notifications import Notification
from snisi_core.models.Reporting import ExpectedReporting


logger = logging.getLogger(__name__)


def get_expected_source_reports(period):
    return ExpectedReporting.objects.filter(
        report_class__slug='nutrition_monthly_routine',
        period=period,
        entity__type__slug='health_center',
        completion_status__in=('', ExpectedReporting.COMPLETION_MISSING))


def end_of_reporting_period_notifications(period):
    """ Send notifications to DTC at end of reporting period """

    now = timezone.now()
    expirate_on = datetime.datetime(now.year, now.month,
                                    ROUTINE_EXTENDED_REPORTING_END_DAY, 0, 0)

    for exp in get_expected_source_reports(period):

        # send notification to DTC with missing reports
        for recipient in Provider.active.filter(location=exp.entity):

            logger.debug("Sending notif to {}".format(recipient))

            Notification.create(
                provider=recipient,
                deliver=Notification.TODAY,
                expirate_on=expirate_on,
                category=PROJECT_BRAND,
                text="Le rapport de routine de {period} pour {entity} "
                     "n'est pas encore arrivé. Envoyez-le impérativement "
                     "avant le 10. Merci."
                     .format(period=period, entity=exp.entity))


def end_of_extended_reporting_period_notifications(period):
    """ Send notifications to DTC at end of extended reporting period

        Send notifications to Districts """

    for exp in get_expected_source_reports(period):

        # send notification to DTC with missing reports
        for recipient in Provider.active.filter(location=exp.entity):

            logger.debug("Sending notif to {}".format(recipient))

            Notification.create(
                provider=recipient,
                deliver=Notification.TODAY,
                expirate_on=period.following().end_on,
                category=PROJECT_BRAND,
                text="Votre rapport de routine de {period} "
                     "n'est pas arrivé. Le niveau central a été "
                     "notifié. Merci de prendre des mesures pour la "
                     "collecte de {periodf}.".format(
                    period=period,
                    periodf=period.following(),
                    entity=exp.entity))
