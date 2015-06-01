#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging
import traceback

import reversion
from django.utils.translation import ugettext as _

from snisi_core.integrity import (ReportIntegrityChecker,
                                  RoutineIntegrityInterface)
from snisi_core.models.Providers import Provider
from snisi_core.models.Entities import Entity
from snisi_core.models.Periods import DayPeriod
from snisi_core.models.Notifications import Notification
from snisi_core.models.Roles import Role
from snisi_core.models.FixedWeekPeriods import (FixedMonthFirstWeek,
                                                FixedMonthSecondWeek,
                                                FixedMonthThirdWeek,
                                                FixedMonthFourthWeek,
                                                FixedMonthFifthWeek)
from snisi_malaria.models import (MalariaR,
                                  EpidemioMalariaR, AggEpidemioMalariaR)
from snisi_core.models.Reporting import (ReportClass, ExpectedReporting,
                                         ExpectedValidation)
from snisi_core.models.ValidationPeriods import DefaultDistrictValidationPeriod
from snisi_malaria import get_domain, PROJECT_BRAND

logger = logging.getLogger(__name__)
validating_role = Role.objects.get(slug='charge_sis')


def create_report(provider, expected_reporting, completed_on,
                  integrity_checker, data_source):

    report = MalariaR.start(period=expected_reporting.period,
                            entity=expected_reporting.entity,
                            created_by=provider,
                            completion_status=MalariaR.COMPLETE,
                            completed_on=completed_on,
                            integrity_status=MalariaR.CORRECT,
                            arrival_status=integrity_checker.get(
                                'arrival_status'),
                            validation_status=MalariaR.NOT_VALIDATED)

    # fill the report from SMS data
    report.add_underfive_data(**{key[3:]: value
                                 for key, value
                                 in integrity_checker.data.items()
                                 if key.startswith('u5')})
    report.add_overfive_data(**{key[3:]: value
                                for key, value
                                in integrity_checker.data.items()
                                if key.startswith('o5')})
    report.add_pregnantwomen_data(**{key[3:]: value
                                     for key, value
                                     in integrity_checker.data.items()
                                     if key.startswith('pw')})
    report.add_stockout_data(**{key: value
                                for key, value
                                in integrity_checker.data.items()
                                if key.startswith('stockout')})

    try:
        with reversion.create_revision():
            report.save()
    except Exception as e:
        logger.error("Unable to save report to DB. Content: {} | Exp: {}"
                     .format(data_source, e))
        logger.debug("".join(traceback.format_exc()))
        return False, ("Une erreur technique s'est "
                       "produite. Réessayez plus tard et "
                       "contactez ANTIM si le problème persiste.")
    else:
        expected_reporting.acknowledge_report(report)

    # VP is District VP of next month
    validation_period = DefaultDistrictValidationPeriod.find_create_by_date(
        report.period.casted().following().middle())

    # VE is the district (CSCOM's parent)
    validating_entity = report.entity.get_health_district()

    # created expected validation for district charge_sis
    ExpectedValidation.objects.create(
        report=report,
        validation_period=validation_period,
        validating_entity=validating_entity,
        validating_role=validating_role)

    # Add alert to validation Entity?
    for recipient in Provider.active.filter(role=validating_role,
                                            location=validating_entity):

        if recipient == provider:
            continue

        Notification.create(
            provider=recipient,
            deliver=Notification.TODAY,
            expirate_on=validation_period.end_on,
            category=PROJECT_BRAND,
            text="L'Unité Sanitaire {hc} vient d'envoyer son rapport de "
                 "routine paludisme mensuel pour {period}. "
                 "No reçu: #{receipt}."
                 .format(hc=report.entity.display_full_name(),
                         period=report.period,
                         receipt=report.receipt)
            )

    return report, ("Le rapport de {cscom} pour {period} "
                    "a été enregistré. "
                    "Le No de reçu est #{receipt}."
                    .format(cscom=report.entity.display_full_name(),
                            period=report.period,
                            receipt=report.receipt))


