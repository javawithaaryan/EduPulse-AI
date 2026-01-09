from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from models import db, Assignment, Submission, Performance, Quiz, Question, QuizAttempt, Attendance
from services.blob_service import BlobService
import json # Added for json.dumps in submit_quiz
from datetime import datetime

student_bp = Blueprint('student', __name__)

@student_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'student': return redirect(url_for('index'))
    # Show all assignments (submitted and not submitted can be filtered in template)
    assignments = Assignment.query.all()
    my_submissions = {s.assignment_id: s for s in Submission.query.filter_by(student_id=current_user.id).all()}
    
    quizzes = Quiz.query.all()
    today = datetime.utcnow().date()
    attendance_today = Attendance.query.filter_by(student_id=current_user.id, date=today).first()
    
    return render_template('dashboard/student.html', 
                          assignments=assignments, 
                          submissions=my_submissions, 
                          quizzes=quizzes, 
                          attempts={},  # Removed to fix SQL error
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

from models import db, Assignment, Submission, Performance, Quiz, Question, QuizAttempt, Attendance, ChatSession, ChatMessage
from services.vision_service import VisionService

# ... imports ...

@student_bp.route('/chat/new', methods=['POST'])
@login_required
def new_chat():
    session = ChatSession(user_id=current_user.id)
    db.session.add(session)
    db.session.commit()
    return {"session_id": session.id, "title": session.title}

@student_bp.route('/student/chats')
@login_required
def list_chats():
    sessions = ChatSession.query.filter_by(user_id=current_user.id).order_by(ChatSession.created_at.desc()).all()
    return {"chats": [s.to_dict() for s in sessions]}

@student_bp.route('/chat/<int:session_id>/history')
@login_required
def get_chat_history(session_id):
    session = ChatSession.query.get_or_404(session_id)
    if session.user_id != current_user.id: return {"error": "Unauthorized"}, 403
    
    messages = session.messages.order_by(ChatMessage.timestamp).all()
    return {"messages": [m.to_dict() for m in messages]}

@student_bp.route('/chat/<int:session_id>/message', methods=['POST'])
@login_required
def send_message(session_id):
    session = ChatSession.query.get_or_404(session_id)
    if session.user_id != current_user.id: return {"error": "Unauthorized"}, 403
    
    data = request.get_json()
    user_content = data.get('message')
    
    if not user_content: return {"error": "Message required"}, 400

    # 1. Save User Message
    user_msg = ChatMessage(session_id=session.id, role='user', content=user_content)
    db.session.add(user_msg)
    db.session.commit()

    # 2. Fetch History
    history_objs = session.messages.order_by(ChatMessage.timestamp).all()
    history = [{"role": m.role, "content": m.content} for m in history_objs]

    # 3. Get AI Response
    from services.openai_service import OpenAIService
    ai_response_content = OpenAIService.ask_ai(history, context="Student Dashboard Chat")

    # 4. Save AI Message
    ai_msg = ChatMessage(session_id=session.id, role='assistant', content=ai_response_content)
    db.session.add(ai_msg)
    db.session.commit()

    return {"response": ai_response_content, "message_id": ai_msg.id}

@student_bp.route('/chat/rag/<int:session_id>/message', methods=['POST'])
@login_required
def send_rag_message(session_id):
    """RAG-powered chat - answers grounded on academic notes only"""
    session = ChatSession.query.get_or_404(session_id)
    if session.user_id != current_user.id: 
        return {"error": "Unauthorized"}, 403
    
    data = request.get_json()
    user_content = data.get('message')
    subject = data.get('subject')  # Optional subject filter
    prompt_mode = data.get('prompt_mode')  # e.g., 'exam', 'summary'
    
    if not user_content: 
        return {"error": "Message required"}, 400

    # Apply prompt modifiers
    if prompt_mode == 'exam':
        user_content = f"Explain this topic in exam-oriented points using my notes: {user_content}"
    elif prompt_mode == 'summary':
        user_content = f"Give a concise summary of this topic from my notes: {user_content}"
    elif prompt_mode == 'syllabus':
        user_content = f"Explain this according to my syllabus/notes: {user_content}"

    # 1. Save User Message
    user_msg = ChatMessage(session_id=session.id, role='user', content=user_content)
    db.session.add(user_msg)
    db.session.commit()

    # 2. Fetch History (last 10 messages for context)
    history_objs = session.messages.order_by(ChatMessage.timestamp).limit(10).all()
    history = [{"role": m.role, "content": m.content} for m in history_objs[:-1]]  # Exclude current

    # 3. Get RAG Response
    from services.openai_service import OpenAIService
    rag_result = OpenAIService.ask_ai_rag(user_content, history, subject)

    # 4. Save AI Message
    ai_msg = ChatMessage(session_id=session.id, role='assistant', content=rag_result['content'])
    db.session.add(ai_msg)
    db.session.commit()

    return {
        "response": rag_result['content'],
        "citations": rag_result.get('citations', []),
        "message_id": ai_msg.id
    }

@student_bp.route('/chat/upload', methods=['POST'])
@login_required
def upload_chat_file():
    if 'file' not in request.files: return {"error": "No file"}, 400
    file = request.files['file']
    if file.filename == '': return {"error": "No file selected"}, 400

    # Upload to Blob (optional, skipping for speed, just processing)
    # Extract Text
    try:
        # We need to save temporarily to process with Vision (or pass stream if supported)
        # VisionService.extract_text expects a URL or local path.
        # For simplicity, let's assuming VisionService deals with it or we mock it for now if needed.
        # Actually VisionService.extract_text takes image_url.
        # We should upload first.
        file_url = BlobService.upload_file(file)
        extracted_text = VisionService.extract_text(file_url)
        
        return {"text": f"I have uploaded a file. Content: {extracted_text}", "url": file_url}
    except Exception as e:
        return {"error": str(e)}, 500

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

@student_bp.route('/api/ask-ai', methods=['POST'])
@login_required
def ask_ai_tutor():
    data = request.get_json()
    if not data:
        return {"error": "Invalid payload"}, 400
    
    question = data.get('question')
    student_name = data.get('studentName', getattr(current_user, 'name', 'Student'))
    grade = data.get('grade', '7')
    subject = data.get('subject', 'General')
    weak_topics = data.get('weakTopics', [])

    if not question:
        return {"error": "Question is required"}, 400

    from services.openai_service import OpenAIService
    response = OpenAIService.ask_tutor(
        question=question,
        student_name=student_name,
        grade=grade,
        subject=subject,
        weak_topics=weak_topics
    )

    return {"response": response}
