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

from snisi_core.permissions import user_root_for
from snisi_core.models.Reporting import ExpectedReporting, SNISIReport
from snisi_core.models.Projects import Cluster
from snisi_web.utils import ensure_entity_in_cluster
from snisi_core.permissions import provider_allowed_or_denied

from snisi_web.utils import entity_periods_context


@login_required
def browser(request,
            cluster_slug, entity_slug=None, period_str=None,
            period_cls=None, report_cls=None, view_name=None, **kwargs):

    context = {}
    cluster = Cluster.get_or_none(cluster_slug)
    perm_slug = "access_{}".format(cluster.domain.slug)
    root = user_root_for(request.user, perm_slug)
    report_classes = cluster.domain \
        .import_from('expected.report_classes_for')(cluster)

    if report_cls is not None:
        report_classes = [rc for rc in report_classes
                          if rc.report_class in report_cls]

    if not report_classes:
        raise Http404("Pas de ReportClass correspondant.")

    context.update(entity_periods_context(
        request=request,
        root=root,
        cluster=cluster,
        view_name=view_name or "report_browser",
        entity_slug=entity_slug,
        report_cls=report_classes[0].report_class,
        perioda_str=period_str,
        periodb_str=None,
        period_cls=period_cls or report_classes[0].period_class,
        assume_previous=False,
        must_be_in_cluster=True,
        backlog_periods=2,
        single_period=True,
    ))

    period = context['perioda']
    entity = context['entity']

    ensure_entity_in_cluster(cluster, entity)

    # check permissions on this entity and raise 403
    provider_allowed_or_denied(request.user, perm_slug, entity)

    entity_period = {'entity': context['entity'], 'period': period}
    expecteds = []
    for report_class in report_classes:
        expecteds += list(ExpectedReporting.objects.filter(
            report_class__in=report_classes, **entity_period))

    expecteds = list(set(expecteds))

    context.update({
        'cluster': cluster,
        'periods': context['all_periods'],
        'period': period,
        'expecteds': expecteds,
        'expected': expecteds[0] if len(expecteds) > 0 else None
    })

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
