# -*- coding: utf-8 -*-
"""
Created on Fri Aug  4 09:18:01 2023

@author: xinyuan.wei
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.formula.api import ols

# Site
site_name = 'ZM-Mon.csv'
file_name = 'Data for Analysis/' + site_name
save_name = 'Climate CO2F/SI_' + site_name

# Load the data
data = pd.read_csv(file_name, sep=',')
data.rename(columns={'GPP_NT_VUT_REF': 'GPP', 'CO2_F_MDS': 'CO2', 'TA_F': 'T', 'SW_IN_F': 'SW', 
                     'VPD_F': 'VPD', 'PA_F': 'Pa', 'P_F': 'P'}, inplace=True)

# Statistical Modeling - Multiple Regression with Interaction Terms
formula = 'GPP ~ P + CO2 + P:CO2'
model = ols(formula, data).fit()

# Climate variable
cvar = 'P'
icvar = 'P:CO2'

# Sensitivity Analysis
cvar_range = np.linspace(data[cvar].min(), data[cvar].max(), 100)

# Initialize an empty DataFrame to store the results
results = pd.DataFrame()

for temp in [data['CO2'].min(), data['CO2'].mean(), data['CO2'].max()]:
    predicted_gpp = model.params['Intercept'] + model.params[cvar] * cvar_range + model.params['CO2'] * temp + model.params[icvar] * cvar_range * temp

    # Adding results to DataFrame
    temp_results = pd.DataFrame({cvar: cvar_range, 'Predicted_GPP': predicted_gpp})
    temp_results['CO2'] = temp
    results = pd.concat([results, temp_results], ignore_index=True)
    
    # Plot Sensitivity Analysis
    plt.plot(cvar_range, predicted_gpp, label=f'CO2: {temp}')
    
plt.xlabel(cvar)
plt.ylabel('GPP')
plt.legend()
plt.title('Sensitivity Analysis')
plt.show()

# Save the DataFrame to a CSV file
results.to_csv(save_name, index=False)
