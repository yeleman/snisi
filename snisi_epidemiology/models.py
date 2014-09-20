#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import datetime

import reversion
from py3compat import implements_to_string
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from django.utils.translation import ugettext_lazy as _, ugettext

from snisi_core.models.Periods import (WeekPeriod, ONE_WEEK_DELTA,
                                       ONE_MICROSECOND_DELTA,
                                       SpecificTypeManager,
                                       normalize_date)
from snisi_core.models.common import pre_save_report, post_save_report
from snisi_core.models.Reporting import (SNISIReport,
                                         PeriodicAggregatedReportInterface,
                                         PERIODICAL_SOURCE,
                                         PERIODICAL_AGGREGATED)
from snisi_epidemiology.xls_export import epid_activities_as_xls

EPI_WEEK = 'epi_week'


class EpiWeekManager(SpecificTypeManager):
    SPECIFIC_TYPE = EPI_WEEK


class EpiWeekPeriod(WeekPeriod):

    class Meta:
        proxy = True
        verbose_name = _("Week Period")
        verbose_name_plural = _("Week Periods")

    objects = EpiWeekManager()

    @classmethod
    def type(cls):
        return EPI_WEEK

    @property
    def pid(self):
        return'eW{}'.format(self.middle().strftime('%W-%Y'))

    @classmethod
    def boundaries(cls, date_obj):
        date_obj = normalize_date(date_obj, as_aware=True)

        monday = date_obj - datetime.timedelta(date_obj.weekday())
        monday = monday.replace(hour=0, minute=0, second=0, microsecond=0)

        friday_noon_dt = datetime.timedelta(days=4, minutes=720)
        friday_noon = monday + friday_noon_dt
        is_next_week = not date_obj < friday_noon

        if not is_next_week:
            start = friday_noon - ONE_WEEK_DELTA
        else:
            start = friday_noon
        end = start + datetime.timedelta(cls.delta()) - ONE_MICROSECOND_DELTA
        return (start, end)

    def strid(self):
        return self.middle().strftime('eW%W-%Y')


class EpiWeekReportingManager(models.Manager):
    def get_queryset(self):
        return super(EpiWeekReportingManager, self) \
            .get_queryset().filter(period_type='epi_week_reporting_period')


class EpiWeekReportingPeriod(WeekPeriod):

    class Meta:
        proxy = True
        verbose_name = _("Week Reporting Period")
        verbose_name_plural = _("Week Reporting Periods")

    objects = EpiWeekReportingManager()

    @classmethod
    def type(cls):
        return 'epi_week_reporting_period'

    @property
    def pid(self):
        return'eWRP{}'.format(self.middle().strftime('%W-%Y'))

    @classmethod
    def boundaries(cls, date_obj):
        epi_week = EpiWeekPeriod.find_create_by_date(
            date_obj, dont_create=True)
        start = epi_week.end_on + ONE_MICROSECOND_DELTA
        end = start + datetime.timedelta(days=2)
        return start, end

    def strid(self):
        return self.middle().strftime('eWRP%W-%Y')


class EpiWeekDistrictValidationManager(models.Manager):
    def get_queryset(self):
        return super(EpiWeekDistrictValidationManager, self) \
            .get_queryset().filter(period_type='epi_week_district_validation')


class EpiWeekDistrictValidationPeriod(WeekPeriod):

    class Meta:
        proxy = True
        verbose_name = _("Week District Validation Period")
        verbose_name_plural = _("Week District Validation Periods")

    objects = EpiWeekDistrictValidationManager()

    @classmethod
    def type(cls):
        return 'epi_week_district_validation'

    @property
    def pid(self):
        return'eWDVP{}'.format(self.middle().strftime('%W-%Y'))

    @classmethod
    def boundaries(cls, date_obj):
        epi_week = EpiWeekPeriod.find_create_by_date(
            date_obj, dont_create=True)
        start = epi_week.end_on + ONE_MICROSECOND_DELTA
        end = start + datetime.timedelta(days=3)
        return start, end

    def strid(self):
        return self.middle().strftime('eWVP%W-%Y')


class EpiWeekRegionValidationManager(models.Manager):
    def get_queryset(self):
        return super(EpiWeekRegionValidationManager, self) \
            .get_queryset().filter(period_type='epi_week_region_validation')


