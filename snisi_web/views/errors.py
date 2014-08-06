#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import traceback

from django.shortcuts import render


def permission_denied(request, template_name='errors/403.html'):
    context = {'error_num': 403}
    return render(request, template_name, context)


def server_error(request, template_name='errors/500.html'):
    context = {'error_num': 500}
    context.update({'traceback': "".join(traceback.format_exc())})

    return render(request, template_name, context)


def bad_request(request, template_name='errors/500.html'):
    context = {'error_num': 400}
    context.update({'traceback': "".join(traceback.format_exc())})

    return render(request, template_name, context)


def not_found(request, template_name='errors/404.html'):
    context = {'error_num': 404}

    return render(request, template_name, context)
