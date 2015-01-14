#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging

from django.core.management.base import BaseCommand

from snisi_core.models.Periods import MonthPeriod
from snisi_core.models.Reporting import (ExpectedReporting)
from snisi_core.models.Projects import Cluster

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):

        period = MonthPeriod.current().previous()
        cluster = Cluster.get_or_none("nutrition_routine")

        districts = [e.casted() for e in cluster.members()
                     if e.type.slug == 'health_district']

        print("DISTRICT,ATTENDUS,ARRIVÉS,COMPLÉTUDE")
        tot_nb_exp = 0
        tot_nb_arr = 0

        for district in districts:
            exps = ExpectedReporting.objects.filter(
                period=period, entity__parent__parent=district,
                report_class__slug='nutrition_monthly_routine')
            nb_exp = exps.count()
            nb_arr = exps.filter(
                completion_status=ExpectedReporting.COMPLETION_COMPLETE) \
                .count()

            tot_nb_exp += nb_exp
            tot_nb_arr += nb_arr

            pc = nb_arr / float(nb_exp)

            print("{ds},{exp},{arr},{pc}".format(
                ds=district.name, exp=nb_exp, arr=nb_arr, pc=pc))

        tot_pc = tot_nb_arr / float(tot_nb_exp)
        print("TOTAL,{exp},{arr},{pc}".format(exp=tot_nb_exp,
                                              arr=tot_nb_arr, pc=tot_pc))
