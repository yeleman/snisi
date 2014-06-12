#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

import reversion
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from django.utils.translation import ugettext_lazy as _, ugettext

from snisi_core.models.common import pre_save_report, post_save_report
from snisi_core.models.Reporting import (SNISIReport,
                                         PeriodicAggregatedReportInterface,
                                         PERIODICAL_SOURCE, PERIODICAL_AGGREGATED)
from snisi_reprohealth.xls_export import pfa_activities_as_xls

class PFActivitiesRIface(models.Model):

    class Meta:
        abstract = True

    LABELS = {
        'intrauterine_devices': _("IUD"),
        'implants': _("Implants"),
        'injections': _("Injections"),
        'pills': _("Pills"),
        'male_condoms': _("Male condoms"),
        'female_condoms': _("Female condoms"),
        'hiv_tests': _("HIV Tests"),
        'iud_removal': _("IUD removals"),
        'implant_removal': _("Implant removals"),
        'tubal_ligations': _("Tubal ligation"),
        'emergency_controls': _("Emergency controls"),
        'new_clients': _("New clients"),
        'previous_clients': _("Previous clients"),
        'under25_visits': _("-25 visits"),
        'over25_visits': _("25+ visits"),
        'very_first_visits': _("First Visits"),
        'short_term_method_visits': _("Short-term method visits"),
        'long_term_method_visits': _("Long-term method visits"),
        'hiv_counseling_clients': _("HIV Counseiling"),
        'hiv_positive_results': _("HIV+ results"),
        'pregnancy_tests': _("Pregnancy Tests"),
    }

    # CAP-providing services
    tubal_ligations = models.PositiveIntegerField(
        verbose_name=_("Tubal Ligations"))
    intrauterine_devices = models.PositiveIntegerField(
        verbose_name=_("IUD"))
    injections = models.PositiveIntegerField(
        verbose_name=_("Injections"))
    pills = models.PositiveIntegerField(
        verbose_name=_("Pills"))
    male_condoms = models.PositiveIntegerField(
        verbose_name=_("Male condoms"))
    female_condoms = models.PositiveIntegerField(
        verbose_name=_("Female condoms"))
    emergency_controls = models.PositiveIntegerField(
        verbose_name=_("Emergency controls"))
    implants = models.PositiveIntegerField(
        verbose_name=_("Implants"))

    # Clients related services
    new_clients = models.PositiveIntegerField(
        verbose_name=_("New Clients"))
    previous_clients = models.PositiveIntegerField(
        verbose_name=_("Previous Clients"))
    under25_visits = models.PositiveIntegerField(
        verbose_name=_("Visits from under 25yo."))
    over25_visits = models.PositiveIntegerField(
        verbose_name=_("Visits from over 25yo."))
    very_first_visits = models.PositiveIntegerField(
        verbose_name=_("Clients visiting for the first time."))
    short_term_method_visits = models.PositiveIntegerField(
        verbose_name=_("Short-term methods related visits"))
    long_term_method_visits = models.PositiveIntegerField(
        verbose_name=_("Long-term methods related visits"))
    hiv_counseling_clients = models.PositiveIntegerField(
        verbose_name=_("HIV Counseiling"))
    hiv_tests = models.PositiveIntegerField(
        verbose_name=_("HIV Tests"))
    hiv_positive_results = models.PositiveIntegerField(
        verbose_name=_("HIV+ results"))

    # non-CAP providing services
    implant_removal = models.PositiveIntegerField(
        verbose_name=_("Implant removals"))
    iud_removal = models.PositiveIntegerField(
        verbose_name=_("IUD removals"))

    # Financial Data
    intrauterine_devices_qty = models.PositiveIntegerField(
        verbose_name=_("IUD: Quantity"))
    intrauterine_devices_price = models.PositiveIntegerField(
        verbose_name=_("IUD: Price"))
    intrauterine_devices_revenue = models.PositiveIntegerField(
        verbose_name=_("IUD: Revenue"))

    implants_qty = models.PositiveIntegerField(
        verbose_name=_("Implants: Quantity"))
    implants_price = models.PositiveIntegerField(
        verbose_name=_("Implants: Price"))
    implants_revenue = models.PositiveIntegerField(
        verbose_name=_("Implants: Revenue"))

    injections_qty = models.PositiveIntegerField(
        verbose_name=_("Injections: Quantity"))
    injections_price = models.PositiveIntegerField(
        verbose_name=_("Injections: Price"))
    injections_revenue = models.PositiveIntegerField(
        verbose_name=_("Injections: Revenue"))

    pills_qty = models.PositiveIntegerField(
        verbose_name=_("Pills: Quantity"))
    pills_price = models.PositiveIntegerField(
        verbose_name=_("Pills: Price"))
    pills_revenue = models.PositiveIntegerField(
        verbose_name=_("Pills: Revenue"))

    male_condoms_qty = models.PositiveIntegerField(
        verbose_name=_("Male Condoms: Quantity"))
    male_condoms_price = models.PositiveIntegerField(
        verbose_name=_("Male Condoms: Price"))
    male_condoms_revenue = models.PositiveIntegerField(
        verbose_name=_("Male Condoms: Revenue"))

    female_condoms_qty = models.PositiveIntegerField(
        verbose_name=_("Female Condoms: Quantity"))
    female_condoms_price = models.PositiveIntegerField(
        verbose_name=_("Female Condoms: Price"))
    female_condoms_revenue = models.PositiveIntegerField(
        verbose_name=_("Female Condoms: Revenue"))

    hiv_tests_qty = models.PositiveIntegerField(
        verbose_name=_("HIV Tests: Quantity"))
    hiv_tests_price = models.PositiveIntegerField(
        verbose_name=_("HIV Tests: Price"))
    hiv_tests_revenue = models.PositiveIntegerField(
        verbose_name=_("HIV Tests: Revenue"))

    iud_removal_qty = models.PositiveIntegerField(
        verbose_name=_("IUD Removals: Quantity"))
    iud_removal_price = models.PositiveIntegerField(
        verbose_name=_("IUD Removals: Price"))
    iud_removal_revenue = models.PositiveIntegerField(
        verbose_name=_("IUD Removals: Revenue"))

    implant_removal_qty = models.PositiveIntegerField(
        verbose_name=_("Implants Removals: Quantity"))
    implant_removal_price = models.PositiveIntegerField(
        verbose_name=_("Implants Removals: Price"))
    implant_removal_revenue = models.PositiveIntegerField(
        verbose_name=_("Implants Removals"))

    # stock
    intrauterine_devices_initial = models.PositiveIntegerField(
        verbose_name=_("IUD: Initial Quantity"))
    intrauterine_devices_used = models.PositiveIntegerField(
        verbose_name=_("IUD: Quantity Used"))
    intrauterine_devices_lost = models.PositiveIntegerField(
        verbose_name=_("IUD: Quantity Lost"))
    intrauterine_devices_received = models.PositiveIntegerField(
        verbose_name=_("IUD: Quantity Received"))

    implants_initial = models.PositiveIntegerField(
        verbose_name=_("Implants: Initial Quantity"))
    implants_used = models.PositiveIntegerField(
        verbose_name=_("Implants: Quantity Used"))
    implants_lost = models.PositiveIntegerField(
        verbose_name=_("Implants: Quantity Lost"))
    implants_received = models.PositiveIntegerField(
        verbose_name=_("Implants: Quantity Received"))

    injections_initial = models.PositiveIntegerField(
        verbose_name=_("Injections: Initial Quantity"))
    injections_used = models.PositiveIntegerField(
        verbose_name=_("Injections: Quantity Used"))
    injections_lost = models.PositiveIntegerField(
        verbose_name=_("Injections: Quantity Lost"))
    injections_received = models.PositiveIntegerField(
        verbose_name=_("Injections: Quantity Received"))

    pills_initial = models.PositiveIntegerField(
        verbose_name=_("Pills: Initial Quantity"))
    pills_used = models.PositiveIntegerField(
        verbose_name=_("Pills: Quantity Used"))
    pills_lost = models.PositiveIntegerField(
        verbose_name=_("Pills: Quantity Lost"))
    pills_received = models.PositiveIntegerField(
        verbose_name=_("Pills: Quantity Received"))

    male_condoms_initial = models.PositiveIntegerField(
        verbose_name=_("Male Condoms: Initial Quantity"))
    male_condoms_used = models.PositiveIntegerField(
        verbose_name=_("Male Condoms: Quantity Used"))
    male_condoms_lost = models.PositiveIntegerField(
        verbose_name=_("Male Condoms: Quantity Lost"))
    male_condoms_received = models.PositiveIntegerField(
        verbose_name=_("Male Condoms: Quantity Received"))

    female_condoms_initial = models.PositiveIntegerField(
        verbose_name=_("Female Condoms: Initial Quantity"))
    female_condoms_used = models.PositiveIntegerField(
        verbose_name=_("Female Condoms: Quantity Used"))
    female_condoms_lost = models.PositiveIntegerField(
        verbose_name=_("Female Condoms: Quantity Lost"))
    female_condoms_received = models.PositiveIntegerField(
        verbose_name=_("Female Condoms: Quantity Received"))

    hiv_tests_initial = models.PositiveIntegerField(
        verbose_name=_("HIV Tests: Initial Quantity"))
    hiv_tests_used = models.PositiveIntegerField(
        verbose_name=_("HIV Tests: Quantity Used"))
    hiv_tests_lost = models.PositiveIntegerField(
        verbose_name=_("HIV Tests: Quantity Lost"))
    hiv_tests_received = models.PositiveIntegerField(
        verbose_name=_("HIV Tests: Quantity Received"))
    pregnancy_tests_initial = models.PositiveIntegerField(
        verbose_name=_("Pregnancy Tests: Initial Quantity"))
    pregnancy_tests_used = models.PositiveIntegerField(
        verbose_name=_("Pregnancy Tests: Quantity Used"))
    pregnancy_tests_lost = models.PositiveIntegerField(
        verbose_name=_("Pregnancy Tests: Quantity Lost"))
    pregnancy_tests_received = models.PositiveIntegerField(
        verbose_name=_("Pregnancy Tests: Quantity Received"))

    def fill_blank(self, **kwargs):
        for field in self.data_fields():
            if not field.endswith('_observation'):
                setattr(self, field, 0)

    @classmethod
    def provided_fields(cls, include_subs=True):
        return ['tubal_ligations',
                'intrauterine_devices',
                'injections',
                'pills',
                'male_condoms',
                'female_condoms',
                'emergency_controls',
                'implants',
                'new_clients',
                'previous_clients',
                'under25_visits',
                'over25_visits',
                'very_first_visits',
                'short_term_method_visits',
                'long_term_method_visits',
                'hiv_counseling_clients',
                'hiv_tests',
                'hiv_positive_results',
                'implant_removal',
                'iud_removal']

    @classmethod
    def financial_fields(cls, include_subs=True):
        fields = ['intrauterine_devices',
                  'implants',
                  'injections',
                  'pills',
                  'male_condoms',
                  'female_condoms',
                  'hiv_tests',
                  'iud_removal',
                  'implant_removal']
        if not include_subs:
            return fields

        ff = []
        for field in fields:
            for suffix in ('qty', 'price', 'revenue'):
                ff.append("{}_{}".format(field, suffix))
        return ff

    @classmethod
    def stocks_fields(cls, include_subs=True):
        fields = ['intrauterine_devices',
                  'implants',
                  'injections',
                  'pills',
                  'male_condoms',
                  'female_condoms',
                  'hiv_tests',
                  'pregnancy_tests']
        if not include_subs:
            return fields

        suffixes = ['initial', 'used', 'lost', 'received']
        if cls == PFActivitiesR:
            suffixes.append('observation')

        ff = []
        for field in fields:
            for suffix in suffixes:
                ff.append("{}_{}".format(field, suffix))
        return ff

    @classmethod
    def label_for_field(cls, field):
        return cls.LABEL.get(field)

    def as_xls(self):
        file_name = "MSI_{entity}s.{month}.{year}.xls" \
                    .format(entity=self.entity.slug,
                            month=self.period.middle().month,
                            year=self.period.middle().year)
        return file_name, pfa_activities_as_xls(self)


