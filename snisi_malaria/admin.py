#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from snisi_core.admin import ReportAdmin
from snisi_malaria.models import (MalariaR, AggMalariaR,
                                  EpidemioMalariaR, AggEpidemioMalariaR,
                                  WeeklyMalariaR, AggWeeklyMalariaR)


class MalariaRAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'period', 'entity', 'receipt',
                    'validation_status', 'arrival_status')
    list_filter = ('period', 'validation_status', 'arrival_status',
                   'integrity_status', 'completion_status')

    fieldsets = (
        (None, {
            'fields': ('receipt',
                       ('completion_status', 'integrity_status',
                        'arrival_status', 'validation_status'),
                       ('period', 'entity'),
                       ('created_by', 'modified_by'))}),
        (_(u"Under 5"), {
            'fields': (('u5_total_consultation_all_causes',
                        'u5_total_suspected_malaria_cases'),
                       ('u5_total_simple_malaria_cases',
                       'u5_total_severe_malaria_cases'),
                       ('u5_total_tested_malaria_cases',
                        'u5_total_confirmed_malaria_cases',
                        'u5_total_treated_malaria_cases'),
                       ('u5_total_inpatient_all_causes',
                       'u5_total_malaria_inpatient'),
                       ('u5_total_death_all_causes',
                       'u5_total_malaria_death'),
                       'u5_total_distributed_bednets')}),
        (_(u"Over 5"), {
            'fields': (('o5_total_consultation_all_causes',
                        'o5_total_suspected_malaria_cases'),
                       ('o5_total_simple_malaria_cases',
                        'o5_total_severe_malaria_cases'),
                       ('o5_total_tested_malaria_cases',
                        'o5_total_confirmed_malaria_cases',
                        'o5_total_treated_malaria_cases'),
                       ('o5_total_inpatient_all_causes',
                        'o5_total_malaria_inpatient'),
                       ('o5_total_death_all_causes',
                        'o5_total_malaria_death'))
        }),
        (_(u"Pregnant Women"), {
            'fields': (('pw_total_consultation_all_causes',
                        'pw_total_suspected_malaria_cases'),
                       'pw_total_severe_malaria_cases',
                       ('pw_total_tested_malaria_cases',
                        'pw_total_confirmed_malaria_cases',
                        'pw_total_treated_malaria_cases'),
                       ('pw_total_inpatient_all_causes',
                        'pw_total_malaria_inpatient'),
                       ('pw_total_death_all_causes',
                        'pw_total_malaria_death'),
                       'pw_total_distributed_bednets',
                       ('pw_total_anc1', 'pw_total_sp1', 'pw_total_sp2'))
        }),
        (_(u"Stock Outs"), {
            'fields': (('stockout_act_children', 'stockout_act_youth',
                       'stockout_act_adult'),
                       ('stockout_artemether', 'stockout_quinine',
                        'stockout_serum'),
                       ('stockout_bednet', 'stockout_rdt', 'stockout_sp'))}),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj is not None:
            return ('receipt',) + self.readonly_fields
        return self.readonly_fields

admin.site.register(MalariaR, MalariaRAdmin)
admin.site.register(AggMalariaR, ReportAdmin)
admin.site.register(EpidemioMalariaR, ReportAdmin)
admin.site.register(AggEpidemioMalariaR, ReportAdmin)
admin.site.register(WeeklyMalariaR, ReportAdmin)
admin.site.register(AggWeeklyMalariaR, ReportAdmin)
