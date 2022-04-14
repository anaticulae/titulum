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
import tests
import tests.conftest

ARCHIVE = utila.join(headlines.ROOT, 'tests/levelfour/expected', exist=True)


@utilatest.longrun
@pytest.mark.parametrize('source', tests.conftest.TEST_TODO)
def test_validate_levelfour(source, testdir, monkeypatch):
    utilatest.fixture_requires(source)
    tests.Evaluate(
        name='levelfour',
        source=source,
        pages=':',
        expected=utila.file_name(source),
        archive=ARCHIVE,
        workdir=testdir.tmpdir,
        monkeypatch=monkeypatch,
    ).evaluate()
