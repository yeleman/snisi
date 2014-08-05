#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging

import reversion
from py3compat import implements_to_string, string_types, text_type
from django.db import models
from django.db.models.query import QuerySet
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from snisi_core.models.common import (pre_save_report_incomplete,
                                      post_save_report)
from snisi_core.models.Providers import Provider
from snisi_core.models.Entities import Entity
from snisi_core.models.Periods import Period
from snisi_core.models.common import (generate_receipt,
                                      create_periodic_agg_report_from)
from snisi_core.models.Roles import Role
from snisi_tools.misc import (import_path, DictDiffer, class_str,
                              get_uuid, short_class_str)
from snisi_core.xls_export import default_xls_export

logger = logging.getLogger(__name__)

PERIODICAL_SOURCE = 'periosrc'
PERIODICAL_AGGREGATED = 'perioagg'
OCCASIONAL_SOURCE = 'occasiosrc'
OCCASIONAL_AGGREGATED = 'occasioagg'
REPORTING_TYPES = {PERIODICAL_SOURCE: _("Periodical Source"),
                   PERIODICAL_AGGREGATED: _("Periodical Aggregated"),
                   OCCASIONAL_SOURCE: _("Occasional Source"),
                   OCCASIONAL_AGGREGATED: _("Occasional Aggregated")}


class SuperMixin(object):

    @classmethod
    def cls_super(cls, method):
        def fail(cls, *args, **kwargs):
            return None
        try:
            return getattr(cls.__mro__[cls.index(cls.__mro__)], method, fail)
        except:
            return fail


def get_autobot():
    return Provider.get_or_none('autobot')


class InterestingFieldsMixin(object):

    @classmethod
    def interesting_fields(cls):
        def exclude(field):
            return field.attname in ('id',) \
                or field.attname.endswith('ptr_id')
        return [f.name for f in cls._meta.concrete_fields if not exclude(f)]


class ReportStatusMixin(object):
    def validated(self):
        return self.filter(validation_status=SNISIReport.VALIDATED)

    def not_validated(self):
        return self.filter(validation_status=SNISIReport.NOT_VALIDATED)

    def refused(self):
        return self.filter(validation_status=SNISIReport.REFUSED)

    def ontime(self):
        return self.filter(arrival_status=SNISIReport.ON_TIME)

    def late(self):
        return self.filter(arrival_status=SNISIReport.LATE)

    def incorrect(self):
        return self.filter(integrity_status=SNISIReport.INCORRECT)

    def correct(self):
        return self.filter(integrity_status=SNISIReport.CORRECT)

    def incomplete(self):
        return self.filter(completion_status=SNISIReport.INCOMPLETE)

    def complete(self):
        return self.filter(completion_status=SNISIReport.COMPLETE)


class ReportStatusQuerySet(QuerySet, ReportStatusMixin):
    pass


class ReportStatusManager(models.Manager, ReportStatusMixin):
    def get_query_set(self):
        return ReportStatusQuerySet(self.model, using=self._db)


