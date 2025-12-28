from flask import Flask, render_template
from config import Config
from models import db, User
from flask_login import LoginManager

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Extensions
    db.init_app(app)
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register Blueprints
    from blueprints.auth.routes import auth_bp
    from blueprints.teacher.routes import teacher_bp
    from blueprints.student.routes import student_bp
    from blueprints.parent.routes import parent_bp
    from blueprints.admin.routes import admin_bp
    from blueprints.attendance.routes import attendance_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(teacher_bp, url_prefix='/teacher')
    app.register_blueprint(student_bp, url_prefix='/student')
    app.register_blueprint(parent_bp, url_prefix='/parent')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(attendance_bp, url_prefix='/attendance')

    # Root Route
    @app.route('/')
    def index():
        return render_template('index.html')

    # Create DB Tables (for development convenience)
    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
