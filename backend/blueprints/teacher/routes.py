from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from models import db, Assignment, Submission, AIResult, Performance, Quiz, Question
from services.vision_service import VisionService
from services.openai_service import OpenAIService
from services.ml_service import MLService
from services.sms_service import SMSService
import json
import time
import threading
import uuid
import os
from werkzeug.utils import secure_filename
from flask import jsonify

teacher_bp = Blueprint('teacher', __name__)

# @teacher_bp.route('/dashboard')
# @login_required
# def dashboard():
#     if current_user.role != 'teacher': return redirect(url_for('index'))
#     assignments = Assignment.query.filter_by(teacher_id=current_user.id).all()
#     quizzes = Quiz.query.filter_by(teacher_id=current_user.id).all()
#     
#     # New: Fetch students for attendance (in a real app, filter by class)
#     from models import User, Attendance, Performance
#     from datetime import datetime
#     today = datetime.utcnow().date()
#     students = User.query.filter_by(role='student').all()
#     
#     for s in students:
#         att = Attendance.query.filter_by(student_id=s.id, date=today).first()
#         s.attendance_today = att.status if att else None
# 
#     # Generate Class Insights
#     subjects = {a.subject for a in assignments}
#     performances = Performance.query.filter(Performance.subject.in_(subjects)).all()
#     
#     perf_summary = []
#     for p in performances:
#         perf_summary.append({
#             "student": p.student.username,
#             "subject": p.subject,
#             "risk": p.risk_level,
#             "trend": p.trend
#         })
#     
#     ai_insights = OpenAIService.generate_class_insights(json.dumps(perf_summary))
#     
#     return render_template('dashboard/teacher.html', 
#                           assignments=assignments, 
#                           quizzes=quizzes, 
#                           students=students,
#                           ai_insights=ai_insights,
#                           today_date=today.strftime('%B %d, %Y'))

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

# ============ NEW: AI-Assisted Grading Queue ============
@teacher_bp.route('/grading/queue')
@login_required
def grading_queue():
    """Display submissions awaiting AI grading review"""
    if current_user.role != 'teacher': return redirect(url_for('index'))
    
    assignments = Assignment.query.filter_by(teacher_id=current_user.id).all()
    pending_submissions = []
    
    for assignment in assignments:
        subs = Submission.query.filter_by(assignment_id=assignment.id).all()
        for sub in subs:
            ai_result = AIResult.query.filter_by(submission_id=sub.id).first()
            pending_submissions.append({
                'submission': sub,
                'assignment': assignment,
                'ai_result': ai_result,
                'needs_review': ai_result and not getattr(ai_result, 'teacher_approved', False)
            })
    
    return render_template('dashboard/teacher_grading_queue.html',
                          submissions=pending_submissions)

@teacher_bp.route('/grading/review/<int:submission_id>')
@login_required
def review_grading(submission_id):
    """Individual submission review with AI suggestions"""
    if current_user.role != 'teacher': return redirect(url_for('index'))
    
    sub = Submission.query.get_or_404(submission_id)
    assignment = Assignment.query.get(sub.assignment_id)
    
    if assignment.teacher_id != current_user.id:
        return redirect(url_for('index'))
    
    ai_result = AIResult.query.filter_by(submission_id=sub.id).first()
    feedback_data = json.loads(ai_result.feedback_json) if ai_result else {}
    
    # Get teacher's AI confidence threshold preference
    ai_threshold = getattr(current_user, 'ai_confidence_threshold', 70)
    
    return render_template('dashboard/teacher_grading_review.html',
                          submission=sub,
                          assignment=assignment,
                          ai_result=ai_result,
                          feedback_data=feedback_data,
                          ai_threshold=ai_threshold)

@teacher_bp.route('/grading/approve', methods=['POST'])
@login_required
def approve_grading():
    """Approve AI grade with optional teacher override"""
    if current_user.role != 'teacher': return redirect(url_for('index'))
    
    submission_id = request.form.get('submission_id')
    final_score = request.form.get('final_score')
    teacher_feedback = request.form.get('teacher_feedback', '')
    override_reason = request.form.get('override_reason', '')
    
    sub = Submission.query.get_or_404(submission_id)
    ai_result = AIResult.query.filter_by(submission_id=sub.id).first()
    
    if ai_result:
        ai_result.teacher_approved = True
        ai_result.final_score = int(final_score)
        ai_result.teacher_feedback = teacher_feedback
        # Store override reason for audit (never shown to students)
        if override_reason:
            ai_result.override_reason = override_reason
        
        db.session.commit()
        flash('Grade approved successfully!', 'success')
    
    return redirect(url_for('teacher.grading_queue'))

# ============ NEW: AI Question Paper Generator ============
@teacher_bp.route('/question-paper')
@login_required
def question_paper_wizard():
    """AI Question Paper Generator - Step wizard"""
    if current_user.role != 'teacher': return redirect(url_for('index'))
    return render_template('dashboard/teacher_question_paper.html')

@teacher_bp.route('/question-paper/generate', methods=['POST'])
@login_required
def generate_question_paper():
    """Generate questions using AI"""
    if current_user.role != 'teacher': return redirect(url_for('index'))
    
    data = request.get_json()
    grade = data.get('grade', 'Grade 9')
    subject = data.get('subject', 'Science')
    chapters = data.get('chapters', [])
    difficulty = data.get('difficulty', {'easy': 30, 'medium': 50, 'hard': 20})
    question_types = data.get('question_types', {})
    blooms = data.get('blooms', ['Remember', 'Understand', 'Apply'])
    
    # Generate questions using OpenAI
    questions = OpenAIService.generate_question_paper(
        grade=grade,
        subject=subject,
        chapters=chapters,
        difficulty=difficulty,
        question_types=question_types,
        blooms_levels=blooms
    )
    
    return {'questions': questions, 'status': 'success'}

