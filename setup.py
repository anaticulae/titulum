#!/usr/bin/env python
# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila

PACKAGES = [
    'headlines',
    'headlines.cluster',
    'headlines.feature',
    'headlines.improve',
    'headlines.levelfour',
    'headlines.multiline',
    'headlines.nlarge',
    'headlines.nolevel',
    'headlines.single',
    'headlines.standard',
]
ENTRY_POINTS = {
    'console_scripts': ['headlines = headlines.cli:main'],
}

if __name__ == "__main__":
    utila.install(__file__)
