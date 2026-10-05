import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-123'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///speak2learn.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    AI_API_KEY = os.environ.get('AI_API_KEY')
    AI_MODEL = os.environ.get('AI_MODEL') or 'gemini-2.5-flash'
