from datetime import datetime
from . import db

class Resource(db.Model):
    __tablename__ = 'resources'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    subject = db.Column(db.String(100), nullable=False)
    topic = db.Column(db.String(100))
    difficulty = db.Column(db.String(20))  # Beginner, Intermediate, Advanced
    resource_type = db.Column(db.String(20))  # PDF, Video, Note, Quiz
    url = db.Column(db.String(500))  # Link to blob storage or external
    uploaded_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class LearningProgress(db.Model):
    __tablename__ = 'learning_progress'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    resource_id = db.Column(db.Integer, db.ForeignKey('resources.id'), nullable=False)
    status = db.Column(db.String(20), default='started')  # started, completed
    last_accessed = db.Column(db.DateTime, default=datetime.utcnow)
    
class LibraryRecommendation(db.Model):
    __tablename__ = 'library_recommendations'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    resource_id = db.Column(db.Integer, db.ForeignKey('resources.id'), nullable=False)
    reason = db.Column(db.Text)  # AI generated reason
    confidence = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