class MalariaRIntegrityChecker(ReportIntegrityChecker,
                               RoutineIntegrityInterface):

    DOMAIN = get_domain()
    report_class = ReportClass.get_or_none("malaria_monthly_routine")

    def _check_completeness(self, **options):
        for field in MalariaR.data_fields():
            if not self.has(field):
                self.add_missing(_("Données manquantes pour {}").format(field),
                                 blocking=True, field=field)

    def _check(self, **options):
        self.check_malaria_data()
        self.chk_period_is_not_future(**options)
        self.chk_entity_exists(**options)
        self.chk_expected_arrival(**options)
        self.chk_provider_permission(**options)

    def check_malaria_data(self):

        no_more_than_text = lambda d: ("{field2} ({f2value}) ne peut pas "
                                       "être supérieur à "
                                       "{field1} ({f1value})").format(**d)
        no_different_than_text = lambda d: ("{field2} ({f2value}) ne peut pas "
                                            "être différent de "
                                            "{field1} ({f1value})").format(**d)
        field_name = lambda f: MalariaR.field_name(f).decode('utf-8')

        # no_more_than_text =
        allcats = ('u5', 'o5', 'pw')
        nopwcat = ('u5', 'o5')

        def test_value_under(fieldref, fieldtest, cats):
            for cat in cats:
                try:
                    fieldtest_slug = '{}_{}'.format(cat, fieldtest)
                    fieldref_slug = '{}_{}'.format(cat, fieldref)
                    dic = {'field2': "[{cat}] {fn}".format(
                        cat=MalariaR.verbose_cat(cat),
                        fn=field_name(fieldtest_slug)),
                        'f2value': self.get(fieldtest_slug),
                        'field1': "[{cat}] {fn}".format(
                        cat=MalariaR.verbose_cat(cat),
                        fn=field_name(fieldref_slug)),
                        'f1value': self.get(fieldref_slug)}
                    if dic['f1value'] < dic['f2value']:
                        self.add_error(no_more_than_text(dic),
                                       field=dic['field2'])
                except:
                    # this missing data should have already been reported
                    pass

        # total > malaria cases
        test_value_under('total_consultation_all_causes',
                         'total_suspected_malaria_cases', allcats)

        # total >  malaria simple
        test_value_under('total_consultation_all_causes',
                         'total_simple_malaria_cases', allcats)

        # total >  malaria severe
        test_value_under('total_consultation_all_causes',
                         'total_severe_malaria_cases', allcats)

        # suspected > malaria simple
        test_value_under('total_suspected_malaria_cases',
                         'total_simple_malaria_cases', allcats)

        # suspected > malaria severe
        test_value_under('total_suspected_malaria_cases',
                         'total_severe_malaria_cases', allcats)

        # suspected > malaria tested
        test_value_under('total_suspected_malaria_cases',
                         'total_tested_malaria_cases', allcats)

        # suspected > malaria confirmed
        test_value_under('total_suspected_malaria_cases',
                         'total_confirmed_malaria_cases', allcats)

        # suspected > simple + severe
        for cat in nopwcat:
            try:
                dic = {
                    'field2':
                        _("[{cat}] {simple} + {severe}")
                        .format(
                            cat=MalariaR.verbose_cat(cat),
                            simple=field_name('{}_total_simple_malaria_cases'
                                              .format(cat)),
                            severe=field_name('{}_total_severe_malaria_cases'
                                              .format(cat))),
                    'f2value': int(self.get('{}_total_simple_malaria_cases'
                                            .format(cat)))
                        + int(self.get('{}_total_severe_malaria_cases'
                                       .format(cat))),
                    'field1': "[{cat}] {fn}".format(
                        cat=MalariaR.verbose_cat(cat),
                        fn=field_name('{}_total_suspected_malaria_cases'
                                      .format(cat))),
                    'f1value': self.get(
                        '{}_total_suspected_malaria_cases'.format(cat))}
                if dic['f1value'] < dic['f2value']:
                    self.add_error(
                        no_more_than_text(dic),
                        field='{}_total_suspected_malaria_cases'.format(cat))
            except:
                pass

        # confirmed != simple + severe
        for cat in allcats:
            try:
                dic = {
                    'field2':
                        _("[{cat}] {simple} + {severe}")
                        .format(
                            cat=MalariaR.verbose_cat(cat),
                            simple=field_name('{}_total_simple_malaria_cases'
                                              .format(cat)),
                            severe=field_name('{}_total_severe_malaria_cases'
                                              .format(cat))),
                    'f2value': int(self.get('{}_total_simple_malaria_cases'
                                            .format(cat)))
                    + int(self.get('{}_total_severe_malaria_cases'
                                   .format(cat))),
                    'field1': "[{cat}] {fn}".format(
                        cat=MalariaR.verbose_cat(cat),
                        fn=field_name('{}_total_confirmed_malaria_cases'
                                      .format(cat))),
                    'f1value': self.get('{}_total_confirmed_malaria_cases'
                                        .format(cat))}
                if dic['f1value'] != dic['f2value']:
                    self.add_error(no_different_than_text(dic),
                                   field='{}_total_confirmed_malaria_cases'
                                         .format(cat))
            except:
                pass

        # tested > confirmed
        test_value_under('total_tested_malaria_cases',
                         'total_confirmed_malaria_cases', allcats)

        # tested > ACT
        test_value_under('total_tested_malaria_cases',
                         'total_treated_malaria_cases', allcats)

        # confirmed > act
        test_value_under('total_confirmed_malaria_cases',
                         'total_treated_malaria_cases', allcats)

        # total inpatient > malaria inpatient
        test_value_under('total_inpatient_all_causes',
                         'total_malaria_inpatient', allcats)

        # total death > malaria death
        test_value_under('total_death_all_causes',
                         'total_malaria_death', allcats)


