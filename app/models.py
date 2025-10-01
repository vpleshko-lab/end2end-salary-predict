from pydantic import BaseModel

class InputData(BaseModel):
    category: str
    title_group: str
    english_level: str
    it_experience_years: int

class OutputData(BaseModel):
    prediction: int
