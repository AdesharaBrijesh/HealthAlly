import streamlit as st
from pymongo import MongoClient
from datetime import datetime, timedelta
import random
from config import MONGO_URI

# MongoDB connection
client = MongoClient(MONGO_URI)
db = client["healthcare_chatbot"]
users_collection = db["users"]
doctors_collection = db["doctors"]
appointments_collection = db["appointments"]

# Check if user is logged in
def is_logged_in():
    return 'user_id' in st.session_state and 'logged_in' in st.session_state and st.session_state['logged_in']

# Fetch user data if logged in
def fetch_user_data():
    if is_logged_in():
        user_id = st.session_state['user_id']
        user_data = users_collection.find_one({"_id": user_id})
        return user_data
    return None

# Fetch doctors based on specialization and availability
def fetch_doctors(specialization=None):
    if specialization:
        doctors = doctors_collection.find({"specialization": specialization, "availability_days": {"$ne": []}})
    else:
        doctors = doctors_collection.find({"availability_days": {"$ne": []}})
    
    return [
        {
            "id": str(doc["_id"]),
            "name": doc["name"],
            "qualification": doc["qualification"],
            "specialization": doc["specialization"],
            "work_hours": {
                "start_time": doc["work_hours"]["start_time"],
                "end_time": doc["work_hours"]["end_time"]
            },
            "availability_days": doc["availability_days"]
        }
        for doc in doctors
    ]

# Get available slots for selected doctor and date
def get_available_slots(doctor, date_str):
    start_time = datetime.strptime(doctor["work_hours"]["start_time"], "%I:%M %p")
    end_time = datetime.strptime(doctor["work_hours"]["end_time"], "%I:%M %p")
    
    slots = []
    current_time = start_time
    while current_time + timedelta(minutes=15) <= end_time:
        slot = f"{current_time.strftime('%I:%M %p')} - {(current_time + timedelta(minutes=15)).strftime('%I:%M %p')}"
        
        existing_appointment = appointments_collection.find_one({
            "doctor_id": doctor["id"],
            "date": date_str,
            "time_slot": slot
        })
        
        if not existing_appointment:
            slots.append(slot)
        
        current_time += timedelta(minutes=15)
    
    return slots

