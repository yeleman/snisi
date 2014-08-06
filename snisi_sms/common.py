#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

from django.utils import timezone


def test(message, **kwargs):
    msg = "Received on {date}"
    try:
        _, content = message.content.split()
        msg += ": {content}"
    except:
        pass

    message.respond(msg.format(date=timezone.now(), content=content))
    return True


def echo(message, **kwargs):
    message.respond(kwargs['args'])
    return True
