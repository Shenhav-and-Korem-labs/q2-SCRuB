
# SCRuB QIIME2 Plugin

<!-- badges: start -->
  [![R-CMD-check](https://github.com/Shenhav-and-Korem-labs/SCRuB/actions/workflows/check-standard.yaml/badge.svg)](https://github.com/Shenhav-and-Korem-labs/SCRuB/actions/workflows/check-standard.yaml)
  [![Codecov test
coverage](https://codecov.io/gh/Shenhav-and-Korem-labs/SCRuB/graph/badge.svg)](https://app.codecov.io/gh/Shenhav-and-Korem-labs/SCRuB)
  <!-- badges: end -->

<img src='../vignettes/SCRuB_logo.png' align="right" height="139" />

SCRuB is a tool designed to help researchers address the common issue of contamination in microbial studies. This package provides an easy to use framework to apply SCRuB to your projects. All you need to get started are n samples x m taxa count matrices for both your samples and controls.

Support
-----------------------
For support using SCRuB, please use our <a href="https://github.com/Shenhav-and-Korem-labs/SCRuB/issues">issues page</a> or email: gia2105@columbia.edu.

## Install q2-SCRuB

If you have not already done so, activate your QIIME environment.

```shell
source activate qiime2-20xx.x
```
Next we will need to ensure some dependancies are installed.

Now we will install SCRuB and the q2-plugin.

```R
# the main SCRuB package, along with all dependencies
> R
> devtools::install_github("shenhav-and-korem-labs/SCRuB")
> torch::install_torch()
> quit()
```
```shell
# the QIIME2 plugin
pip install git+https://github.com/Shenhav-and-Korem-labs/q2-SCRuB.git
```

# Tutorial 

A QIIME2 demo notebook is available [here](https://github.com/Shenhav-and-Korem-labs/q2-SCRuB/blob/master/q2_SCRuB/tutorials/Demo-q2-SCRuB.ipynb)

## Running q2-SCRuB

The QIIME 2 implementation of SCRuB contains a single `SCRuB` function. This takes an input one data frame of feature abundances per sample, and another for the sample's metadata. Additional inputs to the QIIME2 SCRuB implementation are the relevant column names for the metadata and a list outlining the order in which the decontamination should be run. As outputs, QIIME2's `SCRuB` returns a data frame of the decontaminated samples' features. 

The below script outlines a working example for running q2-SCRuB, in which we access the samples and metadata from the `tutorials/data` directory:

```python
import pandas as pd
from qiime2 import Metadata
from q2_SCRuB import SCRuB

# set up the inputs
samples = pd.read_csv('data/plasma_samples.csv', index_col=0)
metadata = pd.read_csv('data/plasma_metadata.csv',index_col=0)
control_order=['control blank DNA extraction', 'control blank library prep']
metadata.index.name='sampleid'

# run SCRuB
scrubbed=SCRuB(samples, 
               Metadata(metadata), 
               'is_control', 
               'sample_type', 
               'sample_well',
               control_order )
```
