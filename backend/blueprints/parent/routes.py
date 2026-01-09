from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from flask_login import login_required, current_user
from models import Performance, User, Fee, PaymentTransaction
from datetime import datetime, date, timedelta
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
    
    # Check for linked student from request args or session
    linked_student_email = request.args.get('student_email') or session.get('active_student_email')
    student_summary = None
    if linked_student_email:
        session['active_student_email'] = linked_student_email
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
    session['active_student_email'] = email
    flash(f'Successfully linked to {email}!', 'success')
    return redirect(url_for('parent.dashboard'))

@parent_bp.route('/fees')
@login_required
def fees():
    if current_user.role != 'parent': return redirect(url_for('index'))
    
    linked_student_email = request.args.get('student_email') or session.get('active_student_email')
    
    student = None
    all_fees = []
    total_due = 0
    history = []
    
    if linked_student_email:
        student = User.query.filter_by(email=linked_student_email, role='student').first()
        if not student:
            # For demo purposes, if student doesn't exist, we'll use a placeholder
            # or just show empty. Let's try to find ANY student if this one fails
            student = User.query.filter_by(role='student').first()
        
        if student:
            session['active_student_email'] = student.email
            existing_fees = Fee.query.filter_by(student_id=student.id).first()
            if not existing_fees:
                # Seed some sample fees
                f1 = Fee(student_id=student.id, title='Quarterly Tuition Fee', amount=1200.0, 
                         due_date=date.today() + timedelta(days=5), category='Tuition', 
                         description='Fees for Jan-Mar Quarter')
                f2 = Fee(student_id=student.id, title='Laboratory Fee', amount=150.0, 
                         due_date=date.today() - timedelta(days=2), category='Lab', 
                         status='Unpaid', description='Scientific lab equipment maintenance')
                f3 = Fee(student_id=student.id, title='Transport Fee', amount=300.0, 
                         due_date=date.today() + timedelta(days=15), category='Transport', 
                         status='Paid', description='Bus services for the month')
                from models import db
                db.session.add_all([f1, f2, f3])
                db.session.commit()

            all_fees = Fee.query.filter_by(student_id=student.id).all()
            total_due = sum(f.amount for f in all_fees if f.status != 'Paid')
            history = PaymentTransaction.query.filter_by(parent_id=current_user.id).all()
            
    return render_template('dashboard/parent_fees.html', 
                                 fees=all_fees, 
                                 total_due=total_due,
                                 student=student,
                                 payment_history=history,
                                 date=date) # Pass date for template comparison

@parent_bp.route('/pay_fee', methods=['POST'])
@login_required
def pay_fee():
    if current_user.role != 'parent': return redirect(url_for('index'))
    
    fee_ids = request.form.getlist('fee_ids')
    if not fee_ids:
        flash('No fees selected for payment.', 'warning')
        return redirect(url_for('parent.fees'))
    
    total_paid = 0
    from models import db
    for fid in fee_ids:
        fee = Fee.query.get(fid)
        if fee and fee.status != 'Paid':
            fee.status = 'Paid'
            total_paid += fee.amount
    
    if total_paid > 0:
        tx = PaymentTransaction(
            parent_id=current_user.id,
            fee_ids=",".join(fee_ids),
            transaction_ref=f"TXN-{int(datetime.now().timestamp())}",
            amount_paid=total_paid,
            method=request.form.get('method', 'UPI')
        )
        db.session.add(tx)
        db.session.commit()
        flash(f'Payment of ${total_paid} successful!', 'success')
    
    return redirect(url_for('parent.fees', student_email=request.form.get('student_email')))

