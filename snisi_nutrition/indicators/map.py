#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging

from snisi_nutrition.indicators.sam import (
    SAMHealedRate, SAMDeceasedRate, SAMAbandonRate, SAMCaseloadTreatedRate)
from snisi_nutrition.indicators.mam import (
    MAMHealedRate, MAMDeceasedRate, MAMAbandonRate, MAMCaseloadTreatedRate)

logger = logging.getLogger(__name__)


