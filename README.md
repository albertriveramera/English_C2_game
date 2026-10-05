# C2 English Proficiency Arcade 🎓🎮
> **Adaptive ELO Browser Game for C1-to-C2 English Mastery**

An offline-first, pure JavaScript browser application designed specifically to bridge the demanding gap between **CEFR C1 (Advanced)** and **CEFR C2 (Mastery)**.

---

## 📖 Context & Genesis of the Project

This project was conceived through an interactive pair-programming journey with a learner standing firmly at a C1 level who sought an engaging, game-like platform to acquire true C2 fluency without running into superficial multiple-choice trivia or repetitive filler.

### Key Milestones in Development:
1. **Initial Concept**: A streamlined browser game with 6 distinct C2 categories, spaced repetition (Leitner 5-box system), and Cambridge-style Key Word Transformations.
2. **Bank Expansion to 1,000+ Items**: Recognizing that small question banks (~30 per category) fail to impart the immense lexical breadth required for C2, the question bank was expanded and meticulously authored to reach **1,005 authentic, unique questions** across 6 categories.
3. **Quality & Option Audit**: An automated audit pipeline was established to eliminate placeholders, guarantee authentic contextual examples, ensure answer option balance across indices (0, 1, 2, 3), and randomize options dynamically at render time.
4. **Transition from XP to ELO**: Arbitrary experience points (XP) were eliminated. In their place, a mathematically rigorous **ELO rating system** was implemented. Questions hold calibrated difficulty ratings, players possess individual skill ratings across all 6 disciplines, grinding single categories is penalized via a rolling variety multiplier, and progression requires both high ELO ratings and verified lifetime correct answers.

---

## 🌟 Key Features

