# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw

import headlines.cluster.clusters


def text(flats, returncluster: bool = False):
    clustered = headlines.cluster.clusters.run(
        flats,
        (
            headlines.cluster.clusters.ClusterProperty.SIZE,
            headlines.cluster.clusters.ClusterProperty.FONT,
        ),
    )
    result = headlines.cluster.clusters.bestmatch(clustered)
    if not result:
        # too few data to determine text style information
        return None
    if returncluster:
        return result, clustered[0] if clustered else []
    return result


def flatten(pages: iamraw.PageTextPropertiesList) -> iamraw.TextProperties:
    result = []
    for page in pages:
        for length, hashed, size, font, distance, ypos, left, right in zip(
                page.length,
                page.hashed,
                page.sizes,
                page.fonts,
                page.distances,
                page.ypos,
                page.left,
                page.right,
        ):
            result.append(
                iamraw.TextProperty(
                    length=length,
                    hashed=hashed,
                    size=size,
                    font=font,
                    before=distance.top,
                    after=distance.bottom,
                    top=ypos[0],
                    bottom=ypos[1],
                    left=left,
                    right=right,
                    page=page.page,
                ))
    return result
