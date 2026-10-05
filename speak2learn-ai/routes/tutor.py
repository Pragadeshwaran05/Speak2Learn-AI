from flask import Blueprint, request, jsonify
from models import db
from models.session import LearningSession
from models.message import Message
from services.ai_service import generate_tutor_response

tutor_bp = Blueprint('tutor', __name__)

@tutor_bp.route('/message', methods=['POST'])
def handle_message():
    data = request.json
    session_id = data.get('session_id')
    content = data.get('message')
    input_type = data.get('input_type', 'text')
    
    if not all([session_id, content]):
        return jsonify({'success': False, 'error': 'Missing session_id or message'}), 400
        
    try:
        learning_session = LearningSession.query.get(session_id)
        if not learning_session:
            return jsonify({'success': False, 'error': 'Session not found'}), 404

        # Save user message
        user_msg = Message(session_id=session_id, role='user', content=content, input_type=input_type)
        db.session.add(user_msg)
        
        # Get history (excluding the message we just added so it's not duplicated in contents)
        history = Message.query.filter(Message.session_id==session_id, Message.id != user_msg.id).order_by(Message.created_at).all()
        
        # Call AI
        ai_response_text = generate_tutor_response(learning_session.topic, history, content)
        
        # Save AI message
        ai_msg = Message(session_id=session_id, role='assistant', content=ai_response_text, input_type='text')
        db.session.add(ai_msg)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'response': ai_response_text,
            'input_type': input_type
        })
    except Exception as e:
        print(f"Error in tutor/message: {e}")
        db.session.rollback()
        return jsonify({'success': False, 'error': 'The AI tutor is temporarily unavailable. Please try again.'}), 500
