#! /bin/bash

#Example input: ./extract_snps_ukbb.sh -t 4 -p <plink_path> -u <ukbb_path> -s <snp_file> -k <keep_iids> -o <output_directory>
#Example: ./extract_snps_ukbb.sh -t 4 -p /storage/home/hcoda1/8/aharris334/scratch/plink -u /storage/home/hcoda1/8/aharris334/scratch/UKB_BGENQC_TO_BED -s /storage/home/hcoda1/8/aharris334/scratch/albumin-1KG_PLR_100_snps.txt -k /storage/coda1/p-jlachance6/0/shared/gini/randomized_pop_iids.txt -o /storage/home/hcoda1/8/aharris334/scratch/albumin

threads=1
#add --keep command

function HELP {
	echo "Use -t flag for number of threads"
	echo "Use -p flag for path to plink"
	echo "Use -u flag for path to UKBB data"
	echo "Use -s flag for SNP files for single trait" #No snp directory and more just a single file 
	echo "Use -k flag to indicate which iids to keep during extraction"
	echo "Use -o flag for output directory"
	exit 2
}

while getopts "t:p:u:s:k:o:v" option; do 
	case $option in
		t) threads=$OPTARG;;
		p) plink_path=$OPTARG;;
		u) ukbb_path=$OPTARG;;
		s) snp_file=$OPTARG;;
		k) keep_iids=$OPTARG;;
		o) out_dir=$OPTARG;;
		v) set -x;;
		\?) HELP;;
	esac
done

#Make the output_dir
mkdir $out_dir

for i in $(seq 1 22); do 
	${plink_path} --bfile ${ukbb_path}/UKB_BED_AFTER_QC_removed182IDs_chr${i} --keep ${keep_iids} --recode A --recode-allele $snp_file --extract $snp_file --out ${out_dir}/genotype_matrix_chr${i} --threads $threads
done


