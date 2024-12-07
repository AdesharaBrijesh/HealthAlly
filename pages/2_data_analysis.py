import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pymongo import MongoClient
from bson import ObjectId
from config import MONGO_URI
import sqlite3

# MongoDB connection
client = MongoClient(MONGO_URI)
db = client["healthcare_chatbot"]

# SQLite Database Connection for Users
def fetch_user_data():
    conn = sqlite3.connect("user_data.db")
    try:
        query = "SELECT * FROM users"
        df = pd.read_sql_query(query, conn)
        return df
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return pd.DataFrame()  # Return empty DataFrame in case of an error
    finally:
        conn.close()

# SQLite Database Connection for Queries
def fetch_queries_data():
    conn = sqlite3.connect("user_data.db")
    try:
        query = "SELECT * FROM queries"
        df = pd.read_sql_query(query, conn)
        return df
    except Exception as e:
        st.error(f"Error fetching query data: {e}")
        return pd.DataFrame()  # Return empty DataFrame in case of an error
    finally:
        conn.close()


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
    # Add a custom Streamlit theme for a modern look
    # st.set_page_config(page_title="Admin Dashboard", page_icon="📊", layout="wide")
    
    if 'is_admin_logged_in' not in st.session_state or not st.session_state.is_admin_logged_in:
        admin_login()  # Show login page
    else:
        # Sidebar for logout and options
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

        # Improved visualization of User Distribution by Department with a sleek barplot
        st.subheader("User Distribution by Department")
        department_counts = user_data['department'].value_counts()
        plt.figure(figsize=(10, 6))
        sns.set(style="whitegrid")
        sns.barplot(x=department_counts.index, y=department_counts.values, palette='coolwarm')
        plt.title("User Distribution by Department", fontsize=16)
        plt.xticks(rotation=45)
        st.pyplot(plt)

        # Enhanced User Age Distribution with styling
        st.subheader("User Age Distribution")
        if 'age' in user_data.columns:
            age_counts = user_data['age'].value_counts()
            plt.figure(figsize=(10, 6))
            sns.set(style="whitegrid")
            sns.lineplot(x=age_counts.index, y=age_counts.values, marker='o', color='teal')
            plt.title("User Age Distribution", fontsize=16)
            st.pyplot(plt)

        st.subheader("Detailed User Data")
        st.dataframe(user_data)

        # Streamlit Application for Viewing Database
        st.title("User & Query Database Viewer 📋")
        st.markdown("View the data stored in the `users` and `queries` tables of the SQLite database.")
        
        # Fetch data from both tables
        user_data = fetch_user_data()
        query_data = fetch_queries_data()

        # Display User Data with Download Button
        if not user_data.empty:
            st.subheader("Registered Users")
            st.dataframe(user_data, use_container_width=True)

            # Optional: Export Users as CSV with a button
            st.download_button(
                label="Download User Data CSV",
                data=user_data.to_csv(index=False),
                file_name="user_data.csv",
                mime="text/csv",
                help="Click to download the user data in CSV format"
            )
        else:
            st.warning("No data found in the users table.")

        # Fetch admin data
        admin_data = fetch_admin_data()
        if not admin_data.empty:
            st.subheader("Admin Data Overview")
            st.dataframe(admin_data)

# Footer at the bottom of the sidebar
st.sidebar.markdown("---")
st.sidebar.text("MyHealthAlly © 2024")
st.sidebar.text("All rights reserved.")

if __name__ == "__main__":
    main()
