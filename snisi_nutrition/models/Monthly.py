#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging

import reversion
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from snisi_core.models.common import (pre_save_report, post_save_report,
                                      create_periodic_agg_report_from)
from snisi_core.models.Reporting import (SNISIReport,
                                         PeriodicAggregatedReportInterface,
                                         PERIODICAL_SOURCE,
                                         PERIODICAL_AGGREGATED)
from snisi_nutrition.models.Common import AbstractURENutritionR
from snisi_nutrition.xls_export import nutrition_monthly_as_xls

logger = logging.getLogger(__name__)


class AbstractNutritionR(SNISIReport):

    class Meta:
        app_label = 'snisi_nutrition'
        abstract = True

    def total_for(self, field):
        return sum([
            getattr(report, 'total_for', lambda x: 0)(field)
            for report in (self.urenam_report,
                           self.urenas_report,
                           self.ureni_report)
            ])

    def sam_total_for(self, field):
        return sum([
            getattr(report, 'total_for', lambda x: 0)(field)
            for report in (self.urenas_report,
                           self.ureni_report)
            ])

    def sam_total_for_age(self, age, field):
        return sum([
            getattr(report, '{}_{}'.format(age, field), 0)
            for report in (self.urenas_report,
                           self.ureni_report)
            ])

    def mam_total_for(self, field):
        return getattr(self.urenam_report, 'total_for', lambda x: 0)(field)

    def sam_comp_total_for(self, field):
        return sum([
            getattr(report, 'comp_total_for', lambda x: 0)(field)
            for report in (self.urenas_report,
                           self.ureni_report)
            ])

    def mam_comp_total_for(self, field):
        return getattr(self.urenam_report,
                       'comp_total_for', lambda x: 0)(field)

    @classmethod
    def all_uren_fields(cls):
        prefixes = ['', 'mam_', 'sam_', 'mam_comp_', 'sam_comp_',
                    'sam_u6_', 'sam_u59o6_', 'sam_o59_']
        uren_fields = AbstractURENutritionR.uren_fields_with_calc()
        return ["{p}{f}".format(p=prefix, f=field)
                for prefix in prefixes for field in uren_fields]

    @property
    def total_start(self):
        return self.total_for('total_start')

    @property
    def total_start_m(self):
        return self.total_for('total_start_m')

    @property
    def total_start_f(self):
        return self.total_for('total_start_f')

    @property
    def new_cases(self):
        return self.total_for('new_cases')

    @property
    def returned(self):
        return self.total_for('returned')

    @property
    def total_in_m(self):
        return self.total_for('total_in_m')

    @property
    def total_in_f(self):
        return self.total_for('total_in_f')

    @property
    def transferred(self):
        return self.total_for('transferred')

    @property
    def grand_total_in(self):
        return self.total_for('grand_total_in')

    @property
    def healed(self):
        return self.total_for('healed')

    @property
    def deceased(self):
        return self.total_for('deceased')

    @property
    def abandon(self):
        return self.total_for('abandon')

    @property
    def not_responding(self):
        return self.total_for('not_responding')

    @property
    def total_out(self):
        return self.total_for('total_out')

    @property
    def total_out_m(self):
        return self.total_for('total_out_m')

    @property
    def total_out_f(self):
        return self.total_for('total_out_f')

    @property
    def referred(self):
        return self.total_for('referred')

    @property
    def grand_total_out(self):
        return self.total_for('grand_total_out')

    @property
    def total_end(self):
        return self.total_for('total_end')

    @property
    def total_end_m(self):
        return self.total_for('total_end_m')

    @property
    def total_end_f(self):
        return self.total_for('total_end_f')

    # MAM only
    @property
    def mam_total_start(self):
        return self.mam_total_for('total_start')

    @property
    def mam_total_start_m(self):
        return self.mam_total_for('total_start_m')

    @property
    def mam_total_start_f(self):
        return self.mam_total_for('total_start_f')

    @property
    def mam_new_cases(self):
        return self.mam_total_for('new_cases')

    @property
    def mam_returned(self):
        return self.mam_total_for('returned')

    @property
    def mam_total_in_m(self):
        return self.mam_total_for('total_in_m')

    @property
    def mam_total_in_f(self):
        return self.mam_total_for('total_in_f')

    @property
    def mam_transferred(self):
        return self.mam_total_for('transferred')

    @property
    def mam_grand_total_in(self):
        return self.mam_total_for('grand_total_in')

    @property
    def mam_healed(self):
        return self.mam_total_for('healed')

    @property
    def mam_deceased(self):
        return self.mam_total_for('deceased')

    @property
    def mam_abandon(self):
        return self.mam_total_for('abandon')

    @property
    def mam_not_responding(self):
        return self.mam_total_for('not_responding')

    @property
    def mam_total_out(self):
        return self.mam_total_for('total_out')

    @property
    def mam_total_out_m(self):
        return self.mam_total_for('total_out_m')

    @property
    def mam_total_out_f(self):
        return self.mam_total_for('total_out_f')

    @property
    def mam_referred(self):
        return self.mam_total_for('referred')

    @property
    def mam_grand_total_out(self):
        return self.mam_total_for('grand_total_out')

    @property
    def mam_total_end(self):
        return self.mam_total_for('total_end')

    @property
    def mam_total_end_m(self):
        return self.mam_total_for('total_end_m')

    @property
    def mam_total_end_f(self):
        return self.mam_total_for('total_end_f')

    # SAM only (SAM/SAM+)
    @property
    def sam_total_start(self):
        return self.sam_total_for('total_start')

    @property
    def sam_total_start_m(self):
        return self.sam_total_for('total_start_m')

    @property
    def sam_total_start_f(self):
        return self.sam_total_for('total_start_f')

    @property
    def sam_new_cases(self):
        return self.sam_total_for('new_cases')

    @property
    def sam_returned(self):
        return self.sam_total_for('returned')

    @property
    def sam_total_in_m(self):
        return self.sam_total_for('total_in_m')

    @property
    def sam_total_in_f(self):
        return self.sam_total_for('total_in_f')

    @property
    def sam_total_in(self):
        return self.sam_total_for('total_in')

    @property
    def sam_transferred(self):
        return self.sam_total_for('transferred')

    @property
    def sam_grand_total_in(self):
        return self.sam_total_for('grand_total_in')

    @property
    def sam_healed(self):
        return self.sam_total_for('healed')

    @property
    def sam_deceased(self):
        return self.sam_total_for('deceased')

    @property
    def sam_abandon(self):
        return self.sam_total_for('abandon')

    @property
    def sam_not_responding(self):
        return self.sam_total_for('not_responding')

    @property
    def sam_total_out(self):
        return self.sam_total_for('total_out')

    @property
    def sam_total_out_m(self):
        return self.sam_total_for('total_out_m')

    @property
    def sam_total_out_f(self):
        return self.sam_total_for('total_out_f')

    @property
    def sam_referred(self):
        return self.sam_total_for('referred')

    @property
    def sam_grand_total_out(self):
        return self.sam_total_for('grand_total_out')

    @property
    def sam_total_end(self):
        return self.sam_total_for('total_end')

    @property
    def sam_total_end_m(self):
        return self.sam_total_for('total_end_m')

    @property
    def sam_total_end_f(self):
        return self.sam_total_for('total_end_f')

    @property
    def sam_healed_rate(self):
        return self.performance_indicator_for('sam_', 'healed')

    @property
    def sam_deceased_rate(self):
        return self.performance_indicator_for('sam_', 'deceased')

    @property
    def sam_abandon_rate(self):
        return self.performance_indicator_for('sam_', 'abandon')

    # COMPARATIVE VALUES
    # MAM only
    @property
    def mam_comp_total_start(self):
        return self.mam_comp_total_for('total_start')

    @property
    def mam_comp_total_start_m(self):
        return self.mam_comp_total_for('total_start_m')

    @property
    def mam_comp_total_start_f(self):
        return self.mam_comp_total_for('total_start_f')

    @property
    def mam_comp_new_cases(self):
        return self.mam_comp_total_for('new_cases')

    @property
    def mam_comp_returned(self):
        return self.mam_comp_total_for('returned')

    @property
    def mam_comp_total_in_m(self):
        return self.mam_comp_total_for('total_in_m')

    @property
    def mam_comp_total_in_f(self):
        return self.mam_comp_total_for('total_in_f')

    @property
    def mam_comp_transferred(self):
        return self.mam_comp_total_for('transferred')

    @property
    def mam_comp_grand_total_in(self):
        return self.mam_comp_total_for('grand_total_in')

    @property
    def mam_comp_healed(self):
        return self.mam_comp_total_for('healed')

    @property
    def mam_comp_deceased(self):
        return self.mam_comp_total_for('deceased')

    @property
    def mam_comp_abandon(self):
        return self.mam_comp_total_for('abandon')

    @property
    def mam_comp_not_responding(self):
        return self.mam_comp_total_for('not_responding')

    @property
    def mam_comp_total_out(self):
        return self.mam_comp_total_for('total_out')

    @property
    def mam_comp_total_out_m(self):
        return self.mam_comp_total_for('total_out_m')

    @property
    def mam_comp_total_out_f(self):
        return self.mam_comp_total_for('total_out_f')

    @property
    def mam_comp_referred(self):
        return self.mam_comp_total_for('referred')

    @property
    def mam_comp_grand_total_out(self):
        return self.mam_comp_total_for('grand_total_out')

    @property
    def mam_comp_total_end(self):
        return self.mam_comp_total_for('total_end')

    @property
    def mam_comp_total_end_m(self):
        return self.mam_comp_total_for('total_end_m')

    @property
    def mam_comp_total_end_f(self):
        return self.mam_comp_total_for('total_end_f')

    @property
    def mam_comp_out_base(self):
        return self.total_performance_for('mam_comp_')

    @property
    def mam_comp_healed_rate(self):
        return self.performance_indicator_for('mam_comp_', 'healed')

    @property
    def mam_comp_deceased_rate(self):
        return self.performance_indicator_for('mam_comp_', 'deceased')

    @property
    def mam_comp_abandon_rate(self):
        return self.performance_indicator_for('mam_comp_', 'abandon')

    # SAM only (SAM/SAM+)
    @property
    def sam_comp_total_start(self):
        return self.sam_comp_total_for('total_start')

    @property
    def sam_comp_total_start_m(self):
        return self.sam_comp_total_for('total_start_m')

    @property
    def sam_comp_total_start_f(self):
        return self.sam_comp_total_for('total_start_f')

    @property
    def sam_comp_new_cases(self):
        return self.sam_comp_total_for('new_cases')

    @property
    def sam_comp_returned(self):
        return self.sam_comp_total_for('returned')

    @property
    def sam_comp_total_in_m(self):
        return self.sam_comp_total_for('total_in_m')

    @property
    def sam_comp_total_in_f(self):
        return self.sam_comp_total_for('total_in_f')

    @property
    def sam_comp_transferred(self):
        return self.sam_comp_total_for('transferred')

    @property
    def sam_comp_grand_total_in(self):
        return self.sam_comp_total_for('grand_total_in')

    @property
    def sam_comp_healed(self):
        return self.sam_comp_total_for('healed')

    @property
    def sam_comp_deceased(self):
        return self.sam_comp_total_for('deceased')

    @property
    def sam_comp_abandon(self):
        return self.sam_comp_total_for('abandon')

    @property
    def sam_comp_not_responding(self):
        return self.sam_comp_total_for('not_responding')

    @property
    def sam_comp_total_out(self):
        return self.sam_comp_total_for('total_out')

    @property
    def sam_comp_total_out_m(self):
        return self.sam_comp_total_for('total_out_m')

    @property
    def sam_comp_total_out_f(self):
        return self.sam_comp_total_for('total_out_f')

    @property
    def sam_comp_referred(self):
        return self.sam_comp_total_for('referred')

    @property
    def sam_comp_grand_total_out(self):
        return self.sam_comp_total_for('grand_total_out')

    @property
    def sam_comp_total_end(self):
        return self.sam_comp_total_for('total_end')

    @property
    def sam_comp_total_end_m(self):
        return self.sam_comp_total_for('total_end_m')

    @property
    def sam_comp_total_end_f(self):
        return self.sam_comp_total_for('total_end_f')

    @property
    def sam_comp_healed_rate(self):
        return self.performance_indicator_for('sam_comp_', 'healed')

    @property
    def sam_comp_deceased_rate(self):
        return self.performance_indicator_for('sam_comp_', 'deceased')

    @property
    def sam_comp_abandon_rate(self):
        return self.performance_indicator_for('sam_comp_', 'abandon')

    @property
    def sam_comp_out_base(self):
        return self.total_performance_for('sam_comp_')

    # SAM WITH AGES (SAM/SAM+)
    @property
    def sam_u6_total_start(self):
        return self.sam_total_for_age('u6', 'total_start')

    @property
    def sam_u6_total_start_m(self):
        return self.sam_total_for_age('u6', 'total_start_m')

    @property
    def sam_u6_total_start_f(self):
        return self.sam_total_for_age('u6', 'total_start_f')

    @property
    def sam_u6_new_cases(self):
        return self.sam_total_for_age('u6', 'new_cases')

    @property
    def sam_u6_returned(self):
        return self.sam_total_for_age('u6', 'returned')

    @property
    def sam_u6_total_in_m(self):
        return self.sam_total_for_age('u6', 'total_in_m')

    @property
    def sam_u6_total_in_f(self):
        return self.sam_total_for_age('u6', 'total_in_f')

    @property
    def sam_u6_total_in(self):
        return self.sam_total_for_age('u6', 'total_in')

    @property
    def sam_u6_transferred(self):
        return self.sam_total_for_age('u6', 'transferred')

    @property
    def sam_u6_grand_total_in(self):
        return self.sam_total_for_age('u6', 'grand_total_in')

    @property
    def sam_u6_healed(self):
        return self.sam_total_for_age('u6', 'healed')

    @property
    def sam_u6_deceased(self):
        return self.sam_total_for_age('u6', 'deceased')

    @property
    def sam_u6_abandon(self):
        return self.sam_total_for_age('u6', 'abandon')

    @property
    def sam_u6_not_responding(self):
        return self.sam_total_for_age('u6', 'not_responding')

    @property
    def sam_u6_total_out(self):
        return self.sam_total_for_age('u6', 'total_out')

    @property
    def sam_u6_total_out_m(self):
        return self.sam_total_for_age('u6', 'total_out_m')

    @property
    def sam_u6_total_out_f(self):
        return self.sam_total_for_age('u6', 'total_out_f')

    @property
    def sam_u6_referred(self):
        return self.sam_total_for_age('u6', 'referred')

    @property
    def sam_u6_grand_total_out(self):
        return self.sam_total_for_age('u6', 'grand_total_out')

    @property
    def sam_u6_total_end(self):
        return self.sam_total_for_age('u6', 'total_end')

    @property
    def sam_u6_total_end_m(self):
        return self.sam_total_for_age('u6', 'total_end_m')

    @property
    def sam_u6_total_end_f(self):
        return self.sam_total_for_age('u6', 'total_end_f')

    @property
    def sam_u6_healed_rate(self):
        return self.performance_indicator_for('sam_u6_', 'healed')

    @property
    def sam_u6_deceased_rate(self):
        return self.performance_indicator_for('sam_u6_', 'deceased')

    @property
    def sam_u6_abandon_rate(self):
        return self.performance_indicator_for('sam_u6_', 'abandon')

    # SAM AGE 2
    @property
    def sam_u59o6_total_start(self):
        return self.sam_total_for_age('u59o6', 'total_start')

    @property
    def sam_u59o6_total_start_m(self):
        return self.sam_total_for_age('u59o6', 'total_start_m')

    @property
    def sam_u59o6_total_start_f(self):
        return self.sam_total_for_age('u59o6', 'total_start_f')

    @property
    def sam_u59o6_new_cases(self):
        return self.sam_total_for_age('u59o6', 'new_cases')

    @property
    def sam_u59o6_returned(self):
        return self.sam_total_for_age('u59o6', 'returned')

    @property
    def sam_u59o6_total_in_m(self):
        return self.sam_total_for_age('u59o6', 'total_in_m')

    @property
    def sam_u59o6_total_in_f(self):
        return self.sam_total_for_age('u59o6', 'total_in_f')

    @property
    def sam_u59o6_total_in(self):
        return self.sam_total_for_age('u59o6', 'total_in')

    @property
    def sam_u59o6_transferred(self):
        return self.sam_total_for_age('u59o6', 'transferred')

    @property
    def sam_u59o6_grand_total_in(self):
        return self.sam_total_for_age('u59o6', 'grand_total_in')

    @property
    def sam_u59o6_healed(self):
        return self.sam_total_for_age('u59o6', 'healed')

    @property
    def sam_u59o6_deceased(self):
        return self.sam_total_for_age('u59o6', 'deceased')

    @property
    def sam_u59o6_abandon(self):
        return self.sam_total_for_age('u59o6', 'abandon')

    @property
    def sam_u59o6_not_responding(self):
        return self.sam_total_for_age('u59o6', 'not_responding')

    @property
    def sam_u59o6_total_out(self):
        return self.sam_total_for_age('u59o6', 'total_out')

    @property
    def sam_u59o6_total_out_m(self):
        return self.sam_total_for_age('u59o6', 'total_out_m')

    @property
    def sam_u59o6_total_out_f(self):
        return self.sam_total_for_age('u59o6', 'total_out_f')

    @property
    def sam_u59o6_referred(self):
        return self.sam_total_for_age('u59o6', 'referred')

    @property
    def sam_u59o6_grand_total_out(self):
        return self.sam_total_for_age('u59o6', 'grand_total_out')

    @property
    def sam_u59o6_total_end(self):
        return self.sam_total_for_age('u59o6', 'total_end')

    @property
    def sam_u59o6_total_end_m(self):
        return self.sam_total_for_age('u59o6', 'total_end_m')

    @property
    def sam_u59o6_total_end_f(self):
        return self.sam_total_for_age('u59o6', 'total_end_f')

    @property
    def sam_u59o6_healed_rate(self):
        return self.performance_indicator_for('sam_u59o6_', 'healed')

    @property
    def sam_u59o6_deceased_rate(self):
        return self.performance_indicator_for('sam_u59o6_', 'deceased')

    @property
    def sam_u59o6_abandon_rate(self):
        return self.performance_indicator_for('sam_u59o6_', 'abandon')

    # SAM AGE 3
    @property
    def sam_o59_total_start(self):
        return self.sam_total_for_age('o59', 'total_start')

    @property
    def sam_o59_total_start_m(self):
        return self.sam_total_for_age('o59', 'total_start_m')

    @property
    def sam_o59_total_start_f(self):
        return self.sam_total_for_age('o59', 'total_start_f')

    @property
    def sam_o59_new_cases(self):
        return self.sam_total_for_age('o59', 'new_cases')

    @property
    def sam_o59_returned(self):
        return self.sam_total_for_age('o59', 'returned')

    @property
    def sam_o59_total_in_m(self):
        return self.sam_total_for_age('o59', 'total_in_m')

    @property
    def sam_o59_total_in_f(self):
        return self.sam_total_for_age('o59', 'total_in_f')

    @property
    def sam_o59_total_in(self):
        return self.sam_total_for_age('o59', 'total_in')

    @property
    def sam_o59_transferred(self):
        return self.sam_total_for_age('o59', 'transferred')

    @property
    def sam_o59_grand_total_in(self):
        return self.sam_total_for_age('o59', 'grand_total_in')

    @property
    def sam_o59_healed(self):
        return self.sam_total_for_age('o59', 'healed')

    @property
    def sam_o59_deceased(self):
        return self.sam_total_for_age('o59', 'deceased')

    @property
    def sam_o59_abandon(self):
        return self.sam_total_for_age('o59', 'abandon')

    @property
    def sam_o59_not_responding(self):
        return self.sam_total_for_age('o59', 'not_responding')

    @property
    def sam_o59_total_out(self):
        return self.sam_total_for_age('o59', 'total_out')

    @property
    def sam_o59_grand_total_out(self):
        return self.sam_total_for_age('o59', 'grand_total_out')

    @property
    def sam_o59_total_end(self):
        return self.sam_total_for_age('o59', 'total_end')

    @property
    def sam_o59_healed_rate(self):
        return self.performance_indicator_for('sam_o59_', 'healed')

    @property
    def sam_o59_deceased_rate(self):
        return self.performance_indicator_for('sam_o59_', 'deceased')

    @property
    def sam_o59_abandon_rate(self):
        return self.performance_indicator_for('sam_o59_', 'abandon')

    ####

    @property
    def total_out_resp(self):
        return self.total_out - self.not_responding

    @property
    def healed_rate(self):
        try:
            return self.healed / self.total_out_resp
        except ZeroDivisionError:
            return 0

    @property
    def deceased_rate(self):
        try:
            return self.deceased / self.total_out_resp
        except ZeroDivisionError:
            return 0

    @property
    def abandon_rate(self):
        try:
            return self.abandon / self.total_out_resp
        except ZeroDivisionError:
            return 0

    # sum of out reasons except not resp.
    def total_performance_for(self, prefix):
        tof = '{}total_out'.format(prefix) \
            if prefix is not None else 'total_out'
        nof = '{}not_responding'.format(prefix) \
            if prefix is not None else 'not_responding'
        return getattr(self, tof, 0) - getattr(self, nof, 0)

    # rate of indicator (healed, deceased, abandon)
    def performance_indicator_for(self, prefix, field):
        f = '{}{}'.format(prefix, field) \
            if prefix != 'all' else '{}'.format(field)
        try:
            return getattr(self, f) / self.total_performance_for(prefix)
        except ZeroDivisionError:
            return 0

    def as_xls(self):
        file_name = "NUT_{entity}.{month}.{year}.xls" \
                    .format(entity=self.entity.slug,
                            month=self.period.middle().month,
                            year=self.period.middle().year)
        return file_name, nutrition_monthly_as_xls(self)


