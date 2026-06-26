# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Multiline
=========

Example
-------

.. code-block:: none

    3. EU-Initiativen zur Bekämpfung der Steuervermeidung und
       des schädlichen Steuerwettbewerbs
"""

import serializeraw

import titulum.feature
import titulum.multiline.run
import titulum.utils


def work(
    text: str,
    textpositions: str,
    sizeandborder: str,
    headerfooter: str,
    fontheader: str = None,
    fontcontent: str = None,
    sections: str = None,
    pages: tuple = None,
) -> str:
    pages = titulum.feature.headlinepart(
        pages=pages,
        sections=sections,
    )
    ptcns = serializeraw.ptcn_fromfile(
        text,
        textpositions,
        sizeandborder,
        headerfooter,
        fontheader,
        fontcontent,
        pages=pages,
    )
    groups = titulum.multiline.run.run(ptcns)
    detected = titulum.utils.convert_headline_result(
        groups=groups,
        strategy=__name__,
    )
    dumped = serializeraw.dump_headlines(detected)
    return dumped
