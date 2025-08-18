# -*- coding: utf-8 -*-
"""
Created on Fri Jun 30 10:46:07 2023

@author: xinyuan.wei
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.formula.api import ols

# Site
site_name = 'US-MMS.csv'
file_name = 'Data for Analysis/' + site_name
save_name = 'Sensitivity Analysis/SI_' + site_name

# Load the data
data = pd.read_csv(file_name, sep=',')
data.rename(columns={'GPP_NT_VUT_REF': 'GPP'}, inplace=True)
data.rename(columns={'CO2_F_MDS': 'CO2'}, inplace=True)
data.rename(columns={'TA_F': 'T'}, inplace=True)
data.rename(columns={'SW_IN_F': 'SW'}, inplace=True)
data.rename(columns={'VPD_F': 'VPD'}, inplace=True)
data.rename(columns={'PA_F': 'Pa'}, inplace=True)
data.rename(columns={'P_F': 'P'}, inplace=True)

# Data Visualization
#sns.pairplot(data, diag_kind='kde')
#plt.show()

# Correlation Analysis
#correlation_matrix = data.corr()
#sns.heatmap(correlation_matrix, annot=True)
#plt.show()

# Statistical Modeling - Multiple Regression with Interaction Terms
formula = 'GPP ~ CO2 + SW + CO2:SW'
model = ols(formula, data).fit()

# Climate variable
cvar = 'SW'
icvar = 'CO2:SW'

# Model Summary
#print(model.summary())

# Sensitivity Analysis
co2_range = np.linspace(data['CO2'].min(), data['CO2'].max(), 100)
predicted_gpp = model.params['Intercept'] + model.params['CO2'] * co2_range

# Initialize an empty DataFrame to store the results
results = pd.DataFrame()

for temp in [data[cvar].min(), data[cvar].mean(), data[cvar].max()]:
    predicted_gpp += model.params[cvar] * temp + model.params[icvar] * co2_range * temp

    # Adding results to DataFrame
    temp_results = pd.DataFrame({'CO2 Concentration': co2_range, 'Predicted_GPP': predicted_gpp})
    temp_results[cvar] = temp
    results = pd.concat([results, temp_results], ignore_index=True)
    
    # Plot Sensitivity Analysis
    plt.plot(co2_range, predicted_gpp, label=f'cvar = {temp}')
    plt.xlabel('CO2 Concentration')
    plt.ylabel('GPP')
    plt.legend()
    
plt.title('Sensitivity Analysis')
plt.show()

# Save the DataFrame to a CSV file
results.to_csv(save_name, index=False)
