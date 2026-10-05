# scripts/audit_bank.py
# Strict quality and integrity auditor for C2 English Arcade Question Banks
import os
import re
import json
import collections

DATA_FILES = [
    ("vocabulary", "data/vocabulary.js"),
    ("collocations", "data/collocations.js"),
    ("phrasal", "data/phrasal.js"),
    ("cloze", "data/cloze.js"),
    ("grammar", "data/grammar.js"),
    ("confusables", "data/confusables.js")
]

def normalize_text(t):
    if not t:
        return ""
    t = t.lower().strip()
    t = re.sub(r"[’']", "'", t)
    t = re.sub(r"[^a-z0-9 ]", " ", t)
    return re.sub(r"\s+", " ", t).strip()

def audit():
    total_questions = 0
    errors = []
    warnings = []
    all_ids = set()
    all_prompts = {}
    level_counts = collections.Counter()
    answer_positions = collections.Counter()
    category_counts = {}

    for mode, filepath in DATA_FILES:
        if not os.path.exists(filepath):
            errors.append(f"Missing file: {filepath}")
            continue

        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        match = re.search(r"window\.C2_DATA\.\w+\s*=\s*(\[.*?\])\s*;", content, re.DOTALL)
        if not match:
            errors.append(f"Cannot parse JSON in {filepath}")
            continue

        try:
            questions = json.loads(match.group(1))
        except Exception as e:
            errors.append(f"JSON syntax error in {filepath}: {e}")
            continue

        category_counts[mode] = len(questions)
        total_questions += len(questions)

        for i, q in enumerate(questions):
            qid = q.get("id")
            if not qid:
                errors.append(f"[{mode}#{i}] Missing 'id'")
            elif qid in all_ids:
                errors.append(f"Duplicate ID '{qid}' found in {mode}")
            else:
                all_ids.add(qid)

            if q.get("mode") != mode:
                errors.append(f"[{qid}] mode '{q.get('mode')}' does not match file category '{mode}'")

            lvl = q.get("level")
            if not lvl or lvl < 1 or lvl > 5:
                errors.append(f"[{qid}] Invalid level {lvl}")
            else:
                level_counts[lvl] += 1

            # Prompt check & prompt deduplication
            raw_prompt = q.get("prompt") or q.get("leadIn") or ""
            norm_prompt = normalize_text(raw_prompt)
            if not norm_prompt:
                errors.append(f"[{qid}] Empty prompt / leadIn")
            elif norm_prompt in all_prompts:
                errors.append(f"Duplicate prompt content between '{qid}' and '{all_prompts[norm_prompt]}' in {mode}")
            else:
                all_prompts[norm_prompt] = qid

            # Pedagogical Explanation
            explain = q.get("explain", "")
            if not explain or len(explain.strip()) < 15:
                errors.append(f"[{qid}] Explanation missing or too short: '{explain}'")

            # Authentic Example Sentence check
            ex = q.get("example", "")
            if not ex or len(ex.strip()) < 20:
                errors.append(f"[{qid}] Example missing or too short: '{ex}'")
            elif "________" in ex:
                errors.append(f"[{qid}] Example contains unresolved placeholder blanks: '{ex}'")
            elif ex.startswith("Context:") or ex.startswith("Correct usage:") or ex.startswith("Correct syntax:"):
                errors.append(f"[{qid}] Example has lazy placeholder prefix: '{ex}'")

            # Type specific checks
            qtype = q.get("type")
            if qtype == "choice":
                opts = q.get("options")
                ans = q.get("answer")
                if not isinstance(opts, list) or len(opts) < 2:
                    errors.append(f"[{qid}] 'options' must be a list of at least 2 items")
                else:
                    norm_opts = [normalize_text(o) for o in opts]
                    if len(set(norm_opts)) < len(opts):
                        errors.append(f"[{qid}] Duplicate options detected in {opts}")
                if not isinstance(ans, int) or ans < 0 or ans >= len(opts):
                    errors.append(f"[{qid}] Answer index {ans} out of bounds for options")
                else:
                    answer_positions[ans] += 1

            elif qtype == "transformation":
                if not q.get("leadIn"):
                    errors.append(f"[{qid}] Missing 'leadIn'")
                if not q.get("keyWord"):
                    errors.append(f"[{qid}] Missing 'keyWord'")
                acc = q.get("accepted")
                if not isinstance(acc, list) or len(acc) < 1:
                    errors.append(f"[{qid}] 'accepted' must be non-empty list of solutions")
                elif len(acc) < 2:
                    warnings.append(f"[{qid}] Transformation has only 1 accepted variant; recommend at least 2.")
            else:
                errors.append(f"[{qid}] Unknown question type '{qtype}'")

    print("==================================================")
    print("      C2 QUESTION BANK AUDIT REPORT")
    print("==================================================")
    for cat, count in category_counts.items():
        print(f"  {cat.capitalize():16} : {count:4d} questions")
    print("--------------------------------------------------")
    print(f"  TOTAL QUESTIONS  : {total_questions:4d}")
    print(f"  UNIQUE PROMPTS   : {len(all_prompts):4d}")
    print(f"  LEVELS           : {dict(sorted(level_counts.items()))}")
    print(f"  ANSWER POSITIONS : {dict(sorted(answer_positions.items()))}")
    print("==================================================")

    if warnings:
        print(f"\n[WARNINGS] ({len(warnings)}):")
        for w in warnings[:10]:
            print(f"  ! {w}")

    if errors:
        print(f"\n[ERRORS] ({len(errors)} found):")
        for e in errors[:30]:
            print(f"  * {e}")
        if len(errors) > 30:
            print(f"  ... and {len(errors) - 30} more errors.")
        return False
    else:
        print("\n[SUCCESS] Bank passed all quality, uniqueness, and schema checks!")
        return True

if __name__ == "__main__":
    success = audit()
    exit(0 if success else 1)
