import os
from flask import Flask, render_template, request, jsonify, Response, session
from services.ai_service import generate_study_plan, generate_quiz, summarize_text, generate_feedback
from services.nlp_service import generate_study_tips, extract_keywords, analyze_text_complexity
from services.data_service import (
    get_resources_for_subject, get_sample_content, save_user_session,
    get_session_statistics, generate_subject_chart, create_schedule_csv
)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")


@app.route('/')
def index():
    """Home page with main navigation."""
    stats = get_session_statistics()
    return render_template('index.html', stats=stats)


@app.route('/study-plan', methods=['GET', 'POST'])
def study_plan():
    """Generate a personalized study plan."""
    if request.method == 'POST':
        subject = request.form.get('subject', 'General')
        hours = int(request.form.get('hours', 2))
        scenario = request.form.get('scenario', 'Exam Preparation')
        days = int(request.form.get('days', 7))
        
        plan = generate_study_plan(subject, hours, scenario, days)
        
        resources = get_resources_for_subject(subject)
        
        save_user_session({
            'subject': subject,
            'hours_per_day': hours,
            'scenario': scenario,
            'feature_used': 'study_plan'
        })
        
        session['current_plan'] = plan
        
        return render_template('study_plan.html', plan=plan, resources=resources, subject=subject)
    
    return render_template('study_plan_form.html')


@app.route('/download-schedule')
def download_schedule():
    """Download study schedule as CSV."""
    plan = session.get('current_plan', {})
    
    if not plan:
        return "No study plan available. Please generate a plan first.", 400
    
    csv_content = create_schedule_csv(plan)
    
    return Response(
        csv_content,
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=study_schedule.csv'}
    )


@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    """Generate and take a quiz."""
    if request.method == 'POST':
        subject = request.form.get('subject', 'General')
        difficulty = request.form.get('difficulty', 'medium')
        num_questions = int(request.form.get('num_questions', 5))
        
        quiz_data = generate_quiz(subject, difficulty, num_questions)
        
        save_user_session({
            'subject': subject,
            'hours_per_day': 0,
            'scenario': f'{difficulty} quiz',
            'feature_used': 'quiz'
        })
        
        session['current_quiz'] = quiz_data
        
        return render_template('quiz.html', quiz=quiz_data, subject=subject)
    
    return render_template('quiz_form.html')


@app.route('/check-quiz', methods=['POST'])
def check_quiz():
    """Check quiz answers and provide feedback."""
    quiz_data = session.get('current_quiz', {})
    answers = request.form.to_dict()
    
    if not quiz_data:
        return jsonify({'error': 'No quiz data found'}), 400
    
    results = []
    correct_count = 0
    
    for question in quiz_data.get('questions', []):
        q_id = str(question['id'])
        user_answer = answers.get(f'q_{q_id}', '')
        correct = user_answer == question['correct_answer']
        
        if correct:
            correct_count += 1
        
        results.append({
            'question': question['question'],
            'user_answer': user_answer,
            'correct_answer': question['correct_answer'],
            'correct': correct,
            'explanation': question.get('explanation', '')
        })
    
    total = len(quiz_data.get('questions', []))
    score = (correct_count / total * 100) if total > 0 else 0
    
    if score >= 80:
        performance = "excellent"
    elif score >= 60:
        performance = "good"
    else:
        performance = "needs improvement"
    
    feedback = generate_feedback(quiz_data.get('quiz_title', 'Quiz'), performance)
    
    return render_template('quiz_results.html', 
                         results=results, 
                         score=score, 
                         correct=correct_count, 
                         total=total,
                         feedback=feedback)


@app.route('/summarize', methods=['GET', 'POST'])
def summarize():
    """Summarize text and extract key points."""
    if request.method == 'POST':
        text = request.form.get('text', '')
        subject = request.form.get('subject', 'General')
        
        if not text:
            return render_template('summarize_form.html', error="Please enter some text to summarize.")
        
        summary = summarize_text(text)
        
        tips = generate_study_tips(text, subject)
        
        complexity = analyze_text_complexity(text)
        
        save_user_session({
            'subject': subject,
            'hours_per_day': 0,
            'scenario': 'text summarization',
            'feature_used': 'summarize'
        })
        
        return render_template('summarize.html', 
                             summary=summary, 
                             tips=tips, 
                             complexity=complexity,
                             original_text=text,
                             subject=subject)
    
    return render_template('summarize_form.html')


@app.route('/resources')
def resources():
    """Show study resources and statistics."""
    stats = get_session_statistics()
    chart = generate_subject_chart()
    
    subjects = ['Mathematics', 'Science', 'History', 'English', 'Computer Science']
    all_resources = {}
    
    for subject in subjects:
        all_resources[subject] = get_resources_for_subject(subject)
    
    return render_template('resources.html', 
                         stats=stats, 
                         chart=chart, 
                         resources=all_resources)


@app.route('/api/feedback', methods=['POST'])
def get_feedback():
    """API endpoint for getting motivational feedback."""
    data = request.get_json()
    subject = data.get('subject', 'your studies')
    performance = data.get('performance', 'good')
    
    feedback = generate_feedback(subject, performance)
    return jsonify(feedback)


if __name__ == '__main__':
    os.makedirs('data', exist_ok=True)
    app.run(host='0.0.0.0', port=5000, debug=True)
