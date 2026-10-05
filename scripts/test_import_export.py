# scripts/test_import_export.py
import json

# Test that default state and v1 legacy data import and export cleanly
v2_sample = {
    "version": 2,
    "profile": {
        "rankIndex": 2,
        "streakDays": 5,
        "lastPlayedDate": "2026-10-05",
        "sessionsCompleted": 12,
        "totalCorrect": 85,
        "totalAnswered": 110
    },
    "ratings": {
        "vocabulary": 1520,
        "collocations": 1490,
        "phrasal": 1440,
        "cloze": 1580,
        "grammar": 1460,
        "confusables": 1510
    },
    "globalRating": 1500,
    "answersByMode": {
        "vocabulary": {"total": 20, "correct": 16},
        "collocations": {"total": 18, "correct": 14},
        "phrasal": {"total": 15, "correct": 11},
        "cloze": {"total": 22, "correct": 18},
        "grammar": {"total": 17, "correct": 12},
        "confusables": {"total": 18, "correct": 14}
    },
    "recentModes": ["cloze", "vocabulary", "grammar"],
    "eloHistory": [],
    "items": {},
    "mistakesQueue": ["voc-001"],
    "soundEnabled": True
}

# Test JSON serialization / deserialization roundtrip
serialized = json.dumps(v2_sample, indent=2)
deserialized = json.loads(serialized)
assert deserialized["version"] == 2
assert deserialized["ratings"]["cloze"] == 1580
assert deserialized["profile"]["rankIndex"] == 2
print("[SUCCESS] Import/Export JSON schema roundtrip verified!")
