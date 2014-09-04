#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

from py3compat import implements_to_string, text_type
from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext
from picklefield.fields import PickledObjectField

from snisi_tools.misc import class_str, import_path


@implements_to_string
class Action(models.Model):

    class Meta:
        app_label = 'snisi_core'
        verbose_name = _("Action")
        verbose_name_plural = _("Action")

    ACTIONS = {
        'logged_in': _("Logged In"),
        'logged_out': _("Logged Out"),
        'changed_passwd': _("Changed Password"),
        'uploaded_report': _("Uploaded Report"),
        'edited_report': _("Edited Report"),
        'validated_report': _("Validated Report"),
        'created_report': _("Created Report"),
        'created_provider': _("Created Provider"),
        'edited_provider': _("Edited Provider"),
        'changed_provider_role_location': _("Changed Provider Role/Location"),
        'disabled_provider': _("Disabled Provider"),
        'enabled_provider': _("Enabled Provider"),
        'edited_profile': _("Edited Profile"),
        'added_phone': _("Added Phone Number"),
        'removed_phone': _("Removed Phone Number"),
        'asked_for_help': _("Asked for Help"),
        'sent_report_sms': _("Sent Report SMS"),
        'sent_unhandled_sms': _("Sent Unhandled SMS"),

        'autovalidated_reports': _("Autovalidated Reports"),
        'created_aggregated_reports': _("Created Aggregated Reports"),

        'created_entity': _("Created Entity"),
        'edited_entity': _("Edited Entity"),
        'disabled_entity': _("Disabled Entity"),
        'enabled_entity': _("Enabled Entity"),
        'created_cluster': _("Created Cluster"),
        'disabled_cluster': _("Disabled Cluster"),
        'enabled_cluster': _("Enabled Cluster"),
        'created_domain': _("Created domain"),
        'created_participations': _("Created Participations"),
        'created_expecteds': _("Created Report Expectations"),
        'started_in_time_data_collection':
            _("Started In Time Data Collection"),
        'ended_in_time_data_collection': _("Ended In Time Data Collection"),
        'started_late_data_collection': _("Started Late Data Collection"),
        'ended_late_data_collection': _("Started Late Data Collection"),
        'started_district_validation': _("Started District Validation"),
        'ended_district_validation': _("Ended District Validation"),
        'started_region_validation': _("Started Region Validation"),
        'ended_region_validation': _("Ended Region Validation"),
        'raised_expection': _("Raised Exception"),
        'generated_static_files': _("Generated Static Files"),
        'restarted_webserver': _("Restarted Web Server"),
    }

    WEB = 'web'
    SMS = 'sms'
    SERVER = 'server'

    IFACES = {
        WEB: _("Web"),
        SMS: _("SMS"),
        SERVER: _("Server")
    }

    slug = models.CharField(max_length=250, choices=ACTIONS.items())
    provider = models.ForeignKey('Provider')
    on = models.DateTimeField(auto_now=True)
    iface = models.CharField(max_length=50, choices=IFACES.items())
    domain = models.ForeignKey('Domain', blank=True, null=True)
    instance_cls = models.CharField(max_length=500, blank=True, null=True)
    instance_pk = models.CharField(max_length=500, blank=True, null=True)
    payload = PickledObjectField(null=True, blank=True)

    def __str__(self):
        return self.display()

    def display(self):
        return ugettext("{provider} {label} on {date}").format(
            provider=self.provider,
            label=self.label(),
            date=self.on)

    def display_noname(self):
        return ugettext("{label} on {date}").format(
            label=self.label(), date=self.on)

    def label(self):
        return self.ACTIONS.get(self.slug)

    @property
    def instance(self):
        return import_path(self.instance_cls).get_or_none(self.instance_pk)

    @classmethod
    def record(cls, slug, provider, iface,
               domain=None, instance=None, payload=None):
        if domain is not None and isinstance(domain, text_type):
            from snisi_core.models.domains import Domain
            domain = Domain.get_or_none(domain)
        if instance is not None:
            instance_cls = class_str(instance.__class__)
            instance_pk = instance.pk
        else:
            instance_cls = instance_pk = None
        return cls.objects.create(
            slug=slug,
            provider=provider,
            iface=iface,
            domain=domain,
            instance_pk=instance_pk,
            instance_cls=instance_cls,
            payload=payload)

    @classmethod
    def last_for(cls, provider, limit=None):
        return cls.objects.filter(provider=provider).order_by('-on')[:limit]
