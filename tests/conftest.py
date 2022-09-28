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
import utilatest
from utilatest import mp  # pylint:disable=W0611
from utilatest import td  # pylint:disable=W0611

import headlines

pytest_plugins = ['pytester', 'xdist']  # pylint: disable=invalid-name

PACKAGE = headlines.PROCESS
power.setup(headlines.ROOT)

RESOURCES = [
    power.BACHELOR028_PDF,
    power.BACHELOR032A_PDF,
    power.BACHELOR032_PDF,
    power.BACHELOR036_PDF,
    power.BACHELOR037_PDF,
    power.BACHELOR039_PDF,
    power.BACHELOR041A_PDF,
    power.BACHELOR051_PDF,
    power.BACHELOR063_PDF,
    power.BACHELOR067_PDF,
    power.BACHELOR077_PDF,
    power.BACHELOR078_PDF,
    power.BACHELOR086_PDF,
    power.BACHELOR090_PDF,
    power.BACHELOR105_PDF,
    power.BACHELOR128_PDF,
    power.BOOK173_PDF,
    power.DISS143_PDF,
    power.DISS172_PDF,
    power.DISS178_PDF,
    power.DISS205_PDF,
    power.DISS218_PDF,
    power.DISS264_PDF,
    power.DISS266_PDF,
    power.DOCU027_PDF,
    power.HC_BACH106,
    power.MASTER031_PDF,
    power.MASTER063_PDF,
    power.MASTER072_PDF,
    power.MASTER075_PDF,
    power.MASTER083_PDF,
    power.MASTER089_PDF,
    power.MASTER098_PDF,
    power.MASTER099_PDF,
    power.MASTER110_PDF,
    power.MASTER116_PDF,
    power.MASTER155_PDF,
]
WORKER = utilatest.worker_count(8, onci=len(RESOURCES))

TEST_TODO = utilatest.test_resources(RESOURCES)


@pytest.mark.usefixtures('session')
def pytest_sessionstart():
    power.run()


def extract(resources):
    genex.extract(
        files=resources,
        caption=True,
        cleanup=True,
        codero=True,
        figureo=True,
        groupme=True,
        sections=True,
        tablero=True,
        worker=WORKER,
    )
