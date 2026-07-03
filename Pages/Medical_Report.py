import streamlit as st
import sqlite3
import pandas as pd
import qrcode
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Medical Report",
    page_icon="📄",
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
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.markdown("""

<div class='title'>

📄 Medical Report

</div>

<div class='subtitle'>

AI Powered Heart Disease Assessment

</div>

""", unsafe_allow_html=True)

st.markdown("---")

# --------------------------------------------------
# DATABASE
# --------------------------------------------------

conn = sqlite3.connect("database.db")

patients = pd.read_sql_query(

    "SELECT patient_id, full_name FROM patients ORDER BY rowid DESC",

    conn

)

if patients.empty:

    st.warning("No patients found.")

    st.stop()

selected_patient = st.selectbox(

    "Select Patient",

    patients["patient_id"]

)

patient = pd.read_sql_query(

    "SELECT * FROM patients WHERE patient_id=?",

    conn,

    params=(selected_patient,)

)

conn.close()

patient = patient.iloc[0]
# --------------------------------------------------
# HOSPITAL HEADER
# --------------------------------------------------

st.markdown("""

<div style="background:white;
padding:20px;
border-radius:12px;
box-shadow:0px 4px 12px rgba(0,0,0,0.10);">

<h1 style="text-align:center;color:#0E5CAD;">

🏥 HeartCare AI Hospital

</h1>

<h4 style="text-align:center;color:gray;">

AI Powered Heart Disease Assessment Report

</h4>

<hr>

</div>

""", unsafe_allow_html=True)

# --------------------------------------------------
# REPORT DETAILS
# --------------------------------------------------

report_no = f"HCAI-{patient['patient_id']}"

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "📄 Report Number",
        report_no
    )

with col2:

    st.metric(
        "📅 Report Date",
        patient["registration_date"]
    )

with col3:

    st.metric(
        "🕒 Report Time",
        patient["registration_time"]
    )

st.markdown("---")

# --------------------------------------------------
# PATIENT INFORMATION
# --------------------------------------------------

st.header("👤 Patient Information")

left, right = st.columns(2)

with left:

    st.write("**Patient ID** :", patient["patient_id"])

    st.write("**Full Name** :", patient["full_name"])

    st.write("**Gender** :", patient["gender"])

    st.write("**Age** :", patient["age"])

    st.write("**Blood Group** :", patient["blood_group"])

    st.write("**Occupation** :", patient["occupation"])

with right:

    st.write("**Mobile** :", patient["mobile"])

    st.write("**Email** :", patient["email"])

    st.write("**City** :", patient["city"])

    st.write("**State** :", patient["state"])

    st.write("**Height** :", patient["height"], "cm")

    st.write("**Weight** :", patient["weight"], "kg")

st.markdown("---")

# --------------------------------------------------
# VITAL SIGNS
# --------------------------------------------------

st.header("🩺 Vital Signs")

v1, v2, v3 = st.columns(3)

with v1:

    st.metric(
        "Blood Pressure",
        patient["blood_pressure"]
    )

with v2:

    st.metric(
        "Heart Rate",
        patient["heart_rate"]
    )

with v3:

    st.metric(
        "BMI",
        patient["bmi"]
    )

st.markdown("---")
# --------------------------------------------------
# CLINICAL PARAMETERS
# --------------------------------------------------

st.header("🩺 Clinical Parameters")

left, right = st.columns(2)

# ---------------- Left ----------------

with left:

    st.write("**Chest Pain Type** :", patient["cp"])

    st.write(
        "**Resting Blood Pressure** :",
        f"{patient['trestbps']} mmHg"
    )

    st.write(
        "**Cholesterol** :",
        f"{patient['chol']} mg/dl"
    )

    st.write(
        "**Fasting Blood Sugar** :",
        patient["fbs"]
    )

    st.write(
        "**Resting ECG** :",
        patient["restecg"]
    )

    st.write(
        "**Maximum Heart Rate** :",
        patient["thalach"]
    )

# ---------------- Right ----------------

with right:

    st.write(
        "**Exercise Induced Angina** :",
        patient["exang"]
    )

    st.write(
        "**Old Peak** :",
        patient["oldpeak"]
    )

    st.write(
        "**ST Slope** :",
        patient["slope"]
    )

    st.write(
        "**Major Vessels** :",
        patient["ca"]
    )

    st.write(
        "**Thalassemia** :",
        patient["thal"]
    )

st.markdown("---")

# --------------------------------------------------
# MEDICAL HISTORY
# --------------------------------------------------

