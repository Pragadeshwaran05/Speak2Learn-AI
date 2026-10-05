document.addEventListener('DOMContentLoaded', () => {
    const chatContainer = document.getElementById('chat-container');
    const chatInput = document.getElementById('chat-input');
    const sendBtn = document.getElementById('send-btn');
    const micBtn = document.getElementById('mic-btn');
    const statusText = document.getElementById('status-text');
    const testUnderstandingBtn = document.getElementById('test-understanding-btn');

    let isListening = false;
    let recognition = null;

    if ('SpeechRecognition' in window || 'webkitSpeechRecognition' in window) {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = 'en-US';

        recognition.onstart = () => {
            isListening = true;
            micBtn.classList.add('listening');
            statusText.textContent = '🎤 Listening...';
        };

        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            sendMessage(transcript, 'voice');
        };

        recognition.onerror = (event) => {
            console.error('Speech recognition error', event.error);
            if (event.error === 'not-allowed') {
                statusText.textContent = 'Microphone access was denied. Please allow microphone permission and try again.';
            } else {
                statusText.textContent = 'We couldn\'t understand the audio. Please try speaking again.';
            }
            micBtn.classList.remove('listening');
            isListening = false;
        };

        recognition.onend = () => {
            micBtn.classList.remove('listening');
            isListening = false;
            if (statusText.textContent === '🎤 Listening...') {
                statusText.textContent = '';
            }
        };
    } else {
        micBtn.disabled = true;
        micBtn.title = 'Voice input is not supported by this browser. Please use a supported browser or type your question.';
    }

    micBtn.addEventListener('click', () => {
        if (!recognition) {
            statusText.textContent = 'Voice input is not supported by this browser. Please use a supported browser or type your question.';
            return;
        }
        if (isListening) {
            recognition.stop();
        } else {
            recognition.start();
        }
    });

    sendBtn.addEventListener('click', () => {
        const text = chatInput.value.trim();
        if (text) sendMessage(text, 'text');
    });

    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            const text = chatInput.value.trim();
            if (text) sendMessage(text, 'text');
        }
    });

    testUnderstandingBtn.addEventListener('click', () => {
        window.location.href = `/evaluate/${SESSION_ID}`;
    });

    async function sendMessage(message, inputType) {
        chatInput.value = '';
        statusText.textContent = '🧠 Thinking...';
        sendBtn.disabled = true;
        
        appendMessage('user', message, inputType);

        try {
            const response = await fetch('/api/tutor/message', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    session_id: SESSION_ID,
                    message: message,
                    input_type: inputType
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                appendMessage('assistant', data.response, 'text');
                statusText.textContent = '';
            } else {
                statusText.textContent = data.error || 'The AI tutor is temporarily unavailable. Please try again.';
            }
        } catch (err) {
            statusText.textContent = 'Network error. Please try again.';
        } finally {
            sendBtn.disabled = false;
        }
    }

    function appendMessage(role, content, inputType) {
        const div = document.createElement('div');
        div.className = `message ${role}`;
        
        let html = `<div class="msg-content">${content.replace(/\\n/g, '<br>')}</div>`;
        
        if (role === 'user') {
            html = `<div class="msg-type-icon">${inputType === 'voice' ? '🎤' : '⌨️'}</div>` + html;
        } else {
            html += `<div class="msg-actions"><button class="listen-btn" data-text="${escapeHtml(content)}">🔊 Listen</button></div>`;
        }
        
        div.innerHTML = html;
        chatContainer.appendChild(div);
        chatContainer.scrollTop = chatContainer.scrollHeight;
        
        if (role === 'assistant') {
            const listenBtn = div.querySelector('.listen-btn');
            listenBtn.addEventListener('click', () => speakText(content));
        }
    }

    function escapeHtml(text) {
        return text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#039;");
    }

    let currentUtterance = null;
    function speakText(text) {
        if (!('speechSynthesis' in window)) {
            alert('Text-to-speech is not supported in your browser.');
            return;
        }
        
        window.speechSynthesis.cancel();
        
        currentUtterance = new SpeechSynthesisUtterance(text);
        window.speechSynthesis.speak(currentUtterance);
    }
    
    document.querySelectorAll('.listen-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            speakText(e.target.getAttribute('data-text'));
        });
    });
});
