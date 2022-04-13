# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila


def has_levelfour(headlines):
    """\
    >>> import iamraw
    >>> assert has_levelfour(iamraw.HeadlineResult()) is not None
    """
    flat = utila.flatten(headlines)
    maxlevel = max(
        [item.level for item in flat if item.level is not None],
        default=0,
    )
    if maxlevel >= 4:
        return True
    # TODO: USE SMARTER DECIDER, MAY COLLECT HEADLINE DUPLICATON
    # THIS STEP IS REQUIRED WHEN STRATEGY ALREADY PARSE LEVEL FOUR
    # HEADLINES.
    counted = 0
    for headline in flat:
        # Headline(title='A) Einführungsphase', level=3, raw='A)
        # Einführungsphase', raw_level='', page=52, container=21,
        # decoration=None)
        if headline.level == 3 and not headline.raw_level:
            counted += 1
    if counted >= 3:
        return True
    return False


def merge_levelfour(extracted, levelfour):
    utila.debug('merge_levelfour')
    # avoid side effects
    result = [item[:] for item in extracted]
    levelfour = levelfour[:]

    def insert(current, result):
        for chapter in result:
            for index, item in enumerate(chapter):
                if current.page > item.page:
                    continue
                start = item.container
                if isinstance(start, tuple):
                    start = start[0]
                if current.page == item.page and current.container > start:
                    continue
                chapter.insert(index, current)
                return

    while levelfour:
        current = levelfour.pop()
        insert(current, result)
    return result
