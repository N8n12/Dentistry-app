import streamlit as st
import pandas as pd

# Simulated patient data
patients = [
    {"Name": "Emma Brown", "DOB": "12/05/1985", "Reason": "Routine", "History": "Check-up every 6 months."},
    {"Name": "James Wilson", "DOB": "30/08/1972", "Reason": "Follow-up", "History": "Tooth extraction in 2023."},
    {"Name": "Sarah Davis", "DOB": "14/01/1990", "Reason": "Teeth cleaning", "History": "Scaling every year."},
    {"Name": "David Lee", "DOB": "26/09/1966", "Reason": "Toothache", "History": "Root canal done in 2022."}
]

# Sidebar navigation
st.sidebar.title("Dental Dashboard")
page = st.sidebar.radio("Go to", ["Practice Overview", "Appointments", "Patients", "Prescriptions", "NHS Activity"])

if page == "Practice Overview":
    st.title("Practice Activity")
    col1, col2 = st.columns(2)
    col1.metric("Private", 12)
    col2.metric("NHS", 9)

elif page == "Appointments":
    st.title("Today's Appointments")
    appointments = pd.DataFrame([
        {"Time": "9:00 AM", "Patient": "Emma Brown", "Duration": "30 mins"},
        {"Time": "10:00 AM", "Patient": "James Wilson", "Duration": "30 mins"},
        {"Time": "11:00 AM", "Patient": "Sarah Davis", "Duration": "30 mins"},
        {"Time": "1:00 PM", "Patient": "David Lee", "Duration": "60 mins"}
    ])
    st.dataframe(appointments)

elif page == "Patients":
    st.title("Patient Records")
    selected_name = st.selectbox("Select a patient", [p["Name"] for p in patients])
    patient = next(p for p in patients if p["Name"] == selected_name)
    st.subheader(f"Details for {selected_name}")
    st.write(f"**DOB:** {patient['DOB']}")
    st.write(f"**Visit Reason:** {patient['Reason']}")
    st.write(f"**History:** {patient['History']}")

    st.markdown("---")
    st.subheader("Add Clinical Notes")
    with st.form("clinical_notes_form"):
        notes = st.text_area("Notes")
        submitted = st.form_submit_button("Save Note")
        if submitted:
            st.success("Note saved successfully.")

elif page == "Prescriptions":
    st.title("Digital Prescription")
    with st.form("prescription_form"):
        patient_name = st.selectbox("Select patient", [p["Name"] for p in patients])
        medication = st.text_input("Medication")
        instructions = st.text_area("Dosage & Instructions")
        submitted = st.form_submit_button("Send Prescription")
        if submitted:
            st.success(f"Prescription for {patient_name} sent successfully.")

elif page == "NHS Activity":
    st.title("NHS Activity Log")
    with st.form("nhs_form"):
        nhs_number = st.text_input("Patient NHS Number")
        treatment_type = st.selectbox("Treatment Type", ["Band 1", "Band 2", "Band 3"])
        procedure_notes = st.text_area("Procedure Notes")
        submitted = st.form_submit_button("Submit to NHS")
        if submitted:
            st.success("NHS activity submitted successfully.")
