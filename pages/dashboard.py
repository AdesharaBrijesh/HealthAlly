import streamlit as st
from pymongo import MongoClient
from bson import ObjectId
import pandas as pd
from config import MONGO_URI

# MongoDB connection
client = MongoClient(MONGO_URI)
db = client["healthcare_chatbot"]
users_collection = db["users"]
admins_collection = db["admins"]
appointments_collection = db["appointments"]
chat_history_collection = db["chat_history"]
doctors_collection = db["doctors"]
first_aid_rooms_collection = db["first_aid_rooms"]

# Admin login function
def admin_login():
    st.title("Admin Login")
    st.write("### Please enter your credentials to access the admin dashboard.")
    
    with st.form(key='admin_login_form'):
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')
        submit_button = st.form_submit_button("Login")

    if submit_button:
        admin = admins_collection.find_one({"username": username, "password": password})

        if admin:
            st.session_state.is_admin_logged_in = True
            st.session_state.admin_username = username
            st.success("Login successful! You can now access the dashboard.")
            st.session_state.show_dashboard = True  # Set a flag to show the dashboard
        else:
            st.error("Invalid username or password.")

# Function to fetch and display data from a specified collection
def display_data(collection, title):
    st.subheader(title)
    data = list(collection.find())
    if data:
        st.dataframe(pd.DataFrame(data))  # Display data as a DataFrame
    else:
        st.write(f"No {title.lower()} data available.")

# Function to add a new document to a collection
def add_document(collection, fields):
    st.subheader(f"Add New {fields['name']}")
    with st.form(key=f'add_{fields["name"].lower()}_form'):
        form_data = {}
        for field in fields['fields']:
            form_data[field] = st.text_input(field.capitalize())
        
        submit_button = st.form_submit_button(f"Add {fields['name']}")
        
        if submit_button:
            collection.insert_one(form_data)
            st.success(f"{fields['name']} added successfully!")

# Function to update a document in a collection
def update_document(collection, fields):
    st.subheader(f"Update {fields['name']}")
    document_id = st.text_input(f"Enter {fields['name']} ID to update:")
    
    if document_id:
        document = collection.find_one({"_id": ObjectId(document_id)})
        if document:
            with st.form(key=f'update_{fields["name"].lower()}_form'):
                form_data = {}
                for field in fields['fields']:
                    form_data[field] = st.text_input(field.capitalize(), value=document.get(field, ''))
                
                submit_button = st.form_submit_button(f"Update {fields['name']}")
                
                if submit_button:
                    collection.update_one({"_id": ObjectId(document_id)}, {"$set": form_data})
                    st.success(f"{fields['name']} updated successfully!")
        else:
            st.error(f"No {fields['name'].lower()} found with that ID.")

# Function to delete a document from a collection
def delete_document(collection, fields):
    st.subheader(f"Delete {fields['name']}")
    document_id = st.text_input(f"Enter {fields['name']} ID to delete:")
    if st.button(f"Delete {fields['name']}"):
        if document_id:
            collection.delete_one({"_id": ObjectId(document_id)})
            st.success(f"{fields['name']} deleted successfully!")
        else:
            st.error("Please enter a valid ID.")

# Admin dashboard function
def dashboard_page():
    if 'is_admin_logged_in' not in st.session_state or not st.session_state.is_admin_logged_in:
        admin_login()  # Show login page
    else:
        st.title("Admin Dashboard")
        st.sidebar.header("Admin Options")
        if st.sidebar.button("Logout"):
            st.session_state.is_admin_logged_in = False
            st.success("Logged out successfully!")
            st.experimental_set_query_params()  # Clear any parameters in the URL
            return  # Exit the function to not show the dashboard
        
        # Define the collections and their respective fields
        collections = {
            "Users": (users_collection, ["username", "email", "enrollment_number", "department", "contact_number", "hostel"]),
            "Admins": (admins_collection, ["username", "email"]),
            "Appointments": (appointments_collection, ["user_id", "doctor_id", "date", "time"]),
            "Chat History": (chat_history_collection, ["user_id", "message", "timestamp"]),
            "Doctors": (doctors_collection, ["name", "specialization", "availability"]),
            "First Aid Rooms": (first_aid_rooms_collection, ["room_number", "location", "medicines"]),
        }

        # Create tabs for each collection
        tabs = st.tabs([name for name in collections.keys()])

        # Display data and CRUD operations in each tab
        for i, (name, (collection, fields)) in enumerate(collections.items()):
            with tabs[i]:
                display_data(collection, f"{name} Data")
                add_document(collection, {"name": name, "fields": fields})
                update_document(collection, {"name": name, "fields": fields})
                delete_document(collection, {"name": name})
                

# Run the dashboard page
if __name__ == "__main__":
    dashboard_page()


# Footer at the bottom of the sidebar
st.sidebar.markdown("---")
st.sidebar.text("MyHealthAlly © 2024")
st.sidebar.text("All rights reserved.")