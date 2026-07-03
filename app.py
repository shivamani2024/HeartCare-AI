import streamlit as st
import sqlite3
import pandas as pd

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="HeartCare AI",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================================================
# CSS
# ==================================================

st.markdown("""
<style>

#MainMenu{
visibility:hidden;
}

header{
visibility:hidden;
}

footer{
visibility:hidden;
}

.stApp{
background:#F5F9FC;
}

.block-container{

padding-top:2rem;
padding-left:3rem;
padding-right:3rem;
padding-bottom:2rem;

}

.title{

text-align:center;
font-size:55px;
font-weight:bold;
color:#0E5CAD;

}

.subtitle{

text-align:center;
font-size:22px;
color:#666666;

}

.section{

font-size:28px;
font-weight:bold;
color:#0E5CAD;

margin-top:20px;

margin-bottom:10px;

}

.footer{

text-align:center;

font-size:15px;

color:gray;

margin-top:40px;

}

.stButton>button{

width:100%;

height:50px;

border-radius:12px;

font-weight:bold;

background:#0E5CAD;

color:white;

border:none;

}

.stButton>button:hover{

background:#1565C0;

color:white;

}

</style>
""", unsafe_allow_html=True)
# ==================================================
# DATABASE
# ==================================================

conn = sqlite3.connect("database.db")

df = pd.read_sql_query(
    "SELECT * FROM patients",
    conn
)

conn.close()

# ==================================================
# DASHBOARD STATISTICS
# ==================================================

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

# Average Age

if len(df) > 0:

    average_age = round(
        df["age"].mean(),
        1
    )

else:

    average_age = 0

# Average Confidence

if len(df["confidence"].dropna()) > 0:

    average_confidence = round(
        df["confidence"].dropna().mean(),
        2
    )

else:

    average_confidence = 0
    # ==================================================
# SIDEBAR
# ==================================================

st.sidebar.title("❤️ HeartCare AI")

st.sidebar.markdown("---")

page = st.sidebar.radio(

    "Navigation",

    [

        "🏠 Dashboard",

        "❤️ Heart Check",

        "📜 History",

        "📄 Medical Report",

        "ℹ️ About"

    ]

)

st.sidebar.markdown("---")

st.sidebar.success(
"""
AI Powered Hospital Management System
"""
)
# ==================================================
# DASHBOARD
# ==================================================

