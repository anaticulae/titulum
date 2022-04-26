# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections
import itertools
import warnings

import configo
import elements
import iamraw
import numpy
import scipy.cluster.vq
import texmex
import utila

import headlines.cluster.merge
import headlines.cluster.parser
import headlines.cluster.validate
import headlines.config
import headlines.utils

NUMPY_SEED = 1 * 2 * 4 * 8 * 16 * 32 * 64

HEADLINE_WORDCOUT_MAX = configo.HV_INT_PLUS(default=20)


def run(
    ptcns: texmex.PTCNs,
    fontstore: iamraw.FontStore,
) -> iamraw.PagesHeadlineList:
    matrix, ptcns = create_matrix(ptcns, fontstore)
    clustered = clusterme(matrix, ptcns)
    extracted = extract_headlines(
        clustered,
        document_length=len(ptcns),
    )
    converted = convert_cluster(extracted, ptcns)
    result = headlines.utils.groupby_level_one(converted)
    return result


def extract_headlines(
    clusters,
    cluster_size_min: int = 5,
    document_length: int = 30,
    **kwargs,
):
    # find headline cluster
    flat = headlines.cluster.validate.valid_headline_clusters(
        clusters=clusters,
        cluster_size_min=cluster_size_min,
        **kwargs,
    )
    # merge multiple headline
    flat = headlines.cluster.merge.merge_headline(flat)
    # skip hidden items
    flat = [item for item in flat if item.visible]
    headline_count_min = headlines.config.HEADLINE_COUNT_MIN(document_length)
    if len(flat) < headline_count_min:
        utila.debug(f'cluster: too few headlines {len(flat)}, require at '
                    f'least {headline_count_min}, disable strategy')
        return []
    # group headlines
    grouped = groupby_level(flat)
    # verify group
    result = verify_level(grouped)
    return result


def convert_cluster(clusters: list, ptcns: texmex.PTCNs) -> list:  # pylint:disable=R0914
    result = []
    for index, cluster in enumerate(clusters):
        for item in cluster:
            text = item.text
            title, level, rawlevel = text, index + 1, ''
            parsed = elements.parse_headline(text)
            if parsed:
                title, level, rawlevel = parsed
            headline = iamraw.Headline(
                title=title,
                level=level,
                raw=text,
                raw_level=rawlevel,
                # page=page.page,
                # container=containerid,
            )
            result.append(headline)
    result = optimize_page_container(
        result,
        ptcns,
    )
    return result


def optimize_page_container(items: list, ptcns: texmex.PTCNs) -> list:
    for headline in items:
        headline.container = -1
        start, end = headline.raw[0:25], headline.raw[-25:]
        for page in reversed(ptcns):
            content = page.debug
            content = content.replace('\n', ' ')
            starts = utila.findindex(content, token=start)
            if not starts:
                continue
            ends = utila.findindex(content, token=end)
            if not ends:
                continue
            container = []
            for index, line in enumerate(page):
                if startswith(line.text, headline.raw):
                    # detect headline only once to determine correct page
                    # and container.
                    line.text = ''
                    container.append(index)
                    continue
                if container and line.text.endswith(end[-10:]):
                    # detect headline only once to determine correct page
                    # and container.
                    # line.text = ''
                    # end requires that start is detected
                    container.append(index)
                    break
            if not container:
                utila.debug(f'could not locate on p{page.page}: {headline.raw}')
                continue
            headline.page = page.page
            if len(container) == 1:
                headline.container = container[0]
            else:
                headline.container = container[0], select_end(container)  # pylint:disable=R0204
            break
    items.sort(key=lambda x: 0 if not x.container else x.container[0]
               if isinstance(x.container, tuple) else x.container)
    items.sort(key=lambda x: x.page)
    return items


def startswith(linestart: str, headline: str) -> bool:
    if linestart.startswith(headline[0:25]):
        if len(headline) < len(linestart):
            return False
        return True
    return False


