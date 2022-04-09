#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import functools

import power
import serializeraw
import utila
import utilatest

import headlines

run, fail = utilatest.create_cli_runner(headlines)


class Evaluate(utilatest.BaseLiner):

    def __init__(self, name, source, pages, expected, archive, workdir,
                 monkeypatch):
        super().__init__(
            program=functools.partial(
                run,
                monkeypatch=monkeypatch,
            ),
            step=f'{name} -VVV',
            pages=pages,
            source=power.link(source),
            workdir=workdir,
            archive=archive,
            loader=self.frompath,
            convert_source=False,
            index=expected,
        )
        self.name = name

    def frompath(self, workdir):
        path = utila.join(workdir, f'headlines__{self.name}_{self.name}.yaml')
        loaded = serializeraw.load_headlines(path)
        return loaded

    def raw(self, value) -> str:
        value = utila.flatten(value)
        collected = [item.raw for item in value]
        result = utila.NEWLINE.join(collected)
        return result
