"""
ChemBioML Platform - Linear Ridge Regressor Trainer with Genetic Algorithm
Version: 0.1.0

This module contains the complete pipeline for training Ridge regression models 
using genetic algorithm-based feature selection and grid search-based hyperparameter tuning.

It handles:
- Data preprocessing and scaling
- Feature selection with GeneticSelectionCV
- Model training and validation
- Metrics reporting (R2, Q2, MAE, RMSE, CCC, etc.)
- Output generation (plots, statistics, saved models)

Author: Viacheslav Muratov
License: GNU General Public License v3.0 (see https://www.gnu.org/licenses/gpl-3.0.en.html)
Date: 22.04.2025
"""

import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import VarianceThreshold
import numpy as np
from sklearn.metrics import r2_score, mean_squared_error, make_scorer
import matplotlib.pyplot as plt
from sklearn.linear_model import Ridge
from sklearn.model_selection import GridSearchCV, cross_val_predict, LeaveOneOut, RandomizedSearchCV
import os
from genetic_selection import GeneticSelectionCV
import pickle
from sklearn.cluster import FeatureAgglomeration
from sklearn import metrics
from .utils import force_clean_memory, calculate_leverage, standardize_residuals, generate_williams_plot_v2, Q2_F1, Q2_F2, Q2_F3, CCC, y_scramble
    
def GA_selector(X_train, y_train, estimator, params, max_features, min_features, cross_val, n_cpu, n_populationT, crossover_probaT, mutation_probaT, n_generationsT, crossover_independent_probaT, mutation_independent_probaT, tournament_sizeT, n_gen_no_changeT):
    estimatorr = estimator.set_params(**params)
    scorer = make_scorer(mean_squared_error, greater_is_better=False)

    selector = GeneticSelectionCV(
        estimatorr,
        cv=cross_val,
        verbose=1,
        scoring=scorer,
        n_population=n_populationT,
        crossover_proba=crossover_probaT,
        mutation_proba=mutation_probaT,
        n_generations=n_generationsT,
        crossover_independent_proba=crossover_independent_probaT,
        mutation_independent_proba=mutation_independent_probaT,
        tournament_size=tournament_sizeT,
        n_gen_no_change=n_gen_no_changeT,
        caching=False,
        n_jobs=n_cpu,
        min_features=min_features,
        max_features=max_features,
        )
    try:
        selector = selector.fit(X_train, y_train)
    finally:
        force_clean_memory()
    
    return selector
    
def data_processing(X_train, X_val, y_train, output_path):

    correlation_with_target = X_train.apply(lambda x: x.corr(y_train))
    absolute_correlation_with_target = correlation_with_target.abs()
    sorted_columns = absolute_correlation_with_target.sort_values(ascending=False).index.tolist()
    X_train = X_train[sorted_columns]     
    original_index_train = X_train.index
    original_index_val = X_val.index
    
    deletor = VarianceThreshold(threshold=0.02)
    X_train_transformed = deletor.fit_transform(X_train)
    
    X_train_reduced = pd.DataFrame(X_train_transformed, columns=X_train.columns[deletor.get_support()], index=original_index_train)
    X_val_reduced = X_val[X_train_reduced.columns].set_index(original_index_val) 

    scaler = StandardScaler()
    scaler.fit(X_train_reduced)
    X_train_reduced_sc = scaler.transform(X_train_reduced)
    X_train_reduced_sc = pd.DataFrame(X_train_reduced_sc, columns=X_train_reduced.columns, index=X_train_reduced.index)

    agglo = FeatureAgglomeration(n_clusters=None, distance_threshold=0.141, linkage='ward')

    X_train_reduced_sc = agglo.fit_transform(X_train_reduced_sc)
    feat = agglo.feature_names_in_

    original_feature_names = agglo.feature_names_in_

    n_clusters = agglo.n_features_in_

    labels = agglo.labels_

    feature_mapping = {}
    original_features = []
    for i in range(n_clusters):
        original_features = original_feature_names[labels == i].tolist()
        feature_mapping[f"Cluster_{i}"] = original_features
    features_list = []
    for cluster, features in feature_mapping.items():
        if features != []:
            features_list.append(features[0])
    with open(f'{output_path}/estimators/FeatureAgglomerationORIGINAL.pkl', 'wb') as file:
        pickle.dump(feat, file)


    X_train_reduced = X_train_reduced[features_list]
    X_val_reduced = X_val_reduced[features_list]
    force_clean_memory()

    return X_train_reduced, X_val_reduced
    
