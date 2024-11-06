import streamlit as st
from pymongo import MongoClient
from PIL import Image
from bson import ObjectId
from config import MONGO_URI

# MongoDB connection
client = MongoClient(MONGO_URI)
db = client["healthcare_chatbot"]
users_collection = db["users"]

def is_logged_in():
    return 'user_id' in st.session_state and 'logged_in' in st.session_state and st.session_state['logged_in']

def profile_page():
    if not is_logged_in():
        st.warning("Please log in to view your profile.")
        return

    user = users_collection.find_one({"_id": ObjectId(st.session_state['user_id'])})

    if user:
        st.title("👤 User Profile")
        profile_pic = user.get('profile_image', None)

        # Display profile picture
        if profile_pic:
            st.image(profile_pic, width=150)
        else:
            placeholder = Image.new('RGB', (150, 150), color=(200, 200, 200))
            st.image(placeholder, caption='Default Profile Picture', width=150)

        # Upload new profile picture
        uploaded_file = st.file_uploader("Upload your profile picture:", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            image = Image.open(uploaded_file).resize((150, 150))
            st.image(image, caption='Profile Picture', use_column_width=True)

            # Save the uploaded image to MongoDB
            users_collection.update_one({"_id": ObjectId(st.session_state['user_id'])}, {"$set": {"profile_image": uploaded_file.getvalue()}})
            st.success("Profile picture updated successfully!")

        # User details
        st.subheader("Your Details")
        new_email = st.text_input("Email", value=user.get('email'))
        new_contact = st.text_input("Contact Number", value=user.get('contact'))
        new_department = st.selectbox("Select Department", [
            "AMPICS", "BSPP", "CCE", "CHAS", "CHSS", "CMEC", "CMS", "CMSR", "DCS", 
            "DMARI", "DSW", "GNUR", "ICT", "IOA", "IOD", "IOO", "IOP", "IOT", "JIM", 
            "KBION", "KKIASR", "MUIS", "SKPCPER", "UVPCE", "VMPCMS", "VMPIM", 
            "GANPAT VIDHYALAY", "SMGPSS", "OTHERS"
        ])
        new_hostel = st.selectbox("Select Hostel", [
            "B1 TOWER HOSTEL", "HOSTEL BLOCK - A", "HOSTEL BLOCK - B", "HOSTEL BLOCK - C", 
            "HOSTEL BLOCK - D", "HOSTEL BLOCK - E", "HOSTEL BLOCK - F", "HOSTEL BLOCK - G", 
            "HOSTEL BLOCK - H", "HOSTEL BLOCK - K", "HOSTEL BLOCK - L", "HOSTEL BLOCK - M", 
            "HOSTEL BLOCK - N", "HOSTEL-UMA(400)", "I.M.J SARVA VIDHYALAY - BALOL", 
            "KVK FARMERS HOSTEL", "MARINE HOSTEL BLOCK - A", "MARINE HOSTEL BLOCK - B", 
            "MARINE HOSTEL BLOCK - C", "N G INTERNATIONAL SCHOOL", "NAYI HOSTEL (MULSAN)", 
            "PARA KELAVANI MANDAL-MEHSANA", "RAMPURA HOSTEL", "SERVANT QUARTER HOSTEL", 
            "VISHWA HOSTEL", "GITANJALI BLOCK - 1", "GITANJALI BLOCK - 2", 
            "ANMOL HEIGHTS HOSTEL", "GIRLS EXECUTIVE A1", "GIRLS EXECUTIVE A2", "Virtuous"
        ])

        # Update profile button
        if st.button("Update Profile"):
            users_collection.update_one({"_id": ObjectId(st.session_state['user_id'])}, {"$set": {
                "email": new_email,
                "contact": new_contact,
                "department": new_department,
                "hostel": new_hostel
            }})
            st.success("Profile updated successfully!")

        # Display user information
        # st.write(f"*Username:* {user.get('username', 'N/A')}")
        st.write(f"*Last Login:* {user.get('last_login', 'N/A')}")

     # Sidebar for Navigation - Display only if logged in
    if st.session_state.logged_in:
        # Define logout button
        if st.sidebar.button("🚪 Logout"):
            logout()  # Call logout function


# Function to handle logout
def logout():
    st.session_state.logged_in = False
    st.session_state.page = "login"  # Redirect to login page


# Manage page redirection based on session state
if is_logged_in():
    profile_page()  # Show profile page if logged in
else:
    st.warning("Please log in to view your profile.")


# Footer at the bottom of the sidebar
st.sidebar.markdown("---")
st.sidebar.text("MyHealthAlly © 2024")
st.sidebar.text("All rights reserved.")

