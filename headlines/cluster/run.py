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

import headlines.cluster.parser
import headlines.cluster.validate
import headlines.utils

NUMPY_SEED = 1 * 2 * 4 * 8 * 16 * 32 * 64


def run(
    ptcns: texmex.PTCNs,
    fontstore: iamraw.FontStore,
) -> iamraw.PagesHeadlineList:
    matrix, ptcns, _ = create_matrix(ptcns, fontstore)
    clustered = clusterme(matrix, ptcns)
    extracted = extract_headlines(clustered)
    converted = convert_cluster(extracted, ptcns)
    result = headlines.utils.groupby_level_one(converted)
    return result


def extract_headlines(clusters, cluster_size_min: int = 5, **kwargs):
    # find headline cluster
    flat, _ = headlines.cluster.validate.valid_headline_clusters(
        clusters=clusters,
        cluster_size_min=cluster_size_min,
        **kwargs,
    )
    # merge multiple headline
    flat = merge_headline(flat)
    # sort headlines
    flat = sorted(flat, key=lambda x: utila.alphabetically(x.text))
    # group headlines
    grouped = groupby_level(flat)
    # verify group
    result = verify_level(grouped)
    return result


def convert_cluster(clusters: list, ptcns) -> list:
    clusters = [{item.text.strip() for item in level} for level in clusters]
    result = []
    for page in ptcns:
        for containerid, line in enumerate(page):
            line_text = line.text.strip()
            current = headline_level(line_text, clusters)
            if current is None:
                continue
            parsed = elements.parse_headline(line_text)
            if parsed:
                title, level, rawlevel = parsed
            else:
                title, level, rawlevel = line_text, current + 1, ''
            headline = iamraw.Headline(
                title=title,
                level=level,
                page=page.page,
                raw=line_text,
                raw_level=rawlevel,
                container=containerid,
            )
            result.append(headline)
    return result


HEADLINE_WORDCOUT_MAX = configo.HV_INT_PLUS(default=20)


def headline_level(line, clusters) -> int:
    current = search_level(line, clusters)
    if current == -1:
        return None
    # TODO: MOVE TO doctextstyle.features
    if elements.noheadline(
            line,
            wordcount_max=HEADLINE_WORDCOUT_MAX,
    ):
        return None
    return current


def search_level(line, clusters):
    # TODO: ADD MECHANISM TO CHECK IF ITEM IS NEAR TO CLUSTER TO FIND
    # MORE HEADLINES
    for index, cluster in enumerate(clusters):
        if line in cluster:
            return index
    return -1


def clusterme(matrix, navis, numbers: int = 20, runtime: int = 12000):
    # running kmeans with invalid `k`/`numbers` leads to non determining loop.
    assert isinstance(numbers, int), type(numbers)
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
    return matrix, ptcns, fontstore


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


def merge_headline(items):
    """Merge multi-line-headlines into a single line."""
    result = []
    done = set()
    for current, before, after in items:
        # use id to use object and not hashed object, cause it is possible
        # than two items of different pages are complete identically.
        if id(current) in done:
            # use item only onces
            continue
        if current.style.fontid != after.style.fontid:
            result.append(current)
            done.add(id(current))
            continue
        if current.style.fontid == before.style.fontid:
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


def verify_level(grouped: list) -> list:
    result = []
    for group in grouped:
        if not any(elements.noheadline_pattern(item.text) for item in group):
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
