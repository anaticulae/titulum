# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""NumberLarge
===========

Detect first level headline with a large Chapter Number.

C O N C L U S I O N         8
"""

import configo
import iamraw
import texmex
import utila


def run(ptcns: texmex.PTCNs) -> iamraw.PagesHeadlineList:
    result = []
    for page in ptcns:
        headline = headline_frompage(page)
        if not headline:
            continue
        result.append([headline])
    return result


BEFORE = configo.HV_PERCENT_PLUS(default=20)


def headline_frompage(page) -> iamraw.Headline:
    content = page.before(BEFORE)
    pagenumbers = []
    headlines = []
    for line in content:
        text, size = line.text.strip(), line.bounding_mean
        if size >= 50:
            isappendix = text.upper() == 'A'
            isnumber = text.isnumeric()
            if isappendix or isnumber:
                pagenumbers.append(text)
                continue
        isheadline = utila.issinglechar(text)
        if isheadline:
            headlines.append(text.replace(' ', ''))
            continue
    if not headlines or len(headlines) > 1:
        return None
    if not pagenumbers or len(pagenumbers) > 1:
        return None
    headline, pagenumber = headlines[0], pagenumbers[0]
    result = iamraw.Headline(
        title=headline,
        level=1,
        page=page.page,
        container=1,  # title
        decoration=0,  # big number
        raw=f'{pagenumber} {headline}',
        # raw_level=pagenumber,
        raw_level=f'{pagenumber}.',
    )
    return result
