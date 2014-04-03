#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import datetime
import re

from django.utils import timezone



# def resp_error(message, action):
#     message.respond("[ERREUR] Impossible de comprendre "
#                     "le SMS pour {}".format(action))
#     return True


# def resp_error_date(message):
#     message.respond("[Date de visite] la date n'est pas valide.")
#     return True


# def conv_str_int(value):
#     try:
#         value = int(value)
#     except:
#         value = None
#     return value


# def resp_error_dob(message):
#     message.respond("[ERREUR] la date de naissance n'est pas valide")
#     return True


# def resp_error_provider(message):
#     message.respond("Aucun utilisateur ne possede ce numero de telephone")
#     return True


# def parse_age_dob(age_or_dob, only_date=False):
#     """ parse argument as date or age. return date and bool if estimation """

#     if re.match(r'^\d{8}$', age_or_dob):
#         auto = False
#         parsed_date = datetime.date(int(age_or_dob[0:4]), int(age_or_dob[4:6]),
#                                     int(age_or_dob[6:8]))
#     else:
#         auto = True
#         today = datetime.date.today()
#         unit = age_or_dob[-1]
#         value = int(age_or_dob[:-1])
#         if unit.lower() == 'a':
#             parsed_date = today - datetime.timedelta(365 * value) - datetime.timedelta(160)
#         elif unit.lower() == 'm':
#             parsed_date = today - datetime.timedelta(30 * value) - datetime.timedelta(15)
#         else:
#             raise ValueError("Age unit unknown: %s" % unit)

#     if only_date:
#         return parsed_date
#     else:
#         return (parsed_date, auto)


# def date_is_old(reporting_date):

#     if (datetime.date.today() - reporting_date).days > 30:
#         raise ValueError("Le {} est passé il y a plus 30 jours".format(reporting_date))


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
