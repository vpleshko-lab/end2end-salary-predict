from fastapi import FastAPI
import pandas as pd
from app.schemas import InputData, OutputData
from models.salary_predictor import SalaryPredictor

app = FastAPI(title="IT Salary Prediction API")
model = SalaryPredictor()

@app.post("/predict", response_model=OutputData)
def predict(input_data: InputData):
    input_data = pd.DataFrame([input_data.dict()])
    predicted_value = model.predict(input_data)[0]

    return OutputData(prediction=predicted_value)
