# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configos

# minimal headline count for a valid extraction, depending on document
# length.
HEADLINE_COUNT_MIN = configos.HolyTable(items=(
    (0, 6),
    (20, 6),
    (30, 8),
    (100, 12),
    (150, 15),
    (200, 15),
    (300, 20),
))
