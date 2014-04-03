#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging
from optparse import make_option

from django.core.management.base import BaseCommand
from snisi_core.models.Notifications import Notification

logger = logging.getLogger(__name__)

AN_HOUR = 3600

TRIGGER_DURATIONS = {
    Notification.IMMEDIATELY: 0,
    Notification.QUICKLY: 4 * AN_HOUR,
    Notification.TODAY: 8 * AN_HOUR,
    Notification.SOON: 36 * AN_HOUR,
    Notification.LATER: 72 * AN_HOUR,
}

class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
        make_option('-t',
                    help='Trigger to send notifications for [immediately, ]',
                    action='store',
                    dest='trigger'),
    )

    def handle(self, *args, **options):
        trigger = options.get('trigger')

        if not trigger in Notification.DELIVER_OPTIONS.keys():
            logger.error("Invalid trigger –{}– for notifications.".format(trigger))
            return

        trigger_duration = TRIGGER_DURATIONS.get(trigger)

        logger.debug("Sending notifications for `{}`: "
                     "notifications {}h+ old"
                     .format(trigger, int(trigger_duration / AN_HOUR)))

        for recipient_dict in Notification.pending_recipients():
            logger.debug("\t{}/{}/{}".format(recipient_dict.get('provider'),
                                             recipient_dict.get('destination_email'),
                                             recipient_dict.get('destination_number')))

            if recipient_dict.get('provider') and not recipient_dict.get('provider').is_active:
                logger.info("Provider is not active anymore. Remove all notifications.")
                Notification.disable_for(provider=recipient_dict.get('provider'))
                continue

            # retrieve duration of oldest notification for user
            provider_duration = Notification.longest_duration_for(**recipient_dict)

            # a notif has reached its duration limit.
            # fire all notifications.
            if provider_duration >= trigger_duration:
                Notification.send_for_recipient(trigger_on=trigger, **recipient_dict)
