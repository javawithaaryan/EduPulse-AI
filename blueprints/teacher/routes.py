from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from models import db, Assignment, Submission, AIResult, Performance, Quiz, Question
from services.vision_service import VisionService
from services.openai_service import OpenAIService
from services.ml_service import MLService
from services.sms_service import SMSService
import json

teacher_bp = Blueprint('teacher', __name__)

@teacher_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'teacher': return redirect(url_for('index'))
    assignments = Assignment.query.filter_by(teacher_id=current_user.id).all()
    quizzes = Quiz.query.filter_by(teacher_id=current_user.id).all()
    
    # New: Fetch students for attendance (in a real app, filter by class)
    from models import User, Attendance, Performance
    from datetime import datetime
    today = datetime.utcnow().date()
    students = User.query.filter_by(role='student').all()
    
    for s in students:
        att = Attendance.query.filter_by(student_id=s.id, date=today).first()
        s.attendance_today = att.status if att else None

    # Generate Class Insights
    subjects = {a.subject for a in assignments}
    performances = Performance.query.filter(Performance.subject.in_(subjects)).all()
    
    perf_summary = []
    for p in performances:
        perf_summary.append({
            "student": p.student.username,
            "subject": p.subject,
            "risk": p.risk_level,
            "trend": p.trend
        })
    
    ai_insights = OpenAIService.generate_class_insights(json.dumps(perf_summary))
    
    return render_template('dashboard/teacher.html', 
                          assignments=assignments, 
                          quizzes=quizzes, 
                          students=students,
                          ai_insights=ai_insights,
                          today_date=today.strftime('%B %d, %Y'))

@teacher_bp.route('/assignment/new', methods=['POST'])
@login_required
def create_assignment():
    if current_user.role != 'teacher': return redirect(url_for('index'))
    
    title = request.form.get('title')
    subject = request.form.get('subject')
    rubric = request.form.get('rubric')
    max_marks = request.form.get('max_marks')
    
    assignment = Assignment(
        title=title, 
        subject=subject, 
        rubric=rubric, 
        max_marks=int(max_marks), 
        teacher_id=current_user.id
    )
    db.session.add(assignment)
    db.session.commit()
    flash('Assignment created successfully', 'success')
    return redirect(url_for('teacher.dashboard'))

@teacher_bp.route('/assignment/<int:id>/grade')
@login_required
def trigger_grading(id):
    assignment = Assignment.query.get_or_404(id)
    if assignment.teacher_id != current_user.id: return redirect(url_for('index'))
    
    submissions = Submission.query.filter_by(assignment_id=id, status='pending').all()
    count = 0
    
    for sub in submissions:
        # 1. OCR
        extracted_text = VisionService.extract_text(sub.file_url)
        sub.extracted_text = extracted_text
        
        # 2. AI Grading
        ai_response = OpenAIService.grade_submission(
            extracted_text, assignment.subject, "Grade 10", assignment.rubric, assignment.max_marks
        )
        
        # 3. Store Result
        result = AIResult(
            submission_id=sub.id,
            score=ai_response.get('score', 0),
            feedback_json=json.dumps(ai_response),
            strengths=json.dumps(ai_response.get('strengths', [])),
            improvements=json.dumps(ai_response.get('improvements', []))
        )
        db.session.add(result)
        sub.status = 'graded'
        
        # 4. Update Performance (ML)
        # Fetch attendance rate for this student in this subject (mock logic for now)
        from models import Attendance
        attendance_records = Attendance.query.filter_by(student_id=sub.student_id).all()
        present_count = sum(1 for a in attendance_records if a.status == 'Present')
        attendance_rate = (present_count / len(attendance_records) * 100) if attendance_records else 100
        
        risk_data = MLService.predict_risk(sub.student_id, [ai_response.get('score', 0)], attendance_rate)
        
        # Update or Create Performance Record
        perf = Performance.query.filter_by(student_id=sub.student_id, subject=assignment.subject).first()
        if not perf:
            perf = Performance(student_id=sub.student_id, subject=assignment.subject)
            db.session.add(perf)
        
        perf.risk_level = risk_data['risk_level']
        perf.trend = risk_data['trend']
        
        # 5. Send SMS if High Risk
        if perf.risk_level == 'high':
            # In a real app, we'd look up parent phone. Mocking sending to generic.
            SMSService.send_alert("PARENT_PHONE", sub.student.username, "high")
        
        count += 1

    db.session.commit()
    flash(f'Graded {count} submissions with AI!', 'success')
    return redirect(url_for('teacher.dashboard'))

@teacher_bp.route('/quiz/new', methods=['POST'])
@login_required
def create_quiz():
    if current_user.role != 'teacher': return redirect(url_for('index'))
    
    title = request.form.get('title')
    subject = request.form.get('subject')
    questions_data = request.form.get('questions') # Expecting JSON string from frontend
    
    quiz = Quiz(title=title, subject=subject, teacher_id=current_user.id)
    db.session.add(quiz)
    
    if questions_data:
        try:
            questions = json.loads(questions_data)
            for q in questions:
                new_q = Question(
                    quiz=quiz,
                    text=q['text'],
                    options=q['options'],
                    correct_answer=q['correct_answer'],
                    explanation=q.get('explanation', '')
                )
                db.session.add(new_q)
        except Exception as e:
            db.session.rollback()
            flash(f'Error processing questions: {str(e)}', 'danger')
            return redirect(url_for('teacher.dashboard'))
            
    db.session.commit()
    flash('Quiz created successfully!', 'success')
    return redirect(url_for('teacher.dashboard'))
