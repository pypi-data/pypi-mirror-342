"""
ChemBioML Platform - Utility Functions
Version: 0.1.0

This module provides supporting functions for memory cleanup, leverage calculation,
residual standardization, Williams plot generation, Q² metric variants, 
concordance correlation coefficient (CCC), and Y-scrambling for model robustness.

These utilities are shared across both the training and prediction modules.

Author: Viacheslav Muratov
License: GNU General Public License v3.0 (see https://www.gnu.org/licenses/gpl-3.0.en.html)
Date: 22.04.2025
"""

import gc
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score, mean_squared_error
import matplotlib.pyplot as plt
from numpy.linalg import inv
from sklearn.utils import shuffle

def force_clean_memory():
    for n in range(10):
        gc.collect()

def calculate_leverage(data, matrix_inverse):
    leverage_indices = []
    for index, row in data.iterrows():
        x_i = row.values
        leverage = np.dot(x_i, np.dot(matrix_inverse, x_i.T))
        leverage_indices.append(leverage)
    return leverage_indices

def standardize_residuals(observed, predicted):
    residuals = observed - predicted
    return StandardScaler().fit_transform(residuals.reshape(-1, 1)).flatten()

def generate_williams_plot_v2(train_data, test_data, observed_train, predicted_train, observed_test, predicted_test, epoch, output_path, annotation_offset_x=0.005, annotation_offset_y=0.3):


    matrix_inverse = inv(np.dot(train_data.T, train_data))
    leverage_train = calculate_leverage(train_data, matrix_inverse)
    leverage_test = calculate_leverage(test_data, matrix_inverse)
    standardized_residuals_train = standardize_residuals(observed_train, predicted_train)
    standardized_residuals_test = standardize_residuals(observed_test, predicted_test)
    

    df_train = pd.DataFrame({
        'Leverage': leverage_train,
        'Standardized Residuals': standardized_residuals_train
    }, index=train_data.index)
    
    df_test = pd.DataFrame({
        'Leverage': leverage_test,
        'Standardized Residuals': standardized_residuals_test
    }, index=test_data.index)

    plt.figure(figsize=(10, 7.5))


    plt.scatter(leverage_train, standardized_residuals_train, s=120, c='lightblue', marker='^', edgecolors='darkblue', linewidth=1.5, alpha=0.7)
    plt.scatter(leverage_test, standardized_residuals_test, s=120, c='salmon', marker='D', edgecolors='darkred', linewidth=1.5, alpha=0.7)

    plt.ylim(-4, 4)
    plt.legend(['Training set', 'Validation set'], loc='upper left', frameon=False, fontsize=15)
    plt.xlabel('Leverages', fontsize='15')
    plt.ylabel('Standardized Residuals', fontsize='15')
    plt.xticks(size=15)
    plt.yticks(size=15)
    plt.axhline(y=3, color='gray', linestyle='--')
    plt.axhline(y=-3, color='gray', linestyle='--')
    plt.axvline(x=(3 * len(train_data.columns) / len(train_data)), linestyle='--')
    plt.savefig(f'{output_path}/{epoch}/plots/williams_plot.jpg', dpi=600)
    force_clean_memory()
    
    return df_train, df_test

def Q2_F1(test_obs, test_pred, train_obs):

    squared_resid=[]
    for x in range(0, len(test_obs)):
        squared_resid.append(np.power((test_obs[x]-test_pred[x]), 2))
    sum_sq_resid = np.sum(squared_resid)

    squared_summary = []
    mean_y_train = np.mean(train_obs)
    for x in range(0, len(test_obs)):
        squared_summary.append(np.power((test_obs[x]-mean_y_train), 2))
    sum_squared_summary = np.sum(squared_summary)

    q2_f1 = 1 - (sum_sq_resid/sum_squared_summary)
    return q2_f1


