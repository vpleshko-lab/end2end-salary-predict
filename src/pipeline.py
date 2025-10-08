import pandas as pd
import numpy as np

from src.utils.paths import DATA_DIR
from src.data.preprocessing import select_and_rename_features, standardization_seniority_features
from src.data.preprocessing import drop_unspecified_positions, feature_balancing_category, preprocessing_feature_english
from src.data.preprocessing import cleaning_outliers_experience, cleaning_outliers_salary, export_dataframe

from src.data.feature_engineering import standardization_job_category

def run_pipeline(input_csv, save: bool):
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
    df = export_dataframe(df, save=save)

    # Stage 2: preparing data for training


    # stage 3: training and export model

    return df
