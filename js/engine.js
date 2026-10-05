// Game Engine: scoring, adaptive difficulty, XP, ranks, and session generation
(function () {
  'use strict';

  const RANKS = [
    { minXp: 0, title: 'C1 Contender', badge: '🥉', next: 250, desc: 'Solid C1 footing. Ramping up precision.' },
    { minXp: 251, title: 'C1+ Advanced', badge: '🥈', next: 750, desc: 'Refined nuances and complex structures.' },
    { minXp: 751, title: 'Pre-C2 Vanguard', badge: '🥇', next: 1600, desc: 'High idiomatic command and rhetorical mastery.' },
    { minXp: 1601, title: 'C2 Candidate', badge: '💎', next: 3000, desc: 'Approaching native-like scholarly and stylistic fluency.' },
    { minXp: 3001, title: 'C2 Master of English', badge: '👑', next: null, desc: 'Full Mastery (CEFR C2). Exceptional lexical breadth.' }
  ];

  function getRank(xp) {
    let current = RANKS[0];
    for (let i = 0; i < RANKS.length; i++) {
      if (xp >= RANKS[i].minXp) {
        current = RANKS[i];
      } else {
        break;
      }
    }
    return current;
  }

  function getAllQuestions() {
    const bank = window.C2_DATA || {};
    let all = [];
    Object.values(bank).forEach(arr => {
      if (Array.isArray(arr)) {
        all = all.concat(arr);
      }
    });
    return all;
  }

  function getQuestionById(id) {
    const all = getAllQuestions();
    return all.find(q => q.id === id) || null;
  }

  function getTodayString() {
    const now = new Date();
    const y = now.getFullYear();
    const m = String(now.getMonth() + 1).padStart(2, '0');
    const d = String(now.getDate()).padStart(2, '0');
    return `${y}-${m}-${d}`;
  }

  function updateDailyStreak(state) {
    const today = getTodayString();
    const last = state.profile.lastPlayedDate;

    if (!last) {
      state.profile.streakDays = 1;
    } else if (last === today) {
      // already played today, streak remains
    } else {
      const lastDate = new Date(last);
      const currentDate = new Date(today);
      const diffDays = Math.round((currentDate - lastDate) / (1000 * 60 * 60 * 24));
      if (diffDays === 1) {
        state.profile.streakDays = (state.profile.streakDays || 0) + 1;
      } else if (diffDays > 1) {
        state.profile.streakDays = 1;
      }
    }
    state.profile.lastPlayedDate = today;
  }

  function calculateQuestionXp(question, sessionStreak) {
    const base = (question.level || 2) * 12;
    // Streak multiplier: 1x, 1.2x, 1.4x, up to 2x
    const multiplier = Math.min(2.0, 1.0 + (sessionStreak * 0.1));
    return Math.round(base * multiplier);
  }

  function updateAdaptiveLevel(state, mode, wasCorrect) {
    if (!state.adaptiveLevels[mode]) state.adaptiveLevels[mode] = 2;
    if (!state.modeStreaks[mode]) state.modeStreaks[mode] = 0;

    let leveledUp = false;
    let leveledDown = false;

    if (wasCorrect) {
      if (state.modeStreaks[mode] < 0) state.modeStreaks[mode] = 0;
      state.modeStreaks[mode] += 1;

      // 3 consecutive correct in this mode -> level up (max 5)
      if (state.modeStreaks[mode] >= 3 && state.adaptiveLevels[mode] < 5) {
        state.adaptiveLevels[mode] += 1;
        state.modeStreaks[mode] = 0;
        leveledUp = true;
      }
    } else {
      if (state.modeStreaks[mode] > 0) state.modeStreaks[mode] = 0;
      state.modeStreaks[mode] -= 1;

      // 2 consecutive mistakes in this mode -> level down (min 1)
      if (state.modeStreaks[mode] <= -2 && state.adaptiveLevels[mode] > 1) {
        state.adaptiveLevels[mode] -= 1;
        state.modeStreaks[mode] = 0;
        leveledDown = true;
      }
    }

    return { leveledUp, leveledDown, newLevel: state.adaptiveLevels[mode] };
  }

  // Normalize text for Cambridge Key Word Transformations:
  // Lowercase, trim, remove punctuation, collapse whitespace
  function normalizeText(str) {
    if (!str) return '';
    return str
      .toLowerCase()
      .replace(/[’']/g, "'") // standardise apostrophe
      .replace(/[.,/#!$%^&*;:{}=\-_`~()?]/g, ' ') // replace punctuation with space
      .replace(/\s+/g, ' ') // collapse multiple spaces
      .trim();
  }

  function checkTransformationAnswer(question, userInput) {
    const normalizedInput = normalizeText(userInput);
    if (!normalizedInput) return false;

    for (let i = 0; i < question.accepted.length; i++) {
      const normalizedTarget = normalizeText(question.accepted[i]);
      if (normalizedInput === normalizedTarget) {
        return true;
      }
    }
    return false;
  }

  function shuffle(arr) {
    const copy = arr.slice();
    for (let i = copy.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      const temp = copy[i];
      copy[i] = copy[j];
      copy[j] = temp;
    }
    return copy;
  }

  function buildDailySession(state, count = 12) {
    const all = getAllQuestions();
    const selected = [];
    const usedIds = new Set();

    // 1. Due mistakes or SRS items (up to 4)
    const mistakeIds = state.mistakesQueue || [];
    for (let id of mistakeIds) {
      if (selected.length >= 4) break;
      const q = getQuestionById(id);
      if (q && !usedIds.has(q.id)) {
        selected.push(q);
        usedIds.add(q.id);
      }
    }

    const dueIds = window.C2SRS.getDueQuestionIds(state);
    for (let id of dueIds) {
      if (selected.length >= 5) break;
      if (!usedIds.has(id)) {
        const q = getQuestionById(id);
        if (q) {
          selected.push(q);
          usedIds.add(q.id);
        }
      }
    }

    // 2. Sample across categories respecting adaptive difficulty
    const categories = ['vocabulary', 'collocations', 'phrasal', 'cloze', 'grammar', 'confusables'];
    const bank = window.C2_DATA || {};

    // Shuffle categories so we cycle through evenly
    const cycledCats = shuffle(categories);

    let catIndex = 0;
    let attempts = 0;
    while (selected.length < count && attempts < 100) {
      attempts++;
      const cat = cycledCats[catIndex % cycledCats.length];
      catIndex++;
      const catQuestions = bank[cat] || [];
      const targetLevel = state.adaptiveLevels[cat] || 2;

      // Prefer questions close to targetLevel (targetLevel, targetLevel+1, targetLevel-1)
      const available = catQuestions.filter(q => !usedIds.has(q.id));
      if (available.length === 0) continue;

      // Sort by distance to targetLevel
      available.sort((a, b) => Math.abs(a.level - targetLevel) - Math.abs(b.level - targetLevel));

      // Pick one from top candidates
      const pick = available[0];
      selected.push(pick);
      usedIds.add(pick.id);
    }

    return shuffle(selected);
  }

  function buildModeSession(state, mode, count = 10) {
    const bank = window.C2_DATA || {};
    const catQuestions = bank[mode] || [];
    if (catQuestions.length === 0) return [];

    const targetLevel = state.adaptiveLevels[mode] || 2;
    const shuffled = shuffle(catQuestions);

    // Sort partially by distance to target level
    shuffled.sort((a, b) => Math.abs(a.level - targetLevel) - Math.abs(b.level - targetLevel));

    return shuffled.slice(0, count);
  }

  function buildMistakesSession(state) {
    const mistakeIds = state.mistakesQueue || [];
    const questions = [];
    mistakeIds.forEach(id => {
      const q = getQuestionById(id);
      if (q) questions.push(q);
    });
    return shuffle(questions);
  }

  window.C2Engine = {
    RANKS: RANKS,
    getRank: getRank,
    getAllQuestions: getAllQuestions,
    getQuestionById: getQuestionById,
    updateDailyStreak: updateDailyStreak,
    calculateQuestionXp: calculateQuestionXp,
    updateAdaptiveLevel: updateAdaptiveLevel,
    checkTransformationAnswer: checkTransformationAnswer,
    buildDailySession: buildDailySession,
    buildModeSession: buildModeSession,
    buildMistakesSession: buildMistakesSession
  };
})();
