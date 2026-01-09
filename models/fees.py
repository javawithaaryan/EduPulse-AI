from . import db
from datetime import datetime

class Fee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default='Unpaid') # Unpaid, Paid, Partially Paid
    category = db.Column(db.String(50)) # Tuition, Transport, Lab, etc.
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    student = db.relationship('User', backref=db.backref('fees', lazy=True))

class PaymentTransaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    fee_ids = db.Column(db.String(200)) # Stored as comma-separated IDs
    transaction_ref = db.Column(db.String(100), unique=True)
    amount_paid = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    method = db.Column(db.String(50)) # UPI, Card, Netbanking, Cash
    status = db.Column(db.String(20), default='Success')

    parent = db.relationship('User', backref=db.backref('payments', lazy=True))
