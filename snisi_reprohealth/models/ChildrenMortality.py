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
from snisi_core.models.Entities import AdministrativeEntity
from snisi_core.models.Reporting import (SNISIReport,
                                         PeriodicAggregatedReportInterface,
                                         OCCASIONAL_SOURCE, OCCASIONAL_AGGREGATED)


class ChildrenDeathR(SNISIReport):

    HOME = 'home'
    CENTER = 'health_center'
    OTHER = 'other'
    DEATHPLACE = {
        HOME: _("Home"),
        CENTER: _("Health Center"),
        OTHER: _("Other")
    }

    MALE = 'male'
    FEMALE = 'female'
    SEX = {
        FEMALE: _("Female"),
        MALE: _("Male")
    }

    CAUSE_FEVER = 'female'
    CAUSE_DIARRHEA = 'diarrhea'
    CAUSE_DYSPNEA = 'dyspnea'
    CAUSE_ANEMIA = 'anemia'
    CAUSE_RASH = 'rash'
    CAUSE_COUGH = 'cough'
    CAUSE_VOMITING = 'vomiting'
    CAUSE_NUCHAL_RIGIDITY = 'nuchal_rigidity'
    CAUSE_RED_EYE = 'red_eye'
    CAUSE_EAT_REFUSAL = 'eat_refusal'
    CAUSE_OTHER = 'other'
    DEATH_CAUSES = {
        CAUSE_FEVER: _("Fever"),
        CAUSE_DIARRHEA: _("Diarrhea"),
        CAUSE_DYSPNEA: _("Dyspnea"),
        CAUSE_ANEMIA: _("Anemia"),
        CAUSE_RASH: _("Rash"),
        CAUSE_COUGH: _("Cough"),
        CAUSE_VOMITING: _("Vomiting"),
        CAUSE_NUCHAL_RIGIDITY: _("Nuchal Rigidity"),
        CAUSE_RED_EYE: _("Red Eye"),
        CAUSE_EAT_REFUSAL: _("Eat Refusal"),
        CAUSE_OTHER: _("Other")
    }

    REPORTING_TYPE = OCCASIONAL_SOURCE
    RECEIPT_FORMAT = "__{id}__"

    class Meta:
        app_label = 'snisi_reprohealth'
        verbose_name = _("Children Mortality Report")
        verbose_name_plural = _("Children Mortality Reports")

    reporting_location = models.ForeignKey(AdministrativeEntity,
                                           related_name='children_reported_in',
                                           verbose_name=_("Reporting location"))
    name = models.CharField(max_length=100,
                            verbose_name=_("Name of the deceased"))
    sex = models.CharField(max_length=45,
                           choices=SEX.items(),
                           verbose_name=_("Sex"))
    dob = models.DateField(verbose_name=_("Date of birth"))
    dob_auto = models.BooleanField(default=False,
                                   verbose_name=_("DOB is an estimation?"))
    dod = models.DateField(verbose_name=_("Date of death"))
    death_location = models.ForeignKey(AdministrativeEntity,
                                       related_name='children_dead_in',
                                       verbose_name=_("Death Location"))
    death_place = models.CharField(max_length=45,
                                   choices=DEATHPLACE.items(),
                                   verbose_name=_("Place of death"))

    cause_of_death = models.CharField(max_length=45,
                                      choices=DEATH_CAUSES.items())

    def add_data(self,
                 name, sex, dob, dob_auto, dod, death_place, cause_of_death):
        self.name = name
        self.sex = sex
        self.dob = dob
        self.dob_auto = dob_auto
        self.dod = dod
        self.death_place = death_place
        self.cause_of_death = cause_of_death

    def __str__(self):
        return ugettext("{name}/{dod}").format(name=self.name.title(),
                                               dod=self.dod.strftime('%d-%m-%Y'))

receiver(pre_save, sender=ChildrenDeathR)(pre_save_report)
receiver(post_save, sender=ChildrenDeathR)(post_save_report)

