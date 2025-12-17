import os
import json
import random
from openai import OpenAI

api_key = os.environ.get("OPENAI_API_KEY")
client = None
if api_key:
    client = OpenAI(api_key=api_key)

def generate_study_plan(subject, hours_per_day, scenario, days=7):
    """Generate a personalized study plan using AI."""
    prompt = f"""Create a detailed {days}-day study plan for a student studying {subject}.
    
Requirements:
- Study hours per day: {hours_per_day}
- Scenario: {scenario}
- Include specific topics to cover each day
- Add time blocks with activities
- Include short breaks
- Make it practical and achievable

Format the response as JSON with this structure:
{{
    "plan_title": "Study Plan for {subject}",
    "total_days": {days},
    "hours_per_day": {hours_per_day},
    "daily_schedule": [
        {{
            "day": 1,
            "focus_topic": "Topic name",
            "activities": [
                {{"time": "9:00 AM - 10:00 AM", "activity": "Activity description"}},
                {{"time": "10:00 AM - 10:15 AM", "activity": "Short break"}}
            ],
            "goals": ["Goal 1", "Goal 2"]
        }}
    ],
    "weekly_goals": ["Goal 1", "Goal 2", "Goal 3"]
}}

Only respond with valid JSON, no additional text."""

    if not client:
        return create_fallback_study_plan(subject, hours_per_day, scenario, days)

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful study planning assistant. Always respond with valid JSON only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        result = response.choices[0].message.content.strip()
        if result.startswith("```json"):
            result = result[7:]
        if result.startswith("```"):
            result = result[3:]
        if result.endswith("```"):
            result = result[:-3]
        
        return json.loads(result.strip())
    except Exception as e:
        return create_fallback_study_plan(subject, hours_per_day, scenario, days)


def generate_quiz(subject, difficulty="medium", num_questions=5):
    """Generate a quiz with multiple-choice questions."""
    if not client:
        return create_fallback_quiz(subject, difficulty, num_questions)
    
    prompt = f"""Create a {difficulty} difficulty quiz about {subject} with {num_questions} multiple-choice questions.

Format the response as JSON with this structure:
{{
    "quiz_title": "Quiz: {subject}",
    "difficulty": "{difficulty}",
    "questions": [
        {{
            "id": 1,
            "question": "Question text here?",
            "options": ["A) Option 1", "B) Option 2", "C) Option 3", "D) Option 4"],
            "correct_answer": "A",
            "explanation": "Brief explanation of why this is correct"
        }}
    ]
}}

Only respond with valid JSON, no additional text."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an educational quiz creator. Always respond with valid JSON only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        result = response.choices[0].message.content.strip()
        if result.startswith("```json"):
            result = result[7:]
        if result.startswith("```"):
            result = result[3:]
        if result.endswith("```"):
            result = result[:-3]
        
        return json.loads(result.strip())
    except Exception as e:
        return create_fallback_quiz(subject, difficulty, num_questions)


def summarize_text(text, max_words=50):
    """Summarize provided text into key points."""
    if not client:
        return {
            "summary": text[:200] + "..." if len(text) > 200 else text,
            "key_points": ["Key concept from the text", "Important information", "Main idea"],
            "word_count": len(text.split())
        }
    
    prompt = f"""Summarize the following text into approximately {max_words} words. 
Extract the key points and main ideas.

Text to summarize:
{text}

Format the response as JSON:
{{
    "summary": "The summarized text here",
    "key_points": ["Point 1", "Point 2", "Point 3"],
    "word_count": number
}}

Only respond with valid JSON, no additional text."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a text summarization assistant. Always respond with valid JSON only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=500
        )
        
        result = response.choices[0].message.content.strip()
        if result.startswith("```json"):
            result = result[7:]
        if result.startswith("```"):
            result = result[3:]
        if result.endswith("```"):
            result = result[:-3]
        
        return json.loads(result.strip())
    except Exception as e:
        return {
            "summary": text[:200] + "..." if len(text) > 200 else text,
            "key_points": ["Key concept from the text"],
            "word_count": len(text.split())
        }


