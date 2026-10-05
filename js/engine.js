// js/engine.js
// Game Engine: ELO-weighted session generation, question retrieval, streak tracking, and answer validation
(function () {
  'use strict';

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

    const accepted = question.accepted || [];
    for (let i = 0; i < accepted.length; i++) {
      const normalizedTarget = normalizeText(accepted[i]);
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
    const selected = [];
    const usedIds = new Set();

    // 1. Due mistakes or SRS items (up to 3 items)
    const mistakeIds = state.mistakesQueue || [];
    for (let id of mistakeIds) {
      if (selected.length >= 2) break;
      const q = getQuestionById(id);
      if (q && !usedIds.has(q.id)) {
        selected.push(q);
        usedIds.add(q.id);
      }
    }

    if (window.C2SRS && window.C2SRS.getDueQuestionIds) {
      const dueIds = window.C2SRS.getDueQuestionIds(state);
      for (let id of dueIds) {
        if (selected.length >= 3) break;
        if (!usedIds.has(id)) {
          const q = getQuestionById(id);
          if (q) {
            selected.push(q);
            usedIds.add(q.id);
          }
        }
      }
    }

    // 2. Balanced ELO-weighted sampling across all 6 categories
    const categories = ['vocabulary', 'collocations', 'phrasal', 'cloze', 'grammar', 'confusables'];
    const bank = window.C2_DATA || {};
    const cycledCats = shuffle(categories);

    let catIndex = 0;
    let attempts = 0;
    while (selected.length < count && attempts < 100) {
      attempts++;
      const cat = cycledCats[catIndex % cycledCats.length];
      catIndex++;
      const catQuestions = (bank[cat] || []).filter(q => !usedIds.has(q.id));
      if (catQuestions.length === 0) continue;

      const playerCatRating = (state.ratings && state.ratings[cat]) ? state.ratings[cat] : 1400;
      const picked = window.C2ELO.pickWeighted(catQuestions, playerCatRating, 1);
      if (picked.length > 0) {
        selected.push(picked[0]);
        usedIds.add(picked[0].id);
      }
    }

    return shuffle(selected);
  }

  function buildModeSession(state, mode, count = 10) {
    const bank = window.C2_DATA || {};
    const catQuestions = bank[mode] || [];
    if (catQuestions.length === 0) return [];

    const playerRating = (state.ratings && state.ratings[mode]) ? state.ratings[mode] : 1400;
    return window.C2ELO.pickWeighted(catQuestions, playerRating, count);
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
    getAllQuestions: getAllQuestions,
    getQuestionById: getQuestionById,
    updateDailyStreak: updateDailyStreak,
    checkTransformationAnswer: checkTransformationAnswer,
    buildDailySession: buildDailySession,
    buildModeSession: buildModeSession,
    buildMistakesSession: buildMistakesSession
  };
})();
