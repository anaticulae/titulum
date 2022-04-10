# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw


def groupby_level_one(heads: list) -> iamraw.PagesHeadlineList:
    result = []
    # detect chapter starts
    levelone = [
        index for (index, item) in enumerate(heads) if item.level in (None, 1)
    ]
    # group headlines into chapters
    result = [
        heads[index:after]
        for (index, after) in zip(levelone[:-1], levelone[1:])
    ]
    if levelone:
        # do not forget the last group
        result.append(heads[levelone[-1]:])
    return result
