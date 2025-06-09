from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

# Load model
model = joblib.load("model.pkl")

app = FastAPI()

# Input schema
class LoadInput(BaseModel):
    forecast_load: float
    hour: int
    day: int
    month: int
    weekday: int

@app.post("/predict")
def predict_load(data: LoadInput):
    X = np.array([[data.forecast_load, data.hour, data.day, data.month, data.weekday]])
    prediction = model.predict(X)[0]
    return {"predicted_load_actual": round(prediction, 2)}
