#! /usr/bin/env python3

#Example input: ./generate_snp_file.py -i /Volumes/T7/prive_sf_211_PLR_9ancestries/albumin-1KG_PLR.txt -n 100 -o ~/Desktop/
#This script will operate in a continuous pipeline to calculate the divergence for a single trait 

import pandas as pd
import argparse as ap
import os
import time

parser = ap.ArgumentParser()
parser = ap.ArgumentParser(description="Generate SNP file for single trait")
parser.add_argument("-i", "--input", help="input trait file", required=True)
parser.add_argument("-n", "--number", help="number of top SNPs to extract", type=int, default=100, required=False)
parser.add_argument("-o", "--out_dir", help="output directory", required=True)
args = parser.parse_args()

#Load into pandas dataframe
df = pd.read_csv(args.input, delimiter = '\t')
df['effect_weight'] = df['effect_weight'].apply(lambda x: abs(x)) #calculate absolute value for the weight 
df.sort_values(['effect_weight'], ascending=False, inplace=True) #ordering by abs(effect weight)

#Load two relevant columns into a tuple 
rsList = []
stop = args.number
for index in df.index[0:stop]:
	rsList.append((df['rsID'][index], df['A2'][index])) #Tuple to be used in the creation of snp_list.txt

os.chdir(args.out_dir) #move to snp_list_dir

#Extracting the suffix of the filename 
filename = args.input #file path to break down
filename = filename.split('/')
filename = filename[-1]

#Writing to output
output = open(filename, 'w')
for item in rsList:
	item = '\t'.join(item)
	output.write(item)
	output.write('\n')
output.close()




