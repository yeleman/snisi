#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import json
import datetime

from optparse import make_option
from django.core.management.base import BaseCommand
from django.db import IntegrityError

from snisi_core.models.Roles import Role
from snisi_core.models.Providers import Provider
from snisi_core.models.Numbers import PhoneNumber, PhoneNumberType
from snisi_tools.datetime import datetime_from_iso, DEBUG_change_system_date
from snisi_tools.pnlp_import import entity_from
from snisi_tools.numbers import normalized_phonenumber

new_slug_matrix = {}

female_firstnames = ["Kardiatou", "Saran", "Salimata", "Djeneba", "Sadio",
                     "Emeline", "Ramata", "Mariam", "Monique",
                     "Aminata", "Baïni", "Alice", "Fatoumata",
                     "Fatouma", "Assitan", "Aminata", "Viviane",
                     "Anacleta", "Katie", "Kalidi", "Zana", "Djénéba Jeanne",
                     "Hidya", "Suzi", "Seriba", "Adélaïde", "Christine",
                     "Diakalia", "Abibatou", "Djéneba", "Aissata", "Adama",
                     "Rachel", "Fanta", "Sukanta", "Djénébou",
                     "Coumba", "Diahara", "Kadidia",
                     "Madina", "Sadia", "Bintou", "Cristina", "Keneko",
                     "Mintou", "Huberte", "Mama", "Clara"]

role_matrix = {
    'partners': 'partner',
    'district': 'charge_sis',
    'region': 'charge_sis',
    'cscom': 'dtc',
    'pnlp': 'central',
    'antim': 'snisi_tech',
    'national': 'central'}

maiden_names = ['Coulibaly', 'Traoré', 'Diarra', 'Diallo', 'Sougoué']

november = datetime.datetime(2011, 11, 30, 12, 0)
july = datetime.datetime(2012, 7, 31, 12, 0)


