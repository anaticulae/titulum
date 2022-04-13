# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import texmex

import headlines.cluster.run


def run(
    ptcns: texmex.PTCNs,
    fontstore: iamraw.FontStore,
) -> iamraw.PagesHeadlineList:
    matrix, ptcns, _ = headlines.cluster.run.create_matrix(ptcns, fontstore)
    clustered = headlines.cluster.run.clusterme(matrix, ptcns)
    extracted = headlines.cluster.run.extract_headlines(
        clustered,
        document_length=len(ptcns),
    )
    if len(extracted) < 4:
        # disable strategy
        return []
    levelfour = [extracted[3]]
    converted = headlines.cluster.run.convert_cluster(
        levelfour,
        ptcns,
    )
    for item in converted:
        item.level = 4
    result = [converted]
    return result
