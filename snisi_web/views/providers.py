#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

from django import forms
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import Http404
from django.utils.translation import ugettext as _, ugettext_lazy
from django.contrib.auth.decorators import login_required

# from snisi_web.decorators import provider_required
from snisi_web import default_context
from snisi_core.models.Providers import Provider
from snisi_core.models.Numbers import PhoneNumberType, PhoneNumber
from snisi_tools.numbers import (phonenumber_repr, normalized_phonenumber,
                                 phonenumber_cleaned, operator_from_malinumber)
from snisi_web.views.admin import ProviderRoleLocationForm


class PhoneNumberForm(forms.Form):

    identity = forms.CharField(
        max_length=75, label='',
        help_text=_("If not a Mali number, use +indicator syntax."),
        widget=forms.TextInput(
            attrs={'class': 'pure-input-1-3',
                   'placeholder': _("Phone number...")}))

    def clean_identity(self):
        numbersent = self.cleaned_data.get('identity')
        normalized = normalized_phonenumber(numbersent)
        if normalized is None:
            raise forms.ValidationError(_("Invalid Phone Number: %(value)s"),
                                        code='invalid',
                                        params={'value': numbersent})
        if PhoneNumber.objects.filter(identity=normalized).count():
            pn = PhoneNumber.objects.get(identity=normalized)
            raise forms.ValidationError(
                _("Phone Number already in use by %(value)s"),
                code='invalid',
                params={'value': pn.provider})
        return normalized


class ProviderForm(forms.ModelForm):

    class Meta:
        model = Provider
        fields = ['gender', 'title', 'maiden_name', 'first_name',
                  'middle_name', 'last_name', 'email', 'position']


class ProviderPasswordForm(forms.Form):
    password1 = forms.CharField(max_length=100,
                                label=ugettext_lazy("New Password"),
                                widget=forms.PasswordInput(render_value=False))
    password2 = forms.CharField(max_length=100,
                                label=ugettext_lazy("Confirm New Password"),
                                widget=forms.PasswordInput(render_value=False))

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if not password2:
            raise forms.ValidationError(_("You must confirm your password"))
        if password1 != password2:
            raise forms.ValidationError(_("Your passwords do not match"))
        return password2


