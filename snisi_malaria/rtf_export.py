#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging
import os

from rtfw import Document, Section, Paragraph, ParagraphPS, Image
from rtfw import Renderer
from django.conf import settings

from snisi_malaria.models import MalariaR
from snisi_core.models.Periods import MonthPeriod
from snisi_core.models.Reporting import ExpectedReporting
from snisi_core.rtf_export import (widgets_for_indicator, generic_table,
                                   title_for_text, neutral_style)
from snisi_tools.misc import import_path, get_resource
from snisi_tools.path import mkdir_p

logger = logging.getLogger(__name__)


def get_malaria_template(entity, periods, graph_periods, quarter_num, year):
    doc = Document()
    ss = doc.StyleSheet
    section = Section()
    doc.Sections.append(section)

    pps_center = ParagraphPS(alignment=ParagraphPS.CENTER)
    h1 = ss.ParagraphStyles.Heading1

    header_png = get_resource('malaria', 'header_malaria_report.png')

    section.append(Paragraph(ss.ParagraphStyles.Normal,
                             pps_center, Image(header_png)))

    section.append(Paragraph(h1, pps_center, "RAPPORT TRIMESTRIEL"))

    section.append(Paragraph(h1, pps_center,
                             "Données de Routine sur le Paludisme au Mali"))
    section.append(Paragraph(h1, pps_center,
                             "Trimestre {qnum}: Période de {speriod} "
                             "à {eperiod}"
                             .format(qnum=quarter_num,
                                     speriod=periods[0],
                                     eperiod=periods[-1])))
    section.append(Paragraph(h1, pps_center,
                             "MODÈLE DE RAPPORT POUR {}"
                             .format(entity.display_full_name())))
    section.append(Paragraph(ss.ParagraphStyles.Normal, ""))

    return doc


def get_section(document, text, break_type=Section.PAGE):
    section = Section(break_type=break_type)
    document.Sections.append(section)
    ps = ParagraphPS()
    p = Paragraph(document.StyleSheet.ParagraphStyles.Heading1, ps)
    p.append(text)
    section.append(p)
    return section


def health_region_report(entity, periods, graph_periods, quarter_num, year):

    WIDGET_DICT = import_path('snisi_malaria.indicators.'
                              'quarter_report.WIDGET_DICT',
                              failsafe=True)

    doc = get_malaria_template(entity, periods, graph_periods,
                               quarter_num, year)

    def add_widget(section, widget_slug, break_before=False):
        indicator_cls = WIDGET_DICT.get(widget_slug)
        if indicator_cls.rendering_type == 'graph':
            indic_periods = graph_periods
        else:
            indic_periods = periods
        indicator_table = indicator_cls(
            entity=entity, periods=indic_periods)
        widgets = widgets_for_indicator(doc,
                                        indicator_table,
                                        break_before=break_before)
        for widget in widgets:
            section.append(widget)

    sectiona = get_section(doc, "A. MORBIDITÉ – MORTALITÉ")
    add_widget(sectiona, 'Tableau1')
    add_widget(sectiona, 'Figure1')
    add_widget(sectiona, 'Figure2', break_before=True)
    add_widget(sectiona, 'Figure3')
    # add_widget(sectiona, 'Figure4')
    add_widget(sectiona, 'Figure5', break_before=True)
    add_widget(sectiona, 'Figure6')

    sectionb = get_section(doc, "B. TRAITEMENT PAR CTA")
    add_widget(sectionb, 'Figure7')
    add_widget(sectionb, 'Figure8')

    sectionc = get_section(doc, "C. CPN, MILD, TIP")
    add_widget(sectionc, 'Figure9')
    add_widget(sectionc, 'Figure10')

    sectiond = get_section(doc, "D. GESTION DE STOCKS")
    add_widget(sectiond, 'Figure11')
    add_widget(sectiond, 'Figure12')

    sectione = get_section(doc,
                           "E. COMPLÉTUDE ET PROMPTITUDE DU RAPPORTAGE")
    add_widget(sectione, 'Figure13')
    add_widget(sectione, 'Figure14')

    get_section(doc, "COMMENTAIRES D'ENSEMBLE")

    get_section(doc, "RECOMMENDATIONS", None)

    return doc


