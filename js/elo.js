// js/elo.js
// Advanced ELO Rating, Variety Multiplier, and Adaptive Progression Engine
(function () {
  'use strict';

  const MODES = ['vocabulary', 'collocations', 'phrasal', 'cloze', 'grammar', 'confusables'];

  const CFG = {
    DEFAULT_RATING: 1400,
    BASE_K_PROVISIONAL: 40, // < 30 answers in mode
    BASE_K_CALIBRATED: 28,  // 30..99 answers in mode
    BASE_K_MASTERED: 20,    // >= 100 answers in mode
    PROVISIONAL_CUTOFF: 30,
    CALIBRATED_CUTOFF: 100,

    HISTORY_WINDOW: 40,     // recent answers for variety evaluation
    VARIETY_MIN_ANSWERS: 10,
    VARIETY_OVERPLAYED_THRESHOLD: 0.25,  // > 25% share of recent 40 answers
    VARIETY_UNDERPLAYED_THRESHOLD: 0.10, // < 10% share of recent 40 answers
    VARIETY_MAX_PENALTY: 0.50,          // drops down to 0.50x
    VARIETY_MAX_BONUS: 1.20,            // rises up to 1.20x

    LEVEL_RATINGS: {
      1: 1100,
      2: 1250,
      3: 1400,
      4: 1550,
      5: 1700
    },
    TRANSFORMATION_BONUS: 25,
    HYSTERESIS_BUFFER: 25,

    RANKS: [
      {
        index: 0,
        title: 'C1 Contender',
        badge: '🥉',
        minElo: 1200,
        minCorrect: 0,
        desc: 'Solid C1 footing. Ramping up precision.'
      },
      {
        index: 1,
        title: 'C1+ Advanced',
        badge: '🥈',
        minElo: 1350,
        minCorrect: 25,
        desc: 'Refined nuances and complex structures.'
      },
      {
        index: 2,
        title: 'Pre-C2 Proficient',
        badge: '🥇',
        minElo: 1500,
        minCorrect: 60,
        desc: 'High idiomatic command and rhetorical mastery.'
      },
      {
        index: 3,
        title: 'C2 Candidate',
        badge: '💎',
        minElo: 1650,
        minCorrect: 120,
        desc: 'Approaching native-like scholarly and stylistic fluency.'
      },
      {
        index: 4,
        title: 'C2 Master',
        badge: '👑',
        minElo: 1800,
        minCorrect: 200,
        desc: 'Full Mastery (CEFR C2). Exceptional lexical breadth.'
      }
    ]
  };

  function questionRating(q) {
    if (!q) return CFG.DEFAULT_RATING;
    let base = q.rating;
    if (typeof base !== 'number') {
      base = CFG.LEVEL_RATINGS[q.level] || CFG.DEFAULT_RATING;
    }
    if (q.type === 'transformation') {
      base += CFG.TRANSFORMATION_BONUS;
    }
    return base;
  }

  function expectedScore(playerRating, qRating, qType) {
    const diff = (qRating - playerRating) / 400;
    const stdExpected = 1 / (1 + Math.pow(10, diff));

    if (qType === 'choice') {
      // 4-choice guess floor adjustment (c = 0.25)
      const c = 0.25;
      const adjusted = c + (1 - c) * stdExpected;
      return Math.min(0.99, Math.max(0.01, adjusted));
    }

    // Open/Transformation (no guess floor)
    return Math.min(0.99, Math.max(0.01, stdExpected));
  }

  function kFactor(answerCount) {
    const count = answerCount || 0;
    if (count < CFG.PROVISIONAL_CUTOFF) return CFG.BASE_K_PROVISIONAL;
    if (count < CFG.CALIBRATED_CUTOFF) return CFG.BASE_K_CALIBRATED;
    return CFG.BASE_K_MASTERED;
  }

  function varietyMultiplier(recentModes, currentMode) {
    const history = recentModes || [];
    const count = history.length;

    if (count < CFG.VARIETY_MIN_ANSWERS) {
      return {
        multiplier: 1.0,
        share: count > 0 ? (history.filter(m => m === currentMode).length / count) : (1 / 6),
        label: 'Balanced (Calibrating)',
        isBonus: false,
        isPenalty: false
      };
    }

    const modeCount = history.filter(m => m === currentMode).length;
    const share = modeCount / count;

    if (share > CFG.VARIETY_OVERPLAYED_THRESHOLD) {
      // Penalty down to 0.50x
      const excess = share - CFG.VARIETY_OVERPLAYED_THRESHOLD;
      const penaltyProgress = Math.min(1.0, excess / 0.40);
      const mult = Math.max(CFG.VARIETY_MAX_PENALTY, 1.0 - (penaltyProgress * (1.0 - CFG.VARIETY_MAX_PENALTY)));
      const rounded = Math.round(mult * 100) / 100;
      return {
        multiplier: rounded,
        share: share,
        label: `Overplayed (${Math.round(share * 100)}% share): ×${rounded.toFixed(2)} gain penalty`,
        isBonus: false,
        isPenalty: true
      };
    }

    if (share < CFG.VARIETY_UNDERPLAYED_THRESHOLD) {
      // Bonus up to 1.20x
      const deficit = CFG.VARIETY_UNDERPLAYED_THRESHOLD - share;
      const bonusProgress = Math.min(1.0, deficit / CFG.VARIETY_UNDERPLAYED_THRESHOLD);
      const mult = Math.min(CFG.VARIETY_MAX_BONUS, 1.0 + (bonusProgress * (CFG.VARIETY_MAX_BONUS - 1.0)));
      const rounded = Math.round(mult * 100) / 100;
      return {
        multiplier: rounded,
        share: share,
        label: `Neglected category (${Math.round(share * 100)}% share): ×${rounded.toFixed(2)} variety bonus`,
        isBonus: true,
        isPenalty: false
      };
    }

    return {
      multiplier: 1.0,
      share: share,
      label: 'Balanced variety',
      isBonus: false,
      isPenalty: false
    };
  }

  function calculateDelta(playerRating, qRating, qType, wasCorrect, answerCount, recentModes, currentMode) {
    const exp = expectedScore(playerRating, qRating, qType);
    const k = kFactor(answerCount);
    const outcome = wasCorrect ? 1.0 : 0.0;
    const rawDelta = k * (outcome - exp);
    const variety = varietyMultiplier(recentModes, currentMode);

    let finalDelta;
    if (wasCorrect) {
      // Apply variety multiplier to gains only
      finalDelta = Math.round(rawDelta * variety.multiplier);
      if (finalDelta < 1) finalDelta = 1; // Minimum +1 on correct answer
    } else {
      // Losses are NEVER reduced by variety penalties
      finalDelta = Math.round(rawDelta);
      if (finalDelta > -1) finalDelta = -1; // Minimum -1 on incorrect answer
    }

    return {
      delta: finalDelta,
      rawDelta: Math.round(rawDelta),
      expected: exp,
      kFactor: k,
      variety: variety,
      qRating: qRating,
      playerRating: playerRating
    };
  }

  function globalRating(state) {
    const ratings = state.ratings || {};
    let sum = 0;
    MODES.forEach(m => {
      sum += (typeof ratings[m] === 'number') ? ratings[m] : CFG.DEFAULT_RATING;
    });
    return Math.round(sum / MODES.length);
  }

  function getRank(globalElo, totalCorrect, currentRankIndex = 0) {
    let activeIndex = currentRankIndex;

    // Check promotions (must meet both Elo and totalCorrect)
    for (let i = CFG.RANKS.length - 1; i >= 0; i--) {
      const r = CFG.RANKS[i];
      if (globalElo >= r.minElo && totalCorrect >= r.minCorrect) {
        if (i > activeIndex) {
          activeIndex = i;
        }
        break;
      }
    }

    // Check demotion with hysteresis buffer (25 pts)
    if (activeIndex > 0) {
      const currentRank = CFG.RANKS[activeIndex];
      if (globalElo < (currentRank.minElo - CFG.HYSTERESIS_BUFFER)) {
        // Demote by one tier
        activeIndex -= 1;
      }
    }

    const currentRank = CFG.RANKS[activeIndex];
    const nextRank = CFG.RANKS[activeIndex + 1] || null;

    let progressElo = 1.0;
    let progressCorrect = 1.0;
    if (nextRank) {
      const eloSpan = nextRank.minElo - currentRank.minElo;
      progressElo = Math.max(0, Math.min(1, (globalElo - currentRank.minElo) / eloSpan));
      const correctSpan = nextRank.minCorrect - currentRank.minCorrect;
      progressCorrect = Math.max(0, Math.min(1, (totalCorrect - currentRank.minCorrect) / correctSpan));
    }

    return {
      index: activeIndex,
      rank: currentRank,
      nextRank: nextRank,
      progressElo: progressElo,
      progressCorrect: progressCorrect,
      overallProgress: Math.min(progressElo, progressCorrect)
    };
  }

  function applyAnswer(state, question, wasCorrect) {
    const mode = question.mode;
    state.ratings = state.ratings || {};
    state.answersByMode = state.answersByMode || {};
    state.recentModes = state.recentModes || [];
    state.eloHistory = state.eloHistory || [];

    if (typeof state.ratings[mode] !== 'number') {
      state.ratings[mode] = CFG.DEFAULT_RATING;
    }
    if (!state.answersByMode[mode]) {
      state.answersByMode[mode] = { total: 0, correct: 0 };
    }

    const pRating = state.ratings[mode];
    const qR = questionRating(question);
    const ansCount = state.answersByMode[mode].total;

    const calc = calculateDelta(pRating, qR, question.type, wasCorrect, ansCount, state.recentModes, mode);

    // Apply to category rating
    const newRating = Math.max(500, pRating + calc.delta);
    state.ratings[mode] = newRating;

    // Update mode answer counts
    state.answersByMode[mode].total += 1;
    if (wasCorrect) {
      state.answersByMode[mode].correct += 1;
    }

    // Append to recentModes FIFO (window of 40)
    state.recentModes.push(mode);
    if (state.recentModes.length > CFG.HISTORY_WINDOW) {
      state.recentModes.shift();
    }

    // Compute new global rating
    const newGlobal = globalRating(state);
    state.globalRating = newGlobal;

    // Check rank progression
    const totalCorrect = state.profile.totalCorrect || 0;
    const currentRankIdx = state.profile.rankIndex || 0;
    const rankInfo = getRank(newGlobal, totalCorrect, currentRankIdx);

    const promoted = rankInfo.index > currentRankIdx;
    const demoted = rankInfo.index < currentRankIdx;
    state.profile.rankIndex = rankInfo.index;

    // Append history entry
    const historyEntry = {
      timestamp: Date.now(),
      qid: question.id,
      mode: mode,
      wasCorrect: wasCorrect,
      qRating: qR,
      oldRating: pRating,
      newRating: newRating,
      delta: calc.delta,
      globalRating: newGlobal,
      rankIndex: rankInfo.index
    };
    state.eloHistory.push(historyEntry);
    if (state.eloHistory.length > 100) {
      state.eloHistory.shift();
    }

    return {
      delta: calc.delta,
      rawDelta: calc.rawDelta,
      expected: calc.expected,
      kFactor: calc.kFactor,
      variety: calc.variety,
      qRating: qR,
      newRating: newRating,
      newGlobal: newGlobal,
      rankInfo: rankInfo,
      promoted: promoted,
      demoted: demoted,
      historyEntry: historyEntry
    };
  }

  function undoLastAnswer(state, lastHistoryEntry, overrideWasCorrect) {
    if (!lastHistoryEntry) return null;

    const mode = lastHistoryEntry.mode;
    // Revert category rating
    state.ratings[mode] -= lastHistoryEntry.delta;

    // Revert answer count
    if (state.answersByMode[mode]) {
      state.answersByMode[mode].total = Math.max(0, state.answersByMode[mode].total - 1);
      if (lastHistoryEntry.wasCorrect) {
        state.answersByMode[mode].correct = Math.max(0, state.answersByMode[mode].correct - 1);
      }
    }

    // Remove from recentModes
    const idx = state.recentModes.lastIndexOf(mode);
    if (idx !== -1) {
      state.recentModes.splice(idx, 1);
    }

    // Remove from history
    const hIdx = state.eloHistory.indexOf(lastHistoryEntry);
    if (hIdx !== -1) {
      state.eloHistory.splice(hIdx, 1);
    }

    // Now re-apply with overrideWasCorrect
    const question = window.C2Engine.getQuestionById(lastHistoryEntry.qid);
    if (!question) return null;

    return applyAnswer(state, question, overrideWasCorrect);
  }

  // Gaussian-weighted sampling around player's rating
  function pickWeighted(questions, targetRating, count) {
    if (!questions || questions.length === 0) return [];
    if (questions.length <= count) {
      return questions.slice();
    }

    const sigma = 180; // Spread of selection
    const pool = questions.slice();
    const picked = [];

    while (picked.length < count && pool.length > 0) {
      let totalWeight = 0;
      const weights = pool.map(q => {
        const qr = questionRating(q);
        const diff = qr - targetRating;
        const w = Math.exp(-(diff * diff) / (2 * sigma * sigma));
        totalWeight += w;
        return w;
      });

      let r = Math.random() * totalWeight;
      let selectedIdx = 0;
      for (let i = 0; i < pool.length; i++) {
        r -= weights[i];
        if (r <= 0) {
          selectedIdx = i;
          break;
        }
      }

      picked.push(pool[selectedIdx]);
      pool.splice(selectedIdx, 1);
    }

    return picked;
  }

  window.C2ELO = {
    MODES: MODES,
    CFG: CFG,
    questionRating: questionRating,
    expectedScore: expectedScore,
    kFactor: kFactor,
    varietyMultiplier: varietyMultiplier,
    calculateDelta: calculateDelta,
    globalRating: globalRating,
    getRank: getRank,
    applyAnswer: applyAnswer,
    undoLastAnswer: undoLastAnswer,
    pickWeighted: pickWeighted
  };
})();
