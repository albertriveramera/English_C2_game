// js/storage.js
// Storage management, schema migration (v1 -> v2), and state persistence for C2 English Arcade
(function () {
  'use strict';

  const STORAGE_KEY = 'c2_arcade_v2_save';
  const LEGACY_V1_KEY = 'c2_arcade_v1_save';

  const DEFAULT_STATE = {
    version: 2,
    profile: {
      rankIndex: 0,
      streakDays: 0,
      lastPlayedDate: null,
      sessionsCompleted: 0,
      totalCorrect: 0,
      totalAnswered: 0
    },
    ratings: {
      vocabulary: 1400,
      collocations: 1400,
      phrasal: 1400,
      cloze: 1400,
      grammar: 1400,
      confusables: 1400
    },
    globalRating: 1400,
    answersByMode: {
      vocabulary: { total: 0, correct: 0 },
      collocations: { total: 0, correct: 0 },
      phrasal: { total: 0, correct: 0 },
      cloze: { total: 0, correct: 0 },
      grammar: { total: 0, correct: 0 },
      confusables: { total: 0, correct: 0 }
    },
    recentModes: [], // rolling window of up to 40 category responses for variety multiplier
    eloHistory: [],  // rolling log of up to 100 ELO changes
    items: {},       // id -> Leitner SRS record
    mistakesQueue: [], // list of question IDs pending redemption
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

  function migrateV1ToV2(v1Data) {
    const v2 = JSON.parse(JSON.stringify(DEFAULT_STATE));

    // Transfer profile stats (omitting legacy XP)
    if (v1Data.profile) {
      v2.profile.streakDays = v1Data.profile.streakDays || 0;
      v2.profile.lastPlayedDate = v1Data.profile.lastPlayedDate || null;
      v2.profile.sessionsCompleted = v1Data.profile.sessionsCompleted || 0;
      v2.profile.totalCorrect = v1Data.profile.totalCorrect || 0;
      v2.profile.totalAnswered = v1Data.profile.totalAnswered || 0;
    }

    // Convert legacy adaptive levels to starting ELO ratings
    const levelToElo = { 1: 1200, 2: 1350, 3: 1480, 4: 1600, 5: 1720 };
    if (v1Data.adaptiveLevels) {
      Object.keys(v2.ratings).forEach(m => {
        const lvl = v1Data.adaptiveLevels[m] || 2;
        v2.ratings[m] = levelToElo[lvl] || 1400;
      });
    }

    // Convert legacy modeStats to answersByMode
    if (v1Data.modeStats) {
      Object.keys(v2.answersByMode).forEach(m => {
        if (v1Data.modeStats[m]) {
          v2.answersByMode[m].total = v1Data.modeStats[m].total || 0;
          v2.answersByMode[m].correct = v1Data.modeStats[m].correct || 0;
        }
      });
    }

    // Transfer SRS items and mistakes queue
    v2.items = v1Data.items || {};
    v2.mistakesQueue = v1Data.mistakesQueue || [];
    v2.soundEnabled = (v1Data.soundEnabled !== undefined) ? v1Data.soundEnabled : true;

    // Calculate initial global rating
    let sum = 0;
    Object.values(v2.ratings).forEach(r => { sum += r; });
    v2.globalRating = Math.round(sum / 6);

    // Calculate rank index
    if (window.C2ELO && window.C2ELO.getRank) {
      const r = window.C2ELO.getRank(v2.globalRating, v2.profile.totalCorrect, 0);
      v2.profile.rankIndex = r.index;
    }

    v2.version = 2;
    return v2;
  }

  function loadState() {
    if (!hasStorage) {
      if (!memoryFallback) {
        memoryFallback = JSON.parse(JSON.stringify(DEFAULT_STATE));
      }
      return memoryFallback;
    }

    try {
      // Check for v2 save
      let raw = window.localStorage.getItem(STORAGE_KEY);
      if (raw) {
        const parsed = JSON.parse(raw);
        // Shallow merge with defaults
        const merged = Object.assign({}, DEFAULT_STATE, parsed, {
          profile: Object.assign({}, DEFAULT_STATE.profile, parsed.profile || {}),
          ratings: Object.assign({}, DEFAULT_STATE.ratings, parsed.ratings || {}),
          answersByMode: Object.assign({}, DEFAULT_STATE.answersByMode, parsed.answersByMode || {}),
          recentModes: parsed.recentModes || [],
          eloHistory: parsed.eloHistory || [],
          items: parsed.items || {},
          mistakesQueue: parsed.mistakesQueue || []
        });
        return merged;
      }

      // Check for legacy v1 save to migrate
      const legacyRaw = window.localStorage.getItem(LEGACY_V1_KEY);
      if (legacyRaw) {
        try {
          const v1Data = JSON.parse(legacyRaw);
          const migrated = migrateV1ToV2(v1Data);
          saveState(migrated);
          // Clean up legacy key
          try { window.localStorage.removeItem(LEGACY_V1_KEY); } catch (e) { }
          return migrated;
        } catch (e) {
          console.warn('Migration failed, starting fresh v2 state:', e);
        }
      }

      // Fresh default state
      const fresh = JSON.parse(JSON.stringify(DEFAULT_STATE));
      saveState(fresh);
      return fresh;
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
        window.localStorage.removeItem(LEGACY_V1_KEY);
      } catch (e) { }
    }
    memoryFallback = null;
    return loadState();
  }

  function exportState(state) {
    const jsonStr = JSON.stringify(state, null, 2);
    const blob = new Blob([jsonStr], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    const dateStr = new Date().toISOString().split('T')[0];
    a.href = url;
    a.download = `c2_english_arcade_save_${dateStr}.json`;
    document.body.appendChild(a);
    a.click();
    setTimeout(() => {
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    }, 100);
  }

  function validateAndImport(jsonString) {
    try {
      const parsed = JSON.parse(jsonString);
      if (!parsed || typeof parsed !== 'object') {
        throw new Error('Invalid JSON format');
      }

      let validState;
      if (parsed.version === 2 && parsed.ratings && parsed.profile) {
        validState = Object.assign({}, DEFAULT_STATE, parsed);
      } else if (parsed.version === 1 || parsed.adaptiveLevels) {
        validState = migrateV1ToV2(parsed);
      } else if (parsed.ratings) {
        validState = Object.assign({}, DEFAULT_STATE, parsed, { version: 2 });
      } else {
        throw new Error('Unrecognized save file schema');
      }

      saveState(validState);
      return { success: true, state: validState };
    } catch (err) {
      return { success: false, error: err.message };
    }
  }

  window.C2Storage = {
    loadState: loadState,
    saveState: saveState,
    resetProgress: resetProgress,
    exportState: exportState,
    validateAndImport: validateAndImport,
    DEFAULT_STATE: DEFAULT_STATE
  };
})();
