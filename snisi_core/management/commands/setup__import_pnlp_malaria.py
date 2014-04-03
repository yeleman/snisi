#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import json
import datetime

import reversion
from optparse import make_option
from django.core.management.base import BaseCommand
from django.utils import timezone

from snisi_core.models.Entities import Entity
from snisi_core.models.Reporting import ExpectedReporting, ReportClass, ExpectedValidation
from snisi_core.models.Periods import MonthPeriod
from snisi_core.models.Providers import Provider
from snisi_core.models.Roles import Role
from snisi_malaria.models import MalariaR, AggMalariaR
from snisi_tools.datetime import datetime_from_iso, DEBUG_change_system_date
from snisi_tools.pnlp_import import period_from, get_provider_from, entity_from #, get_user_from
from snisi_core.models.ValidationPeriods import (
    DefaultDistrictValidationPeriod, DefaultRegionValidationPeriod,
    DefaultNationalValidationPeriod)

new_slug_matrix = {}

# username_matrix = {
#     'sdiarra': 'sdiarra1',
#     'scoulib2': 'scoulib5',
#     'asogou': 'asogou',
#     'cmaiga': 'cmaiga1',
#     'msangare': 'msangar',
#     'tcouliba': 'tcoulib1',
# }

def report_from(receipt):
    return MalariaR.objects.get(receipt=receipt)


def deserialize_malaria(report_data, report):

    def update_sources(report_data, report):
        # non-agg
        return report

        report.sources.empty()
        for source_receipt in report_data.get('sources'):
            report.sources.add(report_from(source_receipt))
        report.save()

        return report

    def deserialize(report_data, report):

        for field, field_data in report_data.items():

            # data fields
            if field.split('_')[0] in ('u5', 'o5', 'pw', 'stockout') or field in ('receipt',):
                setattr(report, field, field_data)

            if field == '_status':
                print("FOUND STATUS:::: {}".format(field_data))
                print(report_data)
                vs = MalariaR.VALIDATED if field_data in ('STATUS_VALIDATED',
                                                          'STATUS_AUTO_VALIDATED') \
                                        else MalariaR.NOT_VALIDATED

                if vs == MalariaR.VALIDATED:
                    validation_date =  datetime_from_iso(report_data.get('modified_on'))
                    if validation_date is None:
                        m = report.period.middle()
                        if report.entity.type.slug == 'health_center':
                            validation_date = datetime.datetime(m.year, m.month, 16, 8, 0)
                        elif report.entity.type.slug == 'health_district':
                            validation_date = datetime.datetime(m.year, m.month, 26, 8, 0)
                        else:
                            validation_date = datetime.datetime(m.year, m.month, 27, 8, 0)
                    auto_validated = field_data == 'STATUS_AUTO_VALIDATED'
                    modified_by = get_provider_from(report_data.get('modified_by'))
                    if modified_by is None or modified_by.username == 'autobot':
                        modified_by = get_provider_from('autobot')
                        auto_validated = True

                    print("VALIDATOR : {}".format(modified_by))
                    expval = ExpectedValidation.objects.get(report=report)
                    print(expval)
                    expval.acknowledge_validation(
                        validated_by=modified_by,
                        validated_on=validation_date,
                        auto_validation=auto_validated)
                    report = report.__class__.objects.get(receipt=report.receipt)

            # datetimes
            if field in ('created_on', 'modified_on'):
                setattr(report, field, datetime_from_iso(report_data.get(field)))

            # period
            if field == 'period':
                setattr(report, field, period_from(report_data.get(field), as_class=MonthPeriod))

            # providers
            if field in ('created_by', 'modified_by'):
                username = report_data.get(field)
                # if username in username_matrix.keys():
                #     username = username_matrix.get(username)
                setattr(report, field, get_provider_from(username))

            # entity
            if field == 'entity':
                setattr(report, field, entity_from(new_slug_matrix[report_data.get(field)]))

        # report level fields
        print(" setting completion_status")
        report.completion_status = MalariaR.COMPLETE
        print(" completion_status is now {}".format(report.completion_status))

        if report_data.get('created_on'):
            setattr(report, 'completed_on', datetime_from_iso(report_data.get('created_on')))

        report.integrity_status = MalariaR.CORRECT
        if getattr(report, 'created_on'):
            report.arrival_status = MalariaR.ON_TIME if report.created_on.day <= 5 else MalariaR.LATE

        return report

    print("serializing...")
    report = deserialize(report_data, report)
    print("saving...")
    report.save()
    print("updating sources...")
    report = update_sources(report_data, report)
    print("done with deserialize_malaria()")
    return report


