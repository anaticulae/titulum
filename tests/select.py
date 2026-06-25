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

import utilo


def main():
    pdf = sys.argv[1]
    completed = utilo.run(
        f'baw test skip --generate --no_insta | grep {pdf}',
        expect=None,
    )
    if completed.returncode:
        if completed.stderr.strip():
            utilo.error(completed.stderr)
        utilo.error('could not locate any tests')
        sys.exit(completed.returncode)
    tests = completed.stdout.strip()
    tests = re.sub(r'[ ]{0,15}\<Function[ ]', '', tests)
    tests = re.sub(r'\]?>', '', tests)
    utilo.log(tests + utilo.NEWLINE * 5)
    tests = tests.splitlines()
    for test in tests:
        cmd = f'baw test nightly -k {test} --no_inst -n1'
        utilo.log(cmd + '\n\n')
        completed = utilo.run(
            cmd,
            expect=None,
        )
        utilo.log(completed.stdout)
        utilo.log(completed.stderr)


if __name__ == "__main__":
    main()
