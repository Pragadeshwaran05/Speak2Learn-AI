document.addEventListener('DOMContentLoaded', () => {
    const questionText = document.getElementById('question-text');
    const answerSection = document.getElementById('answer-section');
    const answerInput = document.getElementById('answer-input');
    const submitBtn = document.getElementById('submit-answer-btn');
    const statusText = document.getElementById('status-text');
    const micBtn = document.getElementById('mic-btn');
    const resultSection = document.getElementById('result-section');
    const backBtn = document.getElementById('back-to-tutor-btn');
    const nextQuestionBtn = document.getElementById('next-question-btn');
    const listenQuestionBtn = document.getElementById('listen-question-btn');
    const listenFeedbackBtn = document.getElementById('listen-feedback-btn');

    let currentQuestion = '';

    startEvaluation();

    async function startEvaluation() {
        try {
            const response = await fetch('/api/evaluator/start', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ session_id: SESSION_ID })
            });
            const data = await response.json();
            
            if (data.success) {
                currentQuestion = data.question;
                questionText.textContent = currentQuestion;
                answerSection.classList.remove('hidden');
                listenQuestionBtn.classList.remove('hidden');
            } else {
                questionText.textContent = data.error || 'Failed to generate question.';
            }
        } catch (err) {
            questionText.textContent = 'Network error. Please try again.';
        }
    }

    let isListening = false;
    let recognition = null;

    if ('SpeechRecognition' in window || 'webkitSpeechRecognition' in window) {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        recognition = new SpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = true;
        recognition.lang = 'en-US';

        recognition.onstart = () => {
            isListening = true;
            micBtn.classList.add('listening');
            answerInput.placeholder = 'Listening...';
        };

        recognition.onresult = (event) => {
            let finalTranscript = '';
            let interimTranscript = '';
            for (let i = event.resultIndex; i < event.results.length; ++i) {
                if (event.results[i].isFinal) {
                    finalTranscript += event.results[i][0].transcript;
                } else {
                    interimTranscript += event.results[i][0].transcript;
                }
            }
            if (finalTranscript) {
                answerInput.value += (answerInput.value ? ' ' : '') + finalTranscript;
            }
        };

        recognition.onerror = (event) => {
            console.error(event);
            isListening = false;
            micBtn.classList.remove('listening');
            answerInput.placeholder = 'Type your answer here...';
        };

        recognition.onend = () => {
            isListening = false;
            micBtn.classList.remove('listening');
            answerInput.placeholder = 'Type your answer here...';
        };
    }

    micBtn.addEventListener('click', () => {
        if (!recognition) return;
        if (isListening) {
            recognition.stop();
        } else {
            recognition.start();
        }
    });

    submitBtn.addEventListener('click', async () => {
        const answer = answerInput.value.trim();
        if (!answer) return;

        if (isListening) recognition.stop();
        
        submitBtn.disabled = true;
        statusText.textContent = '🔍 Evaluating your answer...';
        
        try {
            const response = await fetch('/api/evaluator/answer', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    session_id: SESSION_ID,
                    question: currentQuestion,
                    answer: answer
                })
            });
            const data = await response.json();
            
            if (data.success) {
                displayResult(data.evaluation);
            } else {
                statusText.textContent = data.error || 'Evaluation failed.';
                submitBtn.disabled = false;
            }
        } catch (err) {
            statusText.textContent = 'Network error. Please try again.';
            submitBtn.disabled = false;
        }
    });

    function displayResult(eval) {
        answerSection.classList.add('hidden');
        resultSection.classList.remove('hidden');
        
        const scoreDisplay = document.getElementById('score-display');
        scoreDisplay.textContent = `${eval.score}%`;
        
        const understandingLevel = document.getElementById('understanding-level');
        understandingLevel.textContent = `Understanding: ${eval.understanding_level}`;
        
        const strengthsList = document.getElementById('strengths-list');
        strengthsList.innerHTML = eval.strengths.map(s => `<li>✓ ${s}</li>`).join('');
        
        const weaknessesList = document.getElementById('weaknesses-list');
        const weaknesses = [...(eval.missing_concepts || []), ...(eval.misconceptions || [])];
        weaknessesList.innerHTML = weaknesses.length ? weaknesses.map(w => `<li>• ${w}</li>`).join('') : '<li>None</li>';
        
        document.getElementById('feedback-text').textContent = eval.feedback;
    }

    nextQuestionBtn.addEventListener('click', () => {
        resultSection.classList.add('hidden');
        answerInput.value = '';
        submitBtn.disabled = false;
        statusText.textContent = '';
        questionText.textContent = 'Generating next question... 🎯';
        listenQuestionBtn.classList.add('hidden');
        startEvaluation();
    });

    backBtn.addEventListener('click', () => {
        window.location.href = `/tutor/${SESSION_ID}`;
    });

    function speakText(text) {
        if (!('speechSynthesis' in window)) return;
        window.speechSynthesis.cancel();
        const utterance = new SpeechSynthesisUtterance(text);
        window.speechSynthesis.speak(utterance);
    }
    
    listenQuestionBtn.addEventListener('click', () => speakText(currentQuestion));
    listenFeedbackBtn.addEventListener('click', () => {
        speakText(document.getElementById('feedback-text').textContent);
    });
});
