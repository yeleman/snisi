#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

import reversion
from django.db import models
from django.db.models import Q
from django.db.models.query import QuerySet
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from snisi_core.models.common import pre_save_report, post_save_report
from snisi_core.models.Reporting import (SNISIReport,
                                         PeriodicAggregatedReportInterface,
                                         ReportStatusMixin,
                                         PERIODICAL_SOURCE, PERIODICAL_AGGREGATED)

class StockoutMixin(object):
    def has_stockouts(self):
        return self.filter(Q(male_condom=0) |
                           Q(female_condom=0) |
                           Q(oral_pills=0) |
                           Q(injectable=0) |
                           Q(iud=0) |
                           Q(implants=0) |
                           Q(female_sterilization=0) |
                           Q(male_sterilization=0))


class RHProductsQuerySet(QuerySet, ReportStatusMixin, StockoutMixin):
    pass


class RHProductsManager(models.Manager, ReportStatusMixin, StockoutMixin):
    def get_query_set(self):
        return RHProductsQuerySet(self.model, using=self._db)


class RHProductsR(SNISIReport):

    """ Complies with snisi_reporting.DataBrowser """

    YES = 'Y'
    NO = 'N'
    YESNO = {
        YES: _("Yes"),
        NO: _("No")
    }
    NOT_PROVIDED = -1
    SUPPLIES_AVAILABLE = 1
    SUPPLIES_NOT_AVAILABLE = 0
    SUPPLIES_NOT_PROVIDED = -1
    YESNOAVAIL = {
        SUPPLIES_AVAILABLE: _("Yes. Supplies available"),
        SUPPLIES_NOT_AVAILABLE: _("Yes. Supplies not available"),
        SUPPLIES_NOT_PROVIDED: _("No")
    }

    REPORTING_TYPE = PERIODICAL_SOURCE
    RECEIPT_FORMAT = "{period}-BDN/{rand}"
    UNIQUE_TOGETHER = ('period', 'entity')

    class Meta:
        app_label = 'snisi_reprohealth'
        verbose_name = _("RH Commodities Report")
        verbose_name_plural = _("RH Commodities Reports")

    # Services offered
    family_planning = models.BooleanField()
    delivery_services = models.BooleanField()

    # Modern contraceptive methods providded at the SDP
    male_condom = models.IntegerField(
        _("Male condom. Quantity in hand (pieces) or -1."))
    female_condom = models.IntegerField(
        _("Female condom. Quantity in hand (pieces) or -1."))
    oral_pills = models.IntegerField(
        _("Oral pills. Quantity in hand (cycles) or -1."))
    injectable = models.IntegerField(
        _("Injectable. Quantity in hand (vials) or -1."))
    iud = models.IntegerField(
        _("IUD. Quantity in hand (unit) or -1."))
    implants = models.IntegerField(
        _("Implants. Quantity in hand (unit) or -1."))
    female_sterilization = models.IntegerField(
        verbose_name=_("Female sterilization"),
        choices=YESNOAVAIL.items())
    male_sterilization = models.IntegerField(
        verbose_name=_("Male sterilization"),
        choices=YESNOAVAIL.items())

    # Availability of live-saving maternal/RH medecine
    amoxicillin_ij = models.IntegerField(
        _("Amoxicillin (Injectable). Quantity in hand (vials) or -1."))
    amoxicillin_cap_gel = models.IntegerField(
        _("Amoxicillin (capsule/gel). Quantity in hand (capsules) or -1."))
    amoxicillin_suspension = models.IntegerField(
        _("Amoxicillin (Suspension). Quantity in hand (vials) or -1."))
    azithromycine_tab = models.IntegerField(
        _("Azithromicine (tablet/gel). Quantity in hand (tablets) or -1."))
    azithromycine_suspension = models.IntegerField(
        _("Azithromicine (Suspension). Quantity in hand (bottles) or -1."))
    benzathine_penicillin = models.IntegerField(
        _("Benzatine penicillin. Quantity in hand (vials) or -1."))
    cefexime = models.IntegerField(
        _("Cefexime. Quantity in hand (tablets) or -1."))
    clotrimazole = models.IntegerField(
        _("Clotrimazole. Quantity in hand (tablets) or -1."))
    ergometrine_tab = models.IntegerField(
        _("Ergometrine (tablets). Quantity in hand (tablets) or -1."))
    ergometrine_vials = models.IntegerField(
        _("Ergometrine (vials). Quantity in hand (vials) or -1."))
    iron = models.IntegerField(
        _("Iron. Quantity in hand (tablets) or -1."))
    folate = models.IntegerField(
        _("Folate. Quantity in hand (tablets) or -1."))
    iron_folate = models.IntegerField(
        _("Iron/Folate. Quantity in hand (tablets) or -1."))
    magnesium_sulfate = models.IntegerField(
        _("Magnesium Sulfate. Quantity in hand (vials) or -1."))
    metronidazole = models.IntegerField(
        _("Metronidazole (injectable). Quantity in hand (vials) or -1."))
    oxytocine = models.IntegerField(
        _("Oxytocine. Quantity in hand (vials) or -1."))
    ceftriaxone_500 = models.IntegerField(
        _("Ceftriaxone 500mg. Quantity in hand (tablets) or -1."))
    ceftriaxone_1000 = models.IntegerField(
        _("Ceftriaxone 1g. Quantity in hand (tablets) or -1."))

    objects = RHProductsManager()
    rhproducts = RHProductsManager()

    def add_data(self, family_planning,
                 delivery_services,
                 male_condom,
                 female_condom,
                 oral_pills,
                 injectable,
                 iud,
                 implants,
                 female_sterilization,
                 male_sterilization,
                 amoxicillin_ij,
                 amoxicillin_cap_gel,
                 amoxicillin_suspension,
                 azithromycine_tab,
                 azithromycine_suspension,
                 benzathine_penicillin,
                 cefexime,
                 clotrimazole,
                 ergometrine_tab,
                 ergometrine_vials,
                 iron,
                 folate,
                 iron_folate,
                 magnesium_sulfate,
                 metronidazole,
                 oxytocine,
                 ceftriaxone_500,
                 ceftriaxone_1000):
        self.family_planning = family_planning
        self.delivery_services = delivery_services
        self.male_condom = male_condom
        self.female_condom = female_condom
        self.oral_pills = oral_pills
        self.injectable = injectable
        self.iud = iud
        self.implants = implants
        self.female_sterilization = female_sterilization
        self.male_sterilization = male_sterilization
        self.amoxicillin_ij = amoxicillin_ij
        self.amoxicillin_cap_gel = amoxicillin_cap_gel
        self.amoxicillin_suspension = amoxicillin_suspension
        self.azithromycine_tab = azithromycine_tab
        self.azithromycine_suspension = azithromycine_suspension
        self.benzathine_penicillin = benzathine_penicillin
        self.cefexime = cefexime
        self.clotrimazole = clotrimazole
        self.ergometrine_tab = ergometrine_tab
        self.ergometrine_vials = ergometrine_vials
        self.iron = iron
        self.folate = folate
        self.iron_folate = iron_folate
        self.magnesium_sulfate = magnesium_sulfate
        self.metronidazole = metronidazole
        self.oxytocine = oxytocine
        self.ceftriaxone_500 = ceftriaxone_500
        self.ceftriaxone_1000 = ceftriaxone_1000

    def fp_stockout_3methods(self):
        w = 0
        for f in ('male_condom', 'female_condom', 'oral_pills', 'injectable',
                  'iud', 'implants',
                  'female_sterilization', 'male_sterilization'):
            if getattr(self, f) == 0:
                w += 1
        return w >= 3

