import streamlit as st
import sqlite3
import pandas as pd
from database import delete_patient

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Patient History",
    page_icon="📜",
    layout="wide"
)

# --------------------------------------------------
# DASHBOARD BUTTON
# --------------------------------------------------

col1, col2 = st.columns([1,5])

with col1:

    if st.button("⬅ Dashboard"):

        st.switch_page("app.py")

# --------------------------------------------------
# CSS
# --------------------------------------------------

st.markdown("""
<style>

#MainMenu{
visibility:hidden;
}

footer{
visibility:hidden;
}

header{
visibility:hidden;
}

.stApp{

background:#F4F8FB;

}

.title{

text-align:center;
font-size:42px;
font-weight:bold;
color:#0E5CAD;

}

.subtitle{

text-align:center;
font-size:18px;
color:gray;
margin-bottom:20px;

}

.card{

background:white;
padding:20px;
border-radius:15px;
box-shadow:0px 4px 12px rgba(0,0,0,0.10);

}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.markdown("""

<div class='title'>

📜 Patient History

</div>

<div class='subtitle'>

Hospital Patient Management System

</div>

""", unsafe_allow_html=True)

st.markdown("---")

# --------------------------------------------------
# DATABASE
# --------------------------------------------------

conn = sqlite3.connect("database.db")

query = """

SELECT *

FROM patients

ORDER BY rowid DESC

"""

df = pd.read_sql_query(query, conn)

conn.close()

# --------------------------------------------------
# NO PATIENTS
# --------------------------------------------------

if df.empty:

    st.warning("No patients have been registered yet.")

    st.stop()
    # --------------------------------------------------
# DASHBOARD STATISTICS
# --------------------------------------------------

total_patients = len(df)

high_risk = len(
    df[df["prediction"] == "High Risk"]
)

low_risk = len(
    df[df["prediction"] == "Low Risk"]
)

pending = len(
    df[df["prediction"].isna()]
)

st.header("📊 Dashboard")

c1, c2, c3, c4 = st.columns(4)

with c1:

    st.metric(
        "👥 Total Patients",
        total_patients
    )

with c2:

    st.metric(
        "🔴 High Risk",
        high_risk
    )

with c3:

    st.metric(
        "🟢 Low Risk",
        low_risk
    )

with c4:

    st.metric(
        "⏳ Pending",
        pending
    )

st.markdown("---")

# --------------------------------------------------
# SEARCH & FILTERS
# --------------------------------------------------

st.header("🔍 Search & Filters")

col1, col2, col3 = st.columns(3)

with col1:

    search = st.text_input(
        "Search Patient",
        placeholder="Patient ID or Name"
    )

with col2:

    risk_filter = st.selectbox(
        "Risk Level",
        [
            "All",
            "High Risk",
            "Low Risk",
            "Pending"
        ]
    )

with col3:

    gender_filter = st.selectbox(
        "Gender",
        [
            "All",
            "Male",
            "Female"
        ]
    )

date_filter = st.text_input(
    "Registration Date",
    placeholder="dd-mm-yyyy"
)

# --------------------------------------------------
# APPLY FILTERS
# --------------------------------------------------

filtered_df = df.copy()

# Search

if search:

    filtered_df = filtered_df[

        filtered_df["patient_id"].astype(str).str.contains(
            search,
            case=False
        )

        |

        filtered_df["full_name"].astype(str).str.contains(
            search,
            case=False
        )

    ]

# Risk Filter

if risk_filter != "All":

    if risk_filter == "Pending":

        filtered_df = filtered_df[
            filtered_df["prediction"].isna()
        ]

    else:

        filtered_df = filtered_df[
            filtered_df["prediction"] == risk_filter
        ]

# Gender Filter

if gender_filter != "All":

    filtered_df = filtered_df[
        filtered_df["gender"] == gender_filter
    ]

# Date Filter

if date_filter:

    filtered_df = filtered_df[

        filtered_df["registration_date"].astype(str).str.contains(
            date_filter,
            case=False
        )

    ]

st.markdown("---")
# --------------------------------------------------
# RISK DISTRIBUTION
# --------------------------------------------------

st.header("📊 Risk Distribution")

chart = pd.DataFrame(
    {
        "Patients": [

            len(filtered_df[filtered_df["prediction"] == "High Risk"]),

            len(filtered_df[filtered_df["prediction"] == "Low Risk"]),

            len(filtered_df[filtered_df["prediction"].isna()])

        ]
    },
    index=[
        "High Risk",
        "Low Risk",
        "Pending"
    ]
)

st.bar_chart(chart)

st.markdown("---")

# --------------------------------------------------
# PATIENT RECORDS
# --------------------------------------------------

st.header("📋 Patient Records")

display_df = filtered_df[
    [
        "patient_id",
        "full_name",
        "gender",
        "age",
        "mobile",
        "prediction",
        "confidence",
        "registration_date"
    ]
].copy()

display_df.insert(
    0,
    "S.No",
    range(1, len(display_df) + 1)
)

display_df.rename(
    columns={
        "patient_id": "Patient ID",
        "full_name": "Patient Name",
        "gender": "Gender",
        "age": "Age",
        "mobile": "Mobile",
        "prediction": "Prediction",
        "confidence": "Confidence (%)",
        "registration_date": "Registration Date"
    },
    inplace=True
)

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)

st.markdown("---")

# --------------------------------------------------
# SELECT PATIENT
# --------------------------------------------------

st.header("👤 Patient Details")

if filtered_df.empty:

    st.warning("No patient found.")

    st.stop()

selected_patient = st.selectbox(

    "Select Patient",

    filtered_df["patient_id"]

)

conn = sqlite3.connect("database.db")

patient = pd.read_sql_query(

    "SELECT * FROM patients WHERE patient_id=?",

    conn,

    params=(selected_patient,)

)

conn.close()

patient = patient.iloc[0]
# --------------------------------------------------
# PATIENT DETAILS CARD
# --------------------------------------------------

st.markdown("---")

st.header("🏥 Patient Details")

left, right = st.columns(2)

# --------------------------------------------------
# PERSONAL INFORMATION
# --------------------------------------------------

with left:

    st.subheader("👤 Personal Information")

    st.info(f"Patient ID : {patient['patient_id']}")

    st.write("**Full Name** :", patient["full_name"])

    st.write("**Gender** :", patient["gender"])

    st.write("**Age** :", patient["age"])

    st.write("**Blood Group** :", patient["blood_group"])

    st.write("**Mobile** :", patient["mobile"])

    st.write("**Email** :", patient["email"])

    st.write("**Address** :", patient["address"])

    st.write("**City** :", patient["city"])

    st.write("**State** :", patient["state"])

# --------------------------------------------------
# MEDICAL INFORMATION
# --------------------------------------------------

with right:

    st.subheader("❤️ Medical Information")

    st.write("**Blood Pressure** :", patient["blood_pressure"])

    st.write("**Heart Rate** :", patient["heart_rate"])

    st.write("**Diabetes** :", patient["diabetes"])

    st.write("**Smoking** :", patient["smoking"])

    st.write("**Alcohol** :", patient["alcohol"])

    st.write("**Family History** :", patient["family_history"])

    st.write("**Chief Complaint** :", patient["chief_complaint"])

st.markdown("---")

# --------------------------------------------------
# CLINICAL PARAMETERS
# --------------------------------------------------

st.header("🩺 Clinical Parameters")

c1, c2 = st.columns(2)

with c1:

    st.write("**Chest Pain Type** :", patient["cp"])

    st.write("**Resting BP** :", patient["trestbps"])

    st.write("**Cholesterol** :", patient["chol"])

    st.write("**Fasting Blood Sugar** :", patient["fbs"])

    st.write("**Rest ECG** :", patient["restecg"])

with c2:

    st.write("**Maximum Heart Rate** :", patient["thalach"])

    st.write("**Exercise Angina** :", patient["exang"])

    st.write("**Old Peak** :", patient["oldpeak"])

    st.write("**Slope** :", patient["slope"])

    st.write("**Major Vessels** :", patient["ca"])

    st.write("**Thalassemia** :", patient["thal"])

st.markdown("---")
# --------------------------------------------------
# AI PREDICTION RESULT
# --------------------------------------------------

st.header("🤖 AI Prediction")

prediction = patient["prediction"]
confidence = patient["confidence"]

if prediction == "High Risk":

    st.error("🔴 HIGH RISK")

elif prediction == "Low Risk":

    st.success("🟢 LOW RISK")

else:

    st.warning("⏳ PREDICTION PENDING")

if pd.notna(confidence):

    st.metric(
        "Prediction Confidence",
        f"{confidence:.2f}%"
    )

    st.progress(float(confidence) / 100)

st.markdown("---")

# --------------------------------------------------
# ACTION BUTTONS
# --------------------------------------------------

st.header("⚙ Patient Actions")

left, center, right = st.columns(3)

# ---------------- Medical Report ----------------

with left:

    if st.button(
        "📄 Open Medical Report",
        use_container_width=True
    ):

        st.switch_page("pages/Medical_Report.py")

# ---------------- Delete Patient ----------------

with center:

    confirm_delete = st.checkbox(
        "Confirm Delete"
    )

    if st.button(
        "🗑 Delete Patient",
        use_container_width=True
    ):

        if confirm_delete:

            delete_patient(
                patient["patient_id"]
            )

            st.success(
                "✅ Patient deleted successfully."
            )

            st.rerun()

        else:

            st.warning(
                "Please confirm before deleting."
            )

# ---------------- Export CSV ----------------

with right:

    csv = filtered_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(

        label="⬇ Export CSV",

        data=csv,

        file_name="Patient_History.csv",

        mime="text/csv",

        use_container_width=True

    )

st.markdown("---")

# --------------------------------------------------
# QUICK SUMMARY
# --------------------------------------------------

st.header("📋 Quick Summary")

summary = pd.DataFrame({

    "Field":[
        "Patient ID",
        "Patient Name",
        "Prediction",
        "Confidence",
        "Registration Date"
    ],

    "Value":[
        patient["patient_id"],
        patient["full_name"],
        patient["prediction"],
        f"{patient['confidence']:.2f}%"
        if pd.notna(patient["confidence"])
        else "Pending",
        patient["registration_date"]
    ]

})

st.table(summary)

st.markdown("---")

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown(
"""
<div style='text-align:center;color:gray;'>

❤️ <b>HeartCare AI</b><br>

Hospital Patient Management System<br><br>

Developed by <b>Shivamani Rao</b>

</div>
""",
unsafe_allow_html=True
)