@implements_to_string
class SNISIReport(SuperMixin, InterestingFieldsMixin, models.Model):

    # Completion Status
    COMPLETE = 'complete'
    INCOMPLETE = 'incomplete'
    COMPLETION_STATUSES = {
        COMPLETE: _("Complete"),
        INCOMPLETE: _("Incomplete")
    }

    # Integrity Status
    NOT_CHECKED = 'not_checked'
    INCORRECT = 'incorrect'
    CORRECT = 'correct'
    INTEGRITY_STATUSES = {
        NOT_CHECKED: _("Not Checked"),
        INCORRECT: _("Incorrect"),
        CORRECT: _("Correct")
    }

    # Promptitude
    ON_TIME = 'arrived_on_time'
    LATE = 'arrived_late'
    NOT_APPLICABLE = 'not_applicable'
    ARRIVAL_STATUSES = {
        ON_TIME: _("Arrived On Time"),
        LATE: _("Arrived Late"),
        NOT_APPLICABLE: _("N/A")
    }

    # Validation
    NOT_VALIDATED = 'not_validated'
    VALIDATED = 'validated'
    REFUSED = 'refused'
    VALIDATION_STATUSES = {
        NOT_VALIDATED: _("Not Validated"),
        VALIDATED: _("Validated"),
        REFUSED: _("Refused"),
        NOT_APPLICABLE: _("N/a")
    }

    ###
    # INTERFACE
    ###
    REPORTING_TYPE = None
    RECEIPT_FORMAT = "__{uuid}__"
    UNIQUE_TOGETHER = None
    INTEGRITY_CHECKER = None

    class Meta:
        app_label = 'snisi_core'

    # Reports might get deleted/recreated so a custom PK will insure
    # that FK are accurate.
    uuid = models.CharField(max_length=200, primary_key=True, default=get_uuid)

    # Unique receipt for the report. Never altered after post_save
    receipt = models.CharField(max_length=200, unique=True)

    # Provider who created report. never altered.
    created_by = models.ForeignKey(Provider,
                                   related_name='%(app_label)s_'
                                                '%(class)s_reports',
                                   verbose_name=_("Created By"))
    # date of creation. Never altered.
    created_on = models.DateTimeField(default=timezone.now,
                                      verbose_name=_("Created On"))

    # last Provider who edited report. Initialized with created_by
    modified_by = models.ForeignKey(Provider,
                                    null=True, blank=True,
                                    verbose_name=_("Modified By"),
                                    related_name='own_modified_reports')
    # last time report was edited. Initialized with created_on
    modified_on = models.DateTimeField(default=timezone.now,
                                       verbose_name=_("Modified On"))
    # Completion State.
    completion_status = models.CharField(max_length=40,
                                         choices=COMPLETION_STATUSES.items(),
                                         default=INCOMPLETE)
    completed_on = models.DateTimeField(null=True, blank=True)
    # Integrity State: wheter data are correct or not (!= validation)
    integrity_status = models.CharField(max_length=40,
                                        choices=INTEGRITY_STATUSES.items(),
                                        default=NOT_CHECKED)
    # Promptitude State. Shouldn't be altered
    arrival_status = models.CharField(max_length=40,
                                      choices=ARRIVAL_STATUSES.items(),
                                      default=NOT_APPLICABLE)
    # Validation State
    validation_status = models.CharField(max_length=40,
                                         choices=VALIDATION_STATUSES.items(),
                                         default=NOT_APPLICABLE)
    validated_on = models.DateTimeField(null=True, blank=True)
    validated_by = models.ForeignKey(Provider,
                                     null=True, blank=True,
                                     verbose_name=_("Validated By"),
                                     related_name='own_validated_reports')
    auto_validated = models.BooleanField(default=False)

    # Related Location
    entity = models.ForeignKey(Entity,
                               related_name='%(app_label)s_'
                                            '%(class)s_reports',
                               null=True, blank=True)

    # Related Location
    period = models.ForeignKey(Period,
                               related_name='%(app_label)s_'
                                            '%(class)s_reports',
                               null=True, blank=True)

    report_cls = models.CharField(max_length=512, blank=True, null=True)

    # django manager first
    objects = ReportStatusManager()
    statuses = ReportStatusManager()
    django = models.Manager()

    def __str__(self):
        return "{receipt}".format(receipt=self.receipt)

    def casted(self):
        try:
            cls = import_path(self.report_cls)
        except (IndexError, AttributeError, ImportError):
            cls = self.__class__
        return cls.objects.get(receipt=self.receipt)

    def cast(self, cls):
        return cls.objects.get(receipt=self.receipt)

    def save(self, *args, **kwargs):
        # record Class Path in report_cls to ease casting
        if self.report_cls is None:
            self.report_cls = class_str(self.__class__)

        if self.UNIQUE_TOGETHER is not None:
            # from django's models.base.py
            unique_checks = []
            unique_togethers = [(self.__class__, self.UNIQUE_TOGETHER)]
            for parent_class in self._meta.parents.keys():
                if parent_class._meta.unique_together:
                    unique_togethers.append((
                        parent_class,
                        parent_class._meta.unique_together))

            for model_class, unique_together in unique_togethers:
                for check in unique_together:
                    unique_checks.append((model_class, tuple(check)))
            errors = self._perform_unique_checks(unique_checks)
            if errors:
                raise ValidationError(errors)
        return super(SNISIReport, self).save(*args, **kwargs)

    @classmethod
    def create(cls, *args, **kwargs):
        return cls.django.create(*args, **args)

    def as_form(self, cls_only=False):
        from django import forms

        class SNISIReportForm(forms.ModelForm):
            class Meta:
                model = self.casted().__class__
        if cls_only:
            return SNISIReportForm
        return SNISIReportForm(instance=self)

    @classmethod
    def start_report(cls, *args, **kwargs):
        report = cls(*args, **kwargs)
        report.fill_blank()
        return report

    @classmethod
    def start(cls, *args, **kwargs):
        return cls.start_report(*args, **kwargs)

    def to_dict(self):
        return {field: self.get(field)
                for field in self.data_fields()
                + self.meta_fields() + self.meta_agg_fields()}

    @classmethod
    def version_dict(cls, version):
        return {field: version.field_dict.get(field, None)
                for field in cls.data_fields()
                + cls.meta_fields() + cls.meta_agg_fields()}

    def get(self, slug):
        return getattr(self, slug)

    @classmethod
    def field_name(cls, slug):
        field = cls._meta.get_field(slug)
        vn = field.verbose_name
        if not isinstance(vn, string_types):
            vn = vn.encode('utf-8')
        if vn:
            return vn
        return field.name

    @classmethod
    def data_fields(cls):
        metas = cls.meta_fields() + cls.meta_agg_fields()
        return [field for field in cls.interesting_fields()
                if field not in metas]

    def data_dict(self):
        return {field: getattr(self, field, None)
                for field in self.data_fields()}

    @classmethod
    def version_data_dict(cls, version):
        return {field: version.field_dict.get(field, None)
                for field in cls.data_fields()}

    @classmethod
    def meta_fields(cls):
        return SNISIReport.interesting_fields()

    @classmethod
    def meta_agg_fields(cls):
        return []

    def fill_blank(self):
        pass

    @classmethod
    def generate_receipt(cls, instance):
        return generate_receipt(instance)

    def casted_period(self, period_cls):
        cp = self.period
        cp.__class__ = period_cls
        return cp

    def casted_entity(self, entity_cls):
        ce = self.entity
        ce.__class__ = entity_cls
        return ce

    def record_validation(self,
                          validated=True,
                          validated_by=None,
                          validated_on=None,
                          auto_validated=True):
        self.validation_status = self.VALIDATED \
            if validated else self.NOT_VALIDATED
        self.validated_on = validated_on \
            if validated_on is not None else timezone.now()
        self.validated_by = validated_by
        self.auto_validated = auto_validated
        with reversion.create_revision():
            self.save()
            reversion.set_user(validated_by)

    @property
    def verbose_arrival_status(self):
        return text_type(self.ARRIVAL_STATUSES.get(self.arrival_status))

    @property
    def verbose_validation_status(self):
        return text_type(self.VALIDATION_STATUSES.get(self.validation_status))

    @property
    def verbose_completion_status(self):
        return text_type(self.COMPLETION_STATUSES.get(self.completion_status))

    @property
    def verbose_integrity_status(self):
        return text_type(self.INTEGRITY_STATUSES.get(self.integrity_status))

    @property
    def validated(self):
        return self.validation_status == self.VALIDATED

    @property
    def on_time(self):
        return self.arrival_status == self.ON_TIME

    @property
    def complete(self):
        return self.completion_status == self.COMPLETE

    def versions(self):
        return list(reversion.get_unique_for_object(self))

    def history(self, only_data=True):
        report_data = None
        updates = []
        for version in self.versions():
            if report_data is None:
                if only_data:
                    report_data = self.data_dict()
                else:
                    report_data = self.to_dict()

            if only_data:
                new_version = self.version_data_dict(version)
            else:
                new_version = self.version_dict(version)
            version_update = {field: new_version.get(field)
                              for field
                              in DictDiffer(new_version,
                                            report_data).changed()}
            if len(version_update):
                updates.append(version_update)
        return updates

    def diff(self, only_data=True):
        versions = self.versions()
        if not len(versions) > 1:
            return {}
        version = versions[-1]
        if only_data:
            report_data = self.data_dict()
            last_version = self.version_data_dict(version)
        else:
            report_data = self.to_dict()
            last_version = self.version_dict(version)

        return {field: last_version.get(field)
                for field in DictDiffer(last_version, report_data).changed()}

    def difflog(self, only_data=True):
        return {field: {'original': original_value,
                        'current': getattr(self, field)}
                for field, original_value
                in self.diff(only_data=only_data).items()}

    def altered(self, only_data=True):
        return len(self.history(only_data=only_data))

    def report_class(self, for_source=False):
        if for_source and hasattr(self, 'INDIVIDUAL_CLS'):
            cls = class_str(self.INDIVIDUAL_CLS)
            rtype = self.INDIVIDUAL_CLS.REPORTING_TYPE
        else:
            cls = class_str(self)
            rtype = self.REPORTING_TYPE
        try:
            return ReportClass.objects.get(cls=cls, report_type=rtype)
        except:
            return None

    def get_expected_reportings(self, with_source=True, with_agg=True):
        erl = []
        if with_source:
            erl += ExpectedReporting.objects.filter(
                report_class=self.report_class(for_source=True),
                period=self.period,
                entity__slug__in=[
                    e.slug for e in self.entity.get_descendants_of(
                        include_self=True)])
        if with_agg:
            erl += ExpectedReporting.objects.filter(
                report_class=self.report_class(for_source=False),
                period=self.period,
                entity__slug=self.entity.slug)
        return list(set(erl))

    @classmethod
    def get_or_none(cls, receipt):
        try:
            return cls.objects.get(receipt=receipt).casted()
        except cls.DoesNotExist:
            return None

    def report_type_name(self):
        try:
            rc = ReportClass.objects.get(cls=self.report_cls,
                                         report_type=self.REPORTING_TYPE)
        except:
            return short_class_str(self.report_cls)
        return rc.name

    def as_xls(self):
        return default_xls_export(self)

    @classmethod
    def is_aggregated(cls):
        return cls.REPORTING_TYPE in (PERIODICAL_AGGREGATED,
                                      OCCASIONAL_AGGREGATED)

