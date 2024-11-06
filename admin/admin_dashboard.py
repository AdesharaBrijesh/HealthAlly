import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pymongo import MongoClient
from bson import ObjectId

client = MongoClient("mongodb+srv://mrhashtag292:qLeJHyZFTClgHixL@cluster.wooif.mongodb.net/?retryWrites=true&w=majority&appName=Cluster")
db = client["healthcare_chatbot"]
users_collection = db["users"]

def is_admin():
    user = users_collection.find_one({"_id": ObjectId(st.session_state.get('user_id'))})
    return user and user.get('is_admin', False)

def dashboard_pagedashboard_page():
    if not is_admin():
        st.warning("You do not have permission to access this page.")
        return

    st.title("Admin Dashboard")

    users = users_collection.find()
    user_list = [{"Username": user.get("username"), "Email": user.get("email"), "Contact": user.get("contact"), "Department": user.get("department")} for user in users]

    if user_list:
        df = pd.DataFrame(user_list)
        st.subheader("User List")
        st.dataframe(df)

        st.subheader("Data Visualization")
        dept_count = df["Department"].value_counts()
        sns.barplot(x=dept_count.index, y=dept_count.values)
        plt.title("User Count by Department")
        plt.xticks(rotation=45)
        st.pyplot(plt)
    else:
        st.warning("No users found.")
