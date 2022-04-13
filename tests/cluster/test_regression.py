# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import serializeraw

import headlines.cluster.parser


def test_filter_level4_headlines_bachelor067():
    """Rawmaker determines bold font correctly."""
    source = power.link(power.BACHELOR067_PDF)

    page59 = serializeraw.ptcn_frompath(source, pages=59)[0]
    fontstore = serializeraw.fs_frompath(source, pages=59)

    vector = headlines.cluster.parser.parse_vector(
        navigator=page59,
        fontstore=fontstore,
    )
    bold = [item for item in vector[1] if item == headlines.cluster.parser.BOLD]
    # three bold headlines:
    # 1 Quellcode/Skripte(Auszüge)
    # 1.1 Performance-Messungen
    # 1.2 Monitoring
    assert len(bold) == 3
