from models import db
from datetime import datetime
import json

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(50), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    questions = db.relationship('Question', backref='quiz', lazy=True, cascade="all, delete-orphan")
    attempts = db.relationship('QuizAttempt', backref='quiz', lazy=True)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'))
    text = db.Column(db.Text, nullable=False)
    options_json = db.Column(db.Text, nullable=False) # Store as JSON string
    correct_answer = db.Column(db.String(255), nullable=False)
    explanation = db.Column(db.Text)

    @property
    def options(self):
        return json.loads(self.options_json)

    @options.setter
    def options(self, value):
        self.options_json = json.dumps(value)

class QuizAttempt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'))
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    score = db.Column(db.Float)
    total_questions = db.Column(db.Integer)
    feedback = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
