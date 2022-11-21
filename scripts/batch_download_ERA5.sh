#!/bin/bash

# This script calls download_ERA5.py in a loop to download multiple 
# years of ERA5 data.

#SBATCH --account=boemgom
#SBATCH --time=02:59:00
#SBATCH --job-name=download_ERA5
#SBATCH --nodes=1 # This should be number_cores/36 (36 cores on Eagle)
#SBATCH --ntasks-per-node=36
#SBATCH --mail-user rrolph@nrel.gov
#SBATCH --mail-type BEGIN,END,FAIL
#SBATCH --output=EagleLogs/%j.%n.download_ERA5.log

number_cores=36

module purge
module load conda
conda activate /home/rrolph/gulf_of_mexico/gulf_of_mexico_env

for year in {1992..2021}
do
	echo ${year}
	export year=$year
	python3 download_ERA5.py ${year}
done




