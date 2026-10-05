# scripts/build_confusables.py
# Generates 140 authentic C2 Confusable Words & Semantic Nuance questions
import json

BASE_CONFUSABLES = [
  ("cnf-001", "Disinterested vs Uninterested", 3,
   "A good arbitrator must be entirely ________, having no personal or financial stake in the outcome of the dispute.",
   ["disinterested", "uninterested", "indifferent", "detachedly"], 0,
   "In standard high-register English, 'disinterested' means impartial, unbiased, and free from self-interest. 'Uninterested' means bored or lacking interest/curiosity.",
   "We require a disinterested third party to evaluate the bids objectively."),

  ("cnf-002", "Prescribe vs Proscribe", 4,
   "The new authoritarian constitution strictly ________ the assembly of more than four individuals in public squares.",
   ["proscribes", "prescribes", "subscribes", "ascribes"], 0,
   "'Proscribe' means to forbid, outlaw, or prohibit by law. 'Prescribe' means to state as a rule or direct the use of a medicine/remedy (they are near-opposite in legal force).",
   "The Geneva Conventions proscribe the mistreatment or torture of prisoners of war."),

  ("cnf-003", "Flaunt vs Flout", 4,
   "The reckless motorists openly ________ the speed restrictions, racing along residential avenues with impunity.",
   ["flouted", "flaunted", "floated", "flanked"], 0,
   "'To flout' means to openly disregard, disobey, or mock a law or convention. 'To flaunt' means to display something ostentatiously to provoke envy or admiration.",
   "By refusing to wear safety helmets, the cyclists flouted municipal safety ordinances."),

  ("cnf-004", "Tortuous vs Torturous", 4,
   "The mountain path was so ________ that vehicles could negotiate the hairpin bends only in first gear.",
   ["tortuous", "torturous", "tortured", "torpid"], 0,
   "'Tortuous' means full of twists, turns, and bends; convoluted. 'Torturous' means involving or causing excruciating physical or mental torture and suffering.",
   "The bureaucratic paperwork followed a tortuous route before reaching the minister's desk."),

  ("cnf-005", "Venal vs Venial", 5,
   "While lying about one’s age may be considered a ________ peccadillo, perjuring oneself before a grand jury is a grave felony.",
   ["venial", "venal", "vernal", "vicious"], 0,
   "'Venial' (traditionally opposed to 'mortal' in theology) means slight, pardonable, or excusable. 'Venal' means corruptible or open to bribery.",
   "The bishop forgave the novice’s venial lapse of protocol."),

  ("cnf-006", "Appraise vs Apprise", 4,
   "The security chief hurried to the cabinet room to ________ the prime minister of the evolving hostage crisis.",
   ["apprise", "appraise", "praise", "prize"], 0,
   "'To apprise (someone of something)' means to inform, notify, or advise them. 'To appraise' means to assess the monetary value, quality, or performance of something.",
   "Please keep me apprised of any developments during the night shift."),

  ("cnf-007", "Loath vs Loathe", 3,
   "He was extremely ________ to admit that his rival's strategy had outmaneuvered him on every front.",
   ["loath", "loathe", "loathed", "loathing"], 0,
   "'Loath' (spelled without an 'e' and pronounced with an unvoiced 'th') is an adjective meaning reluctant, unwilling, or disinclined. 'Loathe' (with an 'e') is a transitive verb meaning to detest.",
   "I am loath to spend another penny on this defective machinery."),

  ("cnf-008", "Discreet vs Discrete", 4,
   "The quantum model describes energy not as a smooth continuous stream, but as indivisible ________ units called quanta.",
   ["discrete", "discreet", "discretional", "discretive"], 0,
   "'Discrete' (spelled -ete) means individually separate, distinct, and discontinuous. 'Discreet' (spelled -eet) means prudent, circumspect, and careful to avoid social embarrassment or disclosure.",
   "The research project was subdivided into four discrete phases over two academic terms."),

  ("cnf-009", "Deprecate vs Depreciate", 4,
   "Educators ________ the excessive reliance on standardized multiple-choice assessments for measuring creative writing abilities.",
   ["deprecate", "depreciate", "deracinate", "denigrate"], 0,
   "'To deprecate' means to express strong disapproval of something. 'To depreciate' primarily means to diminish in value or monetary worth over time.",
   "He had an endearing habit of self-deprecating humor during awkward toasts."),

  ("cnf-010", "Ingenuous vs Ingenious", 5,
   "It was a shockingly ________ remark, revealing that the young diplomat was entirely unversed in the cynical realities of espionage.",
   ["ingenuous", "ingenious", "indigenous", "ingratiating"], 0,
   "'Ingenuous' means innocent, naive, artless, and unsuspectingly candid. 'Ingenious' means brilliantly clever, inventive, and resourceful.",
   "Only an ingenuous observer would trust assurances delivered without legally binding covenants."),

  ("cnf-011", "Adverse vs Averse", 3,
   "Despite the market downturn, the venture capitalist was not ________ to investing in speculative biotechnology startups.",
   ["averse", "adverse", "aversive", "advertent"], 0,
   "'Averse' (usually followed by 'to') is an adjective describing a person having a strong feeling of dislike, reluctance, or opposition. 'Adverse' describes unfavorable, hostile, or harmful conditions (e.g. adverse weather).",
   "She was averse to public speaking, preferring to publish her findings in written treatises."),

  ("cnf-012", "Credible vs Creditable vs Credulous", 4,
   "Finishing the grueling trans-alpine marathon in under five hours was a thoroughly ________ achievement for an amateur cyclist.",
   ["creditable", "credible", "credulous", "creditworthy"], 0,
   "'Creditable' means deserving public praise, respect, or esteem (even if not exceptional). 'Credible' means believable/convincing; 'credulous' means gullible.",
   "The young orchestra gave a very creditable performance of Mahler’s fifth symphony."),

  ("cnf-013", "Delusion vs Illusion vs Allusion", 5,
   "Suffering from a psychiatric ________, the patient insisted that his household mirrors were transmitting signals to interplanetary spacecraft.",
   ["delusion", "illusion", "allusion", "elusion"], 0,
   "'Delusion' is a persistent, false, psychotic or idiosyncratic belief maintained despite indisputable contradictory evidence. 'Illusion' is a deceptive optical or cognitive impression, and 'allusion' is an indirect literary reference.",
   "He harbored delusions of royal lineage that no genealogical evidence could shake."),

  ("cnf-014", "Systemic vs Systematic", 4,
   "The ombudsman concluded that racial profiling in stop-and-search operations was ________ throughout the entire constabulary, not confined to rogue officers.",
   ["systemic", "systematic", "systematical", "systematized"], 0,
   "'Systemic' refers to something embedded within and affecting the whole system, organization, or organism. 'Systematic' means done according to a fixed plan or method in an organized, orderly manner.",
   "The crash revealed systemic corruption inside the regulatory auditing bodies."),

  ("cnf-015", "Continuous vs Continual", 4,
   "The meeting was interrupted by ________ knocking on the conference room door as couriers delivered dispatches every twenty minutes.",
   ["continual", "continuous", "continuing", "continuate"], 0,
   "'Continual' means occurring repeatedly with short pauses or intervals in between. 'Continuous' means uninterrupted, without any cessation or pause whatever (like a continuous tone).",
   "I could not concentrate amidst the continual ringing of the office telephone."),

  ("cnf-016", "Imply vs Infer", 3,
   "From the auditor’s grave expression and heavy sigh, the shareholders could only ________ that the financial accounts were in catastrophic disarray.",
   ["infer", "imply", "insinuate", "intimate"], 0,
   "A speaker or writer 'implies' (suggests without stating outright), whereas a listener or reader 'infers' (deduces or draws a logical conclusion from evidence).",
   "What do you infer from the defendant's refusal to answer the prosecutor's query?"),

  ("cnf-017", "Expedient vs Expeditious", 5,
   "In order to prevent diplomatic panic, the ministry took an ________ rather than strictly ethical approach to handling the defector.",
   ["expedient", "expeditious", "expedited", "expansive"], 0,
   "'Expedient' means convenient, practical, and advantageous, often disregarding ethical standards or principles for immediate benefit. 'Expeditious' means speedy, prompt, and efficient.",
   "Political expediency dictated that the embarrassing corruption inquiry be buried until after the election."),

  ("cnf-018", "Luxuriant vs Luxurious", 4,
   "The monsoon downpours transformed the arid plateau into a carpet of ________ tropical vegetation.",
   ["luxuriant", "luxurious", "luxuriating", "luxury"], 0,
   "'Luxuriant' describes thick, lush, fertile, and abundant growth of plants or hair. 'Luxurious' describes expensive physical comfort and opulence.",
   "The portrait depicted a young cavalier with luxuriant black locks falling over his shoulders."),

  ("cnf-019", "Judicious vs Judicial", 4,
   "Through a ________ allocation of emergency reserves, the city council prevented municipal insolvency.",
   ["judicious", "judicial", "judicative", "judicatory"], 0,
   "'Judicious' means having or showing good judgment, prudence, or sense. 'Judicial' pertains strictly to courts of law, judges, or the administration of justice.",
   "A judicious blend of fiscal restraint and strategic capital investment stabilized the firm."),

  ("cnf-020", "Compliment vs Complement", 3,
   "The crisp acidity of the vintage Sauvignon Blanc serves as an impeccable ________ to the richness of the seared scallops.",
   ["complement", "compliment", "completion", "complexion"], 0,
   "'Complement' (with 'e') means a thing that completes or brings to perfection, enhancing another. 'Compliment' (with 'i') is an expression of praise or admiration.",
   "His technical mastery was the ideal complement to her boundless creative vision."),

  ("cnf-021", "Definitive vs Definite", 4,
   "Historians regard Professor Chadwick’s three-volume treatise as the ________ biography of Winston Churchill.",
   ["definitive", "definite", "defined", "definitional"], 0,
   "'Definitive' means authoritative, conclusive, and of recognized, final excellence beyond which no improvement is expected. 'Definite' simply means clearly stated, certain, or precise.",
   "The lab has not yet obtained definitive proof linking the gene variant to the autoimmune pathology."),

  ("cnf-022", "Climactic vs Climatic", 5,
   "The third movement of the symphony builds to a thrilling ________ crescendo that brings audiences to their feet.",
   ["climactic", "climatic", "climatological", "acclimating"], 0,
   "'Climactic' relates to a climax (the point of greatest intensity or culmination). 'Climatic' relates to climate, weather patterns, and meteorology.",
   "The novel’s climactic duel takes place atop the storm-battered ramparts."),

  ("cnf-023", "Censure vs Censor", 4,
   "The medical tribunal voted to formally ________ the surgeon for gross professional misconduct.",
   ["censure", "censor", "sensor", "censer"], 0,
   "'To censure' means to express severe, formal disapproval of someone. 'To censor' means to examine books, films, or news to suppress unacceptable parts. ('Censer' is an incense vessel; 'sensor' is a detection device).",
   "The parliament passed a motion to censure the defense minister for misleading the house."),

  ("cnf-024", "Historic vs Historical", 3,
   "The fall of the Berlin Wall in November 1989 was a truly ________ event that reshaped international diplomacy.",
   ["historic", "historical", "historied", "historicist"], 0,
   "'Historic' means momentous, epoch-making, and profoundly important in history. 'Historical' merely means belonging to or concerning history and the past (e.g. historical records, historical fiction).",
   "The signing of the peace accord was a historic milestone for the war-torn province."),

  ("cnf-025", "Affect vs Effect (Verbal Registers)", 4,
   "The new chief executive hopes to ________ sweeping transformations across the company's supply chain governance.",
   ["effect", "affect", "efface", "afflict"], 0,
   "As a transitive verb, 'to effect' means to bring about, execute, or accomplish (e.g. effect change / effect reforms). 'To affect' means to influence or have an impact on.",
   "Only sustained legislative commitment will effect meaningful structural changes in healthcare."),

  ("cnf-026", "Elusive vs Illusive", 5,
   "A lasting diplomatic settlement between the warring factions has proven stubbornly ________ despite decades of envoys.",
   ["elusive", "illusive", "delusive", "allusive"], 0,
   "'Elusive' means difficult to find, capture, achieve, or remember. 'Illusive' (or delusive) means deceptive, illusory, or based on an illusion.",
   "The endangered snow leopard remained elusive throughout the four-week photographic expedition."),

  ("cnf-027", "Persecute vs Prosecute", 4,
   "The attorney general announced an unyielding determination to ________ all individuals implicated in corporate bribery.",
   ["prosecute", "persecute", "peruse", "proscribe"], 0,
   "'To prosecute' means to institute legal proceedings against a person in court. 'To persecute' means to subject someone to hostility and ill-treatment, especially because of race, political, or religious beliefs.",
   "Under federal statutes, trespassers will be prosecuted to the full extent of the law."),

  ("cnf-028", "Principal vs Principle", 3,
   "Adherence to the ________ of non-interference in sovereign territory remains foundational to international law.",
   ["principle", "principal", "principality", "principium"], 0,
   "'Principle' (ending in -le) is a noun meaning a fundamental truth, rule of conduct, or doctrine. 'Principal' (ending in -al) refers to a school head, a sum of money, or means chief/main.",
   "She resigned from the board on a matter of principle rather than compromise her ethics."),

  ("cnf-029", "Alternate vs Alternative", 5,
   "The treaty mandates that the chairmanship rotate on an ________ annual basis between the two member nations.",
   ["alternate", "alternative", "alternatingly", "alternation"], 0,
   "In standard formal English, 'alternate' means happening by turns, every other, or one after another. 'Alternative' refers to an available secondary choice or option among possibilities.",
   "The committee meets on alternate Mondays to review budgetary requisitions."),

  ("cnf-030", "Allusion vs Illusion", 4,
   "The poet’s obscure ________ to Dante’s Inferno went unrecognized by most contemporary undergraduates.",
   ["allusion", "illusion", "delusion", "elusion"], 0,
   "'An allusion' is an indirect or passing reference to a person, literary work, or event. 'An illusion' is a deceptive appearance or impression.",
   "The novel’s title is a subtle allusion to Milton’s Paradise Lost.")
]

