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
        if current.style.fontid == before.style.fontid and current.style.underlined == after.style.underlined:
            if current == before:
                # start of page
                bounding = utila.rectangle_max((
                    current.bounding,
                    after.bounding,
                ))
                new = texmex.style.TextInfo(
                    text=f'{current.text.strip()} {after.text.strip()}',
                    style=current.style,
                    bounding=bounding,
                    bounding_mean=current.bounding_mean,
                )
                result.append(new)
                done.add(id(current))
                done.add(id(after))
            else:
                # all styles are equal, merge three of them
                bounding = utila.rectangle_max((
                    before.bounding,
                    current.bounding,
                    after.bounding,
                ))
                text = f'{before.text.strip()} {current.text.strip()} {after.text.strip()}'
                new = texmex.style.TextInfo(
                    text=text,
                    style=current.style,
                    bounding=bounding,
                    bounding_mean=current.bounding_mean,
                )
                result.append(new)
                done.add(id(current))
                done.add(id(before))
                done.add(id(after))
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
