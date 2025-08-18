# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 11:10:06 2023

@author: xinyuan.wei
"""
import os
import glob
import xarray as xr
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

climate_files = {
    'temperature': 'Organized Model Driver/temperature_data.nc',
    'VPD': 'Organized Model Driver/VPD_data.nc',
    'pressure': 'Organized Model Driver/pressure_data.nc',
    'shortwave': 'Organized Model Driver/shortwave_data.nc',
    'precipitation': 'Organized Model Driver/precipitation_data.nc',
    'CO2': 'Organized Model Driver/CO2_data.nc',
}

# Numeric mappings for climate variables
variable_mapping = {
    'CO2': 1, 
    'precipitation': 2, 
    'temperature': 3,
    'VPD': 4, 
    'shortwave': 5, 
    'pressure': 6
}

# Load all climate data into a dictionary
climate_data = {var_name: xr.open_dataset(file) for var_name, file in climate_files.items()}

# Get list of all .nc4 files in the 'Organized Model GPP' directory
nc4_files = glob.glob('Organized Model GPP/*_SG3_Annual_Forest_GPP.nc4')

# Extract all the model names
model_names = [os.path.basename(file).replace('_SG3_Annual_Forest_GPP.nc4', '') for file in nc4_files]

for model_name in model_names:
    print(model_name)
    
    # load GPP dataset
    gpp_file = f'Organized Model GPP/{model_name}_SG3_Annual_Forest_GPP.nc4'
    gpp_ds = xr.open_dataset(gpp_file)

    # create a data array for feature importances
    first_order_importance = xr.DataArray(
        data=np.zeros(gpp_ds['GPP'].isel(time=0).shape, dtype=np.int64),
        dims=['lat', 'lon'],
        coords={
            'lat': gpp_ds['lat'],
            'lon': gpp_ds['lon']
        }
    )

    second_order_importance = first_order_importance.copy()

    for lat in range(gpp_ds.dims['lat']):
        for lon in range(gpp_ds.dims['lon']):
            
            # Skip if the 'GPP' value for this lat/lon is NaN
            if np.isnan(gpp_ds['GPP'].isel(lat=lat, lon=lon)).all():
                continue

            # Create a DataFrame
            df = pd.DataFrame({'GPP': gpp_ds['GPP'].isel(lat=lat, lon=lon).values})
            df = df[df['GPP'].notna()]

            for var_name in climate_data.keys():
                df[var_name] = climate_data[var_name][var_name].isel(lat=lat, lon=lon).values

            # Drop rows with missing GPP values
            df = df.dropna()

            if len(df) > 0:
                
                # Standardize the features
                scaler = StandardScaler()
                df_scaled = pd.DataFrame(scaler.fit_transform(df), columns=df.columns)

                # Define predictors and target variable
                X = df_scaled.drop(columns='GPP')
                y = df_scaled['GPP']

                # Split the data into training and test datasets
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,
                                                                    random_state=42)

                # Fit the RandomForest model
                model_rf = RandomForestRegressor(n_estimators=30, random_state=42)
                model_rf.fit(X_train, y_train)
                importances = model_rf.feature_importances_

                # Find the indices of the first and second most important features
                first_order_idx = np.argmax(importances)
                importances[first_order_idx] = -1
                second_order_idx = np.argmax(importances)

                first_order_importance[lat, lon] = variable_mapping[X.columns[first_order_idx]]
                second_order_importance[lat, lon] = variable_mapping[X.columns[second_order_idx]]

    # Save to new NetCDF files
    if not os.path.exists('Climate Importance'):
        os.makedirs('Climate Importance')
    
    first_order_importance_ds = first_order_importance.to_dataset(name='climate')
    first_order_importance_ds.to_netcdf(f'Climate Importance/{model_name}_1st.nc')
    
    second_order_importance_ds = second_order_importance.to_dataset(name='climate')
    second_order_importance_ds.to_netcdf(f'Climate Importance/{model_name}_2nd.nc')

'''
from sklearn.linear_model import Lasso
from sklearn.metrics import mean_squared_error

        if len(df) > 0:
            
            # standardize the features
            scaler = StandardScaler()
            df_scaled = pd.DataFrame(scaler.fit_transform(df), columns=df.columns)

            # define predictors and target variable
            X = df_scaled.drop(columns='GPP')
            y = df_scaled['GPP']

            # split the data into training and test datasets
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
                
            # fit the Lasso model
            #model_lasso = Lasso(alpha=0.8)
            #model_lasso.fit(X_train, y_train)

            # fit the RandomForest model
            model_rf = RandomForestRegressor(n_estimators=30, random_state=42)
            model_rf.fit(X_train, y_train)

            # get mse for both models
            mse_lasso = mean_squared_error(y_test, model_lasso.predict(X_test))
            mse_rf = mean_squared_error(y_test, model_rf.predict(X_test))

            if mse_lasso < mse_rf:
                # use Lasso model for importance
                importances = np.abs(model_lasso.coef_)
            else:
                # use RandomForest model for importance
                importances = model_rf.feature_importances_

            # find the indices of the first and second most important features
            first_order_idx = np.argmax(importances)
            importances[first_order_idx] = -1
            second_order_idx = np.argmax(importances)

            first_order_importance[lat, lon] = X.columns[first_order_idx]
            second_order_importance[lat, lon] = X.columns[second_order_idx]
'''