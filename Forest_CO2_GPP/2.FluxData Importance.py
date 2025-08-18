# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 12:51:46 2023

@author: xinyuan.wei
"""
import pandas as pd
import numpy as np
import os
import glob
from sklearn.linear_model import Lasso
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

# Lasso regression method
def lasso_model(df, site_name):
    
    # Handle missing values - drop any rows that contain NaN
    df = df.dropna()

    # Standardize the features to have mean=0 and variance=1
    scaler = StandardScaler()
    df_scaled = pd.DataFrame(scaler.fit_transform(df), columns=df.columns)

    # Define predictors and target variable
    X = df_scaled.drop(columns=['GPP_NT_VUT_REF', 'TIMESTAMP'])
    y = df_scaled['GPP_NT_VUT_REF']

    # Split the data into training and test datasets (60% training, 40% test)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, 
                                                        random_state=42)

    # Define the model 
    model = Lasso(alpha=0.1)

    # Fit the model
    model.fit(X_train, y_train)

    # Get feature importances
    importances = np.abs(model.coef_)
    
    # Predict on the test set
    y_pred = model.predict(X_test)

    # Compute metrics
    mse = mean_squared_error(y_test, y_pred)

    # Create a DataFrame for results
    feature_importances = pd.DataFrame({site_name: importances}, 
                                       index=X.columns)

    return feature_importances, mse

# Random Forest regression method
def randomforest_model(df, site_name):
    
    # Handle missing values - drop any rows that contain NaN
    df = df.dropna()

    # Standardize the features to have mean=0 and variance=1
    scaler = StandardScaler()
    df_scaled = pd.DataFrame(scaler.fit_transform(df), columns=df.columns)

    # Define predictors and target variable
    X = df_scaled.drop(columns=['GPP_NT_VUT_REF', 'TIMESTAMP'])
    y = df_scaled['GPP_NT_VUT_REF']

    # Split the data into training and test datasets (60% training, 40% test)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, 
                                                        random_state=42)

    # Define the model 
    model = RandomForestRegressor(n_estimators=50, random_state=42)

    # Fit the model
    model.fit(X_train, y_train)

    # Predict on the test set
    y_pred = model.predict(X_test)

    # Compute metrics
    mse = mean_squared_error(y_test, y_pred)
    
    # Get feature importances
    importances = model.feature_importances_

    # Create a DataFrame for easier visualization
    feature_importances = pd.DataFrame({site_name: importances}, 
                                       index=X.columns)

    return feature_importances, mse

# Iterate over all csv files in the Data for Analysis directory
file_dir = 'Data for Analysis/*.csv'

# Initialize an empty dataframe to hold all importances and metrics
metrix_im = pd.DataFrame()

for file_path in glob.glob(file_dir):
    
    # Load the data
    df = pd.read_csv(file_path, sep=',')
    
    # Extract site name from the file path
    site_name = os.path.splitext(file_path.split('\\')[-1])[0]

    print('Process: ' + site_name)

    # Apply Lasso regression
    importances_la, mse_la = lasso_model(df, site_name + '_la') 
    
    # Apply Random Forest regresson
    importances_rf, mse_rf = randomforest_model(df, site_name + '_rf')
 
    if mse_la < mse_rf:
        metrix_im = pd.concat([metrix_im, importances_la], axis=1)
        
    else:
        metrix_im = pd.concat([metrix_im, importances_rf], axis=1)

# Save the all_importances and all_metrics dataframes to CSV files
metrix_im.to_csv('Feature Importances.csv')

