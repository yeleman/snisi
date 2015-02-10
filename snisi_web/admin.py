#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

from django.contrib import admin

from snisi_core.models.Reporting import (SNISIReport,
                                         ReportClass,
                                         ExpectedReporting,
                                         ExpectedValidation)
from snisi_core.models.Periods import Period
from snisi_core.models.SMSMessages import SMSMessage
from snisi_core.models.Notifications import Notification
from snisi_core.admin import (EntityAdmin, EntityTypeAdmin, PeriodAdmin,
                              PhoneNumberAdmin,
                              PhoneNumberTypeAdmin, RoleAdmin, ProviderAdmin,
                              SNISIReportAdmin, ExpectedReportingAdmin,
                              ExpectedValidationAdmin, SMSMessageAdmin,
                              NotificationAdmin)
from snisi_core.models.Roles import Role
from snisi_core.models.Providers import Provider
from snisi_core.models.Numbers import PhoneNumber, PhoneNumberType
from snisi_core.models.Entities import (HealthEntity, EntityType,
                                        AdministrativeEntity, Entity)
from snisi_core.models.Projects import Domain, Cluster, Participation
from snisi_core.models.Groups import Group
from snisi_core.models.Privileges import Privilege, Accreditation
from snisi_core.models.PeriodicTasks import PeriodicTask

admin.site.register(Provider, ProviderAdmin)
admin.site.register(PhoneNumber, PhoneNumberAdmin)
admin.site.register(PhoneNumberType, PhoneNumberTypeAdmin)
admin.site.register(Period, PeriodAdmin)
admin.site.register(Entity, EntityAdmin)
admin.site.register(HealthEntity, EntityAdmin)
admin.site.register(AdministrativeEntity, EntityAdmin)
admin.site.register(EntityType, EntityTypeAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(ReportClass)
admin.site.register(ExpectedReporting, ExpectedReportingAdmin)
admin.site.register(ExpectedValidation, ExpectedValidationAdmin)
admin.site.register(SNISIReport, SNISIReportAdmin)
admin.site.register(SMSMessage, SMSMessageAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(Domain)
admin.site.register(Cluster)
admin.site.register(Group)
admin.site.register(Participation)
admin.site.register(PeriodicTask)
admin.site.register(Privilege)
admin.site.register(Accreditation)
