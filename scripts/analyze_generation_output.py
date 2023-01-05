
# Plot LCOE heat maps from the reV/NRWAL output.

import pandas as pd
import geopandas as gpd
from rex import Resource
import numpy as np
from revruns import rr
import cartopy.crs as ccrs
import matplotlib.pyplot as plt

# example output file:
# /shared-projects/rev/projects/goMexico/rev/generation/0_17MW_lowSP/0_17MW_lowSP_generation_2007.h5

# Filepaths
basepath = '/shared-projects/rev/projects/goMexico/rev/generation/'
run_name = '0_17MW_lowSP'
datapath = basepath + run_name + '/'



#for year in np.arange(2000,2022):
year = 2007
ifile = datapath + run_name + '_generation_2007.h5'
# Load metadata of the file
res = Resource(ifile)
meta = res.meta
# Display the metadata
meta.keys()
# Display all NRWAL outputs
res.datasets
# Extract the LCOE
meta_geo = meta.rr.to_geo()
# UTM Zone 15N
meta_geo = meta_geo.to_crs(32615)
# add gid
meta_geo = meta_geo.reset_index()
# add a column in the meta_geo dataset that has LCOE data. res contains many variables from NRWAL output 
# (including LCOE).
meta_geo['lcoe_fcr'] = res['lcoe_fcr'] # throws a warning. 

# plot the lcoe
lcoe = meta_geo['lcoe_fcr'].values
lats = meta_geo['latitude'].values
lons = meta_geo['longitude'].values


## you need to reindex your data
# https://stackoverflow.com/questions/72393462/1d-netcdf-to-2d-lat-lon-using-xarray-and-dask
def closest_factor_pair(x: int) -> tuple:
    """
    Tries to find the pair of factors of x, i.e. the
    closest integers to the square root of x.

    Example
    >>> closest_factor_pair(34191)
    (131, 261)
    """
    for i in range(int(np.sqrt(x)), 0, -1):
        if x % i == 0:
            return i, int(x/i)
    return None

new_shape = closest_factor_pair(lats.shape[0])
lats = lats.reshape(new_shape)
lons = lons.reshape(new_shape)
lcoe = lcoe.reshape(new_shape)

fig = plt.figure('map')
ax = fig.add_axes([0.1, 0.12, 0.80, 0.75], projection=ccrs.PlateCarree())
# https://stackoverflow.com/questions/66971453/ho-to-plot-a-cartopy-map-for-every-column
#img = ax.scatter(lons, lats, s=7, c=lcoe/max(lcoe), cmap='viridis', marker='x', transform=ccrs.PlateCarree())
#img = ax.scatter(lons, lats, s=7, cmap='viridis', marker='o', transform=ccrs.PlateCarree())
#img = ax.scatter(lons, lats, lcoe, transform = ccrs.PlateCarree())
# add colorbar
img = ax.contourf(lons, lats, lcoe)
cb = plt.colorbar(img, extend = 'both', spacing = 'proportional', orientation = 'horizontal', cax = fig.add_axes([0.12, 0.07, 0.76, 0.02]))

lat_lon_buffer = 2 # degrees
ax.set_extent([lons.min() - lat_lon_buffer, lons.max()+ lat_lon_buffer, lats.min() - lat_lon_buffer, lats.max() + lat_lon_buffer], crs=ccrs.PlateCarree())
ax.coastlines()
plt.show()

