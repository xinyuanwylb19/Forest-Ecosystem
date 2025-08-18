# -*- coding: utf-8 -*-
"""
Created on Thu Jul  6 15:18:01 2023

@author: xinyuan.wei
"""

import os
import numpy as np
#import matplotlib.pyplot as plt
#import cartopy.feature as cfeature
#import cartopy.crs as ccrs
import glob
from netCDF4 import Dataset

# Function to extract the annual forest GPP
def GPP_Reorganize(input_data, output_data, forest_mask, start_year, end_year):
    # Load the GPP data
    gpp = input_data.variables['GPP'][:] * 3600 * 24 * 365 *1000
    
    # Calculate annual GPP (sum over 12 months)
    num_years = end_year - start_year + 1
    annual_gpp = np.sum(gpp.reshape(-1, 12, *gpp.shape[1:]), axis=1)
    
    # Extract the annual GPP for the period
    annual_gpp = annual_gpp[(start_year-1901):(end_year-1901)+1]
    
    # Apply the forest_mask
    forest_gpp = np.where(forest_mask[None, :, :], annual_gpp, np.nan)

    # Save the annual GPP data to a new NetCDF file
    with Dataset(output_data, 'w', format='NETCDF4_CLASSIC') as output:
        output.createDimension('time', num_years)
        output.createDimension('lat', len(lats))
        output.createDimension('lon', len(lons))

        # Copy 'lat' and 'lon' variables
        lat_var = output.createVariable('lat', lats.dtype, ('lat',))
        lon_var = output.createVariable('lon', lons.dtype, ('lon',))
        lat_var[:] = lats
        lon_var[:] = lons
        
        # Add the forest GPP data
        gpp_var = output.createVariable('GPP', 'f4', ('time', 'lat', 'lon'))
        gpp_var.units = 'kgC m-2 y-1'
        gpp_var.long_name = 'Gross Primary Production'
        output.variables['GPP'][:] = forest_gpp

# Load the biome NetCDF file
biome_path = 'MsTMIP Model Driver/mstmip_driver_global_hd_biome_v1.nc4'
biome_data = Dataset(biome_path, 'r')

# Extract the biome data
lats = biome_data.variables['lat'][:]
lons = biome_data.variables['lon'][:]
biome_type = biome_data.variables['biome_type'][:]

# Filter the forest region where biome_type is > 0 and < 19
forest_mask = ((biome_type > 0) & (biome_type < 19))

'''
# Plot the forest region
# Filter the forest region where biome_type is > 0 and < 19
forest_filtered = np.ma.masked_where((biome_type <= 0) | (biome_type >= 19),
                                     biome_type)

plt.figure(figsize=(12, 6))
ax = plt.axes(projection=ccrs.PlateCarree())
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.BORDERS, linestyle=':')
ax.set_title('Forest Region')

c = ax.pcolormesh(lons, lats, forest_filtered, cmap='viridis', 
                  transform=ccrs.PlateCarree())

# Add color bar
plt.colorbar(c, ax=ax, label='Biome Type', orientation='horizontal')

# Show the plot
plt.show()
'''
      
# Output directory
output_directory = 'Organized Model GPP'

# Ensure that the output directory exists
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Directory containing all GPP files
file_dir = 'MsTMIP Model GPP/'

# Pattern to match all files in the directory
pattern = os.path.join(file_dir, '*.nc4')

# Iterate over all files in the directory
for file_path in glob.glob(pattern):
    # Load the model estimated GPP data
    GPP_data = Dataset(file_path, 'r')
    
    # Extract the file name from the full path
    file_name = os.path.basename(file_path)
    
    # Split the file name into parts
    name_parts = file_name.split('_')
    
    # Construct the new file name
    new_name_parts = name_parts[:-2] + ['Annual', 'Forest', 'GPP.nc4']
    save_name = '_'.join(new_name_parts)
    
    # Construct the full path for the new file
    save_file = os.path.join(output_directory, save_name)
    
    print(f'Processing file: {save_file}\n')
    
    # Apply the function
    GPP_Reorganize(GPP_data, save_file, forest_mask, 1981, 2010)

