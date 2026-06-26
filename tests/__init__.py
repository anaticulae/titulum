#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import functools

import hoverpower
import serializeraw
import utilo
import utilotest

import titulum

run, fail = utilotest.create_cli_runner(titulum)


class Evaluate(utilotest.BaseLiner):

    def __init__(self, name, source, pages, expected, archive, workdir, mp):
        super().__init__(
            program=functools.partial(
                run,
                mp=mp,
            ),
            step=f'{name} -VVV' if name else '',
            pages=pages,
            source=hoverpower.link(source),
            workdir=workdir,
            archive=archive,
            loader=self.frompath,
            convert_source=False,
            index=expected,
        )
        self.name = name.split()[0]

    def frompath(self, workdir):
        path = utilo.join(workdir, f'headlines__{self.name}_{self.name}.yaml')
        loaded = serializeraw.load_headlines(path)
        return loaded

    def raw(self, value) -> str:
        value = utilo.flat(value)
        collected = [rawline(item) for item in value]
        result = utilo.NEWLINE.join(collected)
        return result


def rawline(item) -> str:
    level = 0
    if item.level:
        level = item.level - 1
    raw = '    ' * level
    raw += utilo.normalize_text(
        item.raw,
        strips=True,
    )
    return raw
