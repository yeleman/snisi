#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

# from django.contrib import messages
# from django.shortcuts import render, redirect
from django.shortcuts import render
from django.utils.translation import ugettext_lazy
from django.contrib.auth.decorators import login_required
from django import forms

# from mptt.fields import TreeNodeChoiceField

from snisi_core.models.Roles import Role
from snisi_core.models.Providers import Provider
from snisi_core.models.Entities import Entity
from snisi_core.models.Projects import Cluster
# from snisi_tools.sms import send_sms


# class AddressBookForm(forms.Form):

#     role = forms.ChoiceField(
#         label=ugettext_lazy("Role"),
#         choices=[
#             ('', _("All"))] + [(role.slug, role.name)
#                                for role in
#                                Role.objects.all().order_by('name')])
#     entity = TreeNodeChoiceField(queryset=Entity.objects.all(),
#                                  level_indicator='---',
#                                  label=ugettext_lazy("Entity"))


# class MessageForm(forms.Form):

#     text = forms.CharField(widget=forms.Textarea(), label=("Texte"))

#     def clean_text(self):
#         return self.cleaned_data.get('text')[:150]


class FilterForm(forms.Form):

    cluster = forms.ChoiceField(label=ugettext_lazy("Cluster"),
                                required=False, widget=forms.Select)
    role = forms.ChoiceField(label=ugettext_lazy("Role"),
                             required=False, widget=forms.Select)

    region = forms.ChoiceField(
        label="Région", choices=[],
        widget=forms.Select(
            attrs={'class': 'entity_filter', 'data-level': 'health_region'}))
    district = forms.CharField(
        label="District", required=False,
        widget=forms.Select(
            attrs={'class': 'entity_filter', 'data-level': 'health_district'}))
    health_area = forms.CharField(
        label="Aire Sanitaire", required=False,
        widget=forms.Select(
            attrs={'class': 'entity_filter', 'data-level': 'health_area'}))
    request = forms.CharField(
        label=ugettext_lazy("Recherche"),
        required=False,
        widget=forms.TextInput(attrs={'placeholder': "Nom de famille"}))

    def __init__(self, *args, **kwargs):
        super(FilterForm, self).__init__(*args, **kwargs)

        all_cluster = [
            ('#', "Tous")] + [(c.slug, c.name)
                              for c in Cluster.active.all().order_by('name')]
        all_role = [
            ('#', "Tous")] + [(r.slug, r.name)
                              for r in Role.objects.all().order_by('name')]
        all_region = [
            ("-1", "Toutes")] + [(e.slug, e.name)
                                 for e in Entity.objects.filter(
                                 type__slug='health_region')]

        self.fields['cluster'].choices = all_cluster
        self.fields['role'].choices = all_role
        self.fields['region'].choices = all_region

    def get_clean_location(self):
            ''' Returns sharpest Entity from the multiple selects '''
            is_empty = lambda l: l is None or l == "mali" or l == '-1'
            slug = None
            levels = ['region', 'district', 'health_area']
            while len(levels) and is_empty(slug):
                slug = self.cleaned_data.get(levels.pop()) or None

            if is_empty(slug):
                return None

            entity = Entity.get_or_none(slug)

            if entity is None:
                raise forms.ValidationError("Localité incorrecte.")

            return entity

    def clean_cluster(self):
        return Cluster.get_or_none(self.cleaned_data.get('cluster'))

    def clean_role(self):
        return Role.get_or_none(self.cleaned_data.get('role'))


@login_required
def addressbook(request, template='misc/addressbook.html'):
    context = {'category': 'addressbook'}

    if request.method == "POST":
        form = FilterForm(request.POST)

        if form.is_valid():

            location = form.get_clean_location()

            providers = Provider.active.all().order_by(
                'last_name', 'first_name')

            if form.cleaned_data.get('cluster'):
                providers = providers.filter(
                    location__participations__cluster__slug=form
                    .cleaned_data.get('cluster').slug)

            if form.cleaned_data.get('role'):
                providers = providers.filter(
                    role=form.cleaned_data.get('role'))

            if location:
                providers = providers.filter(
                    location__in=location.get_descendants(True))

            if form.cleaned_data.get('request'):
                providers = providers.filter(
                    last_name__icontains=form.cleaned_data.get('request'))

            # send milage
            context.update({'lineage_data': [
                # 'mali',
                form.cleaned_data.get('region'),
                form.cleaned_data.get('district'),
                form.cleaned_data.get('health_area')]})

            context.update({'providers': providers})
        else:
            pass

    else:
        form = FilterForm()

    context.update({'form': form})

    return render(request, template, context)
