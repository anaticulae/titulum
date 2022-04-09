# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest
import utila
import utilatest

import headlines
import tests

ARCHIVE = utila.join(headlines.ROOT, 'tests/multiline/expected', exist=True)


@pytest.mark.parametrize('source', [
    pytest.param(power.BACHELOR028_PDF, id='bachelor028'),
    pytest.param(power.BACHELOR032A_PDF, id='bachelor032a'),
    pytest.param(power.BACHELOR032_PDF, id='bachelor032'),
    pytest.param(power.BACHELOR036_PDF, id='bachelor036'),
    pytest.param(power.BACHELOR039_PDF, id='bachelor039'),
    pytest.param(power.BACHELOR041A_PDF, id='bachelor041a'),
    pytest.param(power.BACHELOR078_PDF, id='bachelor078'),
    pytest.param(power.BACHELOR086_PDF, id='bachelor086'),
    pytest.param(power.BACHELOR090_PDF, id='bachelor090'),
    pytest.param(power.BACHELOR105_PDF, id='bachelor105'),
])
def test_multiline_validate(source, testdir, monkeypatch):
    utilatest.fixture_requires(source)
    tests.Evaluate(
        name='multiline',
        source=source,
        pages=':',
        expected=utila.file_name(source),
        archive=ARCHIVE,
        workdir=testdir.tmpdir,
        monkeypatch=monkeypatch,
    ).evaluate()