def Q2_F2(test_obs, test_pred, train_obs):

    squared_resid=[]
    for x in range(0, len(test_obs)):
        squared_resid.append(np.power((test_obs[x]-test_pred[x]), 2))
    sum_sq_resid = np.sum(squared_resid)

    squared_summary = []
    mean_y_test = np.mean(test_obs)
    for x in range(0, len(test_obs)):
        squared_summary.append(np.power((test_obs[x]-mean_y_test), 2))
    sum_squared_summary = np.sum(squared_summary)

    q2_f2 = 1 - (sum_sq_resid/sum_squared_summary)
    return(q2_f2)


def Q2_F3(test_obs, test_pred, train_obs):

    squared_resid=[]
    for x in range(0, len(test_obs)):
        squared_resid.append(np.power((test_obs[x]-test_pred[x]), 2))
    sum_sq_resid = np.sum(squared_resid)

    squared_summary = []
    mean_y_test = np.mean(train_obs)
    for x in range(0, len(train_obs)):
        squared_summary.append(np.power((train_obs[x]-mean_y_test), 2))
    sum_squared_summary = np.sum(squared_summary)

    q2_f3 = 1 - ((sum_sq_resid/len(test_obs))/(sum_squared_summary/len(train_obs)))
    return(q2_f3)


def CCC(test_obs, test_pred):

    equat_top = []
    mean_y_test_obs = np.mean(test_obs)
    mean_y_test_pred = np.mean(test_pred)
    for x in range(0, len(test_obs)):
        equat_top.append((test_obs[x]-mean_y_test_obs)*(test_pred[x]-mean_y_test_pred))
        equat_top_sum = 2*np.sum(equat_top)

    equat_bot_1 = []
    equat_bot_2 = []
    equat_bot_3 = []
    for x in range(0, len(test_obs)): 
        equat_bot_1.append(np.power((test_obs[x]-mean_y_test_obs), 2))
        equat_bot_2.append(np.power((test_pred[x]-mean_y_test_pred), 2))
        equat_bot_3.append(np.power((mean_y_test_obs-mean_y_test_pred), 2))

    sum_equat_bot = np.sum(equat_bot_1) + np.sum(equat_bot_2) + np.sum(equat_bot_3)

    ccc = equat_top_sum / sum_equat_bot
    return ccc
    
def y_scramble(estimator, df_x_train, y_train, df_x_test, y_test, params, epoch, output_path,iters=100):

    model = estimator.set_params(**params)

    model.fit(df_x_train, y_train)
    y_train_pred = model.predict(df_x_train)
    y_test_pred = model.predict(df_x_test)
    


    original_r2 = r2_score(y_train, y_train_pred)
    original_q2 = r2_score(y_test, y_test_pred)


    scrambled_r2 = []
    scrambled_q2 = []


    for it in range(iters):

        temp_y = shuffle(y_train)        
        model.fit(df_x_train, temp_y)
        y_temp_train_pred = model.predict(df_x_train)
        y_temp_test_pred = model.predict(df_x_test)

        scrambled_r2.append(r2_score(temp_y, y_temp_train_pred))
        scrambled_q2.append(r2_score(y_test, y_temp_test_pred))

    scrambled_r2_avg = str(round(np.mean(scrambled_r2), 3))
    scrambled_q2_avg = str(round(np.mean(scrambled_q2), 3))
    scrambled_r2_std = str(round(np.std(scrambled_r2), 3))
    scrambled_q2_std = str(round(np.std(scrambled_q2), 3))
    
    scrambled_r2_fin = scrambled_r2_avg + "±" + scrambled_r2_std
    scrambled_q2_fin = scrambled_q2_avg + "±" + scrambled_q2_std
    
    scr_set = pd.DataFrame({'R2_scr': scrambled_r2, 'Q2_scr': scrambled_q2})
    scr_set.to_excel(f'{output_path}/{epoch}/sets/y_randomisation_set.xlsx', index=True)
    force_clean_memory()
    
    return scrambled_r2_fin, scrambled_q2_fin
