#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging

from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.static import serve

logger = logging.getLogger(__name__)


@login_required
def serve_protected_files(request, fpath=None):
    if settings.SERVE_PROTECTED_FILES:
        return serve(request, fpath, settings.FILES_REPOSITORY, True)

    response = HttpResponse()
    response['Content-Type'] = ''
    response['X-Accel-Redirect'] = "{protected_url}/{fpath}".format(
        protected_url=settings.FILES_REPOSITORY_URL_PATH,
        fpath=fpath)
    return response
