""" 
Extract lat/lon/swh 

"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import xarray as xr
import os
from os.path import exists
import cfgrib
from cdo import *
cdo = Cdo()
import geopandas as gpd
 
## Specify filepaths
sitename = 'gulf_of_mexico'
datapath = '/projects/boemgom/data/ERA5/swh_combined_windwaves_swell/grib/'

# Take annual average from hourly data
# this is commented because it was already done.
'''for year in np.arange(1992,2022):
	swh_data_ifile_grb = datapath + sitename + '_' + str(year) + '.grib'
	swh_data_ofile_grb = datapath + 'annual_mean/' + sitename + '_' + str(year) + '_swh.grib'
	
	# Take the annual average swh
	cdo.yearmean(input=swh_data_ifile_grb,output=swh_data_ofile_grb)
	print(year)
'''

# take the average swh across all available years
#xr.open_mfdataset(swh_data_ifiles_grb, parallel=True)  ## this took up too much disk space
# cdo  timmean  -cat '*.nc'  mean.nc  # this bash command was put in a .sh where the annual average swh files are
# cdo.timmean(input=swh_data_ifiles_grb, output=swh_data_ofile_grb) # this does not work

time_period_mean_swh_ifile = '/shared-projects/rev/projects/goMexico/data/mean_1992thru2021_swh.grib'

## Open dataset
ds = cfgrib.open_datasets(time_period_mean_swh_ifile)
ds_waves = ds[0]
ds_waves_data = ds_waves['swh'].values
ds_lats = ds[0].latitude.values
ds_lons = ds[0].longitude.values

points = gpd.read_file("/shared-projects/rev/projects/goMexico/data/vector/project_points.gpkg").to_crs(3174)



## fill in ERA5 significant wave height to the closest matching lat lon in points
points['swh'] = np.nan # set placeholder for swh 

## you need to append swh to the correct row based on latitude and longitude from points 
# points[['latitude','longitude']]

# Find lat/lon that is contained in the ncfile which is closest to the input lat/lon
def geo_idx(dd, dd_array):
   """search for nearest decimal degree in an array of decimal degrees and return the index.
     np.argmin returns the indices of minium value along an axis.
     so subtract dd from all values in dd_array, take absolute value and find index of minium.
    """
   geo_idx = (np.abs(dd_array - dd)).argmin()
   return geo_idx

## commented below because already ran
'''for i in np.arange(0,points.latitude.shape[0]):
	print(i)
	idx_lat = geo_idx(points.latitude[i], ds_lats)
	idx_lon = geo_idx(points.longitude[i], ds_lons)
	swh_closest_to_points_array1 = ds_waves['swh'][idx_lat,idx_lon].data
	print('lat from points file: ' + str(points.latitude[i]) + ' lat from ERA5 waves: ' + str(ds_lats[idx_lat]))
	print('lon from points file: ' + str(points.longitude[i]) + ' lon from ERA5 waves: ' + str(ds_lons[idx_lon]))
	# append data to points
	points.loc[i, 'swh'] = swh_closest_to_points_array1
	
# save new points file that now includes swh
points.to_file('/shared-projects/rev/projects/goMexico/data/vector/project_points_with_swh.gpkg')

'''
