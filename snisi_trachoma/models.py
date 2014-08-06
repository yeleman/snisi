#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import inspect

import numpy
import reversion
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from snisi_core.models.common import pre_save_report, post_save_report
from snisi_core.models.Providers import Provider
from snisi_core.models.Entities import Entity
from snisi_core.models.Reporting import (SNISIReport,
                                         PeriodicAggregatedReportInterface,
                                         OCCASIONAL_SOURCE,
                                         OCCASIONAL_AGGREGATED)


class TTBacklogVillageR(SNISIReport):

    REPORTING_TYPE = OCCASIONAL_SOURCE
    RECEIPT_FORMAT = "TTV/{id}-{rand}"

    class Meta:
        app_label = 'snisi_trachoma'
        verbose_name = _("TT Backlog Village Report")
        verbose_name_plural = _("TT Backlog Village Reports")

    location = models.ForeignKey(Entity)
    consultation_male = models.PositiveIntegerField(
        verbose_name="Consultations Hommes")
    consultation_female = models.PositiveIntegerField(
        verbose_name="Consultations Femmes")
    surgery_male = models.PositiveIntegerField(
        verbose_name="Chirurgies Hommes")
    surgery_female = models.PositiveIntegerField(
        verbose_name="Chirurgies Femmes")
    refusal_male = models.PositiveIntegerField(
        verbose_name="Refus Hommes")
    refusal_female = models.PositiveIntegerField(
        verbose_name="Refus Femmes")
    recidivism_male = models.PositiveIntegerField(
        verbose_name="Récidives Hommes")
    recidivism_female = models.PositiveIntegerField(
        verbose_name="Récidives Femmes")
    community_assistance = models.BooleanField(
        verbose_name="Assistance relais")
    arrived_on = models.DateField(
        verbose_name="Date d'arrivée")
    left_on = models.DateField(
        verbose_name="Date de départ")

    def visit_duration(self):
        return self.left_on - self.arrived_on

receiver(pre_save, sender=TTBacklogVillageR)(pre_save_report)
receiver(post_save, sender=TTBacklogVillageR)(post_save_report)
reversion.register(TTBacklogVillageR, follow=['snisireport_ptr'])


class TTBacklogMissionR(SNISIReport):

    REPORTING_TYPE = OCCASIONAL_SOURCE
    RECEIPT_FORMAT = "TTM/{id}-{rand}"

    ADVANCED = 'advanced'
    MOBILE = 'mobile'
    FIXED = 'fixed'

    STRATEGIES = {
        FIXED: _("Fixed"),
        MOBILE: _("Mobile"),
        ADVANCED: _("Advanced")
    }

    AMO = 'AMO'
    TSO = 'TSO'
    OPT = 'OPT'

    OPERATOR_TYPES = {
        AMO: _("AMO"),
        TSO: _("TSO"),
        OPT: _("OPT")
    }

    class Meta:
        app_label = 'snisi_trachoma'
        verbose_name = _("TT Backlog Mission Report")
        verbose_name_plural = _("TT Backlog Mission Reports")

    # meta fields
    started_on = models.DateField(verbose_name="Date de démarrage")
    ended_on = models.DateField(verbose_name="Date de fin",
                                blank=True, null=True)
    operator = models.ForeignKey(Provider, verbose_name="Opérateur")
    operator_type = models.CharField(
        max_length=75,
        choices=OPERATOR_TYPES.items(), verbose_name="Profil opérateur")
    strategy = models.CharField(
        max_length=75, choices=STRATEGIES.items(),
        verbose_name="Stratégie")

    village_reports = models.ManyToManyField(
        TTBacklogVillageR,
        verbose_name=_("Rapports Villages"),
        blank=True, null=True)

    # total values for all villages. real-time updated
    consultation_male = models.PositiveIntegerField(
        verbose_name="Consultations Hommes",
        default=0)
    consultation_female = models.PositiveIntegerField(
        verbose_name="Consultations Femmes",
        default=0)
    surgery_male = models.PositiveIntegerField(
        verbose_name="Chirurgies Hommes",
        default=0)
    surgery_female = models.PositiveIntegerField(
        verbose_name="Chirurgies Femmes",
        default=0)
    refusal_male = models.PositiveIntegerField(
        verbose_name="Refus Hommes",
        default=0)
    refusal_female = models.PositiveIntegerField(
        verbose_name="Refus Femmes",
        default=0)
    recidivism_male = models.PositiveIntegerField(
        verbose_name="Récidives Hommes",
        default=0)
    recidivism_female = models.PositiveIntegerField(
        verbose_name="Récidives Femmes",
        default=0)
    community_assistance = models.BooleanField(
        verbose_name="Assistance relais",
        default=0)

    # raw statistics from village reports. real-time updated
    nb_village_reports = models.PositiveIntegerField(
        verbose_name="Nb de villages visités", default=0)
    nb_community_assistance = models.PositiveIntegerField(
        verbose_name="Nb de village avec aide relais", default=0)
    nb_days_min = models.PositiveIntegerField(default=0)
    nb_days_max = models.PositiveIntegerField(default=0)
    nb_days_mean = models.FloatField(default=0)
    nb_days_median = models.FloatField(default=0)

    def total_for_field(self, field):
        values = []
        for cat in ('male', 'female'):
            fname = '{}_{}'.format(field, cat)
            if hasattr(self, fname):
                values.append(getattr(self, fname))
        return sum(values)

    @property
    def consultation(self):
        return self.total_for_field(inspect.stack()[0][3])

    @property
    def surgery(self):
        return self.total_for_field(inspect.stack()[0][3])

    @property
    def refusal(self):
        return self.total_for_field(inspect.stack()[0][3])

    @property
    def recidivism(self):
        return self.total_for_field(inspect.stack()[0][3])

    def add_village(self, report):

        # no duplicates
        if report in self.village_reports.all():
            return

        # add the report
        self.village_reports.add(report)
        self.nb_village_reports += 1

        # update all pure-data fields
        for field_part in ('consultation', 'surgery', 'refusal', 'recidivism'):
            for gender in ('male', 'female'):
                field = '{}_{}'.format(field_part, gender)
                setattr(self,
                        field,
                        getattr(self, field, 0) + getattr(report, field, 0))

        # add calculated fields
        if report.community_assistance:
            self.nb_community_assistance += 1

        durations = [r.visit_duration().days
                     for r in self.village_reports.all()]
        self.nb_days_min = numpy.min(durations)
        self.nb_days_max = numpy.max(durations)
        self.nb_days_mean = numpy.mean(durations)
        self.nb_days_median = numpy.median(durations)

        with reversion.create_revision():
            self.save()

