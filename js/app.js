// js/app.js
// Master Application Controller for C2 English Arcade (ELO Edition)
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
        if (confirm('Leave current practice session? Current round will end.')) {
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
      title: 'Daily C2 Proficiency Challenge',
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
      streak: 0,
      sessionStartGlobalElo: window.C2ELO.globalRating(state),
      results: [],
      lastCalculation: null,
      lastHistoryEntry: null
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

    const qRating = window.C2ELO.questionRating(q);

    if (modeTag) modeTag.textContent = q.mode.toUpperCase();
    if (levelTag) levelTag.textContent = `${qRating} ELO (L${q.level})`;
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

    // Create randomized display permutation of option indices
    const indices = q.options.map((_, i) => i);
    for (let i = indices.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      const temp = indices[i];
      indices[i] = indices[j];
      indices[j] = temp;
    }
    activeSession.currentDisplayMapping = indices;

    const keyLabels = ['1', '2', '3', '4'];
    indices.forEach((origIdx, dispIdx) => {
      const opt = q.options[origIdx];
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'option-btn';
      btn.dataset.dispIdx = dispIdx;
      btn.dataset.origIdx = origIdx;

      btn.innerHTML = `
        <span class="option-key">${keyLabels[dispIdx]}</span>
        <span class="option-text">${opt}</span>
      `;

      btn.addEventListener('click', () => {
        handleChoiceSelection(dispIdx);
      });

      optionsGrid.appendChild(btn);
    });

    container.appendChild(optionsGrid);
  }

  function renderTransformationQuestion(q, container) {
    // 1. Lead-in sentence
    const leadInEl = document.createElement('div');
    leadInEl.className = 'transformation-lead-in';
    leadInEl.textContent = q.leadIn;
    container.appendChild(leadInEl);

    // 2. Key Word Card
    const kwCard = document.createElement('div');
    kwCard.className = 'transformation-keyword-card';
    kwCard.innerHTML = `
      <div class="keyword-label">KEY WORD (DO NOT CHANGE FORM)</div>
      <div class="keyword-text">${q.keyWord}</div>
    `;
    container.appendChild(kwCard);

    // 3. Transformation Sentence with Gap
    const gapSentence = document.createElement('div');
    gapSentence.className = 'transformation-gap-sentence';
    gapSentence.innerHTML = `
      <span>${q.gapPrefix || ''}</span>
      <span class="prompt-gap" style="margin: 0 4px;">[ 3 to 8 words ]</span>
      <span>${q.gapSuffix || ''}</span>
    `;
    container.appendChild(gapSentence);

    // 4. User Input Box
    const inputWrap = document.createElement('div');
    inputWrap.className = 'transformation-input-wrap';

    const input = document.createElement('input');
    input.type = 'text';
    input.id = 'transformation-user-input';
    input.className = 'transformation-input';
    input.placeholder = `Type the missing words (including '${q.keyWord}')...`;
    input.autocomplete = 'off';
    input.autocorrect = 'off';
    input.autocapitalize = 'off';
    input.spellcheck = false;

    inputWrap.appendChild(input);

    const actions = document.createElement('div');
    actions.style.display = 'flex';
    actions.style.gap = '10px';
    actions.style.marginTop = '12px';
    actions.style.justifyContent = 'flex-end';

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

  function handleChoiceSelection(displayedIndex) {
    if (waitingForContinue) return;
    const q = activeSession.questions[activeSession.currentIndex];
    const mapping = activeSession.currentDisplayMapping || [0, 1, 2, 3];
    const origIndex = mapping[displayedIndex];
    const isCorrect = origIndex === q.answer;

    // Disable all option buttons and apply correct/wrong styling
    const buttons = document.querySelectorAll('.option-btn');
    buttons.forEach((btn, dIdx) => {
      btn.disabled = true;
      const bOrig = mapping[dIdx];
      if (bOrig === q.answer) {
        btn.classList.add(isCorrect ? 'selected-correct' : 'revealed-answer');
      } else if (dIdx === displayedIndex && !isCorrect) {
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

    processAnswerResult(q, isCorrect, userText);
  }

  function processAnswerResult(q, isCorrect, userText = '') {
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

    // Apply ELO calculation & rating update
    const calc = window.C2ELO.applyAnswer(state, q, isCorrect);
    activeSession.lastCalculation = calc;
    activeSession.lastHistoryEntry = calc.historyEntry;

    // Profile counters
    state.profile.totalAnswered = (state.profile.totalAnswered || 0) + 1;
    if (isCorrect) {
      state.profile.totalCorrect = (state.profile.totalCorrect || 0) + 1;
    }

    // Manage Leitner SRS & Mistakes Queue
    window.C2SRS.recordResult(state, q.id, isCorrect);
    if (!isCorrect) {
      if (!state.mistakesQueue.includes(q.id)) {
        state.mistakesQueue.push(q.id);
      }
    } else {
      const mIdx = state.mistakesQueue.indexOf(q.id);
      if (mIdx !== -1) {
        state.mistakesQueue.splice(mIdx, 1);
      }
    }

    // Save state
    window.C2Storage.saveState(state);

    // Update visual feedback
    window.C2UI.showEloDeltaBadge(calc.delta);
    window.C2UI.updateHeaderStats(state);

    if (calc.promoted) {
      window.C2UI.launchConfetti();
      if (state.soundEnabled) {
        setTimeout(() => window.C2UI.playLevelUpSound(), 300);
      }
    }

    // Render Explanatory Feedback
    renderFeedbackCard(q, isCorrect, calc);
  }

  function renderFeedbackCard(q, isCorrect, calc) {
    const feedbackWrap = document.getElementById('session-feedback-wrap');
    if (!feedbackWrap) return;

    let targetAnswerHtml = '';
    if (q.type === 'transformation') {
      targetAnswerHtml = `
        <div style="margin-bottom: 12px; font-size: 0.95rem; color: #a5b4fc;">
          <strong>Accepted Solutions:</strong> ${q.accepted.map(a => `<code>${q.gapPrefix || ''}<strong>${a}</strong>${q.gapSuffix || ''}</code>`).join(' &bull; ')}
        </div>
      `;
    }

    let promotionNotice = '';
    if (calc.promoted) {
      promotionNotice = `
        <div style="color: #6ee7b7; font-weight: 800; font-size: 0.95rem; margin-bottom: 10px; background: rgba(16, 185, 129, 0.15); padding: 8px 12px; border-radius: 8px; border: 1px solid rgba(16, 185, 129, 0.4);">
          🎉 RANK UP: You are now <strong>${calc.rankInfo.rank.badge} ${calc.rankInfo.rank.title}</strong>!
        </div>
      `;
    }

    const deltaSign = calc.delta >= 0 ? '+' : '';
    const badgeClass = calc.delta >= 0 ? 'gain' : 'loss';

    let overrideButtonHtml = '';
    if (q.type === 'transformation' && !isCorrect) {
      overrideButtonHtml = `
        <div>
          <button type="button" class="btn-override-correct" id="btn-override-kwt">
            ✓ My phrasing was also valid (Mark as Correct & Adjust ELO)
          </button>
        </div>
      `;
    }

    feedbackWrap.innerHTML = `
      <div class="feedback-card">
        <div class="feedback-header">
          <div class="feedback-status ${isCorrect ? 'correct' : 'wrong'}">
            <span>${isCorrect ? '✓ Spot on!' : '✕ Not quite'}</span>
          </div>
          <span class="elo-gained-badge ${badgeClass}">${deltaSign}${calc.delta} ELO</span>
        </div>

        ${promotionNotice}

        <!-- ELO Probability & Rating Metadata -->
        <div class="elo-meta-details">
          <div class="elo-meta-item"><span>Win Probability:</span> <strong>${Math.round(calc.expected * 100)}%</strong></div>
          <div class="elo-meta-item"><span>Question:</span> <strong>${calc.qRating} ELO</strong></div>
          <div class="elo-meta-item"><span>Skill ELO:</span> <strong>${calc.newRating}</strong></div>
          <div class="elo-meta-item"><span>Variety:</span> <strong>×${calc.variety.multiplier.toFixed(2)}</strong></div>
        </div>

        ${targetAnswerHtml}
        ${overrideButtonHtml}

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

    // Hook override button if present
    const overrideBtn = document.getElementById('btn-override-kwt');
    if (overrideBtn) {
      overrideBtn.addEventListener('click', () => {
        if (!activeSession || !activeSession.lastHistoryEntry) return;

        const overrideCalc = window.C2ELO.undoLastAnswer(state, activeSession.lastHistoryEntry, true);
        if (overrideCalc) {
          activeSession.correctCount++;
          // remove from mistakes queue if there
          const mIdx = state.mistakesQueue.indexOf(q.id);
          if (mIdx !== -1) {
            state.mistakesQueue.splice(mIdx, 1);
          }
          window.C2SRS.recordResult(state, q.id, true);
          window.C2Storage.saveState(state);

          window.C2UI.showEloDeltaBadge(overrideCalc.delta);
          window.C2UI.updateHeaderStats(state);

          overrideBtn.disabled = true;
          overrideBtn.textContent = `✓ Overridden as Correct (+${overrideCalc.delta} ELO applied)`;
          overrideBtn.style.color = '#34d399';
          overrideBtn.style.borderColor = '#10b981';

          // Update badge in feedback card
          const badge = feedbackWrap.querySelector('.elo-gained-badge');
          if (badge) {
            badge.className = 'elo-gained-badge gain';
            badge.textContent = `+${overrideCalc.delta} ELO`;
          }

          if (state.soundEnabled) window.C2UI.playCorrectSound();
        }
      });
    }

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
    const endGlobalElo = window.C2ELO.globalRating(state);
    const sessionEloDelta = endGlobalElo - activeSession.sessionStartGlobalElo;

    const titleEl = document.getElementById('results-title');
    const accuracyEl = document.getElementById('results-stat-accuracy');
    const eloEl = document.getElementById('results-stat-elo');
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

    if (accuracyEl) accuracyEl.textContent = `${accuracy}%`;
    if (eloEl) {
      const sign = sessionEloDelta >= 0 ? '+' : '';
      eloEl.textContent = `${sign}${sessionEloDelta} (${endGlobalElo})`;
    }
    if (streakEl) streakEl.textContent = `${state.profile.streakDays} days`;

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
        const dIdx = parseInt(e.key, 10) - 1;
        const btn = document.querySelector(`.option-btn[data-disp-idx="${dIdx}"]`);
        if (btn && !btn.disabled) {
          e.preventDefault();
          handleChoiceSelection(dIdx);
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
        if (confirm('Are you sure you want to reset all ELO ratings, history, and Leitner box mastery? This cannot be undone.')) {
          state = window.C2Storage.resetProgress();
          closeModal();
          renderAllHub();
          alert('Progress and ratings have been reset to default.');
        }
      });
    }

    // Export progress JSON
    const exportBtn = document.getElementById('btn-export-progress');
    if (exportBtn) {
      exportBtn.addEventListener('click', () => {
        window.C2Storage.exportState(state);
      });
    }

    // Import progress JSON
    const importBtn = document.getElementById('btn-import-progress');
    const fileInput = document.getElementById('import-file-input');
    if (importBtn && fileInput) {
      importBtn.addEventListener('click', () => {
        fileInput.value = '';
        fileInput.click();
      });

      fileInput.addEventListener('change', (e) => {
        const file = e.target.files && e.target.files[0];
        if (!file) return;

        const reader = new FileReader();
        reader.onload = (event) => {
          const result = window.C2Storage.validateAndImport(event.target.result);
          if (result.success) {
            state = result.state;
            renderAllHub();
            closeModal();
            const globalElo = window.C2ELO.globalRating(state);
            alert(`Progress restored successfully! Current Global ELO: ${globalElo}`);
          } else {
            alert('Failed to import progress file: ' + result.error);
          }
        };
        reader.readAsText(file);
      });
    }
  }

  function openModal() {
    const modal = document.getElementById('stats-modal');
    if (!modal) return;

    window.C2UI.renderRanksModal(state);
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
