import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pymongo import MongoClient
from bson import ObjectId
from config import MONGO_URI

# MongoDB connection
client = MongoClient(MONGO_URI)
db = client["healthcare_chatbot"]

# Admin login function
def admin_login():
    st.title("Admin Login")
    st.write("### Please enter your credentials to access the data analysis page.")
    
    with st.form(key='admin_login_form'):
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')
        submit_button = st.form_submit_button("Login")

    if submit_button:
        admin = db.admins.find_one({"username": username, "password": password})

        if admin:
            st.session_state.is_admin_logged_in = True
            st.session_state.admin_username = username
            st.success("Login successful! You can now access the data analysis.")
            st.session_state.show_analysis = True  # Set a flag to show the Analysis
        else:
            st.error("Invalid username or password.")

# Function to fetch user data from the database
def fetch_user_data():
    return pd.DataFrame(list(db.users.find()))

# Function to fetch admin data from the database
def fetch_admin_data():
    return pd.DataFrame(list(db.admins.find()))

# Main function to run the analysis page
def main():
    if 'is_admin_logged_in' not in st.session_state or not st.session_state.is_admin_logged_in:
        admin_login()  # Show login page
    else:
        st.sidebar.header("Admin Options")
        if st.sidebar.button("Logout"):
            st.session_state.is_admin_logged_in = False
            st.success("Logged out successfully!")
            st.experimental_set_query_params()  # Clear any parameters in the URL
            return  # Exit the function to not show the dashboard
        
        #  Visualize user data
        st.title("Data Analysis Page")

        # Fetch user data
        user_data = fetch_user_data()

        if user_data.empty:
            st.write("No user data available.")
            return

        # Create a sidebar for filtering options
        st.sidebar.subheader("Filters")
        department_filter = st.sidebar.multiselect("Select Department", options=user_data['department'].unique())

        if department_filter:
            user_data = user_data[user_data['department'].isin(department_filter)]

        st.subheader("User Distribution by Department")
        department_counts = user_data['department'].value_counts()
        plt.figure(figsize=(8, 4))
        sns.barplot(x=department_counts.index, y=department_counts.values, palette='viridis')
        plt.title("User Distribution by Department")
        plt.xticks(rotation=45)
        st.pyplot(plt)

        st.subheader("User Age Distribution")
        if 'age' in user_data.columns:
            age_counts = user_data['age'].value_counts()
            plt.figure(figsize=(8, 4))
            sns.lineplot(x=age_counts.index, y=age_counts.values, marker='o')
            plt.title("User Age Distribution")
            st.pyplot(plt)

        st.subheader("Detailed User Data")
        st.dataframe(user_data)

        # Fetch admin data
        admin_data = fetch_admin_data()
        if not admin_data.empty:
            st.subheader("Admin Data Overview")
            st.dataframe(admin_data)

if __name__ == "__main__":
    main()

# Footer at the bottom of the sidebar
st.sidebar.markdown("---")
st.sidebar.text("MyHealthAlly © 2024")
st.sidebar.text("All rights reserved.")
