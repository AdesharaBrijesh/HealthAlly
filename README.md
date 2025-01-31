# HealthAlly: AI-Powered Healthcare Chatbot for University Students


HealthAlly is an AI-powered healthcare chatbot designed to support university students by providing immediate assistance for both physical and mental health concerns. Built using **Python**, **Streamlit**, and **MongoDB**, this chatbot acts as a virtual healthcare assistant, offering personalized advice on symptoms, treatments, first aid room availability, and doctor appointments—all tailored for the university environment.

Whether it's a common cold, stress from exams, or any health-related issue, students can rely on HealthAlly for quick guidance and support. The chatbot also helps students navigate through healthcare resources available on campus, from medicines in first aid rooms to booking consultations with campus doctors.

👉 **Live Demo**: [HealthAlly Live Demo](https://myhealthally.streamlit.app/)

---

## Features

### 1. **Symptom Diagnosis**
   - The chatbot uses a pre-trained machine learning model to accurately diagnose symptoms reported by the student, suggesting the most probable conditions, treatments, and medications.

### 2. **First Aid Room Information**
   - The chatbot checks the availability of medicines in the campus first aid rooms by referencing the specific department where the student is located. It ensures students have access to immediate care options if needed.

### 3. **Mental Health Support**
   - Understanding that university life can be stressful, the chatbot assists students in managing mental health concerns by offering stress-relief suggestions, tips for maintaining mental well-being, and connecting students to counseling services if necessary.

### 4. **Appointment Booking**
   - Students can book appointments with university healthcare providers (doctors, counselors, etc.) directly through the chatbot interface. The chatbot ensures that students are guided to book timely consultations based on their symptoms or concerns.

### 5. **Academic and Study-Related Health**
   - The chatbot provides advice on maintaining physical and mental health during exam seasons, managing study-related stress, taking breaks, and improving overall academic performance through good health practices.

### 6. **Real-Time Assistance**
   - The chatbot is available 24/7 to address any urgent health or wellness issues, making it a reliable companion for students anytime they need it.

---

## Target Audience

HealthAlly is primarily designed for **university students** and addresses the following needs:
- **Physical Health Concerns**: Diagnosing common illnesses like fever, cough, cold, headaches, and more based on symptoms described by the student.
- **Mental Health and Stress Management**: Providing resources to manage stress, anxiety, and mental health challenges commonly faced by students.
- **Campus Healthcare Resources**: Assisting students in accessing medicines and healthcare resources within their university campus, especially first aid and health consultations.
- **Convenience**: Students can manage their health directly through a user-friendly interface, without the need to wait for in-person consultations.

---

## Prerequisites

To run this project locally, ensure you have the following installed:
- **Python** (3.8 or higher)
- **MongoDB** account (for hosting your database)
- **Streamlit**
- Required Python libraries (listed in `requirements.txt`)

---

## Installation

### 1. Fork or Clone the Repository
You can either fork the repository to your GitHub account or clone it directly to your local machine using the following command:
```bash
git clone https://github.com/AdesharaBrijesh/HealthAlly.git
```

### 2. Install Dependencies
After cloning the repository, navigate to the project directory:
```bash
cd adesharabrijesh-healthally
```

Create and activate a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate   # For Windows: venv\Scripts\activate
```

Install the required Python dependencies by running:
```bash
pip install -r requirements.txt
```

### 3. MongoDB Configuration
Create a `config.py` file in the root directory of the project to securely store your MongoDB connection URL. The `config.py` file should look like this:
```python
# config.py
MONGO_URI = "your_mongodb_connection_url"
```
Replace `"your_mongodb_connection_url"` with your actual MongoDB connection URL. You can find this in your MongoDB Atlas cluster.

**Important**: Ensure the `config.py` file is NOT pushed to GitHub. It should be listed in the `.gitignore` file to prevent sensitive information from being exposed.

### 4. Running the Application
To run the app locally, use the following command:
```bash
streamlit run streamlit_app.py
```
This will start the application on your local machine, and you can view it in your browser at `http://localhost:8501`.

---

## Project Structure

```
adesharabrijesh-healthally/
├── README.md               # Project documentation
├── config.py               # MongoDB connection URL (should not be pushed to GitHub)
├── requirements.txt        # List of Python dependencies
├── streamlit_app.py        # Entry point for the Streamlit app
├── user_data.db            # Database for user-related data
├── x.txt                   # (Optional: Add description if needed)
├── data/                   # Directory containing data files
│   └── data.csv            # CSV file with symptoms, conditions, treatments, and medicines
├── model/                  # Directory containing AI models and related files
│   ├── llm.py              # Language model for symptom diagnosis
│   ├── medicine.py         # Medicine-related functions
│   ├── medicine_df.pkl     # Preprocessed medicine data
│   ├── medicine_faiss_index.bin  # FAISS index for medicine search
│   └── sentence_transformer_model.pkl  # Sentence transformer model
├── pages/                  # Pages for the app (for Streamlit multi-page setup)
│   ├── 0_helthChat.py      # Main chat interface
│   ├── 1_appointment_booking.py  # Appointment booking page
│   ├── 2_data_analysis.py  # Data analysis page
│   ├── 3_history.py        # Chat history page
│   ├── 5_profile.py        # User profile page
│   ├── chat.py             # Chat functionality
│   ├── dashboard.py        # Dashboard page
│   └── login.py            # Login page
└── styles/                 # Custom CSS for the app
    └── sidebar.css         # Sidebar styles
```

---

## Usage

Once the application is up and running, here's how to use it:
1. **Select Department**: Choose the department you are experiencing symptoms in.
2. **Describe Symptoms**: Enter the symptoms you're experiencing, and click "Submit Symptoms."
3. **View Diagnosis**: The chatbot will suggest a condition, treatment, precautions, and recommend medicine based on your symptoms.
4. **Check Medicine Availability**: It will check if the suggested medicines are available in the first aid room of your selected department.
5. **Book Appointment**: If your symptoms persist for more than 2 days, the chatbot will suggest booking an appointment with a doctor.

---

## Contributing

We welcome contributions! If you'd like to contribute to the project, feel free to fork the repository and submit a pull request with your changes. Please ensure to follow the project's code style and include tests where applicable.

---

## License

This project is open source and available under the **MIT License**.

---

## Acknowledgements

- **MongoDB Atlas** for hosting the database.
- **Streamlit** for the easy-to-use dashboard framework.
- **Pandas** for handling and analyzing the data.
- **Sentence Transformers** for enabling semantic search in the chatbot.

---

**Note**: Always ensure sensitive credentials (like MongoDB URI) are kept secure and are not exposed to the public.

---
