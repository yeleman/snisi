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

    # Disable direct edit/validation of this report type (always through NutR)
    no_edition = True

    IS_URENAM = False
    IS_URENAS = False
    IS_URENI = False

    AGE_LABELS = {
        'u6': "0-6m",  # URENI
        'u23o6': "6-23m",  # URENAM
        'u59o23': "23-59m",  # URENAM
        'u59o6': "6-59m",  # URENAS, URENI
        'o59': "59m+",  # URENAM, URENAS, URENI
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
                           'healed', 'deceased', 'abandon', 'not_responding',
                           'total_out_m', 'total_out_f']
            if age == 'pw':
                fields += ['total_start_m', 'total_in_m',
                           'total_out_m', 'total_end_m']

        return list(set(fields))

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
        return cls.age_sum_for_dict(data, age, ['total_in', 'transferred'])

    @classmethod
    def total_out_for(cls, data, age):
        return cls.age_sum_for_dict(data, age, ['total_out_m', 'total_out_f'])

    @classmethod
    def grand_total_out_for(cls, data, age):
        return cls.age_sum_for_dict(data, age, ['total_out', 'referred'])

    @classmethod
    def total_end_for(cls, data, age):
        return cls.age_sum_for_dict(data, age, ['total_end_m', 'total_end_f'])

    @classmethod
    def expand_data_for(cls, data, age):
        for field in cls.uren_fields():
            afield = '{age}_{field}'.format(age=age, field=field)
            if field in cls.silent_uren_fields(age):
                data.update({afield: 0})

        data.update(
            {'{}_total_start'.format(age):
             cls.total_start_for(data, age)})
        data.update(
            {'{}_total_in'.format(age):
             cls.total_in_for(data, age)})
        data.update(
            {'{}_grand_total_in'.format(age):
             cls.grand_total_in_for(data, age)})
        data.update(
            {'{}_total_out'.format(age):
             cls.total_out_for(data, age)})
        data.update(
            {'{}_grand_total_out'.format(age):
             cls.grand_total_out_for(data, age)})
        data.update(
            {'{}_total_end'.format(age):
             cls.total_end_for(data, age)})
        return data

    def age_lines(self):
        def fdata(age, field):
            return {
                'slug': "{}_{}".format(age, field),
                'full_slug': "urenam_{}_{}".format(age, field),
                'value': getattr(self, "{}_{}".format(age, field), 0)
            }
        lines = []
        for age in self.age_groups():
            line = {'label': self.age_str(age),
                    'age': age,
                    'fields': [fdata(age, field)
                               for field in self.uren_fields()
                               if field not in self.silent_uren_fields(age)]}
            lines.append(line)
        return lines

    # TOTALS FOR ALL AGES
    def total_for(self, field):
        return sum([getattr(self, "{}_{}".format(age, field), 0)
                    for age in self.age_groups()])

    @property
    def total_start(self):
        return self.total_for('total_start')

    @property
    def total_start_m(self):
        return self.total_for('total_start_m')

    @property
    def total_start_f(self):
        return self.total_for('total_start_f')

    @property
    def new_cases(self):
        return self.total_for('new_cases')

    @property
    def returned(self):
        return self.total_for('returned')

    @property
    def total_in(self):
        return self.total_for('total_in')

    @property
    def total_in_m(self):
        return self.total_for('total_in_m')

    @property
    def total_in_f(self):
        return self.total_for('total_in_f')

    @property
    def transferred(self):
        return self.total_for('transferred')

    @property
    def grand_total_in(self):
        return self.total_for('grand_total_in')

    @property
    def healed(self):
        return self.total_for('healed')

    @property
    def deceased(self):
        return self.total_for('deceased')

    @property
    def abandon(self):
        return self.total_for('abandon')

    @property
    def not_responding(self):
        return self.total_for('not_responding')

    @property
    def total_out(self):
        return self.total_for('total_out')

    @property
    def total_out_m(self):
        return self.total_for('total_out_m')

    @property
    def total_out_f(self):
        return self.total_for('total_out_f')

    @property
    def referred(self):
        return self.total_for('referred')

    @property
    def grand_total_out(self):
        return self.total_for('grand_total_out')

    @property
    def total_end(self):
        return self.total_for('total_end')

    @property
    def total_end_m(self):
        return self.total_for('total_end_m')

    @property
    def total_end_f(self):
        return self.total_for('total_end_f')
