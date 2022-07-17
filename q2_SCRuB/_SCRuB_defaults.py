# Configuration file where you can set the parameter default values and
# descriptions.

DEFAULT_ORDER = 'NA'
DEFAULT_WELL_COL = 'sample_well'
DEFAULT_SAMPLE_COL = 'sample_type'
DEFAULT_CONTROL_COL = 'is_control'


DESC_META = ('Sample metadata file containing sources'
             ' and sinks for source tracking.')
DESC_TBL = ('Feature table file containing samples'
            ' and controls for decontaminatoin.')
DESC_MP = ('The decontaminated samples returned from SCRuB.')

DESC_CONTROL_COL = ('Name of the 0 vs 1 metadata column indicating which entries represent contamination sources')

DESC_SAMPLE_COL = ('Name of the `str` metadata column indicating sample types' )

DESC_WELL_COL = ('Name of the `str` metadata column (in "A10, B9" format) identifying each sample sequencing location.')

DESC_CONTROL_ORDER = ('List identifying the order in which control types should be used for contamination removal.')
                   
