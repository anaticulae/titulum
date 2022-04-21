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

import elements
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
    sizes = textsizes(navigator)
    bolds = bold(navigator, fontstore)
    italics = italic(navigator, fontstore)
    underlines = underlined(navigator)
    fonts = textfonts(navigator, fontstore)
    top, bottom = topbottom(navigator)
    left, right = leftright(navigator)
    visibles = visible(navigator)
    equal_length = [
        len(item) for item in
        [sizes, fonts, top, bottom, left, right, underlines, visibles]
    ]
    assert len(set(equal_length)) == 1, f'different iter length {equal_length}'
    result = [
        sizes,
        bolds,
        italics,
        underlines,
        left,
        uppers,
        visibles,
    ]
    return result


def textlength(navigator) -> utila.Ints:
    return textvalue(navigator, selector=lambda item: len(item.text.strip()))


def visible(navigator) -> utila.Ints:

    def invisible(item):
        if not item.visible:
            return True
        if elements.noheadline(item.text):
            return True
        return False

    return textvalue(
        navigator,
        selector=lambda x: 100 if not invisible(x) else 1,
    )


# float is required to use cluster algorithm
BOLD = 100.0
NO_BOLD = 10.0


def bold(navigator, fontstore) -> utila.Floats:

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

    def isbold(item) -> float:
        fontids = texmex.TextStyle.fontids(
            item.style,
            more_than_eighty_or_nothing,
        )
        if len(fontids) > 1:
            return NO_BOLD
        font = fontstore[item.style.fontid]
        weight = font.weight
        if weight == iamraw.Weight.BOLD:
            return BOLD
        return NO_BOLD

    return textvalue(navigator, selector=isbold)


def underlined(navigator) -> utila.Floats:

    def isunderlined(item):
        return 100.0 if item.style.underlined else 10.0

    return textvalue(navigator, selector=isunderlined)


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


def textfonts(
    navi: texmex.NavigatorMixin,
    fontstore: iamraw.FontStore,
) -> utila.Ints:
    assert issubclass(navi.__class__, texmex.NavigatorMixin), type(navi)
    collected = []
    for line in navi:
        # determine most common font family
        family = [[char.font] * char.width for char in line.style]
        family = utila.flatten(family)
        collected.append(utila.mode(family))
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
