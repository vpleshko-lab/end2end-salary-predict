import pandas as pd

from src.utils.paths import DATA_DIR
from src.data.preprocessing import (
    select_and_rename_features,
    standardization_seniority_features,
    drop_unspecified_positions,
    feature_balancing_category,
    preprocessing_feature_english,
    cleaning_outliers_experience,
    cleaning_outliers_salary,
    export_dataframe,
)
from src.data.feature_engineering import standardization_job_category

from src.models.prepare_training_data import (
    preparing_and_split,
    preparing_features_for_training,
)
from src.models.train_model import run_training
from src.models.exctract_configs import build_configs
from src.utils.logger import get_logger

logger = get_logger(__name__)

# ---------- препроцессинг та підготовка даних ----------
def preprocces_data(input_csv, save_data: bool):
    """Обробка сирих даних (preprocessing + feature engineering)"""

    # load data
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

# ---------- підготовка даних ----------
def prepare_training_data(df,
                          target_column = str('salary_usd'),
                          train_size = float(0.75)):
    """Підготовка даних для тренування"""

    data_bundle = preparing_and_split(df, target_column, train_size)
    train_preprocessor = preparing_features_for_training(data_bundle)

    return data_bundle, train_preprocessor

# ---------- тренування моделі ----------
def start_training_model(data_bundle, preprocessor, save_model: bool):
    """Блок тренування моделі"""
    run_training(data_bundle, preprocessor, save_best_model=save_model)

# ---------- підготовка та побудова конфігів ----------
def preparing_and_exporting_configs(df):
    build_configs(df)

# ---------- main pipeline function ----------
def main(save_data: bool = False,
                 save_model: bool = False,
                 save_configs: bool = False
                 ):
    logger.info("=== Start pipeline ===")

    try:
        logger.info('Loading data and preprocessing data from CSV...')
        df = preprocces_data(input_csv=DATA_DIR / 'raw/2025_june_raw.csv',
                             save_data=save_data)
        logger.info(f'Preprocessing complete. Data shape: {df.shape}')

        logger.info('Stage 1: Splitting and feature preparation...')
        data_bundle, preprocessor = prepare_training_data(df=df,
                                                          target_column='salary_usd',
                                                          train_size=0.80)
        logger.info('Data split complete.')

        logger.info('Stage 2: model training')
        model_pipeline = start_training_model(data_bundle,
                                              preprocessor=preprocessor,
                                              save_model=save_model)
        logger.info('Training complete.')

        if save_configs:

            logger.info('Stage 4: bulding and saving configs by dataset')
            preparing_and_exporting_configs(df=df)
            logger.info('Configs successfully exctracted.')


    except Exception as e:
        logger.exception('Pipeline failed: {e}')
        raise e

    logger.info('=== Pipeline finished successfully ===')
    return model_pipeline

# ---------- Точка входу ----------
if __name__ == '__main__':
    try:
        main(save_data=True,
             save_model=True,
             save_configs=True)
    except Exception as e:
        logger.exception(f'Pipeline failed with error')
        raise
