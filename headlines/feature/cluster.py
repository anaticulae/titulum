# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import serializeraw
import utila

import headlines.cluster.run
import headlines.improve.levelfour
import headlines.utils


def work(  # pylint:disable=R0914
    text: str,
    textpositions: str,
    sizeandborder: str,
    headerfooter: str,
    fontheader: str = None,
    fontcontent: str = None,
    sections: str = None,
    xlevelfour: str = None,
    pages: tuple = None,
) -> str:
    pages = headlines.feature.headlinepart(
        pages=pages,
        sections=sections,
    )
    levelfour = None
    if utila.exists(xlevelfour):
        levelfour = serializeraw.load_headlines(xlevelfour, pages=pages)
    fontstore = serializeraw.create_fontstore(
        header=fontheader,
        content=fontcontent,
        pages=pages,
    )
    ptcns = serializeraw.ptcn_fromfile(
        text,
        textpositions,
        sizeandborder,
        headerfooter,
        fontheader,
        fontcontent,
        pages=pages,
    )
    groups = headlines.cluster.run.run(
        ptcns=ptcns,
        fontstore=fontstore,
    )
    improved = headlines.improve.levelfour.merge_ifbetter(
        groups,
        levelfour,
    )
    detected = headlines.utils.convert_headline_result(
        groups=improved,
        strategy=__name__,
    )
    dumped = serializeraw.dump_headlines(detected)
    return dumped
