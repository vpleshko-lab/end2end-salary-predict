from enum import Enum
from pydantic import BaseModel

# input
class InputData(BaseModel):
    job_category: str
    seniority_level: str
    english_level: str
    experience_years: int

# output
class OutputData(BaseModel):
    prediction: int