@login_required
def edit_profile(request, username=None, **kwargs):
    context = default_context()
    is_update = username is not None

    if is_update:
        if not request.user.role.slug in ['snisi_admin', 'snisi_tech']:
            raise PermissionDenied
        provider = Provider.get_or_none(username)
        if not provider:
            raise Http404("Provider `{}` not found!".format(username))
        redirect_view = 'profile_update'
    else:
        provider = request.user
        redirect_view = 'profile'

    is_password = 'password1' in request.POST
    is_newphone = 'identity' in request.POST

    # creating default forms for no-action-yet
    form = ProviderForm(instance=provider)
    passwd_form = ProviderPasswordForm()
    phone_form = PhoneNumberForm()

    # main infos form being sent
    if request.method == 'POST' and not is_password and not is_newphone:
        form = ProviderForm(request.POST)
        if form.is_valid() and not is_password:
            provider.gender = form.cleaned_data.get('gender')
            provider.title = form.cleaned_data.get('title')
            provider.maiden_name = form.cleaned_data.get('maiden_name')
            provider.first_name = form.cleaned_data.get('first_name')
            provider.middle_name = form.cleaned_data.get('middle_name')
            provider.last_name = form.cleaned_data.get('last_name')
            provider.position = form.cleaned_data.get('position')
            provider.email = form.cleaned_data.get('email')
            provider.phone_number = form.cleaned_data.get('phone_number')
            provider.phone_number_extra = \
                form.cleaned_data.get('phone_number_extra')
            provider.save()
            messages.success(request, _("Profile details updated."))
            if is_update:
                return redirect(redirect_view, username=provider.username)
            else:
                return redirect(redirect_view)
        else:
            messages.warning(request,
                             _("Your request failed. See bellow."))

    # password change form
    if request.method == 'POST' and is_password:
        passwd_form = ProviderPasswordForm(request.POST)
        if passwd_form.is_valid() and is_password:
            provider.set_password(
                passwd_form.cleaned_data.get('password1'))
            provider.save()
            messages.success(request, _("Password updated."))
            if is_update:
                return redirect(redirect_view, username=provider.username)
            else:
                return redirect('logout')
        else:
            messages.warning(request,
                             _("Your password change request failed. "
                               " See bellow."))

    # new phone number form
    if request.method == 'POST' and is_newphone:
        phone_form = PhoneNumberForm(request.POST)
        if phone_form.is_valid() and is_newphone:
            identity = phone_form.cleaned_data.get('identity')
            indicator, number = phonenumber_cleaned(identity)
            operator = operator_from_malinumber(identity)
            if number.startswith('7229'):
                type_slug = 'flotte'
            else:
                if PhoneNumberType.objects.filter(
                        slug='perso_{}'.format(operator)).count():
                    type_slug = 'perso_{}'.format(operator)
                else:
                    type_slug = 'perso_other'

            category = PhoneNumberType.objects.get(slug=type_slug)
            try:
                PhoneNumber.objects.create(
                    identity=identity,
                    category=category,
                    priority=category.priority,
                    provider=provider)
                messages.success(request,
                                 _("Added new phone number: {}")
                                 .format(phonenumber_repr(identity)))
            except Exception as e:
                messages.error(request,
                               _("Error in creating phone number {}.\n{}")
                               .format(phonenumber_repr(identity), e))
            if is_update:
                return redirect(redirect_view, username=provider.username)
            else:
                return redirect(redirect_view)
        else:
            messages.warning(request,
                             _("Your new phone request failed. See bellow."))

    context.update({'form': form,
                    'passwd_form': passwd_form,
                    'is_update': is_update,
                    'phone_form': phone_form,
                    'provider': provider})

    return render(request,
                  kwargs.get('template_name', "misc/edit_profile.html"),
                  context)


@login_required
def public_profile(request, username, **kwargs):
    context = {'has_admin': True}

    provider = Provider.get_or_none(username, with_inactive=True)
    if not provider:
        raise Http404("Provider `{}` not found!".format(username))
    context.update({'provider': provider})

    # admin
    if request.method == 'POST':
        previous_role = provider.role
        previous_location = provider.location.casted()
        form = ProviderRoleLocationForm(request.POST,
                                        instance=provider,
                                        requester=request.user)
        if form.is_valid():
            if form.cleaned_data['location'] == previous_location \
                    and form.cleaned_data['role'] == previous_role:
                messages.warning(request,
                                 _("New role and location are identical to "
                                   "previous ones. No change made."))
            else:
                provider.role = form.cleaned_data['role']
                provider.location = form.cleaned_data['location']
                provider.save()
                messages.success(request,
                                 _("{provider} has been moved from “{prole} at"
                                   " {plocation}” to “{role} at {location}”.")
                                 .format(provider=provider.get_full_name(),
                                         prole=previous_role,
                                         plocation=previous_location,
                                         role=provider.role,
                                         location=provider.location))

            return redirect('public_profile', username=username)
    else:
        form = ProviderRoleLocationForm(instance=provider,
                                        requester=request.user)
    context.update({'form': form})

    return render(request,
                  kwargs.get('template_name', "misc/public_profile.html"),
                  context)


def remove_number_from_profile(request, identity):

    try:
        pn = PhoneNumber.objects.get(identity=identity,
                                     provider=request.user)
    except:
        messages.error(request,
                       _("Unable to remove phone number {} from your account."
                         "Either it doesn't exist or it's not yours.")
                       .format(phonenumber_repr(identity)))
        return redirect('profile')

    pn.delete()
    messages.success(request,
                     _("Removed phone number: {}")
                     .format(phonenumber_repr(identity)))
    return redirect('profile')