class PFActivitiesR(PFActivitiesRIface, SNISIReport):

    REPORTING_TYPE = PERIODICAL_SOURCE
    RECEIPT_FORMAT = "MP{id}/{entity__slug}-{day}"
    UNIQUE_TOGETHER = [('period', 'entity')]
    INTEGRITY_CHECKER = 'snisi_reprohealth.integrity.PFActivitiesRIntegrityChecker'

    class Meta:
        app_label = 'snisi_reprohealth'
        verbose_name = _("Provided Services Report")
        verbose_name_plural = _("Provided Services Reports")

    intrauterine_devices_observation = models.CharField(
        max_length=500, null=True, blank=True)

    implants_observation = models.CharField(
        max_length=500, null=True, blank=True)

    injections_observation = models.CharField(
        max_length=500, null=True, blank=True)

    pills_observation = models.CharField(
        max_length=500, null=True, blank=True)

    male_condoms_observation = models.CharField(
        max_length=500, null=True, blank=True)

    female_condoms_observation = models.CharField(
        max_length=500, null=True, blank=True)

    hiv_tests_observation = models.CharField(
        max_length=500, null=True, blank=True)

    pregnancy_tests_observation = models.CharField(
        max_length=500, null=True, blank=True)


receiver(pre_save, sender=PFActivitiesR)(pre_save_report)
receiver(post_save, sender=PFActivitiesR)(post_save_report)

