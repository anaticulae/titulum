#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import utilo
import utilo.cli

import titulum

DESCRIPTION = ''

WORKPLAN = [
    utilo.create_step(
        'levelfour',
        inputs=[
            utilo.ResultFile('rawmaker', 'text_text'),
            utilo.ResultFile('rawmaker', 'text_positions'),
            utilo.ResultFile('rawmaker', 'border_pages'),
            utilo.ResultFile('footnote', 'result_result'),
            utilo.ResultFile('rawmaker', 'fonts_header'),
            utilo.ResultFile('rawmaker', 'fonts_content'),
            utilo.ResultFile('sections', 'section_result', optional=True),
        ],
        output=('levelfour',),
    ),
    utilo.create_step(
        'cluster',
        inputs=[
            utilo.ResultFile('rawmaker', 'text_text'),
            utilo.ResultFile('rawmaker', 'text_positions'),
            utilo.ResultFile('rawmaker', 'border_pages'),
            utilo.ResultFile('footnote', 'result_result'),
            utilo.ResultFile('rawmaker', 'fonts_header'),
            utilo.ResultFile('rawmaker', 'fonts_content'),
            utilo.ResultFile('sections', 'section_result', optional=True),
            utilo.ResultFile('headlines', 'levelfour_levelfour', optional=True),
        ],
        output=('cluster',),
    ),
    utilo.create_step(
        'multiline',
        inputs=[
            utilo.ResultFile('rawmaker', 'text_text'),
            utilo.ResultFile('rawmaker', 'text_positions'),
            utilo.ResultFile('rawmaker', 'border_pages'),
            utilo.ResultFile('footnote', 'result_result'),
            utilo.ResultFile('rawmaker', 'fonts_header'),
            utilo.ResultFile('rawmaker', 'fonts_content'),
            utilo.ResultFile('sections', 'section_result', optional=True),
        ],
        output=('multiline',),
    ),
    utilo.create_step(
        'nolevel',
        inputs=[
            utilo.ResultFile('rawmaker', 'text_text'),
            utilo.ResultFile('rawmaker', 'text_positions'),
            utilo.ResultFile('rawmaker', 'border_pages'),
            utilo.ResultFile('footnote', 'result_result'),
            utilo.ResultFile('rawmaker', 'fonts_header'),
            utilo.ResultFile('rawmaker', 'fonts_content'),
            utilo.ResultFile('sections', 'section_result', optional=True),
        ],
        output=('nolevel',),
    ),
    utilo.create_step(
        'nlarge',
        inputs=[
            utilo.ResultFile('rawmaker', 'text_text'),
            utilo.ResultFile('rawmaker', 'text_positions'),
            utilo.ResultFile('rawmaker', 'border_pages'),
            utilo.ResultFile('footnote', 'result_result'),
            utilo.ResultFile('rawmaker', 'fonts_header'),
            utilo.ResultFile('rawmaker', 'fonts_content'),
            utilo.ResultFile('sections', 'section_result', optional=True),
        ],
        output=('nlarge',),
    ),
    utilo.create_step(
        'single',
        inputs=[
            utilo.ResultFile('rawmaker', 'text_text'),
            utilo.ResultFile('rawmaker', 'text_positions'),
            utilo.ResultFile('rawmaker', 'border_pages'),
            utilo.ResultFile('footnote', 'result_result'),
            utilo.ResultFile('rawmaker', 'fonts_header'),
            utilo.ResultFile('rawmaker', 'fonts_content'),
            utilo.ResultFile('sections', 'section_result', optional=True),
        ],
        output=('single',),
    ),
    utilo.create_step(
        'standard',
        inputs=[
            utilo.ResultFile('rawmaker', 'text_text'),
            utilo.ResultFile('rawmaker', 'text_positions'),
            utilo.ResultFile('rawmaker', 'border_pages'),
            utilo.ResultFile('footnote', 'result_result'),
            utilo.ResultFile('rawmaker', 'fonts_header'),
            utilo.ResultFile('rawmaker', 'fonts_content'),
            utilo.ResultFile('sections', 'section_result', optional=True),
        ],
        output=('standard',),
    ),
    utilo.create_step(
        'result',
        inputs=[
            utilo.ResultFile('headlines', 'cluster_cluster', optional=True),
            utilo.ResultFile('headlines', 'multiline_multiline', optional=True),
            utilo.ResultFile('headlines', 'nolevel_nolevel', optional=True),
            utilo.ResultFile('headlines', 'nlarge_nlarge', optional=True),
            utilo.ResultFile('headlines', 'single_single', optional=True),
            utilo.ResultFile('headlines', 'standard_standard', optional=True),
        ],
        output=('result',),
    ),
    utilo.create_step(
        'legacy',
        inputs=[
            utilo.ResultFile('headlines', 'result_result', optional=True),
        ],
        output=('result',),
    ),
]


@utilo.saveme
def main():
    utilo.featurepack(
        root=titulum.ROOT,
        workplan=WORKPLAN,
        featurepackage='titulum.feature',
        config=utilo.FeaturePackConfig(
            description=DESCRIPTION,
            multiprocessed=True,
            name=titulum.PROCESS,
            pages=True,
            version=titulum.__version__,
            rename=rename,
        ),
    )


def rename(path):
    # TODO: REMOVE AFTER REPLACING WORDS IN THE WHOLE CHAIN.
    if not isinstance(path, str):
        path = [rename(item) for item in path]
        return path
    path = utilo.rreplace(
        path,
        pattern='headlines__legacy_result',
        replace='words__headlines_headlines',
    )
    # TODO: WHAT SHALL WE DO WITH: words__headlines_oneline.yaml?
    return path
