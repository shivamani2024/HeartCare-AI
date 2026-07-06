import streamlit as st
from datetime import datetime, date
from database import save_patient

# --------------------------------------------------
# Page Config
# --------------------------------------------------

st.set_page_config(
    page_title="Patient Registration",
    page_icon="👤",
    layout="wide"
)

# --------------------------------------------------
# CSS
# --------------------------------------------------

st.markdown("""
<style>

.stApp{
    background:#F4F8FB;
}

header{
visibility:hidden;
}

footer{
visibility:hidden;
}

#MainMenu{
visibility:hidden;
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

padding:30px;

border-radius:15px;

box-shadow:0px 6px 18px rgba(0,0,0,0.12);

}

.stButton>button{

width:100%;

height:48px;

border-radius:10px;

font-size:16px;

font-weight:bold;

background:#0E5CAD;

color:white;

}

.stButton>button:hover{

background:#1565C0;

}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Header
# --------------------------------------------------

st.markdown("""
<div class='title'>
👤 Patient Registration
</div>

<div class='subtitle'>
Register Patient Before Heart Disease Prediction
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Navigation
# --------------------------------------------------

left, right = st.columns([1,5])

with left:

    if st.button("⬅ Dashboard"):

        st.switch_page("app.py")

st.markdown("---")

# --------------------------------------------------
# Patient ID
# --------------------------------------------------

patient_id = "HC" + datetime.now().strftime("%Y%m%d%H%M%S")

# --------------------------------------------------
# Registration Form
# --------------------------------------------------

st.markdown("<div class='card'>", unsafe_allow_html=True)

st.header("👤 Personal Information")

col1,col2 = st.columns(2)

with col1:

    st.text_input(
        "Patient ID",
        value=patient_id,
        disabled=True
    )

    full_name = st.text_input("Full Name")

    gender = st.selectbox(
        "Gender",
        [
            "Male",
            "Female",
            "Other"
        ]
    )

    blood_group = st.selectbox(
        "Blood Group",
        [
            "A+","A-",
            "B+","B-",
            "AB+","AB-",
            "O+","O-"
        ]
    )

with col2:

    dob = st.date_input(
        "Date of Birth",
        value=date(2000,1,1),
        min_value=date(1900,1,1),
        max_value=date.today()
    )

    today = date.today()

    age = today.year - dob.year - (
        (today.month,today.day) <
        (dob.month,dob.day)
    )

    st.number_input(
        "Age",
        value=age,
        disabled=True
    )

    marital_status = st.selectbox(
        "Marital Status",
        [
            "Single",
            "Married",
            "Divorced",
            "Widowed"
        ]
    )

    occupation = st.text_input("Occupation")

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")
# --------------------------------------------------
# Contact Information
# --------------------------------------------------

st.markdown("<div class='card'>", unsafe_allow_html=True)

st.header("📞 Contact Information")

col1, col2 = st.columns(2)

with col1:

    mobile = st.text_input(
        "Mobile Number",
        placeholder="9876543210"
    )

    email = st.text_input(
        "Email Address",
        placeholder="patient@email.com"
    )

    address = st.text_area(
        "Full Address",
        height=100
    )

with col2:

    city = st.text_input("City")

    state = st.selectbox(
        "State",
        [
            "Andhra Pradesh",
            "Arunachal Pradesh",
            "Assam",
            "Bihar",
            "Chhattisgarh",
            "Goa",
            "Gujarat",
            "Haryana",
            "Himachal Pradesh",
            "Jharkhand",
            "Karnataka",
            "Kerala",
            "Madhya Pradesh",
            "Maharashtra",
            "Manipur",
            "Meghalaya",
            "Mizoram",
            "Nagaland",
            "Odisha",
            "Punjab",
            "Rajasthan",
            "Sikkim",
            "Tamil Nadu",
            "Telangana",
            "Tripura",
            "Uttar Pradesh",
            "Uttarakhand",
            "West Bengal"
        ]
    )

    pincode = st.text_input(
        "PIN Code",
        placeholder="500001"
    )

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")
# --------------------------------------------------
# Emergency Contact
# --------------------------------------------------

st.markdown("<div class='card'>", unsafe_allow_html=True)

st.header("🚨 Emergency Contact")

col1, col2 = st.columns(2)

with col1:

    guardian_name = st.text_input(
        "Guardian / Family Member Name"
    )

    relationship = st.selectbox(
        "Relationship",
        [
            "Father",
            "Mother",
            "Brother",
            "Sister",
            "Spouse",
            "Son",
            "Daughter",
            "Friend",
            "Other"
        ]
    )

with col2:

    emergency_mobile = st.text_input(
        "Emergency Contact Number",
        placeholder="9876543210"
    )

    emergency_email = st.text_input(
        "Emergency Email (Optional)"
    )

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")
# --------------------------------------------------
# Medical Information
# --------------------------------------------------

st.markdown("<div class='card'>", unsafe_allow_html=True)

st.header("🩺 Medical Information")

col1, col2 = st.columns(2)

# ---------------- Left Column ----------------

with col1:

    height = st.number_input(
        "Height (cm)",
        min_value=50,
        max_value=250,
        value=170
    )

    weight = st.number_input(
        "Weight (kg)",
        min_value=10,
        max_value=250,
        value=70
    )

    bmi = round(weight / ((height / 100) ** 2), 2)

    st.number_input(
        "BMI",
        value=bmi,
        disabled=True
    )

    blood_pressure = st.text_input(
        "Blood Pressure",
        placeholder="120/80"
    )

    heart_rate = st.number_input(
        "Heart Rate (BPM)",
        min_value=30,
        max_value=220,
        value=72
    )

# ---------------- Right Column ----------------

with col2:

    diabetes = st.selectbox(
        "Diabetes",
        ["No", "Yes"]
    )

    smoking = st.selectbox(
        "Smoking",
        ["No", "Yes"]
    )

    alcohol = st.selectbox(
        "Alcohol Consumption",
        ["No", "Occasionally", "Regularly"]
    )

    family_history = st.selectbox(
        "Family History of Heart Disease",
        ["No", "Yes"]
    )

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")
# --------------------------------------------------
# Lifestyle & Medical History
# --------------------------------------------------

st.markdown("<div class='card'>", unsafe_allow_html=True)

st.header("📋 Lifestyle & Medical History")

allergies = st.text_area(
    "Known Allergies",
    placeholder="Penicillin, Dust Allergy, None..."
)

medications = st.text_area(
    "Current Medications",
    placeholder="List current medications..."
)

past_history = st.text_area(
    "Past Medical History",
    placeholder="Hypertension, Diabetes, Surgery..."
)

chief_complaint = st.text_area(
    "Chief Complaint / Reason for Visit",
    placeholder="Chest pain, dizziness, breathing difficulty..."
)

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")
# --------------------------------------------------
# Consent
# --------------------------------------------------

consent = st.checkbox(
    "I confirm that the above information is correct."
)

st.markdown("---")
# --------------------------------------------------
# Save Buttons
# --------------------------------------------------

col1, col2 = st.columns(2)

with col1:
    save = st.button(
        "💾 Save Patient",
        use_container_width=True
    )

with col2:
    proceed = st.button(
        "➡ Save & Continue",
        use_container_width=True
    )

# --------------------------------------------------
# Save Patient Data
# --------------------------------------------------

if save or proceed:

    if full_name.strip() == "":
        st.error("⚠ Please enter the patient's full name.")

    elif mobile.strip() == "":
        st.error("⚠ Please enter the mobile number.")

    elif not mobile.isdigit() or len(mobile) != 10:
        st.error("⚠ Mobile number must contain exactly 10 digits.")

    elif guardian_name.strip() == "":
        st.error("⚠ Please enter the guardian's name.")

    elif emergency_mobile.strip() == "":
        st.error("⚠ Please enter the emergency contact number.")

    elif not emergency_mobile.isdigit() or len(emergency_mobile) != 10:
        st.error("⚠ Emergency contact number must contain exactly 10 digits.")

    elif not consent:
        st.error("⚠ Please accept the declaration before continuing.")

    else:

        patient_data = (

            patient_id,
            full_name,
            gender,
            str(dob),
            age,
            blood_group,
            marital_status,
            occupation,

            mobile,
            email,
            address,
            city,
            state,
            pincode,

            guardian_name,
            relationship,
            emergency_mobile,
            emergency_email,

            height,
            weight,
            bmi,

            blood_pressure,
            heart_rate,
            diabetes,
            smoking,
            alcohol,
            family_history,

            allergies,
            medications,
            past_history,
            chief_complaint,

            # Clinical Parameters
            None,      # cp
            None,      # trestbps
            None,      # chol
            None,      # fbs
            None,      # restecg
            None,      # thalach
            None,      # exang
            None,      # oldpeak
            None,      # slope
            None,      # ca
            None,      # thal

            # Prediction
            None,      # prediction
            None,      # confidence

            datetime.now().strftime("%d-%m-%Y"),
            datetime.now().strftime("%I:%M %p")

        )

        save_patient(patient_data)

        st.success("✅ Patient Registered Successfully!")

        st.balloons()

        if proceed:
            st.switch_page("pages/Heart_Check.py")