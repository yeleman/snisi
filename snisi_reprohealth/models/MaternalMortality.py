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

from snisi_core.models.Entities import AdministrativeEntity
from snisi_core.models.common import pre_save_report, post_save_report
from snisi_core.models.Reporting import (SNISIReport,
                                         PeriodicAggregatedReportInterface,
                                         OCCASIONAL_SOURCE,
                                         OCCASIONAL_AGGREGATED)


class MaternalDeathR(SNISIReport):

    CAUSE_BLEEDING = 'bleeding'
    CAUSE_FEVER = 'fever'
    CAUSE_HTN = 'htn'
    CAUSE_DIARRHEA = 'diarrhea'
    CAUSE_CRISIS = 'crisis'
    CAUSE_MISCARRIAGE = 'miscarriage'
    CAUSE_ABORTION = 'abortion'
    CAUSE_OTHER = 'other'
    DEATH_CAUSES = {
        CAUSE_BLEEDING: _("Bleeding"),
        CAUSE_FEVER: _("Fever"),
        CAUSE_HTN: _("High Blood Pressure"),
        CAUSE_DIARRHEA: _("Diarrhea"),
        CAUSE_CRISIS: _("Crisis"),
        CAUSE_MISCARRIAGE: _("Miscarriage"),
        CAUSE_ABORTION: _("Abortion"),
        CAUSE_OTHER: _("Other")
    }

    REPORTING_TYPE = OCCASIONAL_SOURCE
    RECEIPT_FORMAT = "__{id}__"

    class Meta:
        app_label = 'snisi_reprohealth'
        verbose_name = _("Maternal Mortality Report")
        verbose_name_plural = _("Maternal Mortality Reports")

    reporting_location = models.ForeignKey(
        AdministrativeEntity, related_name='maternal_reported_in',
        verbose_name=_("Reporting location"))
    name = models.CharField(max_length=100,
                            verbose_name=_("Name of the deceased"))
    dob = models.DateField(verbose_name=_("Date of birth"))
    dob_auto = models.BooleanField(default=False,
                                   verbose_name=_("DOB is an estimation?"))
    dod = models.DateField(verbose_name=_("Date of death"))
    death_location = models.ForeignKey(AdministrativeEntity,
                                       related_name='maternal_dead_in',
                                       verbose_name=_("Place of death"))
    living_children = models.PositiveIntegerField(
        verbose_name=_("Living children of the deceased"))
    dead_children = models.PositiveIntegerField(
        verbose_name=_("Dead children of the deceased"))
    pregnant = models.BooleanField(verbose_name=_("Pregnant?"))
    pregnancy_weeks = models.PositiveIntegerField(
        null=True,
        verbose_name=_("Duration of the pregnancy (weeks)"))
    pregnancy_related_death = models.BooleanField(
        default=False, verbose_name=_("Pregnancy related death"))

    cause_of_death = models.CharField(
        max_length=1, choices=DEATH_CAUSES.items())

    def add_data(self, name, dob, dob_auto, dod, death_location,
                 living_children, dead_children, pregnant,
                 pregnancy_weeks, pregnancy_related_death, cause_of_death):
        self.name = name
        self.dob = dob
        self.dob_auto = dob_auto
        self.dod = dod
        self.living_children = living_children
        self.dead_children = dead_children
        self.pregnant = pregnant
        self.pregnancy_weeks = pregnancy_weeks
        self.pregnancy_related_death = pregnancy_related_death
        self.cause_of_death = cause_of_death

    def __str__(self):
        return ugettext("{name}/{dod}").format(
            name=self.name.title(),
            dod=self.dod.strftime('%d-%m-%Y'))

receiver(pre_save, sender=MaternalDeathR)(pre_save_report)
receiver(post_save, sender=MaternalDeathR)(post_save_report)

reversion.register(MaternalDeathR)


