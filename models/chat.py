from datetime import datetime
from . import db

class ChatSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(100), default="New Conversation")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    # Relationships
    messages = db.relationship('ChatMessage', backref='session', lazy='dynamic', cascade="all, delete-orphan")
    user = db.relationship('User', backref='chat_sessions')

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'created_at': self.created_at.isoformat(),
            'message_count': self.messages.count()
        }

class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('chat_session.id'), nullable=False)
    role = db.Column(db.String(20), nullable=False) # 'user', 'assistant', 'system'
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Optional: For file uploads
    has_attachment = db.Column(db.Boolean, default=False)
    attachment_url = db.Column(db.String(500), nullable=True) # If we store files in blob storage

    def to_dict(self):
        return {
            'id': self.id,
            'role': self.role,
            'content': self.content,
            'timestamp': self.timestamp.isoformat(),
            'has_attachment': self.has_attachment,
            'attachment_url': self.attachment_url
        }
