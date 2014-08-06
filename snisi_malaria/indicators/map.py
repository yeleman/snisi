#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

from snisi_core.models.Projects import Cluster
from snisi_malaria.models import MalariaR
from snisi_malaria.indicators.common import MalariaIndicator
from snisi_core.models.Reporting import ExpectedReporting
from snisi_tools.caching import descendants_slugs

cluster = Cluster.get_or_none("malaria_monthly_routine")


class NumberOfHealthUnitsWithin(MalariaIndicator):
    name = "Nombre total de structures dans le district"

    def _compute(self):
        return ExpectedReporting.objects.filter(
            entity__type__slug='health_center',
            period=self.period).filter(
                entity__slug__in=descendants_slugs(cluster, self.entity.slug)
                + [self.entity.slug]
            ).count()


class NumberOfHealthUnitsInTime(MalariaIndicator):
    name = ("Nombre de structures ayant transmis leurs formulaires de "
            "collecte dans les délais prévus")

    def _compute(self):
        if self.is_hc():
            if self.expected and self.expected.satisfied \
                    and self.report.ON_TIME:
                return 1
            else:
                return 0
        if self.expected and self.expected.satisfied:
            return sum([1 for r in MalariaR.objects.filter(
                period=self.period,
                entity__slug__in=descendants_slugs(cluster, self.entity.slug))
                if r.ON_TIME])
            return self.report.nb_source_reports_arrived_on_time
        return None


class NumberOfHealthUnitsReporting(MalariaIndicator):
    name = "Nombre de structures ayant transmis leurs formulaires."
    is_yesno = True

    def _compute(self):
        if self.is_hc():
            if self.expected and self.expected.satisfied:
                return 1
            else:
                return 0
        if self.expected and self.expected.satisfied:
            return MalariaR.objects.filter(
                period=self.period,
                entity__slug__in=descendants_slugs(cluster,
                                                   self.entity.slug)).count()
            return self.report.nb_source_reports_arrived
        return None


class PercentageOfHealthUnitsReportingInTime(MalariaIndicator):
    name = ("Pourcentage de structures ayant transmis leurs données "
            "dans les délais prévus")
    is_ratio = True
    is_geo_friendly = True
    geo_section = "Données"
    is_yesno = True

    def _compute(self):
        try:
            return NumberOfHealthUnitsInTime.clone_from(self).data \
                / NumberOfHealthUnitsWithin.clone_from(self).data
        except:
            return 0


class PercentageOfHealthUnitsReporting(MalariaIndicator):
    name = "Pourcentage de structures ayant transmis leurs données"
    is_ratio = True
    is_geo_friendly = True
    geo_section = "Données"
    is_yesno = True

    def _compute(self):
        try:
            return NumberOfHealthUnitsReporting.clone_from(self).data \
                / NumberOfHealthUnitsWithin.clone_from(self).data
        except:
            return 0


class TotalInpatientMalaria(MalariaIndicator):
    name = ("Pourcentage des cas de paludisme hospitalisés "
            "chez les 5 ans et plus")
    is_ratio = True
    is_geo_friendly = True
    geo_section = "Prise en Charge (PEC)"
    # is_yesno = True

    def _compute(self):
        return self.divide(self.report.total_malaria_inpatient,
                           self.report.total_inpatient_all_causes)


class TotalConfirmedMalariaCases(MalariaIndicator):
    name = "Pourcentage des cas de paludisme confirmés par GE/TDR tout age"
    is_ratio = True
    is_geo_friendly = True
    geo_section = "Prise en Charge (PEC)"
    # is_yesno = True

    def _compute(self):
        return self.divide(self.report.total_confirmed_malaria_cases,
                           self.report.total_tested_malaria_cases)


class TotalTestedMalariaCases(MalariaIndicator):
    name = "Pourcentage des cas suspects testés par GE/TDR tout age"
    is_ratio = True
    is_geo_friendly = True
    geo_section = "Prise en Charge (PEC)"
    # is_yesno = True

    def _compute(self):
        return self.divide(self.report.total_tested_malaria_cases,
                           self.report.total_suspected_malaria_cases)


class TotalU5ConfirmedMalariaCases(MalariaIndicator):
    name = ("Pourcentage des cas de paludisme confirmés par GE/TDR "
            "chez les moins de 5ans")
    is_ratio = True
    is_geo_friendly = True
    geo_section = "Prise en Charge (PEC)"
    # is_yesno = True

    def _compute(self):
        return self.divide(self.report.u5_total_tested_malaria_cases,
                           self.report.u5_total_suspected_malaria_cases)


class TotalU5TestedMalariaCases(MalariaIndicator):
    name = ("Pourcentage des cas suspects testés par GE/TDR "
            "chez les moins de 5ans")
    is_ratio = True
    is_geo_friendly = True
    geo_section = "Prise en Charge (PEC)"
    # is_yesno = True

    def _compute(self):
        return self.divide(self.report.u5_total_tested_malaria_cases,
                           self.report.u5_total_suspected_malaria_cases)


