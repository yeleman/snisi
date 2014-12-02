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


def handle_report_edition(report, form, provider):

    integrity_cls = import_path(report.INTEGRITY_CHECKER,
                                failsafe=True)
    if integrity_cls is not None:
        data_checker = integrity_cls()
        for field in report.data_fields():
            data_checker.set(field, form.cleaned_data.get(field))

        # period & entity from report
        data_checker.set('period', report.period)
        data_checker.set('entity', report.entity)
        data_checker.set('submitter', provider)

        data_checker.check(is_edition=True)
        if data_checker.is_valid():

            new_report = form.save(commit=False)
            new_report.modified_by = provider
            new_report.modified_on = timezone.now()

            try:
                with reversion.create_revision():
                    new_report.save()
                    reversion.set_user(provider)
            except:
                return data_checker, None

            return data_checker, new_report
    return None, None


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

    pending = [ev for ev in pending
               if not getattr(ev.report.casted(), 'no_edition', False)]

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

    rcls = report.casted().__class__
    handle_report_func = handle_report_edition
    ReportFormCls = modelform_factory(model=rcls, fields=report.data_fields())
    domain = rcls.get_domain()
    if domain is not None:
        # Report Form Class might be custom based on Report Class
        try:
            ReportFormCls = domain.import_from(
                'validation.get_form_class_for')(rcls)
        except:
            pass
        # Handling of report form might be custom to domain/report
        try:
            handle_report_func = domain.import_from(
                'validation.handle_report_edition')
        except:
            pass

    if request.method == 'POST':
        form = ReportFormCls(request.POST, instance=report)
        if form.is_valid():

            data_checker, new_report = handle_report_func(
                report, form, request.user)

            if new_report is None:
                messages.error(request,
                               "Erreur lors de l'enregistrement des "
                               "modifications du rapport.\nMerci de "
                               "réessayer. Si le problème persiste, "
                               "contactez la Hotline.")
            else:
                text_message = ("Données enregistrées pour {}. "
                                "Le rapport n'est toujours "
                                "pas validé !".format(report))
                messages.info(request, text_message)

            context.update({'data_checker': data_checker})
        else:
            # django form validation errors
            pass
    else:
        form = ReportFormCls(instance=report)

    context.update({'form': form})

    return render(request,
                  kwargs.get('template_name', 'validation_edit.html'),
                  context)


def handle_do_validation(report, provider):
    # mark report as validated
    expected_val = report.expected_validations.get()

    if not expected_val.validation_period.casted().contains(timezone.now()):
        return (False, "Impossible de valider ce rapport en dehors "
                       "de la période de validation ({})"
                       .format(expected_val.validation_period))
    else:
        expected_val.acknowledge_validation(
            validated=True,
            validated_by=provider,
            validated_on=timezone.now(),
            auto_validated=False)

        # confirm validation
        return (True, "Le rapport {cls} nº {receipt} pour {period} "
                      "a été validé par {by}"
                      .format(cls=report.report_class(),
                              receipt=report.receipt,
                              period=report.period,
                              by=report.validated_by))


@login_required
@user_role_within(['charge_sis'])
def do_validation(request, report_receipt, **kwargs):
    report = SNISIReport.get_or_none(report_receipt)
    if report is None:
        raise Http404("No report for receipt {}".format(report_receipt))

    do_validation_func = handle_do_validation
    domain = report.get_domain()
    if domain is not None:
        try:
            do_validation_func = domain.import_from(
                'validation.do_validation', failsafe=False)
        except:
            pass

    success, message = do_validation_func(report, request.user)

    if success:
        messages.success(request, message)
    else:
        messages.error(request, message)

    return redirect('validation')
