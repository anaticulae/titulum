# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import statistics

import elements
import texmex
import utila


def valid_headline_clusters(
    clusters,
    cluster_size_min: int = 5,
    cluster_rate_min: float = 0.3,
    cluster_headline_median_length_min: int = 10,
    x0_max_diff: float = 100.0,
    whitespace_rate_max: float = 0.2,
):
    collected = []
    for cluster in clusters:
        cluster = clean_cluster(
            cluster,
            x0_max_diff=x0_max_diff,
        )
        if invalid_cluster(
                cluster,
                x0_max_diff=x0_max_diff,
                cluster_rate_min=cluster_rate_min,
                cluster_size_min=cluster_size_min,
                headline_median_length_min=cluster_headline_median_length_min,
                whitespace_rate_max=whitespace_rate_max,
        ):
            continue
        collected.append(cluster)
    flat = utila.flatten(collected)
    return flat


def invalid_cluster(  # pylint:disable=R0911
    cluster,
    cluster_size_min: int = 5,
    cluster_rate_min: float = 0.3,
    headline_median_length_min: int = 10,
    x0_max_diff: float = 100.0,
    whitespace_rate_max: float = 0.2,
) -> bool:
    cluster = clean_cluster(
        cluster,
        x0_max_diff=x0_max_diff,
    )
    if len(cluster) <= cluster_size_min:
        return True
    rate, median = headline_rate(cluster)
    if rate < cluster_rate_min:
        return True
    if median < headline_median_length_min:
        return True
    if noheadline_cluster(cluster):
        return True
    if whitespace_rate(cluster) > whitespace_rate_max:
        return True
    if is_hidden(cluster):
        return True
    return False


def clean_cluster(
    cluster,
    x0_max_diff: float = 15.0,
) -> list:

    def left_right_aligned(bounding: tuple) -> bool:
        # skip too right or too left items
        if 35.0 <= bounding[0] < (75.0 + x0_max_diff):
            return True
        # 595.28
        if (595.28 - 75.0 - x0_max_diff) <= bounding[2] < 595.28 - 35.0:
            return True
        return False

    valid = [item for item in cluster if left_right_aligned(item[0].bounding)]
    # skip `Kapitel 1`-pattern
    valid = [
        item for item in valid if not elements.noheadline(item[0].text) or
        not elements.noheadline_pattern(item[0].text)
    ]
    return valid


def headline_rate(cluster):
    # TODO: MOVE TO ELEMENTS?
    median = statistics.median([len(item[0].text) for item in cluster])
    headlines = [
        item for item in cluster if elements.isheadline(
            item[0].text,
            strict=False,
        )
    ]
    return len(headlines) / len(cluster), median


def whitespace_rate(cluster) -> float:
    charcount = 0
    whitespaces = 0
    for item in cluster:
        charcount += len(item[0].text)
        whitespaces += item[0].text.count(' ')
    if not charcount:
        return 0.0
    return whitespaces / charcount


def is_hidden(cluster) -> bool:
    hidden, other = utila.partition(
        items=cluster,
        key=lambda x: x[0].state == texmex.TextState.HIDDEN,
    )
    hidden_rate = utila.rate_rel(  # pylint:disable=W0612
        len(hidden),
        len(other),
    )
    return False


def noheadline_cluster(cluster, pagerate_max: float = 0.5):
    """\
     2. Klassifikation 5
     3. Steuerung 13
     4. Anwendung 17
    """
    if len(cluster) < 4:
        return False
    with_pageending = [
        item for item in cluster if utila.isnumber(item[0].text.split(' ')[-1])
    ]
    pagerate = len(with_pageending) / len(cluster)
    if pagerate > pagerate_max:
        return True
    return False
