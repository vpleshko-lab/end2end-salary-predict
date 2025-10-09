import joblib
import pandas as pd
import json

from src.utils.paths import DATA_DIR, MODELS_DIR
from src.utils.logger import get_logger

logger = get_logger(__name__)

def exctract_allowed_values(df: pd.DataFrame):
    """
    Формування JSON конфігу для allowed_values.json
    """
    try:
        job_category = df['job_category'].unique().tolist()
        seniority_level = df['seniority_level'].unique().tolist()
        english_level = df['english_level'].unique().tolist()

    except FileNotFoundError as e:
        logger.error(f'Data configs not found {e}')
        raise

    except Exception as e:
        logger.exception(f"Unexpected error while building configs (allowed_vals): {e}.")
        raise

    else:
        logger.info("Allowed values successfully exctracted.")
        return {
            'job_category': job_category,
            'seniority_level': seniority_level,
            'english_level': english_level
        }

def dump_allowed_values(values_bundle: dict,
                        path: str = 'configs/allowed_values.json'):
    """Збереження конфігу у .JSON форматі за шляхом"""
    try:
        with open(path, 'w') as f:
            json.dump(values_bundle, f, indent=2)
            logger.info(f'Allowed values succesfully saved to {path}')
    except Exception as e:
        logger.exception(f'Error saving allowed values: {e}')
        raise

def exctract_features_configs(df: pd.DataFrame):
    """Формування JSON конфігу для column_features.json"""
    result = {}
    sample = df.iloc[1]
    sample = sample.drop('salary_usd')

    try:
        for k, v in sample.items():
            val = v[0] if isinstance(v, list) else v
            if isinstance(val, (int, float)):
                result[k] = 'numeric'
            elif isinstance(val, (str, bool)):
                result[k] = 'categorical'
    except Exception as e:
        logger.exception(f'Unexpected error while building configs for feature cols: {e}.')
        raise
    else:
        logger.info('Columns features configs successfully exctracted.')
        return {
            'columns': list(result.keys()),
            'types': result
        }
def dump_features_configs(values_bundle: dict,
                         path: str = 'configs/column_features.json'):
    """Збереження конфігу колонок у .JSON форматі за шляхом """
    try:
        with open(path, 'w') as f:
            json.dump(values_bundle, f, indent=2)
            logger.info(f'Column features configs succesfully saved to {path}')
    except Exception as e:
        logger.exception(f'Error saving features columns configs: {e}')
        raise

def build_configs(df: pd.DataFrame):

    logger.info('Building configs')
    # allowed values.json
    allowed_values = exctract_allowed_values(df)
    dump_allowed_values(allowed_values)

    # feature columns.json
    feature_columns_values = exctract_features_configs(df)
    dump_features_configs(feature_columns_values)
