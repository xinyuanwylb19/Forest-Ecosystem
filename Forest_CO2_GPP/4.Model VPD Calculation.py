# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 10:12:45 2023

@author: xinyuan.wei
"""

import os
import numpy as np
from netCDF4 import Dataset
import math

input_dir = 'Organized Model Driver'
output_dir = 'Organized Model Driver'
temperature_filename = 'temperature_data.nc'
humidity_filename = 'humidity_data.nc'
pressure_filename = 'pressure_data.nc'
output_filename = 'VPD_data.nc'

# Define function for the Clausius-Clapeyron equation
def svp(t):
    return 0.6108 * np.exp((17.27 * t) / (t + 237.3))

# Open the original nc files
with Dataset(os.path.join(input_dir, temperature_filename), 'r') as t_nc,\
    Dataset(os.path.join(input_dir, humidity_filename), 'r') as h_nc,\
    Dataset(os.path.join(input_dir, pressure_filename), 'r') as p_nc:

    # Extract the data
    temperature = t_nc.variables['temperature'][:]  # In Celsius
    humidity = h_nc.variables['humidity'][:]  # In g/g
    pressure = p_nc.variables['pressure'][:]  # In kPa

    # Calculate SVP and AVP
    SVP = svp(temperature)
    AVP = ((humidity * pressure) / (0.622 + (0.378 * humidity)))

    # Calculate VPD
    VPD = (SVP - AVP) / 10000

    # Get latitude and longitude values
    lats = t_nc.variables['lat'][:]
    lons = t_nc.variables['lon'][:]

# Save the VPD data as a new NetCDF file
with Dataset(os.path.join(output_dir, output_filename), 'w') as nc:
    # Create dimensions
    nc.createDimension('time', None)  # Or replace None with the length of your time dimension
    nc.createDimension('lat', len(lats))
    nc.createDimension('lon', len(lons))

    # Create variables and assign data
    times = nc.createVariable('time', 'f4', ('time',))
    latitudes = nc.createVariable('lat', 'f4', ('lat',))
    longitudes = nc.createVariable('lon', 'f4', ('lon',))
    vpd_data = nc.createVariable('VPD', 'f4', ('time', 'lat', 'lon',))

    times[:] = np.arange(1981, 2011)
    latitudes[:] = lats
    longitudes[:] = lons
    vpd_data[:] = VPD
