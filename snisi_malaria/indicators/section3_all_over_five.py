#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

from snisi_malaria.indicators.common import MalariaIndicator
from snisi_malaria.indicators.section3 import TITLE as TITLE_3
from snisi_core.indicators import IndicatorTable, is_ref, ref_is, hide


class AllOverFiveInpatientAllCauses(MalariaIndicator):
    name = "Total des hospitalisations (toutes causes confondues)"

    def _compute(self):
        return sum([self.report.o5_total_inpatient_all_causes,
                    self.report.pw_total_inpatient_all_causes])


class AllOverFiveMalariaInpatient(MalariaIndicator):
    name = "Total des hospitalisations pour paludisme grave"

    def _compute(self):
        return sum([self.report.o5_total_malaria_inpatient,
                    self.report.pw_total_malaria_inpatient])


class AllOverFiveMalariaInpatientFigure(AllOverFiveMalariaInpatient):
    name = "% des hospitalisations pour paludisme grave"


class HospitalisationPlusde5ansTous(IndicatorTable):
    """ Tableau: Hospitalisation  chez les 5 ans et plus"""
    name = "Tableau 4.1c"
    title = "5 ans et plus"
    caption = "Hospitalisation chez les 5 ans et plus (tous)"
    rendering_type = 'table'
    add_percentage = True
    add_total = True

    INDICATORS = [
        is_ref(AllOverFiveInpatientAllCauses),
        ref_is(0)(AllOverFiveMalariaInpatient),
    ]


class ProportionHospitalisations(IndicatorTable):
    """ Graphe: Proportion des hospitalisations pour paludisme grave chez les

        personnes de 5 ans et plus (par rapport aux hospitalisations toutes
        causes confondues) """

    name = "Figure 4.1c"
    caption = ("Proportion des hospitalisations pour paludisme grave chez "
               "les personnes de 5 ans et plus (par rapport aux "
               "hospitalisations toutes causes confondues)")
    rendering_type = 'graph'
    as_percentage = True

    INDICATORS = [
        hide(is_ref(AllOverFiveInpatientAllCauses)),
        ref_is(0)(AllOverFiveMalariaInpatientFigure),
    ]


WIDGETS = [HospitalisationPlusde5ansTous, ProportionHospitalisations]
TITLE = "{} / 5 ans et plus (tous)".format(TITLE_3)
