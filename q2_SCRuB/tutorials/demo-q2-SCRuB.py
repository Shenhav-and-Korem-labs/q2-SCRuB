

import numpy as np
import pandas as pd
from qiime2 import Metadata
from q2_SCRuB import SCRuB

samples = pd.read_csv('data/plasma_smaples.csv', index_col=0)
metadata = pd.read_csv('data/plasma_metadata.csv',index_col=0)
control_order=['control blank DNA extraction', 'control blank library prep']
metadata.index.name='sampleid'

scrubbed=SCRuB(samples, 
               Metadata(metadata), 
               'is_control', 
               'sample_type', 
               'sample_well',
               control_order )

print(scrubbed.iloc[:20, :20])