receiver(pre_save, sender=RHProductsR)(pre_save_report)
receiver(post_save, sender=RHProductsR)(post_save_report)

reversion.register(RHProductsR)


class AggRHProductsR(PeriodicAggregatedReportInterface, SNISIReport):

    REPORTING_TYPE = PERIODICAL_AGGREGATED
    INDIVIDUAL_CLS = RHProductsR
    UNIQUE_TOGETHER = [('period', 'entity'),]

    class Meta:
        app_label = 'snisi_reprohealth'
        verbose_name = _("Aggregated RH Commodities Report")
        verbose_name_plural = _("Aggregated RH Commodities Reports")

    # Services offered
    family_planning_provided = models.PositiveIntegerField()
    delivery_services_provided = models.PositiveIntegerField()

    # Modern contraceptive methods providded at the SDP
    male_condom_provided = models.PositiveIntegerField()
    male_condom_available = models.PositiveIntegerField()
    female_condom_provided = models.PositiveIntegerField()
    female_condom_available = models.PositiveIntegerField()
    oral_pills_provided = models.PositiveIntegerField()
    oral_pills_available = models.PositiveIntegerField()
    injectable_provided = models.PositiveIntegerField()
    injectable_available = models.PositiveIntegerField()
    iud_provided = models.PositiveIntegerField()
    iud_available = models.PositiveIntegerField()
    implants_provided = models.PositiveIntegerField()
    implants_available = models.PositiveIntegerField()

    female_sterilization_available = models.PositiveIntegerField()
    female_sterilization_provided = models.PositiveIntegerField()

    male_sterilization_available = models.PositiveIntegerField()
    male_sterilization_provided = models.PositiveIntegerField()

    # Availability of live-saving maternal/RH medecine
    amoxicillin_ij_provided = models.PositiveIntegerField()
    amoxicillin_ij_available = models.PositiveIntegerField()
    amoxicillin_cap_gel_provided = models.PositiveIntegerField()
    amoxicillin_cap_gel_available = models.PositiveIntegerField()
    amoxicillin_suspension_provided = models.PositiveIntegerField()
    amoxicillin_suspension_available = models.PositiveIntegerField()
    azithromycine_tab_provided = models.PositiveIntegerField()
    azithromycine_tab_available = models.PositiveIntegerField()
    azithromycine_suspension_provided = models.PositiveIntegerField()
    azithromycine_suspension_available = models.PositiveIntegerField()
    benzathine_penicillin_provided = models.PositiveIntegerField()
    benzathine_penicillin_available = models.PositiveIntegerField()
    cefexime_provided = models.PositiveIntegerField()
    cefexime_available = models.PositiveIntegerField()
    clotrimazole_provided = models.PositiveIntegerField()
    clotrimazole_available = models.PositiveIntegerField()
    ergometrine_tab_provided = models.PositiveIntegerField()
    ergometrine_tab_available = models.PositiveIntegerField()
    ergometrine_vials_provided = models.PositiveIntegerField()
    ergometrine_vials_available = models.PositiveIntegerField()
    iron_provided = models.PositiveIntegerField()
    iron_available = models.PositiveIntegerField()
    folate_provided = models.PositiveIntegerField()
    folate_available = models.PositiveIntegerField()
    iron_folate_provided = models.PositiveIntegerField()
    iron_folate_available = models.PositiveIntegerField()
    magnesium_sulfate_provided = models.PositiveIntegerField()
    magnesium_sulfate_available = models.PositiveIntegerField()
    metronidazole_provided = models.PositiveIntegerField()
    metronidazole_available = models.PositiveIntegerField()
    oxytocine_provided = models.PositiveIntegerField()
    oxytocine_available = models.PositiveIntegerField()

    ceftriaxone_500_provided = models.PositiveIntegerField()
    ceftriaxone_500_available = models.PositiveIntegerField()
    ceftriaxone_1000_provided = models.PositiveIntegerField()
    ceftriaxone_1000_available = models.PositiveIntegerField()

    indiv_sources = models.ManyToManyField(INDIVIDUAL_CLS,
        verbose_name=_(u"Primary. Sources"),
        blank=True, null=True,
        related_name='source_agg_%(class)s_reports')

    @classmethod
    def update_instance_with_indiv(cls, report, instance):

        cls.update_instance_with_indiv_meta(report, instance)

        for field in instance.data_fields():
            if field in ('family_planning', 'delivery_services'):
                if getattr(instance, field):
                    agg_field = "{}_provided".format(field)
                    setattr(report, agg_field,
                            getattr(report, agg_field, 0) + 1)
            elif field in ('female_sterilization', 'male_sterilization'):

                if getattr(instance, field, instance.SUPPLIES_NOT_PROVIDED) \
                    in (instance.SUPPLIES_AVAILABLE,
                        instance.SUPPLIES_NOT_AVAILABLE):

                    prov_field = "{}_provided".format(field)
                    setattr(report, prov_field,
                            getattr(report, prov_field, 0) + 1)

                    if getattr(instance, field, instance.SUPPLIES_NOT_PROVIDED) \
                       == instance.SUPPLIES_AVAILABLE:

                        avail_field = "{}_available".format(field)
                        setattr(report, avail_field, getattr(report, avail_field, 0) + 1)
            else:
                if getattr(instance, field, instance.NOT_PROVIDED) != instance.NOT_PROVIDED:

                    prov_field = "{}_provided".format(field)
                    setattr(report, prov_field,
                            getattr(report, prov_field, 0) + 1)

                    if getattr(instance, field, instance.NOT_PROVIDED) > 0:
                        avail_field = "{}_available".format(field)
                        setattr(report, avail_field, getattr(report, avail_field, 0) + 1)

    @classmethod
    def update_instance_with_agg(cls, report, instance):

        cls.update_instance_with_agg_meta(report, instance)

        for field in cls.data_fields():
            setattr(report, field,
                    getattr(report, field, 0) + getattr(instance, field, 0))


receiver(pre_save, sender=AggRHProductsR)(pre_save_report)
receiver(post_save, sender=AggRHProductsR)(post_save_report)

reversion.register(AggRHProductsR)
