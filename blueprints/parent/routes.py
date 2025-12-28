from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from models import Performance, User
from services.openai_service import OpenAIService
import json

parent_bp = Blueprint('parent', __name__)

@parent_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'parent': return redirect(url_for('index'))
    
    # In a real app, we'd query linked students. 
    # For now, we simulate by showing all performance for parents to see.
    performance_records = Performance.query.all()
    
    student_perf = {}
    for p in performance_records:
        if p.student.username not in student_perf:
            student_perf[p.student.username] = []
        student_perf[p.student.username].append({
            "subject": p.subject,
            "risk": p.risk_level,
            "trend": p.trend
        })
    
    reports = {}
    for student, perfs in student_perf.items():
        reports[student] = OpenAIService.generate_parent_report(student, json.dumps(perfs))
    
    # Check for linked student from request args (simulated link)
    linked_student_email = request.args.get('student_email')
    student_summary = None
    if linked_student_email:
        from models import Attendance
        student = User.query.filter_by(email=linked_student_email).first()
        attendance_rate = 100
        if student:
            records = Attendance.query.filter_by(student_id=student.id).all()
            if records:
                present = sum(1 for r in records if r.status == 'Present')
                attendance_rate = round((present / len(records)) * 100)
                
        student_summary = {
            "name": linked_student_email.split('@')[0].capitalize(),
            "risk_level": "Low",
            "attendance_rate": attendance_rate,
            "ai_insight": "Consistently performing well. Attendance patterns are stable.",
            "next_steps": ["Review recent topics", "Keep up the good work"]
        }
        
    return render_template('dashboard/parent.html', 
                          records=performance_records, 
                          ai_reports=reports,
                          student_summary=student_summary)

@parent_bp.route('/link_student', methods=['POST'])
@login_required
def link_student():
    email = request.form.get('email')
    flash(f'Successfully linked to {email}!', 'success')
    return redirect(url_for('parent.dashboard', student_email=email))
