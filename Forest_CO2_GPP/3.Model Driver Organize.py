# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 13:48:37 2023

@author: xinyuan.wei
"""

import os
import numpy as np
from netCDF4 import Dataset
from netCDF4 import num2date
from cftime import DatetimeGregorian

input_dir = 'MsTMIP Model Driver'
output_dir = 'Organized Model Driver'

'''
############## Pressure ##############
output_filename = 'pressure_data.nc'
# Loop through the files and calculate the yearly mean pressure
yearly_means = []
for year in range(1981, 2011):
    filename = f'mstmip_driver_global_hd_climate_press_monthly_mean_{year}_v1.nc4'
    file_path = os.path.join(input_dir, filename)
    
    with Dataset(file_path, 'r') as nc:
        pressure = nc.variables['press'][:]  # Shape (12, 360, 720)
        yearly_mean = np.mean(pressure, axis=0)  # Shape (360, 720)
        yearly_means.append(yearly_mean)
        # Get latitude and longitude values from the first file
        if year == 1981:
            lats = nc.variables['lat'][:]  # Shape (360,)
            lons = nc.variables['lon'][:]  # Shape (720,)

# Convert list of arrays to a 3D array
all_data = np.stack(yearly_means, axis=0)  # Shape (30, 360, 720)

# Save as a new NetCDF file
output_file_path = os.path.join(output_dir, output_filename)
with Dataset(output_file_path, 'w') as nc:
    # Create dimensions
    nc.createDimension('time', 30)
    nc.createDimension('lat', len(lats))
    nc.createDimension('lon', len(lons))

    # Create variables and assign data
    times = nc.createVariable('time', 'f4', ('time',))
    latitudes = nc.createVariable('lat', 'f4', ('lat',))
    longitudes = nc.createVariable('lon', 'f4', ('lon',))
    pressures = nc.createVariable('pressure', 'f4', ('time', 'lat', 'lon',))

    times[:] = np.arange(1981, 2011)
    latitudes[:] = lats
    longitudes[:] = lons
    pressures[:] = all_data
'''

'''
############## Precipitation ##############
output_filename = 'precipitation_data.nc'
# Loop through the files and calculate the yearly total precipitation
yearly_totals = []
for year in range(1981, 2011):
    filename = f'mstmip_driver_global_hd_climate_rain_monthly_total_{year}_v1.nc4'
    file_path = os.path.join(input_dir, filename)
    
    with Dataset(file_path, 'r') as nc:
        prep = nc.variables['rain_monthly'][:]  # Shape (12, 360, 720)
        yearly_total = np.sum(prep, axis=0)  # Shape (360, 720)
        yearly_totals.append(yearly_total)
        # Get latitude and longitude values from the first file
        if year == 1981:
            lats = nc.variables['lat'][:]  # Shape (360,)
            lons = nc.variables['lon'][:]  # Shape (720,)

# Convert list of arrays to a 3D array
all_data = np.stack(yearly_totals, axis=0)  # Shape (30, 360, 720)

# Save as a new NetCDF file
output_file_path = os.path.join(output_dir, output_filename)
with Dataset(output_file_path, 'w') as nc:
    # Create dimensions
    nc.createDimension('time', 30)
    nc.createDimension('lat', len(lats))
    nc.createDimension('lon', len(lons))

    # Create variables and assign data
    times = nc.createVariable('time', 'f4', ('time',))
    latitudes = nc.createVariable('lat', 'f4', ('lat',))
    longitudes = nc.createVariable('lon', 'f4', ('lon',))
    preps = nc.createVariable('precipitation', 'f4', ('time', 'lat', 'lon',))

    times[:] = np.arange(1981, 2011)
    latitudes[:] = lats
    longitudes[:] = lons
    preps[:] = all_data
'''
'''
############## Temperature ##############
output_filename = 'temperature_data.nc'
# Loop through the files and calculate the yearly mean temperature
yearly_means = []
for year in range(1981, 2011):
    filename = f'mstmip_driver_global_hd_climate_tair_monthly_mean_{year}_v1.nc4'
    file_path = os.path.join(input_dir, filename)
    
    with Dataset(file_path, 'r') as nc:
        temp = nc.variables['Tair_monthly'][:]  # Shape (12, 360, 720)
        yearly_mean = np.mean(temp, axis=0)  # Shape (360, 720)
        yearly_means.append(yearly_mean)
        # Get latitude and longitude values from the first file
        if year == 1981:
            lats = nc.variables['lat'][:]  # Shape (360,)
            lons = nc.variables['lon'][:]  # Shape (720,)

# Convert list of arrays to a 3D array
all_data = np.stack(yearly_means, axis=0)  # Shape (30, 360, 720)

# Save as a new NetCDF file
output_file_path = os.path.join(output_dir, output_filename)
with Dataset(output_file_path, 'w') as nc:
    # Create dimensions
    nc.createDimension('time', 30)
    nc.createDimension('lat', len(lats))
    nc.createDimension('lon', len(lons))

    # Create variables and assign data
    times = nc.createVariable('time', 'f4', ('time',))
    latitudes = nc.createVariable('lat', 'f4', ('lat',))
    longitudes = nc.createVariable('lon', 'f4', ('lon',))
    temps = nc.createVariable('temperature', 'f4', ('time', 'lat', 'lon',))

    times[:] = np.arange(1981, 2011)
    latitudes[:] = lats
    longitudes[:] = lons
    temps[:] = all_data
'''
'''
############## Shortwave Radiation ##############
output_filename = 'shortwave_data.nc'
# Loop through the files and calculate the yearly mean temperature
yearly_means = []
for year in range(1981, 2011):
    filename = f'mstmip_driver_global_hd_climate_swdown_monthly_mean_{year}_v1.nc4'
    file_path = os.path.join(input_dir, filename)
    
    with Dataset(file_path, 'r') as nc:
        shortwave = nc.variables['swdown_monthly'][:]  # Shape (12, 360, 720)
        yearly_mean = np.mean(shortwave, axis=0)  # Shape (360, 720)
        yearly_means.append(yearly_mean)
        # Get latitude and longitude values from the first file
        if year == 1981:
            lats = nc.variables['lat'][:]  # Shape (360,)
            lons = nc.variables['lon'][:]  # Shape (720,)

# Convert list of arrays to a 3D array
all_data = np.stack(yearly_means, axis=0)  # Shape (30, 360, 720)

# Save as a new NetCDF file
output_file_path = os.path.join(output_dir, output_filename)
with Dataset(output_file_path, 'w') as nc:
    # Create dimensions
    nc.createDimension('time', 30)
    nc.createDimension('lat', len(lats))
    nc.createDimension('lon', len(lons))

    # Create variables and assign data
    times = nc.createVariable('time', 'f4', ('time',))
    latitudes = nc.createVariable('lat', 'f4', ('lat',))
    longitudes = nc.createVariable('lon', 'f4', ('lon',))
    shortwaves = nc.createVariable('shortwave', 'f4', ('time', 'lat', 'lon',))

    times[:] = np.arange(1981, 2011)
    latitudes[:] = lats
    longitudes[:] = lons
    shortwaves[:] = all_data
'''

'''
input_dir = 'MsTMIP Model Driver'
output_dir = 'Organized MsTMIP Model Driver'
input_filename = 'mstmip_driver_global_hd_co2_v1.nc4'
output_filename = 'CO2_data.nc'

file_path = os.path.join(input_dir, input_filename)

# Read the original nc file
with Dataset(file_path, 'r') as nc:
    # Convert time values to datetime objects
    time_units = nc.variables['time'].units
    time_cal = nc.variables['time'].calendar
    dates = num2date(nc.variables['time'][:], units=time_units, calendar=time_cal)
    
    # Get the indices for the time period 1981 to 2010
    start_index = np.where(dates >= DatetimeGregorian(1981, 1, 1))[0][0]
    end_index = np.where(dates <= DatetimeGregorian(2010, 12, 31))[0][-1]
    
    # Extract the CO2 data for the desired period
    CO2 = nc.variables['CO2'][start_index:end_index+1, :, :]  # Shape (360, 720, time_period)
    
    # Compute the annual mean CO2 concentration for each grid
    annual_mean_CO2 = CO2.reshape(-1, 12, CO2.shape[1], CO2.shape[2]).mean(axis=1)  # Shape (30, 360, 720)
    
    # Get latitude and longitude values
    lats = nc.variables['lat'][:]  # Shape (360,)
    lons = nc.variables['lon'][:]  # Shape (720,)

# Save as a new NetCDF file
output_file_path = os.path.join(output_dir, output_filename)
with Dataset(output_file_path, 'w') as nc:
    # Create dimensions
    nc.createDimension('time', 30)
    nc.createDimension('lat', len(lats))
    nc.createDimension('lon', len(lons))

    # Create variables and assign data
    times = nc.createVariable('time', 'f4', ('time',))
    latitudes = nc.createVariable('lat', 'f4', ('lat',))
    longitudes = nc.createVariable('lon', 'f4', ('lon',))
    concentrations = nc.createVariable('CO2', 'f4', ('time', 'lat', 'lon',))

    times[:] = np.arange(1981, 2011)
    latitudes[:] = lats
    longitudes[:] = lons
    concentrations[:] = annual_mean_CO2
'''

############## Pressure ##############
output_filename = 'humidity_data.nc'
# Loop through the files and calculate the yearly mean specific humidity
yearly_means = []
for year in range(1981, 2011):
    filename = f'mstmip_driver_global_hd_climate_qair_monthly_mean_{year}_v1.nc4'
    file_path = os.path.join(input_dir, filename)
    
    with Dataset(file_path, 'r') as nc:
        humidity = nc.variables['qair'][:]  # Shape (12, 360, 720)
        yearly_mean = np.mean(humidity, axis=0)  # Shape (360, 720)
        yearly_means.append(yearly_mean)
        # Get latitude and longitude values from the first file
        if year == 1981:
            lats = nc.variables['lat'][:]  # Shape (360,)
            lons = nc.variables['lon'][:]  # Shape (720,)

# Convert list of arrays to a 3D array
all_data = np.stack(yearly_means, axis=0)  # Shape (30, 360, 720)

# Save as a new NetCDF file
output_file_path = os.path.join(output_dir, output_filename)
with Dataset(output_file_path, 'w') as nc:
    # Create dimensions
    nc.createDimension('time', 30)
    nc.createDimension('lat', len(lats))
    nc.createDimension('lon', len(lons))

    # Create variables and assign data
    times = nc.createVariable('time', 'f4', ('time',))
    latitudes = nc.createVariable('lat', 'f4', ('lat',))
    longitudes = nc.createVariable('lon', 'f4', ('lon',))
    humiditys = nc.createVariable('humidity', 'f4', ('time', 'lat', 'lon',))

    times[:] = np.arange(1981, 2011)
    latitudes[:] = lats
    longitudes[:] = lons
    humiditys[:] = all_data
