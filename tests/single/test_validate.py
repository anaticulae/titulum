# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pytest
import utilo
import utilotest

import tests
import tests.conftest
import titulum

ARCHIVE = utilo.join(titulum.ROOT, 'tests/single/expected', exist=True)


@pytest.mark.parametrize('source', tests.conftest.TEST_TODO)
def test_validate_single(source, td, mp):
    utilotest.fixture_requires(source)
    tests.Evaluate(
        name='single',
        source=source,
        pages=':',
        expected=utilo.file_name(source),
        archive=ARCHIVE,
        workdir=td.tmpdir,
        mp=mp,
    ).evaluate()
