#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging

from py3compat import implements_to_string
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _, ugettext

logger = logging.getLogger(__name__)


@implements_to_string
class PeriodicTask(models.Model):

    """ Records whether an action has been executed or not """

    class Meta:
        app_label = 'snisi_core'
        verbose_name = _("Periodic Task")
        verbose_name_plural = _("Periodic Tasks")

    slug = models.CharField(max_length=255, unique=True)
    created_on = models.DateTimeField("created", default=timezone.now)
    category = models.CharField(max_length=300, null=True, blank=True)
    triggered = models.BooleanField(default=False)
    triggered_on = models.DateTimeField("triggered on", null=True, blank=True)

    def __str__(self):
        return ugettext("{}{}").format(self.slug, "/*"
                                       if self.triggered else "")

    def can_trigger(self):
        return not self.triggered

    @classmethod
    def get_or_none(cls, slug):
        try:
            return cls.objects.get(slug=slug)
        except cls.DoesNotExist:
            return None

    @classmethod
    def get_or_create(cls, slug, category=None):
        return cls.objects.get_or_create(slug=slug,
                                         category=category)

    @classmethod
    def can_trigger_with(cls, slug, category=None):
        task, created = cls.get_or_create(slug, category)
        if created:
            return True
        return task.can_trigger()

    def trigger(self):
        if not self.can_trigger():
            return False
        self.triggered = True
        self.triggered_on = timezone.now()
        self.save()
        return True

    # debug only
    def untrigger(self):
        if not self.triggered:
            return False
        self.triggered = False
        self.triggered_on = None
        self.save()
        return True
