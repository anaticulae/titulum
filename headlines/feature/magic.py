# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import serializeraw

import headlines.utils


def work() -> str:
    detected = headlines.utils.convert_headline_result(
        groups=[],
        strategy=__name__,
    )
    dumped = serializeraw.dump_headlines(detected)
    return dumped