# ============ NEW: Attendance Overview ============
@parent_bp.route('/attendance')
@login_required
def attendance():
    """Detailed attendance overview for linked child"""
    if current_user.role != 'parent': return redirect(url_for('index'))
    
    from models import Attendance
    
    linked_student_email = request.args.get('student_email') or session.get('active_student_email')
    student = None
    attendance_data = []
    monthly_rate = 0
    absence_details = []
    
    if linked_student_email:
        student = User.query.filter_by(email=linked_student_email).first()
        if student:
            # Get attendance for this month
            today = date.today()
            first_of_month = today.replace(day=1)
            
            records = Attendance.query.filter(
                Attendance.student_id == student.id,
                Attendance.date >= first_of_month
            ).all()
            
            total_days = len(records)
            present_days = sum(1 for r in records if r.status == 'Present')
            monthly_rate = round((present_days / total_days) * 100) if total_days > 0 else 100
            
            # Calendar data
            for r in records:
                attendance_data.append({
                    'date': r.date,
                    'status': r.status,
                    'day': r.date.day
                })
            
            # Absence details
            absences = [r for r in records if r.status != 'Present']
            for a in absences:
                absence_details.append({
                    'date': a.date.strftime('%b %d, %Y'),
                    'day': a.date.strftime('%A'),
                    'reason': getattr(a, 'reason', 'Not specified'),
                    'excused': getattr(a, 'excused', False)
                })
    
    return render_template('dashboard/parent_attendance.html',
                          student=student,
                          attendance_data=attendance_data,
                          monthly_rate=monthly_rate,
                          absence_details=absence_details,
                          present_days=present_days if linked_student_email and student else 0,
                          total_days=total_days if linked_student_email and student else 0)

# ============ NEW: Messages & Communication ============
@parent_bp.route('/messages')
@login_required
def messages():
    """Teacher-parent communication hub"""
    if current_user.role != 'parent': return redirect(url_for('index'))
    
    # Mock messages data (in real app, would query from Message model)
    mock_messages = [
        {
            'type': 'announcement',
            'title': 'Science Exhibition on Jan 25',
            'content': 'Students are encouraged to prepare projects on environmental topics. Deadline: Jan 20.',
            'from': 'School Admin',
            'date': datetime.now() - timedelta(hours=2),
            'read': False
        },
        {
            'type': 'feedback',
            'title': 'Weekly Progress Update',
            'content': 'Your child has been very active in class discussions this week. Science project was well-researched.',
            'from': 'Mrs. Sharma (Class Teacher)',
            'date': datetime.now() - timedelta(days=1),
            'read': True
        },
        {
            'type': 'meeting',
            'title': 'Parent-Teacher Meeting',
            'content': 'Date: Jan 15, 2026 | Time: 3:00 PM | Mode: In-Person | Venue: Room 204',
            'from': 'School Admin',
            'date': datetime.now() - timedelta(days=3),
            'read': True
        }
    ]
    
    return render_template('dashboard/parent_messages.html',
                          messages=mock_messages)

# ============ Enhanced Dashboard with Child Progress ============
@parent_bp.route('/progress')
@login_required  
def child_progress():
    """Detailed child progress overview"""
    if current_user.role != 'parent': return redirect(url_for('index'))
    
    from models import Attendance
    
    linked_student_email = request.args.get('student_email') or session.get('active_student_email')
    
    if not linked_student_email:
        return redirect(url_for('parent.dashboard'))
    
    student = User.query.filter_by(email=linked_student_email).first()
    if not student:
        flash('Student not found.', 'warning')
        return redirect(url_for('parent.dashboard'))
    
    # Get performance data
    performances = Performance.query.filter_by(student_id=student.id).all()
    
    # Calculate subject progress
    subject_progress = []
    for p in performances:
        trend_icon = '📈' if p.trend == 'improving' else '📉' if p.trend == 'declining' else '→'
        score = 85 if p.risk_level == 'low' else 70 if p.risk_level == 'medium' else 55
        subject_progress.append({
            'subject': p.subject,
            'score': score,
            'trend': p.trend,
            'trend_icon': trend_icon,
            'status': 'good' if p.risk_level == 'low' else 'attention' if p.risk_level == 'medium' else 'struggling'
        })
    
    # Overall status
    low_risk_count = sum(1 for p in performances if p.risk_level == 'low')
    overall_status = 'Doing Well' if low_risk_count >= len(performances) / 2 else 'Needs Attention'
    
    # Attendance
    attendance_records = Attendance.query.filter_by(student_id=student.id).all()
    attendance_rate = 95
    if attendance_records:
        present = sum(1 for r in attendance_records if r.status == 'Present')
        attendance_rate = round((present / len(attendance_records)) * 100)
    
    # AI suggestions
    suggestions = [
        "📚 Review Social Studies Chapter 4 together",
        "⏰ Help maintain homework schedule",
        "🎉 Celebrate the Science improvement!"
    ]
    
    return render_template('dashboard/parent_progress.html',
                          student=student,
                          subject_progress=subject_progress,
                          overall_status=overall_status,
                          attendance_rate=attendance_rate,
                          suggestions=suggestions)