st.header("📋 Medical History")

left, right = st.columns(2)

with left:

    st.write("**Diabetes** :", patient["diabetes"])

    st.write("**Smoking** :", patient["smoking"])

    st.write("**Alcohol** :", patient["alcohol"])

    st.write(
        "**Family History** :",
        patient["family_history"]
    )

with right:

    st.write("**Allergies** :", patient["allergies"])

    st.write(
        "**Current Medications** :",
        patient["medications"]
    )

    st.write(
        "**Past Medical History** :",
        patient["past_history"]
    )

    st.write(
        "**Chief Complaint** :",
        patient["chief_complaint"]
    )

st.markdown("---")
# --------------------------------------------------
# AI PREDICTION
# --------------------------------------------------

st.header("🤖 AI Prediction")

prediction = patient["prediction"]
confidence = patient["confidence"]

if prediction == "High Risk":

    st.error("🔴 HIGH RISK OF HEART DISEASE")

elif prediction == "Low Risk":

    st.success("🟢 LOW RISK OF HEART DISEASE")

else:

    st.warning("⏳ Prediction Pending")

# ---------------- Confidence ----------------

if pd.notna(confidence):

    st.metric(
        "Prediction Confidence",
        f"{confidence:.2f}%"
    )

    st.progress(float(confidence) / 100)

st.markdown("---")

# --------------------------------------------------
# AI RECOMMENDATION
# --------------------------------------------------

st.header("💊 AI Recommendation")

if prediction == "High Risk":

    st.error("""

✔ Consult a Cardiologist immediately.

✔ Monitor Blood Pressure regularly.

✔ Reduce Cholesterol.

✔ Maintain a Heart Healthy Diet.

✔ Exercise only under medical supervision.

✔ Stop Smoking and Alcohol.

✔ Schedule a complete Cardiac Examination.

""")

elif prediction == "Low Risk":

    st.success("""

✔ Continue a healthy lifestyle.

✔ Exercise at least 30 minutes daily.

✔ Eat nutritious food.

✔ Maintain healthy body weight.

✔ Sleep 7–8 hours daily.

✔ Annual Heart Check-up is recommended.

""")

else:

    st.info("Prediction has not been performed yet.")

st.markdown("---")

# --------------------------------------------------
# EXPLAINABLE AI
# --------------------------------------------------

st.header("🧠 Explainable AI")

reasons = []

# High Cholesterol

if pd.notna(patient["chol"]) and patient["chol"] >= 240:
    reasons.append(
        "High Cholesterol may increase cardiovascular risk."
    )

# High Blood Pressure

if pd.notna(patient["trestbps"]) and patient["trestbps"] >= 140:
    reasons.append(
        "Resting Blood Pressure is above the normal range."
    )

# Chest Pain

if patient["cp"] == "Asymptomatic":
    reasons.append(
        "Asymptomatic chest pain is a significant clinical indicator."
    )

# Exercise Angina

if patient["exang"] == "Yes":
    reasons.append(
        "Exercise-induced angina is present."
    )

# Diabetes

if patient["diabetes"] == "Yes":
    reasons.append(
        "Diabetes is a major risk factor for heart disease."
    )

# Smoking

if patient["smoking"] == "Yes":
    reasons.append(
        "Smoking significantly increases cardiac risk."
    )

# Family History

if patient["family_history"] == "Yes":
    reasons.append(
        "Positive family history increases susceptibility."
    )

# Heart Rate

if pd.notna(patient["thalach"]) and patient["thalach"] < 100:
    reasons.append(
        "Maximum heart rate is lower than expected."
    )

if len(reasons) == 0:

    st.success(
        "No major clinical risk factors were detected based on the available information."
    )

else:

    for reason in reasons:

        st.write("✅", reason)

st.markdown("---")
# --------------------------------------------------
# GENERATE PROFESSIONAL PDF
# --------------------------------------------------

styles = getSampleStyleSheet()

