# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configo
import elements
import iamraw
import texmex
import utila

import headlines.judge
import headlines.level
import headlines.utils

HEADLINE_LENGTH_MIN = configo.HV_INT_PLUS(default=7)

HEADLINE_FONT_SIZE_MAX = configo.HV_INT_PLUS(default=75, limit=120)

HEADLINE_COUNT_PERPAGE_MAX = configo.HV_INT_PLUS(default=5)


def run(
    ptcns: texmex.PTNs,
    page_parser: callable = None,
    finalizer: callable = None,
) -> iamraw.PagesHeadlineList:
    page_parser = parse_page if not page_parser else page_parser
    finalizer = finalize if not finalizer else finalizer
    textsize = texmex.document_textsize(navigators=ptcns)
    if textsize is None:
        utila.error('empty document, skip standard')
        return []
    textdistance = texmex.document_textdist_from_ptcns(
        navigators=ptcns,
        digits=0,
    )
    collected = []
    for page in ptcns:
        parsed = page_parser(page, textsize, textdistance)
        if not parsed:
            continue
        collected.extend(parsed)
    if not headlines.judge.skip_if_too_few(
            collected,
            document_length=len(ptcns),
            strategy=__name__,
    ):
        return []
    result = finalizer(collected)
    return result


def finalize(collected) -> list:
    # TODO: ADJUST INTERFACE LATER
    # update level
    headlines.level.cluster_headline_level({0: collected})
    result = headlines.utils.groupby_level_one(collected)
    return result


def parse_page(  # pylint:disable=R0914
    ptcn: texmex.PTCN,
    textsize,
    textdistance,
    headline_extractor: callable = None,
):
    if not headline_extractor:
        headline_extractor = extract_headline
    bounds = texmex.textbounds(ptcn, ptcn.content)
    without_content = [item.bounds for item in bounds]
    # PageContentNavigator: skip header and footer content
    textdistances = texmex.fontdistance_textbounds(without_content)
    textfeeds = [item.bounds.leftdist for item in bounds]
    parsed = []
    for containerid, item in enumerate(ptcn):
        splitted = item.text.splitlines()
        if len(splitted) > 1:
            # TODO: REMOVE?
            continue
        headline = headline_extractor(
            textinfo=item,
            textdistances=textdistances,
            textfeeds=textfeeds,
            textsize=textsize,
            textdistance=textdistance,
            ptcn=ptcn,
            containerid=containerid,
            double=True,
        )
        if not headline:
            # try again without double line extractor
            headline = headline_extractor(
                textinfo=item,
                textdistances=textdistances,
                textfeeds=textfeeds,
                textsize=textsize,
                textdistance=textdistance,
                ptcn=ptcn,
                containerid=containerid,
                double=False,
            )
        if not headline:
            continue
        parsed.append(headline)
    # filter duplication
    single = utila.Single()
    result = []
    for headline in parsed:
        containers = utila.ensure_tuple(headline.container)
        if [item for item in containers if single.contains(item)]:
            continue
        result.append(headline)
    if len(result) > HEADLINE_COUNT_PERPAGE_MAX:
        utila.debug(f'too many headlines: {len(result)} on page: {ptcn.page}')
        return []
    return result


