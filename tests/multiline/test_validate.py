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

ARCHIVE = utila.join(headlines.ROOT, 'tests/multiline/expected', exist=True)


@pytest.mark.parametrize('source', tests.conftest.TEST_TODO)
def test_validate_multiline(source, td, mp):
    utilatest.fixture_requires(source)
    tests.Evaluate(
        name='multiline',
        source=source,
        pages=':',
        expected=utila.file_name(source),
        archive=ARCHIVE,
        workdir=td.tmpdir,
        mp=mp,
    ).evaluate()
