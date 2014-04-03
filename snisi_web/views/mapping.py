#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from snisi_core.models.Periods import MonthPeriod


@login_required
def webmap(request, reportcls_slug):
    context = {'page_slug': 'map'}

    context.update({'periods': MonthPeriod.objects.all()})

    return render(request, 'map.html', context)
