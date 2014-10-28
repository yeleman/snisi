#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

from django.utils import timezone
from django.conf import settings

from snisi_core.models.Providers import Provider
from snisi_sms.reply import SMSReply
from snisi_tools.sms import send_sms


def test(message):
    msg = "Received on {date}"
    try:
        _, content = message.content.split()
        msg += ": {content}"
    except:
        content = None

    message.respond(msg.format(date=timezone.now(), content=content))
    return True


def echo(message):
    try:
        kw, args = message.content.split(" ", 1)
    except:
        args = "-"
    message.respond(args)
    return True


def change_passwd(message):

    reply = SMSReply(message, "PASS")

    error_start = "Impossible de changer votre mot de passe."
    try:
        kw, username, old_password, new_password = \
            message.content.strip().lower().split()
    except ValueError:
        return reply.error(
            "{} Le format du SMS est incorrect.".format(error_start))

    try:
        provider = Provider.active.get(username=username)
    except Provider.DoesNotExist:
        return reply.error(
            "{} Ce nom d'utilisateur ({}) n'existe pas."
            .format(error_start, username))

    if not provider.check_password(old_password):
        return reply.error(
            "{} Votre ancien mot de passe est incorrect."
            .format(error_start))

    try:
        provider.set_password(new_password)
        provider.save()
    except:
        return reply.error(
            "{} Essayez un autre nouveau mot de passe."
            .format(error_start))

    return reply.success("Votre mot de passe a été changé et est "
                         "effectif immédiatement. Merci.")


def ask_for_help(message, nousername=False):

    reply = SMSReply(message, "AIDE")

    try:
        hotline = settings.HOTLINE_NUMBER
    except:
        hotline = '70061482'

    try:
        kw, username = message.content.strip().lower().split()
    except:
        username = None

    if username is not None:
        try:
            username = username.split(':')[1]
        except:
            username = None

    provider = None
    if username:
        try:
            provider = Provider.objects.get(username=username)
        except Provider.DoesNotExist:
            pass

    if not provider:
        provider = Provider.from_phone_number(identity=message.identity)

    if not provider:
        text_message = ("[DEMANDE AIDE] Non identifié: {}"
                        .format(message.identity))
    else:
        text_message = "[DEMANDE AIDE] {provider}".format(
            provider=provider.name())

    send_sms(hotline, text_message)

    return reply.success("Votre demande d'aide a été prise en compte. "
                         "Merci de patienter ou d'appeller la Hotline "
                         "au {}".format(hotline))
