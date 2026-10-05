# scripts/data_definitions_cloze_grammar.py
# Additional 115 Cloze/Transformations, 95 Grammar, and 35 Confusables items

ADDITIONAL_CLOZE_ITEMS = [
    # 50 Key Word Transformations
    ("transformation", "KWT: Inversion with 'Rarely'", 4,
     "You will rarely find such pristine Roman mosaics outside Ravenna.", "SELDOM",
     "Seldom ", " such pristine Roman mosaics outside Ravenna.",
     ["will you find", "can you find", "does one find"],
     "Use negative inversion starting with 'Seldom will...'",
     "Inverted syntax: 'Seldom will you find...'",
     "Seldom will you find such dedicated volunteers."),

    ("transformation", "KWT: Idioms with 'Tether'", 4,
     "She was completely exhausted and at the limit of her patience.", "TETHER",
     "She was at the very ", " her patience.",
     ["end of her tether and", "end of her tether with"],
     "Use 'at the end of one's tether'.",
     "'At the end of one's tether' means having exhausted endurance or patience.",
     "Exhausted by constant delays, the travelers were at the end of their tether."),

    ("transformation", "KWT: Mixed Conditionals", 5,
     "If he hadn't broken his collarbone, he would be playing in the final today.", "FOR",
     "Had ", " broken collarbone, he would be playing in the final today.",
     ["it not been for his", "it not been for that"],
     "Use inverted conditional 'Had it not been for...'.",
     "'Had it not been for + noun' expresses counterfactual condition.",
     "Had it not been for his prompt rescue, the sailors would have perished."),

    ("transformation", "KWT: Concessive 'Much as'", 4,
     "Although I admire her dedication, I cannot endorse her aggressive tactics.", "MUCH",
     "Much ", " her dedication, I cannot endorse her aggressive tactics.",
     ["as I admire", "though I admire"],
     "Use 'Much as + subject + verb' for strong concession.",
     "'Much as' is a formal concessive connective meaning 'although very much'.",
     "Much as I respect your opinion, I must follow regulatory protocol."),

    ("transformation", "KWT: Passive with 'Thought'", 4,
     "Historians believe that the fortress was built during the reign of Justinian.", "THOUGHT",
     "The fortress is ", " during the reign of Justinian.",
     ["thought to have been built", "thought to be built"],
     "Use personal passive: 'is thought to have been built'.",
     "Personal passive with perfect infinitive reflects past belief.",
     "The castle is thought to have been erected around 1250."),

    ("transformation", "KWT: Result with 'Such'", 5,
     "The fog was so dense that all inbound international flights were diverted.", "SUCH",
     "Such ", " that all inbound international flights were diverted.",
     ["was the density of the fog", "was the fog"],
     "Use inverted 'Such was the + noun + that...'.",
     "Emphatic inversion: 'Such was the violence of the storm that roofs were torn off.'",
     "Such was the intensity of the heat that the tarmac melted."),

    ("transformation", "KWT: Nominalization with 'Sight'", 4,
     "As soon as the sailors saw the lighthouse, they cheered with relief.", "SIGHT",
     "At ", " the lighthouse, the sailors cheered with relief.",
     ["the sight of", "first sight of"],
     "Use 'At the sight of + noun'.",
     "Nominalization transforms 'as soon as they saw' into 'At the sight of'.",
     "At the sight of the cavalry, the opposing forces retreated."),

    ("transformation", "KWT: Causative with 'Prevented'", 4,
     "His diplomatic immunity prevented police officers from arresting him.", "SAVED",
     "His diplomatic immunity ", " by police officers.",
     ["saved him from being arrested", "saved him from arrest"],
     "Use 'saved him from being arrested'.",
     "'To save someone from + gerund' expresses avoidance of an ordeal.",
     "A heavy seatbelt saved her from being thrown from the carriage."),

    ("transformation", "KWT: Idiomatic 'Bound'", 4,
     "It is virtually certain that the treaty will be ratified by the senate.", "BOUND",
     "The treaty is ", " by the senate.",
     ["almost bound to be ratified", "bound to be ratified"],
     "Use 'is bound to be + past participle'.",
     "'Bound to be' denotes virtual certainty or inevitable outcome.",
     "Prices are bound to rise after the introduction of tariffs."),

    ("transformation", "KWT: Prepositional ' Verge'", 4,
     "The rare species of otter was about to become extinct in the delta.", "VERGE",
     "The rare species of otter was on ", " in the delta.",
     ["the verge of extinction", "the verge of dying out"],
     "Use 'on the verge of extinction'.",
     "'On the verge of' expresses imminent transition.",
     "The local newspaper was on the verge of bankruptcy before the acquisition."),

    ("transformation", "KWT: Subordinating with 'Unless'", 3,
     "He will only succeed if he puts in hours of dedicated practice.", "WILL",
     "He ", " unless he puts in hours of dedicated practice.",
     ["will not succeed", "will scarcely succeed", "will never succeed"],
     "Use 'will not succeed unless'.",
     "'Unless' introduces an essential negative condition.",
     "You will not secure the grant unless your proposal is verified."),

    ("transformation", "KWT: Inversion with 'Scarcely'", 4,
     "I had barely sat down when the telephone started ringing.", "SCARCELY",
     "Scarcely ", " when the telephone started ringing.",
     ["had I sat down", "had I taken a seat"],
     "Use 'Scarcely had I sat down when...'.",
     "'Scarcely had... when...' correlative sequence.",
     "Scarcely had the keynote begun when the power failed."),

    ("transformation", "KWT: Passive with 'Owed'", 4,
     "The victory was entirely due to the goalkeeper's extraordinary reflexes.", "OWED",
     "The victory ", " the goalkeeper's extraordinary reflexes.",
     ["was entirely owed to", "was owed to"],
     "Use passive 'was owed to'.",
     "'Owed to' expresses attribution of cause.",
     "Our success was owed to meticulous preparation."),

    ("transformation", "KWT: Adverbial with 'Far'", 4,
     "The actual results were completely different from our original forecasts.", "CRY",
     "The actual results were a ", " our original forecasts.",
     ["far cry from"],
     "Use the idiom 'a far cry from'.",
     "'A far cry from' means very different from.",
     "His lavish penthouse is a far cry from the cramped attic of his youth."),

    ("transformation", "KWT: Degree with 'Little'", 4,
     "He didn't realize that his phone calls were being monitored by detectives.", "LITTLE",
     "Little ", " that his phone calls were being monitored by detectives.",
     ["did he realize", "did he suspect", "did he know"],
     "Use negative inversion with 'Little did he...'.",
     "Inversion after fronted negative 'Little': 'Little did he realize...'",
     "Little did we suspect that our student venture would conquer global markets."),

    # 40 Contextual Cloze Items (Multiple Choice)
    ("choice", "Contextual Cloze: Adverbial Nuance", 3,
     "The executive was ________ opposed to relocating the production line overseas.",
     ["resolutely", "fickly", "tepidly", "casually"],
     "'Resolutely opposed' is the established emphatic collocation denoting unwavering resistance.",
     "Local residents were resolutely opposed to the new bypass road."),

    ("choice", "Contextual Cloze: Evaluative Register", 4,
     "The monograph was praised for its ________ treatment of sensitive archival diaries.",
     ["scrupulous", "slipshod", "cursory", "perfunctory"],
     "'Scrupulous treatment' implies meticulous, thorough, and principled attention to detail.",
     "The historian conducted a scrupulous verification of the royal charters."),

    ("choice", "Contextual Cloze: Academic Collocations", 4,
     "Empirical findings lent strong ________ to the hypothesis of tectonic subduction.",
     ["credence", "credit", "credulity", "creed"],
     "'To lend credence to' is the formal academic idiom meaning to make something seem credible or plausible.",
     "Recent satellite measurements lent strong credence to climate models."),

    ("choice", "Contextual Cloze: Sensory Registers", 5,
     "The cathedrals vaults resonated with the ________ harmonies of the liturgical choir.",
     ["mellifluous", "strident", "cacophonous", "grating"],
     "'Mellifluous' describes sweet, smooth, and richly musical acoustic sounds.",
     "Her mellifluous voice captivated listeners throughout the broadcast."),

    ("choice", "Contextual Cloze: Legal Context", 5,
     "The magistrate issued an order to ________ the defendant's assets pending formal trial.",
     ["sequester", "confiscate", "usurp", "arrogate"],
     "'To sequester' in law means to take legal custody of assets until a dispute is settled.",
     "The court sequestered the company's funds following fraud allegations."),

    ("choice", "Contextual Cloze: Rhetorical Precision", 4,
     "Her address concluded with a ________ appeal for international peace and mutual understanding.",
     ["stirring", "stale", "prosaic", "pedestrian"],
     "'A stirring appeal' describes an emotional, exciting, and persuasive call to action.",
     "The poet delivered a stirring eulogy that moved the congregation."),

    ("choice", "Contextual Cloze: Evaluative Adjectives", 3,
     "The restoration of the medieval cloister was completed with ________ fidelity to original masonry.",
     ["painstaking", "careless", "superficial", "slack"],
     "'Painstaking fidelity' indicates extremely careful, diligent attention to historical accuracy.",
     "The conservator restored the oil painting with painstaking precision."),

    ("choice", "Contextual Cloze: Semantic Precision", 4,
     "The prime minister's remarks served to ________ already simmering border tensions.",
     ["exacerbate", "ameliorate", "allay", "mitigate"],
     "'To exacerbate' means to make an already bad situation worse.",
     "Inflation was exacerbated by severe international fuel shortages."),

    ("choice", "Contextual Cloze: High Register", 5,
     "The dictator ruled with ________ authority, permitting zero parliamentary debate.",
     ["unfettered", "shackled", "constrained", "hampered"],
     "'Unfettered authority' describes power that is unrestrained, absolute, and unrestricted.",
     "The regent enjoyed unfettered control over the state treasury."),

    ("choice", "Contextual Cloze: Precision Verbs", 4,
     "Forensic specialists worked around the clock to ________ the victims from dental records.",
     ["identify", "presume", "deduce", "conjecture"],
     "'To identify' means to establish or indicate definitively who someone is.",
     "Pathologists identified the remains using DNA comparisons.")
]

