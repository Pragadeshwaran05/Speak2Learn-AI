from datetime import datetime
from . import db

class LearningSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(200), nullable=False)
    difficulty = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    messages = db.relationship('Message', backref='session', lazy=True, cascade="all, delete-orphan")
    evaluations = db.relationship('Evaluation', backref='session', lazy=True, cascade="all, delete-orphan")