class TotalPWConfirmedMalariaCases(MalariaIndicator):
    name = ("Pourcentage des cas de paludisme confirmés par GE/TDR "
            "chez les femmes enceintes")
    is_ratio = True
    is_geo_friendly = True
    geo_section = "Prise en Charge (PEC)"
    # is_yesno = True

    def _compute(self):
        return self.divide(self.report.pw_total_confirmed_malaria_cases,
                           self.report.pw_total_tested_malaria_cases)


class TotalPWTestedMalariaCases(MalariaIndicator):
    name = ("Pourcentage des cas suspects testés par GE/TDR "
            "chez les femmes enceintes")
    is_ratio = True
    is_geo_friendly = True
    geo_section = "Prise en Charge (PEC)"
    # is_yesno = True

    def _compute(self):
        return self.divide(self.report.pw_total_tested_malaria_cases,
                           self.report.pw_total_suspected_malaria_cases)


class TotalO5ACTTreatedMalariaCases(MalariaIndicator):
    name = ("Pourcentage des cas de paludisme simples confirmés et "
            "traités par CTA chez les 5ans et plus")
    is_ratio = True
    is_geo_friendly = True
    geo_section = "Prise en Charge (PEC)"
    # is_yesno = True

    def _compute(self):
        return self.divide(self.report.o5_total_treated_malaria_cases,
                           self.report.o5_total_confirmed_malaria_cases)


class TotalU5ACTTreatedMalariaCases(MalariaIndicator):
    name = ("Pourcentage des cas de paludisme simples confirmés et "
            "traités par CTA chez les moins de 5ans")
    is_ratio = True
    is_geo_friendly = True
    geo_section = "Prise en Charge (PEC)"
    # is_yesno = True

    def _compute(self):
        return self.divide(self.report.u5_total_treated_malaria_cases,
                           self.report.u5_total_confirmed_malaria_cases)


class HealthUnitsWithoutACTYouthStockout(MalariaIndicator):
    name = "Structures sans rupture de stock en CTA Adolescent"
    is_ratio = True
    is_geo_friendly = True
    geo_section = "Intrants"
    is_yesno = True

    def _compute(self):
        if self.is_hc():
            return not self.report.stockout_act_youth == self.report.YES

        nb_stockout = sum([bool(v == MalariaR.NO)
                           for v in self.all_hc_values('stockout_act_youth')])
        return self.divide(nb_stockout,
                           NumberOfHealthUnitsReporting.clone_from(self).data)


class HealthUnitsWithoutACTAdultStockout(MalariaIndicator):
    name = "Structures sans rupture de stock en CTA Adulte"
    is_ratio = True
    is_geo_friendly = True
    geo_section = "Intrants"
    is_yesno = True

    def _compute(self):
        if self.is_hc():
            return not self.report.stockout_act_adult == self.report.YES

        nb_stockout = sum([bool(v == MalariaR.NO)
                           for v in self.all_hc_values('stockout_act_adult')])
        return self.divide(nb_stockout,
                           NumberOfHealthUnitsReporting.clone_from(self).data)


class HealthUnitsWithoutACTChildrenStockout(MalariaIndicator):
    name = "Structures sans rupture de stock en CTA Nourisson-Enfant"
    is_ratio = True
    is_geo_friendly = True
    geo_section = "Intrants"
    is_yesno = True

    def _compute(self):
        if self.is_hc():
            return not self.report.stockout_act_children == self.report.YES

        nb_stockout = sum([bool(v == MalariaR.NO)
                           for v in
                           self.all_hc_values('stockout_act_children')])
        return self.divide(nb_stockout,
                           NumberOfHealthUnitsReporting.clone_from(self).data)


class HealthUnitsWithoutBednetStockout(MalariaIndicator):
    name = "Structures sans rupture de stock de MILD"
    is_ratio = True
    is_geo_friendly = True
    geo_section = "Intrants"
    is_yesno = True

    def _compute(self):
        if self.is_hc():
            return not self.report.stockout_bednet == self.report.YES

        nb_stockout = sum([bool(v == MalariaR.NO)
                           for v in self.all_hc_values('stockout_bednet')])
        return self.divide(nb_stockout,
                           NumberOfHealthUnitsReporting.clone_from(self).data)


class HealthUnitsWithoutRDTStockout(MalariaIndicator):
    name = "Structures sans rupture de stock de TDR"
    is_ratio = True
    is_geo_friendly = True
    geo_section = "Intrants"
    is_yesno = True

    def _compute(self):
        if self.is_hc():
            return not self.report.stockout_rdt == self.report.YES

        nb_stockout = sum([bool(v == MalariaR.NO)
                           for v in self.all_hc_values('stockout_rdt')])
        return self.divide(nb_stockout,
                           NumberOfHealthUnitsReporting.clone_from(self).data)


class HealthUnitsWithoutSPStockout(MalariaIndicator):
    name = "Structures sans rupture de stock de SP"
    is_ratio = True
    is_geo_friendly = True
    geo_section = "Intrants"
    is_yesno = True

    def _compute(self):
        if self.is_hc():
            return not self.report.stockout_sp == self.report.YES

        nb_stockout = sum([bool(v == MalariaR.NO)
                           for v in self.all_hc_values('stockout_sp')])
        return self.divide(nb_stockout,
                           NumberOfHealthUnitsReporting.clone_from(self).data)
