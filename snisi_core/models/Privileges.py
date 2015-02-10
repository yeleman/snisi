#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

from py3compat import implements_to_string
from django.db import models
from django.utils.translation import ugettext_lazy as _


@implements_to_string
class Privilege(models.Model):

    """ A named collection of non-exclusive permissions """

    class Meta:
        app_label = 'snisi_core'
        verbose_name = _("Privilege")
        verbose_name_plural = _("Privileges")

    slug = models.SlugField(_("Slug"), max_length=50, primary_key=True)
    name = models.CharField(_("Name"), max_length=100)

    def __str__(self):
        return self.name

    @classmethod
    def get_or_none(cls, slug):
        try:
            return cls.objects.get(slug=slug)
        except cls.DoesNotExist:
            return None


@implements_to_string
class Accreditation(models.Model):

    """ Intermediate table for Privilege and Provider """

    class Meta:
        app_label = 'snisi_core'
        verbose_name = _("Accreditation")
        verbose_name_plural = _("Accreditations")

    privilege = models.ForeignKey(Privilege)
    provider = models.ForeignKey('Provider')
    location = models.ForeignKey('Entity')

    def __str__(self):
        if self.location.level == 0:
            return _("{provider}").format(provider=self.privilege)
        return _("{provider} at {location}").format(
            provider=self.privilege, location=self.location)
