#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

import reversion
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404
from django.forms.models import modelform_factory

from snisi_core.models.Reporting import ExpectedValidation, SNISIReport
from snisi_web.decorators import user_role_within
from snisi_tools.misc import import_path


@login_required
@user_role_within(['charge_sis', 'dtc'])
def pending_validation_list(request, template_name='validation_list.html'):

    context = {}

    pending = ExpectedValidation.objects.filter(
        validating_entity=request.user.location,
        validating_role=request.user.role,
        validation_period__start_on__lte=timezone.now(),
        validation_period__end_on__gt=timezone.now(),
        satisfied=False)

    context.update({'pending_list': pending})

    return render(request, template_name, context)


@login_required
@user_role_within(['charge_sis'])
def edit_report(request, report_receipt, **kwargs):
    context = {}

    report = SNISIReport.get_or_none(report_receipt)
    if report is None:
        raise Http404

    # mark report as validated
    expected_val = report.expected_validations.get()

    if not expected_val.validation_period.casted().contains(timezone.now()):
        messages.error(request, "Impossible de valider ce rapport en dehors "
                                "de la période de validation ({})"
                                .format(expected_val.validation_period))
        return redirect('validation')

    context.update({'report': report,
                    'edit_template': "report/edit_{}.html"
                                     .format(report.report_class().slug)})

    ReportFormCls = modelform_factory(model=report.casted().__class__,
                                      fields=report.data_fields())

    if request.method == 'POST':
        form = ReportFormCls(request.POST, instance=report)
        if form.is_valid():

            integrity_cls = import_path(report.INTEGRITY_CHECKER, failsafe=True)
            if not integrity_cls is None:
                data_checker = integrity_cls()
                for field in report.data_fields():
                    data_checker.set(field, form.cleaned_data.get(field))

                data_checker.check()
                if data_checker.is_valid():

                    new_report = form.save(commit=False)
                    new_report.modified_by = request.user
                    new_report.modified_on = timezone.now()

                    try:
                        with reversion.create_revision():
                            new_report.save()
                            reversion.set_user(request.user)
                    except:
                        messages.error(request,
                                       "Erreur lors de l'enregistrement des "
                                       "modifications du rapport.\nMerci de "
                                       "réessayer. Si le problème persiste, "
                                       "contactez la Hotline.")
                    else:
                        text_message = ("Données enregistrées pour {}. "
                                        "Le rapport n'est toujours pas validé !"
                                        .format(report))
                        messages.info(request, text_message)
                else:
                    # messages.error(request, "Données incorrectes")
                    text_message = None
                context.update({'data_checker': data_checker,
                                'text_message': text_message})

        else:
            # django form validation errors
            pass
    else:
        form = ReportFormCls(instance=report)

    context.update({'form': form})

    return render(request,
                  kwargs.get('template_name', 'validation_edit.html'),
                  context)


@login_required
@user_role_within(['charge_sis'])
def do_validation(request, report_receipt, **kwargs):
    report = SNISIReport.get_or_none(report_receipt)
    if report is None:
        raise Http404("No report for receipt {}".format(report_receipt))

    # mark report as validated
    expected_val = report.expected_validations.get()

    if not expected_val.validation_period.casted().contains(timezone.now()):
        messages.error(request, "Impossible de valider ce rapport en dehors "
                                "de la période de validation ({})"
                                .format(expected_val.validation_period))
    else:
        expected_val.acknowledge_validation(
            validated=True,
            validated_by=request.user,
            validated_on=timezone.now(),
            auto_validated=False)

        # confirm validation
        messages.success(request, "Le rapport {cls} nº {receipt} pour {period} "
                                  "a été validé par {by}"
                                  .format(cls=report.report_class(),
                                          receipt=report.receipt,
                                          period=report.period,
                                          by=report.validated_by))

    return redirect('validation')
