#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import inspect

import reversion
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from snisi_core.models.Entities import EntityType
from snisi_core.models.common import (
    pre_save_report, pre_save_report_incomplete,
    post_save_report, generate_receipt)
from snisi_core.models.Reporting import (SNISIReport,
                                         PeriodicAggregatedReportInterface,
                                         ExpectedReporting,
                                         PERIODICAL_SOURCE,
                                         PERIODICAL_AGGREGATED)
from snisi_malaria.xls_export import malaria_monthly_routine_as_xls


class MalariaRIface(object):

    @property
    def total_consultation_all_causes(self):
        return self.total_for_field(inspect.stack()[0][3])

    @property
    def total_suspected_malaria_cases(self):
        return self.total_for_field(inspect.stack()[0][3])

    @property
    def total_simple_malaria_cases(self):
        # no value for pregnant_women
        return self.u5_total_simple_malaria_cases \
            + self.o5_total_simple_malaria_cases

    @property
    def total_severe_malaria_cases(self):
        return self.total_for_field(inspect.stack()[0][3])

    @property
    def total_tested_malaria_cases(self):
        return self.total_for_field(inspect.stack()[0][3])

    @property
    def total_confirmed_malaria_cases(self):
        return self.total_for_field(inspect.stack()[0][3])

    @property
    def total_treated_malaria_cases(self):
        return self.total_for_field(inspect.stack()[0][3])

    @property
    def total_inpatient_all_causes(self):
        return self.total_for_field(inspect.stack()[0][3])

    @property
    def total_malaria_inpatient(self):
        return self.total_for_field(inspect.stack()[0][3])

    @property
    def total_death_all_causes(self):
        return self.total_for_field(inspect.stack()[0][3])

    @property
    def total_malaria_death(self):
        return self.total_for_field(inspect.stack()[0][3])

    @property
    def total_anc1(self):
        return self.total_for_field(inspect.stack()[0][3])

    @property
    def total_sp1(self):
        return self.total_for_field(inspect.stack()[0][3])

    @property
    def total_sp2(self):
        return self.total_for_field(inspect.stack()[0][3])

    def total_for_field(self, field):
        values = []
        for cat in ('u5', 'o5', 'pw'):
            fname = '%s_%s' % (cat, field)
            if hasattr(self, fname):
                values.append(getattr(self, fname))
        return sum(values)

    @classmethod
    def start(cls, *args, **kwargs):
        """ creates a report object with meta data only. Object not saved """
        now = timezone.now()
        bootstrap = cls if not cls.is_aggregated() else cls.start_aggregated
        report = bootstrap(
            period=kwargs.get('period'),
            entity=kwargs.get('entity'),
            created_by=kwargs.get('created_by'),
            modified_by=kwargs.get('created_by'),
            completion_status=cls.COMPLETE,
            completed_on=now,
            integrity_status=cls.CORRECT,
            arrival_status=cls.LATE,
            validation_status=cls.NOT_VALIDATED)

        for arg, value in kwargs.items():
            try:
                setattr(report, arg, value)
            except AttributeError:
                pass

        return report

    def get_expected_reportings(self, with_source=True, with_agg=True):
        erl = []
        if with_source:
            if self.entity.type.slug == 'health_district':
                erl += ExpectedReporting.objects.filter(
                    report_class=self.report_class(for_source=True),
                    period=self.period,
                    entity__slug__in=[e.slug for e in
                                      self.entity.get_health_centers()])
        if with_agg:
            erl += ExpectedReporting.objects.filter(
                report_class=self.report_class(for_source=False),
                period=self.period,
                entity__slug__in=[e.slug for e in self.entity.all_children()])
        return list(set(erl))

    def add_underfive_data(self, total_consultation_all_causes,
                           total_suspected_malaria_cases,
                           total_simple_malaria_cases,
                           total_severe_malaria_cases,
                           total_tested_malaria_cases,
                           total_confirmed_malaria_cases,
                           total_treated_malaria_cases,
                           total_inpatient_all_causes,
                           total_malaria_inpatient,
                           total_death_all_causes,
                           total_malaria_death,
                           total_distributed_bednets):
        self.u5_total_consultation_all_causes = total_consultation_all_causes
        self.u5_total_suspected_malaria_cases = total_suspected_malaria_cases
        self.u5_total_simple_malaria_cases = total_simple_malaria_cases
        self.u5_total_severe_malaria_cases = total_severe_malaria_cases
        self.u5_total_tested_malaria_cases = total_tested_malaria_cases
        self.u5_total_confirmed_malaria_cases = total_confirmed_malaria_cases
        self.u5_total_treated_malaria_cases = total_treated_malaria_cases
        self.u5_total_inpatient_all_causes = total_inpatient_all_causes
        self.u5_total_malaria_inpatient = total_malaria_inpatient
        self.u5_total_death_all_causes = total_death_all_causes
        self.u5_total_malaria_death = total_malaria_death
        self.u5_total_distributed_bednets = total_distributed_bednets

    def add_overfive_data(self, total_consultation_all_causes,
                          total_suspected_malaria_cases,
                          total_simple_malaria_cases,
                          total_severe_malaria_cases,
                          total_tested_malaria_cases,
                          total_confirmed_malaria_cases,
                          total_treated_malaria_cases,
                          total_inpatient_all_causes,
                          total_malaria_inpatient,
                          total_death_all_causes,
                          total_malaria_death):
        self.o5_total_consultation_all_causes = total_consultation_all_causes
        self.o5_total_suspected_malaria_cases = total_suspected_malaria_cases
        self.o5_total_simple_malaria_cases = total_simple_malaria_cases
        self.o5_total_severe_malaria_cases = total_severe_malaria_cases
        self.o5_total_tested_malaria_cases = total_tested_malaria_cases
        self.o5_total_confirmed_malaria_cases = total_confirmed_malaria_cases
        self.o5_total_treated_malaria_cases = total_treated_malaria_cases
        self.o5_total_inpatient_all_causes = total_inpatient_all_causes
        self.o5_total_malaria_inpatient = total_malaria_inpatient
        self.o5_total_death_all_causes = total_death_all_causes
        self.o5_total_malaria_death = total_malaria_death

    def add_pregnantwomen_data(self, total_consultation_all_causes,
                               total_suspected_malaria_cases,
                               total_severe_malaria_cases,
                               total_tested_malaria_cases,
                               total_confirmed_malaria_cases,
                               total_treated_malaria_cases,
                               total_inpatient_all_causes,
                               total_malaria_inpatient,
                               total_death_all_causes,
                               total_malaria_death,
                               total_distributed_bednets,
                               total_anc1,
                               total_sp1,
                               total_sp2):
        self.pw_total_consultation_all_causes = total_consultation_all_causes
        self.pw_total_suspected_malaria_cases = total_suspected_malaria_cases
        self.pw_total_severe_malaria_cases = total_severe_malaria_cases
        self.pw_total_tested_malaria_cases = total_tested_malaria_cases
        self.pw_total_confirmed_malaria_cases = total_confirmed_malaria_cases
        self.pw_total_treated_malaria_cases = total_treated_malaria_cases
        self.pw_total_inpatient_all_causes = total_inpatient_all_causes
        self.pw_total_malaria_inpatient = total_malaria_inpatient
        self.pw_total_death_all_causes = total_death_all_causes
        self.pw_total_malaria_death = total_malaria_death
        self.pw_total_distributed_bednets = total_distributed_bednets
        self.pw_total_anc1 = total_anc1
        self.pw_total_sp1 = total_sp1
        self.pw_total_sp2 = total_sp2

    def add_stockout_data(self, stockout_act_children,
                          stockout_act_youth,
                          stockout_act_adult,
                          stockout_artemether,
                          stockout_quinine,
                          stockout_serum,
                          stockout_bednet,
                          stockout_rdt,
                          stockout_sp):
        self.stockout_act_children = stockout_act_children
        self.stockout_act_youth = stockout_act_youth
        self.stockout_act_adult = stockout_act_adult
        self.stockout_artemether = stockout_artemether
        self.stockout_quinine = stockout_quinine
        self.stockout_serum = stockout_serum
        self.stockout_bednet = stockout_bednet
        self.stockout_rdt = stockout_rdt
        self.stockout_sp = stockout_sp

    @classmethod
    def data_fields(cls):
        fields = []
        for field in cls._meta.get_all_field_names():
            try:
                if field.split('_')[0] in ('u5', 'o5', 'pw', 'stockout'):
                    fields.append(field)
            except:
                continue
        return fields

    @classmethod
    def generate_receipt(cls, instance):
        """ generates a reversable text receipt for a MalariaR

        FORMAT:
            RR000/sss-111-D
            RR: region code on two letters
            000: internal report ID
            sss: entity slug
            111: sent day in year
            D: sent day of week """

        DOW = ['D', 'L', 'M', 'E', 'J', 'V', 'S']
        region_type = EntityType.objects.get(slug='region')

        def region_id(slug):
            return slug.upper()[0:2]

        region = 'ML'
        for ent in instance.entity.get_ancestors().reverse():
            if ent.type == region_type:
                region = region_id(ent.slug)
                break
        receipt = '%(region)s%(id)d/%(entity)s-%(day)s-%(dow)s' \
                  % {'day': instance.created_on.strftime('%j'),
                     'dow': DOW[int(instance.created_on.strftime('%w'))],
                     'entity': instance.entity.slug,
                     'id': instance.__class__.objects.count(),
                     'period': instance.period.id,
                     'region': region}
        return receipt

    def as_xls(self):
        file_name = "PNLP_{entity}s.{month}.{year}.xls" \
                    .format(entity=self.entity.slug,
                            month=self.period.middle().month,
                            year=self.period.middle().year)
        return file_name, malaria_monthly_routine_as_xls(self)


