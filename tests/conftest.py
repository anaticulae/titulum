# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import gennex
import hoverpower
import pytest
import utilotest
from utilotest import mp  # pylint:disable=W0611
from utilotest import td  # pylint:disable=W0611

pytest_plugins = ['pytester', 'xdist']  # pylint: disable=invalid-name

hoverpower.setup(__file__)

RESOURCES = [
    hoverpower.BACHELOR028_PDF,
    hoverpower.BACHELOR032A_PDF,
    hoverpower.BACHELOR032_PDF,
    hoverpower.BACHELOR036_PDF,
    hoverpower.BACHELOR037_PDF,
    hoverpower.BACHELOR039_PDF,
    hoverpower.BACHELOR041A_PDF,
    hoverpower.BACHELOR051_PDF,
    hoverpower.BACHELOR063_PDF,
    hoverpower.BACHELOR067_PDF,
    hoverpower.BACHELOR077_PDF,
    hoverpower.BACHELOR078_PDF,
    hoverpower.BACHELOR086_PDF,
    hoverpower.BACHELOR090_PDF,
    hoverpower.BACHELOR105_PDF,
    hoverpower.BACHELOR128_PDF,
    hoverpower.BOOK173_PDF,
    hoverpower.DISS143_PDF,
    hoverpower.DISS172_PDF,
    #hoverpower.DISS178_PDF,
    #hoverpower.DISS205_PDF,
    #hoverpower.DISS218_PDF,
    #hoverpower.DISS264_PDF,
    #hoverpower.DISS266_PDF,
    hoverpower.DOCU027_PDF,
    #hoverpower.HC_BACH106,
    hoverpower.MASTER031_PDF,
    hoverpower.MASTER063_PDF,
    hoverpower.MASTER072_PDF,
    hoverpower.MASTER075_PDF,
    hoverpower.MASTER083_PDF,
    hoverpower.MASTER089_PDF,
    hoverpower.MASTER098_PDF,
    hoverpower.MASTER099_PDF,
    hoverpower.MASTER110_PDF,
    #hoverpower.MASTER116_PDF,
    #hoverpower.MASTER155_PDF,
]
WORKER = utilotest.worker_count(8, onci=len(RESOURCES))

TEST_TODO = utilotest.test_resources(RESOURCES)


@pytest.mark.usefixtures('session')
def pytest_sessionstart():
    hoverpower.run()


def extract(resources):
    gennex.extract(
        files=resources,
        caption=True,
        cleanup=True,
        codero=True,
        figureo=True,
        footnote=True,
        headnote=True,
        groupme=True,
        pagenumber=True,
        sections=True,
        tablero=True,
        worker=WORKER,
    )