# we need to ensure non-handled reports gets created with a correct receipt
receiver(pre_save, sender=SNISIReport)(pre_save_report_incomplete)
receiver(post_save, sender=SNISIReport)(post_save_report)

reversion.register(SNISIReport)


class PeriodicAggregatedReportInterface(models.Model):

    class Meta:
        abstract = True

    INDIVIDUAL_CLS = None

    PERIODIC_AGG_MIXIN_FIELDS = ['nb_source_reports_expected',
                                 'nb_source_reports_arrived',
                                 'nb_source_reports_arrived_on_time',
                                 'nb_source_reports_arrived_correct',
                                 'nb_source_reports_arrived_complete',
                                 'nb_source_reports_altered',
                                 'nb_source_reports_validated',
                                 'nb_source_reports_auto_validated',
                                 'nb_agg_reports_altered',
                                 'nb_agg_reports_validated',
                                 'nb_agg_reports_auto_validated']

    # all agg reports engaged (district, region)
    agg_sources = models.ManyToManyField(
        'self',
        verbose_name=_("Aggr. Sources (all)"),
        blank=True, null=True,
        related_name='aggregated_agg_%(class)s_reports',
        symmetrical=False)

    # only those who were used to build this numbers (region)
    direct_agg_sources = models.ManyToManyField(
        'self',
        verbose_name=_("Aggr. Sources (direct)"),
        blank=True, null=True,
        related_name='direct_aggregated_agg_%(class)s_reports',
        symmetrical=False)

    nb_source_reports_expected = models.PositiveIntegerField(
        blank=True, null=True)
    nb_source_reports_arrived = models.PositiveIntegerField(
        blank=True, null=True)
    nb_source_reports_arrived_on_time = models.PositiveIntegerField(
        blank=True, null=True)
    nb_source_reports_arrived_correct = models.PositiveIntegerField(
        blank=True, null=True)
    nb_source_reports_arrived_complete = models.PositiveIntegerField(
        blank=True, null=True)

    nb_source_reports_altered = models.PositiveIntegerField(
        blank=True, null=True)
    nb_source_reports_validated = models.PositiveIntegerField(
        blank=True, null=True)
    nb_source_reports_auto_validated = models.PositiveIntegerField(
        blank=True, null=True)

    nb_agg_reports_altered = models.PositiveIntegerField(
        blank=True, null=True)
    nb_agg_reports_validated = models.PositiveIntegerField(
        blank=True, null=True)
    nb_agg_reports_auto_validated = models.PositiveIntegerField(
        blank=True, null=True)

    def sources(self):
        return self.indiv_sources.all() + self.agg_sources.all()

    def direct_sources(self):
        return self.direct_indiv_sources.all() + self.direct_agg_sources.all()

    @classmethod
    def update_sources_lists_from(cls, report, instance,
                                  instance_is_agg=False):
        report = report.casted()
        instance = instance.casted()

        if not report.receipt:
            report.save()

        if not instance_is_agg:
            # this instance is direct so it goes to both
            report.indiv_sources.add(instance)
            report.direct_indiv_sources.add(instance)
        else:
            # this agg instance should be in both
            report.agg_sources.add(instance)
            report.direct_agg_sources.add(instance)

            # instance's sources need to be fetch
            for indirect_instance in instance.indiv_sources.all():
                if indirect_instance not in report.indiv_sources.all():
                    report.indiv_sources.add(indirect_instance)

            for indirect_instance in instance.agg_sources.all():
                if indirect_instance not in report.agg_sources.all():
                    report.agg_sources.add(indirect_instance)

    @classmethod
    def update_instance_with_indiv_meta(cls, report, instance):
        def _update(field):
            setattr(report, field, getattr(report, field, 0) + 1)

        for field in cls.PERIODIC_AGG_MIXIN_FIELDS:
            if getattr(report, field) is None:
                setattr(report, field, 0)

        _update('nb_source_reports_arrived')

        if instance.arrival_status == instance.ON_TIME:
            _update('nb_source_reports_arrived_on_time')

        if instance.integrity_status == instance.CORRECT:
            _update('nb_source_reports_arrived_correct')

        if instance.completion_status == instance.COMPLETE:
            _update('nb_source_reports_arrived_complete')

        if instance.altered():
            _update('nb_source_reports_altered')

        if instance.validation_status == instance.VALIDATED:
            _update('nb_source_reports_validated')

        if instance.auto_validated:
            _update('nb_source_reports_auto_validated')

        # fill the sources lists
        cls.update_sources_lists_from(report=report, instance=instance,
                                      instance_is_agg=False)

    @classmethod
    def update_instance_with_agg_meta(cls, report, instance):

        def _update(field):
            setattr(report, field, getattr(report, field, 0) + 1)

        for field in cls.meta_agg_fields():
            setattr(report, field,
                    (getattr(report, field, 0) or 0)
                    + (getattr(instance, field, 0) or 0))

        if instance.altered():
            _update('nb_agg_reports_altered')

        if instance.validation_status == instance.VALIDATED:
            _update('nb_agg_reports_validated')

        if instance.auto_validated:
            _update('nb_agg_reports_auto_validated')

        # fill the sources lists
        cls.update_sources_lists_from(report=report, instance=instance,
                                      instance_is_agg=True)

    @classmethod
    def meta_agg_fields(cls):
        return cls.PERIODIC_AGG_MIXIN_FIELDS

    @classmethod
    def update_instance_with_indiv(cls, report, instance):
        for field in instance.data_fields():
                setattr(report, field,
                        (getattr(report, field, 0) or 0)
                        + (getattr(instance, field, 0) or 0))

    @classmethod
    def update_instance_with_agg(cls, report, instance):
        for field in cls.data_fields():
            setattr(report, field,
                    (getattr(report, field, 0) or 0)
                    + (getattr(instance, field, 0) or 0))

    @classmethod
    def create_from(cls, period, entity, created_by,
                    indiv_sources=None, agg_sources=None):
        return create_periodic_agg_report_from(
            cls, period=period, entity=entity,
            created_by=created_by, indiv_cls=cls.INDIVIDUAL_CLS,
            indiv_sources=indiv_sources,
            agg_sources=agg_sources)

    @classmethod
    def start(cls, *args, **kwargs):
        return cls.start_aggreagted(*args, **kwargs)

    @classmethod
    def start_aggregated(cls, *args, **kwargs):
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

    def update_expected_reportings_number(self):
        self.nb_source_reports_expected = \
            len(self.get_expected_reportings(with_source=True, with_agg=False))

    def set_reporting_status_fields(self,
                                    completion_ok=True,
                                    integrity_ok=True,
                                    arrival_ok=True,
                                    auto_validate=False):
        autobot = get_autobot()
        self.created_by = autobot
        self.created_on = timezone.now()
        self.modified_by = autobot
        self.modified_on = timezone.now()
        if completion_ok:
            self.completion_status = self.COMPLETE
            self.completed_on = timezone.now()
        if integrity_ok:
            self.integrity_status = self.CORRECT
        if arrival_ok:
            self.arrival_status = self.ON_TIME
        if auto_validate:
            self.validation_status = self.VALIDATED
            self.validated_on = timezone.now()
            self.validated_by = autobot
            self.auto_validated = True


