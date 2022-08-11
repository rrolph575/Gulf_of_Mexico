#!/bin/bash

# This script calls download_ERA5.py in a loop to download multiple 
# years of ERA5 data.

number_cores=36

module purge
module load conda
conda activate /home/rrolph/gulf_of_mexico/gulf_of_mexico_env

for year in {1992..2021}
do
	echo $year
	export year=$year
	python3 download_ERA5.py $year
done