class EpiWeekRegionValidationPeriod(WeekPeriod):

    class Meta:
        proxy = True
        verbose_name = _("Week Region Validation Period")
        verbose_name_plural = _("Week Region Validation Periods")

    objects = EpiWeekRegionValidationManager()

    @classmethod
    def type(cls):
        return 'epi_week_region_validation'

    @property
    def pid(self):
        return'eWRVP{}'.format(self.middle().strftime('%W-%Y'))

    @classmethod
    def boundaries(cls, date_obj):
        epi_week = EpiWeekPeriod.find_create_by_date(
            date_obj, dont_create=True)
        start = epi_week.end_on + ONE_MICROSECOND_DELTA
        end = start + datetime.timedelta(days=4)
        return start, end

    def strid(self):
        return self.middle().strftime('eWRVP%W-%Y')


class AbstractEpidemiologyR(SNISIReport):

    class Meta:
        app_label = 'snisi_epidemiology'
        abstract = True

    DISEASE_NAMES = {
        'ebola': _("Ebola"),
        'acute_flaccid_paralysis': _("AFP"),
        'influenza_a_h1n1': _("Influenza A H1N1"),
        'cholera': _("Cholera"),
        'red_diarrhea': _("Red Diarrhea"),
        'measles': _("Measles"),
        'yellow_fever': _("Yellow Fever"),
        'neonatal_tetanus': _("NNT"),
        'meningitis': _("Meningitis"),
        'rabies': _("Rabies"),
        'acute_measles_diarrhea': _("Acute Measles Diarrhea"),
        'other_notifiable_disease': _("Other Notifiable Diseases")
    }

    ebola_case = models.IntegerField(_("Suspected Ebola cases"))
    ebola_death = models.IntegerField(_("Suspected Ebola death"))

    acute_flaccid_paralysis_case = models.IntegerField(
        _("Suspected AFP cases"))
    acute_flaccid_paralysis_death = models.IntegerField(
        _("Suspected AFP death"))

    influenza_a_h1n1_case = models.IntegerField(
        _("Suspected Influenza A H1N1 cases"))
    influenza_a_h1n1_death = models.IntegerField(
        _("Suspected Influenza A H1N1 death"))

    cholera_case = models.IntegerField(_("Suspected Cholera cases"))
    cholera_death = models.IntegerField(_("Suspected Cholera death"))

    red_diarrhea_case = models.IntegerField(_("Suspected Red Diarrhea cases"))
    red_diarrhea_death = models.IntegerField(_("Suspected Red Diarrhea death"))

    measles_case = models.IntegerField(_("Suspected Measles cases"))
    measles_death = models.IntegerField(_("Suspected Measles death"))

    yellow_fever_case = models.IntegerField(_("Suspected Yellow Fever cases"))
    yellow_fever_death = models.IntegerField(_("Suspected Yellow Fever death"))

    neonatal_tetanus_case = models.IntegerField(_("Suspected NNT cases"))
    neonatal_tetanus_death = models.IntegerField(_("Suspected NNT death"))

    meningitis_case = models.IntegerField(_("Suspected Meningitis cases"))
    meningitis_death = models.IntegerField(_("Suspected Meningitis death"))

    rabies_case = models.IntegerField(_("Suspected Rabies cases"))
    rabies_death = models.IntegerField(_("Suspected Rabies death"))

    acute_measles_diarrhea_case = models.IntegerField(
        _("Suspected Acute Measles Diarrhea cases"))
    acute_measles_diarrhea_death = models.IntegerField(
        _("Suspected Acute Measles Diarrhea death"))

    other_notifiable_disease_case = models.IntegerField(
        _("Suspected Other Notifiable Diseases cases"))
    other_notifiable_disease_death = models.IntegerField(
        _("Suspected Other Notifiable Diseases death"))

    def add_data(self, ebola_case,
                 ebola_death,
                 acute_flaccid_paralysis_case,
                 acute_flaccid_paralysis_death,
                 influenza_a_h1n1_case,
                 influenza_a_h1n1_death,
                 cholera_case,
                 cholera_death,
                 red_diarrhea_case,
                 red_diarrhea_death,
                 measles_case,
                 measles_death,
                 yellow_fever_case,
                 yellow_fever_death,
                 neonatal_tetanus_case,
                 neonatal_tetanus_death,
                 meningitis_case,
                 meningitis_death,
                 rabies_case,
                 rabies_death,
                 acute_measles_diarrhea_case,
                 acute_measles_diarrhea_death,
                 other_notifiable_disease_case,
                 other_notifiable_disease_death):
        self.ebola_case = ebola_case
        self.ebola_death = ebola_death
        self.acute_flaccid_paralysis_case = acute_flaccid_paralysis_case
        self.acute_flaccid_paralysis_death = acute_flaccid_paralysis_death
        self.influenza_a_h1n1_case = influenza_a_h1n1_case
        self.influenza_a_h1n1_death = influenza_a_h1n1_death
        self.cholera_case = cholera_case
        self.cholera_death = cholera_death
        self.red_diarrhea_case = red_diarrhea_case
        self.red_diarrhea_death = red_diarrhea_death
        self.measles_case = measles_case
        self.measles_death = measles_death
        self.yellow_fever_case = yellow_fever_case
        self.yellow_fever_death = yellow_fever_death
        self.neonatal_tetanus_case = neonatal_tetanus_case
        self.neonatal_tetanus_death = neonatal_tetanus_death
        self.meningitis_case = meningitis_case
        self.meningitis_death = meningitis_death
        self.rabies_case = rabies_case
        self.rabies_death = rabies_death
        self.acute_measles_diarrhea_case = acute_measles_diarrhea_case
        self.acute_measles_diarrhea_death = acute_measles_diarrhea_death
        self.other_notifiable_disease_case = other_notifiable_disease_case
        self.other_notifiable_disease_death = other_notifiable_disease_death

    def __str__(self):
        return ugettext("{cscom} / {period} / {receipt}").format(
            cscom=self.entity.display_full_name(),
            period=self.period,
            receipt=self.receipt)

    def fill_blank(self):
        for field in self.data_fields():
            setattr(self, field, 0)

    def as_xls(self):
        file_name = "MADO_{entity}.{day}.{month}.{year}.xls" \
                    .format(entity=self.entity.slug,
                            day=self.period.middle().day,
                            month=self.period.middle().month,
                            year=self.period.middle().year)
        return file_name, epid_activities_as_xls(self)

    def nb_cases_total(self):
        return sum([getattr(self, field, 0)
                    for field in self.case_fields()])

    def nb_deaths_total(self):
        return sum([getattr(self, field, 0)
                    for field in self.death_fields()])

    @classmethod
    def case_fields(cls):
        return [field for field in cls.data_fields()
                if field.endswith('_case')]

    @classmethod
    def death_fields(cls):
        return [field for field in cls.data_fields()
                if field.endswith('_death')]

    @classmethod
    def disease_fields(cls):
        return [field.rsplit('_', 1)[0] for field in cls.data_fields()
                if field.endswith('_case')]

    @classmethod
    def disease_name(cls, disease):
        return cls.DISEASE_NAMES.get(disease)

    def name_cases_deaths(self):
        lines = []
        for disease in self.disease_fields():
            line = [self.disease_name(disease),
                    getattr(self, '{}_case'.format(disease), 0),
                    getattr(self, '{}_death'.format(disease), 0)]
            lines.append(line)
        return lines


