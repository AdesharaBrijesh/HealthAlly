import streamlit as st
from datetime import datetime
from pymongo import MongoClient
from config import MONGO_URI

# MongoDB connection
client = MongoClient(MONGO_URI)
db = client["healthcare_chatbot"]
users_collection = db["users"]

# Function to display chat page (dummy function for demonstration)
def chat_page():
    st.title("Login Page")
    st.write(f"Welcome to MyHealthAlly, {st.session_state['username']}!")
    st.write(f"You are already logged in so feel free to explore the features of our app!")

# Login and Signup combined
def login_page():
    st.title("Welcome to MyHealthAlly")

    # Display tabs for login and signup
    tab1, tab2 = st.tabs(["Login", "Signup"])

    # Login tab
    with tab1:
        st.subheader("Login")
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")

        if st.button("Login"):
            # Check if user exists in the database
            user = users_collection.find_one({"username": username, "password": password})
            if user:
                st.session_state['user_id'] = str(user['_id'])
                st.session_state['logged_in'] = True
                st.session_state['username'] = username
                st.success("Logged in successfully!")

                # Set the page to chat in session state
                st.session_state['page'] = "chat"  
                st.rerun()  # Rerun the app to redirect to the chat page
            else:
                st.error("Invalid credentials. Please try again.")

    # Signup tab
    with tab2:
        st.subheader("Signup")
        new_username = st.text_input("Create Username", placeholder="Choose a username")
        email = st.text_input("Email", placeholder="Enter your email")
        new_password = st.text_input("Create Password", type="password", placeholder="Choose a password")
        contact = st.text_input("Contact Number", placeholder="Your contact number")
        enrollment = st.text_input("Enrollment Number", placeholder="Your enrollment number")
        department = st.selectbox("Select Department", [
            "AMPICS", "BSPP", "CCE", "CHAS", "CHSS", "CMEC", "CMS", "CMSR", "DCS", "DMARI", 
            "DSW", "GNUR", "ICT", "IOA", "IOD", "IOO", "IOP", "IOT", "JIM", "KBION", "KKIASR", 
            "MUIS", "SKPCPER", "UVPCE", "VMPCMS", "VMPIM", "GANPAT VIDHYALAY", "SMGPSS", "OTHERS"
        ])
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

        if st.button("Sign Up"):
            # Check if username already exists
            if users_collection.find_one({"username": new_username}):
                st.error("Username already taken. Please choose another.")
            else:
                new_user = {
                    "username": new_username,
                    "email": email,
                    "password": new_password,
                    "contact": contact,
                    "enrollment": enrollment,
                    "department": department,
                    "hostel": hostel,
                    "last_login": datetime.now()
                }
                users_collection.insert_one(new_user)
                st.success("Account created successfully! You can now log in.")

                # Automatically redirect to the chat page after successful signup
                st.session_state['logged_in'] = True
                st.session_state['username'] = new_username
                st.session_state['page'] = "chat"  
                st.rerun()  # Rerun the app to redirect to the chat page
    

# Function to handle logout
def logout():
    st.session_state.logged_in = False
    st.session_state.page = "login"  # Redirect to login page


# Manage page redirection based on session state
if 'logged_in' in st.session_state and st.session_state['logged_in']:
    chat_page()  # Redirect to the chat page if logged in
     # Sidebar for Navigation - Display only if logged in
    if st.session_state.logged_in:
        # Define logout button
        if st.sidebar.button("🚪 Logout"):
            logout()  # Call logout function

else:
    login_page()  # Show login page if not logged in


# Footer at the bottom of the sidebar
st.sidebar.markdown("---")
st.sidebar.text("MyHealthAlly © 2024")
st.sidebar.text("All rights reserved.")