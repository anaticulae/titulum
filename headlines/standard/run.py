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

HEADLINE_LENGTH_MIN = configo.HV_INT_PLUS(default=7)


def run(ptcns: texmex.PTNs) -> iamraw.PagesHeadlineList:
    textsize = texmex.document_textsize(navigators=ptcns)
    textdistance = texmex.document_textdist_from_ptcns(
        navigators=ptcns,
        digits=0,
    )
    collected = []
    for page in ptcns:
        parsed = parse_page(page, textsize, textdistance)
        if not parsed:
            continue
        collected.extend(parsed)
    collected = groupby_level_one(collected)
    return collected


def parse_page(ptcn: texmex.PTCN, textsize, textdistance):
    bounds = texmex.textbounds(ptcn, ptcn.content)
    without_content = [item.bounds for item in bounds]
    # PageContentNavigator: skip header and footer content
    textdistances = texmex.fontdistance_textbounds(without_content)
    textfeeds = [item.bounds.leftdist for item in bounds]
    result = []
    for containerid, item in enumerate(ptcn):
        splitted = item.text.splitlines()
        if len(splitted) > 1:
            # TODO: REMOVE?
            continue
        headline = extract_headline(
            textinfo=item,
            textdistances=textdistances,
            textfeeds=textfeeds,
            textsize=textsize,
            textdistance=textdistance,
            ptcn=ptcn,
            containerid=containerid,
        )
        if not headline:
            # try again with double line extractor
            headline = extract_headline(
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
            continue
        result.append(headline)
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
):  # pylint:disable=R0914
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

    if elements.noheadline(text):
        return None

    # dist_top = textdistances[containerid]
    # try:
    #     dist_bottom = None if lastitem else textdistances[look_forward]
    # except IndexError:
    #     return None
    # style = dict(
    #     textsize=textsize,
    #     before=dist_top,
    #     after=dist_bottom,
    #     feed=textfeed,
    # )
    decoration = headline_decoration(
        navigator=ptcn,
        containerid=containerid,
    )
    parsed = elements.parse_headline(text.strip())
    raw_level = parsed[2] if parsed else None
    level = parsed[1] if parsed else None
    headline = iamraw.Headline(
        container=containerid,
        level=level,
        page=ptcn.page,
        raw=text.strip(),
        title=text.strip(),
        decoration=decoration,
        raw_level=raw_level,
    )
    return headline


def headline_decoration(navigator, containerid: int) -> int:
    if not navigator:
        # HACK
        return None
    before = navigator[containerid - 1] if containerid > 0 else None
    # after = navigator[containerid + 1] if containerid + 1 < len(navigator) else None
    if before and elements.noheadline_pattern(before.text):
        return containerid - 1
    return None


DISTANCE_TOO_SMALL = configo.HolyTable(
    items=(
        (0, 1.2),
        (1, 1.15),
        (2, 1.1),
        (3, 1.0),
    ),
    right_outranges_none=False,
)
TEXTSIZE_TOO_SMALL = configo.HolyTable(
    items=(
        (0, 1.12),
        (1, 1.08),
        (2, 1.05),
        (3, 1.0),
    ),
    right_outranges_none=False,
)


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


def groupby_level_one(heads: list) -> iamraw.PagesHeadlineList:
    result = []
    # detect chapter starts
    levelone = [
        index for (index, item) in enumerate(heads) if item.level in (None, 1)
    ]
    # group headlines into chapters
    result = [
        heads[index:after]
        for (index, after) in zip(levelone[:-1], levelone[1:])
    ]
    if levelone:
        # do not forget the last group
        result.append(heads[levelone[-1]:])
    return result
