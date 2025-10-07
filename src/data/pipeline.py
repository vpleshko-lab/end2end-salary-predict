import pandas as pd
import numpy as np

from src.utils.paths import DATA_DIR
from src.data.preprocessing import select_and_rename_features


def run_pipeline(input_csv, output_csv=None):
    df = pd.read_csv(input_csv, encoding='cp1251')
    df = select_and_rename_features(df)

    return df
