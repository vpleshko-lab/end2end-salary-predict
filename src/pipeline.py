import pandas as pd
import numpy as np

from src.utils.paths import DATA_DIR
from src.data.preprocessing import select_and_rename_features, standardization_seniority_features
from src.data.preprocessing import drop_unspecified_positions, feature_balancing_category, preprocessing_feature_english
from src.data.preprocessing import cleaning_outliers_experience, cleaning_outliers_salary, export_dataframe
from src.data.feature_engineering import standardization_job_category

from src.models.prepare_training_data import preparing_and_split, preparing_features_for_training
from src.models.train_model import run_training

from src.utils.logger import get_logger

logger = get_logger(__name__)

def preprocces_data(input_csv, save_data: bool):
    """Блок для обробки даних"""

    # Stage 1: preprocessing and preparing data
    df = pd.read_csv(input_csv, encoding='cp1251')

    # preprocessing
    df = select_and_rename_features(df) # вибірка ключових фіч та коректні назви
    df = standardization_seniority_features(df) # стандартизація фічів
    df = drop_unspecified_positions(df)

    # feature engineering
    df = standardization_job_category(df)

    # preprocessing 2
    df = feature_balancing_category(df)
    df = preprocessing_feature_english(df)
    df = cleaning_outliers_experience(df)
    df = cleaning_outliers_salary(df)

    # sort and export

    df = export_dataframe(df, save_data)

    return df

def prepare_training_data(df,
                          target_column = str('salary_usd'),
                          train_size = float(0.75)):
    """Блок підготовки даних для подачі у тренування моделі"""

    data_bundle = preparing_and_split(df, target_column, train_size)
    train_preprocessor = preparing_features_for_training(data_bundle)

    return data_bundle, train_preprocessor

def start_training_model(data_bundle, preprocessor, save_model: bool):
    """Блок тренування моделі"""
    run_training(data_bundle, preprocessor, save_best_model=save_model)

def run_pipeline():
    logger.info("=== Start pipeline ===")

    try:
        logger.info('Loading data and preprocessing data from CSV...')
        df = preprocces_data(input_csv=DATA_DIR / 'raw/2025_june_raw.csv', save_data=False)
        logger.info(f'Preprocessing complete. Data shape: {df.shape}')

        logger.info('Stage 1: Splitting and feature preparation...')
        data_bundle, preprocessor = prepare_training_data(df=df, target_column='salary_usd', train_size=0.80)
        logger.info('Data split complete.')

        logger.info('Stage 2: model training')
        model_pipeline = start_training_model(data_bundle, preprocessor=preprocessor, save_model=True)
        logger.info('Training complete.')

    except Exception as e:
        logger.exception('Pipeline failed: {e}')
        raise e

    logger.info('=== Pipeline finished successfully ===')
    return model_pipeline
