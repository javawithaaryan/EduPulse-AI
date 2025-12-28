from datetime import datetime
from . import db

class EmotionalCheckin(db.Model):
    __tablename__ = 'emotional_checkins'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, default=datetime.utcnow)
    mood_level = db.Column(db.Integer)  # 1-5 (1=struggling, 5=excellent)
    stress_level = db.Column(db.Integer)  # 1-5 (1=calm, 5=very stressed)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class SupportLog(db.Model):
    __tablename__ = 'support_logs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    trigger_type = db.Column(db.String(50))  # low_mood, high_stress, etc
    ai_response = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
