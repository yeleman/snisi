#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

import reversion
from py3compat import implements_to_string
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from django.utils.translation import ugettext_lazy as _, ugettext

from snisi_core.models.common import pre_save_report, post_save_report
from snisi_core.models.Reporting import (SNISIReport,
                                         PeriodicAggregatedReportInterface,
                                         PERIODICAL_SOURCE, PERIODICAL_AGGREGATED)


class AbstractEpidemiologyR(SNISIReport):

    RECEIPT_FORMAT = 'dd'

    class Meta:
        app_label = 'snisi_epidemiology'
        abstract = True

    ebola_case = models.IntegerField(_("Ebola cases"))
    ebola_death = models.IntegerField(_("Ebola death"))

    acute_flaccid_paralysis_case = models.IntegerField(_("AFP cases"))
    acute_flaccid_paralysis_death = models.IntegerField(_("AFP death"))

    influenza_a_h1n1_case = models.IntegerField(_("Influenza A H1N1 cases"))
    influenza_a_h1n1_death = models.IntegerField(_("Influenza A H1N1 death"))

    cholera_case = models.IntegerField(_("Cholera cases"))
    cholera_death = models.IntegerField(_("Cholera death"))

    red_diarrhea_case = models.IntegerField(_("Red Diarrhea cases"))
    red_diarrhea_death = models.IntegerField(_("Red Diarrhea death"))

    measles_case = models.IntegerField(_("Measles cases"))
    measles_death = models.IntegerField(_("Measles death"))

    yellow_fever_case = models.IntegerField(_("Yellow Fever cases"))
    yellow_fever_death = models.IntegerField(_("Yellow Fever death"))

    neonatal_tetanus_case = models.IntegerField(_("NNT cases"))
    neonatal_tetanus_death = models.IntegerField(_("NNT death"))

    meningitis_case = models.IntegerField(_("Meningitis cases"))
    meningitis_death = models.IntegerField(_("Meningitis death"))

    rabies_case = models.IntegerField(_("Rabies cases"))
    rabies_death = models.IntegerField(_("Rabies death"))

    acute_measles_diarrhea_case = models.IntegerField(_("Acute Measles Diarrhea cases"))
    acute_measles_diarrhea_death = models.IntegerField(_("Acute Measles Diarrhea death"))

    other_notifiable_disease_case = models.IntegerField(_("Other Notifiable Diseases cases"))
    other_notifiable_disease_death = models.IntegerField(_("Other Notifiable Diseases death"))

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
        for field in self.to_dict().keys():
            setattr(self, field, 0)


@implements_to_string
class EpidemiologyR(AbstractEpidemiologyR):

    REPORTING_TYPE = PERIODICAL_SOURCE

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
    INDIVIDUAL_CLS = EpidemiologyR
    UNIQUE_TOGETHER = [('period', 'entity'), ]

    class Meta:
        app_label = 'snisi_epidemiology'
        verbose_name = _("Aggregated Epidemiology Report")
        verbose_name_plural = _("Aggregated Epidemiology Reports")

    indiv_sources = models.ManyToManyField(INDIVIDUAL_CLS,
        verbose_name=_(u"Primary. Sources"),
        blank=True, null=True,
        related_name='source_agg_%(class)s_reports')

receiver(pre_save, sender=AggEpidemiologyR)(pre_save_report)
receiver(post_save, sender=AggEpidemiologyR)(post_save_report)

reversion.register(AggEpidemiologyR)
