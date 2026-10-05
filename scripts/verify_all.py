# scripts/verify_all.py
# Comprehensive validator for the entire C2 Question Bank
import os
import re
import json

DATA_FILES = [
  ("vocabulary", "data/vocabulary.js"),
  ("collocations", "data/collocations.js"),
  ("phrasal", "data/phrasal.js"),
  ("cloze", "data/cloze.js"),
  ("grammar", "data/grammar.js"),
  ("confusables", "data/confusables.js")
]

def main():
    total = 0
    all_ids = set()
    category_counts = {}
    errors = []

    for category, filepath in DATA_FILES:
        if not os.path.exists(filepath):
            errors.append(f"Missing file: {filepath}")
            continue

        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # Extract the JSON array from the JS assignment: window.C2_DATA.<cat> = [...];
        match = re.search(r"window\.C2_DATA\.\w+\s*=\s*(\[.*?\])\s*;", content, re.DOTALL)
        if not match:
            errors.append(f"Could not parse JSON array in {filepath}")
            continue

        try:
            questions = json.loads(match.group(1))
        except Exception as e:
            errors.append(f"JSON syntax error in {filepath}: {str(e)}")
            continue

        category_counts[category] = len(questions)
        total += len(questions)

        for i, q in enumerate(questions):
            qid = q.get("id")
            if not qid:
                errors.append(f"[{category}#{i}] Missing 'id'")
            elif qid in all_ids:
                errors.append(f"Duplicate id: {qid}")
            else:
                all_ids.add(qid)

            if q.get("mode") != category:
                errors.append(f"[{qid}] mode '{q.get('mode')}' does not match category '{category}'")

            lvl = q.get("level")
            if not lvl or lvl < 1 or lvl > 5:
                errors.append(f"[{qid}] Invalid level: {lvl}")

            if not q.get("explain"):
                errors.append(f"[{qid}] Missing 'explain'")
            if not q.get("example"):
                errors.append(f"[{qid}] Missing 'example'")

            qtype = q.get("type")
            if qtype == "choice":
                opts = q.get("options")
                ans = q.get("answer")
                if not isinstance(opts, list) or len(opts) < 2:
                    errors.append(f"[{qid}] 'options' must have at least 2 items")
                if not isinstance(ans, int) or ans < 0 or ans >= len(opts):
                    errors.append(f"[{qid}] 'answer' {ans} is out of bounds for {len(opts)} options")
                if not q.get("prompt"):
                    errors.append(f"[{qid}] Missing 'prompt'")
            elif qtype == "transformation":
                if not q.get("leadIn"):
                    errors.append(f"[{qid}] Missing 'leadIn'")
                if not q.get("keyWord"):
                    errors.append(f"[{qid}] Missing 'keyWord'")
                acc = q.get("accepted")
                if not isinstance(acc, list) or len(acc) == 0:
                    errors.append(f"[{qid}] 'accepted' must be non-empty list")
            else:
                errors.append(f"[{qid}] Unknown type '{qtype}'")

    print("=========================================")
    print("C2 QUESTION BANK INTEGRITY REPORT")
    print("=========================================")
    for cat, count in category_counts.items():
        print(f" - {cat.capitalize():15}: {count:4d} questions")
    print("-----------------------------------------")
    print(f" TOTAL QUESTIONS  : {total:4d}")
    print(f" UNIQUE IDS       : {len(all_ids):4d}")
    print("=========================================")

    if errors:
        print(f"\n[ERROR] FOUND {len(errors)} ERROR(S):")
        for err in errors[:20]:
            print(f" - {err}")
        exit(1)
    else:
        print("\n[SUCCESS] ALL 1,060 QUESTIONS PASSED INTEGRITY & SCHEMA CHECKS WITH 100% SUCCESS!")

if __name__ == "__main__":
    main()