@implements_to_string
class ReportClass(models.Model):

    class Meta:
        app_label = 'snisi_core'
        verbose_name = _("Report Class")
        verbose_name_plural = _("Report Classes")
        unique_together = [('cls', 'period_cls', 'report_type')]

    slug = models.SlugField(_("Slug"), max_length=75, primary_key=True)
    name = models.CharField(_("Name"), max_length=150)
    cls = models.CharField(_("cls"), max_length=75)
    period_cls = models.CharField(_("Period Type"), max_length=75)
    report_type = models.CharField(max_length=30,
                                   choices=REPORTING_TYPES.items())

    def __str__(self):
        return self.name

    @classmethod
    def get_or_none(cls, slug):
        try:
            return cls.objects.get(slug=slug)
        except cls.DoesNotExist:
            return None

    @property
    def period_class(self):
        if '.' not in self.period_cls:
            period_cls = 'snisi_core.models.Periods.{}'.format(self.period_cls)
        else:
            period_cls = self.period_cls
        return import_path(period_cls)

    @property
    def report_class(self):
        if '.' not in self.cls:
            cls = 'snisi_core.models.{}'.format(self.cls)
        else:
            cls = self.cls
        return import_path(cls)

    @property
    def is_individual(self):
        return self.report_type == self.INDIVIDUAL

    def casted_period(self, period):
        period.cast(self.period_class)
        return period

    def casted_report(self, report):
        return report.casted(self.report_class)


