// Leitner Spaced Repetition System (SRS) for C2 English Arcade
(function () {
  'use strict';

  // Intervals in milliseconds:
  // Box 1: 0 (due immediately / same session)
  // Box 2: 1 day
  // Box 3: 3 days
  // Box 4: 7 days
  // Box 5: 21 days (Mastered)
  const INTERVALS = {
    1: 0,
    2: 1 * 24 * 60 * 60 * 1000,
    3: 3 * 24 * 60 * 60 * 1000,
    4: 7 * 24 * 60 * 60 * 1000,
    5: 21 * 24 * 60 * 60 * 1000
  };

  function recordResult(state, questionId, isCorrect) {
    const now = Date.now();
    let item = state.items[questionId];

    if (!item) {
      item = {
        box: 1,
        timesCorrect: 0,
        timesWrong: 0,
        lastSeen: now,
        nextReview: now
      };
    }

    item.lastSeen = now;

    if (isCorrect) {
      item.timesCorrect = (item.timesCorrect || 0) + 1;
      // Advance box up to 5
      const currentBox = item.box || 1;
      item.box = Math.min(5, currentBox + 1);
      item.nextReview = now + (INTERVALS[item.box] || INTERVALS[5]);

      // If in mistakesQueue, remove it
      const mistakeIdx = state.mistakesQueue.indexOf(questionId);
      if (mistakeIdx !== -1) {
        state.mistakesQueue.splice(mistakeIdx, 1);
      }
    } else {
      item.timesWrong = (item.timesWrong || 0) + 1;
      // Demote to box 1
      item.box = 1;
      item.nextReview = now; // due right away

      // Add to mistakes queue if not already there
      if (!state.mistakesQueue.includes(questionId)) {
        state.mistakesQueue.push(questionId);
      }
    }

    state.items[questionId] = item;
    return item;
  }

  function getDueQuestionIds(state) {
    const now = Date.now();
    const due = [];
    for (const [id, item] of Object.entries(state.items || {})) {
      if (item.nextReview && item.nextReview <= now && item.box < 5) {
        due.push(id);
      }
    }
    return due;
  }

  function getMasterySummary(allQuestions, state) {
    let unseen = 0;
    let learning = 0; // Box 1 & 2
    let reviewing = 0; // Box 3 & 4
    let mastered = 0; // Box 5

    allQuestions.forEach(q => {
      const record = state.items[q.id];
      if (!record) {
        unseen++;
      } else if (record.box === 5) {
        mastered++;
      } else if (record.box >= 3) {
        reviewing++;
      } else {
        learning++;
      }
    });

    return {
      total: allQuestions.length,
      unseen: unseen,
      learning: learning,
      reviewing: reviewing,
      mastered: mastered,
      masteryPercent: allQuestions.length > 0 ? Math.round((mastered / allQuestions.length) * 100) : 0
    };
  }

  window.C2SRS = {
    recordResult: recordResult,
    getDueQuestionIds: getDueQuestionIds,
    getMasterySummary: getMasterySummary,
    INTERVALS: INTERVALS
  };
})();
