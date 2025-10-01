from pydantic import BaseModel

class InputData(BaseModel):
    category: str
    level: str
    english: str
    experience_years: int

class OutputData(BaseModel):
    prediction: int
