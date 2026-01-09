from . import db
import json

class AIResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    submission_id = db.Column(db.Integer, db.ForeignKey('submission.id'), nullable=False)
    score = db.Column(db.Float, nullable=False)
    feedback_json = db.Column(db.Text, nullable=False) # Complete JSON response
    # Helper fields for easy query (optional, but good for MVP analytics)
    strengths = db.Column(db.Text) 
    improvements = db.Column(db.Text)

    def get_feedback_dict(self):
        try:
            return json.loads(self.feedback_json)
        except:
            return {}