class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
        make_option('-f',
                    help='JSON export of all PNLP providers',
                    action='store',
                    dest='input_file'),
        make_option('-m',
                    help='JSON matrix of old and new codes',
                    action='store',
                    dest='matrix_input_file'),
        make_option('-u',
                    help='JSON matrix of old and new users',
                    action='store',
                    dest='matrix_input_user_file'),
        )

    def handle(self, *args, **options):
        global new_slug_matrix

        matrix_input_file = open(options.get('matrix_input_file'), 'r')
        matrix = json.load(matrix_input_file)
        users_matrix = json.load(open(options.get('matrix_input_user_file'), 'r'))
        get_entry = lambda l, new_username: [e for e in l if e['new_username'] == new_username][-1]

        new_slug_matrix = matrix['old_new']
        new_slug_matrix.update({
            'mali': 'mali',
            'segou': '2732',
            'bamako': '9GR8',
            'mopti': 'SSH3'})

        ssangare = {
            "date_joined": "2013-07-24T10:00:00",
            "entity": "maci1",
            "first_name": "Sidiki",
            "is_active": True,
            "is_staff": False,
            "is_superuser": False,
            "last_login": "2013-07-24T10:00:00",
            "last_name": "Sangaré",
            "password": "pbkdf2_sha256$12000$0chjcCnjHwuG$V3O/KjSLQLstLh3/IJHiPCMrSornNXaP5sbYhkGuR/A=",
            "phone_number": "+22370061548",
            "phone_number_extra": None,
            "pwhash": "aa",
            "role": "cscom",
            "username": "ssangare"
        }

        input_file = open(options.get('input_file'), 'r')
        malaria_users = json.load(input_file) + [ssangare,]

        # change date to NOVEMBER 11
        DEBUG_change_system_date(november, True)

        print("Removing all providers...")
        Provider.objects.all().delete()

        print("Creating Providers...")

        duplicates = {}
        missed_locations = []

        for provider_data in malaria_users:
            print(provider_data['username'])

            # If user has a changind location. Create with the old one.
            if provider_data['username'] in [i['new_username'] for i in users_matrix]:
                entry = get_entry(users_matrix, provider_data['username'])
                provider_data['entity'] = entry['old_entity']

            phone_number = normalized_phonenumber(provider_data['phone_number'])
            phone_number2 = normalized_phonenumber(provider_data['phone_number_extra'])
            try:
                provider_data['location'] = entity_from(new_slug_matrix[provider_data['entity']])
            except KeyError:
                missed_locations.append(provider_data['entity'])
                continue

            provider_data['last_login'] = datetime_from_iso(provider_data['last_login'])
            provider_data['date_joined'] = datetime_from_iso(provider_data['date_joined'])
            role_slug = role_matrix.get(provider_data['role'])
            provider_data['role'] = Role.objects.get(slug=role_slug)

            del(provider_data['entity'])
            del(provider_data['pwhash'])
            del(provider_data['phone_number'])
            del(provider_data['phone_number_extra'])

            fd = provider_data['first_name'].split()
            if len(fd) and fd[0] in maiden_names:
                provider_data.update({'maiden_name': fd[0]})
                fd = fd[1:]
                provider_data.update({'first_name': " ".join(fd)})

            if len(fd) > 1:
                provider_data.update({'first_name': fd[0],
                                      'middle_name': " ".join(fd[1:])})

            if provider_data['first_name'] in female_firstnames:
                provider_data.update({
                    'gender': Provider.FEMALE,
                    'title': Provider.MISTRESS})
            else:
                provider_data.update({
                    'gender': Provider.MALE,
                    'title': Provider.MISTER})

            if role_slug == 'dtc' or \
                provider_data['username'] in ('mkonat1', 'itraor', 'ktraor',
                                              'sfomba', 'sfomba1', 'olya',
                                              'olya1', 'tdackouo', 'bcamara',
                                              'akonate',):
                provider_data.update({'title': Provider.DOCTOR})

            if provider_data['username'] == 'maaa':
                provider_data['gender'] = Provider.FEMALE
                provider_data['first_name'] = "Baba"
                provider_data['last_name'] = "Moller"

            if provider_data['username'] == 'baaa':
                provider_data['first_name'] = "Faraba"
                provider_data['last_name'] = "Samaké"

            if provider_data['username'] == 'aaga':
                provider_data['first_name'] = "Abderhamane"
                provider_data['last_name'] = "Ag Alhousséiini"

            if provider_data['username'] == 'saaa':
                provider_data['gender'] = Provider.FEMALE
                provider_data['first_name'] = "Suzi"
                provider_data['last_name'] = "Svaen-oven"
                provider_data['title'] = Provider.MISS

            if provider_data['username'] == 'btraore':
                provider_data['is_active'] = False
                phone_number = phone_number2
                phone_number2 = normalized_phonenumber(None)

            if provider_data['username'] in ('shounton', 'sfomba',
                                             'olya1', 'mdiabat', 'blya1',
                                             'afadiga', 'jdoe', 'ttest',
                                             'tolytest'):
                continue

            provider = Provider(**provider_data)
            provider.save()

            for num in (phone_number, phone_number2):
                if not num is None and num not in ('+22300000000', '+22312345678'):
                    try:
                        p = PhoneNumber.from_guess(num, provider)
                        if num.startswith('+2237229'):
                            p.category = PhoneNumberType.objects.get(slug='flotte')
                            p.save()
                    except IntegrityError:
                        duplicates.update({
                            num: (provider, PhoneNumber.by_identity(num))})
            print(provider)

        # print("\n".join(missed_locations))

        # for number, providers in duplicates.items():
        #     print("{}:  {}".format(number, ",".join(list([unicode(p) for p in providers]))))


        print("Updating Providers...")
        # if updating (2012-07-31), change location and save
        DEBUG_change_system_date(july, True)
        for entry in users_matrix:
            print(entry)
            provider = Provider.objects.get(username=entry['new_username'])
            print(provider)

            provider.location = entity_from(new_slug_matrix[entry['new_entity']])
            provider.save()

        DEBUG_change_system_date(None, True)
