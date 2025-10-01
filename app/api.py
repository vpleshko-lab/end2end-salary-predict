from fastapi import FastAPI
import pandas as pd
from app.models import InputData, OutputData
from src.scripts.prediction import SalaryPredictor

app = FastAPI()
model = SalaryPredictor()

@app.post("/predict", response_model=OutputData)
def predict(input_data: InputData):
    input_data = pd.DataFrame([input_data.dict()])
    predicted_value = model.predict(input_data)[0]

    return OutputData(prediction=predicted_value)
