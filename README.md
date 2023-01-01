# Divergence_Pipeline README
Pipeline to calculate divergence for single trait
Order: generate_SNP_file.py > extract_snps_ukbb.sh > calc_effect_dose.py > R script

Pipeline
- `generate_SNP_file.py`: Generate SNP file for single trait.
- `extract_snps_ukbb.sh`: Extract SNPs for a subset of individuals in the UKBB.
- `calc_effect_dose.py`: Calculate effect dose for each UKBB individual using the matrix. 
