import os
import tempfile
import subprocess
import numpy as np
import pandas as pd
from pandas import DataFrame
from qiime2 import Metadata
from q2_types.feature_table import (FeatureTable,
                                    Frequency,
                                    RelativeFrequency)
import pyreadr
import ast
import biom
from biom import load_table


import rpy2.robjects as ro
from rpy2.robjects import pandas2ri
from rpy2.robjects.conversion import localconverter


def run_commands(cmds, verbose=True):
    """
    This function is a script runner.
    It was obtained from https://github.com/ggloor
    /q2-aldex2/blob/master/q2_aldex2/_method.py
    also dada2
    """
    if verbose:
        print("Running external command line application(s). This may print "
              "messages to stdout and/or stderr.")
        print("The command(s) being run are below. These commands cannot "
              "be manually re-run as they will depend on temporary files that "
              "no longer exist.")
    for cmd in cmds:
        if verbose:
            print("\nCommand:", end=' ')
            print(" ".join(cmd), end='\n\n')
        subprocess.run(cmd, check=True)


def scrub_format(meta: pd.DataFrame,
                 control_idx_column: str,
                 sample_type_column: str,
                 well_location_column: str) -> pd.DataFrame:
    """
    Helper function to format metadata for SCRuB.
    """
    cols=[control_idx_column, sample_type_column] 
    if type(well_location_column)==str:
        cols+= [well_location_column]
    
    return( meta[cols] )


def SCRuB(table: biom.Table, #pd.DataFrame,
          metadata: DataFrame,# Metadata,
          control_idx_column: str = None,
          sample_type_column: str = 'sample_type',
          well_location_column: str= 'well_id',
          control_order: list= 'NA' ) -> pd.DataFrame:

    # read from table csvs if paths are provided
    if type(table)==str:
        if table[-4:]=='.biom':
            table=load_table(table)
        else:
            table=pd.read_csv(table, index_col=0, sep='\t')
    if type(metadata)==str:
        metadata=Metadata( pd.read_csv(metadata, index_col=0, sep='\t') )
    
    print('Running SCRuB on Qiime2!')
    cols=[control_idx_column, sample_type_column] 
    if type(well_location_column)==str:
        cols+= [well_location_column]

    # import and check all columns given are in dataframe
    try:
        metadata = metadata.to_dataframe()
    except:
        pass
    
    
    try:
        table = table.to_dataframe()
    except:
        pass
    
    is_inverted=False
    if table.index.isin(metadata.index.values).mean() < table.columns.isin(metadata.index.values).mean():
        table=table.T
        is_inverted=True
    
    # replace seperation character in metadata
    metadata = metadata.replace('_', '-',
                                regex=True)
    metadata.index = metadata.index.astype(str)
    metadata.index = [ind.replace('_', '-')
                      for ind in metadata.index]
    
        
    if control_idx_column is None:
        control_idx_column='is_negative_control'
        if 'empo_2' in metadata.columns:
            metadata[control_idx_column] = metadata['empo_2'].str.lower().str.contains('negative')
        elif 'qiita_empo_2' in metadata.columns:
            metadata[control_idx_column] = metadata['qiita_empo_2'].str.lower().str.contains('negative')
        else:
            raise(ValueError('No control_idx_column specified, an no empo_2 column is provided to infer which samples are negative controls!'))
    
    
    # check columns are in metadata
    if not all([col_ in metadata.columns for col_ in cols]):
        raise ValueError('Not all columns given are present in the'
                         ' sample metadata file. Please check that'
                         ' the input columns are in the given metdata.')

    # keep only those columns
    scrub_meta = metadata.dropna(subset=cols).loc[:, cols]
    
    try:
        scrub_order=ast.literal_eval(control_order)
    except:
        pass
    
    scrub_order=[ ','.join([ a.replace(',', '_') for a in control_order ]) if type(control_order) in [list, np.ndarray]
                 else control_order if type(control_order)==str else
                 'NA'][0]

    scrub_meta = scrub_format(scrub_meta,
                              control_idx_column,
                              sample_type_column,
                              well_location_column)

    
    # filter the metadata & table so they are matched
    shared_index = list(set(table.index) & set(scrub_meta.index))
    scrub_meta = scrub_meta.loc[shared_index]
    table = table.loc[shared_index]

    # save all intermediate files into tmp dir
    with tempfile.TemporaryDirectory() as temp_dir_name:
        # save the tmp dir locations
        biom_fp = os.path.join(temp_dir_name, 'samples.csv')
        map_fp = os.path.join(temp_dir_name, 'metadata.csv')
        summary_fp = os.path.join(temp_dir_name, 'scrubbed.Rdata')

        # Need to manually specify header=True for Series (i.e. "meta"). It's
        # already the default for DataFrames (i.e. "table"), but we manually
        # specify it here anyway to alleviate any potential confusion.
        table.to_csv(biom_fp, header=True)
        scrub_meta.to_csv(map_fp, header=True)


        # build command for SCRuB
        cmd = ['run_SCRuB.R',
               '--samples_counts_path', biom_fp,
               '--sample_metadata_path', map_fp,
               '--control_order', scrub_order,
               '--output_path', summary_fp]

        try:
            run_commands([cmd])
        except subprocess.CalledProcessError as e:
            print(e)
            raise Exception("An error was encountered while running SCRuB"
                            " in R (return code %d), please inspect stdout"
                            " and stderr to learn more." % e.returncode)

        # if run was sucessful import the data and return
#         scrubbed = pd.read_csv(summary_fp, index_col=0)
        
        ro.r.load(summary_fp)
        decont=ro.r['scr_out'][0]
        with localconverter(ro.default_converter + pandas2ri.converter):
            decontaminated_samples = pd.DataFrame(ro.conversion.rpy2py(decont), 
                                                  index= list(decont.rownames),
                                                  columns=list(decont.colnames)
                                                  )

        out_metadata=metadata.loc[decontaminated_samples.index]
        out_metadata['p'] = list( ro.r['scr_out'][1] )
        
        return decontaminated_samples#, out_metadata
