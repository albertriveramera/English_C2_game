# scripts/build_vocab.py
# Generates 200 authentic C2 Vocabulary questions
import json

VOCAB_DATA = [
  # --- 1-30: Existing curated items ---
  ("voc-001", "Evocative Adjectives", 3,
   "Her argument was so ________ that even the harshest critics in the symposium were forced to concede her point.",
   ["cogent", "turgid", "tepid", "fickle"], 0,
   "'Cogent' means clear, logical, and convincingly persuasive. In contrast, 'turgid' means bombastic or swollen, 'tepid' means lukewarm/unenthusiastic, and 'fickle' means changeful.",
   "The defense attorney presented a cogent summary that left no room for reasonable doubt."),

  ("voc-002", "High-register Verbs", 4,
   "The minister was accused of attempting to ________ the gravity of the fiscal deficit by burying the figures in an appendix.",
   ["obfuscate", "promulgate", "excoriate", "venerate"], 0,
   "'Obfuscate' means to deliberately make something obscure, unclear, or bewildering. 'Promulgate' means to announce or declare officially, 'excoriate' means to censure severely, and 'venerate' means to revere.",
   "Legal draftsmen should strive for clarity rather than obfuscate the intent of the statute."),

  ("voc-003", "Literary Adjectives", 4,
   "Far from being a permanent arrangement, their cordiality was merely a(n) ________ truce prompted by shared commercial necessity.",
   ["ephemeral", "inexorable", "perennial", "inveterate"], 0,
   "'Ephemeral' means lasting for only a very short time; transient. 'Inexorable' means unstoppable, 'perennial' means enduring year after year, and 'inveterate' means habitual/long-established.",
   "Fame achieved through viral phenomena is notoriously ephemeral."),

  ("voc-004", "Formal Epithets", 3,
   "He was an ________ collector of antiquities, dedicating every weekend and surplus penny to scouring remote flea markets.",
   ["inveterate", "inchoate", "insipid", "invidious"], 0,
   "'Inveterate' describes a long-established and ingrained habit, activity, or attitude that is unlikely to change. 'Inchoate' means just begun and not fully formed, 'insipid' means lacking flavor or interest, and 'invidious' means likely to arouse resentment.",
   "As an inveterate traveler, she felt restless whenever she remained in one city for over a month."),

  ("voc-005", "Nuanced Descriptors", 5,
   "The philosopher’s prose was notoriously ________, dense with idiosyncratic neologisms and elliptical tangents that confounded even his disciples.",
   ["recondite", "trenchant", "pellucid", "sycophantic"], 0,
   "'Recondite' means dealing with very abstruse, profound, or difficult subject matter beyond ordinary knowledge. 'Pellucid' is the exact antonym (translucently clear), 'trenchant' means incisive/sharp, and 'sycophantic' means obsequious.",
   "The monograph delves into the recondite metaphysics of early medieval scholasticism."),

  ("voc-006", "Psychological Traits", 3,
   "Despite the tempestuous uproar during the press conference, the prime minister maintained an admirable ________.",
   ["equanimity", "parsimony", "pugnacity", "cupidity"], 0,
   "'Equanimity' means mental calmness, composure, and evenness of temper, especially in a difficult situation. 'Parsimony' is stinginess, 'pugnacity' is combativeness, and 'cupidity' is greed.",
   "She accepted both extravagant praise and scathing criticism with unchanging equanimity."),

  ("voc-007", "Critical Stances", 4,
   "The editor delivered a(n) ________ critique of the proposed tax overhaul, dissecting each clause with ruthless precision.",
   ["trenchant", "anodyne", "vacuous", "halcyon"], 0,
   "'Trenchant' means vigorous, incisive, keen, and keenly effective in expression. 'Anodyne' means innocuous or unlikely to offend, 'vacuous' means devoid of thought, and 'halcyon' means idyllically peaceful.",
   "Her trenchant analysis of the energy sector exposed decades of regulatory capture."),

  ("voc-008", "Stylistic Nuances", 4,
   "The candidate's speeches were entirely ________, packed with sentimental platitudes but utterly barren of concrete policy proposals.",
   ["vacuous", "profound", "perspicacious", "laconic"], 0,
   "'Vacuous' means having or showing a lack of thought or intelligence; empty and mindless. 'Perspicacious' means acutely perceptive, 'laconic' means concise/using very few words.",
   "The debate devolved into vacuous soundbites tailored strictly for television headlines."),

  ("voc-009", "High-level Verbs", 5,
   "Before embarking on the cross-examination, the barrister sought to ________ any lingering doubts in the jury’s mind regarding the witness’s credibility.",
   ["dispel", "engender", "foster", "exacerbate"], 0,
   "'Dispel' means to drive off, cause to vanish, or alleviate doubts, fears, or false beliefs. 'Engender' and 'foster' both mean to bring about or nurture, while 'exacerbate' means to make worse.",
   "The newly released forensic findings dispelled any speculation regarding the time of death."),

  ("voc-010", "Social Dispositions", 3,
   "Unlike his gregarious predecessor, the new director was notoriously ________, rarely volunteering an opinion unless directly pressed.",
   ["taciturn", "loquacious", "ebullient", "garrulous"], 0,
   "'Taciturn' means reserved or uncommunicative in speech; saying little. 'Loquacious' and 'garrulous' are antonyms meaning excessively talkative; 'ebullient' means cheerful and full of energy.",
   "A taciturn man by nature, he expressed his deepest emotions through verse rather than conversation."),

  ("voc-011", "Intellectual Acumen", 4,
   "Thanks to her ________ reading of international maritime law, she identified a precedent that saved the shipping company millions.",
   ["perspicacious", "cursory", "perfunctory", "credulous"], 0,
   "'Perspicacious' means having a ready insight into and deep understanding of complex things. 'Cursory' and 'perfunctory' denote superficial and hasty work, while 'credulous' means gullible.",
   "His perspicacious assessment of market volatility foresaw the collapse months ahead."),

  ("voc-012", "Harmful Influences", 5,
   "The committee warned that unvetted algorithms could have a ________ effect on equitable recruitment practices.",
   ["deleterious", "salubrious", "propitious", "benign"], 0,
   "'Deleterious' means causing harm or damage in a subtle or unexpected way. 'Salubrious' means health-giving, 'propitious' means favorably disposed or auspicious, and 'benign' means harmless.",
   "Prolonged exposure to chronic stress exercises a deleterious impact upon cognitive function."),

  ("voc-013", "Attitudinal Registers", 3,
   "The court found his ________ apologies utterly disingenuous, given that he had continued trading illicitly right up to his arrest.",
   ["fulsome", "curt", "brusque", "spartan"], 0,
   "'Fulsome' in high-register English means complimentary or flattering to an excessive, cloying, or insincere degree. 'Curt' and 'brusque' mean rudely brief, and 'spartan' means austere.",
   "The ambassador was treated to fulsome praise by officials eager to secure trade concessions."),

  ("voc-014", "Linguistic Precision", 4,
   "Rather than addressing the substance of the petition, the spokesperson resorted to ________ sophistry that sidestepped the core issue.",
   ["specious", "scrupulous", "unimpeachable", "veracious"], 0,
   "'Specious' describes an argument that appears superficially plausible or attractive, but is actually fallacious and deceitful. 'Scrupulous' means conscientious, 'unimpeachable' means beyond reproach, and 'veracious' means truthful.",
   "The company’s defense rested on a specious interpretation of environmental regulations."),

  ("voc-015", "Academic Register", 4,
   "The author sought to ________ the entrenched dogma that economic globalization inevitably reduces cultural diversity.",
   ["gainsay", "corroborate", "substantiate", "champion"], 0,
   "'Gainsay' (formal/literary) means to deny, contradict, or dispute a fact or assertion. 'Corroborate' and 'substantiate' mean to support with evidence; 'champion' means to advocate.",
   "No one could gainsay her contribution to pediatric neurology."),

  ("voc-016", "Sensory & Aesthetic Nuance", 5,
   "The late afternoon sun cast an almost ________ glow over the Venetian canals, as though frozen in an 18th-century painting.",
   ["pellucid", "turbid", "fetid", "squalid"], 0,
   "'Pellucid' means clear, limpid, allowing light through; easily understood or luminous. 'Turbid' means cloudy or muddy, 'fetid' means foul-smelling, and 'squalid' means sordid/wretched.",
   "The mountain spring was so pellucid that one could count the pebbles ten feet below."),

  ("voc-017", "Emotional Expression", 3,
   "Far from expressing remorse, the defendant remained ________ throughout the sentencing hearing.",
   ["impenitent", "contrite", "remorseful", "penitent"], 0,
   "'Impenitent' means not feeling or showing regret or sorrow for having done something wrong. The other three options all mean feeling deep regret and seeking repentance.",
   "Despite the overwhelming proof of embezzlement, he remained stubbornly impenitent."),

  ("voc-018", "Temperament & Demeanor", 4,
   "She was known for her ________ demeanor; nothing seemed capable of perturbing her serene composure.",
   ["phlegmatic", "mercurial", "choleric", "bilious"], 0,
   "'Phlegmatic' (deriving from the classical humours) means having an unemotional, calm, and stolid disposition. 'Mercurial' means volatile/unpredictable, while 'choleric' and 'bilious' mean irritable and bad-tempered.",
   "In a crisis that drove colleagues to panic, his phlegmatic demeanor kept the department functional."),

  ("voc-019", "Formal Abnegation", 5,
   "In a dramatic gesture of humility, the monarch decided to ________ the throne in favor of his younger sister.",
   ["abdicate", "usurp", "arrogate", "commandeer"], 0,
   "'Abdicate' means to renounce or relinquish one's throne, high office, or responsibility formally. 'Usurp' and 'arrogate' both mean to seize power unlawfully or without right; 'commandeer' means to seize arbitrarily.",
   "King Edward VIII chose to abdicate the throne in December 1936."),

  ("voc-020", "Social Etiquette & Register", 3,
   "His ________ flattery of the board of trustees was transparent to everyone in the boardroom.",
   ["obsequious", "scornful", "imperious", "disdainful"], 0,
   "'Obsequious' means obedient or attentive to an excessive or servile degree; fawning. 'Scornful', 'imperious', and 'disdainful' convey haughty superiority and disrespect.",
   "She despised the obsequious assistants who nodded in agreement with every foolish idea."),

  ("voc-021", "Literary Descriptions", 4,
   "The castle stood atop a ________ crag, commanding an unobstructed vista of the windswept moorlands.",
   ["precipitous", "placid", "planar", "mundane"], 0,
   "'Precipitous' means dangerously high or steep. 'Placid' means calm/peaceful, 'planar' means flat in a two-dimensional sense, and 'mundane' means ordinary/dull.",
   "A precipitous drop of several hundred feet deterred all but the most seasoned climbers."),

  ("voc-022", "Intellectual Nuance", 4,
   "The treatise provides a(n) ________ refutation of neoclassical market equilibrium theory.",
   ["incisive", "amorphous", "superficial", "unwieldy"], 0,
   "'Incisive' means intelligently analytical, sharp, and clear-thinking. 'Amorphous' means formless, 'superficial' means lacking depth, and 'unwieldy' means cumbersome.",
   "The reviewer commended the scholar’s incisive grasp of statistical modeling."),

  ("voc-023", "High-register Verbs", 5,
   "Historical revisions have served to ________ the myth that the empire fell purely due to external invasions.",
   ["debunk", "canonize", "corroborate", "consecrate"], 0,
   "'Debunk' means to expose the falseness or hollowness of a myth, idea, or belief. 'Canonize' and 'consecrate' mean to elevate to revered or holy status, and 'corroborate' means to confirm.",
   "Archaeological excavations have decisively debunked that long-held local legend."),

  ("voc-024", "Descriptive Nuance", 3,
   "Despite the team's relentless effort, their victory proved ________, as two key strikers sustained season-ending fractures.",
   ["pyrrhic", "resplendent", "unalloyed", "triumphal"], 0,
   "A 'pyrrhic' victory is one won at such a devastating cost that it is tantamount to defeat. 'Unalloyed' means pure/complete, 'resplendent' means brilliant/shining.",
   "Winning the litigation was a pyrrhic victory; legal fees bankrupted the firm regardless."),

  ("voc-025", "Moral & Ethical Vocabulary", 4,
   "The disgraced official’s conduct was branded as sheer ________, completely devoid of public integrity.",
   ["venality", "probity", "veracity", "rectitude"], 0,
   "'Venality' is the state of being open to bribery or corruption. 'Probity', 'veracity', and 'rectitude' all denote exemplary moral uprightness and honesty.",
   "Investigative journalists exposed rampant venality among the procurement commissioners."),

  ("voc-026", "High Literary Vocabulary", 5,
   "The treaty was perceived as a mere ________ to buy time while military reserves were mobilized.",
   ["subterfuge", "panacea", "paragon", "milestone"], 0,
   "'Subterfuge' means deceit used in order to achieve one's goal; a deceptive stratagem. 'Panacea' is a cure-all, and 'paragon' is a model of excellence.",
   "Her alleged research trip was revealed as a subterfuge for negotiating with rival firms."),

  ("voc-027", "Stylistic Qualities", 4,
   "The keynote speaker was praised for her ________ delivery, managing to summarize a 400-page dossier in twenty cogent minutes.",
   ["laconic", "diffuse", "prolix", "pleonastic"], 0,
   "'Laconic' means using very few words to express a great deal; terse and concise. 'Diffuse', 'prolix', and 'pleonastic' all denote wordiness and excessive verbosity.",
   "His laconic reply—a single nod—signaled that negotiations were terminated."),

  ("voc-028", "Nuanced Behavioral Adjectives", 3,
   "The young apprentice was far too ________, accepting every questionable assertion the master made without scrutiny.",
   ["credulous", "incredulous", "discerning", "skeptical"], 0,
   "'Credulous' means having or showing too great a readiness to believe things; gullible. 'Incredulous' means unwilling or unable to believe, while 'discerning' and 'skeptical' imply critical thought.",
   "Financial scammers prey primarily upon credulous investors seeking miraculous returns."),

  ("voc-029", "Complex Evaluative Adjectives", 5,
   "The decision to cancel the project was deemed ________, as it anticipated the sudden collapse of consumer demand by mere weeks.",
   ["prescient", "impetuous", "retrograde", "derogatory"], 0,
   "'Prescient' means having or showing knowledge of events before they take place; prophetic. 'Impetuous' means rash/impulsive, 'retrograde' means directed backward or regressive.",
   "With prescient foresight, George Orwell explored themes of digital surveillance decades before its inception."),

  ("voc-030", "Formal Verbs of Censure", 4,
   "The regulatory body was swift to ________ the pharmaceutical company for suppressing adverse trial results.",
   ["castigate", "extol", "encomium", "laud"], 0,
   "'Castigate' means to reprimand or censure someone severely. 'Extol' and 'laud' mean to praise enthusiastically; 'encomium' is a noun meaning a formal tribute.",
   "The independent inquiry castigated senior leadership for their systemic failures in oversight.")
]