@implements_to_string
class ExpectedReporting(models.Model):

    PERIODICAL_SOURCE = PERIODICAL_SOURCE
    PERIODICAL_AGGREGATED = PERIODICAL_AGGREGATED
    OCCASIONAL_SOURCE = OCCASIONAL_SOURCE
    OCCASIONAL_AGGREGATED = OCCASIONAL_AGGREGATED

    class Meta:
        app_label = 'snisi_core'
        verbose_name = _("Expected Report")
        verbose_name_plural = _("Expected Reports")

    EXPECTED_SINGLE = 'single'
    EXPECTED_ONEPLUS = 'single_or_more'
    EXPECTED_ZEROPLUS = 'zero_or_more'
    EXPECTED_MULTIPLE = 'multiple'

    COMPLETION_COMPLETE = 'satisfied'
    COMPLETION_MATCHING = 'matching'
    COMPLETION_MISSING = 'missing'

    REPORTING_NUMBERS = {
        EXPECTED_SINGLE: _("Single"),  # 0: missing, 1: complete
        EXPECTED_ONEPLUS: _("1+"),  # 0: missing, 1: matching, 2: matching
        EXPECTED_ZEROPLUS: _("0+"),  # 0: matching, 1: matching
        EXPECTED_MULTIPLE: _("Multiple")  # 0: missing, 1: missing, 2: matching
    }

    REPORTING_COMPLETION = {
        COMPLETION_COMPLETE: _("Complete"),
        COMPLETION_MATCHING: _("Matching"),
        COMPLETION_MISSING: _("Missing")
    }

    report_class = models.ForeignKey(ReportClass)
    reporting_role = models.ForeignKey(Role, blank=True, null=True)
    period = models.ForeignKey(Period, related_name='expr_for_period')
    within_period = models.BooleanField()
    entity = models.ForeignKey(Entity)
    within_entity = models.BooleanField(default=False)
    reporting_period = models.ForeignKey(
        Period, related_name='expr_for_reporting_period',
        blank=True, null=True)
    extended_reporting_period = models.ForeignKey(
        Period, related_name='expr_for_ext_reporting_period',
        blank=True, null=True)
    amount_expected = models.CharField(max_length=30,
                                       choices=REPORTING_NUMBERS.items())
    completion_status = models.CharField(max_length=30,
                                         choices=REPORTING_COMPLETION.items())
    arrived_reports = models.ManyToManyField(
        'SNISIReport', blank=True, null=True,
        related_name='expected_reportings')
    updated_on = models.DateTimeField(default=timezone.now)

    def clone(self, save=False, **kwargs):
        fields = ['report_class', 'reporting_role',
                  'period', 'within_period',
                  'entity', 'within_entity',
                  'reporting_period',
                  'extended_reporting_period',
                  'amount_expected',
                  'completion_status']
        exp = self.__class__()
        for field in fields:
            setattr(exp, field, getattr(self, field))
        for field, value in kwargs.items():
            setattr(exp, field, value)
        if save:
            exp.save()
        return exp

    def __str__(self):
        return ("{entity}{within_entity}-{period}{within_period}-{rclass}"
                .format(entity=self.entity.slug,
                        within_entity="*" if self.within_entity else "",
                        period=self.report_class.casted_period(self.period),
                        within_period="*" if self.within_period else "",
                        rclass=self.report_class))

    @property
    def satisfied(self):
        return self.completion_status == self.COMPLETION_COMPLETE

    @property
    def satisfying(self):
        return self.completion_status != self.COMPLETION_MISSING

    @classmethod
    def get_or_none(cls, *args, **kwargs):
        try:
            return cls.objects.get(*args, **kwargs)
        except cls.DoesNotExist:
            return None

    def _arrived_reports(self):
        # cold reload of arrived reports.
        # should use signals instead
        return []

    def arrived_report(self):
        if not self.satisfied:
            return None
        if self.amount_expected == self.EXPECTED_SINGLE:
            return self.arrived_reports.get().casted()
        return None

    def nb_arrived_reports(self):
        return len(self.arrived_reports.all())

    def _completion_status(self):
        nb_reports = self.nb_arrived_reports()
        if self.amount_expected == self.EXPECTED_SINGLE:
            # 0: missing
            # 1: complete
            if nb_reports >= 1:
                return self.COMPLETION_COMPLETE
            else:
                return self.COMPLETION_MISSING
        elif self.amount_expected == self.EXPECTED_ONEPLUS:
            # 0: missing
            # 1: matching
            # 2: matching
            if nb_reports == 0:
                return self.COMPLETION_MISSING
            else:
                return self.COMPLETION_MATCHING
        elif self.amount_expected == self.EXPECTED_ZEROPLUS:
            # 0: matching
            # 1: matching
            return self.COMPLETION_MATCHING
        else:
            # 0: missing
            # 1: missing
            # 2: matching
            if nb_reports < 2:
                return self.COMPLETION_MISSING
            else:
                return self.COMPLETION_MATCHING

    def _report_matchs(self, report):
        # check report class
        if not isinstance(report, self.report_class.report_class):
            return False
        # check reporting type
        if report.REPORTING_TYPE != self.report_class.report_type:
            return False
        # check period
        if not self.within_period and report.period != self.period:
            return False
        # check period if a within one
        if self.within_period \
            and (report.period.start_on < self.period.start_on
                 or report.period.end_on > self.period.end_on):
            return False
        # check entity
        if not self.within_entity and report.entity.casted() \
                != self.entity.casted():
            return False
        # check entity if a within
        if self.within_entity and report.entity.casted() \
                not in self.entity.get_descendants_of(include_self=True):
            return False

        return True

    def acknowledge_report(self, report):
        if not self._report_matchs(report):
            return False
        self.arrived_reports.add(report)
        self.completion_status = self._completion_status()
        self.updated_on = timezone.now()
        self.save()
        return True


@implements_to_string
class ExpectedValidation(models.Model):

    class Meta:
        app_label = 'snisi_core'
        verbose_name = _("Expected Validation")
        verbose_name_plural = _("Expected Validations")

    report = models.ForeignKey(SNISIReport, primary_key=True,
                               related_name='expected_validations')
    validation_period = models.ForeignKey(Period)  # from 1st to 5th.
    validating_entity = models.ForeignKey(Entity)  # CSCOM, District, Region
    validating_role = models.ForeignKey(Role)  # charge SIS, DTC,
    validated_on = models.DateTimeField(blank=True, null=True)
    satisfied = models.BooleanField(default=False)

    def __str__(self):
        return str(self.report)

    def acknowledge_validation(self,
                               validated=True,
                               validated_by=None,
                               validated_on=None,
                               auto_validated=True):

        self.report.record_validation(validated=validated,
                                      validated_by=validated_by,
                                      validated_on=validated_on,
                                      auto_validated=auto_validated)

        # mark this one complete
        self.satisfied = True
        self.validated_on = validated_on
        self.save()
        return True
