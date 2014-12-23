#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging

from py3compat import implements_to_string
from django.db import models
from django.utils.translation import ugettext_lazy as _

from snisi_core.models.Entities import Entity
from snisi_core.models.Periods import Period, YearPeriod


logger = logging.getLogger(__name__)


@implements_to_string
class ExpectedCaseload(models.Model):

    DATA_FIELDS = ['u59o6_sam', 'u59_sam',
                   'u59o6_mam', 'u59_mam',
                   'pw_mam',
                   'u59o6_sam_80pc', 'u59_sam_80pc',
                   'u59o6_mam_80pc', 'u59_mam_80pc',
                   'pw_mam_80pc']

    class Meta:
        app_label = 'snisi_nutrition'
        unique_together = [('period', 'entity')]
        verbose_name = _("Expected Caseload")
        verbose_name_plural = _("Expected Caseloads")

    # Related Location
    entity = models.ForeignKey(Entity,
                               related_name='exp_caseloads',
                               null=True, blank=True)

    # Related Location
    period = models.ForeignKey(Period,
                               related_name='exp_caseloads',
                               null=True, blank=True)

    u59o6_sam = models.PositiveIntegerField()
    u59_sam = models.PositiveIntegerField()
    u59o6_mam = models.PositiveIntegerField()
    u59_mam = models.PositiveIntegerField()
    pw_mam = models.PositiveIntegerField()

    u59o6_mam_80pc = models.PositiveIntegerField()
    u59_mam_80pc = models.PositiveIntegerField()
    u59o6_sam_80pc = models.PositiveIntegerField()
    u59_sam_80pc = models.PositiveIntegerField()
    pw_mam_80pc = models.PositiveIntegerField()

    def __str__(self):
        return self.name()

    def name(self):
        return "{entity}/{period}".format(entity=self.entity.slug,
                                          period=self.period)

    @classmethod
    def get_or_none(cls, period, entity):
        try:
            return cls.objects.get(period=period, entity=entity)
        except cls.DoesNotExist:
            return None

    @classmethod
    def get_or_none_from(cls, year, entity_slug):
        period = YearPeriod.find_create_from(year=year)
        entity = Entity.get_or_none(entity_slug)
        if period is None or entity is None:
            return None
        return cls.get_or_none(period=period, entity=entity)

    @classmethod
    def update_or_create(cls, year, entity_slug, **kwargs):

        cload = cls.get_or_none_from(year=year, entity_slug=entity_slug)

        if cload is None:
            period = YearPeriod.find_create_from(year=year)
            entity = Entity.get_or_none(entity_slug)
            if period is None or entity is None:
                return None
            cload = cls(period=period, entity=entity)

        for field in cls.DATA_FIELDS:
            setattr(cload, field, kwargs[field])

        cload.save()

        return cload
