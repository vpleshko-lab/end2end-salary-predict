import pandas as pd
from sklearn.model_selection import train_test_split

from src.utils.paths import DATA_DIR


def preparing_and_split(df: pd.DataFrame,
                        target_feature: str,
                        train_size: int):
    """
    Розділення даних на тестові і тренувальні вибірки
    """
    X = df.drop(columns=[target_feature])
    y = df[target_feature]

    # split
    X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                        train_size=train_size,
                                                        random_state=25,
                                                        shuffle=True)

    return X_train, X_test, y_train, y_test
