from flask import Blueprint, render_template, request, jsonify
from models import db
from models.session import LearningSession
from models.message import Message

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/tutor/<int:session_id>')
def tutor(session_id):
    learning_session = LearningSession.query.get_or_404(session_id)
    return render_template('tutor.html', session_id=session_id, topic=learning_session.topic)

@main_bp.route('/evaluate/<int:session_id>')
def evaluate(session_id):
    learning_session = LearningSession.query.get_or_404(session_id)
    return render_template('evaluation.html', session_id=session_id, topic=learning_session.topic)

@main_bp.route('/api/session/create', methods=['POST'])
def create_session():
    data = request.json
    topic = data.get('topic')
    if not topic:
        return jsonify({'success': False, 'error': 'Topic is required'}), 400
    
    new_session = LearningSession(topic=topic)
    db.session.add(new_session)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'session_id': new_session.id
    })

@main_bp.route('/api/session/<int:session_id>')
def get_session(session_id):
    learning_session = LearningSession.query.get_or_404(session_id)
    messages = Message.query.filter_by(session_id=session_id).order_by(Message.created_at).all()
    
    return jsonify({
        'success': True,
        'topic': learning_session.topic,
        'messages': [{
            'id': m.id,
            'role': m.role,
            'content': m.content,
            'input_type': m.input_type
        } for m in messages]
    })