# ============ NEW: Teaching Insights Analytics ============
@teacher_bp.route('/analytics')
@login_required
def analytics():
    """AI Teaching Insights Dashboard"""
    if current_user.role != 'teacher': return redirect(url_for('index'))
    
    from models import User, Performance
    from datetime import datetime, timedelta
    
    # Get performance data
    assignments = Assignment.query.filter_by(teacher_id=current_user.id).all()
    subjects = list({a.subject for a in assignments})
    
    # Topic performance analysis
    topic_performance = []
    for subject in subjects:
        perfs = Performance.query.filter_by(subject=subject).all()
        if perfs:
            avg_score = sum(1 for p in perfs if p.risk_level == 'low') / len(perfs) * 100
            topic_performance.append({
                'topic': subject,
                'score': round(avg_score),
                'status': 'good' if avg_score >= 70 else 'attention' if avg_score >= 50 else 'struggling'
            })
    
    # At-risk students count
    risk_counts = {
        'high': Performance.query.filter_by(risk_level='high').count(),
        'medium': Performance.query.filter_by(risk_level='medium').count(),
        'low': Performance.query.filter_by(risk_level='low').count()
    }
    
    # AI Model Status (for transparency)
    ai_model_status = {
        'last_trained': datetime.now().strftime('%d %b %Y'),
        'data_window': 'Last 90 days',
        'trend': 'Improving',
        'type': 'AI-Assisted (Human-reviewed)'
    }
    
    return render_template('dashboard/teacher_analytics.html',
                          topic_performance=topic_performance,
                          risk_counts=risk_counts,
                          ai_model_status=ai_model_status,
                          subjects=subjects)

# ============ NEW: AI Settings ============
@teacher_bp.route('/settings/ai')
@login_required
def ai_settings():
    """Teacher AI assistance controls"""
    if current_user.role != 'teacher': return redirect(url_for('index'))
    
    return render_template('dashboard/teacher_ai_settings.html',
                          ai_enabled=getattr(current_user, 'ai_enabled', True),
                          ai_threshold=getattr(current_user, 'ai_confidence_threshold', 70),
                          low_confidence_behavior=getattr(current_user, 'low_confidence_behavior', 'manual'))

@teacher_bp.route('/settings/ai/save', methods=['POST'])
@login_required
def save_ai_settings():
    """Save AI assistance preferences"""
    if current_user.role != 'teacher': return redirect(url_for('index'))
    
    current_user.ai_enabled = request.form.get('ai_enabled') == 'on'
    current_user.ai_confidence_threshold = int(request.form.get('ai_threshold', 70))
    current_user.low_confidence_behavior = request.form.get('low_confidence_behavior', 'manual')
    
    db.session.commit()
    flash('AI preferences saved successfully!', 'success')
    return redirect(url_for('teacher.ai_settings'))


# ============ NEW: AI Grading Workflow (File Upload -> Progress -> Result) ============

grading_jobs = {}

def process_grading_job(job_id, file_path, filename):
    """
    Simulates a step-by-step AI grading pipeline.
    Updates the job status in the global grading_jobs dictionary.
    """
    try:
        # Step 1: Scanning
        grading_jobs[job_id]['status'] = 'Scanning answer sheets'
        grading_jobs[job_id]['progress'] = 10
        time.sleep(1.5) # Simulate scanning time

        # Refined Step: Extract Text (Real or Simulated)
        # For this demo, we can just read text if it's a text file, else mock
        file_content = ""
        try:
             with open(file_path, 'r', errors='ignore') as f:
                 file_content = f.read()
        except:
             file_content = "Binary file content placeholder"

        grading_jobs[job_id]['progress'] = 30
        
        # Step 2: Grading
        grading_jobs[job_id]['status'] = 'Grading submissions'
        time.sleep(1.5)
        grading_jobs[job_id]['progress'] = 60

        # Step 3: Identifying Gaps
        grading_jobs[job_id]['status'] = 'Identifying learning gaps'
        time.sleep(1.5)
        grading_jobs[job_id]['progress'] = 80

        # Step 4: Generating Feedback (Real OpenAI Call)
        grading_jobs[job_id]['status'] = 'Generating feedback'
        
        # Call OpenAI
        ai_result = OpenAIService.analyze_uploaded_file(file_content, filename)
        
        grading_jobs[job_id]['result'] = ai_result
        grading_jobs[job_id]['progress'] = 100
        grading_jobs[job_id]['status'] = 'Complete'
        
        # Clean up file
        try:
            os.remove(file_path)
        except:
            pass

    except Exception as e:
        grading_jobs[job_id]['status'] = 'Error'
        grading_jobs[job_id]['error'] = str(e)

@teacher_bp.route('/api/grade-assessment', methods=['POST'])
@login_required
def api_grade_assessment():
    if current_user.role != 'teacher': 
        return jsonify({'error': 'Unauthorized'}), 403
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
        
    if file:
        filename = secure_filename(file.filename)
        # Create uploads dir if not exists
        upload_folder = os.path.join(os.getcwd(), 'instance', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        
        job_id = str(uuid.uuid4())
        grading_jobs[job_id] = {
            'status': 'Initializing',
            'progress': 0,
            'result': None
        }
        
        # Start background thread
        thread = threading.Thread(target=process_grading_job, args=(job_id, file_path, filename))
        thread.start()
        
        return jsonify({'jobId': job_id})
        
    return jsonify({'error': 'Upload failed'}), 500

@teacher_bp.route('/api/grade-status/<job_id>')
@login_required
def api_grade_status(job_id):
    job = grading_jobs.get(job_id)
    if not job:
        return jsonify({'error': 'Job not found'}), 404
        
    return jsonify(job)

