#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import tempfile

from django.utils import timezone
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django import forms

from snisi_web.decorators import user_role_within
from snisi_tools.misc import get_from_snisi_apps, import_path


def handle_uploaded_file(f):
    """ stores temporary file as a real file for form upload """
    tfile = tempfile.NamedTemporaryFile(delete=False)
    for chunk in f.chunks():
        tfile.write(chunk)
    tfile.close()
    return tfile.name


def available_form_upload_types():
    return get_from_snisi_apps('xls_import.EXPORTED_FORMS', fusion_list=True)


def handle_report_upload(excel_form, form, provider):

    excel_form.set('submit_time', timezone.now())
    excel_form.set('submitter', provider)
    excel_form.check()
    if excel_form.is_valid():
        return excel_form.create_report(provider=provider)  # report, txt_msg
    else:
        return None, None


class ExcelUploadForm(forms.Form):

    reportcls = forms.ChoiceField(label="Type de rapport",
                                  choices=available_form_upload_types())
    report_file = forms.FileField(label="Fichier du rapport")

    def get_form_cls(self):
        return import_path(self.cleaned_data.get('reportcls'))


@login_required
@user_role_within(['charge_sis', 'dtc'])
def upload_form(request, template_name='upload_form.html'):

    context = {}
    excel_form = None
    handle_report_func = handle_report_upload

    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():

            filepath = handle_uploaded_file(request.FILES['report_file'])
            excel_form_cls = form.get_form_cls()
            domain = excel_form_cls.get_domain()
            if domain is not None:
                # Handling of report form might be custom to domain/report
                try:
                    handle_report_func = domain.import_from(
                        'upload.handle_report_upload', failsafe=False)
                except:
                    pass
            excel_form = excel_form_cls(filepath)

            new_report, text_message = handle_report_func(
                excel_form, form, request.user)

            if new_report is None:
                # messages.error(request, text_message)
                pass
            else:
                messages.success(request, text_message)
                return redirect('upload')

            context.update({'xlsform': excel_form})
        else:
            # django form validation errors
            pass
    else:
        form = ExcelUploadForm()

    context.update({'form': form})

    return render(request, template_name, context)
