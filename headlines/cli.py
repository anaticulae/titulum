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
        inputs=[
            utila.ResultFile('rawmaker', 'text_text'),
            utila.ResultFile('rawmaker', 'text_positions'),
            utila.ResultFile('rawmaker', 'border_pages'),
            utila.ResultFile('groupme', 'footer_footerheader'),
            utila.ResultFile('rawmaker', 'fonts_header'),
            utila.ResultFile('rawmaker', 'fonts_content'),
            utila.ResultFile('sections', 'section_result', optional=True),
        ],
        output=('cluster',),
    ),
    utila.create_step(
        'levelfour',
        inputs=[
            utila.ResultFile('rawmaker', 'text_text'),
            utila.ResultFile('rawmaker', 'text_positions'),
            utila.ResultFile('rawmaker', 'border_pages'),
            utila.ResultFile('groupme', 'footer_footerheader'),
            utila.ResultFile('rawmaker', 'fonts_header'),
            utila.ResultFile('rawmaker', 'fonts_content'),
            utila.ResultFile('sections', 'section_result', optional=True),
        ],
        output=('levelfour',),
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
            utila.ResultFile('sections', 'section_result', optional=True),
        ],
        output=('multiline',),
    ),
    utila.create_step(
        'nolevel',
        inputs=[
            utila.ResultFile('rawmaker', 'text_text'),
            utila.ResultFile('rawmaker', 'text_positions'),
            utila.ResultFile('rawmaker', 'border_pages'),
            utila.ResultFile('groupme', 'footer_footerheader'),
            utila.ResultFile('rawmaker', 'fonts_header'),
            utila.ResultFile('rawmaker', 'fonts_content'),
            utila.ResultFile('sections', 'section_result', optional=True),
        ],
        output=('nolevel',),
    ),
    utila.create_step(
        'nlarge',
        inputs=[
            utila.ResultFile('rawmaker', 'text_text'),
            utila.ResultFile('rawmaker', 'text_positions'),
            utila.ResultFile('rawmaker', 'border_pages'),
            utila.ResultFile('groupme', 'footer_footerheader'),
            utila.ResultFile('rawmaker', 'fonts_header'),
            utila.ResultFile('rawmaker', 'fonts_content'),
            utila.ResultFile('sections', 'section_result', optional=True),
        ],
        output=('nlarge',),
    ),
    utila.create_step(
        'single',
        inputs=[
            utila.ResultFile('rawmaker', 'text_text'),
            utila.ResultFile('rawmaker', 'text_positions'),
            utila.ResultFile('rawmaker', 'border_pages'),
            utila.ResultFile('groupme', 'footer_footerheader'),
            utila.ResultFile('rawmaker', 'fonts_header'),
            utila.ResultFile('rawmaker', 'fonts_content'),
            utila.ResultFile('sections', 'section_result', optional=True),
        ],
        output=('single',),
    ),
    utila.create_step(
        'standard',
        inputs=[
            utila.ResultFile('rawmaker', 'text_text'),
            utila.ResultFile('rawmaker', 'text_positions'),
            utila.ResultFile('rawmaker', 'border_pages'),
            utila.ResultFile('groupme', 'footer_footerheader'),
            utila.ResultFile('rawmaker', 'fonts_header'),
            utila.ResultFile('rawmaker', 'fonts_content'),
            utila.ResultFile('sections', 'section_result', optional=True),
        ],
        output=('standard',),
    ),
    utila.create_step(
        'result',
        inputs=[
            utila.ResultFile('headlines', 'cluster_cluster', optional=True),
            utila.ResultFile('headlines', 'multiline_multiline', optional=True),
            utila.ResultFile('headlines', 'nolevel_nolevel', optional=True),
            utila.ResultFile('headlines', 'nlarge_nlarge', optional=True),
            utila.ResultFile('headlines', 'single_single', optional=True),
            utila.ResultFile('headlines', 'standard_standard', optional=True),
        ],
        output=('result',),
    ),
    utila.create_step(
        'legacy',
        inputs=[
            utila.ResultFile('headlines', 'result_result', optional=True),
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
            rename=rename,
        ),
    )


def rename(path):
    # TODO: REMOVE AFTER REPLACING WORDS IN THE WHOLE CHAIN.
    if not isinstance(path, str):
        path = [rename(item) for item in path]
        return path
    path = utila.rreplace(
        path,
        pattern='headlines__legacy_result',
        replace='words__headlines_headlines',
    )
    # TODO: WHAT SHALL WE DO WITH: words__headlines_oneline.yaml?
    return path
