#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging
import os

import requests
from django.core.management.base import BaseCommand
from optparse import make_option

from snisi_tools.path import mkdir_p

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
        make_option('-d',
                    help='Destination folder',
                    action='store',
                    dest='dest_folder'),
        make_option('-c',
                    help='Clone Mapbox server',
                    action='store_true',
                    default=False,
                    dest='as_mapbox'),
    )

    def handle(self, *args, **options):

        dest_folder = options.get('dest_folder')
        if not dest_folder:
            logger.error("You must specify a destination folder with -d")
            return
        mkdir_p(dest_folder)

        symbols = list("abcdefghijklmnopqrstuvwxyz0123456789") + ['hospital']

        versions = {
            'true': '28ff00',
            'false': 'ff1500'
        }
        # new colors
        versions = {
            'true': '889f37',
            'false': '4d2c74',
            'missing': '1d3f61',
            'na': '737780',
            'blank': '7e7e7e',
        }
        sizes = "sml"

        headers = {
            'User-agent': ("Mozilla/5.0 (Macintosh; "
                           "Intel Mac OS X 10.8; rv:28.0) "
                           "Gecko/20100101 Firefox/28.0")
        }

        for symbol in symbols:
            for version, color in versions.items():
                for size in sizes:
                    data = {'size': size, 'symbol': symbol,
                            'version': version, 'color': color}
                    dest_fname = ("pin-{size}-{symbol}-{version}.png"
                                  .format(**data))
                    if options.get('as_mapbox'):
                        dest_fname = ("pin-{size}-{symbol}+{color}.png"
                                      .format(**data))
                    url = "http://a.tiles.mapbox.com/v3/marker/pin-{size}" \
                          "-{symbol}+{color}.png".format(**data)

                    logger.info(url)
                    req = requests.get(url, headers=headers)

                    if not req.status_code == requests.codes.ok:
                        logger.error("Request failed with code {}. {}"
                                     .format(req.status_code, req.text))
                        continue

                    if req.content is None:
                        logger.error("Content is None")
                        continue

                    with open(os.path.join(dest_folder, dest_fname), 'w') as f:
                        f.write(req.content)

                    logger.info(dest_fname)

