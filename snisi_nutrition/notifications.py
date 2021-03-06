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
from snisi_nutrition.models.Monthly import NutritionR
from snisi_nutrition.indicators.mam import (
    MAMHealedRate, MAMDeceasedRate, MAMAbandonRate)
from snisi_nutrition.indicators.sam import (
    SAMHealedRate, SAMDeceasedRate, SAMAbandonRate)


logger = logging.getLogger(__name__)


def get_expected_source_reports(period):
    return ExpectedReporting.objects.filter(
        report_class__slug='nutrition_monthly_routine',
        period=period,
        entity__type__slug='health_center',
        completion_status__in=('', ExpectedReporting.COMPLETION_MISSING))


def get_performance_text(report):
    indicators = {'mam': None, 'mas': None}

    if report.entity.casted().has_urenam:
        indicators['mam'] = {
            'healed': MAMHealedRate(entity=report.entity,
                                    period=report.period),
            'abandon': MAMAbandonRate(entity=report.entity,
                                      period=report.period),
            'deceased': MAMDeceasedRate(entity=report.entity,
                                        period=report.period),
        }

    if report.entity.casted().has_urenas \
            or report.entity.casted().has_ureni:
        indicators['sam'] = {
            'healed': SAMHealedRate(entity=report.entity,
                                    period=report.period),
            'abandon': SAMAbandonRate(entity=report.entity,
                                      period=report.period),
            'deceased': SAMDeceasedRate(entity=report.entity,
                                        period=report.period),
        }

    # no indicator to talk about
    if indicators['mam'] is None and indicators['sam'] is None:
        return None

    nb_bad_indic = sum(
        [1 for idict in indicators.values()
         if idict is not None
         for indic in idict.values()
         if indic.get_class() != indic.GOOD])

    if nb_bad_indic == 0:
        return ("Les indicateurs de performance concernant votre "
                "rapport mensuel semblent satisfaisant. "
                "Merci de rester vigilant.")

    umap = {
        'mam': "MAM",
        'sam': "MAS"
    }

    imap = {
        'healed': "Tx guérison",
        'abandon': "Tx abandon",
        'deceased': "Tx décès"
    }

    indic_list = []
    for uren, udict in indicators.items():
        if udict is None:
            continue
        for key, indic in udict.items():
            if not indic.get_class() == indic.GOOD:
                indic_list.append("{u}/{i}: {v}"
                                  .format(u=umap.get(uren),
                                          i=imap.get(key),
                                          v=indic.human))
    return ("Attention, {nb} indicateur(s) de performance non satisfaisant "
            "concernant votre rapport mensuel: {l}"
            .format(nb=nb_bad_indic,
                    l=" - ".join(indic_list)))


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


def performance_indicators_notifications(period):

    # send warning message to DTC with poor performance
    for report in NutritionR.objects.filter(period=period):

        text = get_performance_text(report)
        if text is None:
            continue

        for recipient in Provider.active.filter(location=report.entity):
            logger.debug("Sending notif to {}".format(recipient))

            Notification.create(
                provider=recipient,
                deliver=Notification.SOON,
                expirate_on=period.following().end_on,
                category=PROJECT_BRAND,
                text=text)


def inputs_stockouts_notifications(period):

    from snisi_nutrition.models.Stocks import NutritionStocksR

    def create_notif(recipient, text):
        Notification.create(
            provider=recipient,
            deliver=Notification.SOON,
            expirate_on=period.following().end_on,
            category=PROJECT_BRAND,
            text=text)

    # send warning message to DTC with poor performance
    for report in NutritionR.objects.filter(period=period):

        missing_inputs = []
        ureni_inputs = report.stocks_report.inputs(ureni_only=True)
        for inp in report.stocks_report.inputs():

            # exclude URENI inputs if not URENI
            if not report.entity.casted().has_ureni and inp in ureni_inputs:
                continue

            if not report.stocks_report.balance_for(inp):
                missing_inputs.append(inp)

        if not len(missing_inputs):
            continue

        missing_inputs_names = " * ".join([NutritionStocksR.input_str(inp)
                                           for inp in missing_inputs])

        text = ("Attention, {nb} stock(s) d'intrant à zéro. Approvisionnez "
                "vous urgemment au CSRéf: {l}"
                .format(nb=len(missing_inputs),
                        l=missing_inputs_names))
        text2 = ("Attention, {loc} est en rupture de {nb} intrant(s): {l}"
                 .format(loc=report.entity.casted(),
                         nb=len(missing_inputs),
                         l=missing_inputs_names))

        for recipient in Provider.active.filter(location=report.entity):
            logger.debug("Sending notif to {}".format(recipient))

            # send notification to DTC
            create_notif(recipient, text)

            ds_slugs = ['medecin_chef', 'pf_nut']
            ds_recipients = Provider.find_at(location=report.entity.casted(),
                                             slugs=ds_slugs)
            ds_recipients += Provider.find_at(
                location=report.entity.casted().get_health_district()
                .main_entity, slugs=ds_slugs)

            for ds_recipient in ds_recipients:
                create_notif(ds_recipient, text2)
