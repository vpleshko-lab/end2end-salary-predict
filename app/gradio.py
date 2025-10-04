import gradio as gr
import pandas as pd
import json

from src.scripts.prediction import SalaryPredictor

model = SalaryPredictor()

with open('configs/allowed_values.json', 'r') as json_file:
    json_data = json.load(json_file)

    category_data = list(json_data['job_category'])
    title_data = list(json_data['seniority_level'])
    english_level_data = list(json_data['english_level'])

def gradio_predict(job_category: str,
                   seniority_level: str,
                   english_level: str,
                   experience_years: int):

    input_data = {'job_category': job_category,
                  'seniority_level': seniority_level,
                  'english_level': english_level,
                  'experience_years': experience_years}

    input_data = pd.DataFrame([input_data])
    prediction = model.predict(input_data)[0]

    return prediction

with gr.Blocks(title='Machine Learning Project: IT Salary prediction') as demo:
    gr.Markdown(
        """
        Salary Prediction App\n
        Enter the details below to get a salary prediction.
        """
    )

    with gr.Row():
        with gr.Column(scale=1):
            category_in = gr.Dropdown(
                label='Job Category',
                choices=category_data,
                info='Enter professional category'
            )
            title_in = gr.Dropdown(
                label='Position level',
                choices=title_data,
                info='Enter position level'
            )
            english_in = gr.Dropdown(
                label='English level',
                choices=english_level_data,
                info='Enter your english level'
            )
            experience_in = gr.Number(
                label='Experience years',
                info='Enter experience years'
            )

            submit_btn = gr.Button("Predict Salary", variant='primary')

        with gr.Column(scale=1):
            result_out = gr.Number(label='Predicted salary (USD)', precision=0)

    submit_btn.click(
        fn=gradio_predict,
        inputs=[category_in, title_in, english_in, experience_in],
        outputs=result_out
    )

demo.launch()
