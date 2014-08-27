#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

from py3compat import implements_to_string
from django.db import models
from django.utils.translation import ugettext_lazy as _

from snisi_tools.numbers import (operator_from_malinumber,
                                 phonenumber_repr, normalized_phonenumber)


@implements_to_string
class PhoneNumberType(models.Model):

    class Meta:
        app_label = 'snisi_core'
        verbose_name = _("Phone Number Type")
        verbose_name_plural = _("Phone number types")
        ordering = ('name',)

    slug = models.CharField(max_length=75, primary_key=True)
    name = models.CharField(max_length=50)
    abbr = models.CharField(max_length=10)
    priority = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    @classmethod
    def get_or_none(cls, slug):
        try:
            return cls.objects.get(slug=slug)
        except cls.DoesNotExist:
            return None

    @classmethod
    def from_number(cls, number, is_flotte):
        npn = normalized_phonenumber(number)
        operator = operator_from_malinumber(npn)
        slug = 'flotte' if is_flotte else 'perso_{}'.format(operator)
        return cls.get_or_none(slug)


@implements_to_string
class PhoneNumber(models.Model):

    class Meta:
        app_label = 'snisi_core'
        verbose_name = _("Phone Number")
        verbose_name_plural = _("Phone numbers")
        ordering = ('provider', '-priority')

    identity = models.CharField(max_length=75, primary_key=True)
    category = models.ForeignKey(PhoneNumberType)
    priority = models.PositiveIntegerField(default=0)
    provider = models.ForeignKey('Provider', related_name='phone_numbers')

    def __str__(self):
        return "{num}/{typeabbr}".format(num=self.identity_repr(),
                                         typeabbr=self.category.abbr)

    @classmethod
    def get_or_none(cls, identity):
        try:
            return cls.objects.get(identity=identity)
        except cls.DoesNotExist:
            return None

    def identity_repr(self):
        return phonenumber_repr(self.identity)

    @classmethod
    def from_guess(cls, identity, provider):
        operator = operator_from_malinumber(identity)
        category = PhoneNumberType.objects.get(
            slug="perso_{}".format(operator))
        return cls.objects.create(
            identity=identity,
            category=category,
            priority=category.priority,
            provider=provider)

    @classmethod
    def by_identity(cls, identity):
        return cls.objects.get(identity=identity).provider