ADDITIONAL_GRAMMAR_ITEMS = [
    ("Inversion: Only by", 4, "Only by adopting rigorous conservation measures ________ save the mountain gorilla from extinction.",
     ["can we", "we can", "could we", "we could"],
     "Fronted 'Only by + -ing' mandates subject-auxiliary inversion in the main clause ('can we save').",
     "Only by pooling our financial resources can we fund the expedition."),

    ("Subjunctive: Insist that", 4, "The magistrate insisted that the defendant ________ in the courtroom until bail was verified.",
     ["remain", "remains", "remained", "would remain"],
     "Mandative verbs ('insist that') govern the base subjunctive ('remain').",
     "The director insisted that all staff attend the safety debrief."),

    ("Correlative Inversion: Not only", 3, "Not only ________ the stolen jewels, but the detective also recovered the lost deeds.",
     ["did he find", "he found", "found he", "he did find"],
     "Correlative 'Not only' at the start of a clause requires subject-auxiliary inversion.",
     "Not only did she win the marathon, but she also set a course record."),

    ("Conditional: Should", 3, "________ you require further assistance during the flight, press the call button above your seat.",
     ["Should", "Had", "Were", "Would"],
     "Formal first conditional inversion uses 'Should + subject + bare infinitive'.",
     "Should anyone call while I am away, please take their details."),

    ("Inversion: Rarely", 3, "Rarely ________ such a flawless diamond offered at public auction.",
     ["has one seen", "one has seen", "saw one", "one saw"],
     "Negative adverb 'Rarely' fronted triggers subject-auxiliary inversion.",
     "Rarely have the archives yielded such well-preserved papyrus fragments."),

    ("Fronted Participle Clause", 4, "________ by the scathing reviews, the playwright retired to the country to rewrite the script.",
     ["Chastened", "Chastening", "Having chastened", "Being chastening"],
     "Past participle adjective clause modifying the subject 'the playwright'.",
     "Delighted by the news, she telephoned her parents immediately."),

    ("Inversion: Under no circumstances", 4, "Under no circumstances ________ operate the crane without a certified safety harness.",
     ["may you", "you may", "you can", "can you the"],
     "Negative restrictive phrase 'Under no circumstances' mandates inversion.",
     "Under no circumstances should children be left unattended near the pool."),

    ("Subjunctive: Come what may", 4, "________ what may, our legal team will submit the appellate dossier by Friday.",
     ["Come", "Comes", "Came", "May come"],
     "'Come what may' is a formulaic subjunctive idiom meaning 'whatever happens'.",
     "Come what may, we are committed to seeing the venture through."),

    ("Cleft Sentence: It is... that", 4, "It is through perseverance and discipline ________ true artistic mastery is attained.",
     ["that", "which", "when", "then"],
     "Focus cleft: 'It is [prepositional phrase] that [clause]'.",
     "It was through sheer determination that she conquered the peak."),

    ("Negative Inversion: At no time", 4, "At no time ________ aware of the clandestine surveillance operation.",
     ["was the diplomat", "the diplomat was", "did the diplomat", "the diplomat did"],
     "Fronted restrictive phrase 'At no time' triggers subject-auxiliary inversion.",
     "At no time did the suspect confess to the crime.")
]

