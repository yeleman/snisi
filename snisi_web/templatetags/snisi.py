#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import locale

from py3compat import text_type
from django import template
from django.template.defaultfilters import stringfilter
from django.template.defaulttags import CsrfTokenNode
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _

from snisi_tools.numbers import phonenumber_repr
from snisi_tools.datetime import to_jstimestamp
from snisi_core.models.Reporting import SNISIReport

register = template.Library()
locale.setlocale(locale.LC_ALL, '')


class FakeField(object):
    def __init__(self, *args, **kwargs):
        for name, value in kwargs.items():
            setattr(self, name, value)


@register.filter(name='phone')
@stringfilter
def phone_number_formatter(number):
    ''' format phone number properly for display '''
    return phonenumber_repr(number)


@register.filter(name='pureform')
def format_pure_form(form, pure_class='aligned'):
    output = ''

    if form.non_field_errors():
        output += non_field_errors(form, pure_class)

    for field in form:
        if not field.is_hidden:
            output += pure_field_group(field, pure_class)
    return mark_safe(output)


@register.filter(name='purenonfielderrors')
def non_field_errors(form, pure_class='aligned'):
    output = ''
    if not form.non_field_errors():
        return mark_safe(output)
    output += '<div class="pure-control-group alert alert-danger">\n'
    output += '<label for="__errors__">Erreurs</label>\n'
    output += '<div class="pure-help-inline" name="__errors__">\n'
    output += '<ul class="alert ">\n'
    for error in form.non_field_errors():
        output += '<li class="alert-danger">{}</li>\n'.format(error)
    output += '</ul>\n'
    output += '</div>\n'
    output += '</div>\n'
    return mark_safe(output)


@register.filter(name='purefieldgroup')
def pure_field_group(field, pure_class='aligned'):

    # default size with CSS class
    if 'class' not in field.field.widget.attrs:
        field.field.widget.attrs.update({'class': 'pure-input-1-2'})

    if pure_class == 'inline':
        field.field.widget.attrs.update({'class': 'pure-input'})
    else:
        field.field.widget.attrs.update({'class': 'pure-input-1-2'})

    divcls = 'pure-control-group' if pure_class != 'inline' \
        else 'pure-control-group-inline'

    # field group wrapper with danger
    output = '<div class="{divcls} {alertcls}">\n'.format(
        divcls=divcls,
        alertcls='alert alert-danger' if field.errors else '')
    output += pure_field_label(field)
    output += '\n'
    output += pure_field(field)

    # help_text is an info icon with title-tooltip
    if field.help_text:
        output += ' <i class="icon-info-circled help-text" title="{}"></i>' \
                  .format(field.help_text)
    output += '\n</div>\n'
    return mark_safe(output)


@register.filter(name='purefieldlabel')
def pure_field_label(field):
    error_marker = (' <i class="icon-attention-alt '
                    'alert-danger" title="{}"></i>'
                    .format("\n".join(field.errors)) if field.errors else '')

    output = '<label for="{name}">{label}{errors}</label>'.format(
        name=field.name,
        label=field.label,
        errors=error_marker,
        csscls="alert-danger" if field.errors else '')
    return mark_safe(output)


@register.filter(name='purefield')
def pure_field(field):
    output = ''
    output += text_type(field)
    return mark_safe(output)


