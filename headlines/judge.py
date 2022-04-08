# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configo
import elements
import utila

import headlines.visitor


def invalid_extraction(items) -> bool:
    """Judge extracted strategy and decide if result can be valid.

    1. Strategy: Check longest sequence of level one headlines.
    2. Strategy: Check headline ends with awkward characters.
    """
    items = utila.flatten(items, append=True)
    if all(item.level == 1 for item in items):
        # level one extraction strategy
        return False
    # too many level ones in a row
    levels = [item.level for item in items if item.level is not None]
    grouped = utila.groupby_diff(levels, maxdiff=0, sort=False)
    longest_levelone = utila.longest([item for item in grouped if item[0] == 1])
    if len(longest_levelone) > LEVELONE_IN_A_ROW_MAX(len(items)):
        utila.debug('skip invalid extraction: too many first levels: '
                    f'{longest_levelone} in a row. headlines: {len(items)}')
        return True
    # too many invalid characters at title end
    titles = [item.title.lower().strip() for item in items]
    invalid_endings = len([item for item in titles if item[-1] in ',./;:)-'])
    if invalid_endings > INVALID_ENDING_MAX(len(titles)):
        utila.debug(f'skip invalid extraction: {invalid_endings} {len(titles)}')
        return True
    return False


def score_levelerror(items: list) -> int:
    """Determine holes in ascending headline level.

    This is may indicated by user, but mostly by selecting the wrong
    headline determination algorithm.
    """
    flat = utila.flatten(items)
    flat = utila.flatten(flat, append=True)
    error = 0
    rawlevel = [
        item.raw_level
        for item in flat
        if item.raw_level and elements.level_numbered(item.raw_level)
    ]
    rawlevel = utila.notempty(rawlevel)
    grouped = headlines.visitor.groupby_level(rawlevel)
    for groups in grouped:
        for group in groups:
            group = [elements.determine_patch(item) for item in group]
            if group[0] != 1:
                error += 1
            diffs = utila.diffs(group) if len(group) > 1 else []
            diffs = [item for item in diffs if item != 1]
            error += len(diffs)
    return error


LEVELONE_IN_A_ROW_MAX = configo.HolyTable([
    (0, 4),
    (10, 4),
    (20, 4),
    (30, 4),
    (40, 5),
    (50, 6),
],)

INVALID_ENDING_MAX = configo.HolyTable(
    [
        (0, 1),
        (10, 2),
        (50, 7),
        (120, 10),
    ],
    strategy=utila.Strategy.LINEARISE,
    right_outranges_none=False,
)

ERROR_MAX = configo.HolyTable(
    [
        (0, 0),
        (10, 1),
        (20, 2),
        (30, 4),
        (50, 6),
        (70, 7),
        (90, 9),
        (100, 10),
        (120, 12),
    ],
    strategy=utila.Strategy.LOWER,
    left_outranges_none=False,
    right_outranges_none=False,
)
# give some tolerance if first appraoch was not good enough
ERROR_MAX_PLUS = configo.HV_PERCENT_PLUS(default=150)


def too_many_error(headlinex, second: bool = False) -> bool:
    if not headlinex:
        return False
    headline_count = len(utila.flatten(headlinex))
    if headline_count < 10:  # TODO: MAGIC NUMBER
        # TODO: THINK ABOUT THIS
        # disable check for too few headlines
        return False
    error = score_levelerror(headlinex)
    error_max = ERROR_MAX(headline_count)
    if second:
        # increase max error rate
        error_max = int(error_max * ERROR_MAX_PLUS)
    if error <= error_max:
        # valid extraction
        return False
    utila.debug('skip invalid, too many error: '
                f'{error}/{error_max}:{headline_count}:second:{second}')
    return True
