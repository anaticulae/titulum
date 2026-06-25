# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import statistics

import configos
import elementae
import germania
import iamraw
import texmex
import utilo

import headlines.config
import headlines.judge
import headlines.level
import headlines.utils

# longer word chains may be a sentence or something else
HEADLINE_TOKEN_LENGTH_MAX = configos.HV_INT_PLUS(default=20)
# assume that headlines does not contain many numbers
NUMBERS_IN_HEADLINE_MAX = configos.HV_INT_PLUS(default=5)

HEADLINE_MEDIAN = configos.HolyTable(items=[
    (10, 40),
    (12, 35),
    (14, 30),
    (16, 26),
    (22, 16),
])

HEADLINE_WORDCOUT_MAX = configos.HV_INT_PLUS(default=20)

HEADLINE_H1_TRY = configos.HolyList(items=[
    14.01,
    12.01,
    11.5,
])


def run(ptcns: texmex.PTCNs) -> iamraw.PagesHeadlineList:
    for h1_try in HEADLINE_H1_TRY:
        utilo.debug(f'multiline, try h1_size_min: {h1_try}')
        collected = collect(
            ptcns,
            h1_size_min=h1_try,
        )
        if not collected:
            continue
        if headlines.judge.invalid_extraction(collected):
            continue
        if not headlines.judge.skip_if_too_few(
                collected,
                document_length=len(ptcns),
                strategy=__name__,
        ):
            continue
        result = headlines.utils.groupby_level_one(collected)
        return result
    return []


def collect(ptcns, h1_size_min: float) -> iamraw.Headlines:
    result = []
    for navigator in ptcns:
        extracted = extract_page(
            navigator,
            h1_size_min=h1_size_min,
        )
        if not extracted:
            continue
        result.extend(extracted)
    return result


def extract_page(
    ptcn: texmex.PTCN,
    h1_size_min: float = 12.01,
) -> iamraw.Headlines:
    """Extract headlines on selected page."""
    result = []
    grouped = texmex.group_page_by_size_distance(ptcn)
    befores = [None] + grouped
    for items, before in zip(grouped, befores):
        if wrong_position(items):
            continue
        if invalid_headline_group(items):
            continue
        raw = plain(items)
        parsed = elementae.parse_headline(raw, before)
        if not parsed:
            continue
        title, level, rawlevel = parsed
        if level == 1:
            # first level headline
            if items.size < h1_size_min:
                continue
        if elementae.noheadline(
                title,
                wordcount_max=HEADLINE_WORDCOUT_MAX,
        ):
            continue
        headline = iamraw.Headline(
            container=headline_range(items),
            level=level,
            page=ptcn.page,
            raw=raw,
            raw_level=rawlevel,
            title=utilo.normalize_whitespaces(title),
        )
        # add decorating if required
        if before:
            before = plain(before)
            chapter = elementae.noheadline_pattern(before)
            if chapter:
                headline.decoration = headline.start - 1
        result.append(headline)
    return result


def headline_range(items):
    if len(items) == 1:
        # single line headline
        container = items.firstid
    else:
        container = (items.firstid, items.firstid + len(items) - 1)
    return container


def invalid_headline_group(items) -> bool:
    text = ' '.join([item.text for item in items])
    tokens = germania.word_tokenize(text, validate_sentences=False)
    if len(tokens) >= HEADLINE_TOKEN_LENGTH_MAX:
        # maybe a sentence cause headlines are not so long
        return True
    number_count = len([token for token in tokens if utilo.isnumber(token)])
    if number_count >= NUMBERS_IN_HEADLINE_MAX:
        # assume that headlines does not contain many numbers
        return True
    if len(items) >= 2:  # multiline
        # In general, multiline headlines fill the whole line. If this
        # does not happen, it is other content which is false positive
        # parsed as headline.
        line_length = [len(item.text) for item in items.text]
        median = statistics.median(line_length)
        median_max = HEADLINE_MEDIAN(items.size)
        if median <= median_max:
            utilo.verbose(f'invalid headline group, median: {median}, '
                          f'max: {median_max}')
            return True
    return False


WRONG_POSITION_X0_MAX = configos.HV_FLOAT_PLUS(default=200.0)


def wrong_position(
    items,
    max_x0: float = WRONG_POSITION_X0_MAX,
) -> bool:
    """We assume that headlines start on the left side of the document.
    This should skip false possitive headline extraction.

    TODO: RUN SECOND EXTRACTION WITHOUT LEFTSTARTED AND COMPARE TO
    SUPPORT RIGHT ALIGNED HEADLINES?
    """
    return items.bounding[0] >= max_x0


def filter_headlines(result: iamraw.PagesHeadlineList) -> dict:
    """Convert chapter level based on text distances to logical level
    (1,2,3,4,...).

    Hint: This function updates the level
    TODO: copy items
    """
    utilo.call('convert_level')
    # TODO: VERIFY THIS
    empty = False
    if not result:
        empty = True
    if not any(result.values()):
        empty = True
    if not any(item for item in result.values()):
        empty = True
    if empty:
        # check that result pages are empty
        utilo.info('empty PageHeadlineList')
        return {}
    assert isinstance(result, dict), type(result)
    nolevel = []
    for item in result.values():
        nolevel.extend(item)
    level = [item for item in nolevel if isinstance(item.level, int)]
    if not level:
        result = headlines.level.cluster_headline_level(result)
    return result


def plain(items: list) -> str:
    # TODO: REPLACE WITH UTILA CODE
    raw = ' '.join([item.text.strip() for item in items])
    return raw
