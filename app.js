const task = document.getElementById('task');
const input = document.getElementById('inputText');
const level = document.getElementById('level');
const levelLabel = document.getElementById('level-label');
const submit = document.getElementById('submitBtn');
const clear = document.getElementById('clearBtn');
const resultCard = document.getElementById('resultCard');
const result = document.getElementById('result');
const copy = document.getElementById('copyBtn');

function updateUI() {
  const learning = task.value === 'learn';
  level.classList.toggle('hidden', !learning);
  levelLabel.classList.toggle('hidden', !learning);
  input.placeholder = learning ? 'Enter a topic, e.g. SQL' :
    task.value === 'quiz' ? 'Paste a passage or enter a topic for quiz questions...' :
    'Type your question, topic, or passage here...';
}

task.addEventListener('change', updateUI);
clear.addEventListener('click', () => { input.value = ''; resultCard.classList.add('hidden'); result.innerHTML = ''; });
copy.addEventListener('click', async () => {
  await navigator.clipboard.writeText(result.innerText);
  copy.textContent = 'Copied';
  setTimeout(() => copy.textContent = 'Copy', 1200);
});

function renderQuiz(questions) {
  return questions.map((q, i) => `
    <article class="quiz-question">
      <h3>${i + 1}. ${escapeHtml(q.question)}</h3>
      ${q.options.map((o, j) => `<div class="option">${String.fromCharCode(65+j)}. ${escapeHtml(o)}</div>`).join('')}
      <div class="answer"><strong>Answer:</strong> ${escapeHtml(q.answer)}<br><strong>Why:</strong> ${escapeHtml(q.explanation)}</div>
    </article>`).join('');
}

function escapeHtml(value) {
  return String(value).replace(/[&<>'"]/g, ch => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[ch]));
}

submit.addEventListener('click', async () => {
  const text = input.value.trim();
  if (!text) { resultCard.classList.remove('hidden'); result.innerHTML = '<div class="error">Please enter something first.</div>'; return; }

  submit.disabled = true;
  submit.textContent = 'Generating...';
  resultCard.classList.remove('hidden');
  result.textContent = 'EduGenie is thinking...';

  const routes = {
    qa: '/qa', explain: '/explain', quiz: '/quiz', summarize: '/summarize', learn: '/learn/recommendations'
  };
  const body = task.value === 'quiz' ? { text, count: 3 } :
               task.value === 'learn' ? { topic: text, level: level.value } : { text };
  try {
    const response = await fetch(routes[task.value], { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify(body) });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || 'Request failed');
    result.innerHTML = task.value === 'quiz' ? renderQuiz(data.quiz) : escapeHtml(data.answer || data.summary || data.recommendations);
  } catch (err) {
    result.innerHTML = `<div class="error">${escapeHtml(err.message)}</div>`;
  } finally {
    submit.disabled = false;
    submit.textContent = 'Generate';
  }
});

updateUI();
