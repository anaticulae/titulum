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

ARCHIVE = utilo.join(titulum.ROOT, 'tests/result/expected', exist=True)


@pytest.mark.parametrize('source', tests.conftest.TEST_TODO)
@utilotest.longrun
def test_validate_result(source, td, mp):
    utilotest.fixture_requires(source)
    ResultEvaluate(
        source=source,
        workdir=td.tmpdir,
        mp=mp,
    ).evaluate()


class ResultEvaluate(tests.Evaluate):

    def __init__(self, source, workdir, mp):
        super().__init__(
            name='result --all',
            source=source,
            pages=':',
            expected=utilo.file_name(source),
            archive=ARCHIVE,
            workdir=workdir,
            mp=mp,
        )

    def raw(self, value) -> str:
        if not value:
            return ''
        result = f'STRATEGY:{value.__strategy__}\n\n'
        result += super().raw(value)
        return result
