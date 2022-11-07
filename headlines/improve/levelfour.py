# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections

import utila

import headlines.judge
import headlines.utils


def merge_ifbetter(before, levelfour):
    if not levelfour:
        return before
    levelfour = levelfour[0]
    improved = improve(
        current=before,
        levelfour=levelfour,
    )
    # check if produced result is better
    result = headlines.judge.select_best((before, improved))
    # TODO: CHECK IF IT IS BETTER THAN BEFORE
    return result


def improve(current: list, levelfour):
    """Do not add headlines which are also part of level four."""
    # TODO: DIRTY BUT WORKS
    flat = utila.flat(current)
    done = collections.defaultdict(set)
    for item in levelfour:
        done[item.page].add(item.container)
    selected = []
    for item in flat:
        if item.container in done[item.page]:
            utila.debug(f'headline is levelfour: {item}, skip')
            continue
        selected.append(item)
    selected.extend(levelfour)
    selected.sort(key=lambda x: container(x.container))
    selected.sort(key=lambda x: x.page)
    result = headlines.utils.groupby_level_one(selected)
    return result


def container(item):
    if isinstance(item, tuple):
        return item[0]
    return item


def has_levelfour(items):
    """\
    >>> import iamraw
    >>> assert has_levelfour(iamraw.HeadlineResult()) is not None
    """
    flat = utila.flat(items)
    maxlevel = max(
        (item.level for item in flat if item.level is not None),
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
