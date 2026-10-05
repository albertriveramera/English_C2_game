// UI Rendering, Sound Synthesizer, Confetti and Animations
(function () {
  'use strict';

  // --- Web Audio Sound Synthesizer (No external audio files required!) ---
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
    // Elegant ascending arpeggio (C5 -> E5 -> G5 -> C6)
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
    const xpEl = document.getElementById('stat-xp-val');
    const streakEl = document.getElementById('stat-streak-val');
    const rankEl = document.getElementById('stat-rank-val');
    const rankBadgeEl = document.getElementById('stat-rank-badge');

    const rank = window.C2Engine.getRank(state.profile.xp);

    if (xpEl) xpEl.textContent = state.profile.xp.toLocaleString() + ' XP';
    if (streakEl) streakEl.textContent = state.profile.streakDays + 'd';
    if (rankEl) rankEl.textContent = rank.title;
    if (rankBadgeEl) rankBadgeEl.textContent = rank.badge;
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
      { id: 'vocabulary', title: 'Erudite Vocabulary', icon: '📖', desc: 'Rare, nuanced, and evocative high-register lexical precision.' },
      { id: 'collocations', title: 'Collocations & Idioms', icon: '🔗', desc: 'Fixed prepositional idioms, binomials, and authentic pairings.' },
      { id: 'phrasal', title: 'Nuanced Phrasal Verbs', icon: '⚡', desc: 'Subtle particles, multi-word verbs, and formal idioms.' },
      { id: 'cloze', title: 'Use of English & Cloze', icon: '🧩', desc: 'Cambridge-style Key Word Transformations & semantic cloze.' },
      { id: 'grammar', title: 'Grammar & Inversion', icon: '⚖️', desc: 'Negative inversion, mandative subjunctive, and cleft sentences.' },
      { id: 'confusables', title: 'Confusables & Nuance', icon: '🔍', desc: 'Subtle distinctions in homophones, pairs, and fine semantic shifts.' }
    ];

    const container = document.getElementById('modes-grid-container');
    if (!container) return;

    container.innerHTML = '';

    MODES.forEach(mode => {
      const lvl = state.adaptiveLevels[mode.id] || 2;
      const stats = state.modeStats[mode.id] || { correct: 0, total: 0 };
      const accuracy = stats.total > 0 ? Math.round((stats.correct / stats.total) * 100) : 0;

      const card = document.createElement('div');
      card.className = 'mode-card';
      card.dataset.mode = mode.id;

      card.innerHTML = `
        <div class="mode-card-header">
          <div class="mode-icon">${mode.icon}</div>
          <span class="mode-level-badge">Adaptive Lvl ${lvl}</span>
        </div>
        <h4 class="mode-title">${mode.title}</h4>
        <p class="mode-desc">${mode.desc}</p>
        <div class="mode-card-footer">
          <span>${stats.total > 0 ? accuracy + '% accuracy' : 'Not practiced'}</span>
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

  window.C2UI = {
    playCorrectSound: playCorrectSound,
    playWrongSound: playWrongSound,
    playLevelUpSound: playLevelUpSound,
    playClickSound: playClickSound,
    launchConfetti: launchConfetti,
    updateHeaderStats: updateHeaderStats,
    renderMasteryOverview: renderMasteryOverview,
    renderModeCards: renderModeCards
  };
})();
