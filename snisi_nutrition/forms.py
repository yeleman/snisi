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


class NutritionRForm(forms.ModelForm):

    class Meta:
        model = NutritionR
        fields = []

    def __init__(self, *args, **kwargs):
        super(NutritionRForm, self).__init__(*args, **kwargs)

        instance = kwargs.get('instance')
        entity = Entity.get_or_none(instance.entity.slug)

        uren_map = {
            'urenam': URENAMNutritionR,
            'urenas': URENASNutritionR,
            'ureni': URENINutritionR,
            'stocks': NutritionStocksR
        }

        for uren, rcls in uren_map.items():

            if uren != 'stocks' and not getattr(entity, 'has_{}'.format(uren)):
                continue

            report = getattr(instance, '{}_report'.format(uren))

            for field in rcls.data_fields():
                ff = forms.IntegerField(
                    label=rcls.field_name(field),
                    required=True,
                    initial=getattr(report, field))
                self.fields['{}_{}'.format(uren, field)] = ff
                logger.debug('{}_{}'.format(uren, field))
