FROM python:3.12-slim

WORKDIR /salary-predictor-docker

COPY . /salary-predictor-docker

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt
