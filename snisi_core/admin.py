#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from snisi_core.models.Providers import Provider


class EntityAdmin(admin.ModelAdmin):

    list_display = ('slug', 'name', 'type', 'parent', 'parent_level')
    list_filter = ('type',)
    ordering = ('slug',)
    search_fields = ('slug', 'name')


class EntityTypeAdmin(admin.ModelAdmin):
    pass


class PeriodAdmin(admin.ModelAdmin):
    list_filter = ('period_type',)


class MonthPeriodAdmin(admin.ModelAdmin):
    pass


class YearPeriodAdmin(admin.ModelAdmin):
    pass


class ReportAdmin(admin.ModelAdmin):
    pass


class RoleAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'slug', 'name')


class PhoneNumberAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'identity', 'category', 'priority', 'provider')
    list_filter = ('category', 'priority')


class PhoneNumberTypeAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name', 'priority')


class ProviderAdmin(UserAdmin):
    # form = ProviderModificationForm
    # add_form = ProviderCreationForm
    list_display = ('__str__', 'username', 'email',
                    'first_name', 'last_name', 'is_staff')
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email',
                       'is_superuser', 'is_staff', 'is_active',
                       'role', 'location')}),
        ("Personnal info", {
            'classes': ('wide',),
            'fields': ('gender', 'title', 'maiden_name', 'first_name',
                       'middle_name', 'last_name', 'position')}),
    )

    fieldsets = (
        (None, {'fields': ('username', 'password', 'email',
                           'role', 'location')}),
        (_('Personal info'), {'fields': ('gender', 'title', 'maiden_name',
                                         'first_name', 'middle_name',
                                         'last_name', 'position')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )


class SNISIReportAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'period', 'entity', 'receipt',
                    'validation_status', 'arrival_status')
    list_filter = ('period', 'validation_status', 'arrival_status',
                   'integrity_status', 'completion_status')


class ExpectedReportingAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'period', 'entity',
                    'report_class', 'amount_expected', 'completion_status')
    list_filter = ('report_class', 'amount_expected', 'completion_status')


class ExpectedValidationAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'satisfied', 'validated_on')
    list_filter = ('satisfied',)


class SMSMessageAdmin(admin.ModelAdmin):
    list_display = ('direction', 'identity', 'event_on', 'text', 'handled')
    list_filter = ('direction', 'event_on', 'handled')


class NotificationAdmin(admin.ModelAdmin):

    list_display = ('deliver', 'sent', 'delivery_status', 'category', 'text')
    list_filter = ('deliver', 'sent', 'delivery_status',
                   'level', 'important', 'category')
    ordering = ('created_on',)
    search_fields = ('title', 'text', 'text_short')
