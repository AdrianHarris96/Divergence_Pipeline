#! /usr/bin/env python3

#Example input: ./calc_effect_dose.py -i /Volumes/T7/prive_sf_211_PLR_9ancestries/albumin-1KG_PLR.txt -n 100 -g ~/Desktop/albumin/ -o ~/Desktop/

import pandas as pd
import numpy as np
import argparse as ap
import os
import time

parser = ap.ArgumentParser()
parser = ap.ArgumentParser(description='Calculate effect dose for each UKBB individual using the matrix')
parser.add_argument("-i", "--input", help="input trait file", required=True)
parser.add_argument("-n", "--number", help="number of top SNPs to extract", type=int, default=100, required=False)
parser.add_argument("-g", "--genotype_dir", help="directory of genotype matrices for single trait", required=True)
parser.add_argument("-o", "--out_dir", help="output directory for CSV", required=True)
args = parser.parse_args()

#Load into pandas dataframe and sort
summary_df = pd.read_csv(args.input, delimiter = '\t')
summary_df['abs_effect_weight'] = summary_df['effect_weight'].apply(lambda x: abs(x)) #addition of new_column to sort by while retaining info of 'effect_weight' col
summary_df.sort_values(['abs_effect_weight'], ascending=False, inplace=True)
#print(summary_df)

#Creation of dictionary for each chromosome
chrDictionary = {}
count = 1
while count < 23: #change back to 23 once done
	chrDictionary[count] = {} #creation of nested-dictionary within dictionary
	count += 1

stop = args.number
for index in summary_df.index[0:stop]:
	chromosome = summary_df['chrom'][index] #chromosome number
	rsID_allele = str(summary_df['rsID'][index]) + '_' + str(summary_df['A2'][index])
	chrDictionary[chromosome][rsID_allele] = summary_df['effect_weight'][index]#dictionary with rs_A/T/G/C and effect_size (key:value)

os.chdir(args.genotype_dir) #directory containing genotype matrix files for the trait 

#Calculating effect dosages per individual
final_df = pd.DataFrame() #empty dataframe
for chrom in chrDictionary.keys(): 
	inputFile = 'genotype_matrix_chr' + str(chrom) + '.raw'
	if os.path.exists(inputFile):
		matrix_df = pd.read_csv(inputFile, delimiter = ' ')
		matrix_df = matrix_df.fillna(0) #replace NA with 0
		for key in chrDictionary[chrom].keys(): #iterate through rs_A/T/G/C
			matrix_df[key] = matrix_df[key].apply(lambda x: x*(chrDictionary[chrom][key])) #multiply current dataframe by effect sizes
		if final_df.empty:
			matrix_df = matrix_df.drop(['PAT', 'MAT', 'SEX', 'PHENOTYPE'], axis=1)
			final_df = matrix_df #overwrite the empty one
		else:
			matrix_df = matrix_df.drop(['FID', 'IID', 'PAT', 'MAT', 'SEX', 'PHENOTYPE'], axis=1)
			final_df = pd.concat([final_df, matrix_df], axis=1)	
	else:
		pass

#Loading the iids into the indices
iids = final_df['IID']
final_df.index = iids
final_df.drop(['FID', 'IID'], axis=1, inplace=True)

#Summing across all the rows 
sum_df = final_df.apply(np.sum, axis=1)
del(final_df)
sum_df = pd.DataFrame(sum_df, columns=['PGS'])
sum_df['IID'] = sum_df.index
sum_df.reset_index(drop=True, inplace=True)
#print(sum_df)

os.chdir(args.out_dir) #Move to output directory 

#Constructing the output file name
trait = args.input 
trait = trait.split('/')
trait = trait[-1]
trait = trait.split("-")
trait = trait[0]
ouptut_name = trait + '.csv'

#Simply write to separate CSV file 
sum_df.to_csv(ouptut_name, index=False)

