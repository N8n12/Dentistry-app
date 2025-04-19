import streamlit as st
import pandas as pd
from datetime import datetime
import io
import random

# Initialize session state if not already done
if "patients" not in st.session_state:
    st.session_state.patients = [
        {"Name": "Emma Brown", "DOB": "12/05/1985", "Reason": "Routine", "History": "Check-up every 6 months.", "Allergies": "None", "Treatment History": []},
        {"Name": "James Wilson", "DOB": "30/08/1972", "Reason": "Follow-up", "History": "Tooth extraction in 2023.", "Allergies": "Penicillin", "Treatment History": []},
        {"Name": "Sarah Davis", "DOB": "14/01/1990", "Reason": "Teeth cleaning", "History": "Scaling every year.", "Allergies": "None", "Treatment History": []},
        {"Name": "David Lee", "DOB": "26/09/1966", "Reason": "Toothache", "History": "Root canal done in 2022.", "Allergies": "None", "Treatment History": []}
    ]
    st.session_state.appointments = [
        {"Time": "9:00 AM", "Patient": "Emma Brown", "Duration": "30 mins", "Date": "2025-04-19", "Treatment": "Routine Check-up"},
        {"Time": "10:00 AM", "Patient": "James Wilson", "Duration": "30 mins", "Date": "2025-04-19", "Treatment": "Follow-up extraction"},
        {"Time": "11:00 AM", "Patient": "Sarah Davis", "Duration": "30 mins", "Date": "2025-04-19", "Treatment": "Teeth cleaning"},
        {"Time": "1:00 PM", "Patient": "David Lee", "Duration": "60 mins", "Date": "2025-04-19", "Treatment": "Toothache treatment"}
    ]
    st.session_state.prescriptions = []
    st.session_state.nhs_activity = []
    st.session_state.notes_history = {}  # Store notes history per patient
    st.session_state.bills = []  # Store bills/invoices

# Set up page layout
st.set_page_config(page_title="Dental Dashboard", layout="wide")

# Create tabs using st.tabs
tabs = ["Practice Overview", "Appointments", "Patients", "Prescriptions", "NHS Activity", "Billing", "Add Patient", "Settings"]
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(tabs)

# Main Content for each tab
with tab1:
    st.title("Practice Overview")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Private Appointments", 12)
    with col2:
        st.metric("NHS Appointments", 9)

    st.markdown("---")
    st.subheader("Upcoming Appointments")
    appts = pd.DataFrame(st.session_state.appointments)
    st.table(appts)

with tab2:
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
        treatment_type = st.selectbox("Treatment Type", ["Routine Check-up", "Follow-up", "Teeth Cleaning", "Toothache"])
        submitted = st.form_submit_button("Schedule Appointment")
        if submitted:
            new_appointment = {
                "Time": f"{appointment_time}",
                "Patient": patient_name,
                "Duration": appointment_duration,
                "Date": appointment_date.strftime("%Y-%m-%d"),
                "Treatment": treatment_type
            }
            st.session_state.appointments.append(new_appointment)
            st.success("Appointment scheduled successfully.")

with tab3:
    st.title("Patient Records")
    patient_name_search = st.text_input("Search by Name", key="search_name")
    filtered_patients = [p for p in st.session_state.patients if patient_name_search.lower() in p["Name"].lower()]
    
    selected_name = st.selectbox("Select a Patient", [p["Name"] for p in filtered_patients])
    patient = next(p for p in st.session_state.patients if p["Name"] == selected_name)

    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Name:** {patient['Name']}")
        st.write(f"**DOB:** {patient['DOB']}")
        st.write(f"**Reason for Visit:** {patient['Reason']}")
    with col2:
        st.write(f"**Medical History:**")
        st.info(patient["History"])
        # Use .get() to avoid KeyError in case 'Allergies' is missing
        allergies = patient.get("Allergies", "No allergies recorded")
        st.write(f"**Allergies:** {allergies}")

    st.markdown("---")
    st.subheader("Treatment History")
    if patient["Treatment History"]:
        st.write(patient["Treatment History"])
    else:
        st.write("No treatments recorded for this patient.")
    
    st.subheader("Add Clinical Notes")
    with st.form("clinical_notes_form"):
        note_date = st.date_input("Note Date", value=datetime.today())
        notes = st.text_area("Clinical Notes")
        submitted = st.form_submit_button("Save Note")
        if submitted:
            # Add the new note to the history for the selected patient
            new_note = {
                "Date": note_date.strftime("%Y-%m-%d"),
                "Note": notes
            }
            if selected_name not in st.session_state.notes_history:
                st.session_state.notes_history[selected_name] = []
            st.session_state.notes_history[selected_name].append(new_note)
            st.success("Clinical note added successfully.")
    
    # Export notes to CSV
    if selected_name in st.session_state.notes_history:
        notes_to_export = pd.DataFrame(st.session_state.notes_history[selected_name])
        st.download_button(
            label="Export Notes to CSV",
            data=notes_to_export.to_csv(index=False),
            file_name=f"{selected_name}_notes.csv",
            mime="text/csv"
        )

    # Add new treatment entry
    st.subheader("Add Treatment Record")
    with st.form("add_treatment_form"):
        treatment_date = st.date_input("Treatment Date")
        treatment_type = st.selectbox("Treatment Type", ["Routine Check-up", "Follow-up", "Teeth Cleaning", "Tooth Extraction"])
        treatment_notes = st.text_area("Treatment Notes")
        submitted = st.form_submit_button("Save Treatment")
        if submitted:
            treatment_record = {
                "Date": treatment_date.strftime("%Y-%m-%d"),
                "Treatment Type": treatment_type,
                "Notes": treatment_notes
            }
            patient["Treatment History"].append(treatment_record)
            st.success("Treatment record added successfully.")

