import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import OrdinalEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import KFold

from sklearn.base import BaseEstimator, RegressorMixin, clone
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.ensemble import RandomForestRegressor

class TargetEncoder(BaseEstimator, TransformerMixin):
    """
    Target Encoder з підтримкою cross-validation та smoothing для уникнення overfitting
    """

    def __init__(self, smoothing=1.0, cv=5, handle_unknown='value', fill_value=0):
        """
        Parameters:
        -----------
        smoothing : float, default=1.0
            Параметр регуляризації для smoothing
        cv : int, default=5
            Кількість fold'ів для cross-validation encoding
        handle_unknown : str, default='value'
            Як обробляти невідомі категорії ('value' або 'error')
        fill_value : float, default=0
            Значення для заповнення невідомих категорій
        """
        self.smoothing = smoothing
        self.cv = cv
        self.handle_unknown = handle_unknown
        self.fill_value = fill_value

    def fit(self, X, y=None):
        """
        Навчання encoder'а на тренувальних даних
        """
        if y is None:
            raise ValueError("Target encoder потребує цільової змінної y")

        X = self._validate_input(X)

        # Convert y to numpy array and ensure continuous indexing
        if hasattr(y, 'values'):
            y = y.values
        y = np.asarray(y)

        # Зберігаємо глобальне середнє
        self.global_mean_ = np.mean(y)

        # Для кожної колонки створюємо mapping
        self.encodings_ = {}

        for col_idx in range(X.shape[1]):
            col_data = X[:, col_idx]

            # Основний mapping (без CV)
            df = pd.DataFrame({'category': col_data, 'target': y})
            category_stats = df.groupby('category')['target'].agg(['mean', 'count']).reset_index()

            # Smoothing: (count * category_mean + smoothing * global_mean) / (count + smoothing)
            smoothed_means = (
                (category_stats['count'] * category_stats['mean'] +
                 self.smoothing * self.global_mean_) /
                (category_stats['count'] + self.smoothing)
            )

            basic_mapping = dict(zip(category_stats['category'], smoothed_means))

            # CV mapping для уникнення overfitting
            cv_mapping = self._create_cv_mapping(col_data, y)

            self.encodings_[col_idx] = {
                'basic': basic_mapping,
                'cv': cv_mapping
            }

        return self

    def _create_cv_mapping(self, categories, targets):
        """
        Створює CV-based mapping для уникнення data leakage
        """
        cv_mapping = {}
        kf = KFold(n_splits=self.cv, shuffle=True, random_state=42)

        # Ensure inputs are numpy arrays
        categories = np.asarray(categories)
        targets = np.asarray(targets)

        for train_idx, val_idx in kf.split(categories):
            # Use numpy indexing instead of pandas .iloc
            train_categories = categories[train_idx]
            train_targets = targets[train_idx]

            # Create train fold global mean
            fold_global_mean = np.mean(train_targets)

            # Створюємо mapping на train fold
            df_train = pd.DataFrame({'category': train_categories, 'target': train_targets})
            fold_stats = df_train.groupby('category')['target'].agg(['mean', 'count']).reset_index()

            fold_smoothed = (
                (fold_stats['count'] * fold_stats['mean'] +
                 self.smoothing * fold_global_mean) /
                (fold_stats['count'] + self.smoothing)
            )

            fold_mapping = dict(zip(fold_stats['category'], fold_smoothed))

            # Зберігаємо для validation індексів
            for idx in val_idx:
                category = categories[idx]
                cv_mapping[idx] = fold_mapping.get(category, fold_global_mean)

        return cv_mapping

    def transform(self, X, use_cv=False):
        """
        Трансформація даних

        Parameters:
        -----------
        use_cv : bool, default=False
            Використовувати CV mapping (тільки для тренувальних даних)
        """
        X = self._validate_input(X)
        result = np.zeros_like(X, dtype=float)

        for col_idx in range(X.shape[1]):
            mapping = self.encodings_[col_idx]['basic']

            for row_idx in range(X.shape[0]):
                category = X[row_idx, col_idx]

                if category in mapping:
                    result[row_idx, col_idx] = mapping[category]
                else:
                    if self.handle_unknown == 'value':
                        result[row_idx, col_idx] = self.fill_value
                    else:
                        raise ValueError(f"Невідома категорія: {category}")

        return result

    def fit_transform(self, X, y=None):
        """
        Fit та transform з використанням CV mapping
        """
        self.fit(X, y)
        # Для fit_transform використовуємо CV mapping
        return self._transform_with_cv(X)

    def _transform_with_cv(self, X):
        """
        Спеціальна трансформація з CV mapping для fit_transform
        """
        X = self._validate_input(X)
        result = np.zeros_like(X, dtype=float)

        for col_idx in range(X.shape[1]):
            cv_mapping = self.encodings_[col_idx]['cv']
            basic_mapping = self.encodings_[col_idx]['basic']

            for row_idx in range(X.shape[0]):
                if row_idx in cv_mapping:
                    result[row_idx, col_idx] = cv_mapping[row_idx]
                else:
                    category = X[row_idx, col_idx]
                    result[row_idx, col_idx] = basic_mapping.get(category, self.global_mean_)

        return result

    def _validate_input(self, X):
        """
        Валідація та конвертація вхідних даних
        """
        if hasattr(X, 'values'):  # pandas DataFrame/Series
            return X.values
        return np.asarray(X)


