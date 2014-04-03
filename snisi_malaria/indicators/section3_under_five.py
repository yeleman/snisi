#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

from snisi_malaria.indicators.common import gen_shortcut
from snisi_malaria.indicators.section3 import TITLE as TITLE_3
from snisi_core.indicators import IndicatorTable, is_ref, ref_is, hide


class HospitalisationMoinsde5ans(IndicatorTable):
    """ Tableau: Hospitalisation chez les moins de 5ans """

    name = "Tableau 4.1b"
    title = "Enfants moins de 5 ans"
    caption = "Hospitalisation chez les moins de 5ans"
    rendering_type = 'table'
    add_percentage = True
    add_total = True

    INDICATORS = [
        is_ref(gen_shortcut('u5_total_inpatient_all_causes',
                            "Total des hospitalisations (toutes causes confondues)")),
        ref_is(0)(gen_shortcut('u5_total_malaria_inpatient',
                               "Total des hospitalisations pour paludisme grave")),
    ]



class ProportionHospitalisations(IndicatorTable):
    """ Graphe: Proportion des hospitalisations pour paludisme grave chez les

        moins de5 ans (par rapport aux hospitalisations toutes causes
        confondues) """
    name = "Figure 4.1b"
    caption = ("Proportion des hospitalisations pour paludisme grave chez "
               "les moins de 5 ans (par rapport aux hospitalisations "
               "toutes causes confondues)")
    rendering_type = 'graph'
    as_percentage = True

    INDICATORS = [
        hide(is_ref(gen_shortcut('u5_total_inpatient_all_causes',
                            "Total des hospitalisations (toutes causes confondues)"))),
        ref_is(0)(gen_shortcut('u5_total_malaria_inpatient',
                               "Total des hospitalisations pour paludisme grave")),
    ]


WIDGETS = [HospitalisationMoinsde5ans, ProportionHospitalisations]
TITLE = "{} / Moins de 5 ans".format(TITLE_3)
