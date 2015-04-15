#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging
from collections import OrderedDict

import reversion
from django.utils import timezone
from django.forms.models import modelform_factory

from snisi_core.models.Reporting import PERIODICAL_AGGREGATED
from snisi_web.views.validation import (
    handle_report_edition as original_handle_report_edition,
    handle_do_validation)
from snisi_nutrition.forms import NutritionRForm, AggNutritionRForm
from snisi_core.models.Entities import Entity
from snisi_nutrition.integrity import (
    NutritionRIntegrityChecker,
    URENAMNutritionRIntegrityChecker,
    URENASNutritionRIntegrityChecker,
    URENINutritionRIntegrityChecker,
    StocksNutritionRIntegrityChecker)
from snisi_nutrition.models.Monthly import NutritionR, AggNutritionR
from snisi_nutrition.models.URENAM import AbstractURENAMNutritionR
from snisi_nutrition.models.URENAS import AbstractURENASNutritionR
from snisi_nutrition.models.URENI import AbstractURENINutritionR
from snisi_nutrition.models.Stocks import AbstractNutritionStocksR

logger = logging.getLogger(__name__)


def get_form_class_for(rcls):
    if rcls == NutritionR:
        return NutritionRForm
    elif rcls == AggNutritionR:
        return AggNutritionRForm
    return modelform_factory(model=rcls, fields=rcls.data_fields())


def handle_report_edition(report, form, provider):

    if not isinstance(report.casted(), (NutritionR, AggNutritionR)):
        return original_handle_report_edition(report, form, provider)

    # now we have well formed and authenticated data.
    # let's check for business-logic errors.
    checker = NutritionRIntegrityChecker()

    # feed checker with meta-data
    entity = Entity.get_or_none(report.entity.slug)
    checker.set('entity', entity)
    checker.set('period', report.period)
    checker.set('submitter', provider)

    # ensure we have a expecteds and all
    checker.check(is_edition=True)

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

    master_fields = ['entity', 'period', 'submitter']

    for sr, sr_data in integrity_map.items():
        sr_rcls, sr_cls = sr_data
        if sr == 'stocks' or (getattr(entity, 'has_{}'.format(sr), False)
                              or report.casted().REPORTING_TYPE ==
                              PERIODICAL_AGGREGATED):
            logger.debug("checking {}".format(sr))

            sri = sr_cls()

            # feed checker with meta-data
            for field in master_fields:
                sri.set(field, checker.get(field))

            # feed checker with UREN data
            for field in sr_rcls.data_fields():
                sri.set(field,
                        form.cleaned_data.get('{}_{}'.format(sr, field)))

            sri.check(is_edition=True)
            if not sri.is_valid():
                for feedback in sri.feedbacks:
                    should_raise = sri.raised == feedback
                    checker.add_feedback(feedback, should_raise)
            else:
                sr_checkers[sr] = sri

    # checker now includes sub-reports errors
    if not checker.is_valid():
        return checker, None

    # all sub reports have been checked. we can safely create reports
    logger.debug("ALL UREN AND STOCKS CHECKS PERFORMED. CREATING REPORT")

    # now all reports data are OK. let's actually update reports

    modified_on = timezone.now()

    for sr, sr_data in integrity_map.items():
        sr_rcls, sr_cls = sr_data
        ureport = getattr(report, '{}_report'.format(sr))

        # skip is there's no UREN report
        if ureport is None:
            continue

        # update all values from checker
        checker = sr_checkers[sr]
        for field in sr_rcls.data_fields():
            setattr(ureport, field, checker.get(field))

        # meta-data
        ureport.modified_by = provider
        ureport.modified_on = modified_on

        # save in DB
        with reversion.create_revision():
            ureport.save()
            reversion.set_user(provider)

    report.modified_by = provider
    report.modified_on = modified_on

    # save in DB
    with reversion.create_revision():
        report.save()
        reversion.set_user(provider)

    return checker, report


def do_validation(report, provider):

    # only for month report
    if not isinstance(report.casted(), (AggNutritionR, NutritionR)):
        return handle_do_validation(report, provider)

    def acknowledge(report, validated_on, provider):
        if report is None:
            return
        expected_val = report.expected_validation
        expected_val.acknowledge_validation(
            validated=True,
            validated_by=provider,
            validated_on=validated_on,
            auto_validated=False)

    # mark report as validated
    expected_val = report.expected_validation

    if not expected_val.validation_period.casted().contains(timezone.now()):
        return (False, "Impossible de valider ce rapport en dehors "
                       "de la période de validation ({})"
                       .format(expected_val.validation_period))
    else:
        validated_on = timezone.now()

        acknowledge(report.urenam_report, validated_on, provider)
        acknowledge(report.urenas_report, validated_on, provider)
        acknowledge(report.ureni_report, validated_on, provider)
        acknowledge(report.stocks_report, validated_on, provider)

        expected_val.acknowledge_validation(
            validated=True,
            validated_by=provider,
            validated_on=validated_on,
            auto_validated=False)

        # confirm validation
        return (True, "Le rapport {cls} nº {receipt} pour {period} "
                      "a été validé par {by}"
                      .format(cls=report.report_class(),
                              receipt=report.receipt,
                              period=report.period,
                              by=report.validated_by))
