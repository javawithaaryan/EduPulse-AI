from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from models import db, Assignment, Submission, Performance, Quiz, Question, QuizAttempt
from services.blob_service import BlobService
import json # Added for json.dumps in submit_quiz

student_bp = Blueprint('student', __name__)

@student_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'student': return redirect(url_for('index'))
    # Show all assignments (submitted and not submitted can be filtered in template)
    assignments = Assignment.query.all()
    my_submissions = {s.assignment_id: s for s in Submission.query.filter_by(student_id=current_user.id).all()}
    
    quizzes = Quiz.query.all()
    attempts = {a.quiz_id: a for a in QuizAttempt.query.filter_by(student_id=current_user.id).all()}
    
    from datetime import datetime
    from models import Attendance
    today = datetime.utcnow().date()
    attendance_today = Attendance.query.filter_by(student_id=current_user.id, date=today).first()
    
    return render_template('dashboard/student.html', 
                          assignments=assignments, 
                          submissions=my_submissions, 
                          quizzes=quizzes, 
                          attempts=attempts,
                          attendance_today=attendance_today.status if attendance_today else None,
                          today_date=today.strftime('%B %d, %Y'))

@student_bp.route('/assignment/<int:id>/submit', methods=['POST'])
@login_required
def submit_assignment(id):
    if 'file' not in request.files:
        flash('No file part', 'danger')
        return redirect(url_for('student.dashboard'))
    
    file = request.files['file']
    if file.filename == '':
        flash('No selected file', 'danger')
        return redirect(url_for('student.dashboard'))
        
    file_url = BlobService.upload_file(file)
    
    submission = Submission(
        assignment_id=id,
        student_id=current_user.id,
        file_url=file_url
    )
    db.session.add(submission)
    db.session.commit()
    
    flash('Assignment submitted successfully!', 'success')
    return redirect(url_for('student.dashboard'))

@student_bp.route('/ask-ai', methods=['POST'])
@login_required
def ask_ai():
    if current_user.role != 'student': return {"error": "Unauthorized"}, 403
    
    data = request.get_json()
    question = data.get('question')
    context = data.get('context', 'General Education')
    
    if not question:
        return {"error": "Question is required"}, 400
        
    from services.openai_service import OpenAIService
    response = OpenAIService.ask_ai(question, context)
    
    return {"response": response}

@student_bp.route('/quiz/<int:id>/take')
@login_required
def take_quiz(id):
    quiz = Quiz.query.get_or_404(id)
    # Check if already attempted
    attempt = QuizAttempt.query.filter_by(quiz_id=id, student_id=current_user.id).first()
    if attempt:
        flash('You have already completed this quiz.', 'info')
        return redirect(url_for('student.dashboard'))
    return render_template('dashboard/quiz_taker.html', quiz=quiz)

@student_bp.route('/quiz/<int:id>/submit', methods=['POST'])
@login_required
def submit_quiz(id):
    quiz = Quiz.query.get_or_404(id)
    answers = request.get_json()
    
    correct_count = 0
    total = len(quiz.questions)
    feedback_details = []

    for q in quiz.questions:
        user_ans = answers.get(str(q.id))
        is_correct = (user_ans == q.correct_answer)
        if is_correct: correct_count += 1
        
        feedback_details.append({
            "question": q.text,
            "user_answer": user_ans,
            "correct_answer": q.correct_answer,
            "is_correct": is_correct,
            "explanation": q.explanation
        })

    score = (correct_count / total) * 100 if total > 0 else 0
    
    # AI Feedback based on details
    from services.openai_service import OpenAIService
    ai_feedback = OpenAIService.ask_ai(
        f"The student scored {score}% on a quiz about {quiz.subject}. Details: {json.dumps(feedback_details)}",
        "Educational Coach"
    )

    attempt = QuizAttempt(
        quiz_id=quiz.id,
        student_id=current_user.id,
        score=score,
        total_questions=total,
        feedback=ai_feedback
    )
    db.session.add(attempt)
    db.session.commit()
    
    return {"score": score, "feedback": ai_feedback, "details": feedback_details}

@student_bp.route('/learning_path')
@login_required
def learning_path():
    """Display personalized learning path"""
    from services.adaptive_service import AdaptiveService
    
    # Get subject from query or default to Mathematics
    subject = request.args.get('subject', 'Mathematics')
    
    # Generate adaptive learning path
    path_data = AdaptiveService.get_learning_path(current_user.id, subject)
    
    # Get available subjects
    subjects = ['Mathematics', 'Science', 'Computer Science', 'History', 'English']
    
    return render_template('student/learning_path.html',
                         path_data=path_data,
                         subjects=subjects,
                         current_subject=subject)
