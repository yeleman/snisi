#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import collections

from django.core.exceptions import PermissionDenied


def user_role_within(role_list):
    """ decorator asserting user's role is with the provided list """
    def decorator(target):
        def wrapper(request, *args, **kwargs):
            roles = role_list if isinstance(role_list, collections.Iterable) \
                else [role_list]
            if request.user.role.slug in roles:
                return target(request, *args, **kwargs)
            raise PermissionDenied
        return wrapper
    return decorator


def user_location_type_within(type_slug_list):
    """ decorator asserting user's location__type__slug is in provided list """
    def decorator(target):
        def wrapper(request, *args, **kwargs):
            type_slugs = type_slug_list if isinstance(
                type_slug_list, collections.Iterable) else [type_slug_list]
            if request.user.location.type.slug in type_slugs:
                return target(request, *args, **kwargs)
            raise PermissionDenied
        return wrapper
    return decorator


def user_in_group(group):
    """ decorator asserting user is member of provided group """
    def decorator(target):
        def wrapper(request, *args, **kwargs):
            if group in request.user.groups.all():
                return target(request, *args, **kwargs)
            raise PermissionDenied
        return wrapper
    return decorator


def user_location_level_below(max_level):
    """ decorator asserting user's location__type__slug is in provided list """
    def decorator(target):
        def wrapper(request, *args, **kwargs):
            if request.user.location.level <= max_level:
                return target(request, *args, **kwargs)
            raise PermissionDenied
        return wrapper
    return decorator


def user_location_level_above(min_level):
    """ decorator asserting user's location__type__slug is in provided list """
    def decorator(target):
        def wrapper(request, *args, **kwargs):
            if request.user.location.level >= min_level:
                return target(request, *args, **kwargs)
            raise PermissionDenied
        return wrapper
    return decorator
