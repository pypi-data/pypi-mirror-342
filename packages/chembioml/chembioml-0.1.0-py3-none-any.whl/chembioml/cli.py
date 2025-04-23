"""
ChemBioML Platform - Open-Source (OS)
Version: 0.1.0

This script serves as the main command-line interface for the ChemBioML platform,
allowing users to train and evaluate machine learning models using a Ridge Regression
estimator optimized with a Genetic Algorithm.

Commands:
- Train_linear_Ridge_GA_Regressor: Trains a Ridge regression model with feature selection via GA.
- Predict_linear_Ridge: Makes predictions using a previously trained Ridge model.

Author: Viacheslav Muratov
License: GNU General Public License v3.0 (see https://www.gnu.org/licenses/gpl-3.0.en.html)
Date: 22.04.2025
"""

import argparse
import sys
import warnings
import os
from .LinearRidgeGATrainer import Train_linear_Ridge_GA
from .LinearRidgePredictor import linear_Ridge_predictor

def get_args():
    parser = argparse.ArgumentParser(description="Run ML training with user-specified settings.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    train_parser_linear_ridge_ga = subparsers.add_parser("Train_linear_Ridge_GA_Regressor", help="Train a Ridge GA model")
    train_parser_linear_ridge_ga.add_argument("--input_path", required=True, help="Path and file name of your data.")
    train_parser_linear_ridge_ga.add_argument("--endpoint_name", required=True, help="Name of your endpoint.")
    train_parser_linear_ridge_ga.add_argument("--max_features", type=int, required=True, help="Max number of features used for training.")
    train_parser_linear_ridge_ga.add_argument("--min_features", type=int, required=True, help="Min number of features used for training.")
    train_parser_linear_ridge_ga.add_argument("--output_path", required=True, help="Path to your output folder.")
    train_parser_linear_ridge_ga.add_argument("--n_epochs", type=int, default=3, help="Number of training epochs.")
    train_parser_linear_ridge_ga.add_argument("--n_cpu", type=int, default=-1, help="Number of CPU cores to use (-1 = all cores).")
    train_parser_linear_ridge_ga.add_argument("--n_population", type=int, default=1200, help="Size of the population.")
    train_parser_linear_ridge_ga.add_argument("--crossover_proba", type=float, default=0.5, help="Crossover probability.")
    train_parser_linear_ridge_ga.add_argument("--mutation_proba", type=float, default=0.2, help="Mutation probability.")
    train_parser_linear_ridge_ga.add_argument("--n_generations", type=int, default=170, help="Number of generations.")
    train_parser_linear_ridge_ga.add_argument("--crossover_independent_proba", type=float, default=0.5, help="Crossover independent probability.")
    train_parser_linear_ridge_ga.add_argument("--mutation_independent_proba", type=float, default=0.05, help="Mutation independent probability.")
    train_parser_linear_ridge_ga.add_argument("--tournament_size", type=int, default=3, help="Tournament size.")
    train_parser_linear_ridge_ga.add_argument("--n_gen_no_change", type=int, default=10, help="Number of generations without change.")
    train_parser_linear_ridge_ga.set_defaults(func=Train_linear_Ridge_GA)

    predict_parser_linear_ridge = subparsers.add_parser("Predict_linear_Ridge", help="Use your linear Ridge model for predictions.")
    predict_parser_linear_ridge.add_argument("--features_for_prediction", required=True, help="Path and file name of your data for prediction.")
    predict_parser_linear_ridge.add_argument("--project_path", required=True, help="Path to project with trained models.")
    predict_parser_linear_ridge.add_argument("--model_number", type=int, required=True, help="ID of the model for prediction.")
    predict_parser_linear_ridge.add_argument("--output_path", required=True, help="Path to save the predictions.")
    predict_parser_linear_ridge.set_defaults(func=linear_Ridge_predictor)
    args = parser.parse_args()


    return args

def main():
    os.environ['OPENBLAS_NUM_THREADS'] = '1'
    os.environ['MKL_NUM_THREADS'] = '1'
    warnings.filterwarnings("ignore")
    print("\n\n######ChemBioML Platfrom OS starts working.######\n")
    args = get_args()
    args.func(args)

if __name__ == "__main__":
    main()
