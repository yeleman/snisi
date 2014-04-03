#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import iso8601

# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from snisi_core.models import Provider, Entity, Role
from snisi_tools.misc import import_path


class DictDiffer(object):
    """ Calculate the difference between two dictionaries """
    def __init__(self, current_dict, past_dict):
        self.current_dict, self.past_dict = current_dict, past_dict
        self.current_keys, self.past_keys = [
            set(d.keys()) for d in (current_dict, past_dict)
        ]
        self.intersect = self.current_keys.intersection(self.past_keys)

    def added(self):
        return self.current_keys - self.intersect

    def removed(self):
        return self.past_keys - self.intersect

    def changed(self):
        return set(o for o in self.intersect
                   if self.past_dict[o] != self.current_dict[o])

    def unchanged(self):
        return set(o for o in self.intersect
                   if self.past_dict[o] == self.current_dict[o])


def period_from(period_str, as_class=None):
    cls = import_path(period_str.get('class')) if as_class is None else as_class
    middle = datetime_from(period_str.get('middle'))
    return cls.find_create_by_date(middle)


def role_from(role_str):
    return Role.objects.get(slug=role_str)


def entity_from(entity_str):
    return Entity.objects.get(slug=entity_str)


def get_provider_from(username):
    return None if username is None else Provider.objects.get(username=username)


def get_user_from(username):
    return None if username is None else get_user_model().objects.get(username=username)


def datetime_from(date_str):
    return iso8601.parse_date(date_str)
