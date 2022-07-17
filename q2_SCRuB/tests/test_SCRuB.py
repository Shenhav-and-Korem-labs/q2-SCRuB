


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
        
        samples=pd.read_csv(self.get_data_path('plasma_data.csv'), index_col=0)
        metadata=pd.read_csv(self.get_data_path('plasma_metadata.csv'), index_col=0)
        control_order=metadata.loc[metadata.is_control].sample_type.unique()
        metadata.is_control=metadata.is_control*1
        metadata.index.name = 'sampleid'
        SCRuB(samples, 
              _method.Metadata(metadata), 
              control_idx_column='is_control', 
              sample_type_column='sample_type', 
              well_location_column='sample_well', 
              control_order=control_order )


if __name__ == '__main__':
    unittest.main()