receiver(pre_save, sender=TTBacklogMissionR)(pre_save_report)
receiver(post_save, sender=TTBacklogMissionR)(post_save_report)
reversion.register(TTBacklogMissionR, follow=['snisireport_ptr'])


class AggTTBacklogMissionR(PeriodicAggregatedReportInterface, SNISIReport):

    REPORTING_TYPE = OCCASIONAL_AGGREGATED
    INDIVIDUAL_CLS = TTBacklogMissionR

    class Meta:
        app_label = 'snisi_trachoma'
        verbose_name = _("Aggregated TT Backlog Mission Report")
        verbose_name_plural = _("Aggregated TT Backlog Mission Reports")

    consultation_male = models.PositiveIntegerField(
        verbose_name="Consultations Hommes")
    consultation_female = models.PositiveIntegerField(
        verbose_name="Consultations Femmes")
    surgery_male = models.PositiveIntegerField(
        verbose_name="Chirurgies Hommes")
    surgery_female = models.PositiveIntegerField(
        verbose_name="Chirurgies Femmes")
    refusal_male = models.PositiveIntegerField(
        verbose_name="Refus Hommes")
    refusal_female = models.PositiveIntegerField(
        verbose_name="Refus Femmes")
    recidivism_male = models.PositiveIntegerField(
        verbose_name="Récidives Hommes")
    recidivism_female = models.PositiveIntegerField(
        verbose_name="Récidives Femmes")
    community_assistance = models.BooleanField(
        verbose_name="Assistance relais")

    village_reports = models.ManyToManyField(
        TTBacklogVillageR,
        verbose_name=_("Rapports Villages"),
        blank=True, null=True)

    # raw statistics from village reports. real-time updated
    nb_village_reports = models.PositiveIntegerField()
    nb_community_assistance = models.PositiveIntegerField()
    nb_days_min = models.PositiveIntegerField()
    nb_days_max = models.PositiveIntegerField()
    nb_days_avg = models.FloatField()
    nb_days_med = models.FloatField()

receiver(pre_save, sender=AggTTBacklogMissionR)(pre_save_report)
receiver(post_save, sender=AggTTBacklogMissionR)(post_save_report)

reversion.register(AggTTBacklogMissionR, follow=['snisireport_ptr'])
