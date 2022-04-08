#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import utila
import utila.cli

import headlines

DESCRIPTION = ''

WORKPLAN = [
    utila.create_step(
        'cluster',
        inputs=[],
        output=('cluster',),
    ),
    utila.create_step(
        'magic',
        inputs=[],
        output=('magic',),
    ),
    utila.create_step(
        'multiline',
        inputs=[
            utila.ResultFile('rawmaker', 'text_text'),
            utila.ResultFile('rawmaker', 'text_positions'),
            utila.ResultFile('rawmaker', 'border_pages'),
            utila.ResultFile('groupme', 'footer_footerheader'),
            utila.ResultFile('rawmaker', 'fonts_header'),
            utila.ResultFile('rawmaker', 'fonts_content'),
        ],
        output=('multiline',),
    ),
    utila.create_step(
        'nolevel',
        inputs=[],
        output=('nolevel',),
    ),
    utila.create_step(
        'nlarge',
        inputs=[],
        output=('nlarge',),
    ),
    utila.create_step(
        'single',
        inputs=[],
        output=('single',),
    ),
    utila.create_step(
        'standard',
        inputs=[],
        output=('standard',),
    ),
    utila.create_step(
        'result',
        inputs=[
            utila.ResultFile('headlines', 'cluster_cluster', optional=True),
            utila.ResultFile('headlines', 'magic_magic', optional=True),
            utila.ResultFile('headlines', 'multiline_multiline', optional=True),
            utila.ResultFile('headlines', 'nolevel_nolevel', optional=True),
            utila.ResultFile('headlines', 'nlarge_nlarge', optional=True),
            utila.ResultFile('headlines', 'single_single', optional=True),
            utila.ResultFile('headlines', 'standard_standard', optional=True),
        ],
        output=('result',),
    ),
]


@utila.saveme
def main():
    utila.featurepack(
        root=headlines.ROOT,
        workplan=WORKPLAN,
        featurepackage='headlines.feature',
        config=utila.FeaturePackConfig(
            description=DESCRIPTION,
            multiprocessed=True,
            name=headlines.PROCESS,
            pages=True,
            version=headlines.__version__,
        ),
    )
