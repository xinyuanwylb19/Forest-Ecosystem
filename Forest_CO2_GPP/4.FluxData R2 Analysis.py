# -*- coding: utf-8 -*-
"""
Created on Mon Jul 17 09:26:23 2023

@author: xinyuan.wei
"""

import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Directory containing the CSV files
data_dir = 'R2 CO2 GPP'

# Empty list to hold dataframes
dataframes = []

# Empty figure for plotting
plt.figure(figsize=(10, 6))

# Loop over all CSV files in the directory
for file_name in os.listdir(data_dir):
    if file_name.endswith('.csv'):  # only process CSV files
        full_path = os.path.join(data_dir, file_name)

        # Load the data
        data = pd.read_csv(full_path, sep=',')
        data.rename(columns={'GPP_NT_VUT_REF': 'GPP', 'CO2_F_MDS': 'CO2'}, inplace=True)

        # Normalizing the data
        data['GPP'] = (data['GPP'] - data['GPP'].min()) / (data['GPP'].max() - data['GPP'].min())
        data['CO2'] = (data['CO2'] - data['CO2'].min()) / (data['CO2'].max() - data['CO2'].min())

        # Add to list of dataframes
        dataframes.append(data)

        # Add this data to the plot
        sns.scatterplot(data=data, x='GPP', y='CO2')

# Combine all dataframes
combined = pd.concat(dataframes, ignore_index=True)

# Save combined data to CSV
combined.to_csv('GPP_CO2.csv', index=False)

# Add labels and title to the plot
plt.title('Relationship between normalized GPP and CO2')
plt.xlabel('Normalized GPP')
plt.ylabel('Normalized CO2')
plt.show()
