import pandas as pd

from src.data.configs.categories_mapping import JOB_CATEGORY_MAPPING

def standardization_job_category(df: pd.DataFrame) -> pd.DataFrame:
    """
    Уніфікація значень, використовуючи колонку position,
    після чого створення відповідної категоріальної колонки
    """
    df['job_category'] = df['position'].map(JOB_CATEGORY_MAPPING)
    df.drop(columns=['position'], inplace=True)

    return df
