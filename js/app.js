// Master Application Controller for C2 English Arcade
(function () {
  'use strict';

  let state = null;
  let activeSession = null;
  let waitingForContinue = false;

  function initApp() {
    state = window.C2Storage.loadState();
    window.C2Engine.updateDailyStreak(state);
    window.C2Storage.saveState(state);

    setupNavigation();
    setupKeyboardListeners();
    setupModal();
    renderAllHub();
  }

  function renderAllHub() {
    window.C2UI.updateHeaderStats(state);
    window.C2UI.renderMasteryOverview(state);
    window.C2UI.renderModeCards(state);
    showView('view-hub');
  }

  function showView(viewId) {
    document.querySelectorAll('.view-panel').forEach(panel => {
      panel.classList.remove('active');
    });
    const target = document.getElementById(viewId);
    if (target) {
      target.classList.add('active');
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  }

  function setupNavigation() {
    // Hub daily session button
    const btnDaily = document.getElementById('btn-start-daily');
    if (btnDaily) {
      btnDaily.addEventListener('click', () => {
        if (state.soundEnabled) window.C2UI.playClickSound();
        startDailySession();
      });
    }

    // Hub review mistakes button
    const btnMistakes = document.getElementById('btn-review-mistakes');
    if (btnMistakes) {
      btnMistakes.addEventListener('click', () => {
        if (state.soundEnabled) window.C2UI.playClickSound();
        startMistakesSession();
      });
    }

    // Exit session button
    const btnExit = document.getElementById('btn-session-exit');
    if (btnExit) {
      btnExit.addEventListener('click', () => {
        if (confirm('Leave current practice session? Current session progress will end.')) {
          activeSession = null;
          waitingForContinue = false;
          renderAllHub();
        }
      });
    }

    // Results back to hub
    const btnResultsHub = document.getElementById('btn-results-hub');
    if (btnResultsHub) {
      btnResultsHub.addEventListener('click', () => {
        if (state.soundEnabled) window.C2UI.playClickSound();
        renderAllHub();
      });
    }

    // Results play again
    const btnResultsAgain = document.getElementById('btn-results-again');
    if (btnResultsAgain) {
      btnResultsAgain.addEventListener('click', () => {
        if (state.soundEnabled) window.C2UI.playClickSound();
        if (activeSession && activeSession.type === 'mode') {
          startModeSession(activeSession.mode);
        } else {
          startDailySession();
        }
      });
    }

    // Logo click returns to hub
    const logo = document.getElementById('nav-logo-btn');
    if (logo) {
      logo.addEventListener('click', () => {
        if (activeSession && !confirm('Return to Hub and end current session?')) return;
        activeSession = null;
        waitingForContinue = false;
        renderAllHub();
      });
    }

    // Sound toggle
    const soundBtn = document.getElementById('btn-toggle-sound');
    if (soundBtn) {
      soundBtn.addEventListener('click', () => {
        state.soundEnabled = !state.soundEnabled;
        soundBtn.textContent = state.soundEnabled ? '🔊' : '🔇';
        window.C2Storage.saveState(state);
      });
    }
  }

  // --- Session Initiation ---

  function startDailySession() {
    const questions = window.C2Engine.buildDailySession(state, 12);
    if (questions.length === 0) {
      alert('No questions available in the question bank.');
      return;
    }
    launchSession({
      type: 'daily',
      title: 'Daily C2 Proficiency Session',
      questions: questions
    });
  }

  function startModeSession(mode) {
    const questions = window.C2Engine.buildModeSession(state, mode, 10);
    if (questions.length === 0) {
      alert('No questions available for this mode.');
      return;
    }
    launchSession({
      type: 'mode',
      mode: mode,
      title: `Practice: ${mode.toUpperCase()}`,
      questions: questions
    });
  }

  function startMistakesSession() {
    const questions = window.C2Engine.buildMistakesSession(state);
    if (questions.length === 0) {
      alert('No pending mistakes to review! Outstanding work.');
      return;
    }
    launchSession({
      type: 'mistakes',
      title: 'Mistake Redemption & SRS Review',
      questions: questions
    });
  }

  function launchSession(sessionData) {
    activeSession = {
      type: sessionData.type,
      mode: sessionData.mode || null,
      title: sessionData.title,
      questions: sessionData.questions,
      currentIndex: 0,
      totalCount: sessionData.questions.length,
      correctCount: 0,
      xpEarned: 0,
      streak: 0,
      results: []
    };
    waitingForContinue = false;
    showView('view-session');
    renderCurrentQuestion();
  }

  // --- Question Rendering & Interaction ---

  function renderCurrentQuestion() {
    if (!activeSession) return;
    waitingForContinue = false;

    const q = activeSession.questions[activeSession.currentIndex];
    const total = activeSession.totalCount;
    const currentNum = activeSession.currentIndex + 1;

    // Update Progress
    const counterEl = document.getElementById('session-counter');
    const fillEl = document.getElementById('session-progress-bar');
    const streakEl = document.getElementById('session-streak-counter');

    if (counterEl) counterEl.textContent = `${currentNum} / ${total}`;
    if (fillEl) fillEl.style.width = `${((currentNum - 1) / total) * 100}%`;
    if (streakEl) streakEl.textContent = `🔥 ${activeSession.streak}`;

    // Meta tags
    const modeTag = document.getElementById('question-mode-tag');
    const levelTag = document.getElementById('question-level-tag');
    const topicTag = document.getElementById('question-topic-tag');

    if (modeTag) modeTag.textContent = q.mode.toUpperCase();
    if (levelTag) levelTag.textContent = `CEFR Level ${q.level}`;
    if (topicTag) topicTag.textContent = q.topic || 'Use of English';

    // Clear previous question bodies
    const container = document.getElementById('question-interactive-body');
    const feedbackWrap = document.getElementById('session-feedback-wrap');
    if (feedbackWrap) feedbackWrap.innerHTML = '';
    if (!container) return;
    container.innerHTML = '';

    if (q.type === 'transformation') {
      renderTransformationQuestion(q, container);
    } else {
      renderChoiceQuestion(q, container);
    }
  }

  function renderChoiceQuestion(q, container) {
    const promptEl = document.createElement('div');
    promptEl.className = 'question-prompt';

    // Highlight gap if present
    const formattedPrompt = q.prompt.replace(/________/g, '<span class="prompt-gap">________</span>');
    promptEl.innerHTML = formattedPrompt;
    container.appendChild(promptEl);

    const optionsGrid = document.createElement('div');
    optionsGrid.className = 'options-grid';

    const keyLabels = ['1', '2', '3', '4'];
    q.options.forEach((opt, idx) => {
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'option-btn';
      btn.dataset.idx = idx;

      btn.innerHTML = `
        <span class="option-key">${keyLabels[idx] || (idx + 1)}</span>
        <span class="option-text">${opt}</span>
      `;

      btn.addEventListener('click', () => {
        handleChoiceSelection(idx);
      });

      optionsGrid.appendChild(btn);
    });

    container.appendChild(optionsGrid);
  }

  function renderTransformationQuestion(q, container) {
    // Lead-in sentence
    const leadInEl = document.createElement('div');
    leadInEl.className = 'transformation-lead-in';
    leadInEl.innerHTML = `<strong>Given:</strong> ${q.leadIn}`;
    container.appendChild(leadInEl);

    // Key Word
    const keyWordWrap = document.createElement('div');
    keyWordWrap.className = 'transformation-keyword-box';
    keyWordWrap.innerHTML = `
      <span>Key Word (do not change):</span>
      <span class="transformation-keyword">${q.keyWord}</span>
    `;
    container.appendChild(keyWordWrap);

    // Sentence Frame
    const inputWrap = document.createElement('div');
    inputWrap.className = 'transformation-input-wrap';

    const frameEl = document.createElement('div');
    frameEl.className = 'transformation-sentence-frame';
    frameEl.innerHTML = `<em>Complete the second sentence:</em><br><strong>${q.gapPrefix}</strong> [ ... ] <strong>${q.gapSuffix}</strong>`;
    inputWrap.appendChild(frameEl);

    const input = document.createElement('input');
    input.type = 'text';
    input.className = 'transformation-input';
    input.id = 'transformation-user-input';
    input.placeholder = `Fill the gap (e.g. including '${q.keyWord}')...`;
    input.autocomplete = 'off';
    inputWrap.appendChild(input);

    const actions = document.createElement('div');
    actions.className = 'transformation-actions';

    const submitBtn = document.createElement('button');
    submitBtn.type = 'button';
    submitBtn.className = 'btn-primary';
    submitBtn.style.padding = '10px 22px';
    submitBtn.textContent = 'Submit Answer (Enter)';
    submitBtn.addEventListener('click', () => {
      handleTransformationSubmission(input.value);
    });

    if (q.hint) {
      const hintBtn = document.createElement('button');
      hintBtn.type = 'button';
      hintBtn.className = 'btn-secondary';
      hintBtn.style.padding = '10px 18px';
      hintBtn.textContent = '💡 Hint';
      hintBtn.addEventListener('click', () => {
        alert('HINT: ' + q.hint);
        input.focus();
      });
      actions.appendChild(hintBtn);
    }

    actions.appendChild(submitBtn);
    inputWrap.appendChild(actions);

    container.appendChild(inputWrap);

    // Focus input automatically
    setTimeout(() => {
      input.focus();
    }, 100);

    input.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        e.preventDefault();
        handleTransformationSubmission(input.value);
      }
    });
  }

  // --- Processing Answers ---

  function handleChoiceSelection(selectedIndex) {
    if (waitingForContinue) return;
    const q = activeSession.questions[activeSession.currentIndex];
    const isCorrect = selectedIndex === q.answer;

    // Disable all option buttons
    const buttons = document.querySelectorAll('.option-btn');
    buttons.forEach((btn, idx) => {
      btn.disabled = true;
      if (idx === q.answer) {
        btn.classList.add(isCorrect ? 'selected-correct' : 'revealed-answer');
      } else if (idx === selectedIndex && !isCorrect) {
        btn.classList.add('selected-wrong');
      }
    });

    processAnswerResult(q, isCorrect);
  }

  function handleTransformationSubmission(userText) {
    if (waitingForContinue) return;
    const q = activeSession.questions[activeSession.currentIndex];
    const isCorrect = window.C2Engine.checkTransformationAnswer(q, userText);

    const input = document.getElementById('transformation-user-input');
    if (input) {
      input.disabled = true;
      input.style.borderColor = isCorrect ? '#10b981' : '#f43f5e';
    }

    processAnswerResult(q, isCorrect);
  }

  function processAnswerResult(q, isCorrect) {
    waitingForContinue = true;

    // Update Session Metrics
    if (isCorrect) {
      activeSession.correctCount++;
      activeSession.streak++;
      if (state.soundEnabled) window.C2UI.playCorrectSound();
    } else {
      activeSession.streak = 0;
      if (state.soundEnabled) window.C2UI.playWrongSound();
    }

    const xpGained = isCorrect ? window.C2Engine.calculateQuestionXp(q, activeSession.streak) : 3;
    activeSession.xpEarned += xpGained;

    // Update Profile and Storage
    state.profile.xp += xpGained;
    state.profile.totalAnswered = (state.profile.totalAnswered || 0) + 1;
    if (isCorrect) state.profile.totalCorrect = (state.profile.totalCorrect || 0) + 1;

    // Update Mode Stats
    if (!state.modeStats[q.mode]) state.modeStats[q.mode] = { correct: 0, total: 0 };
    state.modeStats[q.mode].total++;
    if (isCorrect) state.modeStats[q.mode].correct++;

    // Update Leitner SRS & Adaptive Level
    window.C2SRS.recordResult(state, q.id, isCorrect);
    const adaptiveResult = window.C2Engine.updateAdaptiveLevel(state, q.mode, isCorrect);

    if (adaptiveResult.leveledUp && state.soundEnabled) {
      setTimeout(() => window.C2UI.playLevelUpSound(), 350);
    }

    window.C2Storage.saveState(state);
    window.C2UI.updateHeaderStats(state);

    // Render Explanatory Feedback
    renderFeedbackCard(q, isCorrect, xpGained, adaptiveResult);
  }

  function renderFeedbackCard(q, isCorrect, xpGained, adaptiveResult) {
    const feedbackWrap = document.getElementById('session-feedback-wrap');
    if (!feedbackWrap) return;

    let targetAnswerHtml = '';
    if (q.type === 'transformation') {
      targetAnswerHtml = `
        <div style="margin-bottom: 12px; font-size: 0.95rem; color: #a5b4fc;">
          <strong>Accepted Solutions:</strong> ${q.accepted.map(a => `<code>${q.gapPrefix}<strong>${a}</strong>${q.gapSuffix}</code>`).join(' &bull; ')}
        </div>
      `;
    }

    let adaptiveNote = '';
    if (adaptiveResult.leveledUp) {
      adaptiveNote = `<div style="color: #6ee7b7; font-weight: 700; font-size: 0.85rem; margin-bottom: 8px;">🌟 Adaptive Difficulty Increased! Mode '${q.mode}' is now Level ${adaptiveResult.newLevel}.</div>`;
    }

    feedbackWrap.innerHTML = `
      <div class="feedback-card">
        <div class="feedback-header">
          <div class="feedback-status ${isCorrect ? 'correct' : 'wrong'}">
            <span>${isCorrect ? '✓ Spot on!' : '✕ Not quite'}</span>
          </div>
          <span class="xp-gained-badge">+${xpGained} XP</span>
        </div>

        ${adaptiveNote}
        ${targetAnswerHtml}

        <p class="feedback-explanation">${q.explain}</p>

        <div class="feedback-example-box">
          <div class="feedback-example-label">Natural C2 Context & Collocation</div>
          <div class="feedback-example-text">"${q.example}"</div>
        </div>

        <div class="feedback-actions">
          <button type="button" id="btn-feedback-continue" class="btn-primary" style="padding: 12px 28px;">
            Continue (Enter &rarr;)
          </button>
        </div>
      </div>
    `;

    const continueBtn = document.getElementById('btn-feedback-continue');
    if (continueBtn) {
      continueBtn.addEventListener('click', proceedToNext);
      continueBtn.focus();
    }
  }

  function proceedToNext() {
    if (!activeSession) return;
    activeSession.currentIndex++;

    if (activeSession.currentIndex >= activeSession.totalCount) {
      finishSession();
    } else {
      renderCurrentQuestion();
    }
  }

  // --- Session Completion ---

  function finishSession() {
    state.profile.sessionsCompleted = (state.profile.sessionsCompleted || 0) + 1;
    window.C2Storage.saveState(state);

    const accuracy = Math.round((activeSession.correctCount / activeSession.totalCount) * 100);

    const titleEl = document.getElementById('results-title');
    const accuracyEl = document.getElementById('results-stat-accuracy');
    const xpEl = document.getElementById('results-stat-xp');
    const streakEl = document.getElementById('results-stat-streak');
    const trophyEl = document.getElementById('results-trophy');

    if (titleEl) {
      if (accuracy >= 80) {
        titleEl.textContent = 'Exemplary Mastery!';
        trophyEl.textContent = '🏆';
      } else if (accuracy >= 60) {
        titleEl.textContent = 'Solid Performance!';
        trophyEl.textContent = '🌟';
      } else {
        titleEl.textContent = 'Practice Complete!';
        trophyEl.textContent = '📚';
      }
    }

    if (accuracyEl) accuracyEl.textContent = accuracy + '%';
    if (xpEl) xpEl.textContent = '+' + activeSession.xpEarned;
    if (streakEl) streakEl.textContent = state.profile.streakDays + ' days';

    showView('view-results');

    if (accuracy >= 70) {
      window.C2UI.launchConfetti();
    }
    if (state.soundEnabled) {
      window.C2UI.playLevelUpSound();
    }
  }

  // --- Keyboard Shortcuts ---

  function setupKeyboardListeners() {
    window.addEventListener('keydown', (e) => {
      // Don't intercept shortcuts if typing in text input (unless Enter)
      const isInput = document.activeElement && document.activeElement.tagName === 'INPUT';

      if (e.key === 'Escape') {
        closeModal();
        return;
      }

      if (waitingForContinue) {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          proceedToNext();
        }
        return;
      }

      if (isInput) return; // allow natural typing in transformation input

      // 1, 2, 3, 4 for options
      if (['1', '2', '3', '4'].includes(e.key)) {
        const idx = parseInt(e.key, 10) - 1;
        const btn = document.querySelector(`.option-btn[data-idx="${idx}"]`);
        if (btn && !btn.disabled) {
          e.preventDefault();
          handleChoiceSelection(idx);
        }
      }
    });
  }

  // --- Ranks & Stats Modal ---

  function setupModal() {
    const modal = document.getElementById('stats-modal');
    const openBtn = document.getElementById('btn-open-ranks-modal');
    const closeBtn = document.getElementById('btn-modal-close');
    const resetBtn = document.getElementById('btn-reset-progress');

    if (openBtn) {
      openBtn.addEventListener('click', () => {
        openModal();
      });
    }
    if (closeBtn) {
      closeBtn.addEventListener('click', closeModal);
    }
    if (modal) {
      modal.addEventListener('click', (e) => {
        if (e.target === modal) closeModal();
      });
    }
    if (resetBtn) {
      resetBtn.addEventListener('click', () => {
        if (confirm('Are you sure you want to reset all XP, streaks, and Leitner box mastery? This cannot be undone.')) {
          state = window.C2Storage.resetProgress();
          closeModal();
          renderAllHub();
          alert('Progress has been reset.');
        }
      });
    }
  }

  function openModal() {
    const modal = document.getElementById('stats-modal');
    if (!modal) return;

    // Render Ranks list
    const currentXp = state.profile.xp;
    const currentRank = window.C2Engine.getRank(currentXp);
    const ranksList = document.getElementById('modal-ranks-list');

    if (ranksList) {
      ranksList.innerHTML = '';
      window.C2Engine.RANKS.forEach(r => {
        const isCurrent = r.title === currentRank.title;
        const row = document.createElement('div');
        row.className = `rank-item-row ${isCurrent ? 'current' : ''}`;
        row.innerHTML = `
          <div class="rank-item-left">
            <span class="rank-item-badge">${r.badge}</span>
            <div>
              <div class="rank-item-title">${r.title} ${isCurrent ? '<span style="color:#6366f1;font-size:0.75rem;">(Active)</span>' : ''}</div>
              <div style="font-size:0.75rem; color:#94a3b8;">${r.desc}</div>
            </div>
          </div>
          <div class="rank-item-xp">${r.minXp.toLocaleString()} XP</div>
        `;
        ranksList.appendChild(row);
      });
    }

    // Modal Lifetime Stats
    const totalAns = state.profile.totalAnswered || 0;
    const totalCor = state.profile.totalCorrect || 0;
    const overallAcc = totalAns > 0 ? Math.round((totalCor / totalAns) * 100) : 0;

    const elSessions = document.getElementById('modal-stat-sessions');
    const elAccuracy = document.getElementById('modal-stat-accuracy');
    const elMistakes = document.getElementById('modal-stat-mistakes');

    if (elSessions) elSessions.textContent = state.profile.sessionsCompleted || 0;
    if (elAccuracy) elAccuracy.textContent = `${overallAcc}% (${totalCor}/${totalAns})`;
    if (elMistakes) elMistakes.textContent = (state.mistakesQueue || []).length;

    modal.classList.add('active');
  }

  function closeModal() {
    const modal = document.getElementById('stats-modal');
    if (modal) modal.classList.remove('active');
  }

  window.C2App = {
    init: initApp,
    startDailySession: startDailySession,
    startModeSession: startModeSession,
    startMistakesSession: startMistakesSession
  };

  // Run on DOM Ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initApp);
  } else {
    initApp();
  }
})();
