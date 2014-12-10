#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging
import unicodedata
import random
import re

from py3compat import text_type
from snisi_core.models.Providers import Provider
from snisi_core.models.Roles import Role
from snisi_core.models.Entities import Entity
from snisi_core.models.Numbers import PhoneNumber, PhoneNumberType
from snisi_tools.numbers import normalized_phonenumber

logger = logging.getLogger(__name__)

PASSWORD_LENGTH = 8
USERNAME_MIN_LENGTH = 4
USERNAME_MAX_LENGTH = 8
DUMB_PASSWORD_LENGTH = 4


def random_password(dumb=False):
    """ random password suitable for mobile typing """
    if not dumb:
        return ''.join([random.choice('abcdefghijklmnopqrstuvwxyz1234567890')
                        for i in range(PASSWORD_LENGTH)])

    # dumb password
    num_chars = DUMB_PASSWORD_LENGTH
    letters = 'abcdefghijklmnopqrstuvwxyz'
    index = random.randint(0, len(letters) - 1)

    password = letters[index]
    num_chars -= 1
    while num_chars:
        num_chars -= 1
        index += 1
        try:
            password += letters[index]
        except IndexError:
            password += letters[index - len(letters)]
    postfix = random.randint(0, 9)
    password += str(postfix)
    return password


def username_from_name(first_name, last_name):
    """ available username to use on User forged from first and last name """

    def new_slug(text, salt=None):
        """ assemble text and salt providing optimum length """
        if salt:
            username = text[:(USERNAME_MAX_LENGTH - len(salt))] + salt
        else:
            username = text[:USERNAME_MAX_LENGTH]
        if len(username) < USERNAME_MIN_LENGTH:
            username = "{0:{1}<{2}}".format(username, "a", USERNAME_MIN_LENGTH)
        return username

    def is_available(username):
        """ DB check for username use """
        return Provider.objects.filter(username=username).count() == 0

    def jdoe(first, last):
        """ first name initial followed by last name format """
        return "{}{}".format(first[0], last)

    def johndoe(first, last):
        """ first name followed by last name format """
        return "{}{}".format(first, last)

    def iterate(username):
        """ adds and increment a counter at end of username """
        # make sure username matches length requirements
        username = new_slug(username)
        if not is_available(username):
            # find the counter if any
            sp = re.split(r'([0-9]+)$', username)
            if len(sp) == 3:
                # increment existing counter
                username = sp[0]
                salt = text_type(int(sp[1]) + 1)
            else:
                # start counter at 1
                salt = '1'
            # bundle counter and username then loop
            return iterate(new_slug(username, salt))
        else:
            # username is available
            return username

    def string_to_slug(s):
        raw_data = s
        try:
            raw_data = unicodedata.normalize('NFKD',
                                             raw_data.decode('utf-8',
                                                             'replace')) \
                                  .encode('ascii', 'ignore')
        except:
            pass
        return re.sub(r'[^a-z0-9-]+', '', raw_data.lower()).strip()

    # normalize first and last name to ASCII only
    first_name = string_to_slug(first_name.lower())
    last_name = string_to_slug(last_name.lower())

    # iterate over a jdoe format
    return iterate(jdoe(first_name, last_name))


def can_view_entity(provider, entity):
    ''' wheter a provider can access data from an entity '''

    # Providers on Mali can see everything
    if provider.location.level == 0:
        return True
    # if provider's level is bellow request, deny whatever
    if provider.location.level > entity.level:
        return False

    if provider.location.level <= entity.level:
        return entity.get_type(provider.location.type.slug) == \
            provider.location.casted()

    # slow but safer check
    return entity in provider.location.get_types(entity.type.slug)


def reset_password_for(username):
    p = Provider.get_or_none(username)
    if p is None:
        raise ValueError("Username `{}` is not an active Provider"
                         .format(username))
    passwd = random_password(True)
    p.set_password(passwd)
    p.save()
    return passwd


def create_provider(first_name, last_name,
                    role, location,
                    email=None,
                    middle_name=None, maiden_name=None,
                    gender=Provider.UNKNOWN,
                    title=None, position=None,
                    phone_numbers=[]):
    good_numbers = []
    for number in phone_numbers:
        if isinstance(number, (list, tuple)) and len(number) > 1:
            flotte = bool(number[1])
            number = number[0]
        else:
            flotte = False
        npn = normalized_phonenumber(number)
        pnt = PhoneNumberType.from_number(npn, is_flotte=flotte)
        pn = PhoneNumber.get_or_none(npn)
        if pn is not None:
            msg = "Phone number `{}` is already assigned to {}/{}".format(
                npn, pn.provider, pn.provider.username)
            logger.error(msg)
            raise ValueError
        good_numbers.append((npn, pnt, pnt.priority))

    gender = gender if gender in Provider.GENDERS.keys() \
        else Provider.UNKNOWN
    p = Provider.objects.create(
        username=username_from_name(first_name, last_name),
        gender=gender,
        title=title,
        first_name=first_name or None,
        last_name=last_name,
        middle_name=middle_name,
        maiden_name=maiden_name,
        position=position,
        role=Role.get_or_none(role),
        location=Entity.get_or_none(location),
        email=email)
    passwd = random_password(True)
    p.set_password(passwd)
    p.save()
    for npn, pnt, priority in good_numbers:
        PhoneNumber.objects.create(
            identity=npn,
            category=pnt,
            priority=priority,
            provider=p)
    return p, passwd
