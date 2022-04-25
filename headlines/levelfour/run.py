# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import statistics

import elements
import iamraw
import texmex
import utila

import headlines.cluster.run


def run(
    ptcns: texmex.PTCNs,
    fontstore: iamraw.FontStore,
) -> iamraw.PagesHeadlineList:
    matrix, ptcns = headlines.cluster.run.create_matrix(ptcns, fontstore)
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
    filtered = nolevelfour(converted)
    if levelfour_invalid(filtered):
        filtered = []
    if len(filtered) < 5:  # TODO: HOLY VALUE
        filtered = []
    for item in filtered:
        item.level = 4
    result = [filtered]
    return result


def nolevelfour(headlinex: iamraw.Headlines) -> iamraw.Headlines:
    """Elements which are part of headline list, can not be part of level 4."""
    filtered = [
        item for item in headlinex
        if not elements.isheadline(item.title, strict=True)
    ]
    filtered = [
        item for item in filtered if not elements.noheadline(item.title)
    ]
    return filtered


def levelfour_invalid(headlinex) -> bool:
    median = statistics.median([len(item.title) for item in headlinex])
    if median > 40:
        utila.debug(f'invalid levelfour, median: {median} too high')
        return True
    return False