### 1. 1,005 Curated, Authentic C2 Questions
Distributed across six core language pillars:
- **Erudite Vocabulary (203 questions)**: Abstruse lexis, fine semantic nuances, academic and literary registers (*recondite, insouciance, truculent, equanimity, adroit, specious*).
- **Collocations & Idioms (180 questions)**: Deceptive binomials, fixed prepositional collocations, native-speaker idioms (*curry favor, wreak havoc, broach the subject, stem the tide, whet one's appetite*).
- **Nuanced Phrasal Verbs (150 questions)**: Multi-word verbs with abstract meanings (*stave off, flesh out, shore up, zero in on, gloss over, hammer out*).
- **Use of English & Cloze / Key Word Transformations (189 questions)**: Authentic Cambridge C2 Proficiency (CPE) Reading & Use of English Part 4 format. Gaps must be completed in 3 to 8 words using an invariant key word.
- **Grammar & Inversion (148 questions)**: Negative adverbial fronting (*scarcely, no sooner, under no circumstances*), mandative and formulaic subjunctives (*suffice it to say, come what may, lest*), mixed conditionals, and cleft sentences.
- **Confusables & Nuance (135 questions)**: Fine lexical pairs (*complaisant vs complacent, ingenuous vs ingenious, continuous vs continual, presumptive vs presumptuous, venal vs venial, flounder vs founder*).

### 2. Rigorous ELO Rating Architecture
- **Question Ratings**: Calibrated by difficulty tier:
  - Level 1: `1100 ELO`
  - Level 2: `1250 ELO`
  - Level 3: `1400 ELO`
  - Level 4: `1550 ELO`
  - Level 5: `1700 ELO`
  - Open Key Word Transformations receive a `+25 ELO` challenge offset.
- **Guess-Floor Adjusted Expected Score**:
  $$\text{Expected}_{\text{choice}} = c + (1 - c) \cdot \frac{1}{1 + 10^{(R_q - R_p)/400}}$$
  where $c = 0.25$ accounts for the 4-choice random guess probability. For open transformations, $c = 0$.
- **Dynamic K-Factor**:
  - *Provisional* ($<30$ answers in mode): $K = 40$
  - *Calibrated* ($30-99$ answers in mode): $K = 28$
  - *Mastered* ($\ge 100$ answers in mode): $K = 20$
- **Anti-Grinding Variety Multiplier**:
  - A rolling FIFO history of the player's last 40 answered categories is tracked.
  - If a category is **overplayed** ($>25\%$ share of the last 40), its ELO gain multiplier decays smoothly down to **$0.50\times$**.
  - If a category is **neglected** ($<10\%$ share of the last 40), its ELO gain multiplier increases up to **$1.20\times$** as an incentive.
  - **Asymmetric Rule**: Variety penalties apply *strictly to ELO gains (wins)*; losses are **never reduced**, preventing players from gaming the system by repeatedly losing in penalized modes.
- **Global ELO & Gated Proficiency Ranks**:
  - **Global ELO** is calculated as the unweighted mean of all 6 category ratings:
    $$\text{Global ELO} = \text{round}\left(\frac{1}{6} \sum_{c \in \text{Modes}} R_c\right)$$
  - Ranks require **both** reaching the Global ELO threshold and achieving a minimum number of lifetime correct answers:
    - 🥉 **C1 Contender**: $\ge 1200\text{ ELO} \;\&\; 0\text{ correct}$
    - 🥈 **C1+ Advanced**: $\ge 1350\text{ ELO} \;\&\; 25\text{ correct}$
    - 🥇 **Pre-C2 Proficient**: $\ge 1500\text{ ELO} \;\&\; 60\text{ correct}$
    - 💎 **C2 Candidate**: $\ge 1650\text{ ELO} \;\&\; 120\text{ correct}$
    - 👑 **C2 Master**: $\ge 1800\text{ ELO} \;\&\; 200\text{ correct}$
  - **25-Point Hysteresis Buffer**: To prevent rank oscillation on border scores, a player is only demoted if their Global ELO drops more than 25 points below the rank threshold.

### 3. Adaptive Question Selection
When generating sessions, questions are sampled using a Gaussian weighting kernel centered around the player's current category rating ($\sigma = 180\text{ ELO}$), ensuring the player is consistently presented with questions in their "Zone of Proximal Development".

### 4. Pedagogical Depth & Manual Override
- Every question displays an explanatory breakdown and an authentic, natural C2 sentence illustrating correct collocation and register.
- For Key Word Transformations, if the player inputs an idiomatic phrasing not listed in the default dictionary, a **"✓ My answer is also valid (Mark as Correct)"** button allows the user to override the result. This undoes the mistake penalty, awards the full win delta, removes the item from the mistakes queue, and updates Leitner SRS history immediately.

### 5. Spaced Repetition (Leitner 5-Box SRS)
- Boxes 1 through 5 schedule reviews across expanding intervals (1 day, 3 days, 7 days, 14 days, 30 days).
- Missed questions are added to the **Mistakes Redemption Queue** for targeted remediation.

---

## 🚀 How to Run

**Zero installation, build steps, or package managers required.**

1. Simply open `index.html` in any modern web browser (Google Chrome, Microsoft Edge, Mozilla Firefox, Safari).
2. Works 100% offline via the `file://` protocol.
3. All progress is saved automatically to the browser's `localStorage`.
4. Audio effects use the native Web Audio API (no external MP3/WAV files required).

---

## 📁 Repository Structure

```text
English_C2_game/
├── index.html                   # Master single-page application structure
├── README.md                    # Project documentation and architectural overview
│
├── css/
│   └── styles.css               # Luxury dark glassmorphism design system & micro-animations
│
├── js/
│   ├── elo.js                   # ELO calculation, variety multiplier, and rank gating engine
│   ├── storage.js               # State persistence, v1 -> v2 schema migration, reset utilities
│   ├── engine.js                # ELO-weighted session sampling and answer normalization
│   ├── srs.js                   # Leitner 5-box spaced repetition system logic
│   ├── ui.js                    # Web Audio synth, canvas confetti, header pills & modal analytics
│   └── app.js                   # Master application controller and session loop
│
├── data/
│   ├── vocabulary.js            # 203 curated C2 vocabulary items
│   ├── collocations.js          # 180 curated C2 collocations and idioms
│   ├── phrasal.js               # 150 curated C2 phrasal verbs
│   ├── cloze.js                 # 189 curated C2 cloze & Key Word Transformations
│   ├── grammar.js               # 148 curated C2 grammar & inversion questions
│   └── confusables.js           # 135 curated C2 confusables & fine semantic shifts
│
└── scripts/
    ├── audit_bank.py            # Quality auditor (validates uniqueness, examples, options, syntax)
    ├── simulate_elo.py          # Mathematical test suite for ELO, variety penalties, and rank gating
    ├── test_browser_render.py   # Headless browser validation verifying DOM rendering and JS execution
    └── generate_complete_clean_bank.py # Master bank generation pipeline
```

---

## 🧪 Validation & Test Commands

You can execute the automated quality and math verification test suites using Python:

```bash
# 1. Audit question bank uniqueness, schemas, and pedagogical examples (1,005 items)
python scripts/audit_bank.py

# 2. Mathematically simulate ELO curves, variety decay, and hysteresis demotion
python scripts/simulate_elo.py

# 3. Verify headless browser rendering and JavaScript execution via Edge
python scripts/test_browser_render.py
```

---

## 🎓 CEFR C2 Standard Alignment

This game targets the competencies defined by the **Common European Framework of Reference for Languages (CEFR) Level C2**:
- *Can understand with ease virtually everything heard or read.*
- *Can summarize information from different spoken and written sources, reconstructing arguments and accounts in a coherent presentation.*
- *Can express him/herself spontaneously, very fluently and precisely, differentiating finer shades of meaning even in more complex situations.*
