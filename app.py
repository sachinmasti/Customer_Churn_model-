from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from src.schema import CustomerChurn
import joblib
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
model_path = BASE_DIR / 'models' / 'customer_churn_model.joblib'

model_load = joblib.load(model_path)
app = FastAPI()


@app.get('/')
def root():
    return RedirectResponse(url='/home')


@app.get('/home', response_class=HTMLResponse)
def home():
    return """
    <html>
        <head>
            <title>Customer Churn Prediction API</title>
        </head>
        <body style="font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; background-color: #f4f6f9; color: #333;">
            <div style="max-width: 600px; margin: auto; padding: 20px; background: #fff; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                <h1 style="color: #0056b3;">Customer Churn Prediction API</h1>
                <p>Welcome to the home page of the Customer Churn Prediction Service. The API is active and ready to receive requests.</p>
                <hr style="border: 0; border-top: 1px solid #ccc; margin: 20px 0;">
                <h3>Available Endpoints:</h3>
                <ul>
                    <li><strong>Home:</strong> <a href="/home" style="color: #0056b3;">/home</a> (HTML Welcome)</li>
                    <li><strong>Health Check:</strong> <a href="/health" style="color: #0056b3;">/health</a> (JSON Status)</li>
                    <li><strong>Model Load Status:</strong> <a href="/model_load" style="color: #0056b3;">/model_load</a> (JSON Status)</li>
                    <li><strong>API Documentation:</strong> <a href="/docs" style="color: #0056b3;">/docs</a> (Swagger UI)</li>
                </ul>
            </div>
        </body>
    </html>
    """

@app.get('/health')
def health():
    return {'message': 'API service is active and operational.'}

@app.get('/model_load')
async def model_health():
    try:
        model = joblib.load(model_path)
        if model:
            return {
                'message': 'Machine learning model has been loaded successfully.'
            }
    except FileNotFoundError:
        return {
            'message': 'Failed to load model. The model file was not found.'
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