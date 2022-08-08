#!/bin/bash

# This script calls download_ERA5.py in a loop to download multiple 
# years of ERA5 data.

#SBATCH 

for year in {1979..1980}
do
	echo ${year}
	python3 download_ERA5.py ${year} &
done




