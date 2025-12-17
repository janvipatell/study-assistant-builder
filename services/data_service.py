import pandas as pd
import json
import os
import io
import base64
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')


def load_educational_content():
    """Load educational content from JSON file."""
    file_path = os.path.join(DATA_DIR, 'educational_content.json')
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "subjects": {},
            "study_tips_templates": [],
            "motivational_messages": []
        }


def get_resources_for_subject(subject):
    """Get recommended resources for a specific subject."""
    content = load_educational_content()
    subject_lower = subject.lower().replace(" ", "_")
    
    if subject_lower in content.get("subjects", {}):
        return content["subjects"][subject_lower].get("resources", [])
    
    default_resources = [
        {"name": "Khan Academy", "url": "https://www.khanacademy.org"},
        {"name": "Wikipedia", "url": f"https://en.wikipedia.org/wiki/{subject}"},
        {"name": "YouTube Educational", "url": f"https://www.youtube.com/results?search_query={subject}+tutorial"}
    ]
    return default_resources


def get_sample_content(subject):
    """Get sample educational content for a subject."""
    content = load_educational_content()
    subject_lower = subject.lower().replace(" ", "_")
    
    if subject_lower in content.get("subjects", {}):
        return content["subjects"][subject_lower].get("sample_content", "")
    
    return f"{subject} is an important field of study that encompasses various concepts and principles. Understanding the fundamentals is key to mastering this subject."


def get_topics_for_subject(subject):
    """Get topics list for a subject."""
    content = load_educational_content()
    subject_lower = subject.lower().replace(" ", "_")
    
    if subject_lower in content.get("subjects", {}):
        return content["subjects"][subject_lower].get("topics", [])
    
    return ["Introduction", "Basic Concepts", "Advanced Topics", "Practice", "Review"]


def save_user_session(session_data):
    """Save user session data to CSV."""
    sessions_file = os.path.join(DATA_DIR, 'user_sessions.csv')
    
    session_data['timestamp'] = datetime.now().isoformat()
    
    df_new = pd.DataFrame([session_data])
    
    if os.path.exists(sessions_file):
        df_existing = pd.read_csv(sessions_file)
        df = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df = df_new
    
    df.to_csv(sessions_file, index=False)
    return True


def get_session_statistics():
    """Get statistics from user sessions."""
    sessions_file = os.path.join(DATA_DIR, 'user_sessions.csv')
    
    if not os.path.exists(sessions_file):
        return {
            "total_sessions": 0,
            "subjects_studied": {},
            "avg_study_hours": 0
        }
    
    df = pd.read_csv(sessions_file)
    
    stats = {
        "total_sessions": len(df),
        "subjects_studied": df['subject'].value_counts().to_dict() if 'subject' in df.columns else {},
        "avg_study_hours": df['hours_per_day'].mean() if 'hours_per_day' in df.columns else 0
    }
    
    return stats


def generate_subject_chart():
    """Generate a pie chart of subjects studied."""
    stats = get_session_statistics()
    subjects = stats.get("subjects_studied", {})
    
    if not subjects:
        subjects = {"No data yet": 1}
    
    fig, ax = plt.subplots(figsize=(8, 6))
    colors = plt.cm.Set3(range(len(subjects)))
    
    wedges, texts, autotexts = ax.pie(
        subjects.values(),
        labels=subjects.keys(),
        autopct='%1.1f%%',
        colors=colors,
        startangle=90
    )
    
    ax.set_title('Subjects Studied Distribution', fontsize=14, fontweight='bold')
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    plt.close(fig)
    
    return image_base64


def create_schedule_csv(study_plan):
    """Create a downloadable CSV from study plan."""
    rows = []
    
    for day_schedule in study_plan.get("daily_schedule", []):
        day = day_schedule.get("day", 1)
        focus = day_schedule.get("focus_topic", "Study")
        
        for activity in day_schedule.get("activities", []):
            rows.append({
                "Day": day,
                "Focus Topic": focus,
                "Time": activity.get("time", ""),
                "Activity": activity.get("activity", ""),
                "Goals": ", ".join(day_schedule.get("goals", []))
            })
    
    if not rows:
        rows = [{"Day": 1, "Focus Topic": "Study", "Time": "9:00 AM", "Activity": "Begin studying", "Goals": "Complete tasks"}]
    
    df = pd.DataFrame(rows)
    
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    
    return csv_buffer.getvalue()


def clean_data(df):
    """Clean dataframe by removing duplicates and standardizing text."""
    df = df.drop_duplicates()
    
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].str.lower().str.strip()
    
    df = df.fillna("")
    
    return df
