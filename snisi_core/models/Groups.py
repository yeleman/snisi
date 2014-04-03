#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

from py3compat import implements_to_string
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _, ugettext


@implements_to_string
class SNISIGroup(Group):

    class Meta:
        app_label = 'snisi_core'
        verbose_name = _("Group")
        verbose_name_plural = _("Groups")

    def __str__(self):
        return ugettext("{name}").format(name=self.name)

    @classmethod
    def get_or_none(cls, name):
        try:
            return cls.objects.get(name=name)
        except cls.DoesNotExist:
            return None
