import pandas as pd

from src.utils.paths import DATA_DIR
from src.data.pipeline import run_pipeline

def test_pipeline_flow():
    result = run_pipeline(input_csv= DATA_DIR / 'raw/2025_june_raw.csv')
    result.info()

test_pipeline_flow()
