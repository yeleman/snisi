#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

from py3compat import implements_to_string
from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext

from snisi_core.models.Providers import Provider


@implements_to_string
class Group(models.Model):

    class Meta:
        app_label = 'snisi_core'
        verbose_name = _("Group")
        verbose_name_plural = _("Groups")

    slug = models.SlugField(primary_key=True)
    name = models.CharField(max_length=250)
    members = models.ManyToManyField(Provider)

    def __str__(self):
        return ugettext("{name}").format(name=self.name)

    @classmethod
    def get_or_none(cls, slug):
        try:
            return cls.objects.get(slug=slug)
        except cls.DoesNotExist:
            return None