def stat_calc(GA_GS, X_train_sel, X_val_sel, y_train, y_val, n_cpu, epoch, output_path, trainset, params_GA_GS, n_epochs, estimator):
    cv_predictions = cross_val_predict(GA_GS, X_train_sel, y_train, cv=LeaveOneOut(), n_jobs=n_cpu)
    y_pred = GA_GS.predict(X_train_sel)
    y_pred_val = GA_GS.predict(X_val_sel)
    
    train_obss = np.asarray(y_train).reshape(-1)
    train_predd = np.asarray(y_pred).reshape(-1)
    test_obss = np.asarray(y_val).reshape(-1)
    test_predd = np.asarray(y_pred_val).reshape(-1)
    loo_predd = np.asarray(cv_predictions).reshape(-1)

    Yt = y_train
    Yv = y_val


    rmse_of_cal = np.round(np.sqrt(metrics.mean_squared_error(train_obss, train_predd)), 3)
    rmse_of_val = np.round(np.sqrt(metrics.mean_squared_error(test_obss, test_predd)), 3)
    rmse_of_loo = np.round(np.sqrt(metrics.mean_squared_error(train_obss, loo_predd)), 3)



    mae_c = np.round(metrics.mean_absolute_error(train_obss, train_predd), 3)
    mae_v = np.round(metrics.mean_absolute_error(test_obss, test_predd), 3)
    mae_loo = np.round(metrics.mean_absolute_error(y_train, cv_predictions), 3)

    r2 = np.round(r2_score(y_train, y_pred), 3)
    r2loo = np.round(r2_score(y_train, cv_predictions), 3)
    q2 = np.round(r2_score(y_val, y_pred_val), 3)
    
    q2f1 = np.round(Q2_F1(test_obss, test_predd, train_obss), 3)
    q2f2 = np.round(Q2_F2(test_obss, test_predd, train_obss), 3)
    q2f3 = np.round(Q2_F3(test_obss, test_predd, train_obss), 3)
    ccc = np.round(CCC(test_obss, test_predd), 3)
        
    model_vars = list(X_train_sel[:0])
    coe = GA_GS.coef_

    equation = str(np.round(GA_GS.intercept_, 3)) + ' + '
    for co in range(0, len(coe)):
        equation = equation + str(np.round(coe[co], 3)) +' x '+ str(model_vars[co]) + ' + '

    scrambled_r2_avg, scrambled_q2_avg = y_scramble(estimator, X_train_sel, y_train, X_val_sel, y_val, params_GA_GS, epoch, output_path, iters=100)
        
        

    model_stat = pd.DataFrame({'model (epoch)': [epoch],
                                'r2': [r2],
                                'q2loo': [r2loo],
                                'q2': [q2],
                                'rmse_of_cal': [rmse_of_cal],
                                'rmse_of_loo': [rmse_of_loo],
                                'rmse_of_val': [rmse_of_val],
                                'mae_c': [mae_c],
                                'mae_loo': [mae_loo],
                                'mae_v': [mae_v],
                                'q2f1': [q2f1],
                                'q2f2': [q2f2],
                                'q2f3': [q2f3],
                                'ccc': [ccc],
                                'Hyperparameters': [params_GA_GS],
                                'Equation': [equation],
                                'r2_scr': scrambled_r2_avg,
                                'q2_scr': scrambled_q2_avg})
    model_stat.set_index('model (epoch)', inplace=True)       
    
    plt.figure(figsize=(7,7))
    plt_train = plt.scatter(train_predd,Yt, s=100, c='lightblue', marker='^', edgecolors='darkblue', linewidth=1.5, alpha=0.7)
    plt_test = plt.scatter(test_predd,Yv, s=100, c='salmon', marker='D', edgecolors='darkred', linewidth=1.5, alpha=0.7)

    p1 = max(max(train_predd), max(Yt))
    p2 = min(min(train_predd), min(Yv))
    plt.plot([p1, p2], [p1, p2], 'k-', lw=2, alpha=0.5)


    dx = 0.005
    dy = 0.3


    plt.xlabel('Predicted', fontsize='15')
    plt.ylabel('Observed', fontsize='15')
    plt.xticks(size=15)
    plt.yticks(size=15)

    plt.legend((plt_train, plt_test),
                ('Training set','Validation set'),
                scatterpoints = 1,
                loc = 'upper left',
                ncol = 1,
                frameon=False,
                fontsize=15)
    plt.savefig(f'{output_path}/{epoch}/plots/obspred.jpg', dpi=600)

    index_name = trainset.index.name
    DataPoint_train_df = pd.DataFrame({index_name: X_train_sel.index})
    Y_Predicted_train = pd.DataFrame({'Predicted': y_pred})
    cv_predicted_df = pd.DataFrame({'LOO Predicted': cv_predictions})
    OBServed_train = pd.DataFrame({'Observed': y_train})
    obs_pred_df_train = pd.concat([DataPoint_train_df, Y_Predicted_train, cv_predicted_df], axis=1)
    obs_pred_df_train.set_index([index_name], inplace=True)
    obs_pred_df_train = pd.concat([OBServed_train, obs_pred_df_train], axis=1)

    DataPoint_val_df = pd.DataFrame({index_name: X_val_sel.index})
    Y_Predicted_val = pd.DataFrame({'Predicted': y_pred_val})
    OBServed_val = pd.DataFrame({'Observed': y_val})
    obs_pred_df_val = pd.concat([DataPoint_val_df, Y_Predicted_val], axis=1)
    obs_pred_df_val.set_index([index_name], inplace=True)
    obs_pred_df_val = pd.concat([OBServed_val, obs_pred_df_val], axis=1)
    
    try:
        df_train_AD, df_test_AD = generate_williams_plot_v2(X_train_sel, X_val_sel, train_obss, train_predd, test_obss, test_predd, epoch, output_path)
        trainset = pd.concat([obs_pred_df_train, df_train_AD, X_train_sel], axis=1)
        valset = pd.concat([obs_pred_df_val, df_test_AD, X_val_sel], axis=1) 
    except:
        print('Williams plot wasn`t generated for this model')
        trainset = pd.concat([obs_pred_df_train, X_train_sel], axis=1)
        valset = pd.concat([obs_pred_df_val, X_val_sel], axis=1) 

    with open(f'{output_path}/{epoch}/estimators/model.pkl', 'wb') as file:
        pickle.dump(GA_GS, file)
                
    valset.to_excel(f'{output_path}/{epoch}/sets/validation_set.xlsx')
    trainset.to_excel(f'{output_path}/{epoch}/sets/train_set.xlsx')

    force_clean_memory()
    
    return model_stat, r2, r2loo, q2
    
