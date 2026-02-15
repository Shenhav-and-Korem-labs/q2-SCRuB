#!/usr/bin/env Rscript

###################################################
# This R script takes an input:
#  1) a path to a .csv file outlining samples' count-based abundances 
#  2) a path to a .csv file outlining samples' metadata and metadata
#  3) a string outlining teh order the run decontaminations in 
#  4) a path to which teh decontaminated sample file will be written
# and write a csv file of the decontaminatied samples to the specified parth
# It is intended for use with the QIIME2 plugin for SCRuB
#
####################################################

####################################################
#             DESCRIPTION OF ARGUMENTS             #
####################################################
#
# 
library("optparse")

cat(R.version$version.string, "\n")
errQuit <- function(mesg, status=1) { message("Error: ", mesg); q(status=status) }

option_list = list(
  make_option(c("--samples_counts_path"), action="store", default='NULL', type='character',
              help="File path to the .csv file containing sample abundances"),
  make_option(c("--sample_metadata_path"), action="store", default='NULL', type='character',
              help="File path to the .csv file containing sample metadata"),
  make_option(c("--control_order"), action="store", default='NA', type='character',
              help="the order in which control types should be used for contamination removal. Should be inpuuted as a comma-separated list, i.e. 'control blank library prep,control blank extraction control'"),
  make_option(c("--output_path"), action="store", default='NULL', type='character',
              help="File path to store output csv file. If already exists, will be overwritten")
            )

opt <- parse_args(OptionParser(option_list=option_list))

# Assign each of the arguments, in positional order, to an appropriately named R variable
inp.samps <- opt$samples_counts_path
inp.metadata <- opt$sample_metadata_path
cont_order <- opt$control_order
if(cont_order=='NA')cont_order <- NA
out.path <- opt$output_path
### VALIDATE ARGUMENTS ###
# Input directory is expected to contain .fastq.gz file(s)
# that have not yet been filtered and globally trimmed
# to the same length.
if(!file.exists(inp.samps)) {
  errQuit("Input sample file does not exist!")
} else {
  if(!file.exists(inp.metadata)) {
    errQuit("Input metadata file does not exist!")
  }
}
# Output files are to be filenames (not directories) and are to be
# removed and replaced if already present.
for(fn in c(out.path)) {
  if(dir.exists(fn)) {
    errQuit("Output filename ", fn, " is a directory.")
  } else if(file.exists(fn)) {
    invisible(file.remove(fn))
  }
}

## LOAD LIBRARIES ###
suppressMessages({library(SCRuB, quietly=TRUE)})
suppressMessages({library(stringr, quietly=TRUE)})
suppressMessages({library(dplyr, quietly=TRUE)})
suppressMessages({library(rlang, quietly=TRUE)})
cat("SCRuB:", as.character(packageVersion("SCRuB")), "\n")
cat("1) Loading datas\n")
  samples <- read.csv(inp.samps, row.names=1, check.names=FALSE) %>% as.matrix()
  metadata <- read.csv(inp.metadata, row.names=1, check.names=FALSE)
  control_order <- str_split(cont_order, ',')[[1]]
### DECONTAMINATE ###
cat("2) Decontaminating \n")
scr_out <- SCRuB(samples, metadata, control_order)
### WRITE OUTPUT AND QUIT ###
# Formatting as csv plain-text sequence table
cat("3) Write output\n")
# write.csv(scr_out$decontaminated_samples, out.path)
save(scr_out, file=paste0(out.path))
q(status=0)