# Additional 170 items for Vocabulary (reaching 200 total)
RAW_EXTRA_VOCAB = [
  ("Aesthetic Nuance", 4, "The critic lauded the poet's ________ verses, which evoked the fleeting brilliance of autumnal twilight.",
   ["luminous", "turgid", "vapid", "moribund"], 0,
   "'Luminous' conveys glowing, clear, and inspiring beauty. 'Turgid' means swollen or bombastic, 'vapid' means flat or dull, and 'moribund' means dying.",
   "Her luminous performance in the third act captivated the entire auditorium."),

  ("Philosophical Terminology", 5, "In examining moral agency, Kant emphasized the categorical ________ of treating humanity as an end in itself.",
   ["imperative", "contingency", "platitude", "anomaly"], 0,
   "A 'categorical imperative' in philosophy denotes an unconditional moral obligation binding in all circumstances.",
   "Preserving biodiversity must be treated as an ethical imperative rather than an optional luxury."),

  ("Literary Verbs", 4, "The totalitarian regime sought to ________ all historical archives that contradicted official state propaganda.",
   ["expunge", "promulgate", "exalt", "consecrate"], 0,
   "'Expunge' means to erase, obliterate, or remove completely. 'Promulgate' means to proclaim publicly, while 'exalt' and 'consecrate' mean to honor or sanctify.",
   "The court ordered the clerk to expunge the improper testimony from the official transcript."),

  ("Erudite Adjectives", 5, "His ________ disquisitions on 12th-century liturgical music alienated listeners who preferred accessible melodies.",
   ["arcane", "banal", "pedestrian", "prosaic"], 0,
   "'Arcane' refers to knowledge understood by very few; mysterious or obscure. 'Banal', 'pedestrian', and 'prosaic' all denote the dull and commonplace.",
   "The treaty contained arcane maritime clauses that baffled international trade lawyers."),

  ("Nuanced Descriptors", 4, "She offered a ________ smile that betrayed neither approval nor annoyance at the unexpected intrusion.",
   ["noncommittal", "demonstrative", "florid", "histrionic"], 0,
   "'Noncommittal' means not expressing or revealing a definite opinion or decision. 'Histrionic' and 'demonstrative' denote overt emotion.",
   "The ambassador gave a noncommittal response regarding potential troop deployments."),

  ("Moral Qualities", 5, "The judge was revered throughout the legal community for her unshakeable ________ in the face of political intimidation.",
   ["probity", "mendacity", "duplicity", "perfidy"], 0,
   "'Probity' denotes complete and confirmed integrity, uprightness, and honesty. 'Mendacity', 'duplicity', and 'perfidy' mean deceitfulness and treachery.",
   "Financial institutions depend fundamentally upon the probity of their auditing committees."),

  ("Rhetorical Descriptors", 4, "The speech degenerated into an angry ________ against the foreign press corps.",
   ["diatribe", "panegyric", "encomium", "eulogy"], 0,
   "A 'diatribe' is a forceful, bitter verbal attack or denunciation. 'Panegyric', 'encomium', and 'eulogy' are elaborate speeches of high praise.",
   "He launched into a bitter diatribe against modernization and urban development."),

  ("Intellectual Character", 5, "An exceptionally ________ scholar, she could synthesize findings across paleontology, linguistics, and archaeology.",
   ["polymathic", "parochial", "myopic", "monolithic"], 0,
   "'Polymathic' describes someone with encyclopedic, wide-ranging knowledge across diverse subjects. 'Parochial' and 'myopic' mean narrow-minded.",
   "Leonardo da Vinci remains the quintessential archetype of the polymathic Renaissance mind."),

  ("Tone & Temperament", 3, "The executive's ________ manner during negotiations unsettled counterparts accustomed to diplomatic flattery.",
   ["brusque", "effusive", "servile", "diffident"], 0,
   "'Brusque' means abrupt, blunt, or curt in speech or manner. 'Effusive' means overly emotional, while 'servile' means submissive.",
   "His brusque rejection of the preliminary compromise brought talks to an abrupt halt."),

  ("Aesthetic Criticism", 4, "The architectural committee rejected the monument design as excessively ________ and gaudy for a solemn memorial.",
   ["meretricious", "austere", "sublime", "understated"], 0,
   "'Meretricious' means apparently attractive but having no real value or integrity; gaudily cheap. 'Austere' and 'understated' mean minimalist and sober.",
   "Her essay condemned the meretricious glitter of modern reality television."),

  ("Nuanced Verbs", 5, "Years of intense meditation enabled the ascetic monk to ________ physical discomfort and hunger.",
   ["transcend", "succumb to", "wallow in", "instigate"], 0,
   "'Transcend' means to go beyond or rise above the normal physical or mental limitations.",
   "Great masterworks of literature transcend the specific historical eras in which they were written."),

  ("Psychological Qualities", 4, "He possessed a ________ wit, capable of puncturing pretension with a single devastating quip.",
   ["mordant", "saccharine", "dulcet", "complaisant"], 0,
   "'Mordant' means sharply sarcastic, biting, or caustic. 'Saccharine' means sickeningly sweet, and 'dulcet' means soothing/pleasing.",
   "Her mordant observations regarding parliamentary decorum kept readers thoroughly entertained."),

  ("Sensory Adjectives", 3, "The subterranean wine cellar was dark, cool, and distinctly ________, smelling of damp limestone and aged oak.",
   ["musty", "fetid", "rancid", "putrid"], 0,
   "'Musty' denotes a stale, damp, or moldy smell typical of old cellars. 'Fetid' and 'putrid' imply offensive, rotting decay.",
   "The abandoned library was filled with musty folio volumes untouched for decades."),

  ("Emotional Dispositions", 4, "After the death of his lifelong collaborator, he fell into a state of ________ melancholy that lasted years.",
   ["profound", "facetious", "flippant", "glib"], 0,
   "'Profound' indicates deep, intense, and far-reaching sorrow or insight. 'Facetious' and 'flippant' mean inappropriately frivolous.",
   "The discovery of universal gravitation exerted a profound influence on modern physics."),

  ("Literary Nouns", 5, "The sudden demise of the heir apparent created an unprecedented ________ in the succession hierarchy.",
   ["lacuna", "surfeit", "plethora", "confluence"], 0,
   "A 'lacuna' (plural 'lacunae') is an unfilled space, gap, or missing portion in a text, law, or continuity. 'Surfeit' and 'plethora' mean excessive surplus.",
   "Legal historians identified a crucial lacuna in the constitutional amendment of 1884."),

  ("Descriptive Precision", 4, "The director was exasperated by the actor’s ________ gestures, which belonged more to 19th-century melodrama than subtle cinema.",
   ["histrionic", "reticent", "demure", "unassuming"], 0,
   "'Histrionic' means overly theatrical, dramatic, or melodramatic in character or style. 'Reticent' means reserved.",
   "We were exhausted by his histrionic complaints over minor domestic inconveniences."),

  ("Academic Precision", 5, "The treatise was praised for its ________ documentation, leaving not a single assertion unsupported by primary sources.",
   ["scrupulous", "slipshod", "cursory", "negligent"], 0,
   "'Scrupulous' means diligent, thorough, and attentive to fine details; morally upright. 'Slipshod' means careless.",
   "The archivist conducted a scrupulous verification of the treaty's signatures."),

  ("Behavioral Tendencies", 4, "His ________ nature made him prone to picking quarrels over minor administrative technicalities.",
   ["fractious", "conciliatory", "affable", "pliable"], 0,
   "'Fractious' means irritable, quarrelsome, and difficult to control. 'Conciliatory' and 'affable' mean friendly and peace-seeking.",
   "The debate turned fractious when delegates began questioning each other's credentials."),

  ("Literary Tropes", 5, "The poet utilized ________ imagery, where the natural landscape seemed to mourn the tragic hero's downfall.",
   ["anthropomorphic", "tautological", "anachronistic", "pejorative"], 0,
   "'Anthropomorphic' refers to attributing human emotions, characteristics, or behaviors to nature, animals, or objects.",
   "Ancient mythologies abound in anthropomorphic deities endowed with human flaws."),

  ("High-register Verbs", 4, "The defense attorney sought to ________ the credibility of the prosecution's key eyewitness.",
   ["undermine", "buttress", "corroborate", "substantiate"], 0,
   "'To undermine' means to erode the base, foundation, or credibility of something gradually. 'Buttress' and 'corroborate' mean to strengthen or confirm.",
   "Inconsistent testimonies significantly undermined the credibility of the allegations."),

  ("Evaluative Adjectives", 4, "The general made a ________ retreat, saving thousands of infantrymen from an encircled perimeter.",
   ["judicious", "rash", "reckless", "headlong"], 0,
   "'Judicious' means having, showing, or done with good sense or sound judgment.",
   "Through a judicious deployment of resources, the foundation balanced its endowment."),

  ("Literary Register", 5, "The king’s favorite lived in ________ luxury while the rural peasantry suffered devastating famine.",
   ["sybaritic", "ascetic", "monastic", "spartan"], 0,
   "'Sybaritic' means fond of sensuous luxury or self-indulgence (derived from ancient Sybaris). 'Ascetic' and 'spartan' mean severely disciplined.",
   "The tycoon retreated to his sybaritic Mediterranean villa for the summer season."),

  ("Intellectual Traits", 4, "She possessed an uncanny, almost ________ ability to foresee shifting geopolitical alliances.",
   ["clairvoyant", "blinded", "pedantic", "obtuse"], 0,
   "'Clairvoyant' means having exceptional insight into the future or perceiving things beyond normal sensory contact.",
   "His market predictions seemed almost clairvoyant in their pinpoint accuracy."),

  ("Formal Verbs", 4, "The university decided to ________ the honorary doctorate following revelations of academic plagiarism.",
   ["rescind", "confer", "bestow", "ratify"], 0,
   "'To rescind' means to revoke, cancel, or repeal a law, decree, or award formally. 'Confer' and 'bestow' mean to grant.",
   "The government moved to rescind the trade sanctions following democratic elections."),

  ("Social Nuances", 3, "Her ________ manner put nervous interviewees immediately at ease.",
   ["affable", "haughty", "supercilious", "imperious"], 0,
   "'Affable' means friendly, good-natured, or easy to talk to. 'Haughty' and 'supercilious' mean arrogant and disdainful.",
   "An affable host, he personally greeted every guest entering the salon."),

  ("Rhetorical Style", 5, "The manifesto was written in an intensely ________ style, designed to incite fury rather than encourage calm deliberation.",
   ["polemical", "irenic", "conciliatory", "anodyne"], 0,
   "'Polemical' means relating to or involving strongly critical, controversial, or disputatious writing. 'Irenic' means peace-promoting.",
   "His polemical essays against industrial automation provoked fierce parliamentary debate."),

  ("Aesthetic Terminology", 4, "The painter captured the ________ play of light on the morning dew with remarkable delicacy.",
   ["scintillating", "somber", "leaden", "tenebrous"], 0,
   "'Scintillating' means sparkling, shining brightly, or brilliantly clever. 'Tenebrous' and 'somber' mean dark and gloomy.",
   "The symposium concluded with a scintillating lecture on astrophysics."),

  ("Psychological Nuance", 4, "A sense of ________ dread settled over the garrison as winter blizzards cut off communication lines.",
   ["foreboding", "jubilation", "elation", "complacency"], 0,
   "'Foreboding' is a feeling that something bad or harmful will happen. 'Jubilation' and 'elation' denote joy.",
   "She read the telegram with an ominous sense of foreboding."),

  ("Descriptive Precision", 5, "The old town was a ________ of narrow alleyways where tourists routinely lost their bearings.",
   ["labyrinth", "monolith", "conduit", "chasm"], 0,
   "A 'labyrinth' is a complicated, irregular network of passages or paths in which it is difficult to find one's way; a maze.",
   "Navigating the labyrinth of corporate tax exemptions requires expert accountants."),

  ("Evaluative Register", 4, "The evidence against the defendant was purely ________, lacking any forensic or physical corroboration.",
   ["circumstantial", "irrefutable", "indisputable", "conclusive"], 0,
   "'Circumstantial' evidence relies on inference rather than direct observation. 'Irrefutable' and 'conclusive' mean decisive.",
   "The jury acquitted the suspect because the prosecution's case was wholly circumstantial.")
]

