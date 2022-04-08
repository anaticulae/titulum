# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools

import power
import pytest
import serializeraw
import utila
import utilatest

import headlines
import tests

ARCHIVE = utila.join(headlines.ROOT, 'tests/multiline/expected', exist=True)


@pytest.mark.parametrize('source', [
    pytest.param(power.BACHELOR028_PDF, id='bachelor028'),
])
def test_multiline_validate(source, testdir, monkeypatch):
    utilatest.fixture_requires(source)
    Evaluate(
        source=source,
        pages=':',
        expected=utila.file_name(source),
        workdir=testdir.tmpdir,
        monkeypatch=monkeypatch,
    ).evaluate()


class Evaluate(utilatest.BaseLiner):

    def __init__(self, source, pages, expected, workdir, monkeypatch):
        super().__init__(
            program=functools.partial(
                tests.run,
                monkeypatch=monkeypatch,
            ),
            step='multiline -VVV',
            pages=pages,
            source=power.link(source),
            workdir=workdir,
            archive=ARCHIVE,
            loader=self.frompath,
            convert_source=False,
            index=expected,
        )
        self.headlines = power.link(source)

    def frompath(self, workdir):  # pylint:disable=R0201
        path = utila.join(workdir, 'headlines__multiline_multiline.yaml')
        loaded = serializeraw.load_headlines(path)
        return loaded

    def raw(self, value) -> str:
        value = utila.flatten(value)
        collected = [item.raw for item in value]
        result = utila.NEWLINE.join(collected)
        return result
