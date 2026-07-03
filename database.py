import sqlite3
import os

# --------------------------------------------------
# DATABASE CONNECTION
# --------------------------------------------------

DB_NAME = "database.db"

print("Connected Database:", os.path.abspath(DB_NAME))

conn = sqlite3.connect(DB_NAME, check_same_thread=False)

cursor = conn.cursor()

# --------------------------------------------------
# CREATE TABLE
# --------------------------------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS patients(

    patient_id TEXT PRIMARY KEY,

    full_name TEXT,
    gender TEXT,
    dob TEXT,
    age INTEGER,
    blood_group TEXT,
    marital_status TEXT,
    occupation TEXT,

    mobile TEXT,
    email TEXT,
    address TEXT,
    city TEXT,
    state TEXT,
    pincode TEXT,

    guardian_name TEXT,
    relationship TEXT,
    emergency_mobile TEXT,
    emergency_email TEXT,

    height REAL,
    weight REAL,
    bmi REAL,

    blood_pressure TEXT,
    heart_rate INTEGER,
    diabetes TEXT,
    smoking TEXT,
    alcohol TEXT,
    family_history TEXT,

    allergies TEXT,
    medications TEXT,
    past_history TEXT,
    chief_complaint TEXT,

    cp TEXT,
    trestbps INTEGER,
    chol INTEGER,
    fbs TEXT,
    restecg TEXT,
    thalach INTEGER,
    exang TEXT,
    oldpeak REAL,
    slope TEXT,
    ca INTEGER,
    thal TEXT,

    prediction TEXT,
    confidence REAL,

    registration_date TEXT,
    registration_time TEXT

)
""")

conn.commit()
# --------------------------------------------------
# SAVE PATIENT
# --------------------------------------------------

def save_patient(data):

    try:

        cursor.execute(
            "INSERT INTO patients VALUES ({})".format(",".join(["?"] * 46)),
            data
        )

        conn.commit()

        print("✅ Patient Saved Successfully")

    except Exception as e:

        print("Database Error:", e)
        print("Values Supplied:", len(data))
        raise


# --------------------------------------------------
# GET ALL PATIENTS
# --------------------------------------------------

def get_patients():

    cursor.execute(
        """
        SELECT *
        FROM patients
        ORDER BY rowid DESC
        """
    )

    return cursor.fetchall()


# --------------------------------------------------
# GET LATEST PATIENT
# --------------------------------------------------

def latest_patient():

    cursor.execute(
        """
        SELECT *
        FROM patients
        ORDER BY rowid DESC
        LIMIT 1
        """
    )

    return cursor.fetchone()
    # --------------------------------------------------
# UPDATE PREDICTION
# --------------------------------------------------

def update_prediction(
    patient_id,
    prediction,
    confidence
):

    cursor.execute(
        """
        UPDATE patients
        SET
            prediction = ?,
            confidence = ?
        WHERE patient_id = ?
        """,
        (
            prediction,
            confidence,
            patient_id
        )
    )

    conn.commit()


# --------------------------------------------------
# SAVE CLINICAL PARAMETERS
# --------------------------------------------------

def save_clinical_parameters(

    patient_id,
    cp,
    trestbps,
    chol,
    fbs,
    restecg,
    thalach,
    exang,
    oldpeak,
    slope,
    ca,
    thal

):

    cursor.execute(
        """
        UPDATE patients
        SET

            cp = ?,
            trestbps = ?,
            chol = ?,
            fbs = ?,
            restecg = ?,
            thalach = ?,
            exang = ?,
            oldpeak = ?,
            slope = ?,
            ca = ?,
            thal = ?

        WHERE patient_id = ?
        """,
        (
            cp,
            trestbps,
            chol,
            fbs,
            restecg,
            thalach,
            exang,
            oldpeak,
            slope,
            ca,
            thal,
            patient_id
        )
    )

    conn.commit()
    # --------------------------------------------------
# GET PATIENT BY ID
# --------------------------------------------------

def get_patient_by_id(patient_id):

    cursor.execute(
        """
        SELECT *
        FROM patients
        WHERE patient_id = ?
        """,
        (patient_id,)
    )

    return cursor.fetchone()


# --------------------------------------------------
# DELETE PATIENT
# --------------------------------------------------

def delete_patient(patient_id):

    cursor.execute(
        """
        DELETE FROM patients
        WHERE patient_id = ?
        """,
        (patient_id,)
    )

    conn.commit()

    print("✅ Patient Deleted Successfully")


# --------------------------------------------------
# SHOW TABLE COLUMNS
# --------------------------------------------------

def show_columns():

    cursor.execute("PRAGMA table_info(patients)")

    return cursor.fetchall()


# --------------------------------------------------
# CLOSE DATABASE
# --------------------------------------------------

def close_connection():

    conn.close()