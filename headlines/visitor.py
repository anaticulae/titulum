# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Visitor
=======

Visit table of content by numbered level.

>>> headlines = '1. 1.1 1.2 1.3 2. 2.1 2.1.1 2.1.2 2.1.3 2.2 2.3 3.'.split()
>>> groupby_level(headlines)
[[['1.', '2.', '3.']], [['1.1', '1.2', '1.3'], ['2.1', '2.2', '2.3']], [['2.1.1', '2.1.2', '2.1.3']]]

>>> groupby_level(headlines, subgroups=False)
[['1.', '2.', '3.'], ['1.1', '1.2', '1.3'], ['2.1', '2.2', '2.3'], ['2.1.1', '2.1.2', '2.1.3']]
"""

import itertools

import elements


def groupby_level(  # pylint:disable=R1260
    items,
    selector=None,
    determine_level=elements.level_numbered,
    subgroups: bool = True,
):
    if not items:
        return []
    selector = selector if selector else lambda x: x
    result = []
    stack = []
    for item in items:
        item_level = determine_level(selector(item))
        try:
            parent = stack.pop()
        except IndexError:
            result.append([item])
            stack.append(result[-1])
            continue
        stack_level = determine_level(selector(parent[0]))
        if item_level == stack_level:
            # Content is on the same level, therefore they have the same
            # parent together.
            parent.append(item)
            stack.append(parent)
        elif item_level > stack_level:
            # The level of the item to add is higher than the current item
            # in table of content, therefore add the new one as a paranet
            # of current.
            stack.append(parent)
            result.append([item])
            stack.append(result[-1])
        else:
            # the level of the `new_one` is lower than the item in index. that
            # means that the distance of the item to add to the index is
            # samller as the current one.
            # for example: current = 1.4.4.2
            #              item    = 1.5
            # we have to go up in the tree to find a common parent of both
            # and add item.
            while item_level < stack_level:
                try:
                    parent = stack.pop()
                except IndexError:
                    result.append([item])
                    stack.append(result[-1])
                    break
                stack_level = determine_level(selector(parent[0]))
            parent.append(item)
            stack.append(parent)
    if subgroups:
        result = [
            list(value) for _, value in itertools.groupby(
                result,
                key=lambda x: determine_level(x[0]),
            )
        ]
    return result