def generate_feedback(subject, performance="good"):
    """Generate motivational feedback for the student."""
    messages = [
        f"Great job studying {subject}! Keep up the excellent work!",
        f"You're making amazing progress in {subject}!",
        f"Your dedication to {subject} is inspiring!"
    ]
    
    if not client:
        return {
            "message": random.choice(messages),
            "tip": "Review your notes regularly for better retention.",
            "emoji": "star"
        }
    
    prompt = f"""Generate a short, encouraging feedback message for a student who is studying {subject}.
Their performance level is: {performance}

Format the response as JSON:
{{
    "message": "Encouraging message here",
    "tip": "A helpful study tip",
    "emoji": "An appropriate emoji"
}}

Only respond with valid JSON, no additional text."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a supportive educational coach. Always respond with valid JSON only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
            max_tokens=200
        )
        
        result = response.choices[0].message.content.strip()
        if result.startswith("```json"):
            result = result[7:]
        if result.startswith("```"):
            result = result[3:]
        if result.endswith("```"):
            result = result[:-3]
        
        return json.loads(result.strip())
    except Exception as e:
        messages = [
            f"Great job studying {subject}! Keep up the excellent work!",
            f"You're making amazing progress in {subject}!",
            f"Your dedication to {subject} is inspiring!"
        ]
        return {
            "message": random.choice(messages),
            "tip": "Review your notes regularly for better retention.",
            "emoji": "star"
        }


def create_fallback_study_plan(subject, hours_per_day, scenario, days):
    """Create a fallback study plan when API fails."""
    daily_schedule = []
    topics = ["Introduction & Basics", "Core Concepts", "Practice Problems", 
              "Advanced Topics", "Review & Summary", "Mock Tests", "Final Review"]
    
    for i in range(days):
        activities = []
        start_hour = 9
        remaining_hours = hours_per_day
        
        while remaining_hours > 0:
            study_time = min(1, remaining_hours)
            activities.append({
                "time": f"{start_hour}:00 AM - {start_hour + 1}:00 AM",
                "activity": f"Study {topics[i % len(topics)]}"
            })
            start_hour += 1
            remaining_hours -= 1
            
            if remaining_hours > 0:
                activities.append({
                    "time": f"{start_hour}:00 AM - {start_hour}:15 AM",
                    "activity": "Short break"
                })
        
        daily_schedule.append({
            "day": i + 1,
            "focus_topic": topics[i % len(topics)],
            "activities": activities,
            "goals": [f"Complete {topics[i % len(topics)]}", "Take notes", "Practice exercises"]
        })
    
    return {
        "plan_title": f"Study Plan for {subject}",
        "total_days": days,
        "hours_per_day": hours_per_day,
        "daily_schedule": daily_schedule,
        "weekly_goals": [
            f"Master {subject} fundamentals",
            "Complete all practice problems",
            f"Be prepared for {scenario}"
        ]
    }


def create_fallback_quiz(subject, difficulty, num_questions):
    """Create a fallback quiz when API fails."""
    questions = []
    sample_questions = {
        "mathematics": [
            {"q": "What is 2 + 2?", "opts": ["A) 3", "B) 4", "C) 5", "D) 6"], "ans": "B", "exp": "Basic addition."},
            {"q": "What is the square root of 16?", "opts": ["A) 2", "B) 3", "C) 4", "D) 5"], "ans": "C", "exp": "4 x 4 = 16."},
        ],
        "science": [
            {"q": "What is H2O?", "opts": ["A) Oxygen", "B) Hydrogen", "C) Water", "D) Carbon"], "ans": "C", "exp": "H2O is the chemical formula for water."},
            {"q": "What planet is closest to the Sun?", "opts": ["A) Venus", "B) Earth", "C) Mercury", "D) Mars"], "ans": "C", "exp": "Mercury is the closest planet to the Sun."},
        ]
    }
    
    base_questions = sample_questions.get(subject.lower(), sample_questions["science"])
    
    for i in range(num_questions):
        q = base_questions[i % len(base_questions)]
        questions.append({
            "id": i + 1,
            "question": q["q"],
            "options": q["opts"],
            "correct_answer": q["ans"],
            "explanation": q["exp"]
        })
    
    return {
        "quiz_title": f"Quiz: {subject}",
        "difficulty": difficulty,
        "questions": questions
    }
