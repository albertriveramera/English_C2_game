# scripts/simulate_elo.py
# Automated mathematical validation of the C2 ELO rating system, rank gating, and variety multiplier

import math
import collections

MODES = ['vocabulary', 'collocations', 'phrasal', 'cloze', 'grammar', 'confusables']

CFG = {
    'DEFAULT_RATING': 1400,
    'BASE_K_PROVISIONAL': 40,
    'BASE_K_CALIBRATED': 28,
    'BASE_K_MASTERED': 20,
    'PROVISIONAL_CUTOFF': 30,
    'CALIBRATED_CUTOFF': 100,
    'HISTORY_WINDOW': 40,
    'VARIETY_MIN_ANSWERS': 10,
    'VARIETY_OVERPLAYED_THRESHOLD': 0.25,
    'VARIETY_UNDERPLAYED_THRESHOLD': 0.10,
    'VARIETY_MAX_PENALTY': 0.50,
    'VARIETY_MAX_BONUS': 1.20,
    'LEVEL_RATINGS': {1: 1100, 2: 1250, 3: 1400, 4: 1550, 5: 1700},
    'TRANSFORMATION_BONUS': 25,
    'HYSTERESIS_BUFFER': 25,
    'RANKS': [
        {'index': 0, 'title': 'C1 Contender', 'badge': '🥉', 'minElo': 1200, 'minCorrect': 0},
        {'index': 1, 'title': 'C1+ Advanced', 'badge': '🥈', 'minElo': 1350, 'minCorrect': 25},
        {'index': 2, 'title': 'Pre-C2 Proficient', 'badge': '🥇', 'minElo': 1500, 'minCorrect': 60},
        {'index': 3, 'title': 'C2 Candidate', 'badge': '💎', 'minElo': 1650, 'minCorrect': 120},
        {'index': 4, 'title': 'C2 Master', 'badge': '👑', 'minElo': 1800, 'minCorrect': 200}
    ]
}

def question_rating(q):
    base = q.get('rating') or CFG['LEVEL_RATINGS'].get(q.get('level', 3), 1400)
    if q.get('type') == 'transformation':
        base += CFG['TRANSFORMATION_BONUS']
    return base

def expected_score(player_r, q_r, q_type):
    diff = (q_r - player_r) / 400.0
    std_exp = 1.0 / (1.0 + math.pow(10, diff))
    if q_type == 'choice':
        c = 0.25
        return min(0.99, max(0.01, c + (1.0 - c) * std_exp))
    return min(0.99, max(0.01, std_exp))

def k_factor(ans_count):
    if ans_count < CFG['PROVISIONAL_CUTOFF']:
        return CFG['BASE_K_PROVISIONAL']
    if ans_count < CFG['CALIBRATED_CUTOFF']:
        return CFG['BASE_K_CALIBRATED']
    return CFG['BASE_K_MASTERED']

def variety_multiplier(recent_modes, current_mode):
    count = len(recent_modes)
    if count < CFG['VARIETY_MIN_ANSWERS']:
        return 1.0, False, False

    mode_count = sum(1 for m in recent_modes if m == current_mode)
    share = mode_count / count

    if share > CFG['VARIETY_OVERPLAYED_THRESHOLD']:
        excess = share - CFG['VARIETY_OVERPLAYED_THRESHOLD']
        penalty_ratio = min(1.0, excess / 0.40)
        mult = max(CFG['VARIETY_MAX_PENALTY'], 1.0 - penalty_ratio * (1.0 - CFG['VARIETY_MAX_PENALTY']))
        return round(mult, 2), False, True

    if share < CFG['VARIETY_UNDERPLAYED_THRESHOLD']:
        deficit = CFG['VARIETY_UNDERPLAYED_THRESHOLD'] - share
        bonus_ratio = min(1.0, deficit / CFG['VARIETY_UNDERPLAYED_THRESHOLD'])
        mult = min(CFG['VARIETY_MAX_BONUS'], 1.0 + bonus_ratio * (CFG['VARIETY_MAX_BONUS'] - 1.0))
        return round(mult, 2), True, False

    return 1.0, False, False

def calculate_delta(player_r, q_r, q_type, was_correct, ans_count, recent_modes, current_mode):
    exp = expected_score(player_r, q_r, q_type)
    k = k_factor(ans_count)
    s = 1.0 if was_correct else 0.0
    raw = k * (s - exp)
    mult, is_bonus, is_penalty = variety_multiplier(recent_modes, current_mode)

    if was_correct:
        final_d = round(raw * mult)
        if final_d < 1:
            final_d = 1
    else:
        final_d = round(raw)
        if final_d > -1:
            final_d = -1
    return final_d, exp, mult

