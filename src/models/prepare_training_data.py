import pandas as pd
from sklearn.model_selection import train_test_split

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OrdinalEncoder
from sklearn.compose import ColumnTransformer

from src.utils.paths import DATA_DIR
from src.scripts.encoders import TargetEncoder, FrequencyEncoder
from src.models.configs import regression_models


def preparing_and_split(df: pd.DataFrame,
                        target_feature: str,
                        train_size: int) -> dict:
    """
    Розділення даних на тестові і тренувальні вибірки
    """
    X = df.drop(columns=[target_feature])
    y = df[target_feature]

    # спліт даних + відразу скидання індексу через list comprehension
    X_train, X_test, y_train, y_test = [
        df.reset_index(drop=True) for df in train_test_split(X, y,
                                                             train_size=train_size,
                                                             shuffle=True,
                                                             random_state=25)
    ]

    return {
        'X_train': X_train,
        'X_test': X_test,
        'y_train': y_train,
        'y_test': y_test
    }

def preparing_features_for_training(data_bundle):
    """
    Створює препроцесор для різних типів ознак у train/test сплітах.
    """
    X_train = data_bundle['X_train']

    numeric_columns = X_train.select_dtypes(
        include=['float64','int64'])
    numeric_columns = list(numeric_columns)

    ordinal_features = ['english_level']
    frequency_features = ['job_category']
    target_features = ['seniority_level']

    level_order_english = [
        'Elementary',
        'Pre-Intermediate',
        'Intermediate',
        'Upper-Intermediate',
        'Advanced']

    preprocessor = ColumnTransformer([
        ('numeric_features_scaled', StandardScaler(), numeric_columns),

        # pipeline for proccesing TargetEncoder
        ('target_features_scaled', Pipeline([
            ('encoder', TargetEncoder()),
            ('scaler', StandardScaler())
        ]), target_features),

        # pipeline for processing FrequencyEncoder
        ('frequency_features_scaled', Pipeline([
            ('encoder', FrequencyEncoder()),
            ('scaler', StandardScaler())
        ]), frequency_features),

        # pipeline for processing OrdinalEncoder
        ('ordinal_features_scaled', Pipeline([
            ('encoder', OrdinalEncoder(
                categories=[level_order_english])),
            ('scaler', StandardScaler())
        ]), ordinal_features)
    ])

    return preprocessor
