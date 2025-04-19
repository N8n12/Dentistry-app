import streamlit as st
import pandas as pd
from datetime import datetime

# Simulated patient data
if "patients" not in st.session_state:
    st.session_state.patients = [
        {"Name": "Emma Brown", "DOB": "12/05/1985", "Reason": "Routine", "History": "Check-up every 6 months."},
        {"Name": "James Wilson", "DOB": "30/08/1972", "Reason": "Follow-up", "History": "Tooth extraction in 2023."},
        {"Name": "Sarah Davis", "DOB": "14/01/1990", "Reason": "Teeth cleaning", "History": "Scaling every year."},
        {"Name": "David Lee", "DOB": "26/09/1966", "Reason": "Toothache", "History": "Root canal done in 2022."}
    ]

# Set up page layout
st.set_page_config(page_title="Dental Dashboard", layout="wide")

# Sidebar navigation
st.sidebar.title("Dental Dashboard")
page = st.sidebar.radio("Navigate", ["Practice Overview", "Appointments", "Patients", "Prescriptions", "NHS Activity", "Add Patient"])

# Helper function for spacing
def vertical_spacer(lines=1):
    for _ in range(lines):
        st.write("\u200b")

if page == "Practice Overview":
    st.title("Practice Activity Summary")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Private Appointments", 12)
    with col2:
        st.metric("NHS Appointments", 9)

    st.markdown("---")
    st.subheader("Upcoming Appointments")
    appts = pd.DataFrame([
        {"Time": "9:00 AM", "Patient": "Emma Brown", "Duration": "30 mins"},
        {"Time": "10:00 AM", "Patient": "James Wilson", "Duration": "30 mins"},
        {"Time": "11:00 AM", "Patient": "Sarah Davis", "Duration": "30 mins"},
        {"Time": "1:00 PM", "Patient": "David Lee", "Duration": "60 mins"}
    ])
    st.table(appts)

elif page == "Appointments":
    st.title("Today's Appointments")
    appointments = pd.DataFrame([
        {"Time": "9:00 AM", "Patient": "Emma Brown", "Duration": "30 mins"},
        {"Time": "10:00 AM", "Patient": "James Wilson", "Duration": "30 mins"},
        {"Time": "11:00 AM", "Patient": "Sarah Davis", "Duration": "30 mins"},
        {"Time": "1:00 PM", "Patient": "David Lee", "Duration": "60 mins"}
    ])
    st.dataframe(appointments, use_container_width=True)

elif page == "Patients":
    st.title("Patient Records")
    selected_name = st.selectbox("Select a patient", [p["Name"] for p in st.session_state.patients])
    patient = next(p for p in st.session_state.patients if p["Name"] == selected_name)

    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Name:** {patient['Name']}")
        st.write(f"**DOB:** {patient['DOB']}")
        st.write(f"**Visit Reason:** {patient['Reason']}")
    with col2:
        st.write(f"**History:**")
        st.info(patient["History"])

    st.markdown("---")
    st.subheader("Add Clinical Notes")
    with st.form("clinical_notes_form"):
        note_date = st.date_input("Note Date", value=datetime.today())
        notes = st.text_area("Clinical Notes")
        submitted = st.form_submit_button("Save Note")
        if submitted:
            st.success("Note saved successfully.")

elif page == "Prescriptions":
    st.title("Create Digital Prescription")
    with st.form("prescription_form"):
        col1, col2 = st.columns(2)
        with col1:
            patient_name = st.selectbox("Patient Name", [p["Name"] for p in st.session_state.patients])
            medication = st.text_input("Medication")
        with col2:
            dosage = st.text_input("Dosage")
            frequency = st.text_input("Frequency (e.g., twice daily)")

        additional_instructions = st.text_area("Additional Instructions")
        submitted = st.form_submit_button("Send Prescription")
        if submitted:
            st.success(f"Prescription for {patient_name} submitted.")

elif page == "NHS Activity":
    st.title("Log NHS Activity")
    with st.form("nhs_activity_form"):
        nhs_number = st.text_input("Patient NHS Number")
        treatment_type = st.selectbox("Treatment Band", ["Band 1", "Band 2", "Band 3", "Urgent"])
        date_of_treatment = st.date_input("Date of Treatment", value=datetime.today())
        procedure_details = st.text_area("Procedure Notes")

        submitted = st.form_submit_button("Submit NHS Record")
        if submitted:
            st.success("NHS treatment record submitted.")

elif page == "Add Patient":
    st.title("Add New Patient")
    with st.form("add_patient_form"):
        new_name = st.text_input("Full Name")
        new_dob = st.date_input("Date of Birth")
        new_reason = st.selectbox("Reason for Visit", ["Routine", "Follow-up", "Teeth cleaning", "Toothache", "Other"])
        new_history = st.text_area("Medical History")

        submitted = st.form_submit_button("Add Patient")
        if submitted:
            new_patient = {
                "Name": new_name,
                "DOB": new_dob.strftime("%d/%m/%Y"),
                "Reason": new_reason,
                "History": new_history
            }
            st.session_state.patients.append(new_patient)
            st.success(f"Patient {new_name} added successfully.")

st.markdown("""
<style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)
