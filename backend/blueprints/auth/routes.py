from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from models import User, db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect_to_dashboard(current_user.role)
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect_to_dashboard(user.role)
        else:
            flash('Invalid email or password', 'danger')
            
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect_to_dashboard(current_user.role)

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')
        if role not in ['student', 'teacher', 'parent', 'admin']:
            flash('Invalid role selected', 'danger')
            return redirect(url_for('auth.register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already exists', 'danger')
        else:
            user = User(username=username, email=email, role=role)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect_to_dashboard(role)
            
    return render_template('register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

def redirect_to_dashboard(role):
    if role == 'teacher': return redirect(url_for('teacher.dashboard'))
    if role == 'student': return redirect(url_for('student.dashboard'))
    if role == 'parent': return redirect(url_for('parent.dashboard'))
    if role == 'admin': return redirect(url_for('admin.dashboard'))
    return redirect(url_for('index'))