def update_last_revision(report, revision_date, revision_user):
    # if revision_user in username_matrix.keys():
    #     revision_user = username_matrix.get(revision_user)
    version = reversion.get_unique_for_object(report).pop()
    version.revision.date_created = datetime_from_iso(revision_date)
    version.revision.user = None  # get_user_from(revision_user)
    version.save()


class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
        make_option('-f',
                    help='JSON export of all PNLP reports',
                    action='store',
                    dest='input_file'),
        make_option('-m',
                    help='JSON matrix of old and new codes',
                    action='store',
                    dest='matrix_input_file'),
        make_option('-c',
                    help='Delete all MalariaR and AggMalariaR first',
                    action='store_true',
                    dest='clear'),
        make_option('-l',
                    help='Type slug for reports to handle',
                    action='store',
                    dest='level')
        )

    def handle(self, *args, **options):
        global new_slug_matrix

        matrix_input_file = open(options.get('matrix_input_file'), 'r')
        matrix = json.load(matrix_input_file)
        new_slug_matrix = matrix['old_new']

        input_file = open(options.get('input_file'), 'r')
        malaria_reports = json.load(input_file)

        role_chargesis = Role.objects.get(slug='charge_sis')
        autobot = Provider.active.get(username='autobot')

        aug2013 = datetime.datetime(2013, 8, 1).replace(tzinfo=timezone.utc)

        level = options.get('level')

        if options.get('clear'):
            print("Removing all reports...")
            MalariaR.objects.all().delete()
            AggMalariaR.objects.all().delete()
            ExpectedValidation.objects.all().delete()

        print("Creating Reports...")

        report_source = ReportClass.objects.get(slug='malaria_monthly_routine')
        report_agg = ReportClass.objects.get(slug='malaria_monthly_routine_aggregated')

        # create periods
        print("Creating Periods")

        for report_data in malaria_reports:

            # print(report_data)
            old_slug = report_data.get('entity')
            new_slug = new_slug_matrix.get(old_slug)
            # print("new slug: {}".format(new_slug))
            entity = Entity.get_or_none(new_slug)
            if entity is None:
                print(new_slug)

            if not entity.type.slug == level:
                print("Skipping {} / {}".format(entity, entity.type))
                continue
            print("{} -> {}".format(new_slug, entity))

            report_date = datetime_from_iso(report_data['period']['middle'])
            period = MonthPeriod.find_create_by_date(report_date)

            #####
            ## change btraore -> ssangara from aug2013
            ####
            if report_data["created_by"] == "btraore" and report_date > aug2013:
                report_data["created_by"] = "ssangare"
                if report_data["_version"]["user"] == "btraore":
                    report_data["_version"]["user"] = "ssangare"

                if report_data["modified_by"] == "btraore":
                    report_data["modified_by"] = "ssangare"



            reportcls = report_source if entity.type.slug == 'health_center' else report_agg

            valperiodcls = DefaultDistrictValidationPeriod if level == 'health_center' else DefaultRegionValidationPeriod
            if level == 'country':
                valperiodcls = DefaultNationalValidationPeriod

            # Change date to Period start
            DEBUG_change_system_date(period.start_on, True)

            expected_reporting = ExpectedReporting.get_or_none(
                    report_class=reportcls,
                    period=period,
                    within_period=False,
                    entity=entity,
                    within_entity=False,
                    amount_expected=ExpectedReporting.EXPECTED_SINGLE)
            if expected_reporting is None:
                print("NO EXPECTED")
                continue

            # change date to created on
            created_on = datetime_from_iso(report_data['created_on'])
            DEBUG_change_system_date(created_on, True)

            if level == 'health_center':
                report = MalariaR()
                report = deserialize_malaria(report_data, report)
                with reversion.create_revision():
                    report.save()
                    reversion.set_comment("Original version - SNISI import")
                update_last_revision(report,
                                     report_data.get('_version_date'),
                                     report_data.get('modified_by'))

            else:
                report = AggMalariaR.create_from(
                    entity=entity,
                    period=period,
                    created_by=autobot)

            expected_reporting.acknowledge_report(report)

            validating_entity = report.entity if level == 'country' else report.entity.parent
            validating_role = Role.objects.get(slug='validation_bot') if level == 'country' else role_chargesis
            ExpectedValidation.objects.create(
                report=report,
                validation_period=valperiodcls.find_create_by_date(report.period.casted().following().middle()),
                validating_entity=validating_entity,
                validating_role=validating_role,
            )

            for update in report_data.get('updates'):
                print("/// update")
                # change date to created on
                modified_on = datetime_from_iso(report_data['modified_on'])
                DEBUG_change_system_date(modified_on, True)

                report = deserialize_malaria(update, report)
                with reversion.create_revision():
                    report.save()
                    reversion.set_comment("Update - SNISI import")
                update_last_revision(report,
                                     update.get('_version_date'),
                                     update.get('modified_by'))

