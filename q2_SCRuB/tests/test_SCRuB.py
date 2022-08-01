


import os
import unittest
import pandas as pd
import numpy as np
import skbio
import biom
import qiime2
from qiime2.plugin.testing import TestPluginBase
import sys
from q2_SCRuB import SCRuB

class TestSCRuB(TestPluginBase):
    package = 'q2_SCRuB.tests'

    def test_decontamination(self):
        
        # import table
        table =pd.read_csv(self.get_data_path('table.tsv'), sep='\t', index_col=0)
        # import metadata
        metadata = pd.read_csv(self.get_data_path('metadata.tsv'), sep='\t', index_col=0)
        
        scrubbed = SCRuB(table.iloc[:750], 
                 metadata, 
                'is_control', # specifies metadata column where True denotes the negative controls
                'sample_type', # specifies metadata column denoting the sample type
                'well_id', # specifies metadata column representing samples location, in 'A11','B10' format
                ['control blank DNA extraction','control blank library prep']
                )
        
#         samples=pd.read_csv(self.get_data_path('plasma_samples.csv'), index_col=0)
#         metadata=pd.read_csv(self.get_data_path('plasma_metadata.csv'), index_col=0)
#         control_order=metadata.loc[metadata.is_control].sample_type.unique()
#         metadata.is_control=metadata.is_control*1
#         metadata.index.name = 'sampleid'
#         SCRuB(table, 
#               metadata, 
#               control_idx_column='is_control', 
#               sample_type_column='sample_type', 
#               well_location_column='sample_well', 
#               control_order=control_order )


if __name__ == '__main__':
    unittest.main()