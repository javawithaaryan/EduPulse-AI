from . import db
from datetime import datetime

class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    rubric = db.Column(db.Text, nullable=False) # Storing rubric as text for simplicity
    max_marks = db.Column(db.Integer, nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime)

    teacher = db.relationship('User', backref='assignments')
    submissions = db.relationship('Submission', backref='assignment', lazy='dynamic')

    def __repr__(self):
        return f'<Assignment {self.title}>'
