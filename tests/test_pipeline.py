import pandas as pd

from src.utils.paths import DATA_DIR
from src.data.pipeline import run_pipeline

def test_pipeline_flow():
    df = run_pipeline(input_csv= DATA_DIR / 'raw/2025_june_raw.csv',
                      save=False)

    assert isinstance(df, pd.DataFrame)
    assert not df.isna().values.any(), "DataFrame містить NaN"
    assert (DATA_DIR / "processed/model_input_df.csv").exists()
