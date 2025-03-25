# main.py
import streamlit as st
import joblib
import numpy as np

# 1. Cache loading of scaler & model so we don't re-load them on every widget change
@st.cache_resource
def load_resources():
    # Load the scaler you saved during training (e.g., StandardScaler)
    loaded_scaler = joblib.load("scaler.pkl")
    # Load the trained model (Random Forest)
    loaded_model = joblib.load("housing_model.pkl")
    return loaded_scaler, loaded_model

scaler, model = load_resources()

# 2. App title
st.title("Housing Price Prediction App")

# 3. Use a form to collect all inputs
with st.form("prediction_form"):
    # Numeric inputs (the same columns you scaled during training)
    longitude = st.number_input("Longitude", value=-122.23)
    latitude = st.number_input("Latitude", value=37.88)
    housing_median_age = st.number_input("Housing Median Age", value=41.0)
    total_rooms = st.number_input("Total Rooms", value=880)
    total_bedrooms = st.number_input("Total Bedrooms", value=129)
    population = st.number_input("Population", value=322)
    households = st.number_input("Households", value=126)
    median_income = st.number_input("Median Income", value=8.3252)

    # Ocean proximity (5 categories, matching your OneHotEncoder from training)
    ocean_category = st.selectbox(
        "Ocean Proximity",
        ["<1H OCEAN", "INLAND", "ISLAND", "NEAR BAY", "NEAR OCEAN"]
    )

    # The "Submit" button in the form
    submitted = st.form_submit_button("Predict")

# 4. Only run prediction if user clicks "Predict"
if submitted:
    # A) Prepare numeric features in the same order used in training
    numeric_array = np.array([
        longitude,
        latitude,
        housing_median_age,
        total_rooms,
        total_bedrooms,
        population,
        households,
        median_income
    ]).reshape(1, -1)

    # B) Scale the numeric features with the same scaler
    numeric_scaled = scaler.transform(numeric_array)

    # C) One-hot encode ocean proximity (5 columns, matching training order)
    ohe_array = np.array([
        int(ocean_category == "<1H OCEAN"),
        int(ocean_category == "INLAND"),
        int(ocean_category == "ISLAND"),
        int(ocean_category == "NEAR BAY"),
        int(ocean_category == "NEAR OCEAN")
    ]).reshape(1, -1)

    # D) Concatenate scaled numeric + one-hot
    final_input = np.concatenate([numeric_scaled, ohe_array], axis=1)

    # E) Make prediction
    prediction = model.predict(final_input)[0]

    # Debug: Uncomment this line if you need to see the input array,
    # otherwise leave it commented out so the user doesn't see it.
    # st.write("final_input:", final_input)

    # F) Display the result
    st.success(f"Predicted Median House Value: ${prediction:,.2f}")
