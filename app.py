import streamlit as st
import requests
from datetime import datetime, date
import pandas as pd

st.title("TaxiFareModel front")
API_URL = st.secrets.get("SERVICE_URL", "https://taxifare.lewagon.ai/predict")

with st.form("inputs"):
    d = st.date_input("Pickup date", value=date.today())
    t = st.time_input("Pickup time", value=datetime.now().time())
    pickup_datetime = datetime.combine(d, t)

    pickup_lon = st.number_input("Pickup longitude", value=-73.985428, format="%.6f")
    pickup_lat = st.number_input("Pickup latitude", value=40.748817, format="%.6f")
    dropoff_lon = st.number_input("Dropoff longitude", value=-73.985000, format="%.6f")
    dropoff_lat = st.number_input("Dropoff latitude", value=40.758896, format="%.6f")
    passenger_count = st.number_input("Passenger count", min_value=1, max_value=8, value=1, step=1)
    submit = st.form_submit_button("Predict fare")

if submit:
    params = {
        "pickup_datetime": pickup_datetime.strftime("%Y-%m-%d %H:%M:%S"),
        "pickup_longitude": pickup_lon,
        "pickup_latitude": pickup_lat,
        "dropoff_longitude": dropoff_lon,
        "dropoff_latitude": dropoff_lat,
        "passenger_count": int(passenger_count),
    }
    try:
        r = requests.get(API_URL, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
        st.success(f"Predicted fare: {data.get('fare') or data.get('prediction') or data}")
    except Exception as e:
        st.error(f"API request failed: {e}")

# Optional: map preview
st.subheader("Map preview")
st.map(pd.DataFrame({"lat": [pickup_lat, dropoff_lat], "lon": [pickup_lon, dropoff_lon]}))
