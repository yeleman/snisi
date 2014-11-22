#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging
from collections import OrderedDict

from django.utils import timezone

from snisi_nutrition.forms import NutritionRForm
from snisi_core.models.Reporting import ExpectedReporting, ReportClass
from snisi_nutrition.integrity import (
    NutritionRIntegrityChecker,
    create_nut_report,
    URENAMNutritionRIntegrityChecker,
    URENASNutritionRIntegrityChecker,
    URENINutritionRIntegrityChecker,
    StocksNutritionRIntegrityChecker)
from snisi_nutrition.models.URENAM import AbstractURENAMNutritionR
from snisi_nutrition.models.URENAS import AbstractURENASNutritionR
from snisi_nutrition.models.URENI import AbstractURENINutritionR
from snisi_nutrition.models.Stocks import AbstractNutritionStocksR

reportcls_nut = ReportClass.get_or_none(slug='nutrition_monthly_routine')

logger = logging.getLogger(__name__)


def get_form_class_for(rcls):
    return NutritionRForm


def handle_report_upload(excel_form, form, provider):

    excel_form.set('submit_time', timezone.now())
    excel_form.set('submitter', provider)

    # ensure we have a expecteds and all
    excel_form.check()
    if not excel_form.is_valid():
        return None, excel_form.errors.pop().render(short=True)

    # build requirements for report
    entity = excel_form.get('entity')
    period = excel_form.get('period')

    # expected reporting defines if report is expeted or not
    expected_reporting = ExpectedReporting.get_or_none(
        report_class=reportcls_nut,
        period=period,
        within_period=False,
        entity=entity,
        within_entity=False,
        amount_expected=ExpectedReporting.EXPECTED_SINGLE)

    # should have already been checked in excel_form.
    if expected_reporting is None:
        logger.error("Expected reporting not found: "
                     "cls:{cls} - period:{period} - entity:{entity}"
                     .format(cls=reportcls_nut, period=period, entity=entity))
        return None, ("Aucun rapport de routine attendu à "
                      "{entity} pour {period}"
                      .format(entity=entity, period=period))

    # def prepare_checker_with(master_checker, uren_checker, uren):

    #     master_fields = ['entity', 'submit_time', 'submitter']

    #     for field in master_fields:
    #         uren_checker.set(field, excel_form.get(field))

    #     # feed data holder with sms provided data
    #     for key, value in master_checker.to_dict().items():
    #         if not key.startswith(uren):
    #             continue
    #         uren_checker.set(key.replace(uren, ''), value)

    #     # check data
    #     uren_checker.check(has_ureni=entity.has_ureni)

    #     if not uren_checker.is_valid():
    #         return uren_checker.errors.pop().render(short=True)

    # # check data individually for sub reports
    # integrity_map = OrderedDict([
    #     ('urenam', URENAMNutritionRIntegrityChecker),
    #     ('urenas', URENASNutritionRIntegrityChecker),
    #     ('ureni', URENINutritionRIntegrityChecker),
    #     ('stocks', StocksNutritionRIntegrityChecker),
    # ])

    # sr_checkers = {}
    # for sr, sr_cls in integrity_map.items():
    #     if sr == 'stocks' or getattr(entity, 'has_{}'.format(sr), False):
    #         logger.debug("checking {}".format(sr))
    #         sri = sr_cls()
    #         prepare_checker_with(master_checker=excel_form,
    #                              uren_checker=sri, uren=sr)
    #         # if error is not None:
    #         #     return None, error
    #         if not sri.is_valid():
    #             for feedback in sri.feedbacks:
    #                 should_raise = sri.raised == feedback
    #                 excel_form.add_feedback(feedback, False)
    #         else:
    #             sr_checkers[sr] = sri

    # if not excel_form.is_valid():
    #     return None, None

    # check data individually for sub reports
    integrity_map = OrderedDict([
        ('urenam', (AbstractURENAMNutritionR,
                    URENAMNutritionRIntegrityChecker)),
        ('urenas', (AbstractURENASNutritionR,
                    URENASNutritionRIntegrityChecker)),
        ('ureni', (AbstractURENINutritionR,
                   URENINutritionRIntegrityChecker)),
        ('stocks', (AbstractNutritionStocksR,
                    StocksNutritionRIntegrityChecker)),
    ])

    sr_checkers = {}

    master_fields = ['entity', 'period', 'submitter', 'submit_time']

    for sr, sr_data in integrity_map.items():
        sr_rcls, sr_cls = sr_data
        if sr == 'stocks' or getattr(entity, 'has_{}'.format(sr), False):
            logger.debug("checking {}".format(sr))

            sri = sr_cls()

            # feed checker with meta-data
            for field in master_fields:
                sri.set(field, excel_form.get(field))

            # feed checker with UREN data
            for field in sr_rcls.data_fields():
                sri.set(field,
                        excel_form.get('{}_{}'.format(sr, field)))

            sri.check()
            if not sri.is_valid():
                for feedback in sri.feedbacks:
                    # should_raise = sri.raised == feedback
                    excel_form.add_feedback(feedback, False)
            else:
                sr_checkers[sr] = sri

    # checker now includes sub-reports errors
    if not excel_form.is_valid():
        return None, None

    # all sub reports have been checked. we can safely create reports
    logger.debug("[UPLOAD] ALL UREN+STOCKS CHECKS PERFORMED. CREATING REPORT")

    return create_nut_report(
        provider=provider,
        expected_reporting=expected_reporting,
        completed_on=timezone.now(),
        integrity_checker=excel_form,
        data_source=excel_form,
        subreport_checkers=sr_checkers)
