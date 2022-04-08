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

import headlines.multiline.run


def work(
    text: str,
    textpositions: str,
    sizeandborder: str,
    headerfooter: str,
    fontheader: str = None,
    fontcontent: str = None,
    pages: tuple = None,
) -> str:
    ptcns = serializeraw.ptcn_fromfile(
        text,
        textpositions,
        sizeandborder,
        headerfooter,
        fontheader,
        fontcontent,
        pages=pages,
    )
    detected = headlines.multiline.run.run(ptcns)
    dumped = serializeraw.dump_headlines(detected)
    return dumped
