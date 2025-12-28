from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from models import db
from models.user import User
from models.assignment import Assignment
from models.submission import Submission
from models.quiz import Quiz, QuizAttempt
from models.attendance import Attendance
from models.wellbeing import EmotionalCheckin
from datetime import datetime, timedelta

admin_bp = Blueprint('admin', __name__, template_folder='templates')

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    # Check admin authorization
    if current_user.role != 'admin':
        flash("Unauthorized access", "danger")
        return redirect(url_for('index'))
    
    # System Metrics
    total_users = User.query.count()
    total_assignments = Assignment.query.count()
    total_quizzes = Quiz.query.count()
    total_submissions = Submission.query.count()
    
    # Engagement Metrics (last 7 days)
    week_ago = datetime.utcnow() - timedelta(days=7)
    
    active_students = Attendance.query.filter(
        Attendance.date >= week_ago.date()
    ).distinct(Attendance.student_id).count()
    
    quiz_attempts_week = QuizAttempt.query.filter(
        QuizAttempt.submitted_at >= week_ago
    ).count()
    
    # Well-being Check-ins
    checkins_week = EmotionalCheckin.query.filter(
        EmotionalCheckin.created_at >= week_ago
    ).count()
    
    # AI Accuracy (mock - based on average quiz scores)
    recent_attempts = QuizAttempt.query.limit(100).all()
    if recent_attempts:
        avg_score = sum(a.score for a in recent_attempts) / len(recent_attempts)
        ai_accuracy = min(95, max(75, avg_score * 10))  # Scale to 75-95%
    else:
        ai_accuracy = 85
    
    # Weekly submission trend (last 4 weeks)
    weekly_data = []
    for i in range(4):
        week_start = datetime.utcnow() - timedelta(weeks=i+1)
        week_end = datetime.utcnow() - timedelta(weeks=i)
        count = Submission.query.filter(
            Submission.submitted_at >= week_start,
            Submission.submitted_at < week_end
        ).count()
        weekly_data.append({
            'week': f'Week {4-i}',
            'count': count
        })
    weekly_data.reverse()
    
    # Average quiz score trend
    quiz_trend = []
    for i in range(4):
        week_start = datetime.utcnow() - timedelta(weeks=i+1)
        week_end = datetime.utcnow() - timedelta(weeks=i)
        attempts = QuizAttempt.query.filter(
            QuizAttempt.submitted_at >= week_start,
            QuizAttempt.submitted_at < week_end
        ).all()
        avg = sum(a.score for a in attempts) / len(attempts) if attempts else 0
        quiz_trend.append({
            'week': f'Week {4-i}',
            'avg_score': round(avg, 1)
        })
    quiz_trend.reverse()
    
    return render_template('dashboard/admin.html',
                         total_users=total_users,
                         total_assignments=total_assignments,
                         total_quizzes=total_quizzes,
                         total_submissions=total_submissions,
                         active_students=active_students,
                         quiz_attempts_week=quiz_attempts_week,
                         checkins_week=checkins_week,
                         ai_accuracy=round(ai_accuracy, 1),
                         weekly_data=weekly_data,
                         quiz_trend=quiz_trend)
