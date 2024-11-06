# Healthcare Chatbot Project

This is a healthcare chatbot application developed using Python, Streamlit, and MongoDB. The chatbot helps diagnose symptoms, suggest treatments, provide precautions, and help with medicine availability in first aid rooms at different departments. Users can also book appointments with doctors based on the symptoms they describe.

## Features
- **Symptom Diagnosis**: The chatbot diagnoses the user's symptoms based on a pre-trained model and suggests treatments and medicines.
- **First Aid Room Information**: The chatbot checks medicine availability in the selected department's first aid room.
- **Appointment Booking**: Users can book appointments with doctors for further consultation.
- **Live Demo**: A live demo of the application can be accessed via [HealthAlly Demo](https://your-streamlit-link.com).

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
git clone https://github.com/yourusername/healthcare-chatbot.git
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
├── app.py                  # Main application file with Streamlit UI and logic
├── config.py               # MongoDB connection URL (should not be pushed to GitHub)
├── data/                   # Directory containing symptom diagnosis CSV data
│   └── data.csv            # CSV file with symptoms, conditions, treatments, and medicines
├── .gitignore              # Specifies which files/folders should be ignored by Git
├── requirements.txt        # List of Python dependencies
├── README.md               # Project documentation (this file)
```

### .gitignore Example

Ensure that the `.gitignore` file includes `config.py` to prevent it from being pushed to GitHub:

```
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