#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging
import datetime

import numpy
import reversion
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from snisi_core.models.common import (pre_save_report, post_save_report,
                                      get_temp_receipt)
from snisi_core.models.Providers import Provider
from snisi_core.models.Entities import Entity
from snisi_core.models.Reporting import (SNISIReport,
                                         OCCASIONAL_SOURCE)
from snisi_core.identifiers import base_random_id

logger = logging.getLogger(__name__)

AMO = 'AMO'
TSO = 'TSO'
OPT = 'OPT'

OPERATOR_TYPES = {
    AMO: _("AMO"),
    TSO: _("TSO"),
    OPT: _("OPT")
}

RIGHT = 'right'
LEFT = 'left'
EYES = {
    RIGHT: _("R.E"),
    LEFT: _("L.E")
}

MALE = 'male'
FEMALE = 'female'
GENDERS = {
    MALE: _("Male"),
    FEMALE: _("Female")
}

ADVANCED = 'advanced'
MOBILE = 'mobile'
FIXED = 'fixed'

STRATEGIES = {
    FIXED: _("Fixed"),
    MOBILE: _("Mobile"),
    ADVANCED: _("Advanced")
}


class CATSurgeryR(SNISIReport):

    REPORTING_TYPE = OCCASIONAL_SOURCE
    RECEIPT_FORMAT = "CAT/{id}-{rand}"

    class Meta:
        app_label = 'snisi_cataract'
        verbose_name = _("CAT Surgery Report")
        verbose_name_plural = _("CAT Surgery Reports")

    number = models.PositiveIntegerField()
    surgery_ident = models.CharField(max_length=5)
    location = models.ForeignKey(Entity)  # aire de sante
    surgery_date = models.DateField()
    gender = models.CharField(max_length=20, choices=GENDERS.items())
    eye = models.CharField(max_length=20, choices=EYES.items())
    age = models.PositiveIntegerField(help_text=_("in years"))
    result_date = models.DateField(blank=True, null=True)
    visual_acuity = models.PositiveIntegerField(blank=True, null=True)

    def result_delay(self):
        if not self.has_result():
            return None
        return (self.result_date - self.surgery_date).days

    def has_result(self):
        return self.result_date is not None and self.visual_acuity is not None

    @classmethod
    def get_by_ident(cls, ident):
        try:
            return cls.objects.get(surgery_ident=ident)
        except cls.DoesNotExist:
            return None

    @classmethod
    def existing_for(cls, mission, surgery_date, gender, eye, age, number):
        qs = mission.surgery_reports.filter(
            surgery_date=surgery_date,
            gender=gender,
            eye=eye,
            age=age,
            number=number)
        if not qs.count():
            return False
        return qs.get()

    @classmethod
    def get_unused_ident(cls):
        nb_entities = cls.objects.count()
        attempts = 0
        while attempts <= nb_entities + 10:
            attempts += 1
            ident = base_random_id(length=4)
            if cls.objects.filter(surgery_ident=ident).count():
                continue
            return ident
        raise Exception("Unable to compute a free identifier for CATSurgeryR.")

    @property
    def verbose_eye(self):
        return EYES.get(self.eye)

    @property
    def verbose_gender(self):
        return GENDERS.get(self.gender)

    @property
    def verbose_short_gender(self):
        return self.verbose_gender[0]

    @property
    def verbose_features(self):
        return _("{gender}/{age}y/{eye}").format(
            gender=self.verbose_short_gender,
            age=self.age,
            eye=self.verbose_eye)

    def __str__(self):
        return self.surgery_ident


receiver(pre_save, sender=CATSurgeryR)(pre_save_report)
receiver(post_save, sender=CATSurgeryR)(post_save_report)
reversion.register(CATSurgeryR, follow=['snisireport_ptr'])


