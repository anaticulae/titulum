# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections

import elements
import iamraw


def filter_headlines(items: iamraw.PagesHeadlineList):
    if isinstance(items, list):
        items = dict(enumerate(items))
    result = collections.defaultdict(list)
    for chapter, content in items.items():
        chapter_headlines = []
        for headline in content:
            if elements.noheadline(headline.title):
                # Skip toc line entries for example
                continue
            if parsed := elements.parse_leveled_headline(headline.title):
                raw_level = parsed['level']
                headline.level = elements.level_numbered(raw_level)
                headline.raw_level = raw_level
                headline.title = headline.title.replace(raw_level, '').strip()
                chapter_headlines.append(headline)
                continue
            if headline.decoration is not None:
                # Kapitel 1\nEinleitung
                headline.level = 1  # pylint:disable=R0204
                chapter_headlines.append(headline)
                continue
            if elements.isheadline(headline.title):
                chapter_headlines.append(headline)
                continue
        result[chapter].extend(chapter_headlines)
    # require KeyError
    result = dict(result)  # pylint:disable=R0204
    result = remove_duplicated_firstlevel(result)
    return result


DUPLICATION_ALLOWED = 1


def remove_duplicated_firstlevel(
    chapters: dict,
    duplication_allowed=DUPLICATION_ALLOWED,
) -> dict:
    duplication_max = 1 + duplication_allowed
    firstlevels = []
    for headlines in chapters.values():
        for headline in headlines:
            if not isfirstlevel(headline):
                continue
            firstlevels.append(headline.title)
    # determine duplicated headlines
    duplicated = {
        item for item in firstlevels
        if firstlevels.count(item) > duplication_max
    }
    if not duplicated:
        # removing is not required
        return chapters
    for number, chapter in chapters.items():
        # remove duplicated first level headlines
        chapters[number] = [
            item for item in chapter
            if not (isfirstlevel(item) and item.title in duplicated)
        ]
    return chapters


def isfirstlevel(headline) -> bool:
    level = headline.level
    if level is None:
        return True
    if level == 1:
        return True
    if isinstance(level, dict):
        return True
    return False
