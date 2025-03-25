import streamlit as st
import numpy as np
import pandas as pd
import os
from pyspark.sql import SparkSession, Row
from pyspark.ml import PipelineModel

# ----------------------------------------------------------------------------
# 1) Initialize a local SparkSession
# ----------------------------------------------------------------------------
spark = SparkSession.builder \
    .appName("Housing Price Prediction") \
    .master("local[*]") \
    .getOrCreate()

# ----------------------------------------------------------------------------
# 2) Load your saved Spark ML pipeline model
# ----------------------------------------------------------------------------
MODEL_PATH = "housing_best_gbt"  # Folder with metadata/stages
model = PipelineModel.load(MODEL_PATH)

# ----------------------------------------------------------------------------
# 3) Streamlit App Title
# ----------------------------------------------------------------------------
st.title("Housing Price Prediction App (PySpark)")

# ----------------------------------------------------------------------------
# SECTION A: Single-Record Prediction
# ----------------------------------------------------------------------------
st.header("Single Record Prediction")
st.write("Enter the details for one property:")

# Define input fields for your features
longitude = st.number_input("Longitude", value=-122.23)
latitude = st.number_input("Latitude", value=37.88)
housing_median_age = st.number_input("Housing Median Age", value=41.0)
total_rooms = st.number_input("Total Rooms", value=880)
total_bedrooms = st.number_input("Total Bedrooms", value=129)
population = st.number_input("Population", value=322)
households = st.number_input("Households", value=126)
median_income = st.number_input("Median Income", value=8.3252)
ocean_category = st.selectbox(
    "Ocean Proximity",
    ["<1H OCEAN", "INLAND", "ISLAND", "NEAR BAY", "NEAR OCEAN"]
)

# Single-record prediction logic
if st.button("Predict Single Record"):
    input_data = {
        "longitude": float(longitude),
        "latitude": float(latitude),
        "housing_median_age": float(housing_median_age),
        "total_rooms": float(total_rooms),
        "total_bedrooms": float(total_bedrooms),
        "population": float(population),
        "households": float(households),
        "median_income": float(median_income),
        "ocean_proximity": ocean_category
    }

    # Create a Spark DataFrame with one row
    input_df = spark.createDataFrame([Row(**input_data)])
    # Run the model
    prediction_df = model.transform(input_df)
    # Extract the prediction
    prediction_value = prediction_df.select("prediction").collect()[0]["prediction"]
    st.success(f"Predicted Median House Value: ${prediction_value:,.2f}")

# ----------------------------------------------------------------------------
# SECTION B: Batch Predictions (CSV or Excel)
# ----------------------------------------------------------------------------
st.header("Batch Predictions")
st.write("Upload a **CSV** or **Excel (.xlsx)** file with multiple rows to get predictions:")

uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx"])
if uploaded_file is not None:
    # 1) Read file into Pandas
    file_extension = os.path.splitext(uploaded_file.name)[1].lower()
    try:
        if file_extension == ".csv":
            df = pd.read_csv(uploaded_file)
        elif file_extension == ".xlsx":
            df = pd.read_excel(uploaded_file, engine="openpyxl")
        else:
            st.error("Unsupported file format. Please upload CSV or XLSX.")
            st.stop()
    except Exception as e:
        st.error(f"Error reading file: {e}")
        st.stop()

    # 2) Drop NaNs in essential numeric columns
    required_columns = [
        "longitude", "latitude", "housing_median_age",
        "total_rooms", "total_bedrooms", "population",
        "households", "median_income"
    ]
    df = df.dropna(subset=required_columns)

    # 3) Convert cleaned Pandas -> Spark
    try:
        spark_df = spark.createDataFrame(df)
    except Exception as e:
        st.error(f"Error converting to Spark DataFrame: {e}")
        st.stop()

    # 4) Run the model
    try:
        prediction_df = model.transform(spark_df)
    except Exception as e:
        st.error(f"Error running batch prediction: {e}")
        st.stop()

    # 5) Spark -> Pandas -> Excel
    try:
        output_df = prediction_df.toPandas()
    except Exception as e:
        st.error(f"Error converting Spark DataFrame back to Pandas: {e}")
        st.stop()

    output_excel_path = "predictions.xlsx"
    output_df.to_excel(output_excel_path, index=False)

    # 6) Download Button
    with open(output_excel_path, "rb") as f:
        st.download_button(
            label="Download Batch Predictions",
            data=f.read(),
            file_name="predictions.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    st.success("Batch predictions completed! Download your file above.")

# spark.stop()  # Uncomment if you want to stop Spark when the app stops
