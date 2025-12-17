# AI Study Pal

A web-based AI-powered study assistant that helps students learn more effectively.

## Features

- **AI Study Plans**: Generate personalized study schedules based on your subject, available time, and goals
- **Practice Quizzes**: Take AI-generated multiple-choice quizzes with instant feedback
- **Text Summarizer**: Condense study materials and extract key points
- **Study Tips**: Get personalized study tips based on NLP analysis
- **Resource Suggestions**: Access curated learning resources for each subject
- **CSV Export**: Download your study schedules

## Requirements

- Python 3.8+
- OpenAI API key

## Installation (For Local Setup - VS Code)

1. **Clone or download the project files**

2. **Create a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install flask pandas matplotlib scikit-learn nltk openai
   ```

4. **Set up your OpenAI API key**:
   - Create a file named `.env` in the project root
   - Add: `OPENAI_API_KEY=your_api_key_here`
   
   OR set it as an environment variable:
   ```bash
   # On Windows:
   set OPENAI_API_KEY=your_api_key_here
   
   # On Mac/Linux:
   export OPENAI_API_KEY=your_api_key_here
   ```

5. **Run the application**:
   ```bash
   python app.py
   ```

6. **Open in browser**: Go to `http://localhost:5000`

## Project Structure

```
ai-study-pal/
├── app.py                    # Main Flask application
├── services/
│   ├── ai_service.py         # OpenAI integration
│   ├── nlp_service.py        # NLTK text processing
│   └── data_service.py       # Data handling & visualization
├── templates/                # HTML templates
├── data/
│   └── educational_content.json
├── requirements.txt
└── README.md
```

## Technologies Used

- **Backend**: Python, Flask
- **AI**: OpenAI GPT API
- **NLP**: NLTK (Natural Language Toolkit)
- **Data**: Pandas, Matplotlib
- **ML**: scikit-learn
- **Frontend**: HTML, CSS, Bootstrap 5, JavaScript

## How to Use

1. **Study Plan**: Enter your subject, study hours per day, and scenario to generate a personalized plan
2. **Quiz**: Select a subject and difficulty to take a practice quiz
3. **Summarize**: Paste any text to get a summary, keywords, and study tips
4. **Resources**: View recommended learning resources and your study statistics

## For Your Video Presentation

When demonstrating this project:
1. Show the home page with all features
2. Create a study plan and download the CSV
3. Take a quiz and show the results/feedback
4. Summarize some text and show the keywords extracted
5. View the resources page with the statistics chart

## License

This project is for educational purposes.
