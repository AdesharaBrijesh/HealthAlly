import streamlit as st
from datetime import datetime
import pymongo
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from bson import ObjectId
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Initialize MongoDB client
client = pymongo.MongoClient("mongodb+srv://mrhashtag292:qLeJHyZFTClgHixL@cluster.wooif.mongodb.net/?retryWrites=true&w=majority&appName=Cluster")
db = client["healthcare_chatbot"]

# Collection definitions
users_collection = db["users"]
chat_history_collection = db["chat_history"]
first_aid_rooms_collection = db["first_aid_rooms"]
doctors_collection = db["doctors"]
admins_collection = db["admins"]

# Function to check if user is logged in
def is_logged_in():
    return 'user_id' in st.session_state

# Sidebar for the admin dashboard
def sidebar():
    st.sidebar.title("Admin Panel")  # Sidebar Title
    st.sidebar.markdown("Manage users, view data, and perform administrative tasks.")

    # Navigation Menu
    menu_options = {
        "Dashboard": "dashboard",
        "User Management": "user_management",
        "Data Analysis": "data_analysis",
        "Settings": "settings"
    }

    # Create a sidebar menu
    selected_option = st.sidebar.selectbox("Select an option:", options=list(menu_options.keys()))

    # Example of icons usage (You can replace these with your preferred icons)
    # if selected_option == "Login/Signup":
    #     st.sidebar.markdown("### Login/Signup 🔐")
    #     login_page()  # Call your Login/Signup function here
    # if selected_option == "Profile":
    #     st.sidebar.markdown("### Profile 👤")
    #     profile_page()  # Call your Profile function here
    # if selected_option == "Chat":
    #     st.sidebar.markdown("### Chat 💬")
    #     chat_page()  # Call your Chat function here
    if selected_option == "Dashboard":
        st.sidebar.markdown("### Dashboard 🏠")
    if selected_option == "History":
        st.sidebar.markdown("### History 🏠")
        chat_history_page()  # Call your History function here
    elif selected_option == "User Management":
        st.sidebar.markdown("### User Management 👥")
        user_management_page()  # Call user management function
    elif selected_option == "Data Analysis":
        st.sidebar.markdown("### Data Analysis 📊")
        data_analysis_page()  # Call data analysis function
    elif selected_option == "Settings":
        st.sidebar.markdown("### Settings ⚙️")
        settings_page()  # Call settings function

