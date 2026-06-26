# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Surround
========

Check the area before and after the detected line to may merge them into
detected headline.
"""

import contextlib

import elementae
import utilo


def run(headlines, ptcns):
    return before_and_after(headlines, ptcns)


def before_and_after(headlines, ptcns):
    for chapter in headlines:
        for headline in chapter:
            page = utilo.select_page(ptcns, headline.page)
            headline_expand(headline, page)
    return headlines


def headline_expand(headline, page):
    before, after = None, None  # pylint:disable=W0612
    with contextlib.suppress(IndexError):
        headline_start = headline.container
        if isinstance(headline_start, tuple):
            headline_start = headline_start[0]
        before = page[headline_start - 1]
    with contextlib.suppress(IndexError):
        headline_end = headline.container
        if isinstance(headline_end, tuple):
            headline_end = headline_end[-1]
        after = page[headline_end + 1]
    # TODO: UNUSED AFTER
    if before:
        if elementae.noheadline_pattern(before.text):
            headline.decorator = headline_start - 1
    return headline
