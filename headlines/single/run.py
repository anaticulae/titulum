# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configos
import elementae
import iamraw
import texmex

import headlines.judge
import headlines.utils

SINGLEPAGE_LINES_MAX = configos.HV_INT_PLUS(default=3)


def run(ptcns: texmex.PTCNs) -> iamraw.PagesHeadlineList:
    collected = []
    for page in ptcns:
        parsed = parse_page(page)
        if not parsed:
            continue
        if headlines.judge.invalid_extraction(parsed):
            continue
        parsed = headlines.utils.groupby_level_one(parsed)
        collected.extend(parsed)
    return collected


def parse_page(ptcn) -> iamraw.Headlines:
    if len(ptcn) > SINGLEPAGE_LINES_MAX:
        # TODO: MAKE THIS COUNT SIZE DEPENDENT?
        return None
    result = []
    for container, line in enumerate(ptcn):
        # TODO: HOLY VALUE
        if line.bounding_mean < 18.0:
            continue
        if not elementae.isheadline(line.text):
            continue
        parsed = elementae.parse_headline(line.text)
        if parsed:
            title, level, rawlevel = parsed
        else:
            title, level, rawlevel = line, 1, ''
        result.append(
            iamraw.Headline(
                title=title.strip(),
                container=container,
                level=level,
                raw=line.text,
                raw_level=rawlevel,
                page=ptcn.page,
            ))
    return result
