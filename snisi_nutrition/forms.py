#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging

from django import forms

from snisi_core.models.Entities import Entity
from snisi_nutrition.models.URENAM import URENAMNutritionR, AggURENAMNutritionR
from snisi_nutrition.models.URENAS import URENASNutritionR, AggURENASNutritionR
from snisi_nutrition.models.URENI import URENINutritionR, AggURENINutritionR
from snisi_nutrition.models.Stocks import NutritionStocksR, AggNutritionStocksR
from snisi_nutrition.models.Monthly import NutritionR, AggNutritionR

logger = logging.getLogger(__name__)


class NutritionRFormIFace(object):

    def initialize(self, is_agg, instance):
        entity = Entity.get_or_none(instance.entity.slug)

        uren_map = {
            'urenam': AggURENAMNutritionR if is_agg else URENAMNutritionR,
            'urenas': AggURENASNutritionR if is_agg else URENASNutritionR,
            'ureni': AggURENINutritionR if is_agg else URENINutritionR,
            'stocks': AggNutritionStocksR if is_agg else NutritionStocksR
        }

        float_fields = ['supercereal_initial',
                        'supercereal_received',
                        'supercereal_used',
                        'supercereal_lost']

        for uren, rcls in uren_map.items():

            if uren != 'stocks' and \
                    not getattr(entity, 'has_{}'.format(uren)) and not is_agg:
                continue

            report = getattr(instance, '{}_report'.format(uren))

            for field in rcls.data_fields():
                ffcls = forms.FloatField \
                    if field in float_fields else forms.IntegerField
                ff = ffcls(
                    label=rcls.field_name(field),
                    required=True,
                    min_value=0,
                    localize=False,
                    initial=getattr(report, field))
                self.fields['{}_{}'.format(uren, field)] = ff


class NutritionRForm(forms.ModelForm, NutritionRFormIFace):

    class Meta:
        model = NutritionR
        fields = []

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        super(NutritionRForm, self).__init__(*args, **kwargs)
        self.initialize(False, instance)


class AggNutritionRForm(forms.ModelForm, NutritionRFormIFace):

    class Meta:
        model = AggNutritionR
        fields = []

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        super(AggNutritionRForm, self).__init__(*args, **kwargs)
        self.initialize(True, instance)
