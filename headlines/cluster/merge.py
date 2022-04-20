# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import texmex
import utila


def merge_headline(items: list) -> list:
    """Merge multi-line-headlines into a single line."""
    result = []
    done = set()
    for current, before, after in items:
        # use id to use object and not hashed object, cause it is possible
        # than two items of different pages are complete identically.
        if id(current) in done:
            # use item only onces
            continue
        if different_style(current, after):
            result.append(current)
            done.add(id(current))
            continue
        if current.style.fontid != before.style.fontid:
            continue
        if current.style.underlined != before.style.underlined:
            continue
        if current == before:
            # start of page
            merged = merge_lines(
                current,
                after,
            )
            result.append(merged)
            done.add(id(current))
            done.add(id(after))
        else:
            # all styles are equal, merge three of them
            merged = merge_lines(
                before,
                current,
                after,
            )
            result.append(merged)
            done.add(id(before))
            done.add(id(current))
            done.add(id(after))
    return result


def merge_lines(*args) -> texmex.TextInfo:
    bounds = []
    text = []
    for line in args:
        bounds.append(line.bounding)
        text.append(line.text.strip())
    bounding_max = utila.rectangle_max(bounds)
    text: str = ' '.join(text)
    if len(args) == 2:
        # start of page
        current = args[0]
    else:
        # three equal style
        current = args[1]
    result = texmex.TextInfo(
        text=text,
        style=current.style,
        bounding=bounding_max,
        bounding_mean=current.bounding_mean,
    )
    return result


def different_style(current, after) -> bool:
    if current.style.underlined != after.style.underlined:
        return True
    if current.style.fontid != after.style.fontid:
        return True
    if current == after:
        # page end
        return True
    return False
