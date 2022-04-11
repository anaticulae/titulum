# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pytest
import utila
import utilatest

import headlines
import tests.conftest

ARCHIVE = utila.join(headlines.ROOT, 'tests/result/expected', exist=True)

TODO = [
    pytest.param(source, id=utila.file_name(source))
    for source in tests.conftest.RESOURCES
]


@pytest.mark.parametrize('source', TODO)
@utilatest.longrun
def test_result_validate(source, testdir, monkeypatch):
    utilatest.fixture_requires(source)
    tests.Evaluate(
        name='result --all',
        source=source,
        pages=':',
        expected=utila.file_name(source),
        archive=ARCHIVE,
        workdir=testdir.tmpdir,
        monkeypatch=monkeypatch,
    ).evaluate()
