from fastapi import FastAPI,HTTPException
from fastapi.responses import HTMLResponse
from schemas.schema import CustomerChurn
import joblib
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
model_path = BASE_DIR/'model_'/'customer_churn_model.joblib'

model_load = joblib.load(model_path)
app = FastAPI()


@app.get('/home',response_class=HTMLResponse)
def home():
    return {'massage':'this is a home 😎'}

@app.get('/health')
def health():
    return {'massage':'api is working 🌿'}

@app.get('/model_load')
async def model_health():
    try:

        model = joblib.load(model_path)
        if model:
            return {
                'message': 'model is loaded successfully ✈️'
            }
    except FileNotFoundError:
        return {
            'message': 'model is not loaded 🤮'
        }

@app.post('/predict')
def predict(customer:CustomerChurn):
    data = customer.model_dump(exclude={'email','last_contact_date'})
    df = pd.DataFrame([data])

    prediction = model_load.predict_proba(df)[0]

    yes_probability = prediction[list(model_load.classes_).index('yes')]

    label = 'yes' if yes_probability >= 0.465850 else 'no'

    return {
        'label': label,
        'confidence': round(float(yes_probability if label == 'yes' else 1 - yes_probability), 4)
    }