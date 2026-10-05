import os
from flask import Flask
from models import db
from config import Config
from routes.main import main_bp
from routes.tutor import tutor_bp
from routes.evaluator import evaluator_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)

    # Ensure instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(tutor_bp, url_prefix='/api/tutor')
    app.register_blueprint(evaluator_bp, url_prefix='/api/evaluator')

    # Create database tables
    with app.app_context():
        db.create_all()

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
