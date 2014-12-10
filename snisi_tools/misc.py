#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging
import uuid
import os

from django.apps import apps

logger = logging.getLogger(__name__)


def import_path(name, failsafe=False):
    """ import a callable from full module.callable name """
    def _imp(name):
        modname, __, attr = name.rpartition('.')
        if not modname:
            # single module name
            return __import__(attr)
        m = __import__(modname, fromlist=[str(attr)])
        return getattr(m, attr)
    try:
        return _imp(name)
    except (ImportError, AttributeError) as exp:
        logger.debug("Failed to import {}: {}".format(name, exp))
        if failsafe:
            return None
        raise exp


def entities_path(root, entity):
    """ [] or {} for multi-select containing path to root entity """
    paths = []
    if entity.all_children().count():
        try:
            level = entity_children(entity)[0][1].type
        except IndexError:
            level = entity.type
        p = {'selected': None, 'elems': entity_children(entity),
             'level': level}
        paths.append(p)
    while entity.health_parent_first and not entity == root:
        p = {'selected': entity.slug,
             'elems': entity_children(entity.health_parent_first),
             'level': entity.type}
        paths.append(p)
        entity = entity.health_parent_first
    paths.reverse()
    return paths


def entities_path2(root, entity):
    """ [] or {} for multi-select containing path to root entity """
    skip_slugs = ['health_area', 'vfq']
    paths = []
    if len(entity.get_natural_children(skip_slugs=skip_slugs)):
        try:
            level = entity_children2(entity)[0][1].type
        except IndexError:
            level = entity.type
        p = {'selected': None, 'elems': entity_children2(entity),
             'level': level}
        paths.append(p)
    while entity.get_natural_parent(skip_slugs=skip_slugs) \
            and not entity.slug == root.slug:
        p = {'selected': entity.slug,
             'elems':
             entity_children2(
                 entity.get_natural_parent(skip_slugs=skip_slugs)),
             'level': entity.type}
        paths.append(p)
        entity = entity.get_natural_parent(skip_slugs=skip_slugs)
    paths.reverse()
    return paths


def entity_children2(entity):
    """ (entity.slug, entity) of all children of an entity """
    return [(e.slug, e)
            for e in entity.get_natural_children(
                skip_slugs=['health_area', 'vfq'])]


def entity_children(entity):
    """ (entity.slug, entity) of all children of an entity """
    return [(e.slug, e)
            for e in entity.all_children(health_only=True).order_by('name')]


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


def class_str(class_or_object):
    if hasattr(class_or_object, '__mro__'):
        cls = getattr(class_or_object, '__mro__')[0]
        return '{}.{}'.format(cls.__module__, cls.__name__)
    return class_str(class_or_object.__class__)


def short_class_str(class_str):
    ''' shorten a class_str string to reflect only Model name '''
    return class_str.rsplit('.', 0)


def get_uuid():
    return uuid.uuid4().get_urn()[9:]


def get_snisi_apps():
    return [app for app in [p.split('/')[-1] for p in apps.get_app_paths()]
            if app.startswith('snisi_')
            and app not in ('snisi_core', 'snisi_sms',
                            'snisi_web', 'snisi_tools', 'snisi_maint')]


def get_from_snisi_apps(path, fusion_list=False):
    values = []
    for app in get_snisi_apps():
        try:
            values.append(import_path('{app}.{path}'
                                      .format(app=app, path=path)))
        except (ImportError, AttributeError):
            pass
    if not fusion_list:
        return values

    return [value for domain_list in values for value in domain_list]


def get_resource(domain_slug, *file_paths):
    from snisi_core.models.Projects import Domain
    domain = Domain.get_or_none(domain_slug)
    return os.path.join(domain.module_path, 'resources', *file_paths)


def get_not_none(dict, key, default):
    return dict.get(key, default) or 0
