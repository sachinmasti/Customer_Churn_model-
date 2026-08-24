from fastapi import FastAPI,HTTPException
from schemas.schema import CustomerChurn
import joblib
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
model_path = BASE_DIR/'model_'/'customer_churn_model.joblib'

# print(model_path)
app = FastAPI()


@app.get('/home')
def home():
    return {'massage':'this is a home 😎'}
@app.get('/health')
def health():
    return {'massage':'health is api is best 🫶🏼'}

@app.get('/model_load')
async def model_health():
    try:

        print("MODEL PATH:", model_path)
        print("EXISTS:", model_path.exists())
        model = joblib.load(model_path)
        if model:
            return {
                'message': 'model is loaded successfully ✈️'
            }
    except FileNotFoundError:
        return {
            'message': 'model is not loaded 🤮'
        }