def extract_headline(
    textinfo,
    textdistances,
    textfeeds,
    ptcn: texmex.PageTextContentNavigator,
    containerid: int,
    skipper=None,
    double: bool = False,
    **kwargs,
):  # pylint:disable=R0914,R1260,R0911
    """\
    double - parse two line as possible headline(backup strategy)

    TODO: INTRODUCE TRIPPLE
    """
    look_forward = containerid + 2 if double else 1
    text = textinfo.text
    try:
        fontdistance = textdistances[look_forward]
    except IndexError:
        return None
    if containerid:
        # for non page start check distance before and after
        fontdistance += textdistances[containerid]
        fontdistance = fontdistance / 2.0
    textfeed = textfeeds[containerid]
    textsize = texmex.TextStyle.textsizes(textinfo.style)
    distance_toosmall, headline_toosmall, higher_equalthree = too_small(
        text,
        fontdistance,
        textsize,
        **kwargs,
    )
    lastitem = look_forward == len(ptcn)
    if len(text) < HEADLINE_LENGTH_MIN:
        return None
    skipper = should_skip if skipper is None else skipper
    skip = skipper(
        distance_tosmall=distance_toosmall,
        headline_tosmall=headline_toosmall,
        textfeed=textfeed,
        lastitem=lastitem,
    )
    if skip and not higher_equalthree:
        return None
    if textsize > HEADLINE_FONT_SIZE_MAX:
        return None
    raw_text = text.strip()
    # try to merge next container to parse double headline
    merge_next = double and not lastitem and merges_next(
        textinfo,
        ptcn[containerid + 1],
    )
    if merge_next:
        raw_text += ' ' + ptcn[containerid + 1].text
    if elements.noheadline(raw_text):
        return None
    dist_top = textdistances[containerid]
    try:
        dist_bottom = None if lastitem else textdistances[look_forward]
    except IndexError:
        return None
    style = dict(
        textsize=textsize,
        before=dist_top,
        after=dist_bottom,
        feed=textfeed,
    )
    decoration = headline_decoration(
        navigator=ptcn,
        containerid=containerid,
    )
    parsed = elements.parse_headline(raw_text)
    raw_level = parsed[2] if parsed else None
    title = parsed[0] if parsed else raw_text
    # level = parsed[1] if parsed else None
    headline = iamraw.Headline(
        container=(containerid, containerid + 1) if merge_next else containerid,
        level=style,
        page=ptcn.page,
        raw=raw_text,
        title=title,
        decoration=decoration,
        raw_level=raw_level,
    )
    return headline


def merges_next(current, after) -> bool:
    if current.style.textsize() != after.style.textsize():
        return False
    if len(current.text) < len(after.text):
        return False
    parsed = elements.parse_headline(after.text)
    if parsed:
        # raw level
        if parsed[2]:
            return False
    # check equal alignment
    # high diff to ensure that intendet second line is merged
    aligned = utila.near(
        current.bounding[0],
        after.bounding[0],
        diff=70.0,
    )
    aligned |= utila.near(current.bounding[2], after.bounding[2])
    if not aligned:
        return False
    return True


def headline_decoration(navigator, containerid: int) -> int:
    if not navigator:
        # HACK
        return None
    before = navigator[containerid - 1] if containerid > 0 else None
    # after = navigator[containerid + 1] if containerid + 1 < len(navigator) else None
    if before and elements.noheadline_pattern(before.text):
        return containerid - 1
    return None


DISTANCE_TOO_SMALL = configo.HolyTable(items=[
    (0, 1.2),
    (1, 1.15),
    (2, 1.1),
    (3, 1.0),
])
TEXTSIZE_TOO_SMALL = configo.HolyTable(items=[
    (0, 1.12),
    (1, 1.08),
    (2, 1.05),
    (3, 1.0),
])


def too_small(text, fontdistance, textsize_, **kwargs):
    level = elements.level_numbered(text)
    level = 0 if level is None else level

    distance_tosmall = fontdistance < kwargs['textdistance'] * DISTANCE_TOO_SMALL(level) # yapf:disable
    headline_tosmall = textsize_ < kwargs['textsize'] * TEXTSIZE_TOO_SMALL(level) # yapf:disable

    higher_equalthree = level is not None and level >= 3
    if higher_equalthree:
        # deactivate distance check for 3.1.1. etc. cause it is a very
        # expressive pattern and these headlines can be very small.
        distance_tosmall = False
        headline_tosmall = False
    return distance_tosmall, headline_tosmall, higher_equalthree


def should_skip(
        distance_tosmall,
        headline_tosmall,
        textfeed,  # pylint:disable=W0613
        lastitem,  # pylint:disable=W0613
):
    # if textfeed > words.headlines.strategies.MAX_HEADLINE_TEXTFEED:
    #     # skip numbered lists
    #     return True
    if distance_tosmall:
        return True
    if headline_tosmall:
        return True
    return False
