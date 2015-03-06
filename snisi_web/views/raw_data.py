#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
# from django.utils.translation import ugettext as _

from snisi_core.models.Periods import Period
from snisi_core.permissions import user_root_for
from snisi_core.models.Entities import Entity
from snisi_core.models.Reporting import ExpectedReporting, SNISIReport
from snisi_core.models.Projects import Cluster
from snisi_web.utils import entity_browser_context, ensure_entity_in_cluster
from snisi_core.permissions import provider_allowed_or_denied


@login_required
def browser(request,
            cluster_slug, entity_slug=None, period_str=None, **kwargs):

    context = {}
    period = None
    entity = None
    cluster = Cluster.get_or_none(cluster_slug)
    perm_slug = "access_{}".format(cluster.domain.slug)
    root = user_root_for(request.user, perm_slug)
    report_classes = cluster.domain \
        .import_from('expected.report_classes_for')(cluster)

    if not report_classes:
        raise Http404("Pas de ReportClass correspondant.")

    def period_from_strid(period_str, reportcls=None):
        period = None
        # find period from string or default to current reporting
        if period_str:
            try:
                period = Period.from_url_str(period_str).casted()
            except:
                pass
        if not period and reportcls:
            period = reportcls.current()

        return period
    period = period_from_strid(period_str, report_classes[0].period_class)

    # find entity or default to provider target
    entity = Entity.get_or_none(entity_slug) or root

    ensure_entity_in_cluster(cluster, entity)

    # check permissions on this entity and raise 403
    provider_allowed_or_denied(request.user, perm_slug, entity)

    entity_period = {'entity': entity, 'period': period}
    expecteds = []
    for report_class in report_classes:
        expecteds += list(ExpectedReporting.objects.filter(
            report_class__in=report_classes, **entity_period))

    expecteds = list(set(expecteds))

    # periods list a a list of all periods with a matching ReportClass
    all_periods = sorted(list(set(
        [e.period.casted()
         for e in ExpectedReporting.objects.filter(
            entity=entity,
            report_class__in=report_classes)
         ])), key=lambda x: x.start_on)

    # if request period is outside of all_periods, just take last of those
    if len(all_periods) and (period is None or period not in all_periods):
        period = all_periods[-1]

    context.update({
        'cluster': cluster,
        'periods': [(p.strid(), p) for p in reversed(all_periods)],
        'period': period,
        # 'entity': entity,
        'expecteds': expecteds,
        'expected': expecteds[0] if len(expecteds) > 0 else None
    })

    # JS entities browser
    context.update(entity_browser_context(
        root=root, selected_entity=entity,
        full_lineage=['country', 'health_region',
                      'health_district', 'health_center'],
        cluster=cluster))

    return render(request,
                  kwargs.get('template_name', 'raw_data.html'),
                  context)


def download_as_excel(request, report_receipt):
    report = SNISIReport.get_or_none(report_receipt)
    if report is None:
        raise Http404("Pas de rapport correspondant au reçu {}"
                      .format(report_receipt))

    if not report.validated:
        raise PermissionDenied("Impossible d'exporter un rapport non validé.")

    file_name, file_content = report.as_xls()
    file_content = file_content.getvalue()

    response = HttpResponse(file_content,
                            content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="%s"' % file_name
    response['Content-Length'] = len(file_content)

    return response
