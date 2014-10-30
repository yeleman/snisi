#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging

from snisi_core.models.Reporting import SNISIReport

logger = logging.getLogger(__name__)


class AbstractURENutritionR(SNISIReport):

    class Meta:
        app_label = 'snisi_nutrition'
        abstract = True

    IS_URENAM = False
    IS_URENAS = False
    IS_URENI = False

    AGE_LABELS = {
        'u6': "0-6m",  # URENI
        'u23o6': "6-23m",  # URENAM
        'u59o23': "23-59m",  # URENAM
        'u59o6': "6-59m",  # URENAS, URENI
        'o59': "59m+",  # URENAS, URENI
        'pw': "FE/FA",  # URENAM
        'exsam': "ExMAS",  # URENAM
    }

    @classmethod
    def uren_str(cls):
        if cls.IS_URENAM:
            return "URENAM"
        if cls.IS_URENAS:
            return "URENAS"
        if cls.IS_URENI:
            return "URENI"

    @classmethod
    def age_str(cls, age_slug):
        return cls.AGE_LABELS.get(age_slug)

    @classmethod
    def uren_fields(cls):
        return [
            'total_start_m', 'total_start_f',
            'new_cases', 'returned',
            'total_in_m', 'total_in_f',
            'transferred',
            'healed', 'deceased', 'abandon', 'not_responding',
            'total_out_m', 'total_out_f',
            'referred',
            'total_end_m', 'total_end_f']

    @classmethod
    def silent_uren_fields(cls, age):
        fields = []
        if cls.IS_URENAM:
            fields += ['transferred']

            if age == 'exsam':
                fields += ['new_cases', 'returned',
                           'total_in_m', 'total_in_f',
                           'healed', 'deceased', 'abandon']

        if not cls.IS_URENI:
            fields += ['not_responding']

        return fields

    # overriden
    @classmethod
    def age_groups(cls):
        return cls.AGE_LABELS.keys()

    # used for all age calculations within report
    def age_sum_for(self, age, fields):
        return sum([getattr(self, '{}_{}'.format(age, field))
                    for field in fields])

    # common helpers for integrity checks
    @classmethod
    def age_sum_for_dict(cls, data, age, fields):
        return sum([data.get('{}_{}'.format(age, field), 0)
                    for field in fields])

    @classmethod
    def total_start_for(cls, data, age):
        return cls.age_sum_for_dict(data, age,
                                    ['total_start_m', 'total_start_f'])

    @classmethod
    def total_in_for(cls, data, age):
        return cls.age_sum_for_dict(data, age, ['total_in_m', 'total_in_f'])

    @classmethod
    def grand_total_in_for(cls, data, age):
        if cls.IS_URENI:
            fields = ['total_in', 'referred']
        else:
            fields = ['total_in', 'transferred']
        return cls.age_sum_for_dict(data, age, fields)

    @classmethod
    def total_out_for(cls, data, age):
        return cls.age_sum_for_dict(data, age, ['total_out_m', 'total_out_f'])

    @classmethod
    def grand_total_out_for(cls, data, age):
        if cls.IS_URENI:
            fields = ['total_out', 'transferred']
        else:
            fields = ['total_out', 'referred']
        return cls.age_sum_for_dict(data, age, fields)

    @classmethod
    def total_end_for(cls, data, age):
        return cls.age_sum_for_dict(data, age, ['total_end_m', 'total_end_f'])

    @classmethod
    def expand_data_for(cls, data, age):
        for field in cls.uren_fields():
            if field in cls.silent_uren_fields(age):
                data.update({field: 0})

        data['total_start'] = cls.total_start_for(data, age)
        data['total_in'] = cls.total_in_for(data, age)
        data['grand_total_in'] = cls.grand_total_in_for(data, age)
        data['total_out'] = cls.total_out_for(data, age)
        data['grand_total_out'] = cls.grand_total_out_for(data, age)
        data['total_end'] = cls.total_end_for(data, age)
        return data
