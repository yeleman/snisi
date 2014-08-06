#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging
import datetime

from django.utils import timezone

from snisi_core.models.Providers import Provider
from snisi_malaria.integrity import PROJECT_BRAND
from snisi_core.models.Notifications import Notification
from snisi_core.models.Reporting import ExpectedReporting
from snisi_malaria.aggregations import get_districts
from snisi_malaria import (ROUTINE_EXTENDED_REPORTING_END_DAY,
                           ROUTINE_DISTRICT_AGG_DAY)

logger = logging.getLogger(__name__)


def get_expected_source_reports(period):
    return ExpectedReporting.objects.filter(
        report_class__slug='malaria_monthly_routine',
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

    now = timezone.now()
    expirate_on = datetime.datetime(now.year, now.month,
                                    ROUTINE_DISTRICT_AGG_DAY, 8, 0)

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
                     "n'est pas arrivé. Le district et la région ont été "
                     "notifiés. Merci de prendre des mesures pour la "
                     "collecte de {periodf}.".format(
                    period=period,
                    periodf=period.following(),
                    entity=exp.entity))

    # send notification to districts
    for district in get_districts():

        nb_missing = len([1 for e in get_expected_source_reports(period)
                          if e.entity.get_health_district() == district])

        if nb_missing == 0:
            text = ("Bravo! Tous les rapports de routine paludisme "
                    " de votre districts ont été "
                    "envoyés. Vous pouvez les consulter et les valider "
                    "dans le système.")
        else:
            text = ("{nb} rapport(s) de routine paludisme de votre "
                    "district n'ont pas été envoyés dans le système. "
                    "Merci de prendre des dispositions pour la prochaine "
                    "collecte. Il est temps désormais de valider les "
                    "rapports arrivés.")

        for recipient in Provider.active.filter(location=district,
                                                role__slug='charge_sis'):

            logger.debug("Sending notif to {}".format(recipient))

            Notification.create(
                provider=recipient,
                deliver=Notification.TODAY,
                expirate_on=expirate_on,
                category=PROJECT_BRAND,
                text=text)
