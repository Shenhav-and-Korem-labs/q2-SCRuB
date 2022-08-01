
import numpy as np
import pandas as pd
import qiime2.sdk
import qiime2.plugin
from qiime2.plugin import (Int, Metadata,
                           Str, Bool, List)

from q2_types.sample_data import SampleData
from q2_types.feature_data import FeatureData

from q2_types.feature_table import (FeatureTable,
                                    Frequency,
                                    RelativeFrequency)
from q2_types.feature_data import (FeatureData,
                                   Taxonomy)

from ._method import SCRuB
from ._SCRuB_defaults import *

from qiime2.plugin import SemanticType
from q2_types.sample_data import SampleData
from q2_types.feature_data import FeatureData

# TODO: will need to fix the version number
__version__ = '0.1.0'

# param types
PARAMETERS = {
#                'table': FeatureTable[Frequency], #pd.DataFrame,
              'metadata': Metadata,
              'control_idx_column': Str,
              'sample_type_column': Str,
              'well_location_column': Str,
              'control_order': Str#List 
             }
# perams descriptions
INPUTDESC = {
              'table': DESC_TBL,
#               'metadata': DESC_META
            }

PARAMETERDESC = {  'metadata': DESC_META,
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
    short_description=('Plugin for SCRuB decontamination'),
    description=('This is a QIIME 2 plugin supporting microbial'
                 ' decontamination through SCRuB.'),
    package='q2_SCRuB')

plugin.methods.register_function(
    function=SCRuB,
    inputs={'table': FeatureTable[Frequency], 
              #Metadata,
           },
    parameters=PARAMETERS,
    outputs=[('scrubbed', FeatureTable[Frequency])#, 
#              ('metadata', Metadata)
            ],
    input_descriptions=INPUTDESC, #{'table': DESC_TBL},
    parameter_descriptions=PARAMETERDESC,
    output_descriptions={'scrubbed': DESC_MP, 
#                          'metdata': 'Sample metdata, including fitted parameters from SCRuB'
                         },
    name='microbial decontamination',
    description=('SCRuB is a tool designed to help researchers address the common issue of contamination in microbial studies. This package provides an easy to use framework to apply SCRuB to your projects. All you need to get started are n samples x m taxa count matrices for both your samples and controls.'),
)

