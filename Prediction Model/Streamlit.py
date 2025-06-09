import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="Energy Load Predictor", layout="centered")
st.title("🔋 Germany Energy Load Predictor")

st.markdown("Enter forecast and time details to get predicted actual energy load.")

# Input form
with st.form("predict_form"):
    forecast_load = st.number_input("Forecast Load (MW)", min_value=0.0, step=10.0)
    dt = st.date_input("Date", datetime.now().date())
    hour = st.number_input("Hour (0-23)", min_value=0, max_value=23, value=datetime.now().hour)

    submitted = st.form_submit_button("Predict")

if submitted:
    payload = {
        "forecast_load": forecast_load,
        "hour": hour,
        "day": dt.day,
        "month": dt.month,
        "weekday": dt.weekday()
    }

    try:
        res = requests.post("http://127.0.0.1:8000/predict", json=payload)
        if res.status_code == 200:
            prediction = res.json()["predicted_load_actual"]
            st.success(f"🔮 Predicted Actual Load: **{prediction:,.2f} MW**")
        else:
            st.error(f"API error: {res.status_code}")
    except Exception as e:
        st.error(f"Failed to connect to API. Error: {e}")
