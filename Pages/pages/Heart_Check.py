import streamlit as st
import joblib
import pandas as pd
import shap
import matplotlib.pyplot as plt

from database import (
    latest_patient,
    update_prediction,
    save_clinical_parameters
)

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Heart Check",
    page_icon="❤️",
    layout="wide"
)

# --------------------------------------------------
# LOAD MODEL
# --------------------------------------------------

model = joblib.load("heart_model.pkl")

# Create SHAP Explainer
explainer = shap.TreeExplainer(model)

# --------------------------------------------------
# FEATURE NAMES
# --------------------------------------------------

feature_names = [
    "age",
    "sex",
    "cp",
    "trestbps",
    "chol",
    "fbs",
    "restecg",
    "thalch",
    "exang",
    "oldpeak",
    "slope",
    "ca",
    "thal"
]

# --------------------------------------------------
# NAVIGATION
# --------------------------------------------------

left, right = st.columns([1, 5])

with left:

    if st.button("⬅ Dashboard"):

        st.switch_page("app.py")

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

.stApp{
    background:#F5F9FC;
}

.title{
    text-align:center;
    font-size:42px;
    font-weight:bold;
    color:#0E5CAD;
}

.subtitle{
    text-align:center;
    color:gray;
    font-size:18px;
}

.card{
    background:white;
    padding:25px;
    border-radius:15px;
    box-shadow:0px 5px 12px rgba(0,0,0,0.12);
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# PAGE TITLE
# --------------------------------------------------

st.markdown("""
<div class='title'>
❤️ Heart Disease Prediction
</div>

<div class='subtitle'>
AI Powered Clinical Risk Assessment
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# --------------------------------------------------
# LOAD LATEST PATIENT
# --------------------------------------------------

patient = latest_patient()

if patient is None:

    st.warning("No patient registered.")

    st.stop()
    # --------------------------------------------------
# PATIENT INFORMATION
# --------------------------------------------------

st.markdown("<div class='card'>", unsafe_allow_html=True)

st.header("👤 Patient Information")

c1, c2, c3 = st.columns(3)

# ------------------------------------------
# Column 1
# ------------------------------------------

with c1:

    st.write("### Patient ID")

    st.info(patient[0])

    st.write("### Full Name")

    st.info(patient[1])

# ------------------------------------------
# Column 2
# ------------------------------------------

with c2:

    st.write("### Gender")

    st.info(patient[2])

    st.write("### Age")

    st.info(patient[4])

# ------------------------------------------
# Column 3
# ------------------------------------------

with c3:

    st.write("### Blood Group")

    st.info(patient[5])

    st.write("### Mobile")

    st.info(patient[8])

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")
# --------------------------------------------------
# CLINICAL PARAMETERS
# --------------------------------------------------

st.header("🩺 Clinical Parameters")

left, right = st.columns(2)

# ==================================================
# LEFT COLUMN
# ==================================================

with left:

    age_input = st.number_input(
        "Age",
        min_value=1,
        max_value=120,
        value=int(patient[4])
    )

    sex = st.selectbox(
        "Sex",
        [
            "Male",
            "Female"
        ]
    )

    cp = st.selectbox(
        "Chest Pain Type",
        [
            "Typical Angina",
            "Atypical Angina",
            "Non-anginal Pain",
            "Asymptomatic"
        ]
    )

    trestbps = st.number_input(
        "Resting Blood Pressure (mm Hg)",
        min_value=80,
        max_value=250,
        value=120
    )

    chol = st.number_input(
        "Serum Cholesterol (mg/dl)",
        min_value=100,
        max_value=700,
        value=200
    )

    fbs = st.selectbox(
        "Fasting Blood Sugar > 120 mg/dl",
        [
            "No",
            "Yes"
        ]
    )

# ==================================================
# RIGHT COLUMN
# ==================================================

with right:

    restecg = st.selectbox(
        "Resting ECG",
        [
            "Normal",
            "ST-T Wave Abnormality",
            "Left Ventricular Hypertrophy"
        ]
    )

    thalch = st.number_input(
        "Maximum Heart Rate",
        min_value=60,
        max_value=250,
        value=150
    )

    exang = st.selectbox(
        "Exercise Induced Angina",
        [
            "No",
            "Yes"
        ]
    )

    oldpeak = st.number_input(
        "Old Peak",
        min_value=0.0,
        max_value=10.0,
        value=1.0,
        step=0.1
    )

    slope = st.selectbox(
        "ST Slope",
        [
            "Upsloping",
            "Flat",
            "Downsloping"
        ]
    )

    ca = st.selectbox(
        "Major Vessels",
        [
            0,
            1,
            2,
            3
        ]
    )

    thal = st.selectbox(
        "Thalassemia",
        [
            "Normal",
            "Fixed Defect",
            "Reversible Defect"
        ]
    )

st.markdown("---")
# --------------------------------------------------
# ENCODE INPUTS
# --------------------------------------------------

# Save original text values for database

cp_text = cp
fbs_text = fbs
restecg_text = restecg
exang_text = exang
slope_text = slope
thal_text = thal

# Encode categorical values

sex = 1 if sex == "Male" else 0

cp = {
    "Typical Angina": 0,
    "Atypical Angina": 1,
    "Non-anginal Pain": 2,
    "Asymptomatic": 3
}[cp]

fbs = 1 if fbs == "Yes" else 0

restecg = {
    "Normal": 0,
    "ST-T Wave Abnormality": 1,
    "Left Ventricular Hypertrophy": 2
}[restecg]

exang = 1 if exang == "Yes" else 0

slope = {
    "Upsloping": 0,
    "Flat": 1,
    "Downsloping": 2
}[slope]

thal = {
    "Normal": 1,
    "Fixed Defect": 2,
    "Reversible Defect": 3
}[thal]

# --------------------------------------------------
# PREDICTION BUTTON
# --------------------------------------------------

predict = st.button(

    "❤️ Predict Heart Disease",

    use_container_width=True

)

# --------------------------------------------------
# PREPARE INPUT
# --------------------------------------------------

if predict:

    input_df = pd.DataFrame(

        [[

            age_input,
            sex,
            cp,
            trestbps,
            chol,
            fbs,
            restecg,
            thalch,
            exang,
            oldpeak,
            slope,
            ca,
            thal

        ]],

        columns=feature_names

    )

    prediction = model.predict(input_df)[0]

    probability = model.predict_proba(input_df)[0]

    confidence = round(

        max(probability) * 100,

        2

    )
        # --------------------------------------------------
    # PREDICTION RESULT
    # --------------------------------------------------

    if prediction == 1:

        result = "High Risk"

        st.error("🔴 High Risk of Heart Disease")

        recommendation = """
• Consult a Cardiologist immediately.

• Monitor Blood Pressure regularly.

• Reduce Cholesterol levels.

• Exercise only under medical supervision.

• Maintain a heart-healthy diet.

• Stop Smoking and Alcohol consumption.
"""

    else:

        result = "Low Risk"

        st.success("🟢 Low Risk of Heart Disease")

        recommendation = """
• Continue a healthy lifestyle.

• Exercise at least 30 minutes daily.

• Eat nutritious food.

• Maintain a healthy body weight.

• Schedule an annual heart check-up.
"""

    # --------------------------------------------------
    # CONFIDENCE SCORE
    # --------------------------------------------------

    st.metric(
        "Prediction Confidence",
        f"{confidence:.2f}%"
    )

    st.progress(confidence / 100)

    st.markdown("---")

    # --------------------------------------------------
    # AI RECOMMENDATION
    # --------------------------------------------------

    st.subheader("💊 AI Recommendation")

    st.info(recommendation)

    st.markdown("---")
        # --------------------------------------------------
    # SAVE CLINICAL PARAMETERS
    # --------------------------------------------------

    save_clinical_parameters(

        patient[0],

        cp_text,

        trestbps,

        chol,

        fbs_text,

        restecg_text,

        thalch,

        exang_text,

        oldpeak,

        slope_text,

        ca,

        thal_text

    )

    # --------------------------------------------------
    # SAVE PREDICTION
    # --------------------------------------------------

    update_prediction(

        patient[0],

        result,

        confidence

    )

    st.success("✅ Prediction saved successfully.")

    st.markdown("---")

    # --------------------------------------------------
    # PREDICTION SUMMARY
    # --------------------------------------------------

    st.subheader("📋 Prediction Summary")

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(

            "Patient",

            patient[1]

        )

    with c2:

        st.metric(

            "Prediction",

            result

        )

    with c3:

        st.metric(

            "Confidence",

            f"{confidence:.2f}%"

        )

    st.markdown("---")

    # --------------------------------------------------
    # NEXT ACTIONS
    # --------------------------------------------------

    st.subheader("📄 Next Actions")

    left, right = st.columns(2)

    with left:

        if st.button(

            "📄 Open Medical Report",

            use_container_width=True

        ):

            st.switch_page(
                "pages/Medical_Report.py"
            )

    with right:

        if st.button(

            "📜 View Patient History",

            use_container_width=True

        ):

            st.switch_page(
                "pages/History.py"
            )

    st.markdown("---")

    # --------------------------------------------------
    # FOOTER
    # --------------------------------------------------

    st.markdown("""

    <center>

    ❤️ HeartCare AI

    AI Powered Heart Disease Prediction System

    </center>

    """, unsafe_allow_html=True)