def select_end(items) -> int:
    """\
    >>> select_end((2, 3, 4, 6))
    4
    >>> select_end((2, 5, 6))
    5
    """
    # TODO: MAY IMPROVE LATER
    assert len(items) >= 2
    start = items[0]
    end = items[1]
    diff = end - start
    if diff > 1:
        return end
    for item in items[2:]:
        diff = item - end
        if diff > 1:
            break
        end = item
    return end


def clusterme(matrix, navis, numbers: int = 20, runtime: int = 12000):
    # running kmeans with invalid `k`/`numbers` leads to non determining loop.
    assert isinstance(numbers, int), type(numbers)
    if len(matrix) == 0:  # pylint:disable=compare-to-zero
        utila.error('empty matrix data, skip cluster strategy')
        return []
    merged = scipy.cluster.vq.whiten(matrix)
    if len(merged) < numbers:
        utila.error(f'too few data: {len(merged)} to run vector strategy')
        return []
    # TODO: REMOVE AFTER HAVING A MORE STABLE ALGO
    numpy.random.seed(NUMPY_SEED)
    _, label = scipy.cluster.vq.kmeans2(
        merged,
        k=numbers,
        iter=runtime,
        minit='points',
    )
    data = numpy.array(merge_neighbors(navis))
    assert len(data) == len(label), f'{len(data)} == {len(label)}'
    grouped = [data[label == item] for item in range(numbers)]
    # remove empty cluster
    notempty = [item for item in grouped if len(item)]
    return notempty


def create_matrix(ptcns, fontstore):
    parsed = headlines.cluster.parser.parses(
        navigators=ptcns,
        fontstore=fontstore,
    )
    merged = connect_pages(parsed)
    # TODO: UUSE NUMPY
    merged = list(itertools.zip_longest(*merged))
    # round it
    merged: numpy.array = numpy.array(merged, dtype=numpy.uint32)
    matrix = numpy.array(merged, dtype=numpy.double)
    return matrix, ptcns


def merge_neighbors(navis):
    result = []
    for page in navis:
        if not page:
            continue
        befores = [page[0]] + page[:-1]
        afters = page[1:] + [page[-1]]
        content = list(zip(page, befores, afters))
        result.extend(content)
    return result


def connect_pages(pages) -> list:
    """\
    >>> connect_pages([
    ...     [[1, 2, 3], [10, 11, 12]],
    ...     [[4, 5, 6], [13, 14, 15]],
    ... ])
    [[1, 2, 3, 4, 5, 6], [10, 11, 12, 13, 14, 15]]
    """
    # TODO: MOVE TO UTILA
    if not pages:
        return []
    result = pages[0][:]
    for items in pages[1:]:
        for insert, current in zip(result, items):
            insert.extend(current)
    return result


def groupby_level(items) -> list:
    # TODO: ADD HEADLINE SIZE GROUPING STRATEGY
    grouped = collections.defaultdict(list)
    for item in items:
        text = item.text
        level = elements.level_numbered(text)
        if level is False:  # pylint:disable=C2001
            level = 4
        if level is None:
            level = 4
        grouped[level - 1].append(item)
    result = [grouped[number] for number in range(len(grouped))]
    return result


def verify_level(grouped: list) -> list:
    result = []
    for group in grouped:
        without_chapterpattern = not any(
            elements.noheadline_pattern(item.text) for item in group)
        if without_chapterpattern:
            # no chapter pattern inside group, add whole group
            result.append(group)
            continue
        # remove no-chapter-pattern
        valid = [
            item for item in group if elements.noheadline_pattern(item.text)
        ]
        result.append(valid)
        # TODO: MOVE INVALID TO GROUP LEVEL 4?
    return result


def disable_warnings():
    # TODO: DO NOT DISABLE ALL WARNINGS
    nowarning = lambda message, category=None, stacklevel=1, source=None: ''  # pylint:disable=W0613
    warnings.warn = nowarning


disable_warnings()
