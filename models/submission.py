from . import db
from datetime import datetime

class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignment.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    file_url = db.Column(db.String(500), nullable=False) # Azure Blob URL
    extracted_text = db.Column(db.Text) # OCR Result
    status = db.Column(db.String(20), default='pending') # pending, graded
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    ai_result = db.relationship('AIResult', backref='submission', uselist=False)

    def __repr__(self):
        return f'<Submission {self.id}>'
