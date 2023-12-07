#!/bin/bash

printenv

trimmedfastqfiles=${fastqfiles//\"$s3downloaddir/\"$trimmeddir}
trimmedfastqfiles=${trimmedfastqfiles//R1_001.fastq/R1_001_val_1.fq}
trimmedfastqfiles=${trimmedfastqfiles//R2_001.fastq/R2_001_val_2.fq}
echo "$trimmedfastqfiles" 
echo "$trimmedfastqfiles"  > /tmp/output/trimmedfastqfiles
mkdir -p $work_dir || exit 1
mkdir -p $genome_dir || exit 1
mkdir -p $download_dir || exit 1