from datetime import datetime
from . import db
import json

class Evaluation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('learning_session.id'), nullable=False)
    question = db.Column(db.Text, nullable=False)
    student_answer = db.Column(db.Text, nullable=False)
    score = db.Column(db.Integer, nullable=False)
    understanding_level = db.Column(db.String(50), nullable=False)
    strengths = db.Column(db.Text, nullable=False) # JSON string
    missing_concepts = db.Column(db.Text, nullable=False) # JSON string
    misconceptions = db.Column(db.Text, nullable=False) # JSON string
    feedback = db.Column(db.Text, nullable=False)
    next_question_focus = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def strengths_list(self):
        return json.loads(self.strengths) if self.strengths else []

    @property
    def missing_concepts_list(self):
        return json.loads(self.missing_concepts) if self.missing_concepts else []
        
    @property
    def misconceptions_list(self):
        return json.loads(self.misconceptions) if self.misconceptions else []
