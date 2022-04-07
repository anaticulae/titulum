# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configo
import iamraw
import utila


def cluster_headline_level(items: iamraw.PagesHeadlineList) -> dict:
    headlines = []
    for chapter in items.values():
        if not chapter:
            continue
        level = [
            item.level
            for item in chapter
            if (item.level is not None and item.level['after'] is not None)
        ]
        headlines.extend(level)
    if not headlines:
        return could_not_cluster(items)
    clustered = equal_headline_cluster(headlines)
    if not clustered:
        # to less data to cluster
        return could_not_cluster(items)
    groups = list(item.center for item in clustered)
    groups = sorted(groups, key=lambda x: x['after'], reverse=True)
    groups = sorted(groups, key=lambda x: x['textsize'], reverse=True)
    border = [(
        item['textsize'],
        item['after'],
        item['feed'],
    ) for item in groups]

    left_or_right = 100.0  # decide if text is right or left feeded
    tolerance = [
        utila.roundme((
            first * 0.15,
            second * 3.0,
            left_or_right,
        )) for first, second, _ in border
    ]
    items = update_level(items, border, tolerance)
    return items


def could_not_cluster(items: iamraw.PagesHeadlineList):
    """Set level to `None` to indicate that clustering is not possible."""
    for chapter in items.values():
        for item in chapter:
            item.level = None
    return items


def update_level(items: iamraw.PagesHeadlineList, border, diff) -> dict:
    for chapter in items.values():
        if not chapter:
            continue
        for headline in chapter:
            textsize = headline.level['textsize']
            after = headline.level['after']
            feed = headline.level['feed']
            current = (textsize, after, feed)
            matched = utila.near_dims(  # pylint:disable=E1101,unexpected-keyword-arg
                current,
                border,
                diff,
                allow_none=True,
            )
            if matched is None:
                headline.level = None
            else:
                matched = matched[0] if isinstance(matched, list) else matched
                headline.level = matched + 1  # matched is zero based
                assert isinstance(matched, int), str(matched)
    return items


TEXTSIZE_DIFF_MAX = configo.HV_FLOAT_PLUS(default=1.5)

AFTER_DIFF_MAX = configo.HV_FLOAT_PLUS(default=0.15)


def equal_headline_cluster(
    todo,
    min_elements: int = 2,
):

    def classificator(candidat, clusteritem):

        def matcher(candidat, clusteritem) -> bool:
            if not equal_fontsize(candidat, clusteritem):
                return False
            if equal_after(candidat, clusteritem):
                return True
            # if equal_feed(candidat, clusteritem):
            #     return True
            return False

        return matcher(candidat, clusteritem)

    return utila.determine_cluster(
        todo,
        classificator,
        min_elements=min_elements,
    )


LEFT_FEED_MAX = configo.HV_FLOAT_PLUS(default=15.0)

RIGHT_FEED_MIN = configo.HV_FLOAT_PLUS(default=200.0)


def equal_feed(candidat, clusteritem) -> bool:
    feed_left_candiat = candidat['feed'] < LEFT_FEED_MAX
    feed_right_candiat = candidat['feed'] >= RIGHT_FEED_MIN

    feed_left_cluster = clusteritem['feed'] < LEFT_FEED_MAX
    feed_right_cluster = clusteritem['feed'] >= RIGHT_FEED_MIN

    if feed_left_candiat != feed_left_cluster:
        return False
    if feed_right_candiat != feed_right_cluster:
        return False
    return True


def equal_fontsize(candidat, clusteritem) -> bool:
    return utila.near(
        current=candidat['textsize'],
        expected=clusteritem['textsize'],
        diff=TEXTSIZE_DIFF_MAX,
    )


def equal_after(candidat, clusteritem) -> bool:
    if clusteritem['after'] is None:
        # None cluster
        return candidat['after'] is None
    if candidat['after'] is None:
        return True
    # 15 percent diff
    if not utila.near(
            current=candidat['after'],
            expected=clusteritem['after'],
            diff=max(clusteritem['after'] * AFTER_DIFF_MAX, 4.0),
    ):
        return False
    return True