class AggMaternalDeathR(PeriodicAggregatedReportInterface, SNISIReport):

    REPORTING_TYPE = OCCASIONAL_AGGREGATED
    INDIVIDUAL_CLS = MaternalDeathR
    RECEIPT_FORMAT = "__{id}__"

    class Meta:
        app_label = 'snisi_reprohealth'
        verbose_name = _("Aggregated Maternal Mortality Report")
        verbose_name_plural = _("Aggregated Maternal Mortality Reports")

    age_under_15 = models.PositiveIntegerField()
    age_under_18 = models.PositiveIntegerField()
    age_under_20 = models.PositiveIntegerField()
    age_under_25 = models.PositiveIntegerField()
    age_under_30 = models.PositiveIntegerField()
    age_under_35 = models.PositiveIntegerField()
    age_under_40 = models.PositiveIntegerField()
    age_under_45 = models.PositiveIntegerField()
    age_under_50 = models.PositiveIntegerField()
    age_over_50 = models.PositiveIntegerField()

    have_living_children = models.PositiveIntegerField()
    have_one_living_children = models.PositiveIntegerField()
    have_two_living_children = models.PositiveIntegerField()
    have_two_plus_living_children = models.PositiveIntegerField()
    have_dead_children = models.PositiveIntegerField()
    have_one_dead_children = models.PositiveIntegerField()
    have_two_dead_children = models.PositiveIntegerField()
    have_two_plus_dead_children = models.PositiveIntegerField()

    is_pregnant = models.PositiveIntegerField()
    is_pregnant_1week = models.PositiveIntegerField()
    is_pregnant_2weeks = models.PositiveIntegerField()
    is_pregnant_3weeks = models.PositiveIntegerField()
    is_pregnant_4weeks = models.PositiveIntegerField()
    is_pregnant_5weeks = models.PositiveIntegerField()
    is_pregnant_6weeks = models.PositiveIntegerField()
    is_pregnant_7weeks = models.PositiveIntegerField()
    is_pregnant_8weeks = models.PositiveIntegerField()
    is_pregnant_9weeks = models.PositiveIntegerField()
    is_pregnant_10weeks = models.PositiveIntegerField()
    is_pregnant_11weeks = models.PositiveIntegerField()
    is_pregnant_12weeks = models.PositiveIntegerField()
    is_pregnant_13weeks = models.PositiveIntegerField()
    is_pregnant_14weeks = models.PositiveIntegerField()
    is_pregnant_15weeks = models.PositiveIntegerField()
    is_pregnant_16weeks = models.PositiveIntegerField()
    is_pregnant_17weeks = models.PositiveIntegerField()
    is_pregnant_18weeks = models.PositiveIntegerField()
    is_pregnant_19weeks = models.PositiveIntegerField()
    is_pregnant_20weeks = models.PositiveIntegerField()
    is_pregnant_21weeks = models.PositiveIntegerField()
    is_pregnant_22weeks = models.PositiveIntegerField()
    is_pregnant_23weeks = models.PositiveIntegerField()
    is_pregnant_24weeks = models.PositiveIntegerField()
    is_pregnant_25weeks = models.PositiveIntegerField()
    is_pregnant_26weeks = models.PositiveIntegerField()
    is_pregnant_27weeks = models.PositiveIntegerField()
    is_pregnant_28weeks = models.PositiveIntegerField()
    is_pregnant_29weeks = models.PositiveIntegerField()
    is_pregnant_30weeks = models.PositiveIntegerField()
    is_pregnant_31weeks = models.PositiveIntegerField()
    is_pregnant_32weeks = models.PositiveIntegerField()
    is_pregnant_33weeks = models.PositiveIntegerField()
    is_pregnant_34weeks = models.PositiveIntegerField()
    is_pregnant_35weeks = models.PositiveIntegerField()
    is_pregnant_36weeks = models.PositiveIntegerField()
    is_pregnant_37weeks = models.PositiveIntegerField()
    is_pregnant_38weeks = models.PositiveIntegerField()
    is_pregnant_39weeks = models.PositiveIntegerField()
    is_pregnant_40weeks = models.PositiveIntegerField()
    is_pregnant_40weeks_plus = models.PositiveIntegerField()

    is_pregnancy_related = models.PositiveIntegerField()

    cause_bleeding = models.PositiveIntegerField()
    cause_fever = models.PositiveIntegerField()
    cause_htn = models.PositiveIntegerField()
    cause_diarrhea = models.PositiveIntegerField()
    cause_crisis = models.PositiveIntegerField()
    cause_miscarriage = models.PositiveIntegerField()
    cause_abortion = models.PositiveIntegerField()
    cause_other = models.PositiveIntegerField()

    indiv_sources = models.ManyToManyField(
        INDIVIDUAL_CLS,
        verbose_name=_(u"Primary. Sources"),
        blank=True,
        related_name='source_agg_%(class)s_reports')

    def fill_blank(self):
        self.age_under_15 = 0
        self.age_under_18 = 0
        self.age_under_20 = 0
        self.age_under_25 = 0
        self.age_under_30 = 0
        self.age_under_35 = 0
        self.age_under_40 = 0
        self.age_under_45 = 0
        self.age_under_50 = 0
        self.age_over_50 = 0

        self.have_living_children = 0
        self.have_dead_children = 0

        self.is_pregnant = 0
        self.is_pregnant_1week = 0
        self.is_pregnant_2weeks = 0
        self.is_pregnant_3weeks = 0
        self.is_pregnant_4weeks = 0
        self.is_pregnant_5weeks = 0
        self.is_pregnant_6weeks = 0
        self.is_pregnant_7weeks = 0
        self.is_pregnant_8weeks = 0
        self.is_pregnant_9weeks = 0
        self.is_pregnant_10weeks = 0
        self.is_pregnant_11weeks = 0
        self.is_pregnant_12weeks = 0
        self.is_pregnant_13weeks = 0
        self.is_pregnant_14weeks = 0
        self.is_pregnant_15weeks = 0
        self.is_pregnant_16weeks = 0
        self.is_pregnant_17weeks = 0
        self.is_pregnant_18weeks = 0
        self.is_pregnant_19weeks = 0
        self.is_pregnant_20weeks = 0
        self.is_pregnant_21weeks = 0
        self.is_pregnant_22weeks = 0
        self.is_pregnant_23weeks = 0
        self.is_pregnant_24weeks = 0
        self.is_pregnant_25weeks = 0
        self.is_pregnant_26weeks = 0
        self.is_pregnant_27weeks = 0
        self.is_pregnant_28weeks = 0
        self.is_pregnant_29weeks = 0
        self.is_pregnant_30weeks = 0
        self.is_pregnant_31weeks = 0
        self.is_pregnant_32weeks = 0
        self.is_pregnant_33weeks = 0
        self.is_pregnant_34weeks = 0
        self.is_pregnant_35weeks = 0
        self.is_pregnant_36weeks = 0
        self.is_pregnant_37weeks = 0
        self.is_pregnant_38weeks = 0
        self.is_pregnant_39weeks = 0
        self.is_pregnant_40weeks = 0
        self.is_pregnant_40weeks_plus = 0

        self.is_pregnancy_related = 0

        self.cause_bleeding = 0
        self.cause_fever = 0
        self.cause_htn = 0
        self.cause_diarrhea = 0
        self.cause_crisis = 0
        self.cause_miscarriage = 0
        self.cause_abortion = 0
        self.cause_other = 0

    @classmethod
    def create_from(cls, period, entity, author):

        # find list of sources
        indiv_sources = MaternalDeathR.objects.filter(
            dod__gte=period.start_on, dod__lte=period.end_on,
            death_location__in=entity.get_children())
        agg_sources = cls.objects.filter(period=period,
                                         entity__in=entity.get_children())

        return PeriodicAggregatedReportInterface.create_from(
            period, entity, author,
            indiv_sources=indiv_sources, agg_sources=agg_sources)

    @classmethod
    def update_instance_with_indiv(cls, report, instance):

        # age
        age_years = (instance.dod - instance.dob).days / 365
        if age_years < 15:
            report.age_under_15 += 1
        if age_years < 18:
            report.age_under_18 += 1
        if age_years < 20:
            report.age_under_20 += 1
        if age_years < 25:
            report.age_under_25 += 1
        if age_years < 30:
            report.age_under_30 += 1
        if age_years < 35:
            report.age_under_35 += 1
        if age_years < 40:
            report.age_under_40 += 1
        if age_years < 45:
            report.age_under_45 += 1
        if age_years < 50:
            report.age_under_50 += 1
        else:
            report.age_over_50 += 1

        # children
        if instance.living_children > 0:
            report.have_living_children += 1
        if instance.living_children == 1:
            report.have_one_living_children += 1
        if instance.living_children == 2:
            report.have_two_living_children += 1
        if instance.living_children > 2:
            report.have_two_plus_living_children += 1
        if instance.dead_children > 0:
            report.have_dead_children += 1
        if instance.dead_children == 1:
            report.have_one_dead_children += 1
        if instance.dead_children == 2:
            report.have_two_dead_children += 1
        if instance.dead_children > 2:
            report.have_two_plus_dead_children += 1

        # pregnancy
        if instance.pregnant:
            report.is_pregnant += 1

        if instance.pregnancy_weeks == 1:
            report.is_pregnant_1week += 1
        if instance.pregnancy_weeks == 2:
            report.is_pregnant_2weeks += 1
        if instance.pregnancy_weeks == 3:
            report.is_pregnant_3weeks += 1
        if instance.pregnancy_weeks == 4:
            report.is_pregnant_4weeks += 1
        if instance.pregnancy_weeks == 5:
            report.is_pregnant_5weeks += 1
        if instance.pregnancy_weeks == 6:
            report.is_pregnant_6weeks += 1
        if instance.pregnancy_weeks == 7:
            report.is_pregnant_7weeks += 1
        if instance.pregnancy_weeks == 8:
            report.is_pregnant_8weeks += 1
        if instance.pregnancy_weeks == 9:
            report.is_pregnant_9weeks += 1
        if instance.pregnancy_weeks == 10:
            report.is_pregnant_10weeks += 1
        if instance.pregnancy_weeks == 11:
            report.is_pregnant_11weeks += 1
        if instance.pregnancy_weeks == 12:
            report.is_pregnant_12weeks += 1
        if instance.pregnancy_weeks == 13:
            report.is_pregnant_13weeks += 1
        if instance.pregnancy_weeks == 14:
            report.is_pregnant_14weeks += 1
        if instance.pregnancy_weeks == 15:
            report.is_pregnant_15weeks += 1
        if instance.pregnancy_weeks == 16:
            report.is_pregnant_16weeks += 1
        if instance.pregnancy_weeks == 17:
            report.is_pregnant_17weeks += 1
        if instance.pregnancy_weeks == 18:
            report.is_pregnant_18weeks += 1
        if instance.pregnancy_weeks == 19:
            report.is_pregnant_19weeks += 1
        if instance.pregnancy_weeks == 20:
            report.is_pregnant_20weeks += 1
        if instance.pregnancy_weeks == 21:
            report.is_pregnant_21weeks += 1
        if instance.pregnancy_weeks == 22:
            report.is_pregnant_22weeks += 1
        if instance.pregnancy_weeks == 23:
            report.is_pregnant_23weeks += 1
        if instance.pregnancy_weeks == 24:
            report.is_pregnant_24weeks += 1
        if instance.pregnancy_weeks == 25:
            report.is_pregnant_25weeks += 1
        if instance.pregnancy_weeks == 26:
            report.is_pregnant_26weeks += 1
        if instance.pregnancy_weeks == 27:
            report.is_pregnant_27weeks += 1
        if instance.pregnancy_weeks == 28:
            report.is_pregnant_28weeks += 1
        if instance.pregnancy_weeks == 29:
            report.is_pregnant_29weeks += 1
        if instance.pregnancy_weeks == 30:
            report.is_pregnant_30weeks += 1
        if instance.pregnancy_weeks == 31:
            report.is_pregnant_31weeks += 1
        if instance.pregnancy_weeks == 32:
            report.is_pregnant_32weeks += 1
        if instance.pregnancy_weeks == 33:
            report.is_pregnant_33weeks += 1
        if instance.pregnancy_weeks == 34:
            report.is_pregnant_34weeks += 1
        if instance.pregnancy_weeks == 35:
            report.is_pregnant_35weeks += 1
        if instance.pregnancy_weeks == 36:
            report.is_pregnant_36weeks += 1
        if instance.pregnancy_weeks == 37:
            report.is_pregnant_37weeks += 1
        if instance.pregnancy_weeks == 38:
            report.is_pregnant_38weeks += 1
        if instance.pregnancy_weeks == 39:
            report.is_pregnant_39weeks += 1
        if instance.pregnancy_weeks == 40:
            report.is_pregnant_40weeks += 1
        if instance.pregnancy_weeks > 40:
            report.is_pregnant_40weeks_plus += 1

        if instance.pregnancy_related_death:
            report.is_pregnancy_related += 1

        # cause of death
        if instance.cause_of_death == instance.CAUSE_BLEEDING:
            report.cause_bleeding += 1
        elif instance.cause_of_death == instance.CAUSE_FEVER:
            report.cause_fever += 1
        elif instance.cause_of_death == instance.CAUSE_HTN:
            report.cause_htn += 1
        elif instance.cause_of_death == instance.CAUSE_DIARRHEA:
            report.cause_diarrhea += 1
        elif instance.cause_of_death == instance.CAUSE_CRISIS:
            report.cause_crisis += 1
        elif instance.cause_of_death == instance.CAUSE_MISCARRIAGE:
            report.cause_miscarriage += 1
        elif instance.cause_of_death == instance.CAUSE_ABORTION:
            report.cause_abortion += 1
        else:
            report.cause_other += 1

    @classmethod
    def update_instance_with_agg(cls, report, instance):

        # age
        report.age_under_15 += instance.age_under_15
        report.age_under_18 += instance.age_under_18
        report.age_under_20 += instance.age_under_20
        report.age_under_25 += instance.age_under_25
        report.age_under_30 += instance.age_under_30
        report.age_under_35 += instance.age_under_35
        report.age_under_40 += instance.age_under_40
        report.age_under_45 += instance.age_under_45
        report.age_under_50 += instance.age_under_50
        report.age_over_50 += instance.age_over_50

        # children
        report.have_living_children += instance.have_living_children
        report.have_one_living_children += instance.have_one_living_children
        report.have_two_living_children += instance.have_two_living_children
        report.have_two_plus_living_children += \
            instance.have_two_plus_living_children
        report.have_dead_children += instance.have_dead_children
        report.have_one_dead_children += instance.have_one_dead_children
        report.have_two_dead_children += instance.have_two_dead_children
        report.have_two_plus_dead_children += \
            instance.have_two_plus_dead_children

        # pregnancy
        report.is_pregnant += instance.is_pregnant
        report.is_pregnant_1week += instance.is_pregnant_1week
        report.is_pregnant_2weeks += instance.is_pregnant_2weeks
        report.is_pregnant_3weeks += instance.is_pregnant_3weeks
        report.is_pregnant_4weeks += instance.is_pregnant_4weeks
        report.is_pregnant_5weeks += instance.is_pregnant_5weeks
        report.is_pregnant_6weeks += instance.is_pregnant_6weeks
        report.is_pregnant_7weeks += instance.is_pregnant_7weeks
        report.is_pregnant_8weeks += instance.is_pregnant_8weeks
        report.is_pregnant_9weeks += instance.is_pregnant_9weeks
        report.is_pregnant_10weeks += instance.is_pregnant_10weeks
        report.is_pregnant_11weeks += instance.is_pregnant_11weeks
        report.is_pregnant_12weeks += instance.is_pregnant_12weeks
        report.is_pregnant_13weeks += instance.is_pregnant_13weeks
        report.is_pregnant_14weeks += instance.is_pregnant_14weeks
        report.is_pregnant_15weeks += instance.is_pregnant_15weeks
        report.is_pregnant_16weeks += instance.is_pregnant_16weeks
        report.is_pregnant_17weeks += instance.is_pregnant_17weeks
        report.is_pregnant_18weeks += instance.is_pregnant_18weeks
        report.is_pregnant_19weeks += instance.is_pregnant_19weeks
        report.is_pregnant_20weeks += instance.is_pregnant_20weeks
        report.is_pregnant_21weeks += instance.is_pregnant_21weeks
        report.is_pregnant_22weeks += instance.is_pregnant_22weeks
        report.is_pregnant_23weeks += instance.is_pregnant_23weeks
        report.is_pregnant_24weeks += instance.is_pregnant_24weeks
        report.is_pregnant_25weeks += instance.is_pregnant_25weeks
        report.is_pregnant_26weeks += instance.is_pregnant_26weeks
        report.is_pregnant_27weeks += instance.is_pregnant_27weeks
        report.is_pregnant_28weeks += instance.is_pregnant_28weeks
        report.is_pregnant_29weeks += instance.is_pregnant_29weeks
        report.is_pregnant_30weeks += instance.is_pregnant_30weeks
        report.is_pregnant_31weeks += instance.is_pregnant_31weeks
        report.is_pregnant_32weeks += instance.is_pregnant_32weeks
        report.is_pregnant_33weeks += instance.is_pregnant_33weeks
        report.is_pregnant_34weeks += instance.is_pregnant_34weeks
        report.is_pregnant_35weeks += instance.is_pregnant_35weeks
        report.is_pregnant_36weeks += instance.is_pregnant_36weeks
        report.is_pregnant_37weeks += instance.is_pregnant_37weeks
        report.is_pregnant_38weeks += instance.is_pregnant_38weeks
        report.is_pregnant_39weeks += instance.is_pregnant_39weeks
        report.is_pregnant_40weeks += instance.is_pregnant_40weeks
        report.is_pregnant_40weeks_plus += instance.is_pregnant_40weeks_plus

        report.is_pregnancy_related += instance.is_pregnancy_related

        # cause of death
        report.cause_bleeding += instance.cause_bleeding
        report.cause_fever += instance.cause_fever
        report.cause_htn += instance.cause_htn
        report.cause_diarrhea += instance.cause_diarrhea
        report.cause_crisis += instance.cause_crisis
        report.cause_miscarriage += instance.cause_miscarriage
        report.cause_abortion += instance.cause_abortion
        report.cause_other += instance.cause_other

receiver(pre_save, sender=AggMaternalDeathR)(pre_save_report)
receiver(post_save, sender=AggMaternalDeathR)(post_save_report)

reversion.register(AggMaternalDeathR)
