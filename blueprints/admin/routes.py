from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'admin':
        return redirect(url_for('index'))
    
    from models import User, Assignment, Submission, Quiz
    total_users = User.query.count()
    total_assignments = Assignment.query.count()
    total_submissions = Submission.query.count()
    total_quizzes = Quiz.query.count()
    
    stats = {
        "grading_time_saved": f"{total_submissions * 5}m", # Simulated 5 mins saved per AI grade
        "assignments_graded": total_submissions,
        "ai_accuracy": "98.2%", # Simulated constant or derived
        "teacher_feedback": f"Managing {total_users} active users across {total_quizzes} interactive modules."
    }
    return render_template('dashboard/admin.html', stats=stats, 
                          counts={'users': total_users, 'assignments': total_assignments, 'quizzes': total_quizzes})