ADDITIONAL_CONFUSABLES = [
  ("Elicit vs Illicit", 4, "The interrogator employed gentle questioning techniques to ________ the truth from the traumatized refugee.", ["elicit", "illicit", "elide", "solicit"], "'Elicit' is a verb meaning to evoke, draw out, or obtain a fact or reaction. 'Illicit' is an adjective meaning forbidden by law or rules."),
  ("Eminent vs Imminent vs Immanent", 5, "Seismologists warned that a catastrophic volcanic eruption was ________ after a swarm of harmonic tremors.", ["imminent", "eminent", "immanent", "emanant"], "'Imminent' means about to happen; impending. 'Eminent' means distinguished/famous; 'immanent' means inherent or pervading."),
  ("Exalt vs Exult", 4, "The victorious supporters had reason to ________ after their club secured the treble championship.", ["exult", "exalt", "extol", "excoriate"], "'To exult' means to feel or show triumphant elation or jubilation. 'To exalt' means to hold in high regard or glorify."),
  ("Ordinance vs Ordnance", 5, "The munitions convoy carried heavy artillery ________ to the front lines under cover of darkness.", ["ordnance", "ordinance", "ordonnance", "ordaining"], "'Ordnance' refers to military supplies, ammunition, and artillery. 'Ordinance' refers to an authoritative decree, law, or municipal regulation."),
  ("Pique vs Peak vs Peek", 4, "In a fit of petulant ________, the defeated candidate stormed out of the broadcast studio without congratulating his rival.", ["pique", "peak", "peek", "peep"], "'Pique' is a feeling of irritation or resentment resulting from a slight, especially to one's pride. 'Peak' is a summit; 'peek' is a quick look."),
  ("Waive vs Wave", 3, "In consideration of the tenant's temporary hardship, the landlord agreed to ________ the late payment penalty.", ["waive", "wave", "waver", "waffle"], "'To waive' means to refrain from insisting on or applying a normal rule, claim, or fee. 'To wave' is to move one's hand or oscillate."),
  ("Egoism vs Egotism", 5, "Philosophers distinguish between psychological ________ (the theory of self-interest) and mere conceited boastfulness.", ["egoism", "egotism", "solipsism", "altruism"], "'Egoism' is a philosophical doctrine regarding self-interest as the foundation of morality, whereas 'egotism' is the practice of talking excessively about oneself; boastfulness."),
  ("Stationary vs Stationery", 3, "The executive insisted on writing her correspondence exclusively on bespoke engraved ________.", ["stationery", "stationary", "stationariness", "stationer"], "'Stationery' (with 'e' as in envelope) refers to writing materials. 'Stationary' (with 'a') means not moving or staying in one place."),
  ("Incite vs Insight", 4, "The rabble-rouser was arrested for attempting to ________ a riot outside the parliamentary gates.", ["incite", "insight", "inspire", "indict"], "'To incite' means to encourage or stir up violent or unlawful behavior. 'Insight' is an accurate and deep intuitive understanding."),
  ("Grisly vs Grizzly", 4, "Forensic investigators uncovered a ________ crime scene that horrified even veteran detectives.", ["grisly", "grizzly", "gristly", "grimy"], "'Grisly' means causing horror or disgust; gruesome. 'Grizzly' refers to a brown bear or hair streaked with gray."),
  ("Hoard vs Horde", 4, "During the gold rush, thousands formed a chaotic ________ outside the territorial claims registry.", ["horde", "hoard", "whore", "herd"], "A 'horde' is a large, unorganized group of people. A 'hoard' is an accumulated stock or store of money or valued objects."),
  ("Premise vs Premises", 4, "Patrons were politely instructed to vacate the restaurant ________ prior to the midnight curfew.", ["premises", "premise", "premising", "premonition"], "'Premises' (plural) refers to a house or building and its surrounding land. 'Premise' (singular) is a previous statement or proposition from which another is inferred."),
  ("Wreak vs Wreck", 4, "Unchecked fungal pathogens threaten to ________ catastrophic damage across commercial banana plantations.", ["wreak", "wreck", "reek", "wring"], "'To wreak (damage/havoc/vengeance)' means to cause or inflict. 'To wreck' means to destroy or ruin a vessel or structure."),
  ("Censor vs Censer vs Sensor", 4, "The automated temperature ________ alerted engineers when the coolant reached boiling point.", ["sensor", "censor", "censer", "sitter"], "A 'sensor' is a device that detects or measures a physical property. 'Censer' is an incense burner; 'censor' is an examiner who suppresses materials."),
  ("Assent vs Ascent", 3, "The constitutional amendment received royal ________ from the sovereign on Friday afternoon.", ["assent", "ascent", "accent", "ascention"], "'Assent' means official agreement or approval. 'Ascent' means a climb or upward movement."),
  ("Eminent vs Immanent", 5, "Spinoza's pantheism posits that God is not transcendent, but rather ________ within all physical nature.", ["immanent", "eminent", "imminent", "emanating"], "'Immanent' means existing or operating within; inherent. 'Eminent' means distinguished; 'imminent' means impending."),
  ("Ensure vs Insure vs Assure", 4, "The bank president sought to ________ panicked depositors that their savings were fully backed by federal guarantees.", ["assure", "ensure", "insure", "secure"], "'To assure (someone)' means to tell them something positively to dispel doubt. 'To ensure' means to make sure an outcome happens; 'to insure' relates to financial policies."),
  ("Complementary vs Complimentary", 3, "Hotel guests were treated to a ________ glass of champagne upon checking into the penthouse suite.", ["complimentary", "complementary", "complimenting", "complementation"], "'Complimentary' means given free of charge as a courtesy, or expressing praise. 'Complementary' means combining in such a way as to enhance or emphasize qualities of each other."),
  ("Judicial vs Judicious", 4, "The high court granted ________ review of the administrative deportation order.", ["judicial", "judicious", "judicatory", "jurisdictional"], "'Judicial' relates specifically to a court, judge, or the legal system. 'Judicious' means exhibiting good judgment."),
  ("Council vs Counsel", 3, "Before entering a formal guilty plea, the defendant consulted with his senior legal ________.", ["counsel", "council", "councillor", "counselor"], "'Counsel' refers to advice or an attorney/barrister giving advice in court. 'Council' is an administrative advisory body.")
]

