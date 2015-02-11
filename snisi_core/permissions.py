#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging

from django.core.exceptions import PermissionDenied

from snisi_core.models.Entities import Entity
from snisi_core.models.Providers import Provider
from snisi_core.models.Projects import Domain
from snisi_tools.misc import split_or

logger = logging.getLogger(__name__)


def provider_is_allowed(provider, slug, location=None):
    """ single entry point for provider permission check

        permission slugs respects the following format:

        <action>_<description>

        action in:
            * access (read data)
            * create-report (create reports)
            * download (download reports and files)
            * edit-report (modify existing reports)
            * validate-report (change validation status)
            # * view-map (maps provide overiew on larger locations)
            * monitor (for snisi-tech only)
            * manage (for snisi-admin only) """

    # not a provider or AnonymousUser
    if not isinstance(provider, Provider) or not provider.is_authenticated():
        return False

    # not properly configured provider
    if not getattr(provider, 'role', None) or \
            not getattr(provider, 'location', None):
        return False

    prole = provider.role.slug
    plocation = provider.location.casted()
    privileges = provider.privileges_dict
    action, domain, extension = split_or(slug, 3, max_split=2,
                                         char="_", default='')

    # admin is god.
    if prole == 'snisi_admin':
        return True

    if location is None:
        location = Entity.get_or_none('mali')
    else:
        location = location.casted()

    for domain in Domain.active.all():
        allow_func = domain.import_from('permissions.provider_is_allowed')
        if allow_func is None:
            continue
        ret = allow_func(prole=prole,
                         plocation=plocation,
                         privileges=privileges,
                         location=location,
                         action=action,
                         domain=domain,
                         extension=extension)
        if ret is None:
            continue
        return ret

    ret = default_permissions(prole=prole,
                              plocation=plocation,
                              privileges=privileges,
                              location=location,
                              action=action,
                              domain=domain,
                              extension=extension)
    if ret is not None:
        return ret

    # default to non-granted
    return False


def default_permissions(prole, plocation, privileges,
                        location, action, domain, extension):

    # snisi-tech can view every-thing
    if prole == 'snisi_tech' and action in ('access',
                                            'download'):
        return True

    # all roles can see data within their area
    # can view data
    if action in ('access', 'download'):
        if plocation in location.get_ancestors(include_self=True):
            return True


def provider_is_allowed_at_home(provider, slug):
    return provider_is_allowed(provider=provider, slug=slug,
                               location=getattr(provider, 'location', None))


def provider_allowed_or_denied(provider, slug, location=None):
    """ easy permission check for view """
    if not provider_is_allowed(provider, slug, location):
        raise PermissionDenied
    return True


def provider_allowed_or_denied_at_home(provider, slug):
    """ easy permission check on provider's own location """
    if not provider_is_allowed_at_home(provider, slug):
        raise PermissionDenied
    return True
