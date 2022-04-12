# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import serializeraw
import utila


def work(
    xcluster: str = None,
    xmultiline: str = None,
    xnolevel: str = None,
    xnlarge: str = None,
    xsingle: str = None,
    xstandard: str = None,
    pages: tuple = None,
) -> str:
    sources = [
        item if utila.exists(item) else None for item in
        [xcluster, xmultiline, xnolevel, xnlarge, xsingle, xstandard]
    ]
    headlines = [
        serializeraw.load_headlines(
            content=source,
            pages=pages,
        ) if source else None for source in sources
    ]
    best: iamraw.HeadlineResult = select_best(headlines)
    if not best:
        best = iamraw.HeadlineResult()
    dumped = serializeraw.dump_headlines(best)
    return dumped


def select_best(headlines) -> iamraw.HeadlineResult:
    if not headlines:
        return []
    # TODO: USE BETTER SELECTOR
    best = headlines[0]
    for headline in headlines[1:]:
        if len(headline) < len(best):
            continue
        best = headline
    return best
