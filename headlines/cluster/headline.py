# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools

import configo
import elements
import iamraw
import utila

import headlines.cluster.clusters

HEADLINE_CLUSTER_SIZE_MIN = configo.HV_INT_PLUS(default=3)

HEADLINE_LENGTH_MIN = configo.HV_INT_PLUS(default=7)

DOT_COUNT_MAX = configo.HV_INT_PLUS(default=5)


def extract(
    flats: iamraw.TextProperties,
    *,
    min_headline_count: int = None,
    min_headline_length: int = None,
    greater_than_text: bool = True,
    headline_start: bool = True,
    returncluster: bool = False,
    distance_before_min: float = 1.2,
    distance_after_min: float = 0.98,
):
    if min_headline_count is None:
        min_headline_count = HEADLINE_CLUSTER_SIZE_MIN
    if min_headline_length is None:
        min_headline_length = HEADLINE_LENGTH_MIN
    detected = distances(flats, greater_than_text=greater_than_text)
    if not detected:
        return []
    flats, (distance_before_textsize, distance_after_textsize) = detected
    # remove too short text chuncks which are not possible headlines
    flats = [item for item in flats if item.length >= min_headline_length]
    selection = (
        headlines.cluster.clusters.ClusterProperty.FONT,
        headlines.cluster.clusters.ClusterProperty.LEFT,
    ) if headline_start else (headlines.cluster.clusters.ClusterProperty.FONT,)
    validator = functools.partial(
        valid_headline,
        before_min=distance_before_textsize * distance_before_min,
        after_min=distance_after_textsize * distance_after_min,
    )
    clustered = headlines.cluster.clusters.run(
        flats,
        selection=selection,
        validator=validator,
        minsize=min_headline_count,
        unique_content=True,  # remove duplicated footer/header content
    )
    result = create_result(
        clustered,
        returncluster=returncluster,
    )
    return result


def create_result(clustered, returncluster: bool = False):
    clustered = validate_headline_cluster(clustered)
    largest_font_size = sorted(
        clustered,
        key=lambda x: x.content[0].size,
        reverse=True,
    )
    result = []
    result_cluster = []
    for index in range(5):
        # analyse maximal five headline levels
        matched = headlines.cluster.clusters.bestmatch(
            largest_font_size,
            number=index,
        )  # pylint:disable=C0103
        if not matched:
            continue
        result.append(matched)
        result_cluster.append(largest_font_size[index].content)
    if returncluster:
        return result, result_cluster
    return result


def distances(flats, greater_than_text):
    textcluster = headlines.cluster.utils.text(flats, returncluster=True)
    if not textcluster:
        # too few data
        return []
    flats = headlines.cluster.clusters.remove(flats, textcluster[1])
    textsize = textcluster[0][0]
    distance_before_textsize, distance_after_textsize = textcluster[0][3]
    if distance_before_textsize is None:
        utila.error('distance before `textsize` is None; '
                    'disable headline detection feature')
    if distance_after_textsize is None:
        utila.error('distance after  `textsize` is None;'
                    ' disable headline detection feature')
    if distance_before_textsize is None or distance_after_textsize is None:
        # disable strategy
        return None
    if greater_than_text:
        flats = [item for item in flats if item.size >= textsize]
    return flats, (distance_before_textsize, distance_after_textsize)


def valid_headline(item, before_min, after_min) -> bool:  # pylint:disable=R0911
    text = item.hashed
    if elements.noheadline(text):
        return False
    if elements.isheadline(text):
        return True
    if item.before is None:
        if elements.noheadline_pattern(text):
            # Kapitel 1 at the start of the page followed by title
            return False
        return True
    if item.after is None:
        return False
    if item.before <= before_min:
        return False
    # TODO: INTRODUCE NEW STRATEGY FOR HEADLINES WITHOUT HUGE DISTANCE
    if item.after < after_min:
        return False
    return True


HEADLINE_SPREAD_MIN = configo.HV_PERCENT_PLUS(default=50)


def validate_headline_cluster(clusters):
    """Check that detected headline style is spread over the document
    and not located on few pages. Lower spreads indicates that more than
    one line on a page is detected as headline, which indicates false
    detection."""

    def valid(cluster) -> bool:
        """\
        Returns:
            1 5 8 10    valid/True     : 1.0   5/5
            1 1 1 2 2   invalid/False  : 0.4   2/5
        """
        pages = utila.make_unique([item.page for item in cluster])
        ratio = len(pages) / len(cluster)
        return ratio >= HEADLINE_SPREAD_MIN

    result = [cluster for cluster in clusters if valid(cluster)]
    return result
