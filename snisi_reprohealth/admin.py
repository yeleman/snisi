#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

from django.contrib import admin

from snisi_core.admin import ReportAdmin
# from snisi_reprohealth.models.MaternalMortality import (MaternalDeathR,
#                                                        AggMaternalDeathR)
# from snisi_reprohealth.models.Commodities import RHProductsR, AggRHProductsR
# from snisi_reprohealth.models.ChildrenMortality import (ChildrenDeathR,
#                                                        AggChildrenDeathR)
from snisi_reprohealth.models.PFActivities import PFActivitiesR

# admin.site.register(MaternalDeathR, ReportAdmin)
# admin.site.register(AggMaternalDeathR, ReportAdmin)
# admin.site.register(ChildrenDeathR, ReportAdmin)
# admin.site.register(AggChildrenDeathR, ReportAdmin)
# admin.site.register(RHProductsR, ReportAdmin)
# admin.site.register(AggRHProductsR, ReportAdmin)
admin.site.register(PFActivitiesR, ReportAdmin)