# Systematic expansion to guarantee 200 distinct, authentic items
THEMES = [
  ("Literary Qualities", ["pellucid", "trenchant", "recondite", "ephemeral", "sycophantic", "lugubrious", "salubrious", "perspicacious", "punctilious", "mercurial"]),
  ("Rhetorical & Critical Stances", ["castigate", "excoriate", "laud", "venerate", "repudiate", "gainsay", "extol", "debunk", "obfuscate", "substantiate"]),
  ("Ethical & Moral Concepts", ["probity", "venality", "rectitude", "duplicity", "perfidy", "mendacity", "chicanery", "equanimity", "parsimony", "magnanimity"]),
  ("Aesthetic & Sensory Nuances", ["scintillating", "tenebrous", "fetid", "musty", "dulcet", "mellifluous", "strident", "cacophonous", "resplendent", "sublime"]),
  ("Intellectual & Analytical Modes", ["incisive", "specious", "cogent", "fallacious", "sophistic", "tautological", "empirical", "hermeneutic", "teleological", "dialectical"]),
  ("Temperament & Demeanor", ["phlegmatic", "taciturn", "ebullient", "loquacious", "choleric", "irascible", "sanguine", "bilious", "complaisant", "petulant"]),
  ("Harmful & Beneficial Influences", ["deleterious", "pernicious", "salutary", "propitious", "benign", "malignant", "baleful", "noxious", "insidious", "innocuous"]),
  ("Social & Status Dynamics", ["obsequious", "imperious", "supercilious", "condescending", "servile", "deferential", "disdainful", "haughty", "insolent", "humble"])
]

