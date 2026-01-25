from flask import Flask, render_template, redirect, url_for, jsonify, abort, send_from_directory
from jinja2 import ChoiceLoader, FileSystemLoader
from flask_cors import CORS
from dotenv import load_dotenv

from dotenv import load_dotenv
import os

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))



from config import Config
from models import db, User
from flask_login import LoginManager

def create_app(config_class=Config):
    import os
    basedir = os.path.abspath(os.path.dirname(__file__))
    frontend_build = os.path.join(basedir, '..', 'frontend', 'build')
    
    app = Flask(__name__, 
                static_folder=frontend_build, 
                template_folder=frontend_build)
    
    # Hybrid Template Loading: Support both React build (index.html) and Backend Templates (login.html)
    app.jinja_loader = ChoiceLoader([
        FileSystemLoader(frontend_build),       # Look in React Build first
        FileSystemLoader(os.path.join(basedir, 'templates')) # Look in Backend Templates
    ])

    app.config.from_object(config_class)


    # Enable CORS
    CORS(app)

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
    from blueprints.api.routes import api_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(teacher_bp, url_prefix='/teacher')
    app.register_blueprint(student_bp, url_prefix='/student')
    app.register_blueprint(parent_bp, url_prefix='/parent')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(attendance_bp, url_prefix='/attendance')
    app.register_blueprint(api_bp, url_prefix='/api')
    
    from blueprints.vision import vision_bp
    app.register_blueprint(vision_bp, url_prefix='/api/vision')

    from blueprints.openai import openai_bp
    app.register_blueprint(openai_bp, url_prefix='/api/openai')
    
    from blueprints.ml import ml_bp
    app.register_blueprint(ml_bp, url_prefix='/api/ml')
    
    
    
    
    from blueprints.library.routes import library_bp
    app.register_blueprint(library_bp, url_prefix='/library')
    
    from blueprints.tasks.routes import tasks_bp
    app.register_blueprint(tasks_bp, url_prefix='/tasks')
    
    from blueprints.wellbeing.routes import wellbeing_bp
    app.register_blueprint(wellbeing_bp, url_prefix='/wellbeing')

    # Root Route


    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def catch_all(path):
        if path.startswith("api"):
            abort(404)
        
        # Check if static file exists
        if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
            
        return render_template('index.html')

    @app.route('/ping', methods=['GET'])
    def ping():
        return jsonify({ "status": "Backend connected 🚀" })

    # Create DB Tables (for development convenience)
    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