reversion.register(PFActivitiesR, follow=['snisireport_ptr'])


class AggPFActivitiesR(PFActivitiesRIface,
                       PeriodicAggregatedReportInterface, SNISIReport):

    REPORTING_TYPE = PERIODICAL_AGGREGATED
    INDIVIDUAL_CLS = PFActivitiesR
    RECEIPT_FORMAT = "AMP{id}/{entity__slug}-{day}"
    UNIQUE_TOGETHER = [('period', 'entity'),]

    class Meta:
        app_label = 'snisi_reprohealth'
        verbose_name = _("Aggregated Provided Services Report")
        verbose_name_plural = _("Aggregated Provided Services Reports")

    # all source reports (CSCOM)
    indiv_sources = models.ManyToManyField(INDIVIDUAL_CLS,
        verbose_name=_("Primary. Sources (all)"),
        blank=True, null=True,
        related_name='source_agg_%(class)s_reports',
        symmetrical=False)

    direct_indiv_sources = models.ManyToManyField(INDIVIDUAL_CLS,
        verbose_name=_("Primary. Sources (direct)"),
        blank=True, null=True,
        related_name='direct_source_agg_%(class)s_reports',
        symmetrical=False)

receiver(pre_save, sender=AggPFActivitiesR)(pre_save_report)
receiver(post_save, sender=AggPFActivitiesR)(post_save_report)

reversion.register(AggPFActivitiesR, follow=['snisireport_ptr'])