def model_fit(X_train_reduced, y_train, X_val_reduced, y_val, estimator, params, param_grid, trainset, max_features, min_features, cross_val, X_tr_no_std, X_val_not_std, n_cpu, n_populationT, crossover_probaT, mutation_probaT, n_generationsT, crossover_independent_probaT, mutation_independent_probaT, tournament_sizeT, n_gen_no_changeT, endpoint_name, n_epochs, output_path):
    
    models = []
    epochs = []


    models_stats = pd.DataFrame(columns=['model (epoch)', 'r2', 'q2loo', 'q2', 'rmse_of_cal','rmse_of_loo', 'rmse_of_val', 'mae_c', 'mae_loo', 'mae_v', 'q2f1', 'q2f2', 'q2f3', 'ccc', 'r2_scr', 'q2_scr', 'Hyperparameters', 'Equation'])
    models_stats.set_index('model (epoch)', inplace=True)
    
    for epoch in range(1, n_epochs+1):

        print(f"Best hyperparameters: {params}.")
        try:
            selector = GA_selector(X_train_reduced, y_train, estimator, params, max_features, min_features, cross_val, n_cpu, n_populationT, crossover_probaT, mutation_probaT, n_generationsT, crossover_independent_probaT, mutation_independent_probaT, tournament_sizeT, n_gen_no_changeT)
            X_train_sel = X_train_reduced.loc[:, selector.support_]
            X_val_sel = X_val_reduced.loc[:, selector.support_]
        
            X_tr_not_std_sel = X_tr_no_std.loc[:, selector.support_]
            X_val_not_std_sel = X_val_not_std.loc[:, selector.support_]
            X_tr_not_std_sel.to_excel(f'{output_path}/{epoch}/sets/training_descs_not_std.xlsx')
            X_val_not_std_sel.to_excel(f'{output_path}/{epoch}/sets/validation_descs_not_std.xlsx')

            print("Features selected.\nStarting new hyperparameter optimization and metrics calculation.")
            scorer = make_scorer(mean_squared_error, greater_is_better=False)
            GA_GS_trainer = GridSearchCV(estimator, param_grid, cv=cross_val, scoring=scorer, n_jobs=n_cpu)
            GA_GS_trainer.fit(X_train_sel, y_train)
            GA_GS = GA_GS_trainer.best_estimator_
            params_GA_GS = GA_GS_trainer.best_params_
    


            model_stat, r2, r2loo, q2 = stat_calc(GA_GS, X_train_sel, X_val_sel, y_train, y_val, n_cpu, epoch, output_path, trainset, params_GA_GS, n_epochs, estimator)
            models_stats = pd.concat([models_stats, model_stat])  
       
            print(f'Model training for epoch {epoch} completed:\nR2: {r2}, Q2loo = {r2loo}, Q2 = {q2}\n')
        finally:
            force_clean_memory()

        if epoch == 1:

            r2loo_check = r2loo
            params = params_GA_GS

        else:
            if r2loo > r2loo_check:
                params = params_GA_GS
                r2loo_check = r2loo         
        models_stats.to_excel(f'{output_path}/model_statistics.xlsx', index=True)
    return  models_stats

