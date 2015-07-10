#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging

from py3compat import implements_to_string
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

from snisi_core.models.Providers import Provider
from snisi_core.models.Numbers import PhoneNumber
from snisi_core import branding
from snisi_tools.emails import send_email
from snisi_tools.sms import send_sms


logger = logging.getLogger(__name__)


def submit_urgent_notifications(sender, instance, **kwargs):
    if instance.is_urgent() and not instance.sent:
        instance.send()


class Destination(object):

    def __init__(self, dtype, identity, short=False):
        self.type = dtype
        self.identity = identity
        self.short = short


@implements_to_string
class Notification(models.Model):

    class Meta:
        app_label = 'snisi_core'
        verbose_name = _("Notification")
        verbose_name_plural = _("Notifications")

    IMMEDIATELY = 'immediately'
    QUICKLY = 'quickly'
    TODAY = 'today'
    SOON = 'soon'
    LATER = 'later'

    DELIVER_OPTIONS = {
        IMMEDIATELY: _("Immediately"),
        QUICKLY: _("Quickly"),
        TODAY: _("Today"),
        SOON: _("Soon"),
        LATER: _("Later"),
    }

    DELIVERED = 'delivered'
    NOT_DELIVERED = 'not_delivered'
    EXPIRED = 'expired'
    UNKNOWN = 'unknown'

    DELIVERY_STATUSES = {
        DELIVERED: _("Delivered"),
        NOT_DELIVERED: _("Not delivered"),
        EXPIRED: _("Expired"),
        UNKNOWN: _("Unknown")
    }

    WARNING = 'warning'
    SUCCESS = 'success'
    ERROR = 'error'
    INFO = 'info'
    ACTION_REQUIRED = 'action_required'

    LEVELS = {
        ACTION_REQUIRED: _("Action Required"),
        INFO: _("Info"),
        SUCCESS: _("Success"),
        WARNING: _("Warning"),
        ERROR: _("Error"),
    }

    LEVEL_TITLES = {
        ACTION_REQUIRED: _("TODO"),
        INFO: None,
        SUCCESS: _("OK"),
        WARNING: _("/!\\"),
        ERROR: _("ERR")
    }

    EMAIL = 'email'
    SMS = 'sms'
    PREFERRED = 'preferred'
    ALL = 'all'
    ALL_CONTACTS = 'all_contacts'

    METHODS = {
        EMAIL: _("Email"),
        SMS: _("SMS"),
        PREFERRED: _("Preferred"),
        ALL: _("All methods"),
        ALL_CONTACTS: _("All contacts")
    }

    created_on = models.DateTimeField(default=timezone.now)

    # person who will receive the notification
    # if not a provider, either email and/or phone number
    provider = models.ForeignKey(Provider, blank=True, null=True)
    destination_email = models.EmailField(blank=True, null=True)
    destination_number = models.CharField(max_length=75, blank=True, null=True)

    deliver = models.CharField(max_length=75, choices=DELIVER_OPTIONS.items())
    sent = models.BooleanField(default=False)
    sent_on = models.DateTimeField(blank=True, null=True)
    delivery_status = models.CharField(max_length=75,
                                       default=UNKNOWN,
                                       choices=DELIVERY_STATUSES.items())
    expirate_on = models.DateTimeField(blank=True, null=True)

    # how to decide which way to send the notification via.
    method = models.CharField(max_length=75,
                              default=PREFERRED,
                              choices=METHODS.items())

    # kind of message
    level = models.CharField(max_length=75,
                             default=INFO,
                             choices=LEVELS.items())
    important = models.BooleanField(default=False)
    # area/project the alert relates to
    category = models.CharField(max_length=75, blank=True, null=True)
    # email subject if applicable
    title = models.TextField(blank=True, null=True)
    # notification body.
    text = models.TextField()
    # shorter version of the notif body. If exists, superseeds messages
    # in small devices (SMS)
    text_short = models.TextField(null=True, blank=True)

    @classmethod
    def create(cls, *args, **kwargs):
        return cls.objects.create(*args, **kwargs)

    def __str__(self):
        return self.message()

    def is_urgent(self):
        return self.deliver == self.IMMEDIATELY

    def message(self, short=False):
        if short and self.text_short:
            return short
        return self.text

    def idle_since(self, now=None):
        self.has_expired()
        if now is None:
            now = timezone.now()
        return now - self.created_on

    @classmethod
    def disable_for(cls, provider=None,
                    destination_email=None, destination_number=None):
        ''' remove all notifications for this user '''
        if provider is None:
            if destination_email is None:
                dest_filter = {'destination_number': destination_number}
            else:
                dest_filter = {'destination_email': destination_email}
        else:
            dest_filter = {'provider': provider}

        cls.objects.filter(sent=False, **dest_filter).delete()

    @classmethod
    def _prefix(cls, short=False, category=None,
                important=False, level=INFO, brand_fallback=True):
        if category:
            categorys = "[{category}]".format(category=category)
        elif brand_fallback:
            categorys = ("[{brand_short}]"
                         .format(brand_short=branding.get('brand_short')))
        else:
            categorys = ""

        if important:
            importants = "[!]" if short else "[important]"
        else:
            importants = ""

        if short:
            levels = ""
        else:
            levels = cls.LEVEL_TITLES.get(level, '') or ''
            if levels.strip():
                levels = "[{level}]".format(level=levels)

        return "{category}{important}{level}".format(
            category=categorys, important=importants, level=levels)

    def prefix(self, short=False, brand_fallback=True):
        return self._prefix(short=short,
                            category=self.category,
                            important=self.important,
                            level=self.level)

    def fmt_title(self, short=False):
        if short:
            return "{prefix}".format(prefix=self.prefix(short))

        title = " ".join(self.title.strip().splitlines()) \
            if self.title else "Nouvelle notification"
        return "{prefix} {title}".format(
            prefix=self.prefix(False), title=title)

    @classmethod
    def title_for_list(cls, notifications, short=False):
        categories = []
        important = False
        levels = []
        for notification in notifications:
            categories.append(notification.category)
            if notification.important:
                important = True
            levels.append(notification.level)
        categories = list(set(categories))
        levels = list(set(levels))
        try:
            categories.remove(None)
        except ValueError:
            pass

        category = None if len(categories) != 1 else categories[0]
        level = None if len(levels) != 1 else levels[0]

        prefix = cls._prefix(short=short,
                             category=category,
                             important=important,
                             level=level)

        title = "{nb} nouvelles notifications".format(nb=len(notifications))

        return "{prefix} {title}".format(prefix=prefix, title=title)

    @classmethod
    def body_for_list(cls, notifications, short=False):
        if short:
            return "/".join([notification.message(True)
                             for notification in notifications])

        return "\n\n".join(["* {prefix} {message}".format(
            prefix=notification.prefix(short=False, brand_fallback=False),
            message=notification.message(False))
            for notification in notifications])

    @classmethod
    def _preferred_method(cls,
                          provider=None,
                          destination_email=None, destination_number=None):
        if not provider:
            return cls.EMAIL if destination_email else cls.SMS
        return cls.EMAIL if provider.email else cls.SMS

    def preferred_method(self):
        return self._preferred_method(
            provider=self.provider,
            destination_email=self.destination_email,
            destination_number=self.destination_number)

    @classmethod
    def _destinations(cls, method,
                      provider=None,
                      destination_email=None, destination_number=None):
        destination_for_email = lambda email: None if email is None \
            else Destination(dtype='email', identity=email, short=False)
        destination_for_number = lambda number: None if number is None \
            else Destination(dtype='sms', identity=number, short=True)

        # email to send to. from provider if exist or manual address
        email = provider.email or destination_email \
            if provider else destination_email
        # number to send to. from provider if exist or manual number
        number = provider.primary_phone() or destination_number \
            if provider else destination_number
        # list of all phone numbers from provider or single one provided
        all_numbers = provider.all_numbers() or [destination_number] \
            if provider else [destination_number]
        # Destination object for email
        email_dest = destination_for_email(email)
        # Destination object for number
        sms_dest = destination_for_number(number)
        # rewrite the method if necessary (preferred)
        method = method if method != cls.PREFERRED else cls._preferred_method(
            provider=provider, destination_email=destination_email,
            destination_number=destination_number)

        if method == cls.EMAIL and email:
            ret = [email_dest]
        elif method == cls.SMS and number:
            ret = [sms_dest]
        elif method == cls.ALL:
            ret = [email_dest, sms_dest]
        elif method == cls.ALL_CONTACTS:
            ret = [email_dest] + [destination_for_number(num)
                                  for num in all_numbers]
        else:
            ret = []
        ret = list(set(ret))
        try:
            ret.remove(None)
        except:
            pass
        return ret

    def destinations(self):
        return self._destinations(method=self.method, provider=self.provider,
                                  destination_email=self.destination_email,
                                  destination_number=self.destination_number)

    def send(self):
        if self.has_expired() or self.sent:
            return False
        for destination in self.destinations():
            self.send_notification(
                destination=destination,
                title=self.fmt_title(short=destination.short),
                body=self.message(short=destination.short))
            self.fire_out()

    def has_expired(self, now=None):
        if now is None:
            now = timezone.now()
        if self.expirate_on and now > self.expirate_on:
            self.delivery_status = self.EXPIRED
            self.save()
            return True
        return False

    @classmethod
    def _use_short(cls, method):
        return True if method == cls.SMS else False

    def use_short(self, method):
        return self._use_short(method)

    def fire_out(self, now=None):
        if now is None:
            now = timezone.now()
        self.sent = True
        self.sent_on = now
        self.save()

    @classmethod
    def send_for_recipient(cls, trigger_on, provider=None,
                           destination_email=None, destination_number=None):

        if provider is None:
            if destination_email is None:
                dest_filter = {'destination_number': destination_number}
            else:
                dest_filter = {'destination_email': destination_email}
        else:
            dest_filter = {'provider': provider}

        notifications = Notification.objects.filter(sent=False) \
                                    .exclude(delivery_status=cls.EXPIRED) \
                                    .filter(**dest_filter).all()

        # create and fill-up a dict indexed by delivery option
        sorted_notifications = {key: [] for key in cls.DELIVER_OPTIONS.keys()}
        [sorted_notifications[notification.deliver].append(notification)
         for notification in notifications]

        # no notification requires sending
        if not len(sorted_notifications.get(trigger_on, [])):
            return False

        if len(notifications) == 1:
            notifications[0].send()
            return notifications

        title = cls.title_for_list(notifications=notifications, short=False)
        body = cls.body_for_list(notifications=notifications, short=False)
        title_short = cls.title_for_list(notifications=notifications,
                                         short=True)
        body_short = cls.body_for_list(notifications=notifications, short=True)
        method = cls._preferred_method(provider=provider,
                                       destination_email=destination_email,
                                       destination_number=destination_number)
        destinations = cls._destinations(method=method, provider=provider,
                                         destination_email=destination_email,
                                         destination_number=destination_number)

        # actually send notifications
        for destination in destinations:
            cls.send_notification(
                destination=destination,
                title=title if not destination.short else title_short,
                body=body if not destination.short else body_short)

        # mark all as submitted
        [notification.fire_out() for notification in notifications]

        return notifications

    @classmethod
    def send_notification(cls, destination, body, title=None):
        logger.info("Sending {} to {}. {} - {}".format(
            destination.type, destination.identity, title, body))

        if destination.type == 'sms':
            # restricted SMS mode
            if settings.FLOTTE_ONLY_NOTIFICATIONS:
                pn = PhoneNumber.get_or_none(destination.identity)
                if pn is None or pn.category != 'flotte':
                    return
            send_sms(destination.identity,
                     "{title} {body}".format(title=title, body=body))

        if destination.type == 'email':
            send_email(recipients=destination.identity,
                       message=body, title=title,
                       sender=branding.get('notification_from'))

    def to_send_dict(self):
        return {
            'provider': self.provider,
            'destination_email': self.destination_email,
            'destination_number': self.destination_number
        }

    @classmethod
    def pending_recipients(cls):
        return [n.to_send_dict()
                for n in Notification.objects.filter(sent=False)
                .exclude(delivery_status=cls.EXPIRED)]

    @classmethod
    def longest_duration_for(cls, provider=None,
                             destination_email=None,
                             destination_number=None):
        qs = cls.objects
        if provider is not None:
            qs = qs.filter(provider=provider)
        elif destination_email is not None:
            qs = qs.filter(destination_email=destination_email)
        elif destination_number is not None:
            qs = qs.filter(destination_number=destination_number)
        else:
            return None

        try:
            longest_notification = qs.order_by('created_on').first()
        except:
            return None

        return int((timezone.now()
                   - longest_notification.created_on).total_seconds())

receiver(post_save, sender=Notification)(submit_urgent_notifications)
