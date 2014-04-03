#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging

import reversion
from py3compat import implements_to_string
from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext
from django.utils import timezone

from snisi_core.models.common import ActiveManager
from snisi_tools.misc import import_path

logger = logging.getLogger(__name__)


@implements_to_string
class Domain(models.Model):

    """ Represent a field of activity in which we collect data.

        Domain is the base on which code separation is built.
        It is tied to an app: snisi_malaria, snisi_trachoma, etc. """

    class Meta:
        app_label = 'snisi_core'
        verbose_name = _("Domain")
        verbose_name_plural = _("Domains")

    slug = models.CharField(primary_key=True, max_length=75)
    name = models.CharField(max_length=250)
    is_active = models.BooleanField(default=True)
    technical_contact = models.ForeignKey('Provider',
        related_name='projects_as_techcontact', blank=True, null=True)
    operational_contact = models.ForeignKey('Provider',
        related_name='projects_as_opcontact', blank=True, null=True)
    short_description = models.CharField(max_length=250, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    module_path = models.CharField(max_length=200, unique=True)

    objects = models.Manager()
    active = ActiveManager()

    def module(self):
        return import_path(self.module_path)

    def import_from(self, path, failsafe=True):
        return self._module_func(func=path, failsafe=failsafe)

    def _module_func(self, func, failsafe=False):
        return import_path('{module}.{func}'.format(module=self.module_path,
                                                    func=func),
                           failsafe=failsafe)

    def _proxy_to_module(self, func_name, entity, adate, failsafe=False):
        return self._module_func(func_name, failsafe=failsafe)(
            project=self, entity=entity, adate=adate)

    def __str__(self):
        return ugettext("{name}").format(name=self.name)

    @classmethod
    def get_or_none(cls, slug):
        try:
            # we don't want to restrict it to active projects
            # as logic depends on existing project ; not it being active
            return cls.objects.get(slug=slug)
        except cls.DoesNotExist:
            return None


@implements_to_string
class Cluster(models.Model):

    """ Represent a group of Entities engaged in a reporting activity

        Cluster are meant to be specific per activity.
        Ex: C1: Malaria Monthly Routine
            C2: Malaria Monthly Routine via SMS
        Entities might be in several Clusters """

    class Meta:
        app_label = 'snisi_core'
        verbose_name = _("Cluster")
        verbose_name_plural = _("Clusters")

    domain = models.ForeignKey('Domain', blank=True, null=True)
    slug = models.CharField(primary_key=True, max_length=75)
    name = models.CharField(max_length=250)
    is_active = models.BooleanField(default=True)
    contact = models.ForeignKey('Provider',
        related_name='clusters_as_contact', blank=True, null=True)

    objects = models.Manager()
    active = ActiveManager()

    def __str__(self):
        return ugettext("{name}").format(name=self.name)

    def members(self, only_active=True):
        qs = self.participations
        if only_active:
            qs = qs.filter(is_active=True)
        return [p.entity.casted() for p in qs.all()]

    def members_at(self, adate):
        pass

    @classmethod
    def get_or_none(cls, slug):
        try:
            return cls.active.get(slug=slug)
        except cls.DoesNotExist:
            return None


@implements_to_string
class Participation(models.Model):

    """ Participation of an Entity in a Cluster.

        Members of a Cluster (Entities with participations) are expected
        to conduct all activities of the Cluster (usually cluster are very
        activity-centric).
        If for some reason an Entity cannot continue participating, we change
        its participation to inactive.
        Participations are versioned so we get history of participations. """

    class Meta:
        app_label = 'snisi_core'
        verbose_name = _("Participation")
        verbose_name_plural = _("Participations")
        unique_together = [('cluster', 'entity')]

    cluster = models.ForeignKey('Cluster', related_name='participations')
    entity = models.ForeignKey('Entity', related_name='participations')
    is_active = models.BooleanField(default=True)
    modified_on = models.DateTimeField(default=timezone.now)

    objects = models.Manager()
    active = ActiveManager()

    def __str__(self):
        return ugettext("{cluster}/{entity}").format(cluster=self.cluster,
                                                     entity=self.entity)

reversion.register(Participation)
