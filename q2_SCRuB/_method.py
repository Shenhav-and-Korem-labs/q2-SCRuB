import os
import tempfile
import subprocess
import numpy as np
import pandas as pd
from qiime2 import Metadata


def run_commands(cmds, verbose=True):
    """
    This function is a script runner.
    It was obtained from https://github.com/ggloor
    /q2-aldex2/blob/master/q2_aldex2/_method.py
    """
    if verbose:
        print("Running external command line application(s). This may print "
              "messages to stdout and/or stderr.")
        print("The command(s) being run are below. These commands cannot "
              "be manually re-run as they will depend on temporary files that "
              "no longer exist.")
    print(cmds)
    for cmd in cmds:
        print(cmd)
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


def SCRuB(table: pd.DataFrame,
          metadata: Metadata,
          control_idx_column: str,
          sample_type_column: str,
          well_location_column: str,
          control_order: list ) -> pd.DataFrame:

    print('Starting to run SCRuB on Qiime2!')
    cols=[control_idx_column, sample_type_column] 
    if type(well_location_column)==str:
        cols+= [well_location_column]

    # import and check all columns given are in dataframe
    metadata = metadata.to_dataframe()
    # replace seperation character in metadata
    metadata = metadata.replace('_', '-',
                                regex=True)
    metadata.index = metadata.index.astype(str)
    metadata.index = [ind.replace('_', '-')
                      for ind in metadata.index]
    # check columns are in metadata
    if not all([col_ in metadata.columns for col_ in cols]):
        raise ValueError('Not all columns given are present in the'
                         ' sample metadata file. Please check that'
                         ' the input columns are in the given metdata.')

    # keep only those columns
    scrub_meta = metadata.dropna(subset=cols)
    scrub_meta = scrub_meta.loc[:, cols]

    # filter the metadata & table so they are matched
    table = table.T
#     shared_index = list(set(table.columns) & set(scrub_meta.index))
#     scrub_meta = scrub_meta.reindex(shared_index)
#     table = table.loc[:, shared_index]
    
    scrub_order=[ ','.join([ a.replace(',', '_') for a in control_order ]) if type(control_order) in [list, np.ndarray]
                 else control_order.replace(',', '_') if type(control_order)==str else
                 'NA'][0]
    print(scrub_order)
    scrub_meta = scrub_format(scrub_meta,
                              control_idx_column,
                              sample_type_column,
                              well_location_column)


    # save all intermediate files into tmp dir
    with tempfile.TemporaryDirectory() as temp_dir_name:
        # save the tmp dir locations
        biom_fp = os.path.join(temp_dir_name, 'samples.csv')
        map_fp = os.path.join(temp_dir_name, 'metadata.csv')
        summary_fp = os.path.join(temp_dir_name, 'scrubbed.csv')

        # Need to manually specify header=True for Series (i.e. "meta"). It's
        # already the default for DataFrames (i.e. "table"), but we manually
        # specify it here anyway to alleviate any potential confusion.
        table.T.to_csv(biom_fp, header=True)
        scrub_meta.to_csv(map_fp, header=True)
        
        table.T.to_csv('tmp_smpz.csv', header=True)
        scrub_meta.to_csv('tmp_metadadz.csv', header=True)

        # build command for SCRuB
        cmd = [ 'Rscript', #Documents/sandbox/q2-SCRuB/q2_SCRuB/assets/
              'run_SCRuB.R',
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

        # if run was sucessfull import the data and return
        scrubbed = pd.read_csv(summary_fp, index_col=0)

        return scrubbed