# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools

import iamraw
import serializeraw
import utila

INVALID = (
    iamraw.sections.Introduction,
    iamraw.sections.Unknown,
    iamraw.MultipleSection,
)


@functools.lru_cache
def headlinepart(pages: tuple, sections: str = None) -> tuple:
    if not utila.exists(sections):
        return pages
    loaded = serializeraw.load_sections(
        sections,
        pages=pages,
    )
    # TODO: A LITTLE BIT COMPLICATED
    loaded = [item for item in loaded if not isinstance(item, INVALID)]
    valid = [utila.rlist(item.start, item.end) for item in loaded]
    valid = utila.flat(valid)
    result = tuple(item for item in valid if not utila.should_skip(item, pages))
    return result
