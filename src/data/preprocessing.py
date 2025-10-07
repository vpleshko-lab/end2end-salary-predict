import pandas as pd
import numpy as np

def select_and_rename_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Обирає ключові колонки з сирого датасету,
    перейменовує їх у стандартні назви і видаляє NaN по цільовій зміні.
    """

    selected_features = {
    'ЗАРПЛАТА / СУМАРНИЙ ДОХІД в IT у $$$ за місяць, лише ставка \nЧИСТИМИ - після сплати податків': 'salary_usd',
    'Тайтл': 'position_level',
    'Категорія': 'category',
    'Почніть вводити і оберіть вашу ОСНОВНУ посаду зі списку': 'position',
    'Знання англійської мови': 'english_level',
    'Загальний стаж роботи за нинішньою ІТ-спеціальністю': 'it_experience_years',
}
    df_selected = df[list(selected_features.keys())].copy()
    df_selected.rename(columns=selected_features, inplace=True)
    df_selected = df_selected.dropna(subset=['salary_usd'])

    return df_selected
