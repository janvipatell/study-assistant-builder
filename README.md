# Study Assistant Builder 🧠📚

A smart web-based Study Assistant built using **Flask** and **AI services** to help students generate personalized study plans, quizzes, summaries, and learning resources.

This project demonstrates how AI can be integrated into a web application to enhance learning productivity.

---

## Features:

- Generate :**personalized study plans**
- Create : **AI-generated quizzes**
- Summarize study topics automatically
- Get :**learning tips** based on subject
- Track user sessions and statistics
- AI-powered text analysis (keywords, complexity)

---

## 🛠️ Tech Stack

### Frontend
- HTML5
- CSS (via templates)
- Jinja2 (Flask templating)

### Backend
- Python
- Flask

### AI / NLP
- AI text generation services
- Basic NLP utilities
- Optional: NLTK (if enabled)

### Data Storage
- JSON files
- CSV files for session tracking

---

## 📂 Project Structure




Study-Assistant-Builder/
│
├── app.py # Main Flask application
├── services/ # Core logic and AI services
│ ├── ai_service.py
│ ├── nlp_service.py
│ └── data_service.py
│
├── templates/ # HTML templates
│
├── data/ # Stored content and user sessions
│
├── pyproject.toml # Project dependencies
└── README.md




---

##  How It Works

1. User selects a subject or study option
2. Flask backend handles the request
3. AI services generate:
   - Study plans 
   - Quizzes
   - Summaries
4. Results are displayed on the web interface
5. Session data is stored for analytics

---

## How to Run the Project

python app.py

## Then open:
http://127.0.0.1:5001/

