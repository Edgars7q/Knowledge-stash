/* Public quick cards are paired with full lessons through lessonId. */
window.STARTER_IDEAS = [
  {
    "id": "quick-prices",
    "lessonId": "econ-prices",
    "category": "Business",
    "title": "A higher price can tell two different stories",
    "hook": "Did buyers want more, or did suppliers become less able to produce?",
    "body": "In a simplified competitive market, stronger demand raises both equilibrium price and traded quantity. A supply decrease raises price but lowers quantity. The cause matters: a failed harvest shifts supply, while the resulting higher price changes buying along the demand curve. A price change alone does not identify which curve moved.",
    "example": "For demand P = 100 − 0.5Q and supply P = 20 + 0.5Q, equilibrium is 80 crates at €60 each. Raising the supply intercept to 44 gives 56 crates at €72. These invented values isolate one mechanism; real markets also have contracts, inventories and other constraints.",
    "takeaway": "Identify what changed first, then trace the effects on price and quantity.",
    "question": "If customer demand and production costs both rise, is the direction of traded quantity certain?"
  },
  {
    "id": "e1",
    "lessonId": "eng-faults",
    "category": "Engineering",
    "title": "A command is not proof of movement",
    "hook": "A PLC output can be ON while the machine stays still.",
    "body": "Reliable diagnostics compare a command with independent feedback. A cylinder should first leave its home sensor, then reach its end sensor within measured time limits. Watching both events separates failure to begin from failure to finish. A missing signal narrows the investigation; it does not prove that a particular component is broken.",
    "example": "The home sensor goes OFF after 0.2 seconds, but the end sensor is still OFF at 3.0 seconds. Arrival is unconfirmed. The actuator may be slow or blocked, or the end sensor may have failed. These are teaching timings, not universal settings or safety-rated protection.",
    "takeaway": "State the measured failure before naming an unverified cause.",
    "question": "What extra observation could help distinguish a mechanical jam from a failed end sensor?"
  },
  {
    "id": "p2",
    "lessonId": "psy-memory",
    "category": "Psychology",
    "title": "Familiar is not the same as remembered",
    "hook": "An answer can feel obvious on the page and disappear when you need it.",
    "body": "Rereading supplies recognition cues. Retrieval practice asks you to reconstruct an answer without those cues, revealing gaps and strengthening later access to successfully retrieved material. Feedback matters: check an attempted explanation against accurate information before repeating it. Spacing these attempts across sessions often improves retention compared with the same practice crowded together.",
    "example": "After studying a formula, close the explanation and describe its variables from memory. Check your answer, correct missing steps, then use the formula in a new problem a few days later. Adjust the delay if recall is impossible; no single schedule suits every learner and topic.",
    "takeaway": "Learn, retrieve, check and revisit. Familiarity alone is weak evidence of understanding.",
    "question": "Could you explain this idea with your notes closed and an example you have not already seen?"
  },
  {
    "id": "s3",
    "lessonId": "sci-turbulence",
    "category": "Science",
    "title": "Faster flow is not the whole turbulence story",
    "hook": "Speed matters, but the fluid, geometry and disturbances matter too.",
    "body": "Reynolds number compares inertial and viscous effects. For a round jet it can be written Re = U × D / ν, using nozzle speed U, diameter D and kinematic viscosity ν. The units cancel. A high value suggests strong inertial effects at that scale; it is not a universal switch that predicts every detail of turbulence.",
    "example": "For air with ν = 1.5 × 10⁻⁵ m²/s, D = 0.040 m and U = 20 m/s, Re is about 53,300. Doubling speed doubles Re. It does not establish that jet spreading or turbulent fluctuations also double; those outcomes require further analysis or measurements.",
    "takeaway": "Use the right length scale and geometry before comparing Reynolds numbers.",
    "question": "Why might equal Reynolds numbers fail to make a pipe flow and a free jet behave identically?"
  },
  {
    "id": "quick-gps",
    "lessonId": "space-gps",
    "category": "Space",
    "title": "GPS depends on clocks that disagree",
    "hook": "Tiny differences in elapsed time become large differences in signal-travel distance.",
    "body": "A GPS receiver uses satellite signal timing to estimate ranges, then solves for position and its own clock offset. Satellite motion makes GPS clocks run roughly 7 microseconds per day slower than an Earth-surface reference; higher gravitational potential makes them run about 45 microseconds faster. The approximate net effect is +38 microseconds per day, which the navigation system must account for.",
    "example": "Light travels about 300 metres in one microsecond. Multiplying that by 38 gives 11,400 metres, or 11.4 km. This is a light-travel distance scale, not an exact daily position error for every receiver: geometry, clock estimation and other corrections also matter.",
    "takeaway": "Keep the signs, units and reference conditions when interpreting a striking physics claim.",
    "question": "Would a satellite in a different orbit necessarily need the same clock correction as GPS?"
  },
  {
    "id": "quick-arguments",
    "lessonId": "phil-arguments",
    "category": "Philosophy",
    "title": "A true conclusion can come from invalid reasoning",
    "hook": "A claim may turn out to be right even when the reasons offered do not establish it.",
    "body": "A deductively valid argument has a structure that cannot lead from true premises to a false conclusion. A sound argument is valid and has true premises. To test validity, look for a possible counterexample: a situation where the premises hold but the conclusion fails. Finding one exposes the gap without proving that the conclusion is always false.",
    "example": "If it rains, the ground gets wet. The ground is wet, so it rained. Sprinklers provide a counterexample: the ground could be wet without rain. It may actually have rained, but these premises alone do not establish that conclusion.",
    "takeaway": "Evaluate the inference separately from whether you agree with the conclusion.",
    "question": "What alternative explanation would challenge an argument you have recently found convincing?"
  },
  {
    "id": "f2",
    "lessonId": "faith-suffering",
    "category": "Faith & ideas",
    "title": "Suffering raises more than one question",
    "hook": "An argument about belief and a person in pain may call for different kinds of response.",
    "body": "The logical problem asks whether suffering and belief in a good, all-powerful God are inconsistent. The evidential problem asks whether suffering counts against that belief. A personal question asks how to support someone in pain. A free-will defence may address harm caused by human choices; it does not by itself explain every disease or natural disaster.",
    "example": "After a bereavement, listening and practical compassion are usually more appropriate than abstract debate. In a seminar, examine what a proposed defence establishes and what remains unanswered. A possible general reason is not knowledge of why a particular person suffered.",
    "takeaway": "Identify the question, the argument’s limits and the needs of the person asking.",
    "question": "How would your response change between an academic discussion and a conversation with a grieving friend?"
  },
  {
    "id": "h4",
    "lessonId": "hist-rail-time",
    "category": "History",
    "title": "Railways made local noon a network problem",
    "hook": "A useful town clock convention became confusing when distant stations had to coordinate.",
    "body": "Earth turns roughly 360 degrees in 24 hours, so one degree of longitude corresponds to about four minutes of mean solar time. Neighbouring towns could therefore keep different local times. Railways needed shared references for timetables and operations; telegraphs helped distribute them. Modern civil time zones are administrative conventions, not direct consequences of longitude alone.",
    "example": "Two towns five degrees apart have local solar times about twenty minutes apart. North American railways adopted standard railway time zones in 1883; the 1884 International Meridian Conference recommended Greenwich as the prime meridian. Neither event instantly established every modern legal time zone.",
    "takeaway": "When local systems connect, their conventions need shared references and explicit agreements.",
    "question": "How could comparing computer logs without their time-zone references create the same kind of confusion?"
  }
];