@implements_to_string
class EpidemiologyR(AbstractEpidemiologyR):

    RECEIPT_FORMAT = ("MDO-{entity__slug}/"
                      "{period__year_short}{period__month}"
                      "{period__day}-{rand}")
    REPORTING_TYPE = PERIODICAL_SOURCE
    UNIQUE_TOGETHER = [('period', 'entity')]

    class Meta:
        app_label = 'snisi_epidemiology'
        verbose_name = _("Epidemiology Report")
        verbose_name_plural = _("Epidemiology Reports")

receiver(pre_save, sender=EpidemiologyR)(pre_save_report)
receiver(post_save, sender=EpidemiologyR)(post_save_report)

reversion.register(EpidemiologyR)


@implements_to_string
class AggEpidemiologyR(PeriodicAggregatedReportInterface,
                       AbstractEpidemiologyR):

    REPORTING_TYPE = PERIODICAL_AGGREGATED
    RECEIPT_FORMAT = ("AMDO-{entity__slug}/"
                      "{period__year_short}{period__month}"
                      "{period__day}-{rand}")
    INDIVIDUAL_CLS = EpidemiologyR
    UNIQUE_TOGETHER = [('period', 'entity')]

    class Meta:
        app_label = 'snisi_epidemiology'
        verbose_name = _("Aggregated Epidemiology Report")
        verbose_name_plural = _("Aggregated Epidemiology Reports")

    indiv_sources = models.ManyToManyField(
        INDIVIDUAL_CLS, verbose_name=_("Primary. Sources"),
        blank=True, null=True,
        related_name='source_agg_%(class)s_reports')

    @classmethod
    def start(cls, *args, **kwargs):
        return cls.start_report(*args, **kwargs)

receiver(pre_save, sender=AggEpidemiologyR)(pre_save_report)
receiver(post_save, sender=AggEpidemiologyR)(post_save_report)

reversion.register(AggEpidemiologyR)