with tab4:
    st.title("Prescriptions")
    
    # Select a patient to prescribe
    patient_name = st.selectbox("Select Patient", [p["Name"] for p in st.session_state.patients])

    st.subheader("Create New Prescription")
    with st.form("prescription_form"):
        prescription_medicine = st.text_input("Medicine Name")
        dosage = st.text_input("Dosage")
        instructions = st.text_area("Instructions")
        submitted = st.form_submit_button("Create Prescription")
        if submitted:
            new_prescription = {
                "Patient": patient_name,
                "Medicine": prescription_medicine,
                "Dosage": dosage,
                "Instructions": instructions,
                "Date": datetime.today().strftime("%Y-%m-%d")
            }
            st.session_state.prescriptions.append(new_prescription)
            st.success("Prescription created successfully.")

    # Display prescriptions
    st.subheader("Existing Prescriptions")
    prescriptions_df = pd.DataFrame(st.session_state.prescriptions)
    st.dataframe(prescriptions_df)

with tab5:
    st.title("NHS Activity")
    
    # NHS Activity form
    st.subheader("Add NHS Activity Record")
    with st.form("nhs_activity_form"):
        patient_name = st.selectbox("Select Patient for NHS Activity", [p["Name"] for p in st.session_state.patients])
        activity_type = st.selectbox("Activity Type", ["Consultation", "Treatment", "Follow-up", "Examination"])
        duration = st.number_input("Duration (minutes)", min_value=0)
        submitted = st.form_submit_button("Add NHS Activity")
        if submitted:
            new_activity = {
                "Patient": patient_name,
                "Activity Type": activity_type,
                "Duration": duration,
                "Date": datetime.today().strftime("%Y-%m-%d")
            }
            st.session_state.nhs_activity.append(new_activity)
            st.success("NHS Activity added successfully.")

    # Display NHS Activity
    st.subheader("NHS Activity Records")
    nhs_activity_df = pd.DataFrame(st.session_state.nhs_activity)
    st.dataframe(nhs_activity_df)

with tab6:
    st.title("Billing")
    selected_patient = st.selectbox("Select Patient for Billing", [p["Name"] for p in st.session_state.patients])
    patient = next(p for p in st.session_state.patients if p["Name"] == selected_patient)

    st.subheader(f"Create Invoice for {selected_patient}")
    treatment_type = st.selectbox("Treatment Type", ["Private", "NHS"])
    total_amount = st.number_input("Total Amount", min_value=0.0, format="%.2f")

    with st.form("billing_form"):
        submitted = st.form_submit_button("Generate Bill")
        if submitted:
            new_bill = {
                "Patient": selected_patient,
                "Treatment Type": treatment_type,
                "Amount": total_amount,
                "Date": datetime.today().strftime("%Y-%m-%d")
            }
            st.session_state.bills.append(new_bill)
            st.success("Invoice generated successfully.")

    # Display generated bills
    st.subheader("Generated Invoices")
    bills_df = pd.DataFrame(st.session_state.bills)
    st.dataframe(bills_df)

with tab7:
    st.title("Add New Patient")
    with st.form("add_patient_form"):
        new_name = st.text_input("Full Name")
        new_dob = st.date_input("Date of Birth")
        new_reason = st.selectbox("Reason for Visit", ["Routine", "Follow-up", "Teeth cleaning", "Toothache", "Other"])
        new_history = st.text_area("Medical History")
        new_allergies = st.text_input("Allergies (if any)")

        submitted = st.form_submit_button("Add Patient")
        if submitted:
            new_patient = {
                "Name": new_name,
                "DOB": new_dob.strftime("%d/%m/%Y"),
                "Reason": new_reason,
                "History": new_history,
                "Allergies": new_allergies,
                "Treatment History": []
            }
            st.session_state.patients.append(new_patient)
            st.success(f"Patient {new_name} added successfully.")

with tab8:
    st.title("Practice Settings")
    st.markdown("Configure your practice's details.")
    practice_name = st.text_input("Practice Name", value="Dental Clinic")
    practice_address = st.text_area("Practice Address")
    contact_number = st.text_input("Contact Number")

    with st.form("settings_form"):
        submitted = st.form_submit_button("Save Settings")
        if submitted:
            st.success("Settings saved successfully.")