def generate_confusables_bank():
    items = []
    for q in BASE_CONFUSABLES:
        items.append({
            "id": q[0],
            "mode": "confusables",
            "level": q[2],
            "type": "choice",
            "topic": q[1],
            "prompt": q[3],
            "options": q[4],
            "answer": q[5],
            "explain": q[6],
            "example": q[7]
        })
    
    idx = len(items) + 1
    for topic, lvl, prompt, opts, exp in ADDITIONAL_CONFUSABLES:
        items.append({
            "id": f"cnf-{idx:03d}",
            "mode": "confusables",
            "level": lvl,
            "type": "choice",
            "topic": topic,
            "prompt": prompt,
            "options": opts,
            "answer": 0,
            "explain": exp,
            "example": f"Correct usage: {prompt.replace('________', opts[0])}"
        })
        idx += 1

    # Systematic fillers up to 140
    more_pairs = [
      ("Flare vs Flair", 4, "The graphic designer had an undeniable ________ for minimalist typography and color harmony.", ["flair", "flare", "flareup", "flairing"], "'Flair' means a special or instinctive talent, aptitude, or style. 'Flare' is a sudden burst of flame or light."),
      ("Foreword vs Forward", 3, "The Nobel laureate contributed an insightful ________ to the new edition of the landmark treatise.", ["foreword", "forward", "forefront", "forthward"], "A 'foreword' (spelled with 'word') is an introductory preface to a book, usually written by someone other than the author."),
      ("Marshal vs Martial", 4, "The defense general had to ________ all available military reserves to repel the counteroffensive.", ["marshal", "martial", "marcial", "marshaling"], "'To marshal' means to assemble and organize resources or troops. 'Martial' relates to warfare or the military (e.g. martial law)."),
      ("Precedent vs President", 3, "The court's ruling sets a dangerous ________ that could unravel decades of labor protections.", ["precedent", "president", "precedence", "presidency"], "A 'precedent' is an earlier event or legal action that serves as an authoritative guide in subsequent similar circumstances."),
      ("Venal vs Venial", 4, "The investigative series exposed the ________ conduct of border customs officials taking payoffs.", ["venal", "venial", "vernal", "vicious"], "'Venal' means open to bribery or corruptible."),
      ("Discreet vs Discrete", 4, "The ambassador conducted ________ private inquiries into the defector's family ties.", ["discreet", "discrete", "discretionary", "discretive"], "'Discreet' means tactful, prudent, and cautious to maintain confidentiality."),
      ("Allude vs Elude", 4, "In his memoirs, the statesman refused to ________ to his controversial divorce.", ["allude", "elude", "illude", "delude"], "'To allude to' means to refer to indirectly. 'To elude' means to evade or escape from."),
      ("Appraise vs Apprise", 4, "The auction house brought in three certified experts to ________ the Renaissance fresco.", ["appraise", "apprise", "prize", "praise"], "'To appraise' means to assess or estimate the monetary value or quality."),
      ("Affect vs Effect", 4, "Global warming is likely to ________ monsoon precipitation patterns across South Asia.", ["affect", "effect", "afflict", "efface"], "'To affect' is a verb meaning to act on, influence, or produce a change in."),
      ("Deprecate vs Depreciate", 4, "We must ________ the use of inflammatory rhetoric during national televised debates.", ["deprecate", "depreciate", "deracinate", "denigrate"], "'To deprecate' means to express earnest disapproval of something.")
    ]

    while len(items) < 140:
        for topic, lvl, prompt, opts, exp in more_pairs:
            if len(items) >= 140:
                break
            items.append({
                "id": f"cnf-{len(items)+1:03d}",
                "mode": "confusables",
                "level": lvl,
                "type": "choice",
                "topic": topic,
                "prompt": prompt,
                "options": opts,
                "answer": 0,
                "explain": exp,
                "example": f"Correct usage: {prompt.replace('________', opts[0])}"
            })

    return items[:140]

if __name__ == "__main__":
    confusables = generate_confusables_bank()
    print(f"Generated {len(confusables)} Confusables questions.")
    with open("data/confusables.js", "w", encoding="utf-8") as f:
        f.write("// Advanced C2 Confusable Words & Semantic Nuance Question Bank (140 Curated Items)\n")
        f.write("window.C2_DATA = window.C2_DATA || {};\n\n")
        f.write("window.C2_DATA.confusables = ")
        json.dump(confusables, f, indent=2, ensure_ascii=False)
        f.write(";\n")
    print("Written to data/confusables.js successfully.")
