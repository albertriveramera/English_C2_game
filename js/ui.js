// js/ui.js
// UI Rendering, Sound Synthesizer, Confetti, Modal Analytics, and Visual Feedback
(function () {
  'use strict';

  // --- Web Audio Sound Synthesizer (Zero external audio files required!) ---
  let audioCtx = null;

  function getAudioContext() {
    if (!audioCtx && (window.AudioContext || window.webkitAudioContext)) {
      audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    }
    if (audioCtx && audioCtx.state === 'suspended') {
      audioCtx.resume();
    }
    return audioCtx;
  }

  function playTone(freq, type, duration, startTime = 0, gainLevel = 0.1) {
    try {
      const ctx = getAudioContext();
      if (!ctx) return;
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();

      osc.type = type;
      osc.frequency.setValueAtTime(freq, ctx.currentTime + startTime);

      gain.gain.setValueAtTime(gainLevel, ctx.currentTime + startTime);
      gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + startTime + duration);

      osc.connect(gain);
      gain.connect(ctx.destination);

      osc.start(ctx.currentTime + startTime);
      osc.stop(ctx.currentTime + startTime + duration);
    } catch (e) {
      // Audio might fail if user hasn't interacted yet
    }
  }

  function playCorrectSound() {
    // Ascending arpeggio (C5 -> E5 -> G5 -> C6)
    playTone(523.25, 'sine', 0.18, 0, 0.12);
    playTone(659.25, 'sine', 0.18, 0.08, 0.12);
    playTone(783.99, 'sine', 0.22, 0.16, 0.12);
    playTone(1046.50, 'sine', 0.35, 0.24, 0.15);
  }

  function playWrongSound() {
    // Gentle soft low chime
    playTone(220, 'triangle', 0.25, 0, 0.15);
    playTone(180, 'triangle', 0.35, 0.08, 0.15);
  }

  function playLevelUpSound() {
    // Fanfare
    playTone(440, 'triangle', 0.12, 0, 0.12);
    playTone(554.37, 'triangle', 0.12, 0.1, 0.12);
    playTone(659.25, 'triangle', 0.15, 0.2, 0.12);
    playTone(880, 'sine', 0.45, 0.3, 0.15);
  }

  function playClickSound() {
    playTone(800, 'sine', 0.03, 0, 0.04);
  }

  // --- Pure Canvas Confetti Burst ---
  function launchConfetti() {
    const canvas = document.createElement('canvas');
    canvas.style.position = 'fixed';
    canvas.style.top = '0';
    canvas.style.left = '0';
    canvas.style.width = '100vw';
    canvas.style.height = '100vh';
    canvas.style.pointerEvents = 'none';
    canvas.style.zIndex = '9999';
    document.body.appendChild(canvas);

    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    const ctx = canvas.getContext('2d');

    const colors = ['#6366f1', '#ec4899', '#06b6d4', '#10b981', '#fbbf24', '#a855f7'];
    const particles = [];
    for (let i = 0; i < 90; i++) {
      particles.push({
        x: canvas.width / 2,
        y: canvas.height / 2,
        vx: (Math.random() - 0.5) * 16,
        vy: (Math.random() - 0.7) * 16,
        size: Math.random() * 8 + 4,
        color: colors[Math.floor(Math.random() * colors.length)],
        rotation: Math.random() * 360,
        rotSpeed: (Math.random() - 0.5) * 8,
        alpha: 1
      });
    }

    let frame = 0;
    function animate() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      let alive = false;
      particles.forEach(p => {
        p.x += p.vx;
        p.y += p.vy;
        p.vy += 0.35; // gravity
        p.alpha -= 0.012;
        p.rotation += p.rotSpeed;

        if (p.alpha > 0) {
          alive = true;
          ctx.save();
          ctx.translate(p.x, p.y);
          ctx.rotate((p.rotation * Math.PI) / 180);
          ctx.fillStyle = p.color;
          ctx.globalAlpha = Math.max(0, p.alpha);
          ctx.fillRect(-p.size / 2, -p.size / 2, p.size, p.size);
          ctx.restore();
        }
      });

      frame++;
      if (alive && frame < 120) {
        requestAnimationFrame(animate);
      } else {
        if (canvas.parentNode) {
          canvas.parentNode.removeChild(canvas);
        }
      }
    }
    requestAnimationFrame(animate);
  }

  // --- Rendering UI Helpers ---

  function updateHeaderStats(state) {
    const eloEl = document.getElementById('stat-elo-val');
    const streakEl = document.getElementById('stat-streak-val');
    const rankEl = document.getElementById('stat-rank-val');
    const rankBadgeEl = document.getElementById('stat-rank-badge');

    const globalElo = window.C2ELO.globalRating(state);
    const rankInfo = window.C2ELO.getRank(globalElo, state.profile.totalCorrect, state.profile.rankIndex);

    if (eloEl) eloEl.textContent = `${globalElo} ELO`;
    if (streakEl) streakEl.textContent = `${state.profile.streakDays}d`;
    if (rankEl) rankEl.textContent = rankInfo.rank.title;
    if (rankBadgeEl) rankBadgeEl.textContent = rankInfo.rank.badge;
  }

  function showEloDeltaBadge(delta) {
    const deltaEl = document.getElementById('stat-elo-delta');
    if (!deltaEl) return;

    deltaEl.style.display = 'inline-block';
    deltaEl.className = 'delta-badge ' + (delta >= 0 ? 'gain' : 'loss');
    deltaEl.textContent = (delta >= 0 ? '+' : '') + delta;

    setTimeout(() => {
      deltaEl.style.display = 'none';
    }, 2800);
  }

  function renderMasteryOverview(state) {
    const all = window.C2Engine.getAllQuestions();
    const summary = window.C2SRS.getMasterySummary(all, state);

    const masteredBar = document.getElementById('bar-mastered');
    const reviewingBar = document.getElementById('bar-reviewing');
    const learningBar = document.getElementById('bar-learning');
    const percentEl = document.getElementById('mastery-percent-text');

    const masteredPct = (summary.mastered / summary.total) * 100;
    const reviewingPct = (summary.reviewing / summary.total) * 100;
    const learningPct = (summary.learning / summary.total) * 100;

    if (masteredBar) masteredBar.style.width = masteredPct + '%';
    if (reviewingBar) reviewingBar.style.width = reviewingPct + '%';
    if (learningBar) learningBar.style.width = learningPct + '%';
    if (percentEl) percentEl.textContent = `${summary.masteryPercent}% Mastery`;

    const countMastered = document.getElementById('legend-mastered-count');
    const countReviewing = document.getElementById('legend-reviewing-count');
    const countLearning = document.getElementById('legend-learning-count');
    const countUnseen = document.getElementById('legend-unseen-count');

    if (countMastered) countMastered.textContent = `Mastered (${summary.mastered.toLocaleString()})`;
    if (countReviewing) countReviewing.textContent = `Review (${summary.reviewing.toLocaleString()})`;
    if (countLearning) countLearning.textContent = `Learning (${summary.learning.toLocaleString()})`;
    if (countUnseen) countUnseen.textContent = `Unseen (${summary.unseen.toLocaleString()})`;

    // Check mistake button badge
    const mistakeBtn = document.getElementById('btn-review-mistakes');
    const mistakeCountBadge = document.getElementById('mistakes-count-badge');
    const mistakeCount = (state.mistakesQueue || []).length;

    if (mistakeBtn && mistakeCountBadge) {
      if (mistakeCount > 0) {
        mistakeBtn.style.display = 'inline-flex';
        mistakeCountBadge.textContent = mistakeCount;
      } else {
        mistakeBtn.style.display = 'none';
      }
    }
  }

  function renderModeCards(state) {
    const MODES = [
      { id: 'vocabulary', title: 'Erudite Vocabulary', icon: '📖', desc: 'Rare, evocative, and high-register lexical precision.' },
      { id: 'collocations', title: 'Collocations & Idioms', icon: '🔗', desc: 'Fixed prepositional idioms, binomials, and authentic pairings.' },
      { id: 'phrasal', title: 'Nuanced Phrasal Verbs', icon: '⚡', desc: 'Subtle particles, multi-word verbs, and formal idioms.' },
      { id: 'cloze', title: 'Use of English & Cloze', icon: '🧩', desc: 'Cambridge-style Key Word Transformations & semantic cloze.' },
      { id: 'grammar', title: 'Grammar & Inversion', icon: '⚖️', desc: 'Negative inversion, mandative subjunctive, and cleft sentences.' },
      { id: 'confusables', title: 'Confusables & Nuance', icon: '🔍', desc: 'Subtle distinctions in pairs, false friends, and register shifts.' }
    ];

    const container = document.getElementById('modes-grid-container');
    if (!container) return;

    container.innerHTML = '';

    MODES.forEach(mode => {
      const rating = (state.ratings && typeof state.ratings[mode.id] === 'number') ? state.ratings[mode.id] : 1400;
      const stats = (state.answersByMode && state.answersByMode[mode.id]) ? state.answersByMode[mode.id] : { total: 0, correct: 0 };
      const accuracy = stats.total > 0 ? Math.round((stats.correct / stats.total) * 100) : 0;
      const variety = window.C2ELO.varietyMultiplier(state.recentModes, mode.id);

      let varietyHtml = '';
      if (variety.isBonus) {
        varietyHtml = `<span class="variety-chip bonus" title="${variety.label}">✨ ×${variety.multiplier.toFixed(2)} bonus</span>`;
      } else if (variety.isPenalty) {
        varietyHtml = `<span class="variety-chip penalty" title="${variety.label}">⚠️ ×${variety.multiplier.toFixed(2)} penalty</span>`;
      } else {
        varietyHtml = `<span class="variety-chip balanced" title="${variety.label}">⚖️ ×1.00 balanced</span>`;
      }

      const card = document.createElement('div');
      card.className = 'mode-card';
      card.dataset.mode = mode.id;

      card.innerHTML = `
        <div class="mode-card-header">
          <div class="mode-icon">${mode.icon}</div>
          <div class="mode-header-badges">
            <span class="mode-elo-tag">${rating} ELO</span>
            ${varietyHtml}
          </div>
        </div>
        <h4 class="mode-title">${mode.title}</h4>
        <p class="mode-desc">${mode.desc}</p>
        <div class="mode-card-footer">
          <span>${stats.total > 0 ? `${accuracy}% acc (${stats.total} ans)` : 'Unranked'}</span>
          <span class="mode-play-prompt">Practice &rarr;</span>
        </div>
      `;

      card.addEventListener('click', () => {
        if (window.C2App) {
          window.C2App.startModeSession(mode.id);
        }
      });

      container.appendChild(card);
    });
  }

  function renderRanksModal(state) {
    // 1. Update Lifetime Stats
    const elSessions = document.getElementById('modal-stat-sessions');
    const elAccuracy = document.getElementById('modal-stat-accuracy');
    const elMistakes = document.getElementById('modal-stat-mistakes');

    const totalAnswered = state.profile.totalAnswered || 0;
    const totalCorrect = state.profile.totalCorrect || 0;
    const accuracy = totalAnswered > 0 ? Math.round((totalCorrect / totalAnswered) * 100) : 0;

    if (elSessions) elSessions.textContent = (state.profile.sessionsCompleted || 0).toLocaleString();
    if (elAccuracy) elAccuracy.textContent = `${accuracy}%`;
    if (elMistakes) elMistakes.textContent = (state.mistakesQueue || []).length;

    const globalElo = window.C2ELO.globalRating(state);
    const rankInfo = window.C2ELO.getRank(globalElo, totalCorrect, state.profile.rankIndex);

    // 2. Render Rank Progress Card
    const progressMount = document.getElementById('modal-rank-progress-mount');
    if (progressMount) {
      if (rankInfo.nextRank) {
        progressMount.innerHTML = `
          <div class="rank-progress-card">
            <div class="rank-progress-header">
              <span>Next Rank: <strong>${rankInfo.nextRank.badge} ${rankInfo.nextRank.title}</strong></span>
              <span>Req: <strong>${rankInfo.nextRank.minElo} ELO</strong> &bull; <strong>${rankInfo.nextRank.minCorrect} Correct</strong></span>
            </div>
            <div style="font-size: 0.76rem; color: #94a3b8; margin-bottom: 4px;">ELO Rating Progress (${globalElo} / ${rankInfo.nextRank.minElo})</div>
            <div class="rank-progress-track">
              <div class="rank-progress-fill" style="width: ${Math.round(rankInfo.progressElo * 100)}%;"></div>
            </div>
            <div style="font-size: 0.76rem; color: #94a3b8; margin-bottom: 4px;">Lifetime Correct Answers (${totalCorrect} / ${rankInfo.nextRank.minCorrect})</div>
            <div class="rank-progress-track">
              <div class="rank-progress-fill" style="width: ${Math.round(rankInfo.progressCorrect * 100)}%; background: linear-gradient(135deg, #10b981, #06b6d4);"></div>
            </div>
          </div>
        `;
      } else {
        progressMount.innerHTML = `
          <div class="rank-progress-card" style="border-color: rgba(236, 72, 153, 0.4); text-align: center;">
            <div style="font-size: 1.1rem; font-weight: 800; color: #f472b6;">👑 Supreme CEFR C2 Master of English</div>
            <p style="font-size: 0.85rem; color: #94a3b8; margin-top: 4px;">You have attained the pinnacle tier of English lexical and syntactic fluency.</p>
          </div>
        `;
      }
    }

    // 3. Render Skill ELO Grid (6 categories)
    const categoryMount = document.getElementById('modal-category-elo-mount');
    if (categoryMount) {
      const MODES = [
        { id: 'vocabulary', name: 'Vocabulary', icon: '📖' },
        { id: 'collocations', name: 'Collocations', icon: '🔗' },
        { id: 'phrasal', name: 'Phrasal Verbs', icon: '⚡' },
        { id: 'cloze', name: 'Cloze & KWT', icon: '🧩' },
        { id: 'grammar', name: 'Grammar', icon: '⚖️' },
        { id: 'confusables', name: 'Confusables', icon: '🔍' }
      ];

      categoryMount.innerHTML = MODES.map(m => {
        const rating = (state.ratings && state.ratings[m.id]) ? state.ratings[m.id] : 1400;
        const stats = (state.answersByMode && state.answersByMode[m.id]) ? state.answersByMode[m.id] : { total: 0, correct: 0 };
        const acc = stats.total > 0 ? Math.round((stats.correct / stats.total) * 100) : 0;
        const variety = window.C2ELO.varietyMultiplier(state.recentModes, m.id);

        let chip = '⚖️ 1.0x';
        if (variety.isBonus) chip = `✨ ×${variety.multiplier.toFixed(2)}`;
        if (variety.isPenalty) chip = `⚠️ ×${variety.multiplier.toFixed(2)}`;

        return `
          <div class="category-elo-card">
            <div class="category-elo-card-top">
              <span class="category-elo-title">${m.icon} ${m.name}</span>
              <span class="category-elo-val">${rating}</span>
            </div>
            <div class="category-elo-card-sub">
              <span>${stats.total} ans &bull; ${acc}%</span>
              <span>${chip}</span>
            </div>
          </div>
        `;
      }).join('');
    }

    // 4. Render Ranks Ladder
    const ranksList = document.getElementById('modal-ranks-list');
    if (ranksList) {
      const allRanks = window.C2ELO.CFG.RANKS;
      ranksList.innerHTML = allRanks.map(r => {
        const isCurrent = r.index === rankInfo.index;
        const isUnlocked = r.index <= rankInfo.index;
        const cls = isCurrent ? 'rank-item-row current' : (isUnlocked ? 'rank-item-row unlocked' : 'rank-item-row locked');

        return `
          <div class="${cls}">
            <div class="rank-item-left">
              <div class="rank-item-badge">${r.badge}</div>
              <div>
                <div class="rank-item-title">${r.title} ${isCurrent ? '<span style="font-size: 0.72rem; color: #818cf8; margin-left: 6px;">(CURRENT TIER)</span>' : ''}</div>
                <div style="font-size: 0.78rem; color: #94a3b8;">${r.desc}</div>
              </div>
            </div>
            <div class="rank-item-elo" style="text-align: right;">
              <div>${r.minElo}+ ELO</div>
              <div style="font-size: 0.72rem; color: #64748b;">${r.minCorrect}+ correct</div>
            </div>
          </div>
        `;
      }).join('');
    }
  }

  window.C2UI = {
    playCorrectSound: playCorrectSound,
    playWrongSound: playWrongSound,
    playLevelUpSound: playLevelUpSound,
    playClickSound: playClickSound,
    launchConfetti: launchConfetti,
    updateHeaderStats: updateHeaderStats,
    showEloDeltaBadge: showEloDeltaBadge,
    renderMasteryOverview: renderMasteryOverview,
    renderModeCards: renderModeCards,
    renderRanksModal: renderRanksModal
  };
})();
