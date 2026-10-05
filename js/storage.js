// Storage management and persistence for C2 English Arcade
(function () {
  'use strict';

  const STORAGE_KEY = 'c2_arcade_v1_save';

  const DEFAULT_STATE = {
    version: 1,
    profile: {
      xp: 0,
      streakDays: 0,
      lastPlayedDate: null,
      sessionsCompleted: 0,
      totalCorrect: 0,
      totalAnswered: 0
    },
    adaptiveLevels: {
      vocabulary: 2,
      collocations: 2,
      phrasal: 2,
      cloze: 2,
      grammar: 2,
      confusables: 2
    },
    modeStreaks: {
      vocabulary: 0,
      collocations: 0,
      phrasal: 0,
      cloze: 0,
      grammar: 0,
      confusables: 0
    },
    items: {}, // id -> { box: 1..5, timesCorrect, timesWrong, lastSeen, nextReview, due }
    mistakesQueue: [], // list of question IDs pending redemption
    modeStats: {
      vocabulary: { correct: 0, total: 0 },
      collocations: { correct: 0, total: 0 },
      phrasal: { correct: 0, total: 0 },
      cloze: { correct: 0, total: 0 },
      grammar: { correct: 0, total: 0 },
      confusables: { correct: 0, total: 0 }
    },
    soundEnabled: true
  };

  let memoryFallback = null;

  function isLocalStorageAvailable() {
    try {
      const testKey = '__c2_storage_test__';
      window.localStorage.setItem(testKey, 'ok');
      window.localStorage.removeItem(testKey);
      return true;
    } catch (e) {
      return false;
    }
  }

  const hasStorage = isLocalStorageAvailable();

  function loadState() {
    if (!hasStorage) {
      if (!memoryFallback) {
        memoryFallback = JSON.parse(JSON.stringify(DEFAULT_STATE));
      }
      return memoryFallback;
    }
    try {
      const raw = window.localStorage.getItem(STORAGE_KEY);
      if (!raw) {
        const fresh = JSON.parse(JSON.stringify(DEFAULT_STATE));
        saveState(fresh);
        return fresh;
      }
      const parsed = JSON.parse(raw);
      // Merge with defaults in case of missing keys
      return Object.assign({}, DEFAULT_STATE, parsed, {
        profile: Object.assign({}, DEFAULT_STATE.profile, parsed.profile || {}),
        adaptiveLevels: Object.assign({}, DEFAULT_STATE.adaptiveLevels, parsed.adaptiveLevels || {}),
        modeStreaks: Object.assign({}, DEFAULT_STATE.modeStreaks, parsed.modeStreaks || {}),
        modeStats: Object.assign({}, DEFAULT_STATE.modeStats, parsed.modeStats || {}),
        items: parsed.items || {},
        mistakesQueue: parsed.mistakesQueue || []
      });
    } catch (err) {
      console.warn('Failed to parse localStorage, resetting to defaults:', err);
      const fallback = JSON.parse(JSON.stringify(DEFAULT_STATE));
      saveState(fallback);
      return fallback;
    }
  }

  function saveState(state) {
    if (!hasStorage) {
      memoryFallback = state;
      return;
    }
    try {
      window.localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
    } catch (err) {
      console.error('Failed to save to localStorage:', err);
    }
  }

  function resetProgress() {
    if (hasStorage) {
      try {
        window.localStorage.removeItem(STORAGE_KEY);
      } catch (e) { }
    }
    memoryFallback = null;
    return loadState();
  }

  window.C2Storage = {
    loadState: loadState,
    saveState: saveState,
    resetProgress: resetProgress,
    DEFAULT_STATE: DEFAULT_STATE
  };
})();