class MalariaRSourceReportChecker(MalariaRIntegrityChecker):

    def _check_completeness(self, **options):
        local_fields = ['year', 'month', 'hc', 'submit_time',
                        'fillin_year', 'fillin_month', 'fillin_day',
                        'submitter']
        for field in MalariaR.data_fields() + local_fields:
            if not self.has(field):
                self.add_missing(_("Données manquantes pour {}").format(field),
                                 blocking=True, field=field)


def create_epidemio_report(provider, expected_reporting, completed_on,
                           integrity_checker, data_source):

    fday = expected_reporting.period.start_on.day
    eday = expected_reporting.period.end_on.day
    day = fday
    daynum = 1
    while day <= eday:
        day_period = DayPeriod.find_create_from(
            year=expected_reporting.period.start_on.year,
            month=expected_reporting.period.start_on.month,
            day=day)

        day_expected = ExpectedReporting.objects.get(
            report_class__slug="malaria_weekly_epidemio",
            period=day_period,
            entity=expected_reporting.entity)

        day_report = EpidemioMalariaR.start(
            period=day_expected.period,
            entity=day_expected.entity,
            created_by=provider,
            completion_status=EpidemioMalariaR.COMPLETE,
            completed_on=completed_on,
            integrity_status=EpidemioMalariaR.CORRECT,
            arrival_status=integrity_checker.get('arrival_status'),
            validation_status=EpidemioMalariaR.NOT_VALIDATED)

        for field in EpidemioMalariaR.data_fields():
            setattr(day_report, field,
                    integrity_checker.get('d{}_{}'.format(daynum, field)))

        try:
            with reversion.create_revision():
                day_report.save()
        except Exception as e:
            logger.error("Unable to save report to DB. Content: {} | Exp: {}"
                         .format(data_source, e))
            logger.debug("".join(traceback.format_exc()))
            return False, ("Une erreur technique s'est "
                           "produite. Réessayez plus tard et "
                           "contactez ANTIM si le problème persiste.")
        else:
            day_expected.acknowledge_report(day_report)

        daynum += 1
        day += 1

    # create weekly aggregated report
    try:
        report = AggEpidemioMalariaR.create_from(
            period=expected_reporting.period,
            entity=expected_reporting.entity,
            created_by=provider)
    except Exception as e:
        logger.error("Unable to save report to DB. Content: {} | Exp: {}"
                     .format(data_source, e))
        logger.debug("".join(traceback.format_exc()))
        return False, ("Une erreur technique s'est "
                       "produite. Réessayez plus tard et "
                       "contactez ANTIM si le problème persiste.")
    else:
        expected_reporting.acknowledge_report(report)

    return report, ("Le rapport de {cscom} pour {period} "
                    "a été enregistré. "
                    "Le No de reçu est #{receipt}."
                    .format(cscom=report.entity.display_full_name(),
                            period=report.period,
                            receipt=report.receipt))