# Login / Signup page
def login_page():
    st.title("Welcome to the Healthcare Chatbot")

    tab1, tab2 = st.tabs(["Login", "Signup"])

    with tab1:
        st.subheader("Login")
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        if st.button("Login"):
            user = users_collection.find_one({"username": username, "password": password})
            if user:
                st.session_state['user_id'] = str(user['_id'])
                st.session_state['logged_in'] = True
                st.session_state['username'] = username
                st.success("Logged in successfully!")
                st.session_state['page'] = "Chat"
            else:
                st.error("Invalid credentials")

    with tab2:
        st.subheader("Signup")
    
        # Fields for signup
        username = st.text_input("Create Username", placeholder="Choose a username")
        email = st.text_input("Email", placeholder="Enter your email")
        password = st.text_input("Create Password", type="password", placeholder="Choose a password")
        contact = st.text_input("Contact Number", placeholder="Your contact number")
        enrollment = st.text_input("Enrollment Number", placeholder="Your enrollment number")
        
        # Department and Hostel selection
        department = st.selectbox("Select Department", ["AMPICS", "BSPP", "CCE", "CHAS", "CHSS", "CMEC", "CMS", "CMSR", "DCS", "DMARI", "DSW", "GNUR", "ICT", "IOA", "IOD", "IOO", "IOP", "IOT", "JIM", "KBION", "KKIASR", "MUIS", "SKPCPER", "UVPCE", "VMPCMS", "VMPIM", "GANPAT VIDHYALAY", "SMGPSS", "OTHERS"])

        # New hostel selection
        hostels = [
            "B1 TOWER HOSTEL", "HOSTEL BLOCK - A", "HOSTEL BLOCK - B", "HOSTEL BLOCK - C", 
            "HOSTEL BLOCK - D", "HOSTEL BLOCK - E", "HOSTEL BLOCK - F", "HOSTEL BLOCK - G", 
            "HOSTEL BLOCK - H", "HOSTEL BLOCK - K", "HOSTEL BLOCK - L", "HOSTEL BLOCK - M", 
            "HOSTEL BLOCK - N", "HOSTEL-UMA(400)", "I.M.J SARVA VIDHYALAY - BALOL", 
            "KVK FARMERS HOSTEL", "MARINE HOSTEL BLOCK - A", "MARINE HOSTEL BLOCK - B", 
            "MARINE HOSTEL BLOCK - C", "N G INTERNATIONAL SCHOOL", "NAYI HOSTEL (MULSAN)", 
            "PARA KELAVANI MANDAL-MEHSANA", "RAMPURA HOSTEL", "SERVANT QUARTER HOSTEL", 
            "VISHWA HOSTEL", "GITANJALI BLOCK - 1", "GITANJALI BLOCK - 2", 
            "ANMOL HEIGHTS HOSTEL", "GIRLS EXECUTIVE A1", "GIRLS EXECUTIVE A2", "Virtuous"
        ]
        hostel = st.selectbox("Select Hostel", hostels)

        # Validation messages
        validation_messages = {
            "username": None,
            "email": None,
            "password": None,
            "contact": None,
            "enrollment": None,
        }

        # Real-time validation
        if username:
            if users_collection.find_one({"username": username}):
                validation_messages["username"] = "Username already taken."
            # else:
            #     validation_messages["username"] = "Username available."

        if email:
            if users_collection.find_one({"email": email}):
                validation_messages["email"] = "Email already in use."
        
        if password:
            if len(password) < 6:
                validation_messages["password"] = "Password must be at least 6 characters long."

        if contact:
            if users_collection.find_one({"contact": contact}):
                validation_messages["contact"] = "Number already in use."

            if not (contact.isdigit() and len(contact) == 10):
                validation_messages["contact"] = "Contact number must be exactly 10 digits and contain only numbers."
        
        if enrollment:
            if users_collection.find_one({"enrollment": enrollment}):
                validation_messages["enrollment"] = "Enrollment already in use."

            if not (enrollment.isdigit() and len(enrollment) == 11):
                validation_messages["enrollment"] = "Enrollment number must be exactly 11 digits and contain only numbers."

        # Display validation messages
        for key, message in validation_messages.items():
            if message:
                st.warning(message)

        # Signup button
        if st.button("Sign Up"):
            # Check if all validations passed
            errors = [key for key, message in validation_messages.items() if message]
            if errors:
                st.error(f"Please correct the following fields: {', '.join(errors)}.")
            else:
                # Create a new user if validations pass
                new_user = {
                    "username": username,
                    "email": email,
                    "password": password,
                    "contact": contact,
                    "enrollment": enrollment,
                    "department": department,
                    "hostel": hostel,
                    "last_login": datetime.now()
                }
                users_collection.insert_one(new_user)
                st.success("Account created successfully! You can log in now.")
                st.session_state['page'] = "Profile"  # Redirect to profile page

