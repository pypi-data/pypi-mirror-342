"""
ChemBioML Platform - Predictor Using Trained Ridge Regressor
Version: 0.1.0

This module loads a trained Ridge model, applies consistent preprocessing
to new input data, and performs predictions with applicability domain (AD)
analysis via leverage.

It includes:
- Input preprocessing (based on previously trained feature subsets and scalers)
- Loading and applying the trained Ridge model
- Saving prediction results along with leverage values

Author: Viacheslav Muratov
License: GNU General Public License v3.0 (see https://www.gnu.org/licenses/gpl-3.0.en.html)
Date: 22.04.2025
"""

import pandas as pd
from sklearn.preprocessing import StandardScaler
import numpy as np
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error, make_scorer, mean_squared_error, pairwise_distances
from sklearn.linear_model import Ridge
import os
from numpy.linalg import inv
import pickle
import argparse
from .utils import calculate_leverage

def linear_Ridge_predictor_data_preprocessing(X_for_pred, orig_train_descs, orig_val_descs, sel_descs, project_path):
    
    pred_descs_init = X_for_pred[orig_train_descs.columns]
    train_descs = orig_train_descs
    pred_descs = pred_descs_init
    val_descs = orig_val_descs
        
    X_train = train_descs[sel_descs.columns]
    X_val = val_descs[sel_descs.columns]
    X_pred = pred_descs[sel_descs.columns]
    
    scaler = StandardScaler()
    scaler.fit(X_train)
    
    X_train_scaled = scaler.transform(X_train)
    X_train_scaled = pd.DataFrame(X_train_scaled, columns=X_train.columns, index=X_train.index)
    
    X_val_scaled = scaler.transform(X_val)
    X_val_scaled = pd.DataFrame(X_val_scaled, columns=X_val.columns, index=X_val.index)
    
    X_pred_scaled = scaler.transform(X_pred)
    X_pred_scaled = pd.DataFrame(X_pred_scaled, columns=X_pred.columns, index=X_pred.index)
    
    return X_train_scaled, X_val_scaled, X_pred_scaled

def linear_Ridge_predictor_model_preparation(model_path, number_of_model, X_train_scaled, X_val_scaled, y_train, y_val):
    
    with open(model_path, 'rb') as file:
        model = pickle.load(file)
    
    y_pred = model.predict(X_train_scaled)
    r2 = round(r2_score(y_train, y_pred), 3)
    
    y_pred_val = model.predict(X_val_scaled)
    q2 = round(r2_score(y_val, y_pred_val), 3)
    
    print(f'Statistics of your model: R2 = {r2}, Q2 = {q2}; Hyperparameters: {model.get_params()}')
    
    return model

def linear_Ridge_predictor_predict_data(model, X_pred_scaled, X_train_scaled):
    
    predictions = model.predict(X_pred_scaled)
    predictions = pd.DataFrame(predictions, columns=['Predicted'], index=X_pred_scaled.index)
    
    matrix_inverse = inv(np.dot(X_train_scaled.T, X_train_scaled))
    leverage_pred = calculate_leverage(X_pred_scaled, matrix_inverse)
    leverage_pred = pd.DataFrame(leverage_pred, columns=[f'Leverage, AD <= {round(3 * len(X_train_scaled.columns) / len(X_train_scaled), 3)}'], index=X_pred_scaled.index)
    result = pd.concat([predictions, leverage_pred], axis=1)
    
    return result

def linear_Ridge_predictor(args):
    print("Selected function Linear Ridge predictor.")
    descs_for_pred_path = args.features_for_prediction
    project_path = args.project_path
    number_of_model = args.model_number
    output_path = args.output_path
    model_path = f'{project_path}/{number_of_model}/estimators/model.pkl'
    
    X_for_pred = pd.read_excel(descs_for_pred_path, index_col=0)
    orig_train_descs = pd.read_excel(f'{project_path}/sets/ProcessedOriginalTrainFeatures.xlsx', index_col=0)
    orig_val_descs = pd.read_excel(f'{project_path}/sets/ProcessedOriginalValidationFeatures.xlsx', index_col=0)
    y_train = pd.read_excel(f'{project_path}/{number_of_model}/sets/train_set.xlsx', index_col=0)['Observed']
    y_val = pd.read_excel(f'{project_path}/{number_of_model}/sets/validation_set.xlsx', index_col=0)['Observed']
    sel_descs = pd.read_excel(f'{project_path}/{number_of_model}/sets/training_descs_not_std.xlsx', index_col=0)
    print("Data preprocessed.")
    
    X_train_scaled, X_val_scaled, X_pred_scaled = linear_Ridge_predictor_data_preprocessing(X_for_pred, orig_train_descs, orig_val_descs, sel_descs, project_path)
    model = linear_Ridge_predictor_model_preparation(model_path, number_of_model, X_train_scaled, X_val_scaled, y_train, y_val)
    result = linear_Ridge_predictor_predict_data(model, X_pred_scaled, X_train_scaled)
    result.to_excel(f'{output_path}/predictions.xlsx')
    print("Prediction saved.")