reversion.register(ChildrenDeathR)


class AggChildrenDeathR(PeriodicAggregatedReportInterface, SNISIReport):

    REPORTING_TYPE = OCCASIONAL_AGGREGATED
    RECEIPT_FORMAT = "__{id}__"
    INDIVIDUAL_CLS = ChildrenDeathR

    class Meta:
        app_label = 'snisi_reprohealth'
        verbose_name = _("Aggregated Children Mortality Report")
        verbose_name_plural = _("Aggregated Children Mortality Reports")

    sex_male = models.PositiveIntegerField()
    sexe_female = models.PositiveIntegerField()

    age_under_1w = models.PositiveIntegerField()
    age_under_2weeks = models.PositiveIntegerField()
    age_under_1month = models.PositiveIntegerField()
    age_under_3month = models.PositiveIntegerField()
    age_under_6month = models.PositiveIntegerField()
    age_under_9month = models.PositiveIntegerField()
    age_under_1 = models.PositiveIntegerField()
    age_under_2 = models.PositiveIntegerField()
    age_under_3 = models.PositiveIntegerField()
    age_under_4 = models.PositiveIntegerField()
    age_under_5 = models.PositiveIntegerField()

    death_home = models.PositiveIntegerField()
    death_center = models.PositiveIntegerField()
    death_other = models.PositiveIntegerField()

    cause_death_fever = models.PositiveIntegerField()
    cause_death_diarrhea = models.PositiveIntegerField()
    cause_death_dyspnea = models.PositiveIntegerField()
    cause_death_anemia = models.PositiveIntegerField()
    cause_death_rash = models.PositiveIntegerField()
    cause_death_cough = models.PositiveIntegerField()
    cause_death_vomiting = models.PositiveIntegerField()
    cause_death_nuchal_rigidity = models.PositiveIntegerField()
    cause_death_red_eye = models.PositiveIntegerField()
    cause_death_eat_refusal = models.PositiveIntegerField()
    cause_death_other = models.PositiveIntegerField()

    indiv_sources = models.ManyToManyField(INDIVIDUAL_CLS,
        verbose_name=_(u"Primary. Sources"),
        blank=True, null=True,
        related_name='source_agg_%(class)s_reports')

    def fill_blank(self):
        self.sex_male = 0
        self.sexe_female = 0

        self.age_under_1w = 0
        self.age_under_2weeks = 0
        self.age_under_1month = 0
        self.age_under_3month = 0
        self.age_under_6month = 0
        self.age_under_9month = 0
        self.age_under_1 = 0
        self.age_under_2 = 0
        self.age_under_3 = 0
        self.age_under_4 = 0
        self.age_under_5 = 0

        self.death_home = 0
        self.death_center = 0
        self.death_other = 0

        self.cause_death_fever = 0
        self.cause_death_diarrhea = 0
        self.cause_death_dyspnea = 0
        self.cause_death_anemia = 0
        self.cause_death_rash = 0
        self.cause_death_cough = 0
        self.cause_death_vomiting = 0
        self.cause_death_nuchal_rigidity = 0
        self.cause_death_red_eye = 0
        self.cause_death_eat_refusal = 0
        self.cause_death_other = 0

    @classmethod
    def create_from(cls, period, entity, author):

        # find list of sources
        indiv_sources = ChildrenDeathR.objects.filter(dod__gte=period.start_on,
                                                      dod__lte=period.end_on,
                                                      death_location__in=entity.get_children())
        agg_sources = cls.objects.filter(period=period,
                                         entity__in=entity.get_children())

        return PeriodicAggregatedReportInterface.create_from(
            period, entity, author,
            indiv_sources=indiv_sources, agg_sources=agg_sources)

    @classmethod
    def update_instance_with_indiv(cls, report, instance):

        # sex
        if instance.sex == instance.MALE:
            report.sex_male += 1
        elif instance.sex == instance.FEMALE:
            report.sexe_female += 1

        # death place
        if instance.death_place == instance.HOME:
            report.death_home += 1
        elif instance.death_place == instance.CENTER:
            report.death_center += 1
        else:
            report.death_other += 1

        # cause of death
        if instance.cause_of_death == instance.CAUSE_FEVER:
            report.cause_death_fever += 1
        elif instance.cause_of_death == instance.CAUSE_DIARRHEA:
            report.cause_death_diarrhea += 1
        elif instance.cause_of_death == instance.CAUSE_DYSPNEA:
            report.cause_death_dyspnea += 1
        elif instance.cause_of_death == instance.CAUSE_ANEMIA:
            report.cause_death_anemia += 1
        elif instance.cause_of_death == instance.CAUSE_RASH:
            report.cause_death_rash += 1
        elif instance.cause_of_death == instance.CAUSE_COUGH:
            report.cause_death_cough += 1
        elif instance.cause_of_death == instance.CAUSE_VOMITING:
            report.cause_death_vomiting += 1
        elif instance.cause_of_death == instance.CAUSE_NUCHAL_RIGIDITY:
            report.cause_death_nuchal_rigidity += 1
        elif instance.cause_of_death == instance.CAUSE_RED_EYE:
            report.cause_death_red_eye += 1
        elif instance.cause_of_death == instance.CAUSE_EAT_REFUSAL:
            report.cause_death_eat_refusal += 1
        else:
            report.cause_death_other += 1

        # age
        age_days = (instance.dod - instance.dob).days
        if age_days < 7:
            report.age_under_1w += 1
        if age_days < 14:
            report.age_under_2weeks += 1
        if age_days < 30:
            report.age_under_1month += 1
        if age_days / 30 < 3:
            report.age_under_3month += 1
        if age_days / 30 < 6:
            report.age_under_6month += 1
        if age_days / 30 < 9:
            report.age_under_9month += 1
        if age_days < 365:
            report.age_under_1 += 1
        if age_days / 365 < 2:
            report.age_under_2 += 1
        if age_days / 365 < 3:
            report.age_under_3 += 1
        if age_days / 365 < 4:
            report.age_under_4 += 1
        if age_days / 365 <= 5:
            report.age_under_5 += 1

    @classmethod
    def update_instance_with_agg(cls, report, instance):

        report.sex_male += instance.sex_male
        report.sexe_female += instance.sexe_female

        report.age_under_1w += instance.age_under_1w
        report.age_under_2weeks += instance.age_under_2weeks
        report.age_under_1month += instance.age_under_1month
        report.age_under_3month += instance.age_under_3month
        report.age_under_6month += instance.age_under_6month
        report.age_under_9month += instance.age_under_9month
        report.age_under_1 += instance.age_under_1
        report.age_under_2 += instance.age_under_2
        report.age_under_3 += instance.age_under_3
        report.age_under_4 += instance.age_under_4
        report.age_under_5 += instance.age_under_5

        report.death_home += instance.death_home
        report.death_center += instance.death_center
        report.death_other += instance.death_other

        report.cause_death_fever += instance.cause_death_fever
        report.cause_death_diarrhea += instance.cause_death_diarrhea
        report.cause_death_dyspnea += instance.cause_death_dyspnea
        report.cause_death_anemia += instance.cause_death_anemia
        report.cause_death_rash += instance.cause_death_rash
        report.cause_death_cough += instance.cause_death_cough
        report.cause_death_vomiting += instance.cause_death_vomiting
        report.cause_death_nuchal_rigidity += instance.cause_death_nuchal_rigidity
        report.cause_death_red_eye += instance.cause_death_red_eye
        report.cause_death_eat_refusal += instance.cause_death_eat_refusal
        report.cause_death_other += instance.cause_death_other

receiver(pre_save, sender=AggChildrenDeathR)(pre_save_report)
receiver(post_save, sender=AggChildrenDeathR)(post_save_report)

reversion.register(AggChildrenDeathR)