class NutritionR(AbstractNutritionR):

    REPORTING_TYPE = PERIODICAL_SOURCE
    RECEIPT_FORMAT = "{period}-NUT/{entity__slug}-{rand}"
    UNIQUE_TOGETHER = [('period', 'entity')]

    class Meta:
        app_label = 'snisi_nutrition'
        verbose_name = _("Nutrition Report")
        verbose_name_plural = _("Nutrition Reports")

    urenam_report = models.ForeignKey(
        'URENAMNutritionR', null=True, blank=True, related_name='nutritionr')
    urenas_report = models.ForeignKey(
        'URENASNutritionR', null=True, blank=True, related_name='nutritionr')
    ureni_report = models.ForeignKey(
        'URENINutritionR', null=True, blank=True, related_name='nutritionr')
    stocks_report = models.ForeignKey(
        'NutritionStocksR', null=True, blank=True, related_name='nutritionr')


receiver(pre_save, sender=NutritionR)(pre_save_report)
receiver(post_save, sender=NutritionR)(post_save_report)

reversion.register(NutritionR)


class AggNutritionR(AbstractNutritionR,
                    PeriodicAggregatedReportInterface, SNISIReport):

    REPORTING_TYPE = PERIODICAL_AGGREGATED
    RECEIPT_FORMAT = "{period}-NUTa/{entity__slug}-{rand}"
    INDIVIDUAL_CLS = NutritionR
    UNIQUE_TOGETHER = [('period', 'entity')]

    class Meta:
        app_label = 'snisi_nutrition'
        verbose_name = _("Aggregated Nutrition Report")
        verbose_name_plural = _("Aggregated Nutrition Reports")

    urenam_report = models.ForeignKey(
        'AggURENAMNutritionR', null=True, blank=True,
        related_name='agg_nutritionr')
    urenas_report = models.ForeignKey(
        'AggURENASNutritionR', null=True, blank=True,
        related_name='agg_nutritionr')
    ureni_report = models.ForeignKey(
        'AggURENINutritionR', null=True, blank=True,
        related_name='agg_nutritionr')
    stocks_report = models.ForeignKey(
        'AggNutritionStocksR', null=True, blank=True,
        related_name='agg_nutritionr')

    indiv_sources = models.ManyToManyField(
        INDIVIDUAL_CLS,
        verbose_name=_(u"Primary. Sources"),
        blank=True, null=True,
        related_name='source_agg_%(class)s_reports')

    direct_indiv_sources = models.ManyToManyField(
        INDIVIDUAL_CLS,
        verbose_name=_("Primary. Sources (direct)"),
        blank=True, null=True,
        related_name='direct_source_agg_%(class)s_reports')

    def fill_blank(self):
        # no fields to set data on
        return

    @classmethod
    def update_instance_with_indiv(cls, report, instance):
        # no data update
        pass

    @classmethod
    def update_instance_with_agg(cls, report, instance):
        # no data update
        pass

    @classmethod
    def create_from(cls, period, entity, created_by,
                    indiv_sources=None, agg_sources=None):
        # AggNutritionR is specific in that it only holds UREN/STOCKS reports
        # for an entity/period and does not carry data.

        if indiv_sources is None:
            if entity.type.slug in ('health_center', 'health_district'):
                indiv_sources = cls.INDIVIDUAL_CLS.objects.filter(
                    period__start_on__gte=period.start_on,
                    period__end_on__lte=period.end_on) \
                    .filter(entity__in=entity.get_health_centers())
            else:
                indiv_sources = []

        if agg_sources is None and not len(indiv_sources):
            agg_sources = cls.objects.filter(
                period__start_on__gte=period.start_on,
                period__end_on__lte=period.end_on) \
                .filter(entity__in=entity.get_natural_children(
                    skip_slugs=['health_area']))

        from snisi_nutrition.models.URENAM import AggURENAMNutritionR
        from snisi_nutrition.models.URENAS import AggURENASNutritionR
        from snisi_nutrition.models.URENI import AggURENINutritionR
        from snisi_nutrition.models.Stocks import AggNutritionStocksR

        def gr(cls):
            try:
                return cls.objects.get(period=period, entity=entity)
            except:
                return None

        stocks_report = gr(AggNutritionStocksR)
        tocopy_fields = ['created_by', 'created_on',
                         'completion_status', 'completed_on',
                         'integrity_status', 'arrival_status',
                         'validation_status', 'validated_on',
                         'validated_by', 'auto_validated']

        # create blank report with data from stock report
        report = create_periodic_agg_report_from(
            cls, period=period, entity=entity,
            created_by=created_by, indiv_cls=cls.INDIVIDUAL_CLS,
            indiv_sources=indiv_sources,
            agg_sources=agg_sources)

        # copy status fields from stocks
        for field in tocopy_fields:
            setattr(report, field, getattr(stocks_report, field))

        if getattr(entity, 'has_urenam', False):
            report.urenam_report = gr(AggURENAMNutritionR)
        if getattr(entity, 'has_urenas', False):
            report.urenas_report = gr(AggURENASNutritionR)
        if getattr(entity, 'has_ureni', False):
            report.ureni_report = gr(AggURENINutritionR)
        report.stocks_report = stocks_report

        with reversion.create_revision():
            report.save()
            reversion.set_user(created_by)

        return report

    # @classmethod
    # def start_aggregated(cls, *args, **kwargs):
    #     rfdict = {}
    #     for field in ('completion_ok', 'integrity_ok',
    #                   'arrival_ok', 'auto_validate'):
    #         if field in kwargs:
    #             rfdict.update({field: kwargs.get(field)})
    #             del kwargs[field]
    #     report = cls.start_report(*args, **kwargs)
    #     report.fill_blank()

    #     # only agg
    #     if hasattr(report, 'set_reporting_status_fields'):
    #         report.set_reporting_status_fields(**rfdict)
    #     if hasattr(report, 'update_expected_reportings_number'):
    #         report.update_expected_reportings_number()
    #     return report


receiver(pre_save, sender=AggNutritionR)(pre_save_report)
receiver(post_save, sender=AggNutritionR)(post_save_report)

reversion.register(AggNutritionR)