def health_district_report(entity, periods, graph_periods, quarter_num, year):

    # district report uses same widgets as region
    WIDGET_DICT = import_path('snisi_malaria.indicators.'
                              'quarter_report.WIDGET_DICT',
                              failsafe=True)

    doc = get_malaria_template(entity, periods, graph_periods,
                               quarter_num, year)

    def add_widget(section, widget_slug, break_before=False):
        indicator_cls = WIDGET_DICT.get(widget_slug)
        if indicator_cls.rendering_type == 'graph':
            indic_periods = graph_periods
        else:
            indic_periods = periods
        indicator_table = indicator_cls(
            entity=entity, periods=indic_periods)
        widgets = widgets_for_indicator(doc,
                                        indicator_table,
                                        break_before=break_before)
        for widget in widgets:
            section.append(widget)

    sectiona = get_section(doc, "A. MORBIDITÉ – MORTALITÉ")
    add_widget(sectiona, 'Tableau1')
    add_widget(sectiona, 'Figure1')
    add_widget(sectiona, 'Figure2', break_before=True)
    add_widget(sectiona, 'Figure3')
    # add_widget(sectiona, 'Figure4')
    add_widget(sectiona, 'Figure5', break_before=True)
    add_widget(sectiona, 'Figure6')

    sectionb = get_section(doc, "B. TRAITEMENT PAR CTA")
    add_widget(sectionb, 'Figure7')
    add_widget(sectionb, 'Figure8')

    sectionc = get_section(doc, "C. CPN, MILD, TIP")
    add_widget(sectionc, 'Figure9')
    add_widget(sectionc, 'Figure10')

    sectiond = get_section(doc, "D. GESTION DE STOCKS")
    add_widget(sectiond, 'Figure11')
    add_widget(sectiond, 'Figure12')

    sectione = get_section(doc,
                           "E. COMPLÉTUDE ET PROMPTITUDE DU RAPPORTAGE")
    add_widget(sectione, 'Figure13')
    add_widget(sectione, 'Figure14')

    get_section(doc, "COMMENTAIRES D'ENSEMBLE")

    get_section(doc, "RECOMMENDATIONS", None)

    return doc


