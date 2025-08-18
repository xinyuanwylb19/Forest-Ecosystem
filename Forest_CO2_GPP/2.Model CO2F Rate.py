# -*- coding: utf-8 -*-
"""
Created on Fri Jul  7 15:05:31 2023

@author: xinyuan.wei
"""
import xarray as xr
import os
import glob

# Directory of the input files
input_dir = 'Organized Model GPP/'

# Directory of the output files
output_dir = 'CO2 Fertilization/'

# Get list of all files
files = glob.glob(os.path.join(input_dir, '*_SG[23]_*.nc4'))

# Extract unique model names
model_names = set([os.path.basename(file).split('_SG')[0] for file in files])

for model_name in model_names:
    # Define the file names for the two scenarios
    file2 = os.path.join(input_dir, model_name + '_SG2_Annual_Forest_GPP.nc4')
    file3 = os.path.join(input_dir, model_name + '_SG3_Annual_Forest_GPP.nc4')

    # Load the netCDF files
    ds2 = xr.open_dataset(file2)
    ds3 = xr.open_dataset(file3)

    # Annual GPP increase rate.
    # This operation will automatically align the datasets on their coordinates.
    rate = (ds3['GPP'] - ds2['GPP']) / ds2['GPP'] * 100

    # Average the GPP increase rate over the 30 years
    # skipna=True will ignore NaNs
    average = rate.sum(dim='time', skipna=True) / 30  

    # Replace values less than or equal to zero with NaNs
    average = average.where(average > 0)

    # Define the output file name
    output_file = os.path.join(output_dir, model_name + '_CFE.nc')

    # Save to a new netCDF file
    average.to_netcdf(output_file)



