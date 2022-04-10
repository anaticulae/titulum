# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools

import elements
import iamraw
import texmex

import headlines.multiline.run
import headlines.standard.run


def run(ptcns: texmex.PTNs) -> iamraw.PagesHeadlineList:
    page_parser = functools.partial(
        headlines.standard.run.parse_page,
        headline_extractor=extract_headline,
    )
    result = headlines.standard.run.run(
        ptcns,
        page_parser=page_parser,
        finalizer=finalizer,
    )
    return result


def finalizer(collected) -> list:
    # TODO: DIRTY, ADJUST THE INTERFACES!
    data = {0: collected}
    result = filter_headlines(data)
    if not result:
        return []
    result = [result[0]]
    return result


def filter_headlines(items):  # pylint:disable=R0201
    """Convert level etc."""
    # TODO: IMprove this
    result = {}
    for number, chapter in items.items():
        # skip `normal` headlines, we want to analyze NoLevelHeadlines
        items = [
            item for item in chapter
            if not item.raw_level and not elements.noheadline_pattern(item.raw)
        ]
        result[number] = items
    # TODO: USE DICT CONVERTER HERE
    result = headlines.multiline.run.filter_headlines(result)
    return result


def should_skip(distance_tosmall, headline_tosmall, **kwargs):  # pylint:disable=W0613
    if distance_tosmall and headline_tosmall:
        return True
    if headline_tosmall:
        return True
    return False


def extract_headline(**kwargs):
    kwargs['textdistance'] = kwargs['textdistance'] * 1.2
    kwargs['textsize'] = kwargs['textsize'] * 1.05
    return headlines.standard.run.extract_headline(
        **kwargs,
        skipper=should_skip,
    )
