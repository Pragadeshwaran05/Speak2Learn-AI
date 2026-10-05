from datetime import datetime
from . import db

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('learning_session.id'), nullable=False)
    role = db.Column(db.String(50), nullable=False) # 'user' or 'assistant'
    content = db.Column(db.Text, nullable=False)
    input_type = db.Column(db.String(50), nullable=False) # 'text' or 'voice'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
