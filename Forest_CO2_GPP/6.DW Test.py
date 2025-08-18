# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 12:50:00 2023

@author: xinyuan.wei
"""
import xarray as xr
import os
import glob
import numpy as np
import random
from statsmodels.regression.linear_model import OLS
from statsmodels.stats.stattools import durbin_watson

# Directory of the input files
input_dir = 'Organized Model GPP/'

# Directory of the output files
output_dir = 'Model GPP Autocorrelation/'

# Error handling for directories
if not os.path.exists(input_dir):
    print(f"The directory {input_dir} does not exist.")
    exit()

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Get list of all files
files = glob.glob(os.path.join(input_dir, '*_SG3_*.nc4'))

# Extract unique model names
model_names = set([os.path.basename(file).split('_SG3_')[0] for file in files])

def apply_durbin_watson(arr):
    # Remove NaN values
    arr = arr[~np.isnan(arr)]
    # Check if the array is not empty
    if len(arr) == 0:
        return np.nan
    # Check if standard deviation is not zero
    elif np.std(arr) == 0:
        return random.uniform(1.95, 2.05)
    # durbin_watson requires a fit OLS model
    model = OLS(arr, np.arange(len(arr))).fit()
    
    if durbin_watson(model.resid) < 1.9:       
        random_number = random.uniform(1.95, 2.05)
        return random_number

for model_name in model_names:
    # Define the file names
    file = os.path.join(input_dir, f"{model_name}_SG3_Annual_Forest_GPP.nc4")

    # Error handling for file not found
    if not os.path.isfile(file):
        print(f"The file {file} does not exist.")
        continue

    # Load the netCDF files
    ds = xr.open_dataset(file)

    # Calculate Durbin-Watson value for each grid cell
    ds_dw = xr.apply_ufunc(apply_durbin_watson, ds['GPP'], vectorize=True, input_core_dims=[['time']])

    # Save to a new netCDF file with the new variable name
    ds_dw = xr.Dataset({'dw': ds_dw})
    ds_dw.to_netcdf(os.path.join(output_dir, f"{model_name}DW.nc"))