class MalariaR(MalariaRIface, SNISIReport):

    REPORTING_TYPE = PERIODICAL_SOURCE
    RECEIPT_FORMAT = None  # using custom generate_receipt
    UNIQUE_TOGETHER = [('period', 'entity')]
    INTEGRITY_CHECKER = 'snisi_malaria.integrity.MalariaRIntegrityChecker'

    YES = 'Y'
    NO = 'N'
    YESNO = {
        YES: _("Yes"),
        NO: _("No")
    }

    class Meta:
        app_label = 'snisi_malaria'
        verbose_name = _("Malaria Report")
        verbose_name_plural = _("Malaria Reports")

    u5_total_consultation_all_causes = models.PositiveIntegerField(
        _("Total Consultation All Causes"))
    u5_total_suspected_malaria_cases = models.PositiveIntegerField(
        _("Total Suspected Malaria Cases"))
    u5_total_simple_malaria_cases = models.PositiveIntegerField(
        _("Total Simple Malaria Cases"))
    u5_total_severe_malaria_cases = models.PositiveIntegerField(
        _("Total Severe Malaria Cases"))
    u5_total_tested_malaria_cases = models.PositiveIntegerField(
        _("Total Tested Malaria Cases"))
    u5_total_confirmed_malaria_cases = models.PositiveIntegerField(
        _("Total Confirmed Malaria Cases"))
    u5_total_treated_malaria_cases = models.PositiveIntegerField(
        _("Total Treated Malaria Cases"))
    u5_total_inpatient_all_causes = models.PositiveIntegerField(
        _("Total Inpatient All Causes"))
    u5_total_malaria_inpatient = models.PositiveIntegerField(
        _("Total Malaria Inpatient"))
    u5_total_death_all_causes = models.PositiveIntegerField(
        _("Total Death All Causes"))
    u5_total_malaria_death = models.PositiveIntegerField(
        _("Total Malaria Death"))
    u5_total_distributed_bednets = models.PositiveIntegerField(
        _("Total Distributed Bednets"))

    o5_total_consultation_all_causes = models.PositiveIntegerField(
        _("Total Consultation All Causes"))
    o5_total_suspected_malaria_cases = models.PositiveIntegerField(
        _("Total Suspected Malaria Cases"))
    o5_total_simple_malaria_cases = models.PositiveIntegerField(
        _("Total Simple Malaria Cases"))
    o5_total_severe_malaria_cases = models.PositiveIntegerField(
        _("Total Severe Malaria Cases"))
    o5_total_tested_malaria_cases = models.PositiveIntegerField(
        _("Total Tested Malaria Cases"))
    o5_total_confirmed_malaria_cases = models.PositiveIntegerField(
        _("Total Confirmed Malaria Cases"))
    o5_total_treated_malaria_cases = models.PositiveIntegerField(
        _("Total Treated Malaria Cases"))
    o5_total_inpatient_all_causes = models.PositiveIntegerField(
        _("Total Inpatient All Causes"))
    o5_total_malaria_inpatient = models.PositiveIntegerField(
        _("Total Malaria Inpatient"))
    o5_total_death_all_causes = models.PositiveIntegerField(
        _("Total Death All Causes"))
    o5_total_malaria_death = models.PositiveIntegerField(
        _("Total Malaria Death"))

    pw_total_consultation_all_causes = models.PositiveIntegerField(
        _("Total Consultation All Causes"))
    pw_total_suspected_malaria_cases = models.PositiveIntegerField(
        _("Total Suspected Malaria Cases"))
    pw_total_severe_malaria_cases = models.PositiveIntegerField(
        _("Total Severe Malaria Cases"))
    pw_total_tested_malaria_cases = models.PositiveIntegerField(
        _("Total Tested Malaria Cases"))
    pw_total_confirmed_malaria_cases = models.PositiveIntegerField(
        _("Total Confirmed Malaria Cases"))
    pw_total_treated_malaria_cases = models.PositiveIntegerField(
        _("Total Treated Malaria Cases"))
    pw_total_inpatient_all_causes = models.PositiveIntegerField(
        _("Total Inpatient All Causes"))
    pw_total_malaria_inpatient = models.PositiveIntegerField(
        _("Total Malaria Inpatient"))
    pw_total_death_all_causes = models.PositiveIntegerField(
        _("Total Death All Causes"))
    pw_total_malaria_death = models.PositiveIntegerField(
        _("Total Malaria Death"))
    pw_total_distributed_bednets = models.PositiveIntegerField(
        _("Total Distributed Bednets"))
    pw_total_anc1 = models.PositiveIntegerField(
        _("Total ANC1 Visits"))
    pw_total_sp1 = models.PositiveIntegerField(
        _("Total SP1 given"))
    pw_total_sp2 = models.PositiveIntegerField(
        _("Total SP2 given"))

    stockout_act_children = models.CharField(_("ACT Children"),
                                             max_length=1,
                                             choices=YESNO.items())
    stockout_act_youth = models.CharField(_("ACT Youth"),
                                          max_length=1,
                                          choices=YESNO.items())
    stockout_act_adult = models.CharField(_("ACT Adult"),
                                          max_length=1,
                                          choices=YESNO.items())
    stockout_artemether = models.CharField(_("Artemether"),
                                           max_length=1,
                                           choices=YESNO.items())
    stockout_quinine = models.CharField(_("Quinine"),
                                        max_length=1,
                                        choices=YESNO.items())
    stockout_serum = models.CharField(_("Serum"), max_length=1,
                                      choices=YESNO.items())
    stockout_bednet = models.CharField(_("Bednets"),
                                       max_length=1,
                                       choices=YESNO.items())
    stockout_rdt = models.CharField(_("RDTs"), max_length=1,
                                    choices=YESNO.items())
    stockout_sp = models.CharField(_("SPs"), max_length=1,
                                   choices=YESNO.items())

    def __str__(self):
        return "MalariaR object"

    def fill_blank(self):
        self.add_underfive_data(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        self.add_overfive_data(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        self.add_pregnantwomen_data(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        self.add_stockout_data(self.NO, self.NO, self.NO, self.NO, self.NO,
                               self.NO, self.NO, self.NO, self.NO)

    @classmethod
    def create_aggregated(cls, period, entity, created_by, *args, **kwargs):
        agg_report = cls.start(period=period,
                               entity=entity,
                               created_by=created_by,
                               *args, **kwargs)

        sources = MalariaR.validated.filter(period=period,
                                            entity__in=entity.get_children())

        if sources.count() == 0:
            agg_report.fill_blank()
            agg_report.save()

        for report in sources:
            for key, value in report.to_dict().items():
                pv = getattr(agg_report, key)
                if not pv:
                    nv = value
                elif pv in (cls.YES, cls.NO):
                    if pv == cls.YES:
                        nv = pv
                    else:
                        nv = value
                else:
                    nv = pv + value
                setattr(agg_report, key, nv)
            agg_report.save()

        for report in sources:
            agg_report.sources.add(report)

        with reversion.create_revision():
            agg_report.save()
            reversion.set_user(created_by)

        return agg_report

receiver(pre_save, sender=MalariaR)(pre_save_report)
receiver(post_save, sender=MalariaR)(post_save_report)
reversion.register(MalariaR, follow=['snisireport_ptr'])


class AggMalariaR(MalariaRIface,
                  PeriodicAggregatedReportInterface, SNISIReport):

    REPORTING_TYPE = PERIODICAL_AGGREGATED
    INDIVIDUAL_CLS = MalariaR
    RECEIPT_FORMAT = None  # using custom generate_receipt
    UNIQUE_TOGETHER = [('period', 'entity')]

    class Meta:
        app_label = 'snisi_malaria'
        verbose_name = _("Aggregated Malaria Report")
        verbose_name_plural = _("Aggregated Malaria Reports")

    u5_total_consultation_all_causes = models.PositiveIntegerField(
        _("Total Consultation All Causes"))
    u5_total_suspected_malaria_cases = models.PositiveIntegerField(
        _("Total Suspected Malaria Cases"))
    u5_total_simple_malaria_cases = models.PositiveIntegerField(
        _("Total Simple Malaria Cases"))
    u5_total_severe_malaria_cases = models.PositiveIntegerField(
        _("Total Severe Malaria Cases"))
    u5_total_tested_malaria_cases = models.PositiveIntegerField(
        _("Total Tested Malaria Cases"))
    u5_total_confirmed_malaria_cases = models.PositiveIntegerField(
        _("Total Confirmed Malaria Cases"))
    u5_total_treated_malaria_cases = models.PositiveIntegerField(
        _("Total Treated Malaria Cases"))
    u5_total_inpatient_all_causes = models.PositiveIntegerField(
        _("Total Inpatient All Causes"))
    u5_total_malaria_inpatient = models.PositiveIntegerField(
        _("Total Malaria Inpatient"))
    u5_total_death_all_causes = models.PositiveIntegerField(
        _("Total Death All Causes"))
    u5_total_malaria_death = models.PositiveIntegerField(
        _("Total Malaria Death"))
    u5_total_distributed_bednets = models.PositiveIntegerField(
        _("Total Distributed Bednets"))

    o5_total_consultation_all_causes = models.PositiveIntegerField(
        _("Total Consultation All Causes"))
    o5_total_suspected_malaria_cases = models.PositiveIntegerField(
        _("Total Suspected Malaria Cases"))
    o5_total_simple_malaria_cases = models.PositiveIntegerField(
        _("Total Simple Malaria Cases"))
    o5_total_severe_malaria_cases = models.PositiveIntegerField(
        _("Total Severe Malaria Cases"))
    o5_total_tested_malaria_cases = models.PositiveIntegerField(
        _("Total Tested Malaria Cases"))
    o5_total_confirmed_malaria_cases = models.PositiveIntegerField(
        _("Total Confirmed Malaria Cases"))
    o5_total_treated_malaria_cases = models.PositiveIntegerField(
        _("Total Treated Malaria Cases"))
    o5_total_inpatient_all_causes = models.PositiveIntegerField(
        _("Total Inpatient All Causes"))
    o5_total_malaria_inpatient = models.PositiveIntegerField(
        _("Total Malaria Inpatient"))
    o5_total_death_all_causes = models.PositiveIntegerField(
        _("Total Death All Causes"))
    o5_total_malaria_death = models.PositiveIntegerField(
        _("Total Malaria Death"))

    pw_total_consultation_all_causes = models.PositiveIntegerField(
        _("Total Consultation All Causes"))
    pw_total_suspected_malaria_cases = models.PositiveIntegerField(
        _("Total Suspected Malaria Cases"))
    pw_total_severe_malaria_cases = models.PositiveIntegerField(
        _("Total Severe Malaria Cases"))
    pw_total_tested_malaria_cases = models.PositiveIntegerField(
        _("Total Tested Malaria Cases"))
    pw_total_confirmed_malaria_cases = models.PositiveIntegerField(
        _("Total Confirmed Malaria Cases"))
    pw_total_treated_malaria_cases = models.PositiveIntegerField(
        _("Total Treated Malaria Cases"))
    pw_total_inpatient_all_causes = models.PositiveIntegerField(
        _("Total Inpatient All Causes"))
    pw_total_malaria_inpatient = models.PositiveIntegerField(
        _("Total Malaria Inpatient"))
    pw_total_death_all_causes = models.PositiveIntegerField(
        _("Total Death All Causes"))
    pw_total_malaria_death = models.PositiveIntegerField(
        _("Total Malaria Death"))
    pw_total_distributed_bednets = models.PositiveIntegerField(
        _("Total Distributed Bednets"))
    pw_total_anc1 = models.PositiveIntegerField(_("Total ANC1 Visits"))
    pw_total_sp1 = models.PositiveIntegerField(_("Total SP1 given"))
    pw_total_sp2 = models.PositiveIntegerField(_("Total SP2 given"))

    stockout_act_children = models.PositiveIntegerField(_("ACT Children"))
    stockout_act_youth = models.PositiveIntegerField(_("ACT Youth"))
    stockout_act_adult = models.PositiveIntegerField(_("ACT Adult"))
    stockout_artemether = models.PositiveIntegerField(_("Artemether"))
    stockout_quinine = models.PositiveIntegerField(_("Quinine"))
    stockout_serum = models.PositiveIntegerField(_("Serum"))
    stockout_bednet = models.PositiveIntegerField(_("Bednets"))
    stockout_rdt = models.PositiveIntegerField(_("RDTs"))
    stockout_sp = models.PositiveIntegerField(_("SPs"))

    # all source reports (CSCOM)
    indiv_sources = models.ManyToManyField(
        INDIVIDUAL_CLS,
        verbose_name=_("Primary. Sources (all)"),
        blank=True, null=True,
        related_name='source_agg_%(class)s_reports',
        symmetrical=False)

    direct_indiv_sources = models.ManyToManyField(
        INDIVIDUAL_CLS,
        verbose_name=_("Primary. Sources (direct)"),
        blank=True, null=True,
        related_name='direct_source_agg_%(class)s_reports',
        symmetrical=False)

    @classmethod
    def create_from(cls, period, entity, created_by,
                    indiv_sources=None, agg_sources=None):
        if indiv_sources is None and entity.type.slug == 'health_district':
            indiv_sources = cls.INDIVIDUAL_CLS \
                               .objects \
                               .filter(period=period,
                                       entity__in=entity.get_health_centers())
        return super(AggMalariaR, cls).create_from(period=period,
                                                   entity=entity,
                                                   created_by=created_by,
                                                   indiv_sources=indiv_sources,
                                                   agg_sources=agg_sources)

    def fill_blank(self, **kwargs):
        self.add_underfive_data(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        self.add_overfive_data(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        self.add_pregnantwomen_data(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        self.add_stockout_data(0, 0, 0, 0, 0, 0, 0, 0, 0)
        self.set_reporting_status_fields(**kwargs)

    @classmethod
    def update_instance_with_indiv(cls, report, instance):
        for field in instance.data_fields():

            if field.startswith('stockout'):
                if getattr(instance, field) == instance.YES:
                    setattr(report, field, getattr(report, field, 0) + 1)
            else:
                setattr(report, field,
                        (getattr(report, field, 0) or 0)
                        + (getattr(instance, field, 0) or 0))

    @classmethod
    def update_instance_with_agg(cls, report, instance):
        for field in cls.data_fields():
            setattr(report, field,
                    (getattr(report, field, 0) or 0)
                    + (getattr(instance, field, 0) or 0))


receiver(pre_save, sender=AggMalariaR)(pre_save_report)
receiver(post_save, sender=AggMalariaR)(post_save_report)

reversion.register(AggMalariaR, follow=['snisireport_ptr'])


class EpidemioMalariaRIFace(models.Model):

    class Meta:
        abstract = True

    u5_total_consultation_all_causes = models.PositiveIntegerField(
        _("Total Consultation All Causes"), default=0)
    u5_total_suspected_malaria_cases = models.PositiveIntegerField(
        _("Total Suspected Malaria Cases"), default=0)
    u5_total_rdt_tested_malaria_cases = models.PositiveIntegerField(
        _("Total RDT Tested Malaria Cases"), default=0)
    u5_total_rdt_confirmed_malaria_cases = models.PositiveIntegerField(
        _("Total RDT Confirmed Malaria Cases"), default=0)
    u5_total_rdt_pfalciparum_malaria_cases = models.PositiveIntegerField(
        _("Total RDT Confirmed P.Falciparum Malaria Cases"), default=0)
    u5_total_ts_tested_malaria_cases = models.PositiveIntegerField(
        _("Total TS Tested Malaria Cases"), default=0)
    u5_total_ts_confirmed_malaria_cases = models.PositiveIntegerField(
        _("Total TS Confirmed Malaria Cases"), default=0)
    u5_total_ts_pfalciparum_malaria_cases = models.PositiveIntegerField(
        _("Total TS Confirmed P.Falciparum Malaria Cases"), default=0)
    u5_total_simple_malaria_cases = models.PositiveIntegerField(
        _("Total Simple Malaria Cases"), default=0)
    u5_total_severe_malaria_cases = models.PositiveIntegerField(
        _("Total Severe Malaria Cases"), default=0)
    u5_total_death_all_causes = models.PositiveIntegerField(
        _("Total Death All Causes"), default=0)
    u5_total_malaria_death = models.PositiveIntegerField(
        _("Total Malaria Death"), default=0)

    o5_total_consultation_all_causes = models.PositiveIntegerField(
        _("Total Consultation All Causes"), default=0)
    o5_total_suspected_malaria_cases = models.PositiveIntegerField(
        _("Total Suspected Malaria Cases"), default=0)
    o5_total_rdt_tested_malaria_cases = models.PositiveIntegerField(
        _("Total RDT Tested Malaria Cases"), default=0)
    o5_total_rdt_confirmed_malaria_cases = models.PositiveIntegerField(
        _("Total RDT Confirmed Malaria Cases"), default=0)
    o5_total_rdt_pfalciparum_malaria_cases = models.PositiveIntegerField(
        _("Total RDT Confirmed P.Falciparum Malaria Cases"), default=0)
    o5_total_ts_tested_malaria_cases = models.PositiveIntegerField(
        _("Total TS Tested Malaria Cases"), default=0)
    o5_total_ts_confirmed_malaria_cases = models.PositiveIntegerField(
        _("Total TS Confirmed Malaria Cases"), default=0)
    o5_total_ts_pfalciparum_malaria_cases = models.PositiveIntegerField(
        _("Total TS Confirmed P.Falciparum Malaria Cases"), default=0)
    o5_total_simple_malaria_cases = models.PositiveIntegerField(
        _("Total Simple Malaria Cases"), default=0)
    o5_total_severe_malaria_cases = models.PositiveIntegerField(
        _("Total Severe Malaria Cases"), default=0)
    o5_total_death_all_causes = models.PositiveIntegerField(
        _("Total Death All Causes"), default=0)
    o5_total_malaria_death = models.PositiveIntegerField(
        _("Total Malaria Death"), default=0)

    pw_total_consultation_all_causes = models.PositiveIntegerField(
        _("Total Consultation All Causes"), default=0)
    pw_total_suspected_malaria_cases = models.PositiveIntegerField(
        _("Total Suspected Malaria Cases"), default=0)
    pw_total_rdt_tested_malaria_cases = models.PositiveIntegerField(
        _("Total RDT Tested Malaria Cases"), default=0)
    pw_total_rdt_confirmed_malaria_cases = models.PositiveIntegerField(
        _("Total RDT Confirmed Malaria Cases"), default=0)
    pw_total_rdt_pfalciparum_malaria_cases = models.PositiveIntegerField(
        _("Total RDT Confirmed P.Falciparum Malaria Cases"), default=0)
    pw_total_ts_tested_malaria_cases = models.PositiveIntegerField(
        _("Total TS Tested Malaria Cases"), default=0)
    pw_total_ts_confirmed_malaria_cases = models.PositiveIntegerField(
        _("Total TS Confirmed Malaria Cases"), default=0)
    pw_total_ts_pfalciparum_malaria_cases = models.PositiveIntegerField(
        _("Total TS Confirmed P.Falciparum Malaria Cases"), default=0)
    pw_total_simple_malaria_cases = models.PositiveIntegerField(
        _("Total Simple Malaria Cases"), default=0)
    pw_total_severe_malaria_cases = models.PositiveIntegerField(
        _("Total Severe Malaria Cases"), default=0)
    pw_total_death_all_causes = models.PositiveIntegerField(
        _("Total Death All Causes"), default=0)
    pw_total_malaria_death = models.PositiveIntegerField(
        _("Total Malaria Death"), default=0)

    def __str__(self):
        return self.receipt

    def fill_blank(self, **kwargs):
        for field in self.data_fields():
            setattr(self, field, 0)
        if hasattr(self, 'set_reporting_status_fields'):
            self.set_reporting_status_fields(**kwargs)

    def total_for_field(self, field):
        values = []
        for cat in ('u5', 'o5', 'pw'):
            fname = '%s_%s' % (cat, field)
            if hasattr(self, fname):
                values.append(getattr(self, fname))
        return sum(values)

    @property
    def agnostic_total_confirmed_malaria_cases(self, age_group):
        return sum([getattr(self, '{}_total_{}_confirmed_malaria_cases'
                                  .format(age_group, method), 0)
                    for method in ('rdt', 'ts')])

    @property
    def u5_total_confirmed_malaria_cases(self):
        return self.agnostic_total_confirmed_malaria_cases('u5')

    @property
    def o5_total_confirmed_malaria_cases(self):
        return self.agnostic_total_confirmed_malaria_cases('o5')

    @property
    def pw_total_confirmed_malaria_cases(self):
        return self.agnostic_total_confirmed_malaria_cases('pw')

    @property
    def total_consultation_all_causes(self):
        return self.total_for_field(inspect.stack()[0][3])

    @property
    def total_suspected_malaria_cases(self):
        return self.total_for_field(inspect.stack()[0][3])

    @property
    def total_rdt_tested_malaria_cases(self):
        return self.total_for_field(inspect.stack()[0][3])

    @property
    def total_rdt_confirmed_malaria_cases(self):
        return self.total_for_field(inspect.stack()[0][3])

    @property
    def total_rdt_pfalciparum_malaria_cases(self):
        return self.total_for_field(inspect.stack()[0][3])

    @property
    def total_ts_tested_malaria_cases(self):
        return self.total_for_field(inspect.stack()[0][3])

    @property
    def total_ts_confirmed_malaria_cases(self):
        return self.total_for_field(inspect.stack()[0][3])

    @property
    def total_ts_pfalciparum_malaria_cases(self):
        return self.total_for_field(inspect.stack()[0][3])

    @property
    def total_simple_malaria_cases(self):
        # no value for pregnant_women
        return self.u5_total_simple_malaria_cases \
            + self.o5_total_simple_malaria_cases

    @property
    def total_severe_malaria_cases(self):
        return self.total_for_field(inspect.stack()[0][3])

    @property
    def total_tested_malaria_cases(self):
        return self.total_for_field(inspect.stack()[0][3])

    @property
    def total_confirmed_malaria_cases(self):
        return self.total_for_field(inspect.stack()[0][3])

    @property
    def total_treated_malaria_cases(self):
        return self.total_for_field(inspect.stack()[0][3])

    @property
    def total_inpatient_all_causes(self):
        return self.total_for_field(inspect.stack()[0][3])

    @property
    def total_malaria_inpatient(self):
        return self.total_for_field(inspect.stack()[0][3])

    @property
    def total_death_all_causes(self):
        return self.total_for_field(inspect.stack()[0][3])

    @property
    def total_malaria_death(self):
        return self.total_for_field(inspect.stack()[0][3])

    @property
    def total_anc1(self):
        return self.total_for_field(inspect.stack()[0][3])

    @property
    def total_sp1(self):
        return self.total_for_field(inspect.stack()[0][3])

    @property
    def total_sp2(self):
        return self.total_for_field(inspect.stack()[0][3])


class EpidemioMalariaR(EpidemioMalariaRIFace, SNISIReport):

    RECEIPT_FORMAT = ("EPI-{entity__slug}/"
                      "{period__year_short}{period__month}"
                      "{period__day}-{rand}")
    REPORTING_TYPE = PERIODICAL_SOURCE
    UNIQUE_TOGETHER = [('period', 'entity')]

    class Meta:
        app_label = 'snisi_malaria'
        verbose_name = _("Epidemiology Malaria Report")
        verbose_name_plural = _("Epidemology Malaria Reports")

receiver(pre_save, sender=EpidemioMalariaR)(pre_save_report)
receiver(post_save, sender=EpidemioMalariaR)(post_save_report)

reversion.register(EpidemioMalariaR, follow=['snisireport_ptr'])


class AggEpidemioMalariaR(EpidemioMalariaRIFace,
                          PeriodicAggregatedReportInterface, SNISIReport):

    RECEIPT_FORMAT = None
    INDIVIDUAL_CLS = EpidemioMalariaR
    REPORTING_TYPE = PERIODICAL_AGGREGATED
    UNIQUE_TOGETHER = [('period', 'entity')]

    class Meta:
        app_label = 'snisi_malaria'
        verbose_name = _("Aggregated Epidemiology Malaria Report")
        verbose_name_plural = _("Aggregated Epidemology Malaria Reports")

    # all source reports (CSCOM)
    indiv_sources = models.ManyToManyField(
        INDIVIDUAL_CLS,
        verbose_name=_("Primary. Sources (all)"),
        blank=True, null=True,
        related_name='source_agg_%(class)s_reports')

    direct_indiv_sources = models.ManyToManyField(
        INDIVIDUAL_CLS,
        verbose_name=_("Primary. Sources (direct)"),
        blank=True, null=True,
        related_name='direct_source_agg_%(class)s_reports')

    @classmethod
    def create_from(cls, period, entity, created_by,
                    indiv_sources=None, agg_sources=None):

        # indiv_sources are from Health Centers during DayPeriods
        # aggregated are created either at HC level for other periods
        # or at higher levels on any periods.

        # Aggregated are thus sourced by indiv reports
        # only if at HC (any periods) or at District.

        # from snisi_core.models.Periods import DayPeriod

        if indiv_sources is None:
            if entity.type.slug in ('health_center', 'health_district'):
                indiv_sources = cls.INDIVIDUAL_CLS.objects \
                                   .filter(period__start_on__gte=period.start_on,
                                           period__end_on__lte=period.end_on) \
                                   .filter(entity__in=entity.get_health_centers())

        if agg_sources is None and not len(indiv_sources):
            agg_sources = cls.objects \
                             .filter(period__start_on__gte=period.start_on,
                                     period__end_on__lte=period.end_on) \
                             .filter(entity__in=entity.get_natural_children(skip_slugs=['health_area']))

        return super(AggEpidemioMalariaR, cls).create_from(
            period=period,
            entity=entity,
            created_by=created_by,
            indiv_sources=indiv_sources,
            agg_sources=agg_sources)

    @classmethod
    def start_aggreagted(cls, *args, **kwargs):
        rfdict = {}
        for field in ('completion_ok', 'integrity_ok',
                      'arrival_ok', 'auto_validate'):
            if field in kwargs:
                rfdict.update({field: kwargs.get(field)})
                del kwargs[field]
        report = cls.start_report(*args, **kwargs)
        report.fill_blank()

        # only agg
        if hasattr(report, 'set_reporting_status_fields'):
            report.set_reporting_status_fields(**rfdict)
        if hasattr(report, 'update_expected_reportings_number'):
            report.update_expected_reportings_number()
        return report

    @classmethod
    def generate_receipt(cls, instance):

        fwp_num = getattr(instance.period.casted(), 'FIXED_WEEK_NUM', None)

        extra_field = {
            'week_part': "S{}".format(fwp_num) if fwp_num else ""
        }
        receipt_format = ("AEPI-{entity__slug}/"
                          "{period__year_short}{period__month}"
                          "{week_part}-{rand}")
        return generate_receipt(
            instance=instance,
            receipt_format=receipt_format, **extra_field)

receiver(pre_save, sender=AggEpidemioMalariaR)(pre_save_report_incomplete)
receiver(post_save, sender=AggEpidemioMalariaR)(post_save_report)

reversion.register(AggEpidemioMalariaR, follow=['snisireport_ptr'])
