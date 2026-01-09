from . import db
from datetime import datetime

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow().date)
    status = db.Column(db.String(20), nullable=False) # Present, Absent, Late, Excused
    method = db.Column(db.String(50), nullable=False) # Manual, QR, Self-Check
    remarks = db.Column(db.String(200))
    
    student = db.relationship('User', backref='attendance_records')

    def __repr__(self):
        return f'<Attendance {self.student.username} - {self.date}: {self.status}>'