class EpidemioMalariaRIntegrityChecker(ReportIntegrityChecker):

    DOMAIN = get_domain()

    def nb_days_for_week(self, year, month, week):
        nb_day_in_month = self.nb_days_for_month(year, month)
        if week < 5:
            return 7
        return nb_day_in_month - 28

    def nb_days_for_month(self, year, month):
        nb_day_in_month = 30
        if month == 2:
            if year in (2012, 2016, 2020):
                nb_day_in_month = 29
            else:
                nb_day_in_month = 28
        if month in (1, 3, 5, 7, 8, 10, 12):
            nb_day_in_month = 31
        return nb_day_in_month

    def _check_completeness(self, **options):

        for field in ('week', 'month', 'year'):
            if not self.has(field):
                self.add_missing(_("Données manquantes "
                                   "pour {}").format(field),
                                 blocking=True, field=field)

        week = self.get('week')
        month = self.get('month')
        year = self.get('year')

        nb_days_this_week = self.nb_days_for_week(year, month, week)
        if nb_days_this_week == 0:
            pass

        for day_num in range(1, 1 + nb_days_this_week):
            for field in EpidemioMalariaR.data_fields():
                fname = "d{}_{}".format(day_num, field)
                if not self.has(fname):
                    self.add_missing(_("Données manquantes "
                                       "pour {}").format(fname),
                                     blocking=True, field=fname)

    def _check(self, **options):

        week = self.get('week')
        month = self.get('month')
        year = self.get('year')

        date_txt = "La valeur pour {} est incorrecte: {}"
        if week not in range(1, 6):
            self.add_error(date_txt.format("semaine", week),
                           blocking=True, field='week')

        if month not in range(1, 13):
            self.add_error(date_txt.format("mois", month),
                           blocking=True, field='month')

        if year not in range(2011, 2020):
            self.add_error(date_txt.format("année", year),
                           blocking=True, field='year')

        # common data-only checks
        self.check_data(**options)

        weekcls_dict = {
            1: FixedMonthFirstWeek,
            2: FixedMonthSecondWeek,
            3: FixedMonthThirdWeek,
            4: FixedMonthFourthWeek,
            5: FixedMonthFifthWeek
        }

        weekcls = weekcls_dict.get(week)

        # Get period and Entity
        period = weekcls.find_create_from(year=year, month=month)
        if period.is_ahead():
            self.add_error("La période indiquée ({period}) est dans "
                           "le futur".format(period=period),
                           blocking=True, field='week')

        entity = Entity.get_or_none(self.get('hc'), type_slug='health_center')
        if entity is None:
            self.add_error("Aucun CSCOM ne correspond au code {}"
                           .format(self.get('hc')),
                           field='hc', blocking=True)
        else:
            self.set('entity', entity)

        week_slug_matrix = {
            FixedMonthFirstWeek:
                'malaria_weekly_epidemio_firstweek_aggregated',
            FixedMonthSecondWeek:
                'malaria_weekly_epidemio_secondweek_aggregated',
            FixedMonthThirdWeek:
                'malaria_weekly_epidemio_thirdweek_aggregated',
            FixedMonthFourthWeek:
                'malaria_weekly_epidemio_fourthweek_aggregated',
            FixedMonthFifthWeek: 'malaria_weekly_epidemio_fifthweek_aggregated'
        }

        # expected reporting defines if report is expeted or not
        expected_reporting = ExpectedReporting.get_or_none(
            report_class=ReportClass.objects.get(
                slug=week_slug_matrix.get(weekcls)),
            period=period,
            within_period=False,
            entity=entity,
            within_entity=False,
            amount_expected=ExpectedReporting.EXPECTED_SINGLE)

        self.set('expected_reporting', expected_reporting)

        if expected_reporting is None:
            self.add_error("Aucun rapport de routine attendu à "
                           "{entity} pour {period}"
                           .format(entity=entity, period=period),
                           blocking=True)

        if expected_reporting.satisfied:
            self.add_error("Le rapport de routine attendu à "
                           "{entity} pour {period} est déjà arrivé"
                           .format(entity=entity, period=period),
                           blocking=True)

        # check if the report arrived in time or not.
        if expected_reporting.reporting_period.contains(
                self.get('submit_time')):
            arrival_status = EpidemioMalariaR.ON_TIME
        elif expected_reporting.extended_reporting_period.contains(
                self.get('submit_time')):
            arrival_status = EpidemioMalariaR.LATE
        else:
            # arrived while not in a reporting period
            if self.get('submit_time') \
                    < expected_reporting.reporting_period.start_on:
                text = ("La période de collecte pour {period} "
                        "n'a pas encore commencée. Rapport refusé.")
            else:
                # arrived too late. We can't accept the report.
                text = ("La période de collecte pour {period} "
                        "est terminée. Rapport refusé.")
            self.add_error(text.format(period=expected_reporting.period),
                           blocking=True, field='period')
        self.set('arrival_status', arrival_status)

        # check permission to submit report.
        self.chk_provider_permission(**options)

    def check_data(self):

        no_more_than_text = lambda d: (
            "[Jour {day_in_month}] {field2} ({f2value}) ne peut pas "
            "être supérieur à {field1} ({f1value})").format(**d)
        field_name = lambda f: EpidemioMalariaR.field_name(f)

        allcats = ('u5', 'o5', 'pw')

        def nb_day_for_week_dict(week, nb_day_in_month):
            start = 1 if week == 1 else 7 * (week - 1) + 1
            end = nb_day_in_month + 1 if week == 5 else start + 7
            return range(start, end)

        def test_value_under(fieldref, fieldtest, nb_day, cats, day_in_month):
            for cat in cats:
                try:
                    dic = {
                        'field2': field_name('{}_{}'.format(cat, fieldtest)),
                        'f2value': self.get('d{}_{}_{}'
                                            .format(nb_day, cat, fieldtest)),
                        'field1': field_name('{}_{}'.format(cat, fieldref)),
                        'f1value': self.get('d{}_{}_{}'
                                            .format(nb_day, cat, fieldref)),
                        'day_in_month': day_in_month}
                    if dic['f1value'] < dic['f2value']:
                        self.add_error(no_more_than_text(dic),
                                       field=dic['field2'])
                except:
                    # this missing data should have already been reported
                    pass
        nb_days_for_month = self.nb_days_for_month(
            self.get('year'), self.get('month'))
        for nb_day, day_in_month in enumerate(nb_day_for_week_dict(
                self.get('week'), nb_days_for_month)):
            nb_day += 1
            # Nbre de cas de palu. (tous suspectés) ne
            # peut pas être supérieur au nbre de total
            # consultation toutes causes confondues
            test_value_under('total_consultation_all_causes',
                             'total_suspected_malaria_cases',
                             nb_day, allcats, day_in_month)
            # Nbre de cas de palu. (testé avec TDR) ne
            # peut pas être supérieur au nbre de palu.(tout suspectés)
            test_value_under('total_suspected_malaria_cases',
                             'total_rdt_tested_malaria_cases',
                             nb_day, allcats, day_in_month)
            # Nbre de cas de palu. (confirmé par TDR) ne
            # peut pas être supérieur au nbre de palu.(tout suspectés)
            test_value_under('total_suspected_malaria_cases',
                             'total_rdt_confirmed_malaria_cases',
                             nb_day, allcats, day_in_month)
            # Nbre de cas de palu. (confirmé par TDR) ne
            # peut pas être supérieur au nbre de palu.(testé avec TDR)
            test_value_under('total_rdt_tested_malaria_cases',
                             'total_rdt_confirmed_malaria_cases',
                             nb_day, allcats, day_in_month)
            # Nbre de cas de palu. (testés avec GE) ne
            # peut pas être supérieur au nbre de palu.(tout suspectés)
            test_value_under('total_suspected_malaria_cases',
                             'total_ts_tested_malaria_cases',
                             nb_day, allcats, day_in_month)
            # Nbre de cas de palu. (confirmé par GE) ne
            # peut pas être supérieur au nbre de palu.(tout suspectés)
            test_value_under('total_suspected_malaria_cases',
                             'total_ts_confirmed_malaria_cases',
                             nb_day, allcats, day_in_month)
            # Nbre de cas de palu. (confirmé par GE) ne
            # peut pas être supérieur au nbre de palu.(testé avec GE)
            test_value_under('total_ts_tested_malaria_cases',
                             'total_ts_confirmed_malaria_cases',
                             nb_day, allcats, day_in_month)
            # Nbre de cas de palu. (simple) ne peut
            # pas être supérieur au nbre de palu.(tout suspectés)
            test_value_under('total_suspected_malaria_cases',
                             'total_simple_malaria_cases',
                             nb_day, allcats, day_in_month)
            # Nbre de cas de palu. (grave) ne peut pas
            # être supérieur au nbre de palu.(tout suspectés)
            test_value_under('total_suspected_malaria_cases',
                             'total_severe_malaria_cases',
                             nb_day, allcats, day_in_month)
            # Nbre de cas de décès dûs au palu. ne peut pas
            # être supérieur au nbre de cas de décès toutes causes confondues
            test_value_under('total_death_all_causes',
                             'total_malaria_death',
                             nb_day, allcats, day_in_month)

            for cat in allcats:

                # Nbre de cas de palu. (simple + grave) ne
                # peut pas être supérieur au nbre de palu.(tout suspectés)
                try:
                    dic = {
                        'field2':
                            _("{simple} + {severe}")
                            .format(
                                simple=field_name(
                                    '{}_total_simple_malaria_cases'
                                    .format(cat)),
                                severe=field_name(
                                    '{}_total_severe_malaria_cases'
                                    .format(cat))),
                        'field1': field_name(
                            '{}_total_suspected_malaria_cases'.format(cat)),
                        'f1value': self.get(
                            'd{}_{}_total_suspected_malaria_cases'
                            .format(nb_day, cat)),
                        'f2value': int(self.get(
                            'd{}_{}_total_simple_malaria_cases'
                            .format(nb_day, cat)))
                            + int(self.get('d{}_{}_total_severe_malaria_cases'
                                           .format(nb_day, cat))),
                        'day_in_month': day_in_month}

                    if dic['f1value'] < dic['f2value']:
                        self.add_error(
                            no_more_than_text(dic),
                            field='{}s_total_confirmed_malaria_cases'
                                  .format(cat))
                except:
                    pass

                # Nbre de cas de palu. (simple + grave) ne
                # peut pas être supérieur au nbre de
                # total consultation toutes causes confondues
                try:
                    dic = {
                        'field2':
                            _("{simple} + {severe}").format(
                                simple=field_name(
                                    '{}_total_simple_malaria_cases'
                                    .format(cat)),
                                severe=field_name(
                                    '{}_total_severe_malaria_cases'
                                    .format(cat))),
                        'field1': field_name('{}_total_consultation_all_causes'
                                             .format(cat)),
                        'f1value': self.get(
                            'd{}_{}_total_consultation_all_causes'
                            .format(nb_day, cat)),
                        'f2value': int(self.get(
                            'd{}_{}_total_simple_malaria_cases'
                            .format(nb_day, cat)))
                            + int(self.get('d{}_{}_total_severe_malaria_cases'
                                           .format(nb_day, cat))),
                        'day_in_month': day_in_month}

                    if dic['f1value'] < dic['f2value']:
                        self.add_error(
                            no_more_than_text(dic),
                            field='{}s_total_confirmed_malaria_cases'
                            .format(cat))
                except:
                    pass
