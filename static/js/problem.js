let timerInterval = null;
let timeElapsed = 0;

document.addEventListener('DOMContentLoaded', function() {
    startTimer();
    setupProblemHandlers();
});

function startTimer() {
    const timerElement = document.getElementById('timer');
    if (!timerElement) return;
    
    timeElapsed = 0;
    timerInterval = setInterval(() => {
        timeElapsed++;
        const minutes = Math.floor(timeElapsed / 60);
        const seconds = timeElapsed % 60;
        timerElement.textContent = `⏱️ ${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
    }, 1000);
}

function stopTimer() {
    if (timerInterval) {
        clearInterval(timerInterval);
        timerInterval = null;
    }
}

function setupProblemHandlers() {
    // Opciones múltiples
    const optionButtons = document.querySelectorAll('.option-btn');
    optionButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            if (this.disabled) return;
            const answer = this.dataset.answer;
            submitAnswer(answer);
        });
    });
    
    // Input numérico
    const answerInput = document.getElementById('answer-input');
    const submitBtn = document.getElementById('submit-answer');
    
    if (answerInput && submitBtn) {
        answerInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                submitAnswer(this.value);
            }
        });
        
        submitBtn.addEventListener('click', function() {
            submitAnswer(answerInput.value);
        });
    }
    
    // Botón de pista
    const hintBtn = document.getElementById('hint-btn');
    if (hintBtn) {
        hintBtn.addEventListener('click', function() {
            if (usedHint) return;
            usedHint = true;
            showHint();
            this.disabled = true;
            this.style.opacity = '0.5';
        });
    }
    
    // Botón de saltar
    const skipBtn = document.getElementById('skip-btn');
    if (skipBtn) {
        skipBtn.addEventListener('click', function() {
            if (confirm('¿Estás seguro de que quieres saltar este problema?')) {
                window.location.href = '/problem';
            }
        });
    }
    
    // Botón siguiente problema
    const nextBtn = document.getElementById('next-problem');
    if (nextBtn) {
        nextBtn.addEventListener('click', function() {
            window.location.href = '/problem';
        });
    }
}

function submitAnswer(answer) {
    stopTimer();
    
    const timeTaken = timeElapsed;
    const correct = checkAnswer(answer);
    
    // Deshabilitar todos los botones
    document.querySelectorAll('.option-btn, #submit-answer').forEach(btn => {
        btn.disabled = true;
    });
    
    // Marcar respuesta correcta/incorrecta
    if (correct) {
        markCorrectAnswer(answer);
        // Animación de confetti
        if (typeof createConfetti === 'function') {
            createConfetti();
        }
    } else {
        markIncorrectAnswer(answer);
        markCorrectAnswer(solution);
    }
    
    // Enviar resultado al servidor
    fetch('/problem/submit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            correct: correct,
            time_taken: timeTaken,
            used_hint: usedHint,
            difficulty: problemData.difficulty,
            topic: problemData.topic
        })
    })
    .then(response => response.json())
    .then(data => {
        showFeedback(correct, data, timeTaken);
    })
    .catch(error => {
        console.error('Error:', error);
        showFeedback(correct, {}, timeTaken);
    });
}

function checkAnswer(answer) {
    // Normalizar respuestas (eliminar espacios, comparar números)
    const normalizedAnswer = String(answer).trim().toLowerCase();
    const normalizedSolution = String(solution).trim().toLowerCase();
    
    // Comparar como números si ambos son numéricos
    const answerNum = parseFloat(normalizedAnswer);
    const solutionNum = parseFloat(normalizedSolution);
    
    if (!isNaN(answerNum) && !isNaN(solutionNum)) {
        // Comparar con tolerancia para decimales
        return Math.abs(answerNum - solutionNum) < 0.01;
    }
    
    return normalizedAnswer === normalizedSolution;
}

function markCorrectAnswer(answer) {
    const buttons = document.querySelectorAll('.option-btn');
    buttons.forEach(btn => {
        if (btn.dataset.answer === answer || btn.textContent.trim() === answer) {
            btn.classList.add('correct');
        }
    });
}

function markIncorrectAnswer(answer) {
    const buttons = document.querySelectorAll('.option-btn');
    buttons.forEach(btn => {
        if (btn.dataset.answer === answer || btn.textContent.trim() === answer) {
            btn.classList.add('incorrect');
        }
    });
}

function showHint() {
    // Mostrar una pista básica (puede mejorarse)
    alert('💡 Pista: Revisa cuidadosamente los datos del problema y piensa en qué operación necesitas realizar.');
}

function showFeedback(correct, data, timeTaken) {
    const feedback = document.getElementById('feedback');
    const feedbackTitle = document.getElementById('feedback-title');
    const feedbackMessage = document.getElementById('feedback-message');
    const feedbackRewards = document.getElementById('feedback-rewards');
    const feedbackBadges = document.getElementById('feedback-badges');
    
    feedback.style.display = 'flex';
    feedback.classList.add(correct ? 'success' : 'error');
    
    if (correct) {
        feedbackTitle.textContent = '¡Correcto! 🎉';
        feedbackMessage.textContent = problemData.explanation || '¡Bien hecho!';
    } else {
        feedbackTitle.textContent = 'Incorrecto 😔';
        feedbackMessage.textContent = `La respuesta correcta era: ${solution}\n\n${problemData.explanation || ''}`;
    }
    
    // Mostrar recompensas
    if (data.xp_earned) {
        feedbackRewards.innerHTML = `
            <div style="display: flex; justify-content: center; gap: 2rem; flex-wrap: wrap;">
                <div>
                    <strong>+${data.xp_earned} XP</strong>
                    ${data.leveled_up ? '<br><span style="color: var(--success-color);">¡Subiste de nivel!</span>' : ''}
                </div>
                <div>
                    <strong>+${data.coins_earned || 0} 🪙</strong>
                </div>
            </div>
        `;
    }
    
    // Mostrar badges obtenidos
    if (data.badges_earned && data.badges_earned.length > 0) {
        feedbackBadges.innerHTML = '<h4>¡Nuevos Logros!</h4>' +
            data.badges_earned.map(badge => 
                `<span class="badge-notification">${badge.icon} ${badge.name}</span>`
            ).join('');
    }
}

