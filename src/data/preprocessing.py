import pandas as pd
import numpy as np

from src.data.configs.seniority_mapping import SENIORITY_LEVEL_MAPPING

def select_and_rename_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Обирає ключові колонки з сирого датасету,
    перейменовує їх у стандартні назви і видаляє NaN по цільовій зміні.
    """

    selected_features = {
    'ЗАРПЛАТА / СУМАРНИЙ ДОХІД в IT у $$$ за місяць, лише ставка \nЧИСТИМИ - після сплати податків': 'salary_usd',
    'Тайтл': 'seniority_level',
    'Почніть вводити і оберіть вашу ОСНОВНУ посаду зі списку': 'position',
    'Знання англійської мови': 'english_level',
    'Загальний стаж роботи за нинішньою ІТ-спеціальністю': 'experience_years',
}
    df_selected = df[list(selected_features.keys())].copy()
    df_selected.rename(columns=selected_features, inplace=True)
    df_selected = df_selected.dropna(subset=['salary_usd'])

    return df_selected

def standardization_seniority_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Уніфікація значень для рівнів експертності
    """
    df['seniority_level'] = df['seniority_level'].map(SENIORITY_LEVEL_MAPPING)
