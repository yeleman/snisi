#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

""" common type checking/conversion for data coming from Excel """

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)


def clean(value):
    """ a stripped unicode """
    return "{}".format(value).strip()


def clean_str(value):
    """ lowercased stripped unicode """
    return clean(value).lower()


def ChoiceList(value, choicelist):
    """ value if included in provided list """
    if value in choicelist:
        return value
    else:
        raise ValueError("{} not in {}".format(value, choicelist))


def LowerChoiceList(value, choicelist):
    """ cleaned value if it is included in provided list """
    if clean_str(value) in choicelist:
        return clean_str(value)
    else:
        raise ValueError("{} not in {}".format(clean_str(value),
                                               choicelist))


def NormalizedChoiceList(value, choicemap):
    """ mapped value of a cleaned index in a provided dict """
    if clean_str(value) in choicemap:
        return choicemap[clean_str(value)]
    else:
        raise ValueError("{} not in {}".format(clean_str(value),
                                               list(choicemap.keys())))


def NormalizedIntChoiceList(value, choicelist):
    """ int value if it is included in provided list of int """
    if int(value) in choicelist:
        return int(value)
    else:
        raise ValueError("{} not in {}".format(clean_str(value), choicelist))
