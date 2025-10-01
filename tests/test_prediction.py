import pandas as pd
from src.scripts.prediction import SalaryPredictor

model = SalaryPredictor()

def test_single_output():

    test_data = {'category': 'Analyst',
                 'title_group': 'Mid-level',
                 'english_level': 'Pre-Intermediate',
                 'it_experience_years': 4.0}

    test_data = pd.DataFrame([test_data])

    prediction = model.predict(test_data)

    print(f'Predicted value = {prediction}')

test_single_output()