def get_rank(global_elo, total_correct, current_idx):
    active_idx = current_idx
    for i in range(len(CFG['RANKS']) - 1, -1, -1):
        r = CFG['RANKS'][i]
        if global_elo >= r['minElo'] and total_correct >= r['minCorrect']:
            if i > active_idx:
                active_idx = i
            break
    if active_idx > 0:
        cur_r = CFG['RANKS'][active_idx]
        if global_elo < (cur_r['minElo'] - CFG['HYSTERESIS_BUFFER']):
            active_idx -= 1
    return active_idx

def run_simulation():
    print("--- 1. Testing Expected Scores & Delta Mechanics ---")
    p_elo = 1400
    # Q at 1400 (choice) -> std_exp = 0.5, guess floor = 0.25 + 0.75*0.5 = 0.625
    d_win, exp, _ = calculate_delta(p_elo, 1400, 'choice', True, 0, [], 'vocabulary')
    d_loss, _, _ = calculate_delta(p_elo, 1400, 'choice', False, 0, [], 'vocabulary')
    print(f"Player 1400 vs Q 1400 (Choice): Expected={exp:.3f}, Win Delta=+{d_win}, Loss Delta={d_loss}")
    assert d_win > 0, "Win delta must be positive"
    assert d_loss < 0, "Loss delta must be negative"

    # Harder question (1700)
    d_win_hard, exp_hard, _ = calculate_delta(p_elo, 1700, 'choice', True, 0, [], 'vocabulary')
    d_loss_hard, _, _ = calculate_delta(p_elo, 1700, 'choice', False, 0, [], 'vocabulary')
    print(f"Player 1400 vs Q 1700 (Hard): Expected={exp_hard:.3f}, Win Delta=+{d_win_hard}, Loss Delta={d_loss_hard}")
    assert d_win_hard > d_win, "Beating harder question must give greater reward"
    assert abs(d_loss_hard) < abs(d_loss), "Losing to harder question must penalize less"

    print("\n--- 2. Testing Variety Multiplier Under Heavy Grinding ---")
    history = ['vocabulary'] * 35 + ['grammar'] * 5
    mult_vocab, _, is_pen = variety_multiplier(history, 'vocabulary')
    mult_cloze, is_bon, _ = variety_multiplier(history, 'cloze')
    print(f"Vocabulary share: 35/40 (87.5%) -> Multiplier: ×{mult_vocab:.2f} (Penalty: {is_pen})")
    print(f"Cloze share: 0/40 (0%) -> Multiplier: ×{mult_cloze:.2f} (Bonus: {is_bon})")
    assert mult_vocab <= 0.50, "Heavy grinding must reduce multiplier to 0.50x floor"
    assert mult_cloze >= 1.20, "Neglected category must receive 1.20x bonus"

    # Verify that loss delta is NEVER reduced by variety penalty
    d_loss_grind, _, m = calculate_delta(p_elo, 1400, 'choice', False, 0, history, 'vocabulary')
    print(f"Loss while grinding: Delta={d_loss_grind} (Standard Loss={d_loss})")
    assert d_loss_grind == d_loss, "Variety penalty must NEVER reduce losses!"

    print("\n--- 3. Testing Rank Gating & 25-pt Hysteresis Buffer ---")
    # Rank 0: Contender
    r0 = get_rank(1200, 0, 0)
    assert r0 == 0

    # Has 1350 ELO but only 10 correct answers (needs 25) -> Must stay Rank 0!
    r_locked = get_rank(1380, 10, 0)
    print(f"Player 1380 ELO with 10 correct answers (req 25): Rank Index = {r_locked} ({CFG['RANKS'][r_locked]['title']})")
    assert r_locked == 0, "Must be gated by minimum correct answers!"

    # Has 1350 ELO AND 25 correct answers -> Promotes to Rank 1!
    r1 = get_rank(1355, 25, 0)
    print(f"Player 1355 ELO with 25 correct answers: Rank Index = {r1} ({CFG['RANKS'][r1]['title']})")
    assert r1 == 1, "Must promote when both conditions are met"

    # ELO drops slightly from 1350 to 1335 (above demotion threshold 1350 - 25 = 1325) -> Stays Rank 1 (Hysteresis)!
    r_hysteresis = get_rank(1335, 30, 1)
    print(f"Player drops to 1335 ELO (Threshold 1325): Rank Index = {r_hysteresis} (Protected by Hysteresis)")
    assert r_hysteresis == 1, "Hysteresis must protect player from demotion on small drop"

    # ELO drops below 1325 -> Demoted to Rank 0
    r_demote = get_rank(1320, 30, 1)
    print(f"Player drops to 1320 ELO (Below 1325): Rank Index = {r_demote} (Demoted)")
    assert r_demote == 0, "Player must demote when dropping below buffer"

    print("\n[SUCCESS] All ELO simulation and validation tests passed flawlessly!")

if __name__ == "__main__":
    run_simulation()