# Appointment booking function
def appointment_booking():
    st.set_page_config(page_title="Book an Appointment", page_icon="💉", layout="wide")
    
    st.title("💼 Book Your Appointment")

    # User data fetch if logged in
    user_data = fetch_user_data() if is_logged_in() else None
    
    st.markdown("<hr>", unsafe_allow_html=True)

    # Appointment Details Section
    st.header("📋 Appointment Details")

    # Pre-fill user data if available
    name = st.text_input("Name", user_data.get("username") if user_data else "")
    enrollment_number = st.text_input("Enrollment Number", user_data.get("enrollment_number") if user_data else "", max_chars=11)
    hosteller_status = st.radio("Are you a Hosteller or Commuter?", ["Hosteller", "Commuter"], index=0 if user_data and user_data.get("hostel") else 1)

    hostel = ""
    if hosteller_status == "Hosteller":
        hostel = st.selectbox("Select Hostel", [
            "B1 TOWER HOSTEL", "HOSTEL BLOCK - A", "HOSTEL BLOCK - B", "HOSTEL BLOCK - C", 
            "HOSTEL BLOCK - D", "HOSTEL BLOCK - E", "HOSTEL BLOCK - F", "HOSTEL BLOCK - G", 
            "HOSTEL BLOCK - H", "HOSTEL BLOCK - K", "HOSTEL BLOCK - L", "HOSTEL BLOCK - M", 
            "HOSTEL BLOCK - N", "HOSTEL-UMA(400)", "I.M.J SARVA VIDHYALAY - BALOL", 
            "KVK FARMERS HOSTEL", "MARINE HOSTEL BLOCK - A", "MARINE HOSTEL BLOCK - B", 
            "MARINE HOSTEL BLOCK - C", "N G INTERNATIONAL SCHOOL", "NAYI HOSTEL (MULSAN)", 
            "PARA KELAVANI MANDAL-MEHSANA", "RAMPURA HOSTEL", "SERVANT QUARTER HOSTEL", 
            "VISHWA HOSTEL", "GITANJALI BLOCK - 1", "GITANJALI BLOCK - 2", "ANMOL HEIGHTS HOSTEL", 
            "GIRLS EXECUTIVE A1", "GIRLS EXECUTIVE A2", "Virtuous"
        ])
    
    contact_number = st.text_input("Contact Number (+91)", user_data.get("contact_number") if user_data else "", max_chars=10)
    selected_department = st.selectbox("College/Department", ["AMPICS", "BSPP", "CCE", "CHAS", "CHSS", "CMEC", "CMS", "CMSR", "DCS", "DMARI", "DSW", "GNUR", "ICT", "IOA", "IOD", "IOO", "IOP", "IOT", "JIM", "KBION", "KKIASR", "MUIS", "SKPCPER", "UVPCE", "VMPCMS", "VMPIM", "GANPAT VIDHYALAY", "SMGPSS"], index=0)

    disease = st.text_input("Disease/Condition")

    # Option to select general or custom doctor
    doctor_type = st.radio("Doctor Type", ["Select Custom Doctor", "Any General Doctor"], index=0)

    if doctor_type == "Select Custom Doctor":
        doctors = fetch_doctors()
    else:
        doctors = fetch_doctors(specialization="General")

    # Doctor dropdown
    doctor_names = [f"{doc['name']} - {doc['specialization']} ({doc['work_hours']['start_time']} - {doc['work_hours']['end_time']})" for doc in doctors]
    selected_doctor = st.selectbox("Select Doctor", doctor_names)
    selected_doctor_data = doctors[doctor_names.index(selected_doctor)]

    # Date selection
    selected_date = st.date_input("Select Appointment Date", min_value=datetime.today())
    
    if selected_date.strftime("%A") not in selected_doctor_data["availability_days"]:
        st.warning(f"The selected doctor is not available on {selected_date.strftime('%A')}. Please choose another date.")
        return

    # Available time slots for the selected doctor and date
    available_slots = get_available_slots(selected_doctor_data, selected_date.strftime("%Y-%m-%d"))
    if available_slots:
        time_slot = st.selectbox("Select Time Slot", available_slots)
    else:
        st.warning("No available time slots for this doctor on the selected date.")
        return

    # Check if all required fields are filled
    if not all([name, enrollment_number, contact_number, disease, time_slot]):
        st.warning("All fields are required to book an appointment. Please fill in all details.")
        return

    # Book appointment button
    if st.button("📅 Book Appointment"):
        appointment_data = {
            "name": name,
            "enrollment_number": enrollment_number,
            "hosteller": hosteller_status,
            "hostel": hostel if hosteller_status == "Hosteller" else "Commuter",
            "contact_number": f"+91{contact_number}",
            "college": selected_department,
            "doctor_id": selected_doctor_data["id"],
            "doctor_name": selected_doctor_data["name"],
            "doctor_specialization": selected_doctor_data["specialization"],
            "doctor_work_hours": f"{selected_doctor_data['work_hours']['start_time']} - {selected_doctor_data['work_hours']['end_time']}",
            "disease": disease,
            "date": selected_date.strftime("%Y-%m-%d"),
            "time_slot": time_slot,
            "appointment_time": datetime.now()
        }
        
        # Insert appointment into database
        appointments_collection.insert_one(appointment_data)
        st.success("Appointment booked successfully! 🎉")
        
        # Show appointment summary
        st.subheader("📋 Appointment Summary")
        st.write(f"**Name:** {name}")
        st.write(f"**Enrollment Number:** {enrollment_number}")
        st.write(f"**Hosteller Status:** {hosteller_status}")
        if hosteller_status == "Hosteller":
            st.write(f"**Hostel:** {hostel}")
        st.write(f"**Contact Number:** +91{contact_number}")
        st.write(f"**College/Department:** {selected_department}")
        st.write(f"**Doctor:** {selected_doctor_data['name']} ({selected_doctor_data['specialization']})")
        st.write(f"**Doctor's Working Hours:** {selected_doctor_data['work_hours']['start_time']} - {selected_doctor_data['work_hours']['end_time']}")
        st.write(f"**Disease/Condition:** {disease}")
        st.write(f"**Appointment Date:** {selected_date.strftime('%Y-%m-%d')}")
        st.write(f"**Appointment Time:** {time_slot}")


if __name__ == "__main__":
    appointment_booking()