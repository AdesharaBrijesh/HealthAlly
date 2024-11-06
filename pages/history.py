import streamlit as st
from pymongo import MongoClient
from datetime import datetime
from config import MONGO_URI

# MongoDB connection
client = MongoClient(MONGO_URI)
db = client["healthcare_chatbot"]
chat_history_collection = db["chat_history"]

# Function to fetch chat history sessions of the logged-in user
def fetch_chat_history(user_id):
    return list(chat_history_collection.find({"user_id": user_id}).sort("timestamp", 1))  # Sort by timestamp, oldest first

# Function to check if user is logged in
def is_logged_in():
    return 'user_id' in st.session_state and 'logged_in' in st.session_state and st.session_state['logged_in']

# Chat history page function
def chat_history_page():
    st.title("Chat History")
    
    if not is_logged_in():
        st.warning("You must be logged in to view chat history.")
        return
    
    user_id = st.session_state['user_id']  # Retrieve user ID from session state
    chat_messages = fetch_chat_history(user_id)

    if not chat_messages:
        st.write("No chat history available.")
        return

    # Search functionality for chat messages
    search_query = st.text_input("Search Chats", "")
    if search_query:
        chat_messages = [
            message for message in chat_messages
            if search_query.lower() in message['message'].lower()
        ]

    # Display each chat session with all messages
    st.subheader("Your Chat History")
    current_session_date = None  # To group messages by session date
    for message in chat_messages:
        timestamp = message.get('timestamp')

        # Check if timestamp is already a datetime object
        if isinstance(timestamp, datetime):
            date_time = timestamp.strftime('%Y-%m-%d %H:%M:%S')
        else:
            # Convert from Unix timestamp if it's an integer
            date_time = datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')

        role = message.get("role", "assistant").capitalize()
        content = message.get("message", "No content available")
        username = message.get("user_id", "Unknown User")

        # Group messages by session date and show as collapsible
        if current_session_date != timestamp.date():
            current_session_date = timestamp.date()
            with st.expander(f"Session on {timestamp.date()}"):
                for msg in chat_messages:
                    if isinstance(msg['timestamp'], datetime):
                        msg_time = msg['timestamp']
                    else:
                        msg_time = datetime.fromtimestamp(msg['timestamp'] / 1000)

                    if msg_time.date() == current_session_date:
                        st.markdown(f"**{msg['role']}** ({msg['user_id']}): {msg['message']}")
                        st.markdown(f"<div style='font-size: 12px; color: grey;'>{msg_time.strftime('%Y-%m-%d %H:%M:%S')}</div>", unsafe_allow_html=True)

    st.sidebar.markdown("---")
    st.sidebar.text("MyHealthAlly © 2024")
    st.sidebar.text("All rights reserved.")

# Run the chat history page
if __name__ == "__main__":
    chat_history_page()