/* Historical cards are retained only for existing bookmarks and reviews.
   Do not list these as new public quick cards. */
window.KS_LEGACY_IDEAS = [
  {
    "id": "p1",
    "category": "Psychology",
    "title": "The illusion of explanatory depth",
    "hook": "Knowing the name of a thing is not the same as understanding it.",
    "body": "We tend to overestimate how well we understand familiar systems. Trying to explain a mechanism step by step often exposes gaps that confidence alone hides.",
    "example": "Try explaining how a bicycle stays balanced, or how a refrigerator transfers heat, without skipping a step.",
    "takeaway": "Test understanding by explaining how something works, not by recognising it.",
    "question": "What everyday object could you explain from first principles?"
  },
  {
    "id": "e1",
    "category": "Engineering",
    "title": "Feedback is what makes control reliable",
    "hook": "A command tells a machine what to do. Feedback tells us what it actually did.",
    "body": "In open-loop control, the controller issues a command without measuring the outcome. Closed-loop control uses a sensor to compare the measured response with the target and correct the error.",
    "example": "A thermostat checks room temperature after switching on the heater; a PLC checks whether a cylinder reached its end sensor.",
    "takeaway": "An output signal is not proof that the physical action completed.",
    "question": "Where could adding feedback make a machine safer?"
  },
  {
    "id": "s1",
    "category": "Science",
    "title": "Entropy is about energy spreading out",
    "hook": "Why does a hot drink cool down on its own, but never spontaneously heat itself?",
    "body": "In an isolated system, entropy tends to increase. One useful interpretation is that energy becomes more dispersed among the available microscopic states.",
    "example": "Heat flows from hot tea into cooler air until the temperatures become more similar.",
    "takeaway": "Natural processes tend toward states with more accessible microscopic arrangements.",
    "question": "How would a refrigerator move heat against that natural direction?"
  },
  {
    "id": "sp1",
    "category": "Space",
    "title": "Looking into space is looking into the past",
    "hook": "Distant objects are seen as they were, not exactly as they are now.",
    "body": "Light travels at a finite speed. The farther away a source is, the longer its light takes to reach us, so observations capture an earlier moment.",
    "example": "We see the Sun roughly eight minutes in the past because its light takes about that long to reach Earth.",
    "takeaway": "Distance in astronomy also represents look-back time.",
    "question": "What does this mean for observing an extremely distant galaxy?"
  },
  {
    "id": "ph1",
    "category": "Philosophy",
    "title": "The map is not the territory",
    "hook": "A model is useful because it simplifies reality—and that is also its limitation.",
    "body": "Maps, equations and mental frameworks omit details to highlight what matters. Trouble starts when we confuse a simplified representation with the full system.",
    "example": "A mechanical model may treat a beam as perfectly rigid even though every real beam deforms.",
    "takeaway": "Ask which assumptions make a model useful and when they break down.",
    "question": "What important information does a KPI dashboard leave out?"
  },
  {
    "id": "b1",
    "category": "Business",
    "title": "Goodhart’s law and broken targets",
    "hook": "When a measure becomes a target, people may optimise the number instead of the goal.",
    "body": "A metric can be a useful signal of performance. But when rewards depend heavily on it, behaviours can shift toward improving the measurement even when the underlying outcome worsens.",
    "example": "Reducing reported maintenance incidents can look good if workers stop logging small faults.",
    "takeaway": "Pair metrics with context, quality checks and real outcomes.",
    "question": "Which metric in your workplace could distort behaviour?"
  },
  {
    "id": "f1",
    "category": "Faith & ideas",
    "title": "The difference between belief and an argument",
    "hook": "Holding a view and supporting that view are two different tasks.",
    "body": "A belief is what someone accepts as true. An argument sets out premises and reasoning intended to justify a conclusion. Evaluating an argument requires examining both the evidence and the logical connection.",
    "example": "“The universe has a beginning” is a claim; an argument about its cause requires additional premises.",
    "takeaway": "Separate the conclusion from the reasons offered to support it.",
    "question": "What evidence would make you revise a deeply held belief?"
  },
  {
    "id": "h1",
    "category": "History",
    "title": "Why standards changed manufacturing",
    "hook": "Interchangeable parts made repair and large-scale production far easier.",
    "body": "When parts are produced to common specifications and tolerances, a replacement can fit without being individually shaped for one particular assembly.",
    "example": "A standardised bolt is easier to source and replace than a custom-threaded fastener.",
    "takeaway": "Standardisation enables scale, maintenance and collaboration.",
    "question": "Which modern industries depend most on interchangeability?"
  },
  {
    "id": "p2",
    "category": "Psychology",
    "title": "Spacing beats cramming for retention",
    "hook": "A little forgetting can make later recall more durable.",
    "body": "Spaced practice schedules review across time rather than compressing repetitions into one session. Retrieving a memory after an interval strengthens future access to it.",
    "example": "Reviewing a concept tomorrow, three days later and a week later often retains it better than rereading it five times today.",
    "takeaway": "Revisit knowledge shortly before it is likely to fade.",
    "question": "Which subject should you put on a review schedule?"
  },
  {
    "id": "e2",
    "category": "Engineering",
    "title": "Why engineers use safety factors",
    "hook": "A component can fail even if the calculated load seems acceptable.",
    "body": "Real-world properties and loads vary. A factor of safety provides a margin between estimated demand and capacity, but the appropriate margin depends on standards, uncertainty and consequences.",
    "example": "A bracket designed for only the expected static load may fail when impact or fatigue is introduced.",
    "takeaway": "Design margins address uncertainty; they do not replace good assumptions.",
    "question": "Which uncertainty would dominate the design of a lifting hook?"
  },
  {
    "id": "s2",
    "category": "Science",
    "title": "Correlation is not causation",
    "hook": "Two variables changing together do not establish a cause-and-effect link.",
    "body": "A third factor, reverse causality or coincidence may explain an observed relationship. Controlled experiments and careful causal reasoning are needed to test mechanisms.",
    "example": "Ice-cream sales and sunburn rise together largely because warm sunny weather affects both.",
    "takeaway": "Always ask what other variable might explain the pattern.",
    "question": "What extra evidence would strengthen a causal claim?"
  },
  {
    "id": "sp2",
    "category": "Space",
    "title": "Why rockets work in a vacuum",
    "hook": "A rocket does not need air to push against.",
    "body": "A rocket expels mass backward at high speed. Conservation of momentum means the rocket gains momentum in the opposite direction.",
    "example": "The same underlying principle makes a released inflated balloon move when air escapes.",
    "takeaway": "Rockets push on their own expelled propellant—not on surrounding air.",
    "question": "Why does propellant exhaust velocity matter so much?"
  },
  {
    "id": "ph2",
    "category": "Philosophy",
    "title": "The strongest version of the other view",
    "hook": "A weak opposing argument is easy to defeat and teaches you almost nothing.",
    "body": "The principle of charity encourages interpreting another person’s argument in a coherent, reasonable way before critiquing it.",
    "example": "Instead of arguing against a caricature of a policy, identify its strongest claimed benefit and test whether the evidence supports it.",
    "takeaway": "Understand a position at its strongest before rejecting it.",
    "question": "Which disagreement could benefit from this approach?"
  },
  {
    "id": "b2",
    "category": "Business",
    "title": "Bottlenecks determine throughput",
    "hook": "Speeding up the wrong step can increase work-in-progress without increasing output.",
    "body": "In a multistage process, the slowest constrained step often limits total output. Improving an unconstrained step may simply produce a larger queue ahead of the bottleneck.",
    "example": "Making a conveyor faster does not help if the packing station cannot handle more units.",
    "takeaway": "Find the constraint before deciding where to invest effort.",
    "question": "What evidence would reveal the real bottleneck in a shop?"
  },
  {
    "id": "f2",
    "category": "Faith & ideas",
    "title": "The problem of suffering has several forms",
    "hook": "An emotional question and a logical argument may need different answers.",
    "body": "Discussions of suffering can ask whether evil makes God’s existence logically impossible, whether it makes God less probable, or how a person can endure suffering. These are related but distinct questions.",
    "example": "A philosophical defence addresses consistency; pastoral support addresses someone’s immediate pain.",
    "takeaway": "Identify what kind of question is being asked before answering.",
    "question": "Which kind of response fits someone who has just suffered a loss?"
  },
  {
    "id": "h2",
    "category": "History",
    "title": "Navigation transformed global trade",
    "hook": "A more reliable position estimate changed the economics of exploration.",
    "body": "Latitude could be estimated using celestial observations; measuring longitude accurately at sea required reliable timekeeping or astronomical methods.",
    "example": "Comparing local solar time with a reference clock helps calculate east–west position.",
    "takeaway": "Sometimes one measurement technology unlocks an entire industry.",
    "question": "What would a navigation error cost a trading ship?"
  },
  {
    "id": "p3",
    "category": "Psychology",
    "title": "Confirmation bias selects the evidence",
    "hook": "We naturally notice what supports our existing view.",
    "body": "Confirmation bias describes a tendency to seek, interpret or remember information in ways that reinforce prior beliefs. Deliberately examining contrary evidence reduces the risk.",
    "example": "A manager who thinks a process is inefficient may notice only delays and overlook improved results.",
    "takeaway": "Actively search for observations that could disprove your explanation.",
    "question": "What result would falsify your current assumption?"
  },
  {
    "id": "e3",
    "category": "Engineering",
    "title": "Why a sensor needs a timeout",
    "hook": "A signal that never arrives can be as important as a signal that arrives unexpectedly.",
    "body": "Sequence diagnostics compare commands with expected feedback within defined time windows. Too-short windows cause nuisance faults; too-long windows delay detection.",
    "example": "After energising an extend valve, a controller expects the extended-limit sensor within a reasonable interval.",
    "takeaway": "A diagnostic needs an expected state, a time window and a defined response.",
    "question": "How would you set a reliable timeout for a pneumatic cylinder?"
  },
  {
    "id": "s3",
    "category": "Science",
    "title": "Reynolds number compares two effects",
    "hook": "It helps predict whether inertia or viscosity dominates fluid flow.",
    "body": "Reynolds number is a dimensionless ratio of inertial to viscous effects. The characteristic length and speed must match the specific flow geometry.",
    "example": "For flow through a round pipe, Reynolds number is often written as Re = ρVD/μ.",
    "takeaway": "Dimensionless groups let very different-sized systems be compared meaningfully.",
    "question": "Why would doubling pipe diameter change Reynolds number?"
  },
  {
    "id": "sp3",
    "category": "Space",
    "title": "A light-year measures distance",
    "hook": "Despite its name, it is not a unit of time.",
    "body": "A light-year is the distance light travels in vacuum during one Julian year. It is useful because interstellar distances are extremely large.",
    "example": "A star four light-years away is so distant that its light needs about four years to reach Earth.",
    "takeaway": "Astronomical units are chosen to make huge scales easier to reason about.",
    "question": "Why do astronomers also use parsecs?"
  },
  {
    "id": "ph3",
    "category": "Philosophy",
    "title": "Opportunity cost is a real cost",
    "hook": "Choosing one action means losing the benefits of your best alternative.",
    "body": "Opportunity cost measures the value of the next-best option you give up. It matters even when no money changes hands.",
    "example": "An hour spent scrolling is an hour not spent practicing a technical skill or resting.",
    "takeaway": "Assess decisions against the best foregone alternative, not against doing nothing.",
    "question": "What choice are you making repeatedly without noticing its cost?"
  },
  {
    "id": "b3",
    "category": "Business",
    "title": "A leading indicator gives earlier warning",
    "hook": "Results tell you what happened. Leading signals may tell you what comes next.",
    "body": "Lagging indicators measure completed outcomes; leading indicators track activities or conditions believed to influence future outcomes. Good leading indicators need validation.",
    "example": "Breakdown hours are lagging; overdue preventive-maintenance tasks may be an early warning.",
    "takeaway": "Combine outcome metrics with useful predictors.",
    "question": "Which daily measure might signal problems before a KPI declines?"
  },
  {
    "id": "f3",
    "category": "Faith & ideas",
    "title": "Historical and philosophical questions differ",
    "hook": "“What happened?” and “What does it mean?” require different methods.",
    "body": "Historical inquiry weighs sources, context and competing explanations. Philosophical inquiry examines concepts, premises and logical implications. Theological arguments may draw on both.",
    "example": "Evaluating an ancient text’s date differs from evaluating a moral argument drawn from it.",
    "takeaway": "Match the method of investigation to the kind of claim.",
    "question": "Is the question you are investigating historical, philosophical or both?"
  },
  {
    "id": "h3",
    "category": "History",
    "title": "The printing press changed the speed of ideas",
    "hook": "Reproducing information cheaply transformed how knowledge spread.",
    "body": "Movable-type printing in Europe greatly reduced the cost of reproducing many texts, supporting wider circulation of scientific, religious and political arguments.",
    "example": "Researchers could consult more similar copies of the same work and criticise each other’s findings.",
    "takeaway": "Information infrastructure shapes how quickly knowledge accumulates.",
    "question": "What modern technology has had a comparable effect?"
  },
  {
    "id": "p4",
    "category": "Psychology",
    "title": "Active recall beats passive rereading",
    "hook": "Remembering is a skill, not just a side effect of reading.",
    "body": "Retrieval practice makes you reconstruct an answer from memory. That effort helps reveal gaps and can improve long-term retention.",
    "example": "Close your notes and explain a formula’s variables and assumptions from memory.",
    "takeaway": "Quiz yourself before checking the answer.",
    "question": "What topic could you test yourself on right now?"
  },
  {
    "id": "e4",
    "category": "Engineering",
    "title": "Tolerance stacking explains assembly surprises",
    "hook": "Many acceptable parts can still make an unacceptable assembly.",
    "body": "A dimensional chain combines several manufacturing variations. Worst-case and statistical stack-up methods estimate how much the final fit can vary.",
    "example": "Five spacers each slightly thicker than nominal may create a clearance problem.",
    "takeaway": "Check the whole assembly, not only individual dimensions.",
    "question": "Where could tolerance stack-up cause a jam in a mechanism?"
  },
  {
    "id": "s4",
    "category": "Science",
    "title": "A scientific model is not a photograph",
    "hook": "A model is useful when its predictions are accurate within its domain.",
    "body": "Physical and numerical models use approximations. Validation compares model predictions with independent observations while documenting limitations.",
    "example": "A turbulence model can fit one jet experiment well but perform poorly in a different flow regime.",
    "takeaway": "Trust a model for demonstrated conditions, not for every imaginable use.",
    "question": "How would you validate a simulation against measurements?"
  },
  {
    "id": "sp4",
    "category": "Space",
    "title": "Orbiting is continuous falling",
    "hook": "Astronauts feel weightless because they and their spacecraft fall together.",
    "body": "An orbiting object is accelerated by gravity while moving sideways fast enough to keep missing the ground. Gravity does not disappear in low Earth orbit.",
    "example": "A ball thrown horizontally falls to Earth; at sufficiently high speed it follows Earth’s curvature.",
    "takeaway": "Orbital motion combines gravity with tangential velocity.",
    "question": "What changes when an orbiting spacecraft slows down?"
  },
  {
    "id": "ph4",
    "category": "Philosophy",
    "title": "A false dilemma hides alternatives",
    "hook": "Not every decision has only two legitimate options.",
    "body": "A false dilemma presents a limited set of choices as though they were exhaustive. Often a mixed approach, staged decision or third option exists.",
    "example": "“Either automate the whole process or keep everything manual” ignores partial automation.",
    "takeaway": "Before choosing A or B, ask whether the framing omitted C.",
    "question": "Which problem currently looks unnecessarily binary?"
  },
  {
    "id": "b4",
    "category": "Business",
    "title": "Small improvements compound",
    "hook": "Repeated small reductions in waste can create substantial cumulative benefits.",
    "body": "Continuous improvement favours observing a process, testing a small change, checking the result and retaining improvements that work.",
    "example": "Saving thirty seconds on a repeated task matters when the task occurs hundreds of times.",
    "takeaway": "Make improvement measurable and repeatable.",
    "question": "What small friction do you see every day?"
  },
  {
    "id": "f4",
    "category": "Faith & ideas",
    "title": "Analogy can clarify without proving",
    "hook": "A helpful comparison may explain an idea without establishing that it is true.",
    "body": "Analogies highlight similarities between familiar and unfamiliar subjects. But the differences may matter just as much as the similarities.",
    "example": "A watchmaker analogy can illustrate design reasoning, yet the conclusion needs its own support.",
    "takeaway": "Use analogies to understand arguments, then examine the actual evidence.",
    "question": "Where does your favourite analogy stop matching reality?"
  },
  {
    "id": "h4",
    "category": "History",
    "title": "Time zones were an engineering solution",
    "hook": "Standard time became increasingly useful when transport and communication sped up.",
    "body": "Before widespread standardisation, towns often kept local solar time. Railways and telegraphs made inconsistent local clocks a practical scheduling problem.",
    "example": "A train timetable spanning multiple towns becomes confusing if each station uses a different clock.",
    "takeaway": "Shared standards often arise when systems become interconnected.",
    "question": "What problems would appear if each city still kept its own time?"
  }
];
