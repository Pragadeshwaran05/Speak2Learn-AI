document.addEventListener('DOMContentLoaded', () => {
    const startForm = document.getElementById('start-learning-form');
    if (startForm) {
        startForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const topicInput = document.getElementById('topic-input').value.trim();
            const startBtn = document.getElementById('start-btn');
            const errorMsg = document.getElementById('error-message');
            const loadingSpinner = document.getElementById('loading-spinner');

            if (!topicInput) return;

            startBtn.disabled = true;
            errorMsg.classList.add('hidden');
            loadingSpinner.classList.remove('hidden');

            try {
                const response = await fetch('/api/session/create', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ topic: topicInput })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    window.location.href = `/tutor/${data.session_id}`;
                } else {
                    errorMsg.textContent = data.error || 'Failed to start session.';
                    errorMsg.classList.remove('hidden');
                }
            } catch (err) {
                errorMsg.textContent = 'Network error. Please try again.';
                errorMsg.classList.remove('hidden');
            } finally {
                startBtn.disabled = false;
                loadingSpinner.classList.add('hidden');
            }
        });
    }
});
