# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections
import typing

import iamraw
import texmex
import utila

VerticalTextDistance = collections.namedtuple(
    'VerticalTextDistance',
    'top, bottom',
)
VerticalTextDistances = typing.List[VerticalTextDistance]


def parses(
    navigators: texmex.PTCNs,
    fontstore: iamraw.FontStore,
) -> iamraw.PageTextPropertiesList:
    result = []
    for navigator in navigators:
        parsed = parse_vector(navigator, fontstore)
        result.append(parsed)
    return result


def parse_vector(
    navigator: texmex.PTCN,
    fontstore: iamraw.FontStore,
) -> iamraw.PageTextProperties:
    if not navigator:
        # empty page
        return []
    uppers = upperrate(navigator)
    # lengths = textlength(navigator)
    # hashed = [item.text.strip() for item in navigator]
    sizes = textsizes(navigator)
    bolds = bold(navigator, fontstore)
    italics = italic(navigator, fontstore)
    fonts = textfonts(navigator, fontstore)
    top, bottom = topbottom(navigator)
    left, right = leftright(navigator)
    equal_length = [
        len(item) for item in [sizes, fonts, top, bottom, left, right]
    ]
    assert len(set(equal_length)) == 1, f'different iter length {equal_length}'
    result = [
        sizes,
        bolds,
        italics,
        left,
        uppers,
    ]
    return result


def textdistances(navigator, digits: int = 1) -> VerticalTextDistances:
    # TODO: MOVE TO TEXMEX
    if not navigator:
        return []
    if len(navigator) == 1:
        # no predecessor and successor
        return [VerticalTextDistance(None, None)]
    ypos = vertical_position(navigator)

    # first
    result = [VerticalTextDistance(None, ypos[0].bottom - ypos[1].bottom)]
    for before, current, after in zip(ypos[0:-2], ypos[1:-1], ypos[2:]):
        # middles
        top_distance = before.bottom - current.bottom
        bottom_distance = current.bottom - after.bottom
        result.append(VerticalTextDistance(top_distance, bottom_distance))
    # last
    result.append(VerticalTextDistance(ypos[-2].bottom - ypos[-1].bottom, None))

    # round to have propper user output/developer handling
    rounded = round_vertical_distances(result, digits=digits)
    return rounded


def round_vertical_distances(items, digits: int = 1):
    """Round list of `VerticalTextDistances`.

    >>> round_vertical_distances([VerticalTextDistance(1.333, None), VerticalTextDistance(5.88, 5.0)])
    [VerticalTextDistance(top=1.3, bottom=None), VerticalTextDistance(top=5.9, bottom=5.0)]
    """
    result = []
    for item in items:
        before = utila.roundme(
            item[0],
            digits=digits,
        ) if item[0] is not None else None
        after = utila.roundme(
            item[1],
            digits=digits,
        ) if item[1] is not None else None
        result.append(VerticalTextDistance(before, after))

    return result


def textlength(navigator) -> utila.Ints:
    return textvalue(navigator, selector=lambda item: len(item.text.strip()))


def textwidth(navigator) -> utila.Floats:
    return textvalue(
        navigator,
        selector=lambda item: item.bounding.x1 - item.bounding.x0,
    )


def bold(navigator, fontstore) -> utila.Floats:

    bold_ = 100.0
    no_bold = 10.0

    def more_than_eighty_or_nothing(items):
        """Bold detection requires that more than eigthy percent of the
        characters are bold.

        In some bolded headlines there are spaces characters which are
        not bold and in some sentences only some words are bold.
        """
        counter = collections.Counter()
        for item in items:
            counter[item] += 1
        item, count = counter.most_common(n=1)[0]
        # TODO: HOLY VALUE
        if count < 0.8 * len(items):
            return set(items)
        return {item}

    def isbold(item):
        fontids = texmex.TextStyle.fontids(
            item.style,
            more_than_eighty_or_nothing,
        )
        if len(fontids) > 1:
            return no_bold
        font = fontstore[item.style.fontid]
        weight = font.weight
        return bold_ if weight == iamraw.Weight.BOLD else no_bold

    return textvalue(navigator, selector=isbold)


def italic(navigator, fontstore) -> utila.Floats:

    def isitalic(item):
        font = fontstore[item.style.fontid]
        style = font.style
        return 100.0 if style == iamraw.Style.ITALIC else 10.0

    return textvalue(navigator, selector=isitalic)


def textuppper(navigator) -> utila.Floats:
    result = textvalue(
        navigator,
        selector=lambda item: len([it for it in item.text if it.isupper()]),
    )
    return result


def upperrate(navigator) -> utila.Floats:
    uppers = textuppper(navigator)
    lengths = textlength(navigator)
    result = [
        100 if length >= 5 and (upper / length) > 0.4 else 10
        for upper, length in zip(uppers, lengths)
    ]
    result = utila.roundme(result, convert=False)
    return result


def textvalue(navigator, selector: callable) -> utila.Ints:
    return [selector(item) for item in navigator]


def textsizes(navi: texmex.NavigatorMixin) -> utila.Floats:
    assert issubclass(navi.__class__, texmex.NavigatorMixin), type(navi)
    collected = []
    for line in navi:
        # determine most common text size
        fontsizes = [
            [char.size] * (char.end - char.start) for char in line.style
        ]
        fontsizes = utila.flatten(fontsizes)
        collected.append(utila.mode(fontsizes, minimize=True))
    return collected


def textfonts(navi: texmex.NavigatorMixin, fontstore=None) -> utila.Ints:
    assert issubclass(navi.__class__, texmex.NavigatorMixin), type(navi)
    collected = []
    for line in navi:
        # determine most common font family
        family = [[char.font] * char.width for char in line.style]
        family = utila.flatten(family)
        collected.append(utila.mode(family))
    if fontstore:
        collected = [hash(fontstore[item].name) for item in collected]
    return collected


def topbottom(navigator) -> VerticalTextDistances:
    if not navigator:
        return []
    border = iamraw.Border(0, navigator.width, 0, navigator.height)
    bounds = texmex.textbounds(navigator, border)
    # ignore empty content
    bounds = [item.bounds for item in bounds if len(item.text)]
    tops = [bounds[0].topdist]
    if len(bounds) > 1:
        tops.extend(utila.diffs([item.topdist for item in bounds]))
    tops: list = utila.roundme(tops, convert=False)
    bottoms = []
    if len(bounds) > 1:
        bottoms.extend(utila.diffs([item.bottomdist for item in bounds]))
    bottoms.append(bounds[-1].bottomdist)
    bottoms: list = utila.roundme(bottoms, convert=False)
    return tops, bottoms


def vertical_position(navigator) -> VerticalTextDistances:
    if not navigator:
        return []
    border = iamraw.Border(0, navigator.width, 0, navigator.height)
    bounds = texmex.textbounds(navigator, border)
    # ignore empty content
    bounds = [item.bounds for item in bounds if len(item.text)]
    dist = [
        VerticalTextDistance(
            item.topdist,
            item.bottomdist,
        ) for item in bounds
    ]
    return dist


def leftright(navigator) -> VerticalTextDistances:
    if not navigator:
        return [], []
    # ignore empty content
    border = iamraw.Border(0, navigator.width, 0, navigator.height)
    bounds = texmex.textbounds(navigator, border)
    bounds = [item.bounds for item in bounds if len(item.text)]
    left = [item.leftdist for item in bounds]
    right = [item.rightdist for item in bounds]
    return left, right
