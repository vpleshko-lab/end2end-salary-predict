import numpy as np
import pandas as pd
import joblib

from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

from src.models.configs.regression_models import REGRESSION_MODELS
from src.utils.paths import MODELS_DIR
from src.utils.logger import get_logger

logger = get_logger(__name__)

def run_training(data_bundle, preprocessor, save_best_model: bool):
    logger.info("Starting model training pipeline...")

    try:
        X_train = data_bundle['X_train']
        X_test = data_bundle['X_test']
        y_train = data_bundle['y_train']
        y_test = data_bundle['y_test']
    except KeyError as e:
        logger.error(f"Missing data key in data_bundle: {e}")
        raise

    results = []
    best_test_r2 = -np.inf
    best_model_info = None

    for name, (model, params) in REGRESSION_MODELS.items():

        try:
            base_pipeline = Pipeline([
                ('preprocessor', preprocessor),
                ('regressor', model)
            ])

            grid = GridSearchCV(
                estimator=base_pipeline,
                param_grid=params,
                scoring='r2',
                n_jobs=-1
            )
            grid.fit(X_train, y_train)

            y_pred_test = grid.predict(X_test)
            y_pred_train = grid.predict(X_train)

        except Exception as e:
            logger.exception(f"Error during training model {name}: {e}")
            continue  # пропускає модель, щоб не зупиняти весь пайплайн

        # Метрики
        def calculate_metrics(var, ground_truth, predictions):
            R2 = r2_score(ground_truth, predictions)
            MAE = mean_absolute_error(ground_truth, predictions)
            RMSE = np.sqrt(mean_squared_error(ground_truth, predictions))
            REL_MAE = MAE / np.mean(predictions) * 100

            return {
                'model': name,
                'dataset_var': var,
                'R2': round(R2, 2),
                'MAE': round(MAE, 1),
                'RMSE': round(RMSE, 1),
                'REL_MAE': round(REL_MAE, 1),
                **({'best_params': grid.best_params_} if var == 'test' else {})
            }

        train_results = calculate_metrics('train', y_train, y_pred_train)
        test_results = calculate_metrics('test', y_test, y_pred_test)

        results.extend([train_results, test_results])

        current_test_r2 = test_results['R2']
        if current_test_r2 > best_test_r2:
            best_test_r2 = current_test_r2
            best_model_info = {
                'name': name,
                'pipeline': grid.best_estimator_,
                'preprocessor': grid.best_estimator_.named_steps['preprocessor'],
                'regressor': grid.best_estimator_.named_steps['regressor'],
                'test_r2': current_test_r2,
                'best_params': grid.best_params_
            }

        logger.info(f"Training for model {name} completed successfully.")

    #  Збереження кращої моделі
    if save_best_model and best_model_info:
        try:
            joblib.dump(best_model_info['pipeline'], MODELS_DIR / "best_model.pkl")
            joblib.dump(best_model_info['preprocessor'], MODELS_DIR / 'preprocessor.pkl')

            metadata = {
                'model_name': best_model_info['name'],
                'test_R2': best_model_info['test_r2'],
                'params': best_model_info['best_params']
            }
            joblib.dump(metadata, MODELS_DIR / "model_metadata.pkl")
            logger.info(f"Best model and metadata saved to {MODELS_DIR}")
        except Exception as e:
            logger.exception(f"Failed to save model artifacts: {e}")
            raise

    if best_model_info:
        logger.info(
            f"Best model: {best_model_info['name']}, "
            f"R2 test: {best_model_info['test_r2']}"
        )
    else:
        logger.warning("No successful model training completed.")

    return best_model_info, results
