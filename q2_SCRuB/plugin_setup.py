
import numpy as np
import pandas as pd
import qiime2.sdk
import qiime2.plugin
from qiime2.plugin import (Int, Metadata,
                           Str, Bool)
from q2_types.feature_table import (FeatureTable,
                                    Frequency,
                                    RelativeFrequency)
from q2_types.feature_data import (FeatureData,
                                   Taxonomy)

from ._method import SCRuB
from ._SCRuB_defaults import *


# TODO: will need to fix the version number
__version__ = '0.1.0'

# param types
PARAMETERS = {
               'table': pd.DataFrame,
              'metadata': Metadata,
              'control_idx_column': str,
              'sample_type_column': str,
              'well_location_column': str,
              'control_order': list 
             }
# perams descriptions
PARAMETERDESC = {
                  'table': DESC_TBL,
                  'metadata': DESC_META,
                  'control_idx_column': DESC_CONTROL_COL,
                  'sample_type_column': DESC_SAMPLE_COL,
                  'well_location_column': DESC_WELL_COL,
                  'control_order': DESC_CONTROL_ORDER 
                }

citations = qiime2.plugin.Citations.load('citations.bib',
                                         package='q2_SCRuB')

plugin = qiime2.plugin.Plugin(
    name='SCRuB',
    version=__version__,
    website="https://github.com/korem-lab/SCRuB",
    citations=[citations['AustinSCRuB2022']],
    short_description=('Plugin for SCRuB decontaminatoin'),
    description=('This is a QIIME 2 plugin supporting microbial'
                 ' decontamination through SCRuB.'),
    package='q2_SCRuB')

plugin.methods.register_function(
    function=SCRuB,
    inputs={'table': FeatureTable[Frequency]},
    parameters=PARAMETERS,
    outputs=[('scrubbed', FeatureTable[Frequency])],
    input_descriptions={'table': DESC_TBL},
    parameter_descriptions=PARAMETERDESC,
    output_descriptions={'proportions': DESC_MP},
    name='microbial source-tracking',
    description=('SCRuB is a tool designed to help researchers address the common issue of contamination in microbial studies. This package provides an easy to use framework to apply SCRuB to your projects. All you need to get started are n samples x m taxa count matrices for both your samples and controls.'),
)