def health_center_report(entity, periods, graph_periods, quarter_num, year):

    def get_widgets_for(document, text, widget,
                        is_table=True, break_before=False):
        widgets = [title_for_text(document=document,
                                  text=text,
                                  break_before=break_before)]
        if is_table:
            widgets.append(neutral_style(document, None))
        widgets.append(widget)
        return widgets

    # special tables
    slug = "malaria_monthly_routine"
    last_period = periods[-1]
    first_period = last_period
    for _ in range(0, 11):
        first_period = first_period.previous()
    count_periods = MonthPeriod.all_from(first_period, last_period)

    def _pc(num, denum):
        try:
            return num / denum * 100
        except ZeroDivisionError:
            return 0

    def add_tableau2(document, section, ref_periods, name, caption):

        def count_value_for(field):
            def _pc(num, denum):
                try:
                    return num / denum * 100
                except ZeroDivisionError:
                    return 0
            count = 0
            total = 0
            for p in ref_periods:
                exp = ExpectedReporting.objects.filter(
                    entity=entity, period=p, report_class__slug=slug)
                if exp.count() == 0:
                    continue
                exp = exp.get()
                total += 1
                if not exp.satisfied:
                    continue
                if getattr(exp.arrived_report(), field, None) == MalariaR.NO:
                    count += 1

            return count, _pc(count, total)

        act_children, pc_act_children = count_value_for(
            'stockout_act_children')
        act_youth, pc_act_youth = count_value_for('stockout_act_youth')
        act_adult, pc_act_adult = count_value_for('stockout_act_adult')
        datamatrix = [
            ["", "Nb. mois", "%"],
            ["CTA Enfant-nourisson", act_children, pc_act_children],
            ["CTA Adolescent", act_youth, pc_act_youth],
            ["CTA Adulte", act_adult, pc_act_adult],
        ]
        table = generic_table(datamatrix)
        text = "{} : {}".format(name, caption)
        for widget in get_widgets_for(document, text, table, True):
            section.append(widget)

    def add_tableau3(document, section, ref_periods, name, caption):

        arrived = 0
        on_time = 0
        total = 0
        for p in ref_periods:
            exp = ExpectedReporting.objects.filter(
                entity=entity, period=p, report_class__slug=slug)
            if exp.count() == 0:
                continue
            exp = exp.get()
            total += 1
            if not exp.satisfied:
                continue
            arrived += 1
            if getattr(exp.arrived_report(),
                       'arrival_status', None) == MalariaR.ON_TIME:
                on_time += 1

        pc_on_time = _pc(on_time, total)
        pc_arrived = _pc(arrived, total)
        datamatrix = [
            ["", "Nb. mois", "%"],
            ["Promptitude", on_time, pc_on_time],
            ["Complétude", arrived, pc_arrived],
        ]
        table = generic_table(datamatrix)
        text = "{} : {}".format(name, caption)
        for widget in get_widgets_for(document, text, table, True):
            section.append(widget)

    # district report uses same widgets as region
    WIDGET_DICT = import_path('snisi_malaria.indicators.'
                              'quarter_report.WIDGET_DICT',
                              failsafe=True)

    doc = get_malaria_template(entity, periods, graph_periods,
                               quarter_num, year)

    def add_widget(section, widget_slug, break_before=False):
        indicator_cls = WIDGET_DICT.get(widget_slug)
        if indicator_cls.rendering_type == 'graph':
            indic_periods = graph_periods
        else:
            indic_periods = periods
        indicator_table = indicator_cls(
            entity=entity, periods=indic_periods)
        widgets = widgets_for_indicator(doc,
                                        indicator_table,
                                        break_before=break_before)
        for widget in widgets:
            section.append(widget)

    sectiona = get_section(doc, "A. MORBIDITÉ – MORTALITÉ")
    add_widget(sectiona, 'Tableau1')
    add_widget(sectiona, 'Figure1')
    add_widget(sectiona, 'Figure2', break_before=True)
    add_widget(sectiona, 'Figure3')
    # add_widget(sectiona, 'Figure4')
    add_widget(sectiona, 'Figure5', break_before=True)
    add_widget(sectiona, 'Figure6')

    sectionb = get_section(doc, "B. TRAITEMENT PAR CTA")
    add_widget(sectionb, 'Figure7')
    add_widget(sectionb, 'Figure8')

    sectionc = get_section(doc, "C. CPN, MILD, TIP")
    add_widget(sectionc, 'Figure9')
    add_widget(sectionc, 'Figure10')

    sectiond = get_section(doc, "D. GESTION DE STOCKS")
    add_tableau2(doc, sectiond,
                 ref_periods=count_periods,
                 name="Tableau 2",
                 caption=("Mois de rapportage sans rupture de stock "
                          "dans la structure "
                          "au cours des 12 derniers mois"))
    add_tableau2(doc, sectiond,
                 ref_periods=periods,
                 name="Tableau 2b",
                 caption=("Mois de rapportage sans rupture de stock "
                          "dans la structure "
                          "au cours des 3 derniers mois"))

    sectione = get_section(doc,
                           "E. COMPLÉTUDE ET PROMPTITUDE DU RAPPORTAGE",
                           None)
    add_tableau3(doc, sectione,
                 ref_periods=count_periods,
                 name="Tableau 3",
                 caption=("Taux de promptitude et complétude du rapportage de "
                          "la structure au cours des 12 derniers mois"))
    add_tableau3(doc, sectione,
                 ref_periods=periods,
                 name="Tableau 3b",
                 caption=("Taux de promptitude et complétude du rapportage de "
                          "la structure au cours des 3 derniers mois"))

    get_section(doc, "COMMENTAIRES D'ENSEMBLE")

    get_section(doc, "RECOMMENDATIONS", None)

    return doc


def generate_section_rtf(entity, periods,
                         widget_dict, title,
                         base_path, filename):

    doc = Document()
    ss = doc.StyleSheet
    section = Section()
    doc.Sections.append(section)

    pps_center = ParagraphPS(alignment=ParagraphPS.CENTER)

    header_png = get_resource('malaria', 'header_malaria_report.png')

    section.append(Paragraph(ss.ParagraphStyles.Normal,
                             pps_center, Image(header_png)))

    ps = ParagraphPS()
    p = Paragraph(doc.StyleSheet.ParagraphStyles.Heading1, ps)
    p.append(title)
    section.append(p)

    graph_periods = periods

    for idx, indicator_cls in enumerate(widget_dict):
        break_before = idx % 2 == 0
        if indicator_cls.rendering_type == 'graph':
            indic_periods = graph_periods
        else:
            indic_periods = periods
        indicator_table = indicator_cls(entity=entity, periods=indic_periods)
        widgets = widgets_for_indicator(doc, indicator_table,
                                        break_before=break_before)
        for widget in widgets:
            section.append(widget)

    report_folder = os.path.join(settings.FILES_REPOSITORY, base_path)
    mkdir_p(report_folder)

    if doc and filename:
        filepath = os.path.join(report_folder, filename)
        with open(filepath, 'w') as f:
            Renderer().Write(doc, f)
