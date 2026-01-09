from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from models import db
from models.tasks import Task, Goal
from datetime import datetime, timedelta

tasks_bp = Blueprint('tasks', __name__, template_folder='templates')

@tasks_bp.route('/hub')
@login_required
def hub():
    # Get user's tasks
    today = datetime.utcnow().date()
    
    # Today's tasks
    today_tasks = Task.query.filter_by(
        user_id=current_user.id,
        status='pending'
    ).filter(
        db.func.date(Task.due_date) == today
    ).all()
    
    # Upcoming tasks (next 7 days)
    week_later = today + timedelta(days=7)
    upcoming_tasks = Task.query.filter_by(
        user_id=current_user.id,
        status='pending'
    ).filter(
        Task.due_date > datetime.utcnow(),
        db.func.date(Task.due_date) <= week_later
    ).order_by(Task.due_date).all()
    
    # Overdue tasks
    overdue_tasks = Task.query.filter_by(
        user_id=current_user.id,
        status='pending'
    ).filter(
        Task.due_date < datetime.utcnow()
    ).all()
    
    # Goals
    goals = Goal.query.filter_by(user_id=current_user.id).all()
    
    return render_template('tasks/hub.html',
                         today_tasks=today_tasks,
                         upcoming_tasks=upcoming_tasks,
                         overdue_tasks=overdue_tasks,
                         goals=goals)

@tasks_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_task():
    if request.method == 'POST':
        title = request.form.get('title')
        due_date_str = request.form.get('due_date')
        priority = request.form.get('priority', 'medium')
        
        due_date = datetime.strptime(due_date_str, '%Y-%m-%d') if due_date_str else None
        
        task = Task(
            user_id=current_user.id,
            title=title,
            description=request.form.get('description'),
            due_date=due_date,
            priority=priority
        )
        db.session.add(task)
        db.session.commit()
        
        flash('Task created!', 'success')
        return redirect(url_for('tasks.hub'))
    
    return render_template('tasks/create.html')

@tasks_bp.route('/<int:id>/complete', methods=['POST'])
@login_required
def complete_task(id):
    task = Task.query.get_or_404(id)
    if task.user_id != current_user.id:
        flash('Unauthorized', 'danger')
        return redirect(url_for('tasks.hub'))
    
    task.status = 'completed'
    task.completed_at = datetime.utcnow()
    db.session.commit()
    
    flash('Task completed! 🎉', 'success')
    return redirect(url_for('tasks.hub'))

@tasks_bp.route('/goal/create', methods=['POST'])
@login_required
def create_goal():
    title = request.form.get('title')
    target_date_str = request.form.get('target_date')
    target_date = datetime.strptime(target_date_str, '%Y-%m-%d') if target_date_str else None
    
    goal = Goal(
        user_id=current_user.id,
        title=title,
        description=request.form.get('description'),
        target_date=target_date
    )
    db.session.add(goal)
    db.session.commit()
    
    flash('Goal set!', 'success')
    return redirect(url_for('tasks.hub'))
