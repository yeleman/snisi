#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging
import os
import tempfile

import requests
from py3compat import text_type
from django.template import loader, Context
from rtfw import (Paragraph, Table, BorderPS, FramePS, Cell,
                  Image, ParagraphPS, TEXT)

from snisi_web.templatetags.snisi import number_format

logger = logging.getLogger(__name__)


globaloptions = '''
{
    lang: {
    months: ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin',  'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre'],
    weekdays: ['Dimanche', 'Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi'],
    decimalPoint: ",",
    downloadPNG: "Exporter en PNG",
    drillUpText: "Revenir à {series.name}.",
    loading: "Chargement…",
    printChart: "Imprimer",
    numericSymbols: [null, null, null, null, null, null],
    resetZoom: "Restaurer niveau de zoom.",
    resetZoomTitle: "Restaurer le niveau de zoom 1:1.",
    shortMonths: [ "Jan" , "Fév" , "Mar" , "Avr" , "Mai" , "Jui" , "Juil" , "Aôu" , "Sep" , "Oct" , "Nov" , "Déc"],
    thousandsSep: " ",
    contextButtonTitle: "Menu contextuel"
},
global: {
    useUTC: true
}
}'''


def retrieve_chart_from_highcharts(highcharts):

    payload = {
        'content': 'options',
        'options': highcharts,
        'globaloptions': globaloptions,
        'type': 'image/png',
        'width': '440',
        'scale': '',
        'constr': 'Chart',
        'callback': ''}

    url = "http://export.highcharts.com"
    req = requests.post(url, data=payload)

    if req.status_code == requests.codes.ok:
        return req.content

    return None


def neutral_style(document, indicator_table):
    return Paragraph(document.StyleSheet.ParagraphStyles.Normal)


def neutral_centered_style(document, indicator_table):
    ps = ParagraphPS(alignment=ParagraphPS.CENTER)
    return Paragraph(document.StyleSheet.ParagraphStyles.Normal, ps)


def widgets_for_indicator(document, indicator_table, break_before=False):
    constructor = graph_for_indicator \
        if indicator_table.rendering_type == 'graph' \
        else table_for_indicator
    widgets = [title_for_indicator(document, indicator_table,
                                   break_before=break_before)]
    if indicator_table.rendering_type == 'table':
        widgets.append(neutral_style(document, indicator_table))
    widgets.append(constructor(document, indicator_table))
    return widgets


def error_widget(document, text):
    p = Paragraph(document.StyleSheet.ParagraphStyles.Normal,
                  text)
    p.append(text)
    return p


def title_for_indicator(document, indicator_table, break_before=False):
    if indicator_table.name:
        text = "{} : {}".format(indicator_table.name,
                                indicator_table.caption)
    else:
        text = indicator_table.caption
    return title_for_text(document=document,
                          text=text,
                          break_before=break_before)


def title_for_text(document, text, break_before=False):
    p = Paragraph(document.StyleSheet.ParagraphStyles.Heading2,
                  ParagraphPS().SetPageBreakBefore(break_before))
    p.append(text)
    return p


def graph_for_indicator(document, indicator_table):

    # get the highcharts code
    context = {'table': indicator_table, 'id': ''}
    highcharts = loader.get_template('highcharts_graph.js') \
                       .render(Context(context))

    # get the image from highcharts.com
    content = retrieve_chart_from_highcharts(highcharts)
    if content is None:
        return error_widget("Impossible de générer l'image")

    # write image to a temporary file
    f = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
    f.write(content)
    f.close()

    # create the image object and remove temp file
    try:
        image = Image(f.name)
    except:
        logger.error("Failed to create image")
        raise
        return Paragraph("Erreur")

    os.unlink(f.name)

    ps = ParagraphPS(alignment=ParagraphPS.CENTER)
    p = Paragraph(document.StyleSheet.ParagraphStyles.Normal, ps)
    p.append(image)
    return p