@register.simple_tag
def pure_form(form, method='POST',
              action=None,
              pure_class='aligned',
              extra_class='',
              csrf_token=None,
              legend=None,
              submit_text="Envoyer",
              with_file=False):
    output = ''
    legend_tag = '<legend>{}</legend>\n'.format(legend) if legend else ''
    form_content = format_pure_form(form, pure_class)

    if pure_class == 'inline':
        form_content = form_content.rsplit('</div>', 1)[0]
        submit_block = ('<button class="pure-button pure-button-primary">\n'
                        '{submit_text}</button>\n</div>\n')
    else:
        submit_block = ('<div class="pure-control-group">\n'
                        '<label></label>\n'
                        '<button class="pure-button pure-button-primary">\n'
                        '{submit_text}</button>\n'
                        '</div>\n')
    submit_block = submit_block.format(submit_text=submit_text or "Envoyer")

    if with_file:
        file_support = ' enctype="multipart/form-data"'
    else:
        file_support = ''

    output += ('<form method="{method}" action="{action}" '
               'class="pure-form pure-form-{pure_class} {extra_class}'
               '"{file_support}>\n'
               '<input type="hidden" name="csrfmiddlewaretoken" '
               'value="{csrf_token}"/>\n'
               '{legend_tag}'
               '<fieldset>\n'
               '{form_content}\n'
               '{submit_block}\n'
               '</fieldset>\n'
               '</form>\n').format(
        method=method or 'POST',
        action=action or '',
        csrf_token=csrf_token or CsrfTokenNode().render(),
        legend_tag=legend_tag,
        pure_class=pure_class or 'aligned',
        extra_class=extra_class or '',
        file_support=file_support,
        submit_block=submit_block,
        form_content=form_content)
    return mark_safe(output)


@register.filter(name='dynfilter')
def dynfilter(obj, params):

    if '|' in params:
        func, args = params.split('|', 1)
        args = args.split('|')
    else:
        func = params

    prop = getattr(obj, func)

    if prop:
        try:
            return prop(*args)
        except:
            return prop()

    try:
        return func(obj, *args)
    except:
        try:
            return func(obj)
        except:
            return obj


@register.filter(name='reporttmpl')
def report_template_name(class_slug):
    return "report/{}.html".format(class_slug)


@register.filter(name='fname')
def report_field_name(report, fname):
    return report.field_name(fname)


@register.filter(name='reportstatus')
@stringfilter
def report_status_verbose(value):
    for v, name in SNISIReport.STATUSES:
        if v.__str__() == value:
            return name
    return value


@register.filter(name='reportyesno')
@stringfilter
def report_yesno_verbose(value):
    try:
        from pnlp_core.models import MalariaReport
    except:
        return value
    for v, name in MalariaReport.YESNO:
        if v.__str__() == value:
            return name
    return value


@register.filter(name='reportvalue')
@stringfilter
def report_value(value):
    try:
        float(value)
        return number_format(value).replace(' ', ' ')  # non-break thin
    except:
        return report_yesno_verbose(value)


@register.filter(name='numberformat')
@stringfilter
def number_format(value, precision=2):
    try:
        format = '%d'
        value = int(value)
    except:
        try:
            format = '%.' + '%df' % precision
            value = float(value)
        except:
            format = '%s'
        else:
            if value.is_integer():
                format = '%d'
                value = int(value)
    try:
        return locale.format(format, value, grouping=True)
    except Exception:
        pass
    return value


@register.filter(name='lvl2css')
def level_to_css_class(value):
    lvlcss_matrix = {
        'error': 'danger',
    }
    return lvlcss_matrix.get(value, value)


@register.filter(name='nb_extra_nums')
def provider_additional_numbers(provider):
    try:
        return len(provider.all_numbers()) - 1
    except:
        return 0


@register.filter(name='to_jstimestamp')
def convert_to_jstimestamp(adate):
    return to_jstimestamp(adate)


@register.filter(name='igetter')
def igetter(obj, key):
    try:
        return obj[key]
    except IndexError:
        return None


@register.filter(name='getter')
def getter(obj, key):
    return getattr(obj, key, None)


@register.filter(name='yesno')
def yesno(val):
    return _("Yes") if bool(val) else _("No")


@register.filter(name='sort_sources')
def sort_sources(slist):
    return sorted(slist, key=lambda r: r.entity.name)


@register.filter(name='percent')
def percent_format(number):
    return "{}%".format(number_format(number * 100))
