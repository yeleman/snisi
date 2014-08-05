#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

from django import template
from django.template.defaultfilters import stringfilter

from snisi_epidemiology.models import AbstractEpidemiologyR

register = template.Library()


@register.filter(name='epidemio_field_name')
@stringfilter
def epidemio_field_name(field):
    return AbstractEpidemiologyR.disease_name(field)
