#!/bin/bash

# Convert .grib to .nc files

# using cdo (Climate data operator), developed at Max Planck Institute 
# for Meteorology

grb_filepath='/projects/boemgom/data/ERA5/swh_combined_windwaves_swell/grib/'

nc_filepath='/projects/boemgom/data/ERA5/swh_combined_windwaves_swell/netcdf/'


# gulf_of_mexico_2004.grib # example ifilename

for year in {1992..1993}
do
	echo ${year}
	grb_filename="${grb_filepath}gulf_of_mexico_${year}.grib"
	nc_filename="${nc_filepath}gulf_of_mexico_${year}.nc"
	cdo -f nc copy $grb_filename $nc_filename
done