def generate_pdf():

    file_name = f"{patient['patient_id']}_Medical_Report.pdf"

    doc = SimpleDocTemplate(file_name)

    story = []

    # --------------------------------------------------
    # HOSPITAL HEADER
    # --------------------------------------------------

    title = Paragraph(

        "<font size=22 color='darkblue'><b>HEARTCARE AI HOSPITAL</b></font>",

        styles["Title"]

    )

    story.append(title)

    story.append(

        Paragraph(

            "<b>AI Powered Heart Disease Assessment Report</b>",

            styles["Heading2"]

        )

    )

    story.append(Spacer(1,20))

    # --------------------------------------------------
    # REPORT DETAILS TABLE
    # --------------------------------------------------

    report_table = [

        ["Report No", f"HCAI-{patient['patient_id']}"],

        ["Report Date", patient["registration_date"]],

        ["Report Time", patient["registration_time"]]

    ]

    table = Table(report_table, colWidths=[170,250])

    table.setStyle(

        TableStyle([

            ("BACKGROUND",(0,0),(0,-1),colors.lightblue),

            ("GRID",(0,0),(-1,-1),1,colors.black),

            ("FONTNAME",(0,0),(-1,-1),"Helvetica-Bold"),

            ("BOTTOMPADDING",(0,0),(-1,-1),8)

        ])

    )

    story.append(table)

    story.append(Spacer(1,20))

    # --------------------------------------------------
    # PATIENT DETAILS
    # --------------------------------------------------

    story.append(

        Paragraph(

            "<b>PATIENT INFORMATION</b>",

            styles["Heading1"]

        )

    )

    patient_table = [

        ["Patient ID", patient["patient_id"]],

        ["Full Name", patient["full_name"]],

        ["Gender", patient["gender"]],

        ["Age", patient["age"]],

        ["Blood Group", patient["blood_group"]],

        ["Mobile", patient["mobile"]],

        ["Email", patient["email"]]

    ]

    table = Table(patient_table, colWidths=[170,250])

    table.setStyle(

        TableStyle([

            ("GRID",(0,0),(-1,-1),1,colors.grey),

            ("BACKGROUND",(0,0),(0,-1),colors.beige),

            ("FONTNAME",(0,0),(-1,-1),"Helvetica")

        ])

    )

    story.append(table)

    story.append(Spacer(1,20))
    # --------------------------------------------------
    # CLINICAL PARAMETERS
    # --------------------------------------------------

    story.append(
        Paragraph(
            "<b>CLINICAL PARAMETERS</b>",
            styles["Heading1"]
        )
    )

    clinical_table = [

        ["Chest Pain Type", patient["cp"]],
        ["Resting Blood Pressure", f"{patient['trestbps']} mmHg"],
        ["Cholesterol", f"{patient['chol']} mg/dl"],
        ["Fasting Blood Sugar", patient["fbs"]],
        ["Rest ECG", patient["restecg"]],
        ["Maximum Heart Rate", patient["thalach"]],
        ["Exercise Angina", patient["exang"]],
        ["Old Peak", patient["oldpeak"]],
        ["ST Slope", patient["slope"]],
        ["Major Vessels", patient["ca"]],
        ["Thalassemia", patient["thal"]]

    ]

    table = Table(
        clinical_table,
        colWidths=[200,220]
    )

    table.setStyle(

        TableStyle([

            ("BACKGROUND",(0,0),(0,-1),colors.lightgrey),

            ("GRID",(0,0),(-1,-1),1,colors.black),

            ("FONTNAME",(0,0),(-1,-1),"Helvetica"),

            ("BOTTOMPADDING",(0,0),(-1,-1),8)

        ])

    )

    story.append(table)

    story.append(Spacer(1,20))

    # --------------------------------------------------
    # AI PREDICTION
    # --------------------------------------------------

    story.append(
        Paragraph(
            "<b>AI PREDICTION</b>",
            styles["Heading1"]
        )
    )

    prediction_table = [
        ["Prediction", prediction],
        ["Confidence", f"{confidence:.2f}%"]
    ]

    table = Table(
        prediction_table,
        colWidths=[180, 240]
    )

    # Set prediction color
    if prediction == "High Risk":

        bg = colors.red

    elif prediction == "Low Risk":

        bg = colors.green

    else:

        bg = colors.orange

    txt = colors.white

    table.setStyle(

        TableStyle([

            ("BACKGROUND", (0, 0), (-1, -1), bg),

            ("TEXTCOLOR", (0, 0), (-1, -1), txt),

            ("GRID", (0, 0), (-1, -1), 1, colors.black),

            ("ALIGN", (0, 0), (-1, -1), "CENTER"),

            ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),

            ("BOTTOMPADDING", (0, 0), (-1, -1), 10)

        ])

    )

    story.append(table)

    story.append(Spacer(1, 20))

    # --------------------------------------------------
    # AI RECOMMENDATION
    # --------------------------------------------------

    story.append(

        Paragraph(
            "<b>AI RECOMMENDATION</b>",
            styles["Heading1"]
        )

    )

    if prediction == "High Risk":

        recommendation = """

        • Consult a Cardiologist immediately.<br/>

        • Reduce Cholesterol levels.<br/>

        • Monitor Blood Pressure.<br/>

        • Exercise only under medical supervision.<br/>

        • Stop Smoking and Alcohol.<br/>

        • Maintain a heart healthy diet.<br/>

        """

    else:

        recommendation = """

        • Continue a healthy lifestyle.<br/>

        • Exercise regularly.<br/>

        • Eat nutritious food.<br/>

        • Maintain healthy weight.<br/>

        • Annual heart check-up recommended.<br/>

        """

    story.append(

        Paragraph(
            recommendation,
            styles["Normal"]
        )

    )

    story.append(Spacer(1,20))
    # --------------------------------------------------
    # EXPLAINABLE AI
    # --------------------------------------------------

    story.append(
        Paragraph(
            "<b>EXPLAINABLE AI</b>",
            styles["Heading1"]
        )
    )

    explain = []

    if pd.notna(patient["chol"]) and patient["chol"] >= 240:
        explain.append("• High cholesterol level detected.")

    if pd.notna(patient["trestbps"]) and patient["trestbps"] >= 140:
        explain.append("• Resting blood pressure is elevated.")

    if patient["cp"] == "Asymptomatic":
        explain.append("• Asymptomatic chest pain increases heart disease risk.")

    if patient["exang"] == "Yes":
        explain.append("• Exercise induced angina detected.")

    if patient["diabetes"] == "Yes":
        explain.append("• Diabetes is a significant cardiovascular risk factor.")

    if patient["smoking"] == "Yes":
        explain.append("• Smoking increases the risk of heart disease.")

    if patient["family_history"] == "Yes":
        explain.append("• Positive family history of heart disease.")

    if len(explain) == 0:

        explain.append(
            "• No major clinical risk factors were identified."
        )

    for item in explain:

        story.append(
            Paragraph(
                item,
                styles["Normal"]
            )
        )

    story.append(Spacer(1,20))

    # --------------------------------------------------
    # QR CODE
    # --------------------------------------------------

    qr_data = f"""
HeartCare AI Hospital

Patient ID : {patient['patient_id']}

Name : {patient['full_name']}

Prediction : {prediction}

Confidence : {confidence:.2f}%

Date : {patient['registration_date']}
"""

    qr = qrcode.make(qr_data)

    qr.save("patient_qr.png")

    story.append(
        Paragraph(
            "<b>REPORT QR CODE</b>",
            styles["Heading1"]
        )
    )

    story.append(
        Image(
            "patient_qr.png",
            width=120,
            height=120
        )
    )

    story.append(Spacer(1,20))

    # --------------------------------------------------
    # SIGNATURES
    # --------------------------------------------------

    story.append(
        Paragraph(
            "<b>SIGNATURES</b>",
            styles["Heading1"]
        )
    )

    signature_table = [

        [

            "Doctor Signature\n\n\n_____________________",

            "Patient Signature\n\n\n_____________________"

        ]

    ]

    table = Table(
        signature_table,
        colWidths=[250,250]
    )

    table.setStyle(

        TableStyle([

            ("GRID",(0,0),(-1,-1),1,colors.white),

            ("ALIGN",(0,0),(-1,-1),"CENTER"),

            ("FONTNAME",(0,0),(-1,-1),"Helvetica-Bold")

        ])

    )

    story.append(table)

    story.append(Spacer(1,20))

    # --------------------------------------------------
    # DISCLAIMER
    # --------------------------------------------------

    story.append(
        Paragraph(
            "<b>DISCLAIMER</b>",
            styles["Heading1"]
        )
    )

    story.append(
        Paragraph(
            "This report is generated using Artificial Intelligence and should only be used as a clinical decision support tool. It is not a substitute for professional medical diagnosis or treatment.",
            styles["Normal"]
        )
    )

    story.append(Spacer(1,20))

    # --------------------------------------------------
    # BUILD PDF
    # --------------------------------------------------

    doc.build(story)

    return file_name
# --------------------------------------------------
# GENERATE PDF
# --------------------------------------------------

st.markdown("---")

st.header("📄 Download Medical Report")

if st.button(
    "📄 Generate Professional PDF",
    use_container_width=True
):

    try:

        pdf = generate_pdf()

        st.success("✅ Medical Report Generated Successfully!")

        with open(pdf, "rb") as file:

            st.download_button(

                label="⬇ Download Medical Report",

                data=file,

                file_name=pdf,

                mime="application/pdf",

                use_container_width=True

            )

    except Exception as e:

        st.error(f"Error : {e}")