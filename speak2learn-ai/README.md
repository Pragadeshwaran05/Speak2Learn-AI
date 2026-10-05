# Speak2Learn AI

"Learn by Speaking. Understand by Doing."

## Overview
Speak2Learn AI is an adaptive educational web application. It features a Voice AI Tutor that adjusts to the student's level and an AI Evaluator that tests their conceptual understanding.

## Core Features
1. **Adaptive AI Voice Tutor:** A voice-enabled conversational AI that adapts explanations based on student interactions.
2. **AI Learning Evaluator:** Dynamically generates conceptual questions, evaluates spoken or written answers, identifies knowledge gaps, and provides targeted feedback.

## Setup Instructions

### Prerequisites
- Python 3.8+
- Browser with Web Speech API support (Google Chrome recommended)

### Installation
1. Clone the repository or navigate to the project directory:
   ```bash
   cd speak2learn-ai
   ```
2. Create and activate a virtual environment (Windows):
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables:
   Copy `.env.example` to `.env` and fill in your AI API key (Gemini).
   ```bash
   AI_API_KEY=your-api-key
   AI_MODEL=gemini-2.5-flash
   ```

### Running the Application
```bash
python app.py
```
Then visit `http://127.0.0.1:5000` in your web browser.

### Troubleshooting
- **Microphone not working:** Ensure you have granted microphone permissions in your browser.
- **AI response errors:** Check your `AI_API_KEY` in `.env` and make sure you have internet connectivity.