class FrequencyEncoder(BaseEstimator, TransformerMixin):
    """
    Frequency Encoder - замінює категорії на частоту їх появи
    """

    def __init__(self, handle_unknown='value', fill_value=0):
        """
        Parameters:
        -----------
        handle_unknown : str, default='value'
            Як обробляти невідомі категорії ('value' або 'error')
        fill_value : int, default=0
            Значення для заповнення невідомих категорій
        """
        self.handle_unknown = handle_unknown
        self.fill_value = fill_value

    def fit(self, X, y=None):
        """
        Навчання encoder'а - підрахунок частот
        """
        X = self._validate_input(X)

        self.frequency_maps_ = {}

        for col_idx in range(X.shape[1]):
            col_data = X[:, col_idx]
            # Підраховуємо частоти
            unique, counts = np.unique(col_data, return_counts=True)
            self.frequency_maps_[col_idx] = dict(zip(unique, counts))

        return self

    def transform(self, X):
        """
        Трансформація категорій у частоти
        """
        X = self._validate_input(X)
        result = np.zeros_like(X, dtype=int)

        for col_idx in range(X.shape[1]):
            freq_map = self.frequency_maps_[col_idx]

            for row_idx in range(X.shape[0]):
                category = X[row_idx, col_idx]

                if category in freq_map:
                    result[row_idx, col_idx] = freq_map[category]
                else:
                    if self.handle_unknown == 'value':
                        result[row_idx, col_idx] = self.fill_value
                    else:
                        raise ValueError(f"Невідома категорія: {category}")

        return result

    def _validate_input(self, X):
        """
        Валідація та конвертація вхідних даних
        """
        if hasattr(X, 'values'):  # pandas DataFrame/Series
            return X.values
        return np.asarray(X)


class TwoStageRegressor(BaseEstimator, RegressorMixin):
    def __init__(self, classifier=None, reg_low=None, reg_high=None, threshold=0.95):
        self.classifier = classifier if classifier else LogisticRegression()
        self.reg_low = reg_low if reg_low else LinearRegression()
        self.reg_high = reg_high if reg_high else RandomForestRegressor()
        self.threshold = threshold

    def fit(self, X, y):
        # Поріг для "топових" зарплат
        cutoff = np.quantile(y, self.threshold)
        self.is_high = (y >= cutoff).astype(int)

        # Навчання класифікатора
        self.classifier_ = clone(self.classifier)
        self.classifier_.fit(X, self.is_high)

        # Навчання регресій
        self.reg_low_ = clone(self.reg_low)
        self.reg_high_ = clone(self.reg_high)

        self.reg_low_.fit(X[self.is_high == 0], y[self.is_high == 0])
        self.reg_high_.fit(X[self.is_high == 1], y[self.is_high == 1])
        return self

    def predict(self, X):
        # Ймовірності належності до "топу"
        is_high_pred = self.classifier_.predict(X)

        # Дві різні регресії
        y_pred_low = self.reg_low_.predict(X)
        y_pred_high = self.reg_high_.predict(X)

        # Комбінуємо
        return np.where(is_high_pred == 1, y_pred_high, y_pred_low)
