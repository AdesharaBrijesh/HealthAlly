import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="MyHealthAlly",
    page_icon="👨‍⚕️",
    layout="wide",
)

# Load custom CSS from an external file for sidebar styling
with open("styles/sidebar.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Initialize session state for login and page management
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "login"  # Default to login initially

# Function to handle logout
def logout():
    st.session_state.logged_in = False
    st.session_state.page = "login"  # Redirect to login page

# Function to show default content after login
def show_default_content():
    st.title("Welcome to MyHealthAlly!")
    st.markdown("""
    MyHealthAlly is your personal health assistant designed to help you manage your health easily and effectively.
    
    **Features:**
    - **Chat with Health Professionals:** Get real-time advice and support for your health queries.
    - **Access to Medical Resources:** Find information on symptoms, treatments, and preventative care.
    - **User-Friendly Dashboard:** Track your health records and appointments in one place.
    
    **Why Choose MyHealthAlly?**
    - **Professional Support:** Connect with certified health professionals at your convenience.
    - **Personalized Experience:** Tailor your health journey based on your needs and preferences.
    - **Engaging Interface:** Enjoy a modern and intuitive interface that makes navigation simple.
    
    ### Get Started!
    Explore the features available to you by navigating through the sidebar.
    """)

    # Optionally, you can add interactive elements like buttons or links
    if st.button("Explore Features"):
        st.markdown("### Coming Soon: More Features!")  # Placeholder for future functionality

# Sidebar for Navigation - Display only if logged in
if st.session_state.logged_in:
    # Define logout button
    if st.sidebar.button("🚪 Logout"):
        logout()  # Call logout function
    show_default_content()

    # Navigation logic based on current page selection
    # if st.session_state.page == "profile":
    #     exec(open("pages/profile.py").read())  # Run the profile page script
    # elif st.session_state.page == "chat":
    #     exec(open("pages/chat.py").read())  # Run the chat page script
    # elif st.session_state.page == "dashboard":
    #     exec(open("pages/dashboard.py").read())  # Run the dashboard page script
    # elif st.session_state.page == "admin_dashboard":
    #     exec(open("admin/admin_dashboard.py").read())  # Run the admin dashboard page script
    # elif st.session_state.page == "data_management":
    #     exec(open("admin/data_management.py").read())  # Run the data management page script
    # elif st.session_state.page == "data_analysis":
    #     exec(open("admin/data_analysis.py").read())  # Run the data analysis page script

else:
    # Show the login page if the user is not logged in
    st.write("Please log in to access the app.")
    exec(open("pages/login.py").read())  # Run the login page script

# Footer at the bottom of the sidebar
# st.sidebar.markdown("---")
# st.sidebar.text("MyHealthAlly © 2024")
# st.sidebar.text("All rights reserved.")
