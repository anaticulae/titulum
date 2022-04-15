#!/usr/bin/env python
# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import re
import sys

import utila


def main():
    pdf = sys.argv[1]
    completed = utila.run(f'baw test skip --generate --no_insta | grep {pdf}')
    tests = completed.stdout.strip()
    tests = re.sub(r'[ ]{0,15}\<Function[ ]', '', tests)
    tests = re.sub(r'\]?>', '', tests)
    utila.log(tests + utila.NEWLINE * 5)
    tests = tests.splitlines()
    for test in tests:
        cmd = f'baw test nightly -k {test} --no_inst -n1'
        utila.log(cmd + '\n\n')
        completed = utila.run(
            cmd,
            expect=None,
        )
        utila.log(completed.stdout)
        utila.log(completed.stderr)


if __name__ == "__main__":
    main()
