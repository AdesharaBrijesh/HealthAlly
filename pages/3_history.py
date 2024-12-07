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

# Function to check if the user is logged in
def is_logged_in():
    return 'user_id' in st.session_state and 'logged_in' in st.session_state and st.session_state['logged_in']

# Function to get datetime from timestamp (handling both datetime and Unix timestamps)
def get_datetime_from_timestamp(timestamp):
    if isinstance(timestamp, datetime):
        return timestamp  # If it's already a datetime object, return it
    elif isinstance(timestamp, int):
        # Convert Unix timestamp (in milliseconds) to datetime object
        return datetime.fromtimestamp(timestamp / 1000)
    else:
        raise ValueError("Unsupported timestamp format")

# Chat history page function
def chat_history_page():
    st.set_page_config(page_title="Chat History", page_icon="📝", layout="wide")
    st.title("Chat History 📜")

    # Custom Styling
    st.markdown(
        """
        <style>
        .sidebar .sidebar-content {
            background-color: #f5f5f5;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            font-size: 16px;
            border-radius: 5px;
            padding: 10px 20px;
        }
        .stButton>button:hover {
            background-color: #45a049;
        }
        .expanderHeader {
            font-weight: bold;
            font-size: 16px;
            color: #3d3d3d;
        }
        .stMarkdown {
            font-size: 14px;
            color: #333;
        }
        .chat-message {
            margin-bottom: 15px;
            padding: 10px;
            border-radius: 8px;
            background-color: #f9f9f9;
            box-shadow: 0px 2px 3px rgba(0, 0, 0, 0.1);
        }
        .assistant-message {
            background-color: #d0f0c0;
        }
        .user-message {
            background-color: #e6e6fa;
        }
        </style>
        """, unsafe_allow_html=True
    )

    if not is_logged_in():
        st.warning("You must be logged in to view chat history.")
        return

    user_id = st.session_state['user_id']  # Retrieve user ID from session state
    chat_messages = fetch_chat_history(user_id)

    if not chat_messages:
        st.write("No chat history available.")
        return

    # Search functionality for chat messages
    st.sidebar.subheader("Search Chats")
    search_query = st.sidebar.text_input("Search", "")

    # Filter chat by date range
    st.sidebar.subheader("Filter by Date")
    start_date = st.sidebar.date_input("Start Date", min_value=min([get_datetime_from_timestamp(msg['timestamp']).date() for msg in chat_messages]) if chat_messages else datetime.today())
    end_date = st.sidebar.date_input("End Date", max_value=datetime.today())

    # Filter the chat messages based on date range and search query
    chat_messages = [
        msg for msg in chat_messages
        if start_date <= get_datetime_from_timestamp(msg['timestamp']).date() <= end_date
        and (search_query.lower() in msg['message'].lower() if search_query else True)
    ]

    # Display each chat session with all messages
    st.subheader("Your Chat History")
    current_session_date = None  # To group messages by session date
    for message in chat_messages:
        timestamp = message.get('timestamp')

        # Use the helper function to get the correct datetime
        timestamp_dt = get_datetime_from_timestamp(timestamp)

        # Format the timestamp for display
        date_time = timestamp_dt.strftime('%Y-%m-%d %H:%M:%S')

        role = message.get("role", "assistant").capitalize()
        content = message.get("message", "No content available")
        username = message.get("user_id", "Unknown User")

        # Group messages by session date and show as collapsible
        if current_session_date != timestamp_dt.date():
            current_session_date = timestamp_dt.date()
            with st.expander(f"Session on {current_session_date}"):
                for msg in chat_messages:
                    msg_time = get_datetime_from_timestamp(msg['timestamp'])

                    if msg_time.date() == current_session_date:
                        # Display user and assistant messages with different styles
                        message_class = "user-message" if msg['role'] == "user" else "assistant-message"
                        st.markdown(f"<div class='chat-message {message_class}'>{msg['message']}</div>", unsafe_allow_html=True)
                        st.markdown(f"<div style='font-size: 12px; color: grey;'>{msg_time.strftime('%Y-%m-%d %H:%M:%S')}</div>", unsafe_allow_html=True)

    # Footer
    st.sidebar.markdown("---")
    st.sidebar.text("MyHealthAlly © 2024")
    st.sidebar.text("All rights reserved.")

# Run the chat history page
if __name__ == "__main__":
    chat_history_page()
