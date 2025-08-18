# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 16:12:38 2023

@author: xinyuan.wei
"""
import os
import zipfile
import glob
import pandas as pd

file_name = 'FluxTower Data'
'''
# Extract all the zip files
for file_name in glob.glob(os.path.join(file_name, '**', '*.zip'), recursive=True):
    with zipfile.ZipFile(file_name, 'r') as zip_ref:
        for member in zip_ref.namelist():
            if 'SUBSET_YY' in member and member.endswith('.csv'):
                # extract only the CSV files with 'SUBSET_YY' in their name
                zip_ref.extract(member, os.path.dirname(file_name))
''' 

# List of variables to extract
columns_to_keep = ['TIMESTAMP', 'TA_F', 'SW_IN_F', 'VPD_F', 'PA_F', 'P_F',
                   'CO2_F_MDS', 'GPP_NT_VUT_REF']

# Directory where the organized data will be stored
if not os.path.exists('Organized Data'):
    os.makedirs('Organized Data')

# Iterate over all csv files in the 'AmeriFlux Data' directory
file_dir = file_name+'\\*_FLUXNET*_SUBSET_YY_*.csv'

for file_path in glob.glob(file_dir, recursive=True):
    
    # Derive the site name from the file path
    site_name = file_path.split('\\')[1].split('_')[1]
    print(site_name)
    
    # Read the csv file into a DataFrame
    data = pd.read_csv(file_path)
    
    # Extract the necessary columns
    data = data[columns_to_keep]
    
    # Save the data to a new csv file
    data.to_csv(f'Organized Data\\{site_name}.csv', index=False)

print('Data extraction completed successfully.')


