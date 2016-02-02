#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging

from django.core.management.base import BaseCommand
from django.db import connections

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, database="default", *args, **options):

        cursor = connections[database].cursor()

        # harmonize to MyISAM first
        cursor.execute(
            "ALTER TABLE snisi_core_snisiprojectparticipation "
            "DROP FOREIGN KEY entity_id_refs_slug_27d6217c;")
        cursor.execute(
            "ALTER TABLE snisi_core_snisiprojectparticipation "
            "DROP FOREIGN KEY project_id_refs_slug_96acf6bc;")
        cursor.execute(
            "ALTER TABLE snisi_core_snisiproject "
            "DROP FOREIGN KEY operational_contact_id_refs_username_d1f73aeb;")
        cursor.execute(
            "ALTER TABLE snisi_core_snisiproject "
            "DROP FOREIGN KEY technical_contact_id_refs_username_d1f73aeb;")
        cursor.execute(
            "ALTER TABLE snisi_core_snisiproject ENGINE=MyISAM;")
        cursor.execute(
            "ALTER TABLE snisi_core_snisiprojectparticipation ENGINE=MyISAM;")

        # now convert all to InnoDB
        cursor.execute("SHOW TABLE STATUS;")

        for row in cursor.fetchall():
            if row[1] != "InnoDB":
                logger.info("Converting {}".format(row[0]))
                result = cursor.execute("ALTER TABLE {} ENGINE=INNODB"
                                        .format(row[0]))
                logger.info(result)
