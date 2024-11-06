# Healthcare Chatbot Project

This healthcare chatbot application is designed to support university students by providing immediate assistance for both physical and mental health concerns. Developed using Python, Streamlit, and MongoDB, the chatbot serves as a virtual healthcare assistant, offering personalized advice on symptoms, treatments, first aid room availability, and doctor appointments—all tailored for the university environment.

Whether it's a common cold, stress from exams, or any health-related issue, students can rely on this tool for quick guidance and support. The chatbot also helps students navigate through healthcare resources available on campus, from medicines in first aid rooms to booking consultations with campus doctors.

## Features

- **Symptom Diagnosis**: The chatbot uses a pre-trained machine learning model to accurately diagnose symptoms reported by the student, suggesting the most probable conditions, treatments, and medications.
  
- **First Aid Room Information**: The chatbot checks the availability of medicines in the campus first aid rooms by referencing the specific department where the student is located. It ensures students have access to immediate care options if needed.

- **Mental Health Support**: Understanding that university life can be stressful, the chatbot can also assist students in managing mental health concerns by offering stress-relief suggestions, tips for maintaining mental well-being, and connecting students to counseling services if necessary.

- **Appointment Booking**: Students can book appointments with university healthcare providers (doctors, counselors, etc.), directly through the chatbot interface. The chatbot ensures that students are guided to book timely consultations based on their symptoms or concerns.

- **Academic and Study-Related Health**: The chatbot provides advice on maintaining physical and mental health during exam seasons, managing study-related stress, taking breaks, and how to improve overall academic performance through good health practices.

- **Real-Time Assistance**: The chatbot is available 24/7 to address any urgent health or wellness issues, making it a reliable companion for students any time they need it.

- **Live Demo**: A live demo of the application can be accessed via [HealthAlly Demo](https://your-streamlit-link.com), providing a seamless experience for potential users to test the functionality and features.

### Target Audience

This chatbot is primarily focused on university students and addresses the following needs:

- **Physical Health Concerns**: It offers support in diagnosing common illnesses like fever, cough, cold, headaches, and more, based on symptoms described by the student.
- **Mental Health and Stress Management**: It provides resources to manage stress, anxiety, and mental health challenges commonly faced by students.
- **Campus Healthcare Resources**: The chatbot assists students in accessing medicines and healthcare resources within their university campus, especially first aid and health consultations.
- **Convenience**: Students can manage their health directly through a user-friendly interface, without the need to wait for in-person consultations.

This project aims to bridge the gap between students and healthcare by providing instant support and information, reducing the time it takes to get the care they need.



## Prerequisites

To run this project locally, ensure you have the following installed:

- Python (3.8 or higher)
- MongoDB account (for hosting your database)
- Streamlit
- Required Python libraries (listed below)

## Installation

### 1. Fork or Clone the Repository

You can either fork the repository to your GitHub account or clone it directly to your local machine using the following command:

```bash
git clone https://github.com/AdesharaBrijesh/HealthAlly.git
```

### 2. Install Dependencies

After cloning the repository, navigate to the project directory:

```bash
cd healthcare-chatbot
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

Make sure to replace `"your_mongodb_connection_url"` with your actual MongoDB connection URL. You can find this in your MongoDB Atlas cluster.

**Important**: Ensure the `config.py` file is NOT pushed to GitHub. It should be listed in the `.gitignore` file to prevent sensitive information from being exposed.

### 4. Running the Application

To run the app locally, use the following command:

```bash
streamlit run app.py
```

This will start the application on your local machine, and you can view it in your browser at `http://localhost:8501`.

### 5. Live Demo

A live version of the healthcare chatbot is available on Streamlit. You can access it here: [HealthAlly Live Demo](https://your-streamlit-link.com).

## Project Structure

```
healthcare-chatbot/
│
├── .vscode/                # Visual Studio Code settings
├── config.py               # MongoDB connection URL (should not be pushed to GitHub)
├── data/                   # Directory containing data files
│   └── data.csv            # CSV file with symptoms, conditions, treatments, and medicines
├── pages/                  # Pages for the app (for Streamlit multi-page setup)
│   ├── appointment_booking.py  # Appointment booking page
│   ├── chat.py             # Chat page
│   ├── dashboard.py        # Dashboard page
│   ├── data_analysis.py    # Data analysis page
│   ├── history.py          # Chat history page
│   ├── login.py            # Login page
│   └── profile.py          # User profile page
├── requirements.txt        # List of Python dependencies
├── streamlit_app.py        # Entry point for the Streamlit app
├── styles/                 # Custom CSS for the app
│   └── sidebar.css         # Sidebar styles
├── venv/                   # Virtual Environment
├── .gitignore              # Specifies which files/folders should be ignored by Git
└── README.md               # Project documentation (this file)

```

### .gitignore Example

Ensure that the `.gitignore` file includes `config.py` to prevent it from being pushed to GitHub:

```
# .gitignore
config.py
venv/
# .gitignore
config.py
venv/
__pycache__/
```

### requirements.txt Example

Here's a sample `requirements.txt` file containing the libraries used in the project:

```
streamlit==1.15.2
pandas==1.5.0
pymongo==4.3.3
```

## Usage

Once the application is up and running, here's how to use it:

1. Select Department: Choose the department you are experiencing symptoms in.
2. Describe Symptoms: Enter the symptoms you're experiencing, and click "Submit Symptoms."
3. View Diagnosis: The chatbot will suggest a condition, treatment, precautions, and recommend medicine based on your symptoms.
4. Check Medicine Availability: It will check if the suggested medicines are available in the first aid room of your selected department.
5. Book Appointment: If your symptoms persist for more than 2 days, the chatbot will suggest booking an appointment with a doctor.

## Contributing

If you'd like to contribute to the project, feel free to fork the repository and submit a pull request with your changes.

Please ensure to follow the project's code style and include tests where applicable.

## License

This project is open source and available under the MIT License.

## Acknowledgements

- MongoDB Atlas for hosting the database.
- Streamlit for the easy-to-use dashboard framework.
- Pandas for handling and analyzing the data.

**Note**: Always ensure sensitive credentials (like MongoDB URI) are kept secure and are not exposed to the public.