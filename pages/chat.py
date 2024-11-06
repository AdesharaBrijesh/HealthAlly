import streamlit as st
import pandas as pd
from pymongo import MongoClient
from datetime import datetime
from config import MONGO_URI

# MongoDB connection
client = MongoClient(MONGO_URI)
db = client["healthcare_chatbot"]
first_aid_rooms_collection = db["first_aid_rooms"]
chat_history_collection = db["chat_history"]

# Load the symptom diagnosis data from CSV
data = pd.read_csv('data/data.csv')

# Check if user is logged in
def is_logged_in():
    return 'user_id' in st.session_state and 'logged_in' in st.session_state and st.session_state['logged_in']

# Fetch first aid room details based on department
def get_first_aid_room(department):
    return first_aid_rooms_collection.find_one({"department": department})

# Save conversation automatically
def save_chat_to_db(user_id, message, role="user"):
    chat_history_collection.insert_one({
        "user_id": user_id,
        "message": message,
        "role": role,
        "timestamp": datetime.now()
    })

# Display messages with formatting
def display_message(role, message):
    if role == "user":
        st.write(f"You: {message}")
    else:
        st.write(f"**HealthAlly**: {message}")

# Diagnose based on symptoms
def diagnose_symptoms(symptoms):
    matched_rows = data[data['Symptom'].str.contains(symptoms, case=False, na=False)]
    if matched_rows.empty:
        return None, None, None, None
    condition = matched_rows.iloc[0]['Condition']
    treatment = matched_rows.iloc[0]['Treatment']
    precaution = matched_rows.iloc[0]['Precaution']
    medicine = matched_rows.iloc[0]['Medicine']
    return condition, treatment, precaution, medicine

# Find alternative locations for medicine
def find_alternative_locations(medicine):
    alternative_departments = []
    # Split the medicine names by '+' and search for each
    medicines_list = medicine.split(' + ')
    for room in first_aid_rooms_collection.find():
        medicines = {med['name']: med['quantity'] for med in room["first_aid_room"]["medicines"]}
        # Check if any of the medicines in the list are available
        if any(med in medicines for med in medicines_list):
            alternative_departments.append(room['department'])
    return alternative_departments

# Main chat function
def chat_page():
    if not is_logged_in():
        st.warning("Please log in to access the chat.")
        return

    st.title("Health Chatbot")

    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # Department selection
    selected_department = st.selectbox("Select Department", [
        "AMPICS", "BSPP", "CCE", "CHAS", "CHSS", "CMEC", "CMS", "CMSR", "DCS", "DMARI", "DSW",
        "GNUR", "ICT", "IOA", "IOD", "IOO", "IOP", "IOT", "JIM", "KBION", "KKIASR", "MUIS",
        "SKPCPER", "UVPCE", "VMPCMS", "VMPIM", "GANPAT VIDHYALAY", "SMGPSS"
    ])

    symptoms = st.text_input("Describe your symptoms:")
    duration = st.number_input("How many days have these symptoms lasted?", min_value=0)

    if st.button("Submit Symptoms"):
        if symptoms:
            st.session_state.messages.append({"role": "user", "content": symptoms})
            save_chat_to_db(st.session_state["user_id"], symptoms, "user")

            # Diagnose symptoms based on the CSV data
            condition, treatment, precaution, medicine = diagnose_symptoms(symptoms)

            if condition is None:
                response = "I'm sorry, I couldn't find a match for your symptoms."
            else:
                response = (
                    f"It seems you may have **{condition}**. Here are some recommendations:\n\n"
                    f"- **Precautions:** {precaution}\n"
                    f"- **Treatment:** {treatment}\n"
                    f"- **Suggested Medicine(s):** {medicine.replace(' + ', ', ')}\n"
                )
            st.session_state.messages.append({"role": "assistant", "content": response})
            save_chat_to_db(st.session_state["user_id"], response, "assistant")

            # Fetch the first aid room for the selected department
            first_aid_room = get_first_aid_room(selected_department)
            if first_aid_room:
                available_medicines = {med['name']: med['quantity'] for med in first_aid_room["first_aid_room"]["medicines"]}

                # Check if any of the medicines (split by '+') are available
                medicines_list = medicine.split(' + ')
                available_in_dept = any(med in available_medicines for med in medicines_list)

                if available_in_dept:
                    location_info = (
                        f"Location: {first_aid_room['first_aid_room']['room_number']}\n"
                        f"Faculty in Charge: {first_aid_room['first_aid_room']['faculty_in_charge']['name']}\n"
                        f"Contact: {first_aid_room['first_aid_room']['faculty_in_charge']['contact']}"
                    )
                    availability_response = (
                        f"You can find **{medicine.replace(' + ', ', ')}** in the first aid room at:\n{location_info}"
                    )
                else:
                    alternative_locations = find_alternative_locations(medicine)
                    if alternative_locations:
                        availability_response = (
                            f"Unfortunately, **{medicine.replace(' + ', ', ')}** is not available in the {selected_department} first aid room. "
                            f"You may find it in the following departments: {', '.join(alternative_locations)}."
                        )
                    else:
                        availability_response = f"**{medicine.replace(' + ', ', ')}** is currently not available in any department first aid room. Please consult a doctor if symptoms persist."

                st.session_state.messages.append({"role": "assistant", "content": availability_response})
                save_chat_to_db(st.session_state["user_id"], availability_response, "assistant")
            else:
                no_record_response = (
                    f"Unfortunately, there are no first aid room records available for the {selected_department} department. "
                    "Please consider consulting a doctor for further assistance."
                )
                st.session_state.messages.append({"role": "assistant", "content": no_record_response})
                save_chat_to_db(st.session_state["user_id"], no_record_response, "assistant")

            # Provide guidance based on duration
            if duration == 0 or duration == 1:
                duration_advice = (
                    "Since this is your first day experiencing symptoms, it may not be a serious concern yet. "
                    "Keep an eye on your symptoms, and follow the suggested precautions."
                )
            elif duration == 2:
                duration_advice = (
                    "If your symptoms continue, keep monitoring and taking the recommended precautions. "
                    "If symptoms worsen, consider consulting a doctor."
                )
            else:
                duration_advice = (
                    "Since your symptoms have persisted for more than 2 days, it's advisable to consult a doctor soon. "
                    "You can navigate to the appointment booking page from the sidebar."
                )
            st.session_state.messages.append({"role": "assistant", "content": duration_advice})
            save_chat_to_db(st.session_state["user_id"], duration_advice, "assistant")

            # Display end-of-chat message
            end_of_chat_message = (
                "Thank you for using **HealthAlly**. Take care of yourself, and feel free to start a new conversation if needed. "
                "Remember, if symptoms persist or worsen, it's always best to consult a healthcare professional."
            )
            st.session_state.messages.append({"role": "assistant", "content": end_of_chat_message})
            save_chat_to_db(st.session_state["user_id"], end_of_chat_message, "assistant")

            # Display all messages in a structured format
            for message in st.session_state.messages:
                display_message(message["role"], message["content"])

            # "New Conversation" button to clear chat history
            if st.button("New Conversation"):
                st.session_state.messages = []

# Run the chat page
if __name__ == "__main__":
    chat_page()

# Sidebar footer
st.sidebar.markdown("---")
st.sidebar.text("MyHealthAlly © 2024")
st.sidebar.text("All rights reserved.")
