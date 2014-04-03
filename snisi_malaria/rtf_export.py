#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging
import os

from rtfw import Document, Section, Paragraph, ParagraphPS, Image, TextPS, TextStyle
from rtfw.PropertySets import Font
from rtfw.Elements import StandardFonts

from snisi_core.rtf_export import widgets_for_indicator
from snisi_tools.misc import import_path

logger = logging.getLogger(__name__)


def get_malaria_template(entity, periods, quarter_num, year):
    doc = Document()
    ss = doc.StyleSheet
    section = Section()
    doc.Sections.append(section)

    pps_center = ParagraphPS(alignment=ParagraphPS.CENTER)
    h1 = ss.ParagraphStyles.Heading1

    # header_bold = TextStyle(TextPS(bold=True)) #, size=18, font=ss.Fonts[26]))
    # ps_header_bold = h1
    # ps_header_bold.SetTextStyle(header_bold)
    # ps_header_bold.SetParagraphPropertySet(pps_center)

    # header_first = TextStyle(TextPS(bold=True, size=16, font=ss.Fonts[1]))
    # ps_header_first = h1
    # ps_header_first.SetTextStyle(header_first)
    # ps_header_first.SetParagraphPropertySet(pps_center)

    # header_times = TextStyle(TextPS(bold=True, size=24, font=ss.Fonts[26]))
    # ps_header_times = h1
    # ps_header_times.SetTextStyle(header_times)
    # ps_header_times.SetParagraphPropertySet(pps_center)

    header_png = os.path.join('snisi_web', 'static', 'img', 'header_malaria_report.png')
    section.append(Paragraph(ss.ParagraphStyles.Normal, pps_center, Image(header_png)))

    section.append(Paragraph(h1, pps_center, "RAPPORT TRIMESTRIEL"))


    section.append(Paragraph(h1, pps_center,
                             "Données de Routine sur le Paludisme au Mali"))
    section.append(Paragraph(h1, pps_center,
                             "Trimestre {qnum}: Période de {speriod} à {eperiod}"
                             .format(qnum=quarter_num,
                                     speriod=periods[0],
                                     eperiod=periods[-1])))
    section.append(Paragraph(h1, pps_center,
                             "MODÈLE DE RAPPORT POUR {}"
                             .format(entity.display_full_name())))
    section.append(Paragraph(ss.ParagraphStyles.Normal, ""))

    return doc


def get_section(document, text):
    section = Section(break_type=Section.PAGE)
    document.Sections.append(section)
    ps = ParagraphPS()
    p = Paragraph(document.StyleSheet.ParagraphStyles.Heading1, ps)
    p.append(text)
    section.append(p)
    return section


def health_region_report(entity, periods, quarter_num, year):

    WIDGET_DICT = import_path('snisi_malaria.indicators.'
                              'quarter_report_region.WIDGET_DICT',
                              failsafe=True)

    doc = get_malaria_template(entity, periods, quarter_num, year)

    def add_widget(section, widget_slug, break_before=False):
        indicator_table = WIDGET_DICT.get(widget_slug)(
            entity=entity, periods=periods)
        widgets = widgets_for_indicator(doc,
                                        indicator_table,
                                        break_before=break_before)
        for widget in widgets:
            section.append( widget )

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

    return doc


def health_district_report(entity, periods, quarter_num, year):

    # district report uses same widgets as region
    WIDGET_DICT = import_path('snisi_malaria.indicators.'
                              'quarter_report_region.WIDGET_DICT',
                              failsafe=True)

    doc = get_malaria_template(entity, periods, quarter_num, year)

    def add_widget(section, widget_slug, break_before=False):
        indicator_table = WIDGET_DICT.get(widget_slug)(
            entity=entity, periods=periods)
        widgets = widgets_for_indicator(doc,
                                        indicator_table,
                                        break_before=break_before)
        for widget in widgets:
            section.append( widget )

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

    return doc