if page == "🏠 Dashboard":

    # ----------------------------------------------
    # HERO SECTION
    # ----------------------------------------------

    st.markdown("""

    <div class='title'>

    ❤️ HeartCare AI

    </div>

    <div class='subtitle'>

    AI Powered Heart Disease Prediction &
    Patient Management System

    </div>

    """, unsafe_allow_html=True)

    st.success(
        "❤️ Early Detection Saves Lives"
    )

    st.write("""

Welcome to **HeartCare AI**.

This application helps hospitals and healthcare professionals
to register patients, predict heart disease using Artificial
Intelligence, manage patient records and generate professional
medical reports.

""")

    st.markdown("---")

    # ----------------------------------------------
    # DASHBOARD ANALYTICS
    # ----------------------------------------------

    st.markdown(
        "<div class='section'>📊 Dashboard Analytics</div>",
        unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns(3)

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

    c4, c5, c6 = st.columns(3)

    with c4:

        st.metric(
            "⏳ Pending",
            pending
        )

    with c5:

        st.metric(
            "🎂 Average Age",
            average_age
        )

    with c6:

        st.metric(
            "❤️ Avg Confidence",
            f"{average_confidence}%"
        )

    st.markdown("---")
        # ==================================================
    # ANALYTICS CHARTS
    # ==================================================

    st.markdown(
        "<div class='section'>📈 Dashboard Analytics</div>",
        unsafe_allow_html=True
    )

    left, right = st.columns(2)

    # ----------------------------------------------
    # Risk Distribution
    # ----------------------------------------------

    with left:

        st.subheader("❤️ Risk Distribution")

        risk_chart = pd.DataFrame(

            {

                "Patients":[

                    high_risk,

                    low_risk,

                    pending

                ]

            },

            index=[

                "High Risk",

                "Low Risk",

                "Pending"

            ]

        )

        st.bar_chart(risk_chart)

    # ----------------------------------------------
    # Gender Distribution
    # ----------------------------------------------

    with right:

        st.subheader("👨 Gender Distribution")

        if len(df) > 0:

            gender_chart = (

                df["gender"]

                .fillna("Unknown")

                .value_counts()

            )

            st.bar_chart(gender_chart)

        else:

            st.info("No patient data available.")

    st.markdown("")

    left, right = st.columns(2)

    # ----------------------------------------------
    # Age Distribution
    # ----------------------------------------------

    with left:

        st.subheader("🎂 Age Distribution")

        if len(df) > 0:

            age_chart = pd.cut(

                df["age"],

                bins=[0,20,30,40,50,60,120],

                labels=[

                    "0-20",

                    "21-30",

                    "31-40",

                    "41-50",

                    "51-60",

                    "60+"

                ]

            ).value_counts().sort_index()

            st.bar_chart(age_chart)

        else:

            st.info("No patient data available.")

    # ----------------------------------------------
    # Average Confidence
    # ----------------------------------------------

    with right:

        st.subheader("❤️ Average Prediction Confidence")

        confidence_chart = pd.DataFrame(

            {

                "Confidence":[

                    average_confidence

                ]

            },

            index=["Average"]

        )

        st.bar_chart(confidence_chart)

    st.markdown("---")    # ==================================================
    # RECENT PATIENTS
    # ==================================================

    st.markdown(
        "<div class='section'>🩺 Recent Patients</div>",
        unsafe_allow_html=True
    )

    if total_patients == 0:

        st.info("No patients have been registered yet.")

    else:

        recent_patients = df.sort_values(
            by="registration_date",
            ascending=False
        )

        display_df = recent_patients[[
            "patient_id",
            "full_name",
            "gender",
            "age",
            "prediction",
            "confidence"
        ]].copy()

        display_df.insert(
            0,
            "S.No",
            range(1, len(display_df) + 1)
        )

        st.dataframe(

            display_df.head(10),

            use_container_width=True,

            hide_index=True

        )

    st.markdown("---")

    # ==================================================
    # QUICK ACTIONS
    # ==================================================

    st.markdown(
        "<div class='section'>🏥 Quick Actions</div>",
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    # ----------------------------------------------
    # Register Patient
    # ----------------------------------------------

    with col1:

        with st.container(border=True):

            st.subheader("👤 Register Patient")

            st.write(
                "Register a new patient before performing heart disease prediction."
            )

            st.write("✔ Personal Information")
            st.write("✔ Contact Details")
            st.write("✔ Medical History")
            st.write("✔ Emergency Contact")

            if st.button(
                "👤 Register New Patient",
                use_container_width=True
            ):

                st.switch_page(
                    "pages/Register_Patient.py"
                )

    # ----------------------------------------------
    # Heart Check
    # ----------------------------------------------

    with col2:

        with st.container(border=True):

            st.subheader("❤️ Heart Disease Prediction")

            st.write(
                "Predict heart disease using Artificial Intelligence."
            )

            st.write("✔ Clinical Parameters")
            st.write("✔ AI Prediction")
            st.write("✔ Confidence Score")
            st.write("✔ AI Recommendation")

            if st.button(
                "❤️ Start Prediction",
                use_container_width=True
            ):

                st.switch_page(
                    "pages/Heart_Check.py"
                )

    st.markdown("")

    col3, col4 = st.columns(2)

    # ----------------------------------------------
    # Patient History
    # ----------------------------------------------

    with col3:

        with st.container(border=True):

            st.subheader("📜 Patient History")

            st.write(
                "View and manage patient history."
            )

            st.write("✔ Search Patients")
            st.write("✔ Risk Filter")
            st.write("✔ Delete Patient")
            st.write("✔ Export CSV")

            if st.button(
                "📜 Open History",
                use_container_width=True
            ):

                st.switch_page(
                    "pages/History.py"
                )

    # ----------------------------------------------
    # Medical Report
    # ----------------------------------------------

    with col4:

        with st.container(border=True):

            st.subheader("📄 Medical Report")

            st.write(
                "Generate professional hospital reports."
            )

            st.write("✔ Professional PDF")
            st.write("✔ QR Code")
            st.write("✔ AI Recommendation")
            st.write("✔ Download Report")

            if st.button(
                "📄 Open Report",
                use_container_width=True
            ):

                st.switch_page(
                    "pages/Medical_Report.py"
                )

    st.markdown("---")
        # ==================================================
    # HEART HEALTH TIPS
    # ==================================================

    st.markdown(
        "<div class='section'>❤️ Heart Health Tips</div>",
        unsafe_allow_html=True
    )

    left, right = st.columns(2)

    with left:

        st.success("""
🥗 Eat a balanced diet

🏃 Exercise at least 30 minutes daily

💧 Drink enough water

😴 Sleep 7–8 hours every night

⚖ Maintain a healthy body weight
""")

    with right:

        st.success("""
🚭 Avoid Smoking

🍺 Limit Alcohol Consumption

🧘 Reduce Stress

🩺 Monitor Blood Pressure

❤️ Get Regular Heart Check-ups
""")

    st.markdown("---")

    # ==================================================
    # EMERGENCY CONTACTS
    # ==================================================

    st.markdown(
        "<div class='section'>🚑 Emergency Contacts</div>",
        unsafe_allow_html=True
    )

    e1, e2, e3, e4 = st.columns(4)

    with e1:
        st.metric("🚑 Ambulance", "108")

    with e2:
        st.metric("🆘 Emergency", "112")

    with e3:
        st.metric("🩸 Blood Bank", "104")

    with e4:
        st.metric("👨‍⚕ Hospital", "24×7")

    st.markdown("---")

    # ==================================================
    # IMPORTANT NOTICE
    # ==================================================

    st.markdown(
        "<div class='section'>📢 Health Notice</div>",
        unsafe_allow_html=True
    )

    st.warning("""
HeartCare AI is an Artificial Intelligence based decision support system.

⚠ The prediction generated by this application **is not a final medical diagnosis.**

Always consult a qualified cardiologist before making medical decisions.
""")

    st.markdown("---")

    # ==================================================
    # CONTACT
    # ==================================================

    st.markdown(
        "<div class='section'>📞 Contact Information</div>",
        unsafe_allow_html=True
    )

    c1, c2 = st.columns(2)

    with c1:

        st.info("""
📧 support@heartcareai.com

📞 +91-9876543210

🌐 www.heartcareai.com
""")

    with c2:

        st.info("""
🏥 HeartCare AI Hospital

📍 Hyderabad, Telangana

🕒 24 × 7 Support
""")

    st.markdown("---")

    # ==================================================
    # FOOTER
    # ==================================================

    st.markdown("""
<div class='footer'>

<hr>

<h3 style="color:#0E5CAD;">
❤️ HeartCare AI
</h3>

<p>
AI Powered Heart Disease Prediction &
Patient Management System
</p>

<p>
Developed by <b>Shivamani Rao</b>
</p>

<p style="color:gray;">
© 2026 HeartCare AI. All Rights Reserved.
</p>

</div>
""", unsafe_allow_html=True)
