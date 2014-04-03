#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

from django.contrib import admin

from snisi_core.admin import ReportAdmin
from snisi_trachoma.models import (TTBacklogVillageR,
                                   TTBacklogMissionR)

admin.site.register(TTBacklogVillageR, ReportAdmin)
admin.site.register(TTBacklogMissionR, ReportAdmin)
