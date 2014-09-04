#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import re

from py3compat import implements_to_string
import reversion
from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, UserManager,
                                        PermissionsMixin)
from django.utils.translation import ugettext_lazy as _, ugettext
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.core.mail import send_mail
from django.core import validators
from django.utils import timezone

from snisi_core.signals import logged_in, logged_out
from snisi_core.models.Actions import Action
from snisi_core.models.common import ActiveManager
from snisi_core.models.Roles import Role
from snisi_core.models.Entities import Entity
from snisi_core.models.Numbers import PhoneNumber


class ProviderManager(UserManager):

    def create_superuser(self, username, email, password, **extra_fields):
        u = self.create_user(username=username,
                             password=password,
                             **extra_fields)
        u.is_staff = True
        u.is_active = True
        u.is_superuser = True
        u.save(using=self._db)
        return u


@implements_to_string
class Provider(AbstractBaseUser, PermissionsMixin):

    MALE = 'male'
    FEMALE = 'female'
    UNKNOWN = 'unknown'
    GENDERS = {
        MALE: _("Man"),
        FEMALE: _("Woman"),
        UNKNOWN: _("Unknown")
    }

    MISTER = 'mister'
    MISTRESS = 'mistress'
    MISS = 'miss'
    DOCTOR = 'doctor'
    PROFESSOR = 'professor'

    TITLES = {
        MISTER: _("Mr."),
        MISTRESS: _("Mrs."),
        MISS: _("Miss"),
        DOCTOR: _("Dr."),
        PROFESSOR: _("Pr.")
    }

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        app_label = 'snisi_core'
        verbose_name = _("Provider")
        verbose_name_plural = _("Providers")

    username = models.CharField(
        _("username"), max_length=50, primary_key=True,
        help_text=_("Required. 50 characters or fewer. "
                    "Letters, numbers and @/./+/-/_ characters"),
        validators=[validators.RegexValidator(re.compile("^[\w.@+-]+$"),
                    _("Enter a valid username."), "invalid")])

    gender = models.CharField(max_length=30,
                              choices=GENDERS.items(),
                              default=UNKNOWN,
                              verbose_name=_("Gender"))
    title = models.CharField(max_length=50,
                             choices=TITLES.items(),
                             blank=True, null=True,
                             verbose_name=_("Title"))
    first_name = models.CharField(max_length=100, blank=True, null=True,
                                  verbose_name=_("First Name"))
    middle_name = models.CharField(max_length=100, blank=True, null=True,
                                   verbose_name=_("Middle Name"))
    last_name = models.CharField(max_length=100, blank=True, null=True,
                                 verbose_name=_("Last Name"))
    maiden_name = models.CharField(max_length=100, blank=True, null=True,
                                   verbose_name=_("Maiden Name"))
    position = models.CharField(max_length=250, blank=True, null=True,
                                verbose_name=_("Position"))

    role = models.ForeignKey(Role, default='guest', verbose_name=_("Role"))
    location = models.ForeignKey(Entity, default='mali',
                                 related_name='contacts',
                                 verbose_name=_("Location"))
    access_since = models.DateTimeField(default=timezone.now,
                                        verbose_name=_("Access Since"))

    email = models.EmailField(_("email address"), blank=True, null=True)
    is_staff = models.BooleanField(
        _("staff status"), default=False,
        help_text=_("Designates whether the user can "
                    "log into this admin site."))
    is_active = models.BooleanField(
        _("active"), default=True,
        help_text=_("Designates whether this user should be treated as "
                    "active. Unselect this instead of deleting accounts."))
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    # django manager first
    objects = ProviderManager()
    active = ActiveManager()

    def __str__(self):
        return self.name()

    @classmethod
    def get_or_none(cls, username, with_inactive=False):
        qs = cls.objects if with_inactive else cls.active
        try:
            return qs.get(username=username)
        except cls.DoesNotExist:
            return None

    @classmethod
    def get_at(cls, location, role_slug=None):
        qs = cls.active.filter(location__slug=location.slug)
        if role_slug is not None:
            qs.filter(role__slug=role_slug)
        return qs

    def save(self, *args, **kwargs):
        author = None
        if 'author' in kwargs.keys():
            author = kwargs.pop('author')

        if 'at' in kwargs.keys():
            at = kwargs.pop('at')
        else:
            at = timezone.now()

        create_revision = False

        try:
            last_version = reversion.get_unique_for_object(self)[0].field_dict
        except (IndexError, AttributeError, TypeError):
            create_revision = True
            last_version = {}

        for field in ('role', 'location', 'is_active'):
            if field == 'is_active':
                current_value = getattr(self, field, False)
            else:
                current_value = getattr(getattr(self, field), 'slug')
            if last_version.get(field, current_value) != current_value:
                create_revision = True
                break

        if create_revision:
            self.access_since = at
            with reversion.create_revision():
                super(Provider, self).save(*args, **kwargs)
                reversion.set_user(author)
        else:
            super(Provider, self).save(*args, **kwargs)

    def history(self):
        version_list = reversion.get_unique_for_object(self)
        updates = []
        for version in reversed(version_list):
            vdata = version.field_dict
            inside_date = vdata.get('access_since')
            updates.append({
                'is_active': vdata.get('is_active'),
                'role': Role.get_or_none(vdata.get('role')),
                'location': Entity.get_or_none(vdata.get('location')),
                'from': vdata.get('access_since'),
                # TODO: fix end date of access
                'to': None,
                'access': self.get_access(at=inside_date),
                'name': self.name(at=inside_date)
            })
        return updates

    def name(self, at=None):
        ''' prefered representation of the provider's name at given date '''
        return self.get_complete_name(at=at, with_position=False)

    # TODO: Add history support for string repr.
    def get_complete_name(self, with_position=True, at=None):
        data = self._name_parts()
        data.update({'title_full_name': self.get_title_full_name()})
        name = ugettext("{title_full_name}/{access}").format(**data)
        if not self.position or not self.position.strip() or not with_position:
            return name.strip()
        return ugettext("{name} ({position})") \
            .format(name=name, position=self.position).strip()

    def get_complete_name_position(self, at=None):
        return self.get_complete_name(at=at, with_position=True)

    def get_full_name(self):
        if not self.has_name_infos():
            return self.username.strip()
        return ugettext("{maiden}{first}{middle}{last}") \
            .format(**self._name_parts()).strip()

    def get_title_full_name(self):
        data = self._name_parts()
        data.update({'full_name': self.get_full_name()})
        return ugettext("{title}{full_name}").format(**data).strip()

    def get_short_name(self):
        if not self.has_name_infos():
            return self.username.strip()
        return ugettext("{first_i}{middle_i}{last}") \
            .format(**self._name_parts()).strip()

    def get_title_short_name(self):
        data = self._name_parts()
        data.update({'short_name': self.get_short_name()})
        return ugettext("{title}{short_name}").format(**data).strip()

    def get_access(self, at=None):
        if not self.is_active:
            return ugettext("Désactivé")
        if not self.location.level:
            return ugettext("{role}").format(role=self.role.name).strip()
        return ugettext("{role} à {location}") \
            .format(role=self.role.name, location=self.location).strip()

    def has_name_infos(self):
        return (self.first_name or self.middle_name
                or self.last_name or self.maiden_name)

    def _name_parts(self):
        empty = ""
        return {
            'position': "{}".format(self.position) if self.position else empty,
            'title': "{} "
            .format(self.TITLES.get(self.title)) if self.title else empty,
            'maiden': "{} "
            .format(self.maiden_name.upper()) if self.maiden_name else empty,
            'first': "{} "
            .format(self.first_name.title()) if self.first_name else empty,
            'first_i': "{}. "
            .format(self.first_name[0].title()) if self.first_name else empty,
            'middle': "{} "
            .format(self.middle_name.title()) if self.middle_name else empty,
            'middle_i': "{} "
            .format(self.middle_name[0].title())
            if self.middle_name else empty,
            'last': "{} "
            .format(self.last_name.upper()) if self.last_name else empty,
            'access': self.get_access(),
        }

    def email_user(self, subject, message, from_email=None):
        if self.email:
            send_mail(subject, message, from_email, [self.email])

    @classmethod
    def from_phone_number(cls, identity, only_active=True):
        try:
            p = PhoneNumber.get_or_none(identity).provider
            if only_active:
                return p if p.active else None
            return p
        except (PhoneNumber.DoesNotExist, AttributeError):
            return None

    def primary_phone(self):
        try:
            return self.primary_number().identity
        except:
            return None

    def primary_number(self):
        try:
            return self.phone_numbers.order_by('-priority').first()
        except:
            return None

    def all_numbers(self):
        return [n.identity for n in self.phone_numbers.order_by('-priority')
                if n is not None]

    def has_permission(self, perm_slug, entity=None):
        """ whether or not User has this permission for Enitity """
        if entity is not None:
            if self.target() is None:
                return False
            if entity not in [entity] + self.target().get_descendants():
                return False

        if self.role() is None:
            return False

        if perm_slug in [p.slug for p in self.role().permissions.all()]:
            return True
        return False

    def is_central(self):
        return self.location.level == 0

    def last_actions(self):
        return Action.last_for(self, limit=10)


reversion.register(Provider)


# catch django signals and emit ours
def on_django_logged_in(sender, user, **kwargs):
    logged_in.send(sender=Provider.__class__,
                   provider=Provider.get_or_none(user.username,
                                                 with_inactive=True))
user_logged_in.connect(on_django_logged_in)


def on_django_logged_out(sender, user, **kwargs):
    logged_out.send(sender=Provider.__class__,
                    provider=Provider.get_or_none(user.username,
                                                  with_inactive=True))
user_logged_out.connect(on_django_logged_out)


# handle logged_in/out signals
def on_logged_in(sender, provider, **kwargs):
    Action.record('logged_in', provider, Action.WEB)
logged_in.connect(on_logged_in)


def on_logged_out(sender, provider, **kwargs):
    Action.record('logged_out', provider, Action.WEB)
logged_out.connect(on_logged_out)
