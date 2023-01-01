#! /usr/bin/env python3

#Divergence Pipeline: Calculate divergence from summary stats for a single trait
#Order: generate_SNP_file.py > extract_snps_ukbb.sh > calc_effect_dose.py > R script
#Example Input: ./divergence_pipe.py -i /storage/coda1/p-jlachance6/0/shared/gini/prive_PLR_9ancestries/albumin-1KG_PLR.txt -o /storage/home/hcoda1/8/aharris334/scratch/ -t 1 -p /storage/home/hcoda1/8/aharris334/scratch/plink -u /storage/home/hcoda1/8/aharris334/scratch/UKB_BGENQC_TO_BED/ -k /storage/coda1/p-jlachance6/0/shared/gini/randomized_pop_iids.txt -g /storage/home/hcoda1/8/aharris334/scratch/tmp/ -n 25

import pandas as pd
import numpy as np
import argparse as ap
import subprocess as sp
import shutil
import os
import time

parser = ap.ArgumentParser()
parser = ap.ArgumentParser(prog = 'Divergence Pipeline', description='Run divergence pipeline: generates SNP file, extracts SNPs, and calculates effect dose', epilog = 'NOTE: Output directory must differ from the directory in which the input summary file is located!\nNOTE: Be sure that divergence_pipeline directory (containing all the scripts) is in your path\nNOTE: For the user input, commands DO NOT end in \\ whereas directories DO!')
parser.add_argument("-i", "--input", help="input trait file", required=True)
parser.add_argument("-n", "--number", help="number of top SNPs to extract", type=int, default=100, required=False)
parser.add_argument("-o", "--out_dir", help="output directory", required=True)
parser.add_argument("-t", "--threads", help="thread numbers", type=int, default=1, required=False)
parser.add_argument("-p", "--plink_path", help="path to plink command", required=True)
parser.add_argument("-u", "--ukbb_path", help="path to UKBB data", required=True)
parser.add_argument("-k", "--keep_iids", help="file indicating which iids to keep during extraction", required=True)
parser.add_argument("-g", "--genotype_dir", help="directory of genotype matrices for single trait", required=True)
args = parser.parse_args()

start = time.time()

#Running generate_snp_file.py
input_file = args.input
snp_file_cli = sp.run(["./generate_SNP_file.py", "-i", args.input, "-n", str(args.number), "-o", args.out_dir])

#Splitting input in python - This is crucial for the second script (the extraction) in the pipeline
input_file = input_file.split('/')
input_file = input_file[-1]
new_snp_file = args.out_dir + input_file

#Running extract_snps_ukbb.sh
extract_cli = sp.run(["./extract_snps_ukbb.sh", "-t", str(args.threads), "-p", args.plink_path, "-u", args.ukbb_path, "-s", new_snp_file, "-k", args.keep_iids, "-o", args.genotype_dir])

#Running calc_effect_dose.py
effect_dose_cli = sp.run(["./calc_effect_dose.py", "-i", args.input, "-n", str(args.number), "-g", args.genotype_dir, "-o", args.out_dir])

#Removal of temp files
os.remove(new_snp_file) 
shutil.rmtree(args.genotype_dir) #remove files within this directory along with directory 

#Check if log needs to be written or appended to 
if not os.path.exists('log.txt'):
    output_file = open('log.txt', 'w')
else:
    output_file = open('log.txt', 'a')

#Stop time
runtime = round((time.time() - start), 2)
print(runtime)

#Writing to log
output_file.write('{0}\t{1}\n'.format(str(args.number), str(runtime)))



