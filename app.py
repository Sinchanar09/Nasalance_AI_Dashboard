import streamlit as st
import pandas as pd
import joblib
import uuid
from datetime import date
from utils.report_generator import generate_report
from utils.database import create_table, insert_patient

st.set_page_config(page_title="Nasalance Clinical AI", layout="wide")

create_table()
model = joblib.load("model/nasalance_regression_model.pkl")

st.title("Nasalance Clinical Analyzer")

# -----------------------------
# INPUTS
# -----------------------------
name = st.text_input("Patient Name")
age = st.number_input("Age", 1, 100)
gender = st.selectbox("Gender", ["Male", "Female"])
language = st.selectbox("Language", ["Kannada", "Malayalam"])

contact = st.text_input("Contact Number")
address = st.text_area("Address")
clinician = st.text_input("Clinician Name")
test_date = st.date_input("Test Date", date.today())

st.subheader("Nasalance Values")
mean = st.number_input("Mean")
min_val = st.number_input("Min")
max_val = st.number_input("Max")
create_table()

insert_patient(name, age, gender, contact, address)

# -----------------------------
# RUN ANALYSIS
# -----------------------------
if st.button("Run AI Analysis"):

    patient_id = str(uuid.uuid4())[:8]

    gender_enc = 0 if gender == "Male" else 1
    lang_enc = 0 if language == "Kannada" else 1

    data = pd.DataFrame([{
        "nasalance_mean": mean,
        "nasalance_range": max_val - min_val,
        "language_encoded": lang_enc,
        "gender_encoded": gender_enc,
        "age": age
    }])

    z = model.predict(data)[0]

    if z < -1:
        category = "Hyponasal"
    elif z > 1:
        category = "Hypernasal"
    else:
        category = "Normal"

    severity = "Mild" if abs(z) < 2 else "Moderate" if abs(z) < 3 else "Severe"

    impression = (
        "Normal nasalance"
        if category == "Normal"
        else "Hypernasality detected"
        if category == "Hypernasal"
        else "Hyponasality detected"
    )

    st.success("Analysis Complete")

    # SAVE STATE
    st.session_state["report"] = {
        "name": name,
        "age": age,
        "gender": gender,
        "contact": contact,
        "address": address,
        "clinician": clinician,
        "date": str(test_date),
        "mean": mean,
        "min": min_val,
        "max": max_val,
        "z": round(z, 3),
        "category": category,
        "severity": severity,
        "impression": impression,
    }

    st.session_state["patient_id"] = patient_id

# -----------------------------
# PDF GENERATION (OUTSIDE)
# -----------------------------
if "report" in st.session_state:

    if st.button("Generate Report"):

        file_path = generate_report(
            st.session_state["report"],
            st.session_state["patient_id"]
        )

        st.success("PDF Generated Successfully!")

        with open(file_path, "rb") as f:
            st.download_button(
                "Download Report",
                f,
                file_name="report.pdf",
                mime="application/pdf"
            )