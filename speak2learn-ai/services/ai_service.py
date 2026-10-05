import os
from google import genai
from google.genai import types
import json

def get_client():
    api_key = os.environ.get('AI_API_KEY')
    if not api_key:
        raise ValueError("AI_API_KEY environment variable not set.")
    return genai.Client(api_key=api_key)

def get_model_name():
    return os.environ.get('AI_MODEL') or 'gemini-2.5-flash'

def generate_tutor_response(topic, conversation_history, user_message):
    client = get_client()
    model = get_model_name()
    
    system_instruction = """You are Speak2Learn AI, an adaptive educational tutor.
Your goal is to help the student genuinely understand the topic, not merely provide an answer.
Rules:
1. Explain clearly.
2. Match the student's apparent level.
3. Use examples when useful.
4. Use analogies when the student struggles.
5. Remember the conversation context.
6. Do not repeat an explanation unchanged when the student says they do not understand.
7. Break difficult concepts into smaller pieces.
8. Encourage the student to reason.
9. Ask short checking questions when appropriate.
10. Do not overwhelm the student with unnecessary information."""

    contents = []
    for msg in conversation_history:
        role = 'user' if msg.role == 'user' else 'model'
        contents.append(types.Content(role=role, parts=[types.Part.from_text(text=msg.content)]))
    
    contents.append(types.Content(role='user', parts=[types.Part.from_text(text=user_message)]))
    
    response = client.models.generate_content(
        model=model,
        contents=contents,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.7
        )
    )
    
    return response.text

def generate_evaluation_question(topic, conversation_history):
    client = get_client()
    model = get_model_name()
    
    system_instruction = f"""You are an educational evaluator for the topic: {topic}.
Based on the conversation history, generate ONE conceptual question to test the student's understanding of what was discussed.
Do not make it multiple choice unless necessary. Prefer conceptual questions.
Return ONLY the question text."""

    contents = []
    for msg in conversation_history:
        role = 'user' if msg.role == 'user' else 'model'
        contents.append(types.Content(role=role, parts=[types.Part.from_text(text=msg.content)]))
        
    contents.append(types.Content(role='user', parts=[types.Part.from_text(text="Generate a question to test my understanding now.")]))

    response = client.models.generate_content(
        model=model,
        contents=contents,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.7
        )
    )
    
    return response.text

def evaluate_student_answer(topic, question, student_answer, conversation_history):
    client = get_client()
    model = get_model_name()
    
    system_instruction = """You are an educational evaluator.
1. Analyze the student's actual answer.
2. Determine conceptual correctness.
3. Identify missing concepts.
4. Detect misconceptions.
5. Assign a justified score (0-100).
6. Provide concise feedback.
7. Identify the student's weakest concept.
8. Generate a useful next-question focus.

Return ONLY structured JSON matching this schema:
{
    "score": 82,
    "understanding_level": "good",
    "strengths": ["string"],
    "missing_concepts": ["string"],
    "misconceptions": ["string"],
    "feedback": "string",
    "next_question_focus": "string"
}
"""

    prompt = f"""
Topic: {topic}
Question: {question}
Student Answer: {student_answer}

Evaluate the student's answer.
"""
    
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.2,
            response_mime_type="application/json"
        )
    )
    
    return json.loads(response.text)
