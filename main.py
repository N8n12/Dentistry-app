import streamlit as st
import pandas as pd
from datetime import datetime

# Initialize session state if not already done
if "patients" not in st.session_state:
    st.session_state.patients = [
        {"Name": "Emma Brown", "DOB": "12/05/1985", "Reason": "Routine", "History": "Check-up every 6 months."},
        {"Name": "James Wilson", "DOB": "30/08/1972", "Reason": "Follow-up", "History": "Tooth extraction in 2023."},
        {"Name": "Sarah Davis", "DOB": "14/01/1990", "Reason": "Teeth cleaning", "History": "Scaling every year."},
        {"Name": "David Lee", "DOB": "26/09/1966", "Reason": "Toothache", "History": "Root canal done in 2022."}
    ]
    st.session_state.appointments = [
        {"Time": "9:00 AM", "Patient": "Emma Brown", "Duration": "30 mins", "Date": "2025-04-19"},
        {"Time": "10:00 AM", "Patient": "James Wilson", "Duration": "30 mins", "Date": "2025-04-19"},
        {"Time": "11:00 AM", "Patient": "Sarah Davis", "Duration": "30 mins", "Date": "2025-04-19"},
        {"Time": "1:00 PM", "Patient": "David Lee", "Duration": "60 mins", "Date": "2025-04-19"}
    ]
    st.session_state.prescriptions = []
    st.session_state.nhs_activity = []

# Set up page layout
st.set_page_config(page_title="Dental Dashboard", layout="wide")

# Sidebar navigation
st.sidebar.title("Dental Dashboard")
page = st.sidebar.radio("Navigate", [
    "Practice Overview", 
    "Appointments", 
    "Patients", 
    "Prescriptions", 
    "NHS Activity", 
    "Add Patient", 
    "Analytics"
])

# Helper function for spacing
def vertical_spacer(lines=1):
    for _ in range(lines):
        st.write("\u200b")

if page == "Practice Overview":
    st.title("Practice Activity Overview")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Private Appointments", 12)
    with col2:
        st.metric("Total NHS Appointments", 9)

    st.markdown("---")
    st.subheader("Upcoming Appointments")
    appts = pd.DataFrame(st.session_state.appointments)
    st.table(appts)

elif page == "Appointments":
    st.title("Appointments")
    appointments = pd.DataFrame(st.session_state.appointments)
    st.dataframe(appointments, use_container_width=True)

    # Add new appointment
    st.subheader("Schedule New Appointment")
    with st.form("appointment_form"):
        patient_name = st.selectbox("Select Patient", [p["Name"] for p in st.session_state.patients])
        appointment_time = st.time_input("Time")
        appointment_date = st.date_input("Date", value=datetime.today())
        appointment_duration = st.selectbox("Duration", ["30 mins", "60 mins"])
        submitted = st.form_submit_button("Schedule Appointment")
        if submitted:
            new_appointment = {
                "Time": f"{appointment_time}",
                "Patient": patient_name,
                "Duration": appointment_duration,
                "Date": appointment_date.strftime("%Y-%m-%d")
            }
            st.session_state.appointments.append(new_appointment)
            st.success("Appointment scheduled successfully.")

elif page == "Patients":
    st.title("Patient Records")
    patient_name_search = st.text_input("Search by Name")
    filtered_patients = [p for p in st.session_state.patients if patient_name_search.lower() in p["Name"].lower()]
    
    selected_name = st.selectbox("Select a Patient", [p["Name"] for p in filtered_patients])
    patient = next(p for p in st.session_state.patients if p["Name"] == selected_name)

    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Name:** {patient['Name']}")
        st.write(f"**DOB:** {patient['DOB']}")
        st.write(f"**Reason for Visit:** {patient['Reason']}")
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
            st.success("Clinical note added successfully.")

elif page == "Prescriptions":
    st.title("Prescriptions")
    patient_name = st.selectbox("Select Patient", [p["Name"] for p in st.session_state.patients])
    medication = st.text_input("Medication")
    dosage = st.text_input("Dosage")
    frequency = st.text_input("Frequency (e.g., twice daily)")
    instructions = st.text_area("Additional Instructions")
    
    with st.form("prescription_form"):
        submitted = st.form_submit_button("Submit Prescription")
        if submitted:
            new_prescription = {
                "Patient": patient_name,
                "Medication": medication,
                "Dosage": dosage,
                "Frequency": frequency,
                "Instructions": instructions
            }
            st.session_state.prescriptions.append(new_prescription)
            st.success("Prescription submitted successfully.")

elif page == "NHS Activity":
    st.title("NHS Activity Log")
    nhs_number = st.text_input("Patient NHS Number")
    treatment_type = st.selectbox("Treatment Band", ["Band 1", "Band 2", "Band 3", "Urgent"])
    treatment_date = st.date_input("Treatment Date", value=datetime.today())
    procedure_notes = st.text_area("Procedure Notes")

    with st.form("nhs_activity_form"):
        submitted = st.form_submit_button("Submit NHS Record")
        if submitted:
            new_activity = {
                "NHS Number": nhs_number,
                "Treatment Type": treatment_type,
                "Date of Treatment": treatment_date.strftime("%Y-%m-%d"),
                "Procedure Notes": procedure_notes
            }
            st.session_state.nhs_activity.append(new_activity)
            st.success("NHS activity recorded.")

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

elif page == "Analytics":
    st.title("Practice Analytics")
    
    # Patient visit statistics
    total_visits = len(st.session_state.patients)
    total_appointments = len(st.session_state.appointments)
    total_prescriptions = len(st.session_state.prescriptions)
    
    st.subheader("Total Visits")
    st.write(f"Total number of patient visits: {total_visits}")
    
    st.subheader("Total Appointments")
    st.write(f"Total number of appointments: {total_appointments}")
    
    st.subheader("Prescriptions Overview")
    st.write(f"Total number of prescriptions: {total_prescriptions}")
    
    # Plot appointment trends (simple bar chart)
    appointment_dates = [appt["Date"] for appt in st.session_state.appointments]
    appt_df = pd.DataFrame(appointment_dates, columns=["Date"])
    appt_counts = appt_df.groupby("Date").size().reset_index(name="Appointments")
    st.bar_chart(appt_counts.set_index("Date"))
    
    vertical_spacer(2)

