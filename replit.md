# AI Study Pal - Project Documentation

## Overview
AI Study Pal is a web-based study assistant application built with Flask that helps students with:
- Personalized AI-generated study plans
- Automated quiz generation with multiple-choice questions
- Text summarization and keyword extraction
- Study tips based on NLP analysis
- Resource recommendations by subject
- Downloadable CSV study schedules

## Project Structure
```
/
├── app.py                    # Main Flask application
├── services/
│   ├── __init__.py
│   ├── ai_service.py         # OpenAI integration for AI features
│   ├── nlp_service.py        # NLTK-based NLP utilities
│   └── data_service.py       # Data handling and visualization
├── templates/
│   ├── base.html             # Base template with navigation
│   ├── index.html            # Home page
│   ├── study_plan_form.html  # Study plan input form
│   ├── study_plan.html       # Study plan results
│   ├── quiz_form.html        # Quiz configuration form
│   ├── quiz.html             # Quiz questions
│   ├── quiz_results.html     # Quiz results and feedback
│   ├── summarize_form.html   # Text summarization form
│   ├── summarize.html        # Summary results
│   └── resources.html        # Resources and statistics
├── data/
│   └── educational_content.json  # Subject data and resources
└── requirements.txt          # Python dependencies
```

## Technologies Used
- **Python 3.11** - Programming language
- **Flask** - Web framework
- **OpenAI API** - AI-powered features (study plans, quizzes, summaries)
- **NLTK** - Natural Language Processing for keyword extraction
- **Pandas** - Data handling and CSV generation
- **Matplotlib** - Data visualization (pie charts)
- **scikit-learn** - Machine learning utilities
- **Bootstrap 5** - Frontend styling

## Key Features
1. **Study Plan Generator**: Creates personalized study schedules based on subject, hours, and scenario
2. **Quiz System**: Generates multiple-choice quizzes with difficulty levels
3. **Text Summarizer**: Condenses text and extracts keywords using NLP
4. **Study Tips**: Generates personalized tips based on content analysis
5. **Resource Suggestions**: Recommends learning resources by subject
6. **CSV Export**: Download study schedules as CSV files

## Environment Variables
- `OPENAI_API_KEY` - Required for AI features
- `SESSION_SECRET` - Flask session secret key

## Running the Application
The application runs on port 5000:
```bash
python app.py
```

## Recent Changes
- Initial project setup (December 2024)
- Created Flask app with all core features
- Implemented AI services using OpenAI
- Added NLP keyword extraction with NLTK
- Created responsive Bootstrap templates
