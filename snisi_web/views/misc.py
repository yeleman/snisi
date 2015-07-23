#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

from django.contrib import messages
from django import forms
from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _, ugettext_lazy
from django.conf import settings

from snisi_web import default_context
from snisi_tools.numbers import phonenumber_repr
from snisi_tools.emails import send_email


def contact_choices(contacts):
    """ returns (a[0], a[1] for a in a list """
    # SUPPORT_CONTACTS contains slug, name, email
    # we need only slug, name for contact form.
    return [(slug, info_dict.get('name', slug))
            for slug, info_dict in settings.SUPPORT_CONTACTS.items()]


class ContactForm(forms.Form):
    """ Simple contact form with recipient choice """

    name = forms.CharField(max_length=50,
                           required=True,
                           label=ugettext_lazy("Your Name"))

    email = forms.EmailField(required=False,
                             label=ugettext_lazy("Your e-mail address"))

    phone_number = forms.CharField(max_length=12,
                                   required=False,
                                   label=ugettext_lazy("Your phone number"))

    subject = forms.CharField(max_length=50,
                              required=False,
                              label=ugettext_lazy("Subject"))

    recipient = forms.ChoiceField(
        required=False, label=ugettext_lazy("Recipient"),
        choices=contact_choices(settings.SUPPORT_CONTACTS),
        help_text=_("Choose PNLP for operational "
                    "requests and ANTIM for "
                    "technical ones."))

    message = forms.CharField(
        required=True, label=ugettext_lazy("Your request"),
        widget=forms.Textarea(
            attrs={'placeholder': _("Your message here...")}))


def contact(request, *args, **kwargs):
    context = default_context({'category': 'contact'})

    if request.method == 'POST':

        form = ContactForm(request.POST)

        if form.is_valid():
            dest_mail = settings.SUPPORT_CONTACTS \
                .get(form.cleaned_data.get('email'), {}) \
                .get('email', settings.HOTLINE_EMAIL)

            mail_cont = {'provider': request.user,
                         'name': form.cleaned_data.get('name'),
                         'email': form.cleaned_data.get('email'),
                         'phone_number': form.cleaned_data.get('phone_number'),
                         'subject': form.cleaned_data.get('subject'),
                         'message': form.cleaned_data.get('message')}
            mail_cont.update(default_context())

            sent, sent_message = send_email(
                recipients=dest_mail,
                context=mail_cont,
                template='emails/support_request.txt',
                title_template='emails/title.support_request.txt')
            if sent:
                messages.success(request, _("Support request sent."))
                return redirect('support')
            else:
                messages.error(request, _("Unable to send request. Please "
                                          "try again later."))

    elif request.method == 'GET':
        if request.user.is_authenticated():
            initial_data = {
                'name': request.user,
                'email': request.user.email,
                'phone_number': phonenumber_repr(request.user.primary_phone())}
        else:
            initial_data = {}

        form = ContactForm(initial=initial_data)

    else:
        form = None

    context.update({'form': form})

    return render(request,
                  kwargs.get('template_name', "misc/contact.html"), context)