def Train_linear_Ridge_GA(args):

    print("Selected function Linear Ridge GA trainer.")
    input_path = args.input_path
    endpoint_name = args.endpoint_name
    max_features = args.max_features
    min_features = args.min_features
    n_epochs = args.n_epochs
    output_path = args.output_path
    n_cpu = args.n_cpu
    # Genetic Algorithm settings
    n_populationT = args.n_population
    crossover_probaT = args.crossover_proba
    mutation_probaT = args.mutation_proba
    n_generationsT = args.n_generations
    crossover_independent_probaT = args.crossover_independent_proba
    mutation_independent_probaT = args.mutation_independent_proba
    tournament_sizeT = args.tournament_size
    n_gen_no_changeT = args.n_gen_no_change
    
    base_path = output_path

    for i in range(1, n_epochs+1):
        folder_name = str(i)
        folder_path1 = os.path.join(base_path, folder_name, 'sets')
        folder_path2 = os.path.join(base_path, folder_name, 'estimators')
        folder_path3 = os.path.join(base_path, folder_name, 'plots')

        if not os.path.exists(folder_path1):
            os.makedirs(folder_path1)
        if not os.path.exists(folder_path2):
            os.makedirs(folder_path2)
        if not os.path.exists(folder_path3):
            os.makedirs(folder_path3)
    folder_path4 = os.path.join(base_path, 'sets')
    if not os.path.exists(folder_path4):
        os.makedirs(folder_path4)
    folder_path5 = os.path.join(base_path, 'estimators')
    if not os.path.exists(folder_path5):
        os.makedirs(folder_path5)
    
    print("Project folders created.\nStarting data preprocessing.")
    trainset = pd.read_excel(input_path, index_col=0, sheet_name='Train')
    valset = pd.read_excel(input_path, index_col=0, sheet_name='Val')
    X_train = trainset.drop(endpoint_name, axis=1)
    y_train = trainset[endpoint_name]
    X_val = valset.drop(endpoint_name, axis=1)
    y_val = valset[endpoint_name]

    X_train_reduced, X_val_reduced = data_processing(X_train, X_val, y_train, output_path)
    X_train_reduced.to_excel(f'{output_path}/sets/ProcessedOriginalTrainFeatures.xlsx', index=True)
    X_val_reduced.to_excel(f'{output_path}/sets/ProcessedOriginalValidationFeatures.xlsx', index=True)

    X_tr_no_std = X_train_reduced
    X_val_not_std = X_val_reduced

    scaler = StandardScaler()
    scaler.fit(X_train_reduced)
    with open(f'{output_path}/estimators/StandardScaler.pkl', 'wb') as file:
        pickle.dump(scaler, file)
    X_train_scaled = scaler.transform(X_train_reduced)
    X_train_scaled = pd.DataFrame(X_train_scaled, columns=X_train_reduced.columns, index=X_train_reduced.index)
    X_val_scaled = scaler.transform(X_val_reduced)
    X_val_scaled = pd.DataFrame(X_val_scaled, columns=X_val_reduced.columns, index=X_val_reduced.index)

    X_train_reduced = X_train_scaled
    X_val_reduced = X_val_scaled
    print("Data preprocessing completed.\nStarting initial hyperparameter optimization.")
    if X_train_reduced.shape[0] < 100:
        cross_val = LeaveOneOut()
        print("Selected LeaveOneOut CV for model optimization due to small dataset size.")
    else:
        cross_val=5
        print("Selected 5-Fold CV for model optimization due to large dataset size.")
    param_grid = {
        'alpha': [1e-4, 1e-3, 1e-2, 1e-1],  # Wide range of alpha
        'fit_intercept': [True, False],
        #'max_iter': [None, 1000, 5000],
        'tol': [1e-4, 1e-3, 1e-2, 1e-1],
        'solver': ['svd', 'cholesky', 'sparse_cg', 'lsqr'],
    }
    estimator = Ridge()
    
    try:
        scorer = make_scorer(mean_squared_error, greater_is_better=False)
        GS_init = RandomizedSearchCV(estimator, param_grid, cv=cross_val, scoring=scorer, n_jobs=n_cpu, verbose=1, n_iter=45)
        GS_init.fit(X_train_reduced, y_train)
        params = GS_init.best_params_
        print("Initial hyperpatameter optimization completed.")
    finally:
        force_clean_memory()
 
    model_fit(X_train_reduced, y_train, X_val_reduced, y_val, estimator, params, param_grid, trainset, max_features, min_features, cross_val, X_tr_no_std, X_val_not_std, n_cpu, n_populationT, crossover_probaT, mutation_probaT, n_generationsT, crossover_independent_probaT, mutation_independent_probaT, tournament_sizeT, n_gen_no_changeT, endpoint_name, n_epochs, output_path)