# Profile page
def profile_page():
    if not is_logged_in():
        st.warning("Please log in to view your profile.")
        return

    user = users_collection.find_one({"_id": ObjectId(st.session_state['user_id'])})
    
    if user:
        st.title("👤 User Profile")
        
        # Display profile picture
        profile_pic = user.get('profile_image', None)
        if profile_pic:
            st.image(profile_pic, width=150)
        else:
            # Create a placeholder image
            placeholder = Image.new('RGB', (150, 150), color=(200, 200, 200))  # Gray placeholder
            st.image(placeholder, caption='Default Profile Picture', width=150)

        # Upload new profile picture
        uploaded_file = st.file_uploader("Upload your profile picture:", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            # Resize image
            image = Image.open(uploaded_file)
            image = image.resize((150, 150))  # Fixed size
            st.image(image, caption='Profile Picture', use_column_width=True)

            # Update database with new profile picture
            users_collection.update_one(
                {"_id": ObjectId(st.session_state['user_id'])},
                {"$set": {"profile_image": uploaded_file.getvalue()}}
            )
            st.success("Profile picture updated successfully!")

        # Display user details
        st.subheader("Your Details")
        st.write(f"*Username:* {user.get('username', 'N/A')}")
        st.write(f"*Email:* {user.get('email', 'N/A')}")
        st.write(f"*Contact:* {user.get('contact', 'N/A')}")
        st.write(f"*Enrollment:* {user.get('enrollment', 'N/A')}")
        st.write(f"*Department:* {user.get('department', 'N/A')}")
        st.write(f"*Hostel:* {user.get('hostel', 'N/A')}")
        st.write(f"*Last Login:* {user.get('last_login', 'N/A')}")
        
        # Button to update other details
        if st.button("Update Details"):
            st.write("Feature to update details will be added here.")

        st.write("Feel free to explore more features of the app!")

# Load model and tokenizer
@st.cache_resource
def load_model():
    tokenizer = AutoTokenizer.from_pretrained("./model")
    model = AutoModelForSequenceClassification.from_pretrained("./model")
    return tokenizer, model

tokenizer, model = load_model()

def predict_disease(symptoms):
    inputs = tokenizer(symptoms, return_tensors="pt", padding=True, truncation=True, max_length=512)
    with torch.no_grad():
        logits = model(**inputs).logits
    predicted_class = torch.argmax(logits, dim=-1).item()
    
    # Use the trained model's prediction directly to get suggestions
    return predicted_class  # This returns the index of the predicted condition

def chat_page():
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    st.title("Health Chatbot")
    
    selected_department = st.selectbox("Select Department", ["AMPICS", "BSPP", "CCE", "CHAS", "CHSS", "CMEC", "CMS", "CMSR", "DCS", "DMARI", "DSW", "GNUR", "ICT", "IOA", "IOD", "IOO", "IOP", "IOT", "JIM", "KBION", "KKIASR", "MUIS", "SKPCPER", "UVPCE", "VMPCMS", "VMPIM", "GANPAT VIDHYALAY", "SMGPSS"])
    symptoms = st.text_input("Enter your symptoms:")
    
    if st.button("Submit Symptoms"):
        if symptoms:
            st.session_state.messages.append({"role": "user", "content": symptoms})
            diagnosis_index = predict_disease(symptoms)  # Get the diagnosis index
            
            # Here, you would retrieve diagnosis, precautions, etc. based on the index
            # For simplicity, let's assume these are defined in a separate function
            diagnosis, precautions, treatment = get_diagnosis_info(diagnosis_index)
            response = f"Diagnosis: {diagnosis}. Precautions: {precautions}. Treatment: {treatment}."
            st.session_state.messages.append({"role": "assistant", "content": response})
    
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.write(f"You: {message['content']}")
        else:
            st.write(f"Bot: {message['content']}")
    
    # Duration input handling
    duration = st.number_input("How many days have you had these symptoms?", min_value=0)
    if st.button("Submit Duration"):
        if duration > 2:
            st.session_state.messages.append({"role": "assistant", "content": "It is advisable to consult a doctor."})
        else:
            st.session_state.messages.append({"role": "assistant", "content": "Please rest and follow precautions."})

def get_diagnosis_info(index):
    # You need to implement this function to map index to diagnosis, precautions, and treatment
    # Example:
    if index == 0:
        return "Seasonal Flu", "Flu vaccination, avoid crowded places", "Rest, antiviral medication, hydration"
    elif index == 1:
        return "Exam Stress Fever", "Regular breaks, proper sleep", "Rest, cooling measures, stress management"
    # Add more conditions based on your training data
    return "Unknown", "No specific precautions", "No specific treatment"

def get_first_aid_room(department):
    # Fetch first aid room information from the collection
    return first_aid_rooms_collection.find_one({"department": department})

def get_logged_in_user():
    # Retrieve logged-in user details from session state or user collection
    return st.session_state["user_details"]

def get_available_doctors():
    # Fetch doctors from the collection with their availability
    return doctors_collection.find({})

def get_available_times(doctor):
    # Return the available time slots for the selected doctor
    return doctor['available_slots']

def confirm_appointment(user, doctor, time):
    # Confirm the appointment by adding it to the appointments collection
    appointments_collection.insert_one({
        "user": user["_id"],
        "doctor": doctor["_id"],
        "time": time,
        "duration": "15 minutes"
    })

def generate_chatbot_response(user_input, department):
    # Simple keyword-based response logic
    if "fever" in user_input.lower():
        return "It seems like you have a fever. I recommend you see a healthcare professional."
    elif "cough" in user_input.lower():
        return "Coughing can be a symptom of various conditions. Please consult a doctor."
    elif department and department != "Select your department":
        return f"As you are in the {department}, please reach out to your department for further assistance."
    else:
        return "I'm here to assist you. Could you please provide more details?"

def admin_login():
    st.title("Admin Login")
    with st.form(key='admin_login_form'):
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')
        submit_button = st.form_submit_button("Login")

    if submit_button:
        admin = admins_collection.find_one({"username": username, "password": password})

        if admin:
            st.session_state.is_admin_logged_in = True
            st.session_state.admin_username = username
            st.success("Login successful!")
            dashboard_page()  # Display user data immediately
        else:
            st.error("Invalid username or password.")

# Function to display user data
def display_user_data():
    users = users_collection.find()  # Get user data

    user_list = []
    hostel_count = {}  # Dictionary to count users per hostel

    for user in users:
        username = user.get("username", 'N/A')
        email = user.get("email", 'N/A')
        enrollment_number = user.get("enrollment_number", 'N/A')
        department = user.get("department", 'N/A')
        contact_number = user.get("contact_number", 'N/A')  
        hostel = user.get("hostel", 'N/A')  

        # Count hostels
        if hostel in hostel_count:
            hostel_count[hostel] += 1
        else:
            hostel_count[hostel] = 1

        user_list.append({
            "Username": username,
            "Email": email,
            "Enrollment Number": enrollment_number,
            "Department": department,
            "Contact Number": contact_number,
            "Hostel": hostel,
        })

    # Display user data in a table format
    if user_list:
        st.write("## User Data")
        st.table(user_list)

        # Create a pie chart for hostel distribution
        if hostel_count:
            st.write("## Hostel Distribution")
            labels = hostel_count.keys()
            sizes = hostel_count.values()

            fig, ax = plt.subplots()
            ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
            ax.axis('equal')  # Equal aspect ratio ensures pie chart is circular.
            st.pyplot(fig)  # Render the pie chart in Streamlit
    else:
        st.write("No user data available.")

# Function to delete a user
def delete_user(user_id):
    users_collection.delete_one({"_id": ObjectId(user_id)})
    st.success("User deleted successfully!")

# Function to visualize data (example with user count by department)
def visualize_data():
    st.subheader("Data Visualization")
    user_counts = users_collection.aggregate([
        {"$group": {"_id": "$department", "count": {"$sum": 1}}}
    ])
    
    data = list(user_counts)
    if data:
        df = pd.DataFrame(data)
        plt.figure(figsize=(10, 5))
        sns.barplot(x="_id", y="count", data=df)
        plt.title("Number of Users by Department")
        plt.xlabel("Department")
        plt.ylabel("Count")
        st.pyplot(plt)

# Admin dashboard function
def dashboard_page():
    # Check if the 'is_admin_logged_in' key exists in session state and its value
    if 'is_admin_logged_in' not in st.session_state or not st.session_state.is_admin_logged_in:
        admin_login()  # Show login page
        return

    st.title("Admin Dashboard")
        
    # Display User Data
    display_user_data()
        
    # Visualize Data
    visualize_data()
        
    # Check for delete action
    user_id_to_delete = st.experimental_get_query_params().get('delete')
    if user_id_to_delete:
        delete_user(user_id_to_delete[0])

def chat_history_page():
    st.title("Chat History")
    st.write("See your previous chats here.")

def user_management_page():
    st.title("User Management")
    st.write("Manage users here.")

def data_analysis_page():
    st.title("Data Analysis")
    st.write("View and analyze data here.")

def settings_page():
    st.title("Settings")
    st.write("Configure your settings here.")


# Main flow of the Streamlit app
def main():
    # sidebar()  # Call the sidebar function
    # Other main app logic can go here
    if 'page' not in st.session_state:
        st.session_state['page'] = 'Login'

    # Sidebar for navigation
    st.sidebar.title("Navigation")
    options = ["Login", "Profile", "Chat", "Chat History", "Admin Dashboard"]
    
    # Only show certain options when logged in
    if is_logged_in():
        options.remove("Login")
    
    page = st.sidebar.radio("Go to", options)

    if page == "Login":
        login_page()
    elif page == "Profile":
        profile_page()
    elif page == "Chat":
        chat_page()
    elif page == "Chat History":
        chat_history_page()
    elif page == "Admin Dashboard":
        dashboard_page()

if __name__ == '__main__':
    main()
