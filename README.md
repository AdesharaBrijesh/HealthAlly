Here’s an enhanced version of your `README.md` with improved structure, clarity, and visual appeal. I've added badges, better formatting, and more detailed sections to make it more professional and user-friendly.

---

# HealthAlly: AI-Powered Healthcare Chatbot for University Students �️

![HealthAlly Demo](https://img.shields.io/badge/Demo-Live%20Demo-green?style=for-the-badge&logo=streamlit)  
![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat&logo=python)  
![Streamlit](https://img.shields.io/badge/Streamlit-UI%20Framework-red?style=flat&logo=streamlit)  
![MongoDB](https://img.shields.io/badge/MongoDB-Database-green?style=flat&logo=mongodb)  

HealthAlly is an **AI-powered healthcare chatbot** designed to support university students by providing immediate assistance for **physical & mental health concerns**. Built with **Python, Streamlit, and MongoDB**, it offers **personalized symptom diagnosis, first-aid room availability, mental health support, and doctor appointment booking**—all tailored for campus life.

👉 **Live Demo**: [Try HealthAlly Now](https://myhealthally.streamlit.app/)  

---

## ✨ Key Features  

| Feature | Description |  
|---------|------------|  
| **🤖 AI Symptom Checker** | Diagnoses conditions based on symptoms using ML & suggests treatments. |  
| **💊 First-Aid Room Tracker** | Checks medicine availability in campus first-aid rooms by department. |  
| **🧠 Mental Health Support** | Provides stress-relief tips & connects to counseling services. |  
| **📅 Doctor Appointment Booking** | Books consultations with campus doctors directly in-chat. |  
| **📚 Academic Wellness Tips** | Advice on managing exam stress, sleep, and study habits. |  
| **24/7 Real-Time Assistance** | Always available for urgent health queries. |  

---

## 🎯 Target Audience  

- **University students** needing quick health guidance.  
- Those facing **physical symptoms** (fever, cough, headaches, etc.).  
- Students struggling with **stress, anxiety, or mental health challenges**.  
- Anyone seeking **campus healthcare resources** (medicines, first aid, doctors).  

---

## 🛠️ Installation  

### 1. Clone the Repository  
```bash
git clone https://github.com/AdesharaBrijesh/HealthAlly.git
cd HealthAlly
```

### 2. Set Up a Virtual Environment (Recommended)  
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install Dependencies  
```bash
pip install -r requirements.txt
```

### 4. Configure MongoDB  
Create a `config.py` file:  
```python
# config.py
MONGO_URI = "your_mongodb_connection_url_here"  # Get this from MongoDB Atlas
```
**⚠️ Never commit `config.py` to GitHub!**  

### 5. Run the App  
```bash
streamlit run streamlit_app.py
```
Visit **`http://localhost:8501`** in your browser.  

---

## 📂 Project Structure  

```
HealthAlly/
├── data/                   # Health datasets (symptoms, treatments, etc.)
│   └── data.csv            
├── model/                  # AI models & embeddings
│   ├── llm.py              # Symptom diagnosis logic
│   ├── medicine.py         # Medicine search functions
│   └── *.pkl/.bin          # Pre-trained model files
├── pages/                  # Streamlit app pages
│   ├── 0_helthChat.py      # Main chat interface
│   ├── 1_appointment_booking.py  # Book doctors
│   └── ...                 # Other pages (history, profile, etc.)
├── styles/                 # Custom CSS
│   └── sidebar.css         
├── streamlit_app.py        # Main app entry point
├── config.py               # Secrets (ignored in Git)
└── requirements.txt        # Python dependencies
```

---

## 🚀 How to Use  

1. **Select your department** (e.g., Computer Science, Medicine).  
2. **Describe symptoms** (e.g., "headache, fever for 2 days").  
3. **Get AI diagnosis** with treatment & medicine suggestions.  
4. **Check first-aid room** for medicine availability.  
5. **Book a doctor** if symptoms persist.  

---

## 🤝 Contributing  

We welcome contributions! Here’s how:  

1. **Fork** the repo.  
2. **Create a branch**: `git checkout -b feature/your-idea`  
3. **Commit changes**: `git commit -m "Add awesome feature"`  
4. **Push**: `git push origin feature/your-idea`  
5. **Open a Pull Request**.  

---

## 📜 License  

This project is licensed under the **MIT License**.  

---

## 🙏 Acknowledgements  

- **MongoDB Atlas** for database hosting.  
- **Streamlit** for the intuitive UI framework.  
- **Hugging Face** for transformer models.  
- **FAISS** for efficient similarity search.  

---

**⚠️ Note**: Always keep credentials (like `MONGO_URI`) private. Use `.gitignore`!
