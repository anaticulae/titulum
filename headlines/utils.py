# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import utila


def prepare_chapter_and_content(sectionx, chapter):
    utila.asserts(sectionx, iamraw.Sections)
    assert sectionx, f'no sections provided: {sectionx}'
    if chapter is None:
        # process all chapter
        # TODO: clearify code
        content = determine_contentrange(sectionx)
        chapter = list(range(len(content)))
    else:
        content = determine_chapters(sectionx)
        chapter = [chapter] if isinstance(chapter, int) else chapter
    return chapter, content


def determine_chapters(root: iamraw.Sections):
    content = [item for item in root if isinstance(item, iamraw.MainPart)]
    if not content:
        # no content in document
        return []
    result = []
    for area in content:
        for chapter in area:
            result.append((chapter.start, chapter.end))
    return result


def determine_contentrange(items) -> 'ChapterRanges':
    """Iterate thrue `sections` and search for `Chapter` to determine
    section start and end.

    In some cases no `Chapter` is present. This can happen if you
    analyse only a few pages or a single one. In this case the start and
    end is defined by normal items.

    Returns:
        list of `ChapterRange` (start, end)
    """
    # analyze all chapter of the document
    # TODO: DO WE NEED PAPERSECTION HERE? ARE THERE SOME CHAPTER?
    contents = [
        item for item in items if isinstance(
            item,
            (
                iamraw.MainPart,
                iamraw.MultipleSection,
                iamraw.Appendix,
                iamraw.Unknown,
            ),
        )
    ]
    chapters = flat_chapters(contents)
    if not chapters and contents:
        # no chapter is present - create `virtual chapter`
        chapters = list(list(content.content) for content in contents)
        chapters = utila.flatten(chapters)
    if not chapters:
        # TODO: INVESTIGATE HERE
        return []
    result = items_before_firstchapter(chapters, contents)
    for current, after in zip(chapters[:-1], chapters[1:]):
        floatrange = isinstance(current.end, float) or isinstance(after.start, float) # yapf:disable
        if current.end == after.start and floatrange:
            # multi page: content on same page
            result.append((current.start, current.end))
        else:
            result.append((current.start, after.start - 1))
    result.append((chapters[-1].start, contents[-1].end))
    # ensure ascending page numbers
    assert all(start <= end for start, end in result), str(result)
    return result


def flat_chapters(contents):
    result = []
    for item in contents:
        if isinstance(item, iamraw.MainPart):
            result.extend(item.content)
        elif isinstance(item, iamraw.Appendix):
            result.append(item)
    result = utila.select_type(
        result,
        (iamraw.Chapter, iamraw.Appendix),
    )
    return result


def items_before_firstchapter(chapters, contents):
    """Determine items before the first **loaded** chapter starts.

    This is required, when loading a part in the middle of a document.
    To extract headlines, it is required to have `Chapter` separators to
    determine the range of the different chapter. Parts of chapter are
    not loaded if start of chapter is not selected.
    """
    assert chapters
    # check if content exists before the first chapter starts
    firstchapter_start = chapters[0].start
    before = [[
        item for item in content.content if item.start < firstchapter_start
    ] for content in contents]
    # remove empty pages
    before = [item for item in before if item]
    before = utila.flatten(before)
    if not before:
        return []
    return [(before[0].start, before[-1].end)]


def groupby_headlinelevel(chapters):
    extracted = list(chapters.values())
    flatten = utila.flatten(extracted)
    grouped = []
    if flatten:
        if isinstance(flatten[0].level, dict):
            # HACK NOLEVEL?
            flatten[0].level = None
        grouped.append([flatten[0]])
    for item in flatten[1:]:
        if isinstance(item.level, dict):
            # HACK NOLEVEL?
            item.level = None
        if item.level is None or item.level == 1:
            grouped.append([item])
        else:
            grouped[-1].append(item)
    return grouped
