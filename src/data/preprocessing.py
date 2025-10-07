import pandas as pd
import numpy as np

from src.utils.paths import DATA_DIR

from src.data.configs.seniority_mapping import SENIORITY_LEVEL_MAPPING
from src.data.configs.experience_mapping import EXPERIENCE_RANGES
from src.data.configs.salary_mapping import SALARY_RANGES

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
    return df

def drop_unspecified_positions(df: pd.DataFrame) -> pd.DataFrame:
    """
    Видалення неінформативних значень у колонці 'Seniority Level'
    """
    indices_drop = df[df['seniority_level'] == 'Not Specified'].index
    df.drop(indices_drop, inplace=True)

    return df

def feature_balancing_category(df: pd.DataFrame,
                      se_scale: int = 100,
                      qa_scale: int = 600,
                      random_state: int = 25
                      ) -> pd.DataFrame:
    """
    Балансування категорії 'job_category' шляхом стратифікованого семплінгу
    для Software Engineering та QA & Testing відносно 'seniority_level' і 'salary_usd'.
    Працює без FutureWarning у старих версіях pandas.
    """

    se_df = df[df['job_category'] == 'Software Engineering']
    qa_df = df[df['job_category'] == 'QA & Testing']
    other_df = df[~df['job_category'].isin(['Software Engineering', 'QA & Testing'])]

    # Стратифікований семплінг Software Engineering
    se_sampled = pd.concat([
        x.sample(min(len(x), max(1, int(se_scale * len(x) / len(se_df)))), random_state=random_state)
        for _, x in se_df.groupby(['seniority_level', 'salary_usd'])
    ], ignore_index=True)

    # Стратифікований семплінг QA & Testing
    qa_sampled = pd.concat([
        x.sample(min(len(x), max(1, int(qa_scale * len(x) / len(qa_df)))), random_state=random_state)
        for _, x in qa_df.groupby(['seniority_level', 'salary_usd'])
    ], ignore_index=True)

    # Об’єднання всіх груп
    balanced_df = pd.concat([se_sampled, qa_sampled, other_df], ignore_index=True)

    return balanced_df

def preprocessing_feature_english(df: pd.DataFrame) -> pd.DataFrame:
    """Очищення малозначимих фіч (мала к-сть + нерелевантний клас)"""

    indices_english = df[df['english_level'] == 'Не знаю взагалі'].index
    df.drop(indices_english, inplace=True)

    return df

def cleaning_outliers_experience(df: pd.DataFrame) -> pd.DataFrame:
    """Очищення фіч 'experience_years' базуючись на 'seniority_level' """
    df_copy = df.copy()
    df_copy['is_outlier'] = False
    df_copy['outlier_score'] = float(0.0)

    def set_outlier_scores():
        for index, row in df_copy.iterrows():
            seniority = row['seniority_level']
            experience = row['experience_years']

            score = 0.0

            if seniority in EXPERIENCE_RANGES:
                rules = EXPERIENCE_RANGES[seniority]

                # змінні для діапазонів
                critical_outlier = rules['critical_outlier']
                outlier_threshold = rules['outlier_threshold']
                acceptable_threshold = rules['acceptable']
                typical_range = rules['typical_range']

                if 'max_outlier' in rules and experience > rules['max_outlier']:
                    score = 1.0
                elif typical_range[0] <= experience <= typical_range[1]:
                    score = 0.0
                elif acceptable_threshold[0] <= experience <= acceptable_threshold[1]:
                    score = 0.25
                elif experience < critical_outlier:
                    score = 0.75
                elif experience < outlier_threshold:
                    score = 0.50
                else:
                    score = 1.0

            if score >= 0.5:
                df_copy.at[index, 'is_outlier'] = True
            df_copy.at[index, 'outlier_score'] = score

            # залишаю лише дані без викидів
            df_normal = df_copy[df_copy['is_outlier'] == False]
            df_normal = df_normal.drop(columns=['is_outlier', 'outlier_score'])

        return df_normal

    df_without_exp_outliers = set_outlier_scores()

    return df_without_exp_outliers

def cleaning_outliers_salary(df: pd.DataFrame) -> pd.DataFrame:
    """Очищення фіч 'salary_usd' базуючись на 'seniority_level' """

    df_copy = df.copy()
    df_copy['is_outlier'] = False
    df_copy['salary_score'] = float(0.0)

    def set_outlier_scores():

        for index, row in df_copy.iterrows():
            seniority = row['seniority_level']
            salary = row['salary_usd']

            score = float(0.0)

            if seniority in SALARY_RANGES:
                rules = SALARY_RANGES[seniority]

                acceptable_threshold = rules['acceptable']
                typical_range = rules['typical_range']
                outlier_threshold = rules['outlier_range']
                critical_range = rules['critical_range']

                if typical_range[0] <= salary <= typical_range[1]:
                    score = 0.0
                elif acceptable_threshold[0] <= salary <= acceptable_threshold[1]:
                    score = 0.25
                elif outlier_threshold[0] <= salary <= outlier_threshold[1]:
                    score = 0.75
                elif critical_range[0] <= salary <= critical_range[1]:
                    score = 1.0
                else:
                    score = 1.0

            if score >= 0.5:
                df_copy.at[index, 'is_outlier'] = True
            df_copy.at[index, 'salary_score'] = score

            # залишаю лише дані без викидів
            df_normal = df_copy[df_copy['is_outlier'] == False]
            df_normal = df_normal.drop(columns=['is_outlier', 'salary_score']).reset_index(drop=True)

        return df_normal

    df_with_salary_outliers = set_outlier_scores()

    return df_with_salary_outliers

def export_dataframe(df: pd.DataFrame,
                     save: bool) -> pd.DataFrame:
    """Сортує фічі у визначеному порядку та (опціонально) зберігає датафрейм у CSV."""

    def sort_features(df: pd.DataFrame) -> pd.DataFrame:
        """Впорядкування фічі у необхідному порядку"""

        cols = ['job_category', 'seniority_level', 'english_level', 'experience_years', 'salary_usd']
        return df[cols].copy()

    df = sort_features(df)

    if save:
        path = DATA_DIR / "processed/model_input_df.csv"
        df.to_csv(path, index=False)

    return df
