from . import db

class Performance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    subject = db.Column(db.String(50), nullable=False)
    risk_score = db.Column(db.Float, default=0.0) # 0.0 to 1.0 (Higher is simpler risk)
    risk_level = db.Column(db.String(20), default='low') # low, medium, high
    trend = db.Column(db.String(20)) # improving, declining, stable
    last_updated = db.Column(db.DateTime, default=db.func.now())
    
    student = db.relationship('User', backref='performance_records')
