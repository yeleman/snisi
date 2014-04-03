#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

from py3compat import implements_to_string
from django.db import models
from django.utils.translation import ugettext_lazy as _


@implements_to_string
class Role(models.Model):

    """ A named collection of Permission (not tied to django.auth) """

    class Meta:
        app_label = 'snisi_core'
        verbose_name = _("Role")
        verbose_name_plural = _("Roles")

    slug = models.SlugField(_("Slug"), max_length=15, primary_key=True)
    name = models.CharField(_("Name"), max_length=50)

    def __str__(self):
        return self.name

    @classmethod
    def get_or_none(cls, slug):
        try:
            return cls.objects.get(slug=slug)
        except cls.DoesNotExist:
            return None