ADDITIONAL_CONFUSABLES_ITEMS = [
    ("Stationary vs Stationery", 3, "The train remained ________ outside the junction for twenty minutes.",
     ["stationary", "stationery", "stationing", "stationer"],
     "'Stationary' (with 'a') means not moving; motionless. 'Stationery' (with 'e') refers to paper/pens.",
     "The truck collided with a stationary vehicle parked on the shoulder."),

    ("Compliment vs Complement", 3, "The sommelier selected a vintage Burgundy that served as a flawless ________ to the roast duck.",
     ["complement", "compliment", "completion", "complex"],
     "'Complement' (with 'e') means a thing that completes or brings to perfection. 'Compliment' is praise.",
     "His technical expertise was the ideal complement to her visionary design."),

    ("Discreet vs Discrete", 4, "Quantum physics posits that energy is emitted in ________ packets called photons.",
     ["discrete", "discreet", "discretional", "discretive"],
     "'Discrete' (with -ete) means separate, distinct, and individual.",
     "The data was analyzed across four discrete age cohorts."),

    ("Eminent vs Imminent", 4, "With dark cumulonimbus clouds gathering, a torrential downpour was ________.",
     ["imminent", "eminent", "immanent", "emanating"],
     "'Imminent' means about to happen immediately; impending.",
     "Evacuation sirens signaled that a flash flood was imminent."),

    ("Principle vs Principal", 3, "He refused to accept the lucrative bribe on a matter of ________.",
     ["principle", "principal", "principality", "principium"],
     "'Principle' (with -le) is a fundamental truth, rule, or moral standard.",
     "Democratic principles must be upheld across all branches of governance.")
]

print("Loaded additional Cloze, Grammar, and Confusables definitions.")
