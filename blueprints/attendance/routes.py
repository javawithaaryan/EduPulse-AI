from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Attendance, User
from datetime import datetime

attendance_bp = Blueprint('attendance', __name__)

@attendance_bp.route('/mark', methods=['POST'])
@login_required
def mark_attendance():
    if current_user.role != 'teacher': return redirect(url_for('index'))
    
    student_id = request.form.get('student_id')
    status = request.form.get('status')
    
    # Check if entry already exists for today
    today = datetime.utcnow().date()
    existing = Attendance.query.filter_by(student_id=student_id, date=today).first()
    
    if existing:
        existing.status = status
    else:
        new_entry = Attendance(
            student_id=student_id,
            date=today,
            status=status,
            method='Manual'
        )
        db.session.add(new_entry)
        
    db.session.commit()
    flash('Attendance updated.', 'success')
    return redirect(url_for('teacher.dashboard'))

@attendance_bp.route('/self_checkin', methods=['POST'])
@login_required
def self_checkin():
    if current_user.role != 'student': return redirect(url_for('index'))
    
    today = datetime.utcnow().date()
    existing = Attendance.query.filter_by(student_id=current_user.id, date=today).first()
    
    if not existing:
        new_entry = Attendance(
            student_id=current_user.id,
            date=today,
            status='Present',
            method='Self-Check'
        )
        db.session.add(new_entry)
        db.session.commit()
        
    flash('Check-in successful!', 'success')
    return redirect(url_for('student.dashboard'))

@attendance_bp.route('/student_qr_checkin', methods=['POST'])
@login_required
def qr_checkin():
    if current_user.role != 'student': return redirect(url_for('index'))
    
    # Real-world: parse JSON QR token. Here: simulated.
    today = datetime.utcnow().date()
    existing = Attendance.query.filter_by(student_id=current_user.id, date=today).first()
    
    if existing:
        existing.status = 'Present'
        existing.method = 'QR-Scan'
    else:
        new_entry = Attendance(student_id=current_user.id, date=today, status='Present', method='QR-Scan')
        db.session.add(new_entry)
        
    db.session.commit()
    flash('QR Scan Verified: Marked as Present!', 'success')
    return redirect(url_for('student.dashboard'))
