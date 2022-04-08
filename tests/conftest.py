# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import genex
import power
import pytest

import headlines

pytest_plugins = ['pytester', 'xdist']  # pylint: disable=invalid-name

PACKAGE = headlines.PROCESS
power.setup(headlines.ROOT)
WORKER = 4

RESOURCES = [
    power.BACHELOR028_PDF,
    power.BACHELOR032A_PDF,
    power.BACHELOR032_PDF,
    power.BACHELOR036_PDF,
    power.BACHELOR039_PDF,
    power.BACHELOR041A_PDF,
    power.BACHELOR078_PDF,
    power.BACHELOR086_PDF,
    power.BACHELOR090_PDF,
    power.BACHELOR105_PDF,
]


@pytest.mark.usefixtures('session')
def pytest_sessionstart():
    power.run()


def extract(resources):
    genex.extract(
        files=resources,
        destination=power.generated(),
        base=power.REPOSITORY,
        groupme=True,
        worker=WORKER,
        pages=':',
    )