def table_for_indicator(document, indicator_table):

    if not indicator_table.nb_lines():
        return error_widget("Aucune période")

    minify = indicator_table.periods > 3
    col_large = 3000
    col_regular = 1000
    col_intro_mini = 2600
    col_mini = 670
    col_mini_pc = 570

    thin_edge = BorderPS(width=20, style=BorderPS.SINGLE)
    # thick_edge = BorderPS( width=80, style=BorderPS.SINGLE )

    def p(text, align_center=False):
        text_elem = TEXT(text, size=14) if minify else text
        return Paragraph(ParagraphPS(
            alignment=ParagraphPS.CENTER if align_center
            else ParagraphPS.LEFT), text_elem)

    thin_frame = FramePS(thin_edge,  thin_edge,  thin_edge,  thin_edge)
    # thick_frame = FramePS( thick_edge, thick_edge, thick_edge, thick_edge )
    # mixed_frame = FramePS( thin_edge,  thick_edge, thin_edge,  thick_edge )

    # build base table (7 columns)
    cols = [col_intro_mini] if minify else [col_large]
    for _ in indicator_table.periods:
        cols.append(col_mini if minify else col_regular)
        if indicator_table.add_percentage:
            cols.append(col_mini_pc if minify else col_regular)
    if indicator_table.add_total:
        cols.append(col_mini if minify else col_regular)
    table = Table(*cols, alignment=Table.CENTER)

    # first header row : title and period names
    args = []
    for period in indicator_table.periods:
        span = 2 if indicator_table.add_percentage else 1
        args.append(Cell(p(text_type(period), True),
                    thin_frame, span=span))
    if indicator_table.add_total:
        args.append(Cell(p("TOTAL", True), thin_frame))

    table.AddRow(Cell(indicator_table.title,
                      thin_frame, start_vertical_merge=True),
                 *args)

    # second header row : Nbre/% sub header
    args = []
    for period in indicator_table.periods:
        args.append(Cell(p("Nbre", True), thin_frame))
        if indicator_table.add_percentage:
            args.append(Cell(p("%", True), thin_frame))
    if indicator_table.add_total:
        args.append(Cell(p("Nbre", True), thin_frame))

    table.AddRow(Cell(thin_frame, vertical_merge=True), *args)

    # data rows
    for line in indicator_table.render_with_labels_human(as_human=True):
        args = []
        for idx, cell_data in enumerate(line):
            align_center = not idx == 0
            args.append(Cell(p(number_format(cell_data), align_center),
                        thin_frame))

        table.AddRow(*args)

    return table


def generic_table(datamatrix, title=""):

    """ Generic Table based on a strict input format:

        datamatrix = [
            ["Item Header", "Col1 header", "Col2 Header"],
            ["Line 1 name", "Col1 Data", "Col2 Data"],
            ["Line 2 name", "Col1 Data", "Col2 Data"],
        ]
    """

    if not len(datamatrix):
        return error_widget("Aucune ligne pour le tableau")

    nb_col = len(datamatrix[-1])

    # smart column sizes
    if nb_col <= 3:
        col_large = 6000
        col_regular = 2000
    elif nb_col <= 5:
        col_large = 4000
        col_regular = 1500
    else:
        col_large = 3000
        col_regular = 1000

    thin_edge = BorderPS(width=20, style=BorderPS.SINGLE)

    def p(text, align_center=False):
        return Paragraph(ParagraphPS(
            alignment=ParagraphPS.CENTER if align_center
            else ParagraphPS.LEFT), text)

    thin_frame = FramePS(thin_edge,  thin_edge,  thin_edge,  thin_edge)

    cols = [col_large]
    for _ in range(1, nb_col):
        cols.append(col_regular)
    table = Table(*cols)

    # first header row : title and period names
    args = []
    for header in datamatrix[0]:
        args.append(Cell(p(text_type(header), True), thin_frame))
    table.AddRow(*args)

    # data rows
    for line in datamatrix[1:]:
        args = []
        for idx, cell_data in enumerate(line):
            align_center = not idx == 0
            args.append(Cell(p(number_format(cell_data), align_center),
                        thin_frame))
        table.AddRow(*args)

    return table