class CATMissionR(SNISIReport):

    REPORTING_TYPE = OCCASIONAL_SOURCE
    RECEIPT_FORMAT = "CATM/{id}-{rand}"

    class Meta:
        app_label = 'snisi_cataract'
        verbose_name = _("CAT Surgery Mission Report")
        verbose_name_plural = _("CAT Surgery Mission Reports")

    # meta fields
    started_on = models.DateField(verbose_name=_("Start Date"))
    ended_on = models.DateField(verbose_name=_("End Date"),
                                blank=True, null=True)
    operator = models.ForeignKey(Provider,
                                 verbose_name=_("Operator"), null=True)
    operator_type = models.CharField(
        max_length=75,
        choices=OPERATOR_TYPES.items(), verbose_name=_("Operatr Profile"),
        null=True)
    strategy = models.CharField(
        max_length=75, choices=STRATEGIES.items(),
        verbose_name=_("Strategy"))

    surgery_reports = models.ManyToManyField(
        CATSurgeryR,
        verbose_name=_("Surgery Reports"),
        blank=True)

    # total values for all surgeries. real-time updated
    nb_surgery_male = models.PositiveIntegerField(default=0)
    nb_surgery_female = models.PositiveIntegerField(default=0)
    nb_surgery_right_eye = models.PositiveIntegerField(default=0)
    nb_surgery_left_eye = models.PositiveIntegerField(default=0)

    # age breakdown
    nb_age_under_15 = models.PositiveIntegerField(default=0)
    nb_age_under_18 = models.PositiveIntegerField(default=0)
    nb_age_under_20 = models.PositiveIntegerField(default=0)
    nb_age_under_25 = models.PositiveIntegerField(default=0)
    nb_age_under_30 = models.PositiveIntegerField(default=0)
    nb_age_under_35 = models.PositiveIntegerField(default=0)
    nb_age_under_40 = models.PositiveIntegerField(default=0)
    nb_age_under_45 = models.PositiveIntegerField(default=0)
    nb_age_under_50 = models.PositiveIntegerField(default=0)
    nb_age_over_50 = models.PositiveIntegerField(default=0)

    # raw statistics from village reports. real-time updated
    nb_surgery_reports = models.PositiveIntegerField(
        verbose_name=_("Nb of surgeries"), default=0)
    nb_days = models.PositiveIntegerField(default=0)

    result_delay_min = models.PositiveIntegerField(default=0)
    result_delay_max = models.PositiveIntegerField(default=0)
    result_delay_mean = models.FloatField(default=0)
    result_delay_median = models.FloatField(default=0)
    result_delay_total = models.PositiveIntegerField(default=0)

    @property
    def is_fixed(self):
        return self.strategy == FIXED

    @property
    def ended(self):
        return self.ended_on is not None

    def add_surgery(self, report):
        # no duplicates
        if report in self.surgery_reports.all():
            return

        # add the report
        self.surgery_reports.add(report)
        self.nb_surgery_reports += 1

        # update all pure-data fields
        for field_part in ('male', 'female', 'right_eye', 'left_eye'):
            field = '{}_{}'.format('surgery', field_part)
            setattr(self,
                    field,
                    getattr(self, field, 0) + getattr(report, field, 0))

        for age_group in self.fields_for_age(report.age):
            field = 'nb_aage_{}'.format(age_group)
            setattr(self,
                    field,
                    getattr(self, field, 0) + getattr(report, field, 0))

        with reversion.create_revision():
            self.save()

    def update_delays(self):
        durations = [r.result_delay()
                     for r in self.surgery_reports.all()
                     if r.result_delay() is not None]
        if not len(durations):
            return
        self.result_delay_min = numpy.min(durations)
        self.result_delay_max = numpy.max(durations)
        self.result_delay_mean = numpy.mean(durations)
        self.result_delay_median = numpy.median(durations)
        self.result_delay_total += numpy.sum(durations)
        if self.ended:
            self.nb_days = (self.ended_on - self.started_on).days

    def close(self, ended_on=None):
        if ended_on is None:
            ended_on = datetime.date.today()
        self.ended_on = ended_on
        self.integrity_status = CATMissionR.CORRECT
        self.completion_status = CATMissionR.COMPLETE
        self.completed_on = ended_on
        self.update_delays()
        try:
            with reversion.create_revision():
                self.save()
        except Exception as e:
            logger.error("Unable to save report to DB. "
                         "Content: {} | Exp: {}"
                         .format('close', e))
            return False, ("Une erreur technique s'est "
                           "produite. Réessayez plus tard et "
                           "contactez ANTIM si le problème persiste.")

    @classmethod
    def fields_for_age(cls, age):
        fields = []
        if age < 15:
            fields.append('age_under_15')
        if age < 18:
            fields.append('age_under_18')
        if age < 20:
            fields.append('age_under_20')
        if age < 25:
            fields.append('age_under_25')
        if age < 30:
            fields.append('age_under_30')
        if age < 35:
            fields.append('age_under_35')
        if age < 40:
            fields.append('age_under_40')
        if age < 45:
            fields.append('age_under_45')
        if age < 50:
            fields.append('age_under_50')
        else:
            fields.append('age_over_50')
        return fields

    @classmethod
    def get_or_create_fixed_for(cls, entity, period, provider):
        try:
            return cls.objects.get(period=period, entity=entity,
                                   strategy=FIXED)
        except cls.DoesNotExist:
            report = cls.start(
                period=period,
                entity=entity,
                created_by=provider,
                completion_status=CATMissionR.INCOMPLETE,
                arrival_status=CATMissionR.ON_TIME,
                validation_status=CATMissionR.NOT_VALIDATED)
            report.started_on = period.start_on
            report.strategy = FIXED
            report.receipt = get_temp_receipt(report)[:10]
            try:
                with reversion.create_revision():
                    report.save()
                return report
            except Exception as e:
                logger.error("Unable to save report to DB. "
                             "Content: {} | Exp: {}"
                             .format('get_or_create_fixed_for', e))
                raise e


receiver(pre_save, sender=CATMissionR)(pre_save_report)
receiver(post_save, sender=CATMissionR)(post_save_report)
reversion.register(CATMissionR, follow=['snisireport_ptr'])
