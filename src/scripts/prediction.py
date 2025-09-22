import joblib # type: ignore
import pandas as pd
import numpy as np
from typing import Dict, List
import logging
from pathlib import Path
import json
from datetime import datetime, UTC
import os

from src.utils.paths import DATA_DIR, MODELS_DIR, LOGS_DIR

logging.basicConfig(level=logging.INFO,
                    format= "%(asctime)s | %(levelname)s | %(name)s | %(message)s")
logger = logging.getLogger(__name__)

class SalaryPredictor:
    def __init__(self, model_path = MODELS_DIR/"best_model.pkl"):
        self.model_path = model_path
        self.model = None
        self.metadata = None
        self.config_values = None
        self.config_features = None
        self.feature_cols = None
        self.logs_path = LOGS_DIR / "prediction_log.csv"

        # load
        try:
            # model and metadata
            self.model = joblib.load(model_path)
            self.metadata = joblib.load(MODELS_DIR/"model_metadata.pkl")

            # configs and additional info about them
            self.config_values = json.load(open('configs/allowed_values.json'))
            self.config_features = json.load(open('configs/column_features.json'))
            self.feature_cols = self.config_features['columns']
            logging.info("Model, metadata and configs succesfully loaded.")
        except FileNotFoundError:
            logging.error(f"Required file not found: {e.filename}")
            raise
        except Exception as e:
            logging.error(f"Error while loading model/metadata: {e}")
            raise

    def validate_input(self, input_data):
        # check for DataFrame type
        if not isinstance(input_data, pd.DataFrame):
            raise ValueError("Input data must be a pandas DataFrame")

        # availability check
        missing_cols = [c for c in self.feature_cols if c not in input_data.columns]
        if missing_cols:
            raise ValueError(f'Missing required columns: {missing_cols}')

        # missing values check
        if input_data[self.feature_cols].isnull().any().any():
            raise ValueError(f'Missing values detected in input data')

        for col, col_type in self.config_features['types'].items():
            if col_type == 'categorical': # перевіряємо тільки категоріальні
                allowed = self.config_values.get(col, []) # список дозволених значень для цієї колонки
                invalid_mask = ~input_data[col].isin(allowed) # створення маски, True там де значення не входить у список

                # якщо є хоча б одне невалідне значення
                if invalid_mask.any():
                    invalid_vals = input_data.loc[invalid_mask, col].tolist()
                    # викидаємо помилку з поясненням
                    raise ValueError(
                        f"Invalid values in column '{col}': {invalid_vals}. "
                        f"Allowed values are: {allowed}"
                    )

        return input_data

    def log_prediction_csv(self, input_data: pd.DataFrame, preds: np.ndarray):
        """Базове логування передбачень """
        log_df = input_data.copy()
        log_df['prediction'] = preds
        log_df['timestamp'] = datetime.now(UTC).isoformat()
        log_df.to_csv(self.logs_path, mode='a', header=not os.path.exists(self.logs_path), index=False)


    def predict(self, input_data):
        """
        input data: pd.DataFrame, вже підготовлені дані у форматі в якому очікує модель
        """
        X_valid = self.validate_input(input_data)
        result = self.model.predict(X_valid[self.feature_cols])
        # checking for compliance with the prediction format
        if not isinstance(result, (list, np.ndarray)):
            raise TypeError("Model predict returned unexpected type")

        result = np.round(result).astype(int)
        result = np.clip(result, 0, None) # limits of predict
        self.log_prediction_csv(input_data, preds=result)

        return result

test_input = {'category': 'Analyst',
              'title_group': 'Mid-level',
              'english_level': 'Pre-Intermediate',
              'it_experience_years': 4.0}
test_df = pd.DataFrame([test_input])

predictor = SalaryPredictor()

prediction = predictor.predict(test_df)
print(prediction)
