from flask import Blueprint, request, jsonify
from models import db
from models.session import LearningSession
from models.message import Message
from models.evaluation import Evaluation
from services.ai_service import generate_evaluation_question, evaluate_student_answer
import json

evaluator_bp = Blueprint('evaluator', __name__)

@evaluator_bp.route('/start', methods=['POST'])
def start_evaluation():
    data = request.json
    session_id = data.get('session_id')
    
    if not session_id:
        return jsonify({'success': False, 'error': 'Missing session_id'}), 400
        
    try:
        learning_session = LearningSession.query.get(session_id)
        if not learning_session:
            return jsonify({'success': False, 'error': 'Session not found'}), 404

        history = Message.query.filter_by(session_id=session_id).order_by(Message.created_at).all()
        
        question = generate_evaluation_question(learning_session.topic, history)
        
        return jsonify({
            'success': True,
            'question': question
        })
    except Exception as e:
        print(f"Error in evaluator/start: {e}")
        return jsonify({'success': False, 'error': 'Could not generate question.'}), 500

@evaluator_bp.route('/answer', methods=['POST'])
def submit_answer():
    data = request.json
    session_id = data.get('session_id')
    question = data.get('question')
    student_answer = data.get('answer')
    
    if not all([session_id, question, student_answer]):
        return jsonify({'success': False, 'error': 'Missing parameters'}), 400
        
    try:
        learning_session = LearningSession.query.get(session_id)
        if not learning_session:
            return jsonify({'success': False, 'error': 'Session not found'}), 404

        history = Message.query.filter_by(session_id=session_id).order_by(Message.created_at).all()
        
        eval_result = evaluate_student_answer(learning_session.topic, question, student_answer, history)
        
        evaluation = Evaluation(
            session_id=session_id,
            question=question,
            student_answer=student_answer,
            score=eval_result.get('score', 0),
            understanding_level=eval_result.get('understanding_level', 'unknown'),
            strengths=json.dumps(eval_result.get('strengths', [])),
            missing_concepts=json.dumps(eval_result.get('missing_concepts', [])),
            misconceptions=json.dumps(eval_result.get('misconceptions', [])),
            feedback=eval_result.get('feedback', ''),
            next_question_focus=eval_result.get('next_question_focus', '')
        )
        db.session.add(evaluation)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'evaluation': eval_result
        })
    except Exception as e:
        print(f"Error in evaluator/answer: {e}")
        db.session.rollback()
        return jsonify({'success': False, 'error': 'Could not evaluate answer.'}), 500

@evaluator_bp.route('/<int:session_id>/history', methods=['GET'])
def get_evaluations(session_id):
    evaluations = Evaluation.query.filter_by(session_id=session_id).order_by(Evaluation.created_at.desc()).all()
    return jsonify({
        'success': True,
        'evaluations': [{
            'id': e.id,
            'question': e.question,
            'score': e.score,
            'feedback': e.feedback,
            'understanding_level': e.understanding_level
        } for e in evaluations]
    })
