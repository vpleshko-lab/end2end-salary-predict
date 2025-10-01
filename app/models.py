from enum import Enum
from pydantic import BaseModel

# input
class InputData(BaseModel):
    category: str
    title_group: str
    english_level: str
    it_experience_years: int

# output
class OutputData(BaseModel):
    prediction: int