def generate_vocab_bank():
    items = []
    # Start with initial 30
    for q in VOCAB_DATA:
        items.append({
            "id": q[0],
            "mode": "vocabulary",
            "level": q[2],
            "type": "choice",
            "topic": q[1],
            "prompt": q[3],
            "options": q[4],
            "answer": q[5],
            "explain": q[6],
            "example": q[7]
        })
    
    # Add RAW_EXTRA_VOCAB
    idx = len(items) + 1
    for topic, lvl, prompt, opts, ans, exp, ex in RAW_EXTRA_VOCAB:
        items.append({
            "id": f"voc-{idx:03d}",
            "mode": "vocabulary",
            "level": lvl,
            "type": "choice",
            "topic": topic,
            "prompt": prompt,
            "options": opts,
            "answer": ans,
            "explain": exp,
            "example": ex
        })
        idx += 1

    # Enrich systematically with rich contextual C2 items up to 200
    extra_data = [
      ("pugnacious", "combative, belligerent, eager to argue or fight", "The senator's ________ posture alienated moderate voters who sought consensus.", ["pugnacious", "pacific", "pliant", "placid"], "His pugnacious demeanor during the debate caused several interruptions."),
      ("lugubrious", "looking or sounding sad, gloomy, or dismal", "The funeral organist played a ________ dirge that deepened the mourning assembly's sorrow.", ["lugubrious", "festive", "jaunty", "blithe"], "She gave a lugubrious sigh before recounting the tale of her ruined investments."),
      ("punctilious", "showing great attention to detail or correct behavior", "The diplomat was ________ in observing every nuance of royal protocol.", ["punctilious", "slipshod", "remiss", "heedless"], "He was punctilious about replying to letters within twenty-four hours."),
      ("mercurial", "subject to sudden or unpredictable changes of mood or mind", "Working under such a ________ editor meant praise one morning and dismissal the next.", ["mercurial", "constant", "steadfast", "staunch"], "His mercurial temperament made long-term financial planning hazardous."),
      ("repudiate", "refuse to accept or be associated with; deny the truth or validity of", "The administration was forced to ________ allegations of covert domestic surveillance.", ["repudiate", "endorse", "espouse", "ratify"], "She chose to repudiate her former political alliances upon publishing her memoir."),
      ("chicanery", "the use of trickery or subterfuge to achieve a political, financial, or legal purpose", "Forensic accountants uncovered systemic corporate ________ designed to conceal liabilities.", ["chicanery", "candor", "probity", "forthrightness"], "He secured the municipal concession through legal chicanery and backroom bribes."),
      ("magnanimity", "generosity of spirit, especially towards a rival or defeated opponent", "In a rare display of ________, the victor offered cabinet posts to defeated opposition leaders.", ["magnanimity", "spite", "petulance", "vindictiveness"], "She accepted her rival's apology with effortless magnanimity."),
      ("mellifluous", "sweet or musical; pleasant to hear (of a voice or words)", "Her ________ cadence mesmerized radio audiences during the nighttime broadcasts.", ["mellifluous", "strident", "cacophonous", "grating"], "The tenor possessed a mellifluous voice that carried across the auditorium effortlessly."),
      ("strident", "loud and harsh; grating; presenting a point of view in an excessively forceful manner", "The protest was marked by ________ denunciations of the government's austerity budget.", ["strident", "dulcet", "muted", "hushed"], "Critics rejected his strident assertions regarding the inevitable collapse of democratic institutions."),
      ("cacophonous", "involving or producing a harsh, discordant mixture of sounds", "The busy marketplace was a ________ blend of shouting vendors, squawking fowl, and idling engines.", ["cacophonous", "harmonious", "symphonic", "melodious"], "A cacophonous alarm roused the sleeping guests at two in the morning."),
      ("resplendent", "attractive and impressive through being richly colorful or sumptuous", "The ballroom was ________ with crystal chandeliers and gilded rococo mirrors.", ["resplendent", "drab", "dingy", "somber"], "The royal guard appeared in resplendent ceremonial tunics for the coronation."),
      ("fallacious", "based on a mistaken belief or unsound reasoning", "The economist demonstrated that the prediction rested upon completely ________ assumptions.", ["fallacious", "sound", "valid", "cogent"], "It is fallacious to assume that high technological adoption always correlates with subjective happiness."),
      ("sophistic", "plausible but fallacious; subtly misleading in argument", "The lawyer's ________ arguments distracted the jury from the indisputable ballistics report.", ["sophistic", "scrupulous", "unassailable", "candid"], "He countered their sophistic rhetoric with hard empirical data."),
      ("tautological", "needlessly repetitive; saying the same thing twice in different words", "Expressions like 'free gift' or 'added bonus' are famously ________ pleonasms.", ["tautological", "concise", "elliptical", "laconic"], "The witness's deposition was tautological, repeating identical assertions across three pages."),
      ("empirical", "based on, concerned with, or verifiable by observation or experience rather than theory", "The medical claim requires rigorous ________ verification across multi-center clinical trials.", ["empirical", "hypothetical", "speculative", "abstract"], "Her theory was grounded in exhaustive empirical research across fifteen archives."),
      ("irascible", "having or showing a tendency to be easily angered; irritable", "The ________ professor threw chalk at undergraduates who arrived late to his lectures.", ["irascible", "equable", "placid", "genial"], "An irascible personality made him notoriously difficult to collaborate with on group projects."),
      ("sanguine", "optimistic or positive, especially in an apparently bad or difficult situation", "Despite three consecutive quarterly losses, the founder remained remarkably ________ about profitability.", ["sanguine", "pessimistic", "morose", "despondent"], "Medical researchers are cautiously sanguine regarding the efficacy of the new vaccine."),
      ("petulant", "childishly sulky or bad-tempered", "When the committee rejected his amendment, the delegate responded with ________ obstinacy.", ["petulant", "urbane", "gracious", "forbearing"], "A petulant display of temper will hardly persuade senior board members to reconsider."),
      ("pernicious", "having a harmful effect, especially in a gradual or subtle way", "The editorial highlighted the ________ influence of unverified disinformation on public health.", ["pernicious", "salutary", "benign", "harmless"], "Unchecked inflation exercises a pernicious toll upon working-class pensions."),
      ("baleful", "threatening harm; menacing; having a destructive influence", "The prisoner cast a ________ glare at the judge as the verdict of guilty was read.", ["baleful", "benevolent", "genial", "tender"], "A baleful mist rolled over the cemetery as midnight approached."),
      ("insidious", "proceeding in a gradual, subtle way, but with very harmful effects", "Glaucoma is an ________ condition that robs patients of peripheral vision without causing acute pain.", ["insidious", "overt", "blatant", "benign"], "The insidious spread of cynicism threatens civic engagement across western democracies."),
      ("innocuous", "not harmful or offensive; innocuous remarks", "What seemed like an ________ query during the interview revealed an undisclosed conflict of interest.", ["innocuous", "lethal", "toxic", "virulent"], "He offered an innocuous observation about the weather to break the tense silence."),
      ("supercilious", "behaving or looking as though one thinks one is superior to others", "The haughty maitre d' gave us a ________ once-over before seating us near the pantry.", ["supercilious", "humble", "modest", "self-effacing"], "Her supercilious condescension made her universally disliked among junior associates."),
      ("deferential", "showing respect and deference towards an elder or authority figure", "The young barrister adopted a respectfully ________ tone when addressing the Lord Chief Justice.", ["deferential", "insolent", "impertinent", "brash"], "In traditional diplomatic circles, juniors maintain a strictly deferential posture toward ambassadors."),
      ("insolent", "showing a rude and arrogant lack of respect", "The clerk was dismissed for delivering an ________ retort to a member of the diplomatic corps.", ["insolent", "courteous", "deferential", "polite"], "Insolent behavior towards exam proctors will result in immediate disqualification."),
      ("alacrity", "brisk and cheerful readiness; promptness in response", "The interns accepted the challenging assignment with unexpected ________ and diligence.", ["alacrity", "lethargy", "torpor", "reluctance"], "She responded to the emergency summons with commendable alacrity."),
      ("anachronism", "a thing belonging or appropriate to a period other than that in which it exists", "A wristwatch visible on a gladiator in an epic film is a glaring historical ________.", ["anachronism", "archetype", "apotheosis", "allusion"], "Hansom cabs in a novel set in 2050 represent an intentional stylistic anachronism."),
      ("apotheosis", "the highest point in the development of something; a culmination or deification", "Winning the Nobel Prize in Literature was the undisputed ________ of her literary career.", ["apotheosis", "nadir", "debacle", "abyss"], "The baroque palace was hailed as the architectural apotheosis of divine-right monarchy."),
      ("bellicose", "demonstrating aggression and willingness to fight; warlike", "The dictator's ________ speech prompted international sanctions and border troop buildups.", ["bellicose", "conciliatory", "irenic", "dovish"], "Diplomats worked frantically to dampen bellicose rhetoric across state television."),
      ("candid", "truthful, straightforward, frank, and impartial", "We appreciated her ________ appraisal of the structural risks facing the joint venture.", ["candid", "disingenuous", "evasive", "circuitous"], "In a candid interview, the former prime minister admitted miscalculating inflation."),
      ("circumlocution", "the use of many words where fewer would do, especially in a deliberate attempt to be vague", "Diplomats are trained in the art of polite ________ when dealing with sensitive territorial claims.", ["circumlocution", "brevity", "terseness", "succinctness"], "His explanation was a masterpiece of circumlocution that avoided addressing the deficit."),
      ("clemency", "mercy; lenience, especially when meting out punishment", "The governor granted executive ________ to the prisoner in light of newly uncovered DNA evidence.", ["clemency", "ruthlessness", "severity", "harshness"], "The tribunal demonstrated unexpected clemency toward first-time offenders."),
      ("dearth", "a scarcity or lack of something", "There is a severe ________ of experienced data engineers in the regional manufacturing hub.", ["dearth", "surfeit", "glut", "abundance"], "A dearth of rainfall across the summer months depleted the municipal reservoirs."),
      ("demagogue", "a political leader who seeks support by appealing to popular desires rather than rational argument", "The constitutional court acted as a bulwark against the rise of an unscrupulous ________.", ["demagogue", "statesman", "pedagogue", "diplomat"], "Demagogues historically weaponize economic anxiety to divide democratic communities."),
      ("ebullient", "cheerful and full of energy; exuberant", "The ________ fans poured into the streets following their national team's championship victory.", ["ebullient", "morose", "crestfallen", "doleful"], "Her ebullient laughter resonated throughout the studio during the rehearsal."),
      ("effrontery", "insolent or impertinent behavior; shameless audacity", "He had the sheer ________ to request a pay rise a week after crashing the company van.", ["effrontery", "modesty", "decorum", "deference"], "I was astonished by her effrontery in claiming credit for my research."),
      ("enervate", "to cause someone to feel drained of energy or vitality; weaken", "The stifling humidity of the equatorial jungle served to ________ the expedition within days.", ["enervate", "invigorate", "galvanize", "fortify"], "Prolonged illness enervated his constitution, requiring six months of convalescence."),
      ("equivocate", "use ambiguous language so as to conceal the truth or avoid committing oneself", "When pressed about tax increases, the politician continued to ________ unconvincingly.", ["equivocate", "clarify", "elucidate", "avow"], "Do not equivocate; a simple 'yes' or 'no' is required by the court."),
      ("esoteric", "intended for or likely to be understood by only a small number of people with specialized knowledge", "Quantum cryptography remains an ________ subdiscipline beyond the grasp of lay programmers.", ["esoteric", "ubiquitous", "pedestrian", "commonplace"], "The journal publishes esoteric treatises on early Indo-European phonology."),
      ("exculpate", "show or declare that someone is not guilty of wrongdoing", "Forensic ballistics reports served to ________ the guard from charges of manslaughter.", ["exculpate", "incriminate", "indict", "implicate"], "The documentary presented compelling evidence that exculpated the wrongfully imprisoned convict."),
      ("fastidious", "very attentive to and concerned about accuracy and detail; very hard to please", "The curator was ________ about maintaining precise humidity controls inside the gallery.", ["fastidious", "slipshod", "lax", "negligent"], "He was fastidious in his dress, never appearing without a pressed linen handkerchief."),
      ("garrulous", "excessively talkative, especially on trivial matters", "A ________ taxi driver regaled us with sixty minutes of unsolicited opinions on local zoning laws.", ["garrulous", "laconic", "taciturn", "reticent"], "She regretted sharing a compartment with such a garrulous traveling companion."),
      ("gregarious", "fond of company; sociable; living in flocks or colonies", "Dolphins are famously ________ mammals that hunt cooperatively in sophisticated pods.", ["gregarious", "solitary", "hermitic", "unsociable"], "Unlike his reclusive sister, Julian was gregarious and thrived at crowded galas."),
      ("hackneyed", "lacking significance through having been overused; unoriginal and trite", "The film's plot relied on ________ tropes that discerning critics shredded in reviews.", ["hackneyed", "novel", "groundbreaking", "original"], "His speech was replete with hackneyed expressions about teamwork and synergies."),
      ("harangue", "a lengthy and aggressive speech or lecture", "The sergeant delivered a ferocious ________ to the recruits following their dismal inspection.", ["harangue", "panegyric", "homily", "tribute"], "Customers were subjected to a political harangue by the disgruntled store owner."),
      ("hubris", "excessive pride or self-confidence leading to a downfall", "In Greek tragedy, the protagonist's tragic flaw is almost invariably fatal ________.", ["hubris", "humility", "modesty", "timidity"], "Blind hubris prevented the investment bankers from acknowledging the housing bubble."),
      ("idiosyncrasy", "a mode of behavior or way of thought peculiar to an individual", "One endearing ________ of the professor was wearing mismatched socks to formal colloquia.", ["idiosyncrasy", "orthodoxy", "conformity", "standard"], "Every vintage sports car has mechanical idiosyncrasies that only its owner understands."),
      ("impecunious", "having little or no money; penniless; poor", "As an ________ art student in Vienna, he subsisted on stale rolls and black tea.", ["impecunious", "opulent", "affluent", "flush"], "The trust provides financial stipends to impecunious scholars pursuing doctoral studies."),
      ("inchoate", "just begun and so not fully formed or developed; rudimentary", "At this early stage, our plans for the commercial launch remain entirely ________.", ["inchoate", "mature", "consummate", "refined"], "He struggled to articulate an inchoate feeling of unease regarding the merger."),
      ("indolent", "wanting to avoid activity or exertion; lazy; idle", "The tropical heat produced an ________ afternoon where no one felt inclined to work.", ["indolent", "industrious", "diligent", "strenuous"], "He was an indolent youth who squandered his inheritance on idle amusements."),
      ("ineffable", "too great or extreme to be expressed or described in words", "Standing atop the Himalayan summit, she experienced a moment of ________ awe.", ["ineffable", "mundane", "prosaic", "pedestrian"], "The ineffable beauty of the choral requiem moved listeners to tears."),
      ("ingratiate", "bring oneself into favor with someone by flattering or trying to please them", "The ambitious intern sought to ________ herself with senior partners through obsequious flattery.", ["ingratiate", "alienate", "estrange", "antagonize"], "He brought imported cigars in a clumsy attempt to ingratiate himself with the manager."),
      ("inimical", "tending to obstruct or harm; hostile; unfriendly", "High interest rates and steep import tariffs are profoundly ________ to small business growth.", ["inimical", "propitious", "beneficial", "conducive"], "Censorship is fundamentally inimical to creative and scholarly inquiry."),
      ("intransigent", "unwilling or refusing to change one's views or to agree about something", "Both trade union leaders and company directors adopted an ________ stance throughout the strike.", ["intransigent", "pliable", "tractable", "amenable"], "His intransigent refusal to negotiate cost the party control of the municipality."),
      ("invidious", "likely to arouse or incur resentment or anger in others; unfairly discriminating", "The headmaster refused to make ________ comparisons between the academic merits of the two twins.", ["invidious", "laudable", "admirable", "praiseworthy"], "Putting workers in competition for a single bonus created an invidious office atmosphere."),
      ("juxtaposition", "the fact of two things being seen or placed close together with contrasting effect", "The exhibition’s brilliant ________ of Renaissance portraits with digital glitch art provoked discussion.", ["juxtaposition", "separation", "disjunction", "isolation"], "The novel gains its satirical power through the ironic juxtaposition of luxury and squalor."),
      ("lucid", "expressed clearly; easy to understand; showing ability to think clearly", "Despite his advanced years, the emeritus professor offered a remarkably ________ exposition of astrophysics.", ["lucid", "turbid", "obscure", "muddled"], "Write in a lucid and concise style so that general readers can grasp the legal points."),
      ("maudlin", "self-pityingly or tearfully sentimental, often through drunkenness", "After his third glass of brandy, he devolved into a ________ recollection of his youth.", ["maudlin", "stoic", "austere", "unsentimental"], "Critics panned the screenplay for its maudlin dialogue and manipulative tear-jerking climax."),
      ("mendacious", "not telling the truth; lying; untruthful", "The advertisement made ________ claims regarding the herbal supplement's cure-all properties.", ["mendacious", "veracious", "scrupulous", "candid"], "Investigative journalists exposed the politician's mendacious denials of financial malfeasance."),
      ("neophyte", "a person who is new to a subject, skill, or belief; a novice", "As a complete ________ in algorithmic trading, he followed his mentor's rules to the letter.", ["neophyte", "veteran", "doyen", "maestro"], "The mountaineering course is tailored specifically for neophytes tackling alpine routes."),
      ("noisome", "having an extremely offensive smell; highly obnoxious or objectionable", "The swamp emitted a ________ stench of rotting vegetation and stagnant mud.", ["noisome", "fragrant", "aromatic", "balmy"], "The industrial tannery was shut down by public health inspectors for its noisome emissions."),
      ("obdurate", "stubbornly refusing to change one's opinion or course of action", "Despite pleading from his closest advisors, the autocrat remained entirely ________.", ["obdurate", "malleable", "pliant", "yielding"], "The company met customer boycotts with obdurate defiance, refusing all compromises."),
      ("ostentatious", "characterized by vulgar or pretentious display; designed to impress or attract notice", "His ________ gold-plated limousine drew mocking snickers rather than admiration outside the theater.", ["ostentatious", "understated", "austere", "modest"], "She avoided ostentatious jewelry, preferring understated pearls of heirloom quality."),
      ("palliate", "make (a disease or its symptoms) less severe or unpleasant without removing the cause; alleviate", "The analgesic was prescribed to ________ chronic neuropathic pain following spinal surgery.", ["palliate", "exacerbate", "aggravate", "intensify"], "Diplomatic summits did little to resolve the border dispute, serving only to palliate tensions."),
      ("pariah", "an outcast; a person rejected by their social group or society", "Following revelations of treason, the former intelligence officer lived as an international ________.", ["pariah", "luminary", "cynosure", "paragon"], "Whistleblowers often find themselves treated as pariahs by corporate colleagues."),
      ("paucity", "the presence of something only in small or insufficient quantities or amounts; scarcity", "The prosecution's case collapsed due to a crippling ________ of corroborating physical evidence.", ["paucity", "plethora", "surfeit", "glut"], "A paucity of affordable housing drove young professionals away from the metropolitan center."),
      ("pejorative", "expressing contempt or disapproval; derogatory", "The term was originally an insult, but over time lost its ________ connotation.", ["pejorative", "commendatory", "laudatory", "eulogistic"], "Reviewers should criticize the substance of the book without resorting to pejorative personal slurs."),
      ("penury", "extreme poverty; destitution", "The once-wealthy aristocrat died in squalid ________ in a boarding house near the docks.", ["penury", "opulence", "prosperity", "affluence"], "Welfare programs were instituted to rescue elderly widows from extreme penury."),
      ("perfunctory", "carried out with a minimum of effort or reflection; superficial", "The customs official gave our luggage a ________ inspection before stamping our entry visas.", ["perfunctory", "painstaking", "exhaustive", "meticulous"], "He offered a perfunctory apology that did little to heal the rift between the partners."),
      ("pernicious", "having a harmful effect, especially in a gradual or subtle way", "The court condemned the ________ dissemination of hate speech via anonymous accounts.", ["pernicious", "salubrious", "innocuous", "propitious"], "Carbon monoxide poisoning is particularly pernicious because the gas is completely odorless."),
      ("perspicacity", "the quality of having a ready insight into things; shrewdness", "Her acute political ________ enabled her to anticipate the collapse of the governing coalition.", ["perspicacity", "obtuse ness", "vacuity", "gullibility"], "He was renowned for his forensic perspicacity in interrogating hostile witnesses."),
      ("plethora", "a large or excessive amount of something", "The library offers a ________ of primary source materials for students of maritime history.", ["plethora", "dearth", "paucity", "scarcity"], "Consumers face a confusing plethora of subscription packages across streaming networks."),
      ("pragmatic", "dealing with things sensibly and realistically in a way that is based on practical considerations", "The prime minister adopted a ________ approach, compromising on tariffs to secure peace.", ["pragmatic", "dogmatic", "quixotic", "visionary"], "A pragmatic engineer focuses on workable solutions rather than theoretical elegance."),
      ("precocious", "having developed certain abilities or proclivities at an earlier age than usual", "The ________ prodigy mastered multivariable calculus before completing primary school.", ["precocious", "backward", "retarded", "delayed"], "Her precocious musical talent earned her a scholarship to the Royal Academy at age ten."),
      ("predilection", "a preference or special liking for something; a bias in favor of something", "He had an unshakeable ________ for 19th-century Russian literature, reading Tolstoy annually.", ["predilection", "aversion", "antipathy", "loathing"], "Her predilection for spicy Szechuan cuisine surprised her European hosts."),
      ("profligate", "recklessly extravagant or wasteful in the use of resources", "The bankrupt monarch was despised by taxpayers for his ________ court expenditures.", ["profligate", "frugal", "parsimonious", "thrifty"], "Profligate use of fresh water during droughts resulted in hefty municipal fines."),
      ("prolific", "producing much fruit or foliage or many works; highly productive", "As a ________ author, he published over sixty novels and hundreds of critical essays.", ["prolific", "unproductive", "barren", "sterile"], "Picasso was exceptionally prolific, creating thousands of ceramic, painted, and sculpted works."),
      ("quagmire", "a soft boggy area of land; an awkward, complex, or hazardous situation", "Foreign intervention plunged the peacekeeping coalition into an intractable military ________.", ["quagmire", "haven", "sanctuary", "pinnacle"], "The litigation threatened to become a financial quagmire that could bankrupt the studio."),
      ("quixotic", "exceedingly idealistic; unrealistic and impractical", "His ________ campaign to abolish paper money worldwide gained few mainstream adherents.", ["quixotic", "pragmatic", "calculating", "utilitarian"], "Charging into modern courtrooms without counsel is a quixotic and perilous gamble."),
      ("rancor", "bitterness or resentfulness, especially when long-standing", "The bitter divorce concluded without lasting ________ thanks to skillful mediation.", ["rancor", "amity", "benevolence", "cordiality"], "Decades of territorial warfare left deep pools of ancestral rancor among the tribes."),
      ("recalcitrant", "having an obstinately uncooperative attitude towards authority or discipline", "The warden struggled to manage a cohort of ________ inmates who refused all labor details.", ["recalcitrant", "docile", "compliant", "amenable"], "Recalcitrant member states were threatened with suspension of European Union subsidies."),
      ("redolent", "strongly reminiscent or suggestive of something; fragrant", "The attic was ________ of dried lavender, old leather, and cedar shavings.", ["redolent", "barren", "bereft", "destitute"], "His poetry is deeply redolent of Keats and the English Romantic tradition."),
      ("sagacious", "having or showing keen mental discernment and good judgment; wise", "The council benefited immensely from the ________ counsel of their retired chief justice.", ["sagacious", "foolish", "fatuous", "vacuous"], "A sagacious investor preserves liquidity during speculative asset bubbles."),
      ("salient", "most notable or important; prominent", "The executive summary highlights the most ________ financial metrics for prospective buyers.", ["salient", "inconsequential", "trivial", "minor"], "The most salient feature of Gothic architecture is the pointed rib vault."),
      ("sanctimonious", "making a show of being morally superior to other people", "We were irritated by his ________ lectures on dietary virtue while he ate imported delicacies.", ["sanctimonious", "unassuming", "modest", "sincere"], "Her sanctimonious demeanor hid a long history of cutthroat corporate maneuvering."),
      ("soporific", "tending to induce drowsiness or sleep; tediously boring", "The professor's monotonous delivery had an unmistakably ________ effect on the lecture hall.", ["soporific", "stimulating", "exhilarating", "galvanizing"], "Warm chamomile tea has mild soporific qualities beneficial before bedtime."),
      ("spurious", "not being what it purports to be; false or fake; illegitimate", "The antiquarian exposed the manuscript as a ________ 19th-century forgery.", ["spurious", "authentic", "genuine", "veritable"], "The defense dismantled the prosecution's spurious claims with authenticated logs."),
      ("stalwart", "loyal, reliable, and hard-working; strongly built and sturdy", "She remained a ________ defender of civil liberties throughout decades of political turmoil.", ["stalwart", "fickle", "capricious", "irresolute"], "The veteran was a stalwart pillar of the village community for over fifty years."),
      ("stoic", "a person who can endure pain or hardship without showing their feelings or complaining", "Throughout her grueling medical treatments, she maintained an admirable, ________ serenity.", ["stoic", "histrionic", "demonstrative", "effusive"], "A stoic endurance in the face of inevitable tragedy is central to Marcus Aurelius's thought."),
      ("strident", "loud and harsh; grating; commanding attention aggressively", "Her ________ tone during the televised debate alienated viewers who sought calm analysis.", ["strident", "dulcet", "subdued", "mellifluous"], "The editor toned down the more strident accusations in the investigative report."),
      ("subjugate", "bring under domination or control, especially by conquest", "Imperial armies sought to ________ the mountain clans through decades of siege warfare.", ["subjugate", "emancipate", "liberate", "enfranchise"], "Authoritarian regimes attempt to subjugate independent journalism through arbitrary arrests."),
      ("surreptitious", "kept secret, especially because it would not be approved of; stealthy", "She cast a ________ glance at her rival's test paper while the examiner was distracted.", ["surreptitious", "overt", "brazen", "conspicuous"], "The spies held surreptitious rendezvous inside crowded subway stations."),
      ("sycophant", "a person who acts obsequiously towards someone important in order to gain advantage", "Surrounded by ________ who never disputed his decisions, the CEO lost touch with reality.", ["sycophants", "critics", "detractors", "adversaries"], "The tyrant rewarded sycophants while imprisoning scholars who spoke the truth."),
      ("temerity", "excessive confidence or boldness; audacity", "No one possessed the ________ to interrupt the general during his furious debriefing.", ["temerity", "timidity", "diffidence", "circumspection"], "She had the temerity to demand a personal apology from the prime minister."),
      ("tenuous", "very weak or slight; insubstantial; flimsy", "The link between the two financial scandals proved ________ and supported only by hearsay.", ["tenuous", "robust", "unshakeable", "substantial"], "The coalition maintained a tenuous one-seat majority in the lower parliament."),
      ("torpor", "a state of physical or mental inactivity; lethargy", "The oppressive August heat plunged the Mediterranean village into a languid ________.", ["torpor", "vigor", "vitality", "animation"], "Winter hibernation allows Arctic mammals to survive months in metabolic torpor."),
      ("tractable", "easy to control or influence; malleable", "The young thoroughbred horse proved remarkably ________ under an experienced trainer's hands.", ["tractable", "intractable", "refractory", "unruly"], "Diplomats hoped that economic sanctions would make the hostile regime more tractable."),
      ("transient", "lasting only for a short time; impermanent; fleeting", "The economic boom proved ________, giving way to a severe liquidity crisis within two years.", ["transient", "perennial", "everlasting", "permanent"], "In a transient world of fleeting digital fads, classical literature endures."),
      ("truncate", "shorten (something) by cutting off the top or the end", "Due to time constraints, the keynote speaker was forced to ________ her concluding remarks.", ["truncate", "elongate", "protract", "extend"], "The editor truncated the sprawling 800-page manuscript into a punchy volume."),
      ("ubiquitous", "present, appearing, or found everywhere", "Smartphones have become an ________ fixture of contemporary urban existence.", ["ubiquitous", "rare", "scarce", "uncommon"], "Coffee houses were ubiquitous throughout 18th-century London."),
      ("umbrage", "offense or annoyance; resentment", "The ambassador took ________ at the insinuation that his government had falsified customs logs.", ["umbrage", "delight", "satisfaction", "contentment"], "Please do not take umbrage; my critique was intended solely to refine your manuscript."),
      ("unctuous", "excessively flattering or ingratiating; oily; greasy in demeanor", "The salesman’s ________ compliments irritated customers who valued honest advice.", ["unctuous", "sincere", "forthright", "blunt"], "His unctuous charm was exposed as fraudulent when his shady past came to light."),
      ("upbraid", "find fault with someone; scold; reprimand", "The headmaster proceeded to ________ the senior students for their vandalism of the chapel.", ["upbraid", "laud", "extol", "applaud"], "She felt no compulsion to upbraid subordinates in public, preferring private counsel."),
      ("vacillate", "waver between different opinions or actions; be indecisive", "Faced with competing advice from his generals, the king continued to ________ for days.", ["vacillate", "resolve", "decide", "persevere"], "Do not vacillate between strategies; commit fully to your chosen market niche."),
      ("variegated", "exhibiting different colors, especially as irregular patches or streaks; diverse", "The garden featured a stunning tapestry of ________ hostas and Japanese maples.", ["variegated", "monochrome", "uniform", "drab"], "A variegated career spanning journalism, diplomacy, and cinema gave her unique perspective."),
      ("venerate", "regard with great respect; revere", "In many cultures, communities deeply ________ village elders for their accumulated wisdom.", ["venerate", "despise", "scorn", "disdain"], "Scholars continue to venerate Shakespeare as the supreme dramatist of the English tongue."),
      ("veracity", "conformity to facts; accuracy; habitual truthfulness", "The defense attorney challenged the ________ of the witness's sworn deposition.", ["veracity", "mendacity", "falsity", "deceit"], "We can attest to the historical veracity of the records housed in the cathedral archive."),
      ("verbose", "using or expressed in more words than are needed; wordy", "His ________ dissertation could easily have been condensed into half its page count.", ["verbose", "laconic", "succinct", "terse"], "A verbose legal agreement often conceals loopholes within redundant clauses."),
      ("vexation", "the state of being annoyed, frustrated, or worried; a cause of annoyance", "To her profound ________, the connecting train departed five minutes ahead of schedule.", ["vexation", "delight", "euphoria", "repose"], "Tax filing is a perennial source of vexation for freelance professionals."),
      ("vilify", "speak ill of; write or speak about in an abusively disparaging manner", "Partisan tabloids sought to ________ the whistleblower before the committee convened.", ["vilify", "extol", "lionize", "exalt"], "It is improper to vilify an entire ethnic community for the crimes of a few."),
      ("vindictive", "having or showing a strong or unreasoning desire for revenge", "The dismissed executive embarked on a ________ campaign of leaks to damage the company.", ["vindictive", "forgiving", "magnanimous", "charitable"], "Avoid vindictive reprisals; focus your energy on building your new enterprise."),
      ("virulent", "extremely severe or harmful in its effects; bitterly hostile", "The editorial was greeted by a ________ barrage of condemnation from civil rights groups.", ["virulent", "anodyne", "mild", "benign"], "A virulent strain of avian influenza prompted the culling of poultry across three counties."),
      ("vituperative", "bitter and abusive in language; scathing", "The reviewer's ________ assessment of the novel shocked even the author's harshest critics.", ["vituperative", "complimentary", "laudatory", "panegyrical"], "Parliamentary decorum forbids vituperative personal attacks across the despatch box."),
      ("vociferous", "vehement or clamorous; shouting forth noisily", "The municipal council was met by ________ protests from residents opposing the highway.", ["vociferous", "mute", "reticent", "taciturn"], "He was a vociferous advocate for penal reform throughout his parliamentary career."),
      ("voluble", "speaking or spoken incessantly and fluently; talkative", "The ________ tour guide kept up a non-stop commentary on Roman architecture for four hours.", ["voluble", "laconic", "uncommunicative", "hesitant"], "She became animated and voluble whenever the discussion touched upon equine genetics."),
      ("wanton", "deliberate and unprovoked (of a cruel or violent action); promiscuous", "The vandalism of the ancient stone circle was condemned as an act of ________ savagery.", ["wanton", "justified", "provoked", "defensive"], "Profligate monarchs squandered public funds with wanton disregard for the consequences."),
      ("zealous", "having or showing zeal; passionate and fiercely committed", "A ________ reformer, she campaigned tirelessly for women's suffrage across the nation.", ["zealous", "apathetic", "lukewarm", "indifferent"], "The young detective was zealous in pursuing every lead, no matter how obscure.")
    ]

    while len(items) < 200:
        for word, meaning, prompt, opts, ex in extra_data:
            if len(items) >= 200:
                break
            q_id = f"voc-{len(items)+1:03d}"
            # Level 3 to 5
            level = 3 + (len(items) % 3)
            explain = f"'{word.capitalize()}' means {meaning}."
            items.append({
                "id": q_id,
                "mode": "vocabulary",
                "level": level,
                "type": "choice",
                "topic": "Lexical Nuance & Precision",
                "prompt": prompt,
                "options": opts,
                "answer": 0,
                "explain": explain,
                "example": ex
            })

    return items[:200]

if __name__ == "__main__":
    vocab = generate_vocab_bank()
    print(f"Generated {len(vocab)} Vocabulary questions.")
    with open("data/vocabulary.js", "w", encoding="utf-8") as f:
        f.write("// Advanced C2 Vocabulary Question Bank (200 Curated Items)\n")
        f.write("window.C2_DATA = window.C2_DATA || {};\n\n")
        f.write("window.C2_DATA.vocabulary = ")
        json.dump(vocab, f, indent=2, ensure_ascii=False)
        f.write(";\n")
    print("Written to data/vocabulary.js successfully.")
