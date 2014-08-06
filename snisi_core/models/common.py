#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import random
import logging

import reversion
from django.db import models

from snisi_tools.misc import get_uuid

logger = logging.getLogger(__file__)


def get_temp_receipt(instance):
    return 'uuid:{uuid}'.format(uuid=get_uuid())


def pre_save_report(sender, instance, **kwargs):
    ''' create a temporary Receipt for Report '''
    # this will allow us to detect failure in registration
    logger.debug("pre_save_report [{}: {}]"
                 .format(instance.receipt, instance.completion_status))
    if not instance.receipt and instance.completion_status \
            == instance.COMPLETE:
        instance.receipt = get_temp_receipt(instance)


def pre_save_report_incomplete(sender, instance, **kwargs):
    ''' create a temporary Receipt for Report '''
    # this will allow us to detect failure in registration
    logger.debug("pre_save_report_incomplete [{}: {}]"
                 .format(instance.receipt, instance.completion_status))
    if not instance.receipt:
        instance.receipt = get_temp_receipt(instance)


def post_save_report(sender, instance, **kwargs):
    ''' Generates appropriate receipt for Report '''
    logger.debug("post_save_report [{}]".format(instance.receipt))
    if instance.receipt.startswith('uuid:'):
        instance.receipt = sender.generate_receipt(instance)
        instance.save()


def receipt_fields(instance, **kwargs):
    ''' generates a reversable text receipt for a SNISIReport '''

    random_part = str(random.randint(0, 9))
    days_of_week = ['D', 'L', 'M', 'E', 'J', 'V', 'S']

    fields = {'day': instance.created_on.strftime('%j'),
              'dow': days_of_week[int(instance.created_on.strftime('%w'))],
              'period__month': instance.period.middle().strftime('%m'),
              'period__year': instance.period.middle().strftime('%Y'),
              'period__day': instance.period.middle().strftime('%d'),
              'period__year_short': instance.period.middle().strftime('%y'),
              'entity__slug': instance.entity.slug,
              'entity__type': instance.entity.type.slug,
              'id': instance.__class__.objects.count(),
              'period__id': instance.period.id,
              'period': instance.period.strid(),
              'rand': random_part,
              'uuid': instance.uuid}
    fields.update(**kwargs)

    return fields


def generate_receipt(instance, receipt_format=None, **kwargs):
    ''' generates a reversable text receipt for a SNISIReport '''

    if receipt_format is None:
        receipt_format = instance.RECEIPT_FORMAT
    return receipt_format.format(**receipt_fields(instance, **kwargs))


def create_periodic_agg_report_from(cls, period, entity,
                                    created_by, indiv_cls=None,
                                    indiv_sources=None,
                                    agg_sources=None):
    """ Create A `cls` (Agg) report from Individual or Aggregated

        Report Class (cls) must obey to the conventional Report API:
        Subclass of Report
        cls.start()
        cls.indiv_sources = PosInt()
        cls.agg_sources = PosInt()
        cls.fill_blank() # if no sources
        cls.update_instance_with_indiv()
        cls.update_instance_with_agg() """

    # create empty
    agg_report = cls.start(entity=entity, period=period, created_by=created_by)
    agg_report.fill_blank()

    # find list of sources
    if indiv_cls is not None and indiv_sources is None:
        indiv_sources = indiv_cls.objects.filter(
            period=period, entity__in=entity.get_health_children())
    else:
        indiv_sources = indiv_sources or []

    if agg_sources is None:
        agg_sources = cls.objects.filter(
            period=period, entity__in=entity.get_health_children())
    else:
        agg_sources = agg_sources or []

    sources = list(indiv_sources) + list(agg_sources)

    # save to allow m2m
    agg_report.save()

    # # keep a record of all sources
    # for report in indiv_sources:
    #     agg_report.direct_indiv_sources.add(report)

    # for report in agg_sources:
    #     agg_report.direct_agg_sources.add(report)

    # loop on all sources
    for source in sources:
        if isinstance(source, indiv_cls):
            cls.update_instance_with_indiv(agg_report, source)
            cls.update_instance_with_indiv_meta(agg_report, source)
        elif isinstance(source, cls):
            cls.update_instance_with_agg(agg_report, source)
            cls.update_instance_with_agg_meta(agg_report, source)

    with reversion.create_revision():
        agg_report.save()
        reversion.set_user(created_by)

    return agg_report


class ActiveManager(models.Manager):

    def get_query_set(self):
        return super(ActiveManager, self).get_query_set() \
                                         .filter(is_active=True)
