# Zorost Signal: "The AI Engineering Skills Map, turned into a training plan"

> **Saved for internal reference** from https://zorost.com/ai-engineering-skills-map-training-guide
> Published 16 AUG 2026 · by Dr. Fereydun Hashemi, Zorost Intelligence.
> This is Zorost Intelligence's own published analysis of Andrew Ng's *AI Engineering Skills Map*.
> Full canonical copy lives on zorost.com; reproduced here as the program's design reference.
> Key takeaways used by this repo: the six-block twelve-week programme with artifact gates,
> the systems-engineering spine (requirements → verification → configuration control),
> the seven competencies the map assumes but does not teach, and the critique that a
> roadmap only expires when the economics change.

---

Agentic AI Engineering
The AI Engineering Skills Map, turned into a training plan
16 AUG 2026
· Zorost Intelligence
Contents
What was actually published
The four areas, unpacked
Area one: building and deploying
Area two: software fundamentals
Area three: coding agents
Area four: shaping the build
Software engineering, reborn
Systems engineering, the spine
What the map assumes
The twelve week programme
What it means for your role
The roles that emerged
How to become a software engineer
How to turn this into a company
Where this goes wrong
Common questions
Next steps
Reference piece. Roughly a 40 minute read, or read your own role, the rebirth section, and the programme.
Implementation is the part that got cheap. Deciding what to implement is the part that got expensive. Every consequence in this article follows from that one sentence.
On 14 August 2026, Andrew Ng and DeepLearning.AI published
The AI Engineering Skills Map
: four skill areas drawn from more than 10,000 job postings, dozens of structured interviews with AI experts, hiring managers and recruiters, survey data, and other online sources.
The four areas are building and deploying AI applications, software engineering fundamentals, using coding agents, and shaping the build. Underneath all four sits a mindset of continuous learning. That is the whole published map.
It is also, deliberately, a beginning. Ng states in the letter that he will expand each area in subsequent letters and share a more detailed map later. As of this writing there is no downloadable diagram, no proficiency levels, no role tracks, and no curriculum. The four areas are prose, not a checklist.
That gap is the reason for this article. A framework you cannot act on is a vocabulary, not a plan. So this piece does five things: it converts the letter into an exact inventory of every competency it names, it argues that the largest consequence of the map is the rebirth of traditional software engineering rather than its retirement, it adds the seven competencies the map depends on and does not teach, it turns the result into a twelve week training programme with a gate at every stage, and it works through what each area means for twelve specific roles, including the two questions people ask us most often, which are how to become a software engineer now that agents write most of the code, and how to turn engineering skill into a company.
Running underneath all of it is a discipline the map never names and every shipped system needs, which is systems engineering. It gets its own section, because it is the thing that turns four separate skills into one workflow that holds.
Everything attributed to Ng is sourced. Everything else is ours, and labelled as ours.
Primary sources
The AI Engineering Skills Map
, The Batch, 14 August 2026
The Batch, issue 366
Announcement on X
andrewng.org writing index
Reading note.
Where this article says "the letter", it means the Batch article linked above. Where it says "we", it means the engineering team at Zorost Intelligence.
What you will be able to do
State the four areas precisely, and name every sub-skill the letter actually lists under each one, without adding invented structure.
Explain why prompt engineering was demoted and what replaced it, in terms a hiring manager will recognise.
Say precisely which parts of traditional software engineering became more valuable, which became less, and which are genuinely new, rather than repeating that fundamentals still matter.
Apply the systems engineering spine, requirements through verification and configuration control, to an AI system that behaves differently on every run.
Identify the seven competencies the map assumes are already handled, which is where most teams lose weeks.
Run a twelve week training programme where every block ends in an artifact someone else can inspect.
Locate your current role on the map, name your real gap, and pick the first thing to build.
Follow a concrete path into software engineering, or from skills into a company, with checkable milestones instead of advice.
What was actually published, and what was not
Precision matters here, because a great deal of secondary commentary is already describing structure the release does not contain.
What the letter contains: a statement of purpose, a methodology paragraph, four named areas presented as a bullet list, four sections of prose explaining each area, a paragraph on continuous learning, and a note that more detail is coming. It closes with a request that readers complete a short survey to help shape future versions.
What it does not contain: a visual map, a downloadable artifact, beginner to advanced levels, core versus specialist tiers, prerequisite ordering, numeric demand scores, role-by-role tracks, or a mapped curriculum. Anyone showing you a tiered diagram with percentages attached has drawn it themselves.
The methodology is worth reading carefully, because it is both the strongest and the weakest part of the release. Strongest: more than 10,000 job postings is a serious corpus, and structured interviews with hiring managers and recruiters capture what the postings leave out. Ng describes the synthesis informally as clustering a very large dataset of jobs and expert interviews, with an eye on both current and near-future skills.
Weakest: none of it is reproducible. The postings dataset, the collection window, the geographic scope, the interview guide, the survey instrument, the respondent count, the weighting between sources, and any numeric ranking among the four areas are all unpublished. There is no way to audit whether area three outweighs area two, or whether the clustering would survive a different sample.
This is not a reason to dismiss the map. It is a reason to treat it as an experienced practitioner's structured judgment supported by data, rather than as a measurement. Read that way, it is genuinely useful, and it agrees with what we see in the work.
Scope: skills, not job titles
The letter makes a distinction that most summaries drop.
AI Engineering skills
are broad.
AI Engineer
is a narrow job title for someone whose job is building AI systems.
Ng's analogy: nearly every developer needs cloud skills, but relatively few hold the title Cloud Engineer. He expects full-stack, data, DevOps, machine learning and AI engineers all to need these skills.
This is why "should I retrain as an AI engineer" is usually the wrong question. The skills are arriving inside the job you already have.
The four areas, unpacked into an inventory
The letter is prose. Below is that prose converted into an inventory: every competency it names, grouped under its area, with nothing added. This is the closest thing to the checklist the release does not yet include.
Every competency the letter names, grouped under its area. Anything we would add appears separately, later in this article.
One structural observation before the detail. Read the four areas in order and they describe a movement outward from the model: first the AI system itself, then the software around it, then the tooling you use to produce that software, then the judgment about what to produce at all. Each area is further from the model and closer to the decision. That direction is the argument.
Area one: building and deploying AI applications
The letter's framing is that AI applications differ from conventional software because their outputs are less predictable, and that the engineer's job is to make that behaviour predictable enough to depend on. The named building blocks are large language models, context engineering, retrieval augmented generation, agentic workflows, machine learning and deep learning. The named methods are statistical measurement, steering, governance, evaluations and error analysis.
The word doing the most work in that list is
measurement
. Conventional software has a binary correctness notion: the test passes or it does not. An AI feature has a distribution of behaviours, and the only honest statement about it is statistical. It answers this class of question correctly about this often, and here is the sample that establishes it.
That single change cascades. If quality is a distribution, then you need a dataset to measure it against, which means eval design becomes an engineering task with its own version control and review. If quality is a distribution, then a release gate is a threshold on a number rather than a green checkmark. If quality is a distribution, then "it looks better" is not evidence, and a team that ships on vibes will regress silently and find out from a customer.
Error analysis is the part almost nobody does and the part that compounds fastest. It is unglamorous: sample fifty real interactions, read them by hand without summarising, write down what specifically went wrong in each, group the failures into classes, count the classes, and fix the largest one. Then add that class to the eval set so it can never come back.
We have never run this loop on a live system and failed to find something surprising in the first hour. Retrieval returning the right document ranked fourth. A date format that silently changed meaning. One customer segment phrasing questions in a way the system had never been tested against. None of those are model problems, and none of them show up in an aggregate score.
The distinction to hold
Evaluation
tells you the current level.
Error analysis
tells you what to do next. Teams that only have the first can watch a number without being able to move it.
Go deeper
Building an agent evaluation harness
A failure taxonomy for agents
Context engineering as a budget
Structured output from language models
Error analysis is a loop that runs for the life of the system. The proportions below it are illustrative of how our own delivery time distributes, not a published benchmark. The ordering is the point.
Note the demotion that this area performs quietly. Prompt engineering is not one of the four areas, and the letter does not list it as a named building block. It survives as a small component of building applications. The skills that displaced it are measurement, error analysis and specification, and the reason is structural: those are the parts of the job that define what correct means, which is precisely the part a model cannot do on your behalf.
Area two: software engineering fundamentals
This is the area most likely to be misread as filler, and it is the one the letter is most pointed about. The argument is not that fundamentals are still nice to have. It is that fundamentals are what let you supervise an agent at all.
The named competencies are cost, scalability, reliability, speed, security, privacy, stack choice, system architecture, data store design and testing. The load-bearing claim is that a coding agent makes architectural tradeoffs continuously, and an inexperienced developer will accept bad ones without noticing, or fail to supply the context that would have produced good ones.
This is the sharpest thing in the letter, and it inverts the popular expectation. The natural assumption in 2023 was that better coding tools would reduce the fundamentals a developer needs. The observed effect is the reverse. When you write the code yourself, you meet each tradeoff at the speed you type, one at a time. When an agent writes it, a hundred tradeoffs are made in ninety seconds and presented as a finished diff. Reviewing that requires more architectural fluency than writing it did, not less.
The letter names uninformed vibe coding as the failure mode. We would put it more concretely. The agent will choose a data store. It will choose whether that endpoint is idempotent. It will choose whether the retry is bounded. It will choose what gets logged and therefore what you can debug at three in the morning. It will choose whether that query is going to be fine at ten thousand rows and catastrophic at ten million. Every one of those is a decision you own, delivered as code you did not write.
There is a second, less obvious consequence. Precise engineering vocabulary is now a control interface. "Make this faster" produces one thing. "This endpoint is doing an N plus one query against the orders table; batch it and add a covering index" produces another. The gap between those two prompts is not prompt engineering, it is knowing what is wrong. That knowledge is area two, and it is now directly convertible into agent output quality.
Why this is the safe investment
Fundamentals are the slowest depreciating asset on the map. A framework you learn this year may be irrelevant in three. Query planning, idempotency, failure modes, cache invalidation and access control have been stable for decades and are the vocabulary you steer agents with.
A useful test
Read a diff your agent produced and try to name three tradeoffs it made that it did not mention. If you cannot find three, you are not yet reviewing it, you are reading it.
Area three: using coding agents
The letter treats agentic coding as a skill in its own right, with a substantial competency list: an accurate mental model of how agents work, knowledge of their limits and how to work around them, context management, the tradeoff between planning and execution, verifiers, evals in the loop, specification writing, multi-agent orchestration, judgments about how much autonomy to grant and when to intervene, and safety practices that prevent an agent from damaging a production database. It closes by noting that the tooling changes fast enough that developers also need a standing process for trying new tools and updating their workflow.
That last item is easy to skim and is arguably the most important. Every specific tool named in any 2026 article about agentic coding has a short half life. The durable skill is the routine: try something new on a schedule, judge it on evidence from your own work, and keep or discard it deliberately rather than by fashion or inertia.
On the substance, the piece we would emphasise hardest is the
verifier
. An agent loop is only as good as the signal that tells it whether it is done. Give an agent a task with a real verifier, a test suite, a type checker, a linter, an eval set, a schema, and it can iterate productively for a long time without you. Give it a task with no verifier and it will produce something confident, plausible and unchecked, and the checking work lands on you at the least convenient moment.
This reframes what a specification is for. A specification is not documentation for humans. It is the definition of done that the loop closes against. That is why area three and area four are joined at the hip: the quality of your specification is the ceiling on how much autonomy you can safely grant.
The autonomy judgment itself deserves more attention than it usually gets. The right question is not how much you trust the agent. It is what the blast radius is if this particular action is wrong. Reading files in a scratch directory is nearly free to get wrong. Writing to a production database is not. The same agent deserves different leashes on those two tasks, and calibrating that per action rather than per session is the skill.
Four questions before you grant autonomy
What is the worst thing this action can do if it is wrong?
Is that reversible, and how quickly?
What verifier will catch it before a human does?
Who is paged if it happens at 3am?
Go deeper
Agent harness architecture
Prompt looping and agent loops
Tool design for agents
Prompt injection and LLM security
Area four: shaping the build
This is the area with the largest consequences and the least concrete guidance, in the letter and everywhere else.
The argument: as agents get better at implementing a clear specification, the engineer's contribution moves upstream into deciding what the specification should say. The named competencies are product sense, understanding business context and customer goals, helping define and drive the build, taking ownership and agency, identifying worthwhile problems and opportunities, and judging when to ship a quick minimum viable product for testing against when the risk or quality bar demands a more careful build.
The letter is explicit that engineers should no longer expect the job to be receiving a pixel-perfect design and implementing it exactly. That expectation is what got automated.
Here is why this area is harder to train than the other three. Areas one through three have verifiers. You can tell whether your eval set is well constructed, whether your architecture holds under load, whether your agent loop converges. Area four has no verifier except reality, and reality returns its result slowly. You find out whether you chose the right problem in months, not minutes.
The practical consequence is that area four can only be trained by making real decisions with real consequences and then actually looking at what happened. Not by reading about product sense. The smallest honest version of that exercise is this: pick a problem nobody assigned you, write the specification yourself, build it, put it in front of a real user, and then write down what you got wrong about the problem. That last step is the one that teaches. Most people skip it, which is why so many portfolios contain projects and so few contain judgment.
There is also an organisational reading. If value is moving to specification and judgment, then organisations that keep engineers away from customers are systematically destroying the thing that now matters. The map has an implication for how teams are structured, not just for what individuals learn.
The cross-cutting fifth element
Ng places
continuous learning
underneath all four areas rather than counting it as one of them. Practices and tools continue to change quickly enough that a static skill set decays.
We would make that concrete: it is not a mindset, it is a calendar entry. A recurring block where you try something new, judge it against your own work, and write down the verdict.
The structural claim underneath the whole map. Every role consequence later in this article follows from this one shift.
Traditional software engineering, reborn
The most common misreading of this map is that software engineering is being retired. The letter says the opposite, and so does the work. What is happening is a rebirth: the same profession, with its centre of gravity moved from producing code to specifying and verifying it.
Ng puts area two, software engineering fundamentals, second on a list of four, and argues that architecture, data stores, testing, security, privacy, scalability, reliability, cost and performance all still matter, because AI does not remove engineering tradeoffs and you need to understand them well enough to steer agents correctly. That is a strong claim and it is easy to skim past. It says fundamentals are not a legacy requirement that survived the transition. They are the instrument you steer with.
The reason is mechanical rather than sentimental. An agent will produce something plausible for almost any instruction. The only thing standing between plausible and correct is a person who can tell the difference, and telling the difference requires exactly the knowledge that used to be needed to write the code in the first place. Remove the fundamentals and you do not get a faster engineer. You get someone who merges whatever compiles.
But "fundamentals still matter" is where most commentary stops, and it is not useful enough to act on. Fundamentals is not one thing. Some parts of the traditional craft became dramatically more valuable, some became close to worthless, and a third set did not exist five years ago. Sorting your own skills into those three buckets is the single most practical exercise in this article.
The one line version
Writing code was never the job. It was the medium. The job was always deciding what should exist and proving that it does. Agents took the medium and left the job.
Why this section exists
Readers kept asking whether it is still worth learning to be a software engineer. It is, more than before, but not the version of the role you may be picturing. The rest of this section is that answer in detail.
Our sorting of the traditional craft into three ledgers. The middle column is the one people avoid reading honestly about their own skill set.
What appreciated
Reading code, at volume and at speed
This is the largest single change and the one least reflected in how people train. For thirty years the profession optimised for writing. The daily reality now is that you read far more code than you produce, most of it written minutes ago by a machine that had no stake in the outcome. Reading fluently, spotting the wrong abstraction in an unfamiliar file, and holding a system in your head while you scan a diff are now core throughput skills rather than senior-engineer bonuses.
Architecture and interface design
Agents are competent inside a file and weak across a system. Deciding where a boundary goes, what crosses it, and what each side is allowed to assume is work an agent will happily do badly and confidently. Bad boundaries are also the most expensive category of mistake to unwind, which is why this skill is being priced upward while typing speed goes to zero.
Testing, and verification design more broadly
A test used to be insurance against your own mistakes. It is now the specification you hand a machine and the gate that decides whether its work ships. The engineer who can express "correct" as something executable controls the loop. The one who cannot is reduced to reading outputs and forming an impression, which does not scale past a few dozen cases.
Debugging from evidence
Agents are good at producing a fix and bad at establishing a cause. Reading a stack trace, forming a hypothesis, bisecting, instrumenting, and confirming is a discipline that transfers completely and is now applied to code you did not write. It is also the skill that most reliably separates people who can operate an AI-assisted codebase from people who can only extend one.
Security and privacy thinking
Named directly in area two, and the stakes rose. A system that acts on its own with real credentials fails differently from one that returns a page. Least privilege, input distrust, secret handling and blast radius are design-time concerns now rather than a review checklist.
Performance and cost reasoning
Also named in area two, and now with a second meaning. Alongside the traditional questions of algorithmic complexity and query plans sits cost per resolved task and latency budget per user action. Both are architecture constraints. An engineer who cannot reason about them ships systems that work in the demo and cannot be afforded in production.
What depreciated
This is the uncomfortable ledger, and being honest about it is more useful than being reassured.
Syntax recall and API memorisation.
Knowing the exact signature without looking it up was a real productivity edge for decades. It is now worth approximately nothing, and time spent maintaining it is time not spent on the appreciating column.
Boilerplate production.
Scaffolding, wiring, adapters, data transfer objects, standard CRUD, the fiftieth form validation. This was a meaningful fraction of many jobs and it is the part agents do best.
Framework trivia as identity.
Deep familiarity with one framework's conventions was a hiring signal because it took months to acquire. It now takes an afternoon with an agent, and the signal has collapsed accordingly.
Greenfield implementation from a finished design.
The letter addresses this directly: engineers should no longer expect the job to be receiving a pixel-perfect design and implementing it exactly. That expectation is precisely what got automated, and it was the traditional entry-level rung.
None of this means the underlying understanding is worthless. Knowing why the framework works the way it does still matters. Knowing its method names does not. The distinction is between understanding and recall, and only recall depreciated.
A test you can run on yourself
Take last week's work and split it by hours. How many went to the appreciating column, how many to the depreciating one? If the second number is large, that is not a judgment on you. It is a description of a job that is about to change, and you now have a specific list of what to move toward.
On juniors
The depreciating column is close to a description of the traditional first job. This is the mechanism behind the entry-level squeeze, and it is why the graduate advice later in this piece is about manufacturing judgment deliberately rather than waiting to be given it.
What is genuinely new
Specification as a deliverable
Writing a specification precise enough for a machine to execute and a reviewer to grade is a new artifact class. It is harder than it looks, because natural language is where ambiguity hides, and an agent will resolve your ambiguity silently rather than asking. The skill is writing the constraints and the out-of-scope list, not the happy path.
Verifier design
Area three names providing verifiers and evals to coding agents. The generalised skill is deciding, before you start, how you will know the result is right, and then making that check cheap enough to run continuously. Compilers, type systems, tests and evals are all verifiers, and choosing the strongest available one for a given task is now a design decision.
Context management
What goes into the window, what is left out, when to compact, and when to start clean. Area three names this explicitly for coding agents, and area one names it for applications. It has no analogue in traditional engineering, and it is the difference between an agent that holds a thread across a long task and one that quietly loses the plot.
Working with non-determinism
The hardest adjustment for a traditionally trained engineer. Correctness becomes a rate, a fix becomes a shift in a distribution, and "it worked when I tried it" stops being a claim. This is a genuine change in mental model rather than a new library, and it is why the map puts statistical thinking and error analysis inside area one.
Orchestration and intervention judgment
Running several agents in parallel, and knowing when to let one continue against when to stop it and take over. Area three names both. The failure mode is symmetrical: intervening too early wastes the leverage, intervening too late means reviewing an hour of confidently wrong work.
Owning code nobody typed
The organisational half of the same problem. Who reviews it, to what standard, who is on call for it, and what happens when it needs to change in a year. Most teams have not written this down, and the ones that have not are accumulating a codebase no human has a model of.
The rebirth, stated plainly
Put the three ledgers together and the shape is clear. Programming is not disappearing. It is moving up a level of abstraction, the way it did when assembly gave way to compiled languages and again when compiled languages gave way to managed runtimes and libraries. Each of those transitions removed a category of manual work, produced a wave of predictions that programmers were finished, and ended with more programmers doing more ambitious things.
What is different this time is the nature of the abstraction. Every previous step up was still deterministic. You wrote something precise in a formal language and the machine did exactly that. This step replaces the formal language with natural language and the exact translation with a probabilistic one. That is why the new skills are what they are: if the translation layer is unreliable, then specifying carefully and verifying rigorously stop being professional virtues and become the entire job.
The clearest external framing of this shift comes from Andrej Karpathy, who describes three paradigms coexisting: Software 1.0, code written by hand; Software 2.0, neural network weights learned from data; and
Software 3.0, models programmed in natural language
, presented at the Y Combinator AI Startup School in June 2025. That framing is his, not Ng's, and the two are compatible. Ng's map is what you need to know to work in the third paradigm without losing the first.
Our own reading, offered as ours: the title "software engineer" is going to survive this and mean something closer to what the word engineer means in other disciplines. An engineer in civil or aerospace practice is not primarily a producer of artifacts. They are someone accountable for a system meeting stated requirements under stated conditions, who signs off. Software borrowed the title without much of that apparatus, largely because producing the artifact was hard enough to fill the role. Now that production is cheap, the rest of the word is arriving, and that is what the next section is about.
Attribution
The three ledgers, the abstraction argument and the closing claim about the word engineer are ours. Area two's contents and the point about pixel-perfect designs are Ng's. The Software 1.0 to 3.0 framing is Karpathy's and is linked in the text.
What we tell new hires
You will be judged on what you can prove, not what you can produce. Bring the artifact and the number attached to it.
Systems engineering, the spine of the whole workflow
The map names four skills. Skills do not ship. What ships is a system, and the discipline that turns separate skills into a system that holds is systems engineering. It appears nowhere in the letter, and in our work it is the difference between a demo and something a regulator, an auditor or a customer will accept.
The distinction is worth stating, because the two terms get used interchangeably and they are not the same. Software engineering is concerned with building the software correctly. Systems engineering is concerned with the whole: requirements, the interfaces between parts, verification that each requirement is met, validation that the requirements were the right ones, configuration control over what is actually deployed, risk and hazard analysis, and traceability from a stated need to the evidence that it is satisfied. It is a lifecycle discipline, and it long predates AI.
It matters more for AI systems than for conventional ones, for a specific reason. An agentic application is a system of systems: a model you did not build and cannot inspect, a retrieval layer over data with its own freshness and lineage properties, a set of tools with real side effects, a human reviewer, and a policy boundary around all of it. Almost none of the interesting failures live inside a single component. They are emergent, they cross boundaries, and they cannot be found by testing the parts in isolation. That is the exact class of problem systems engineering exists to handle.
Not in the letter
This entire section is ours. Ng does not mention systems engineering. We include it because every AI system we have put into production in aviation, pharmaceutical research, manufacturing and federal work needed it, and because its absence is the most common reason a promising prototype never reaches deployment.
The one sentence case
Evals verify a component. Systems engineering is how you know the component you verified is the one that shipped, and that passing it means the system is actually fit for the purpose someone asked for.
The V model adapted to a probabilistic system. Every artifact on the left has a matching form of evidence on the right, and the baseline underneath records exactly which model, prompt and index produced that evidence.
The six practices, translated into AI engineering
Requirements, written before the build
A statement of what the system must do, for whom, under what conditions, and what would constitute failure. In AI work this is unusually important because the acceptance criterion is statistical. "Answers questions about our contracts" is not a requirement. "Returns a cited answer for at least ninety percent of the question set, and declines rather than guesses for the remainder" is one. This is area four with an engineering discipline attached.
Interface control
A register of every boundary in the system and the contract at each one: the model API, the retrieval service, each tool the agent can call, the human review step, and the audit sink. In an agentic system the tool contracts are also the security perimeter, which is why this document does double duty as the trust boundary map.
Verification, which is where evals belong
Verification asks whether the system meets the requirements. Every requirement should name the evidence that satisfies it, and for AI behaviour that evidence is an eval set with a threshold. The discipline that matters is the link: an eval that is not tied to a requirement is a number nobody can act on, and a requirement with no eval is a hope.
Validation, which is not the same thing
Validation asks whether the requirements were right. A system can pass every eval and still be useless because the question set did not resemble what users actually ask. This is the failure we see most often in otherwise competent teams, and the only cure is putting the system in front of real usage early and revising the requirements from what comes back.
Configuration management
A record of exactly what is deployed: model identifier and version, system prompt, retrieval index build, chunking parameters, tool versions, thresholds. AI systems drift without a code change, because a provider can update a model underneath you. If you cannot state which configuration produced last quarter's eval results, you cannot investigate a regression and you cannot defend the system to an auditor.
Risk and traceability
A hazard list of what happens when the system is wrong, ranked by consequence rather than probability, with a mitigation against each. Then a trace from each stated need to the requirement, the design, the evidence and the residual risk. In regulated sectors this is the deliverable that determines whether you deploy at all.
Where this lands in our workflow
We do not run this as a parallel process with its own meetings. It is folded into the same twelve week shape described in the next section, and it is the reason each block ends in an artifact rather than a demo. Concretely, five documents accumulate as the work proceeds, and none of them is long.
A requirements note, one page, written before the first line of code, stating what must be true for the system to be worth deploying. An interface register, a table, listing every boundary and its contract. An evaluation plan that maps each requirement to the eval that verifies it and the threshold that gates release. A configuration record, generated rather than written, capturing model, prompt, index and thresholds for every release. And a hazard list with mitigations, reviewed whenever the system gains a new tool.
That is the entire apparatus. It fits in a folder, and it is the difference between a system somebody can take responsibility for and a system that works when its author is in the room. In aviation, pharmaceutical and federal contexts it also happens to be the shape auditors already expect, which is why the same discipline that makes engineering sense is also the fastest route through a compliance review. Our
federal work
and the
AI Lab method
are both built on this spine.
One honest caveat, because this discipline has a failure mode of its own. Systems engineering applied without judgment becomes documentation theatre, where the artifacts are produced to satisfy a process rather than to make decisions. The test for whether you are doing it correctly is simple: if none of the five documents has ever caused you to change the build, you are writing paperwork, not engineering a system.
Frameworks worth reading
The
NIST AI Risk Management Framework
for the govern, map, measure and manage structure
ISO/IEC/IEEE 15288 for the systems lifecycle vocabulary, if you want the formal version
Sector rules where they apply, which in our work means aviation, GxP and federal authorisation regimes
Minimum viable version
If five documents is too many to start with, start with two: the requirements note and the evaluation plan that maps to it. Those two carry most of the value, and the other three tend to write themselves once those exist.
What the map assumes and does not teach
Four areas is a good compression of a complicated field, and compression costs something. There are seven competencies that the four areas quietly assume are already handled. The seventh is systems engineering, which is large enough that it took its own section above. The remaining six are below. Each one is a place where we have watched capable teams, including our own, lose weeks. We are not proposing them as corrections to the map. They are the layer underneath it.
Our additions, not Ng's. The lower panel is the version we actually use when assessing capability.
Data engineering, which area one starts above
Area one begins at the model and names retrieval augmented generation as a building block. But retrieval quality is a data problem long before it is a model problem. Whether the right document is in the index, whether it is current, whether it is chunked so that the answer survives the split, whether permissions are enforced at retrieval rather than in the prompt, whether the schema changed last Tuesday and nobody noticed: none of that is addressed by a better model, and all of it determines the answer.
This is the single most common root cause we find behind the complaint that the AI gives wrong answers.
Evaluation as a standing discipline, not a bullet point
Evals appear inside area one as one item among a dozen. In a system that is actually in production, evaluation is somebody's job. It has datasets that need curating as the world changes, graders that themselves need validating, drift that needs monitoring, and a release gate with the authority to block a ship.
Treating it as a task rather than a function is how organisations end up with a number nobody trusts and everyone quotes.
Unit economics as a design constraint
The letter names cost among the software tradeoffs. In practice AI systems need a sharper version: cost per resolved task, not cost per token, and a latency budget per user action rather than an average.
Those two numbers constrain architecture directly. They decide whether you can afford a multi-agent design, how many retrieval passes you get, and whether you can run a verifier on every request or only on a sample. Teams that discover them after the architecture is set usually rebuild.
Trust boundaries in a system that acts
A non-deterministic component holding real credentials and real tools is an attack surface with properties conventional security review is not built for. Prompt injection through retrieved content, tool scoping, least privilege for agent identities, and the question of what an attacker can make your agent do on their behalf all belong in the design phase.
Area two names security and privacy. The specific shape of the problem when the vulnerable component is a language model deserves to be called out rather than folded into general practice.
Domain knowledge, especially where there is a regulator
In aviation, pharmaceutical research, regulated manufacturing and federal work, the binding constraint is rarely the model. It is the standard, the audit trail, and what you are permitted to do with the data. An engineer with excellent generic AI skill and no domain reading will produce something that benchmarks well and fails review.
The competency here is knowing which document governs, and reading it. Our own work on
enforcing Simplified Technical English mechanically
exists because that constraint could not be prompted away.
Working on a codebase that agents largely wrote
The map covers using an agent. It does not cover the shared codebase that several people's agents have been writing into for a year. Who reviews it, to what standard, how ownership works for code nobody typed, and who is on call for it are open organisational questions.
This one is genuinely unsolved, and anybody claiming a settled answer is guessing. We flag it because it is arriving whether or not the practice is ready.
The twelve week programme: the map as a training use case
This section is the one people asked for. A framework becomes a plan when it has a sequence, a duration and a gate.
The programme below is six two-week blocks. It is designed around one principle:
every block ends in an artifact someone else can inspect
. Not a completed course, not a certificate, not a notebook. A thing with a URL, a number attached to it, and a stated limitation.
The reason for that principle is the shift described in area four. When implementation was scarce, a certificate was a reasonable proxy for capability, because completing the course meant you could produce the code. Now that implementation is cheap, the certificate proves very little and the artifact proves everything. What a hiring manager wants to know is whether you can tell a good result from a bad one, and only an artifact with numbers on it answers that.
If you only have four weeks
Run blocks one and two, then jump to block six. A deployed thing, an eval set, and a specification you wrote yourself will teach you more than a complete pass through blocks three to five without them.
Prerequisite, honestly stated
You need to be able to write, run and deploy a small program in one language. If you cannot, spend the first month there. No amount of AI skill compensates for it, and area two says so explicitly.
Six blocks, six inspectable artifacts. The habits underneath run for all twelve weeks and matter more than any single block.
Weeks 1 and 2: ship one thin slice
One endpoint, one model call, deployed at a real URL, with request and response logging you can query. Nothing clever. The goal is to cross the entire distance from idea to running service once, early, so that every later block has somewhere to land. Most people who stall in AI learning stall because they never crossed this line and are accumulating notebooks instead.
Gate:
a stranger can use it, and you can show them what it did.
Weeks 3 and 4: write the eval before the feature
Thirty labelled cases minimum, drawn from real or realistic inputs, with a grader you can run in a single command and a baseline number recorded. Then change something and watch the number move. This block is where area one becomes real, and it is the block that converts an enthusiast into an engineer.
Gate:
you can state your current score, and you have at least one change you rejected because the score dropped.
Weeks 5 and 6: own the data path
Add retrieval. Own the ingestion, the chunking, the freshness and the permissions, and then, critically, measure retrieval separately from generation. Most quality problems attributed to models live here, and you cannot see them if you only measure end to end.
Gate:
you can report retrieval recall on your own eval set as a number distinct from answer quality.
Weeks 7 and 8: an agent with real tools
Give it typed tools with narrow scopes, credentials limited to exactly what the task needs, a verifier that closes the loop, and a written blast radius statement for each tool. Then try to break it deliberately, including with hostile content in whatever it retrieves.
Gate:
you can describe, per tool, what happens when the agent is wrong and who finds out.
Weeks 9 and 10: make it affordable
Measure cost per resolved task and p95 latency. Then halve them both without losing eval score. This block teaches more architecture than any reading, because every meaningful reduction forces a real tradeoff: caching, a smaller model on the easy path, fewer retrieval passes, batching, a verifier that runs on a sample instead of everything.
Gate:
a before and after table with cost, latency and eval score in it.
Weeks 11 and 12: shape a build
Choose a problem nobody assigned you. Write the specification yourself, including what success means and what you will not build. Have agents execute it. Put it in front of a real user. Then write down what you got wrong about the problem, which is the actual deliverable.
Gate:
a specification document, a working system, and an honest retrospective on the problem choice.
This is the block most learners skip and the one area four is entirely about. It is also the only block that produces evidence of judgment, which is the thing the 2026 ladder is pricing. If you do one block from this programme, do this one.
The systems engineering thread that runs through all six
Read the blocks again and the spine from the previous section is already there, which is deliberate. Block one establishes a configuration you can point at. Block two is verification, and the eval you write is the evidence for a requirement whether or not you have written the requirement down. Block three is interface control over the data path. Block four is hazard analysis, because a blast radius statement per tool is exactly that. Block five is a non-functional requirement given a number. Block six is validation, which is the discovery that the requirements were partly wrong.
Making the thread explicit costs about two hours across twelve weeks and roughly doubles what the programme is worth to an employer. Before block one, write the one page requirements note. During block two, add a column to your eval plan naming which requirement each eval verifies. From block one onward, have your deployment write a configuration record automatically rather than maintaining it by hand. During block four, start the hazard list. At the end of block six, revise the requirements note and keep both versions, because the diff between them is the clearest evidence of judgment you will produce in the whole programme.
That last point is worth stating on its own. Anyone can show a system that works. Very few candidates can show what they believed at the start, what reality corrected, and how they knew. That diff is the artifact.
Why a gate, not a lesson
A lesson ends when you have understood something. A gate ends when something works and you can show the number. Only the second survives contact with a hiring manager or a customer.
Map the blocks to the areas
Blocks 1 and 3 build
area one
and the data layer under it
Blocks 2 and 5 build the
measurement
and
economics
discipline
Block 4 builds
area three
, including the safety judgment
Block 5 forces
area two
, because every real cost cut is an architecture decision
Block 6 is
area four
, and it is the only one with no verifier but reality
The
systems engineering
artifacts accumulate across all six, described below
Doing this with a team
Run the same six blocks against one shared internal problem rather than six toy problems. The retrospective in block six is worth more when several people were wrong about the same thing.
What it means for your role
The same four areas land very differently depending on where you are standing. Below is a read for eleven roles, with founders handled separately further down. Find yours, then read one you are not, because the contrast is where the map becomes legible.
The gap column is the honest one. It is what your current job does not force you to practise, which is exactly what the market is now pricing.
Data scientists
You are the role that is closest to area one and furthest from shipping. Statistical thinking, measurement discipline, sampling and error analysis are already your native language, and those are precisely the skills that most software engineers now have to acquire painfully. Evaluation design in particular should feel obvious to you, because it is experimental design with a different vocabulary.
The gap is area two, and it is usually larger than data scientists estimate. Not "can you write Python", which you can, but service design, dependency management, testing, deployment, observability, and the operational reality that a thing which runs is different from a thing which runs at 2am under load with someone else on call. The notebook to production distance was always the profession's weak point, and agents shrink the typing part of that distance while leaving the judgment part exactly where it was.
First move:
take a model you have already built and put it behind a live endpoint with an eval gate in continuous integration. Not a demo. Something with a URL, logging, and a test that blocks a merge.
Data engineers
You are in one of the strongest positions on this map, and the reason is structural rather than flattering. Every AI application is a data product wearing a chat interface. Retrieval is a serving layer. Context assembly is a join. Freshness, lineage, schema contracts and cost control are exactly your existing discipline pointed at a new consumer. When an AI system gives wrong answers, the investigation ends in your territory far more often than in the model.
The gap is non-determinism. Your entire profession is built on reproducibility: the same input yields the same output, and a diff means something broke. Language models violate that assumption, and the tooling you trust does not help. You need to become comfortable with distributions, with evaluation sets instead of assertions, and with a quality bar that is statistical rather than binary. That is an uncomfortable but small conceptual move, and it is much smaller than the move software engineers have to make in the other direction.
First move:
build a retrieval service over data you already own, and report recall and freshness as measured numbers rather than as design intentions. Our write-up on
data engineering workflow for governed question answering
is a reasonable starting shape.
AI engineers
Worth restating the letter's own distinction: AI Engineer is a narrow job title, AI Engineering skills are broad. If you already hold the title, this map is less a syllabus than an audit, and the audit usually finds the same two things.
First, depth in area one is often narrower than it looks, concentrated in orchestration frameworks rather than in measurement. Many people who build agentic systems daily have never constructed a proper eval set or run a structured error analysis session, because the frameworks make it easy to build and hard to grade. Second, area two erodes quietly. If you moved into AI work early, you may have missed the years of systems experience that would let you catch a bad architectural choice in an agent's output.
First move:
run one week of genuine error analysis on a system you already operate. Fifty real interactions, read by hand, categorised, counted. Then fix the largest class and add it to the evals. If that exercise surprises you, and it usually does, you have found your gap.
Machine learning engineers
Training, serving and MLOps carry over almost entirely, and the operational instincts transfer better than anyone's. You already know that a model is a liability in production until it is monitored.
The gap is area four, and it is the same gap the whole discipline has: ML engineering culture optimises a metric that somebody else chose. The skill now being priced is choosing it. There is also a smaller adjustment, which is that a great deal of applied AI work no longer involves training anything, and the value has moved to the system around a model you did not build.
First move:
write a specification for something end to end, including what success means and what is out of scope, and have agents execute it. Judge yourself on the specification, not the implementation.
Software engineers
Areas two, three and four are close to home. Architecture, tradeoffs, testing and shipping are your existing craft, and the letter argues explicitly that these become more valuable rather than less, because they are what let you supervise an agent instead of accepting its defaults. You are the role this map most directly protects, which is the argument of
the rebirth section
above.
Protects, but does not leave unchanged. Run the three ledgers against your own week honestly. If most of your hours are still going to production of code from a specification someone else wrote, you are standing in the depreciating column, and seniority will not shelter you from that for long. The engineers doing well right now moved their hours into reading, boundary decisions, verification design and specification.
The gap is statistical thinking, and it is a genuine discomfort rather than a knowledge deficit. You are trained on determinism. A test passes or fails; a bug is reproducible or it is not. Working with systems where correctness is a rate and a fix is measured by a shift in a distribution requires giving up a mental model that has served you well for years. The engineers who make this transition well tend to be the ones who accept early that "it works on my example" is not a claim.
First move:
add an agentic feature to something you own, and gate it with a graded regression suite. The eval set is the artifact, not the feature.
Systems engineers and solution architects
You hold the discipline the whole field is currently reinventing under other names, and mostly badly. Requirements, interface control, verification against validation, configuration baselines and hazard analysis are your existing vocabulary, and they are exactly what separates an AI prototype from a deployable system. Very few people who can build an agent can also state what it is required to do and prove that it does it.
The gap is that your instincts were formed on systems whose components behave the same way twice. A model is a component with a distribution instead of a specification, supplied by a vendor who can change it without telling you. Your verification methods need a statistical form, your configuration baseline needs to include a model version and a prompt, and your interface contracts need to describe behaviour under uncertainty rather than just types.
First move:
take an AI prototype your organisation already has and write the missing spine for it: one page of requirements, an interface register, and an eval plan that maps each requirement to evidence. You will usually find at least one requirement nobody can satisfy, and finding it is the value.
Analytics engineers and BI developers
You hold something the market undervalues and AI systems desperately need: semantic understanding of what the business actually means by its terms. When a question answering system over enterprise data gives a plausible wrong answer, the cause is usually that nobody encoded which revenue definition was intended. That is your work.
The gap is software fundamentals, and specifically the engineering practices that SQL-centred careers can skip: version control as a habit, testing, packaging, deployment and code review. Area two is the whole assignment.
First move:
build a governed question answering tool over marts you already maintain, with an eval set of real business questions and their correct answers. You are unusually well placed to write that eval set, and it is the hardest part.
DevOps and platform engineers
Reliability, security, cost and observability are named across areas two and three, and the emerging operational surface for autonomous systems is unclaimed territory in most organisations. Somebody has to own credentials for agent identities, audit trails for actions taken without a human, rollback for a system that acts, and the pager for all of it. That is a platform problem and it is arriving now.
The gap is evaluating probabilistic output. Your monitoring vocabulary assumes services that are up or down and responses that are correct or erroneous. A system that is up, fast, and quietly wrong twelve percent of the time does not trip any alert you currently have.
First move:
build the platform layer for one agent: scoped credentials, per-tool permissions, full audit of actions, and a quality signal in your dashboards alongside latency and error rate.
Engineering managers and tech leads
Your leverage is now in the review layer and in team norms. When four engineers each direct several agents, throughput rises and so does the volume of code nobody has thought carefully about. The bottleneck moves from production to judgment, and judgment is a team property you can design for.
The gap is that you need enough hands-on fluency to read agent output critically at speed, which is difficult to maintain from a calendar full of meetings. It is also on you to answer the open question from the previous section: what your standard is for reviewing and owning code that no human typed.
First move:
write your team's standard for agent-assisted work. What must be reviewed by a human, what must have a verifier, what may never be delegated, and who owns the result. Then use it for a month and revise it.
Domain experts who are not engineers
You are in a better position than you probably believe, and the reason is area four. The scarce input in most applied AI projects is not engineering, it is knowing which cases matter, which failures are unacceptable, and which regulation governs. An eval set written by a genuine expert is an asset that a strong engineering team cannot produce for themselves at any speed.
The gap is real and it is area two, from close to zero. Be realistic: coding agents make you far more capable than you would have been alone, and they do not substitute for understanding what the system is doing. The honest framing is that you can now build useful things, and you should be careful about what you deploy without an engineer.
First move:
write the eval set nobody else in your organisation could write. Fifty real cases with correct answers and the reasoning behind them. Then find an engineer to trade with. That document is worth more than the demo you were considering building.
New graduates and career changers
This is the hardest read, and it deserves directness rather than encouragement.
The rung you would traditionally have climbed, competent implementation of well-specified work under supervision, is the rung agents now cover most completely. That does not close the field, and the letter says nothing specific about entry-level hiring in either direction. But the entry requirement has moved from "can you implement this" to "can you tell whether this is right", and no first job will hand you that experience the way the old ladder did.
So it has to be manufactured deliberately. The good news is that the tools that removed the old rung also let one person build and deploy far more than a graduate could have five years ago. The portfolio that works now is not three tutorials with different colour schemes. It is three small deployed systems, each with an eval set, a stated cost per task, a documented failure mode and an honest limitation. That collection demonstrates judgment, and judgment is the thing that is scarce.
Two further specifics. First, do not skip fundamentals on the theory that agents cover them. Area two says the opposite, and the market is currently full of people who can produce a working prototype and cannot tell you why it will fall over. Second, depth in one domain beats breadth across five. The graduate who understands one regulated industry properly is competing in a much smaller field than the graduate who has touched every framework.
First move:
the twelve week programme above, in full, in public. Publish each artifact with its numbers and its limits. Twelve weeks of that is a stronger claim than most résumés carry.
Founders are covered in their own section below, because the question deserves more than a paragraph, and because the shape of the argument is clearest there.
The roles that emerged, and the ones emerging now
Two related questions come up constantly: what jobs will exist, and which title should I aim for. The second is the wrong question, and the map explains why. Ng framed these as skills rather than jobs precisely because they recombine into titles faster than anyone can train for a specific one.
It is still worth naming them, because a title is how a budget gets approved and how a job advertisement gets written. Below are twelve, split into the ones already being hired for and the ones we currently see splitting off from existing roles inside client organisations. The second group is where the arbitrage is, because the skill is scarce and the title does not yet have a salary band attached.
Each of these is a slice of the four areas that grew large enough to need its own person. Build the areas and the titles become interchangeable.
Some of these are already advertised. The
AI forward deployed engineer
, an engineer embedded inside a client organisation to customise and tune agentic workflows for that organisation's reality, was described by
Ng himself in June 2026
as one of the buzzy new roles in Silicon Valley. It is areas one, three and four with a customer in the room, and it is a very good job for someone with domain depth.
Others are functions still splitting off from existing roles.
Evaluation engineer
is the clearest case: the person who owns datasets, graders and release gates, and who can prove to someone outside the building that the system works.
Context engineer
owns what enters the model's window and why, which is retrieval, compression, eviction policy and a token budget treated as a design artifact.
Agent operations
is on-call for systems that act.
AI product engineer
is area four with implementation attached, and is probably the closest thing to the full-stack role of this era.
AI assurance and governance
maps systems to frameworks such as the NIST AI Risk Management Framework and the EU AI Act with evidence rather than policy documents, and in regulated sectors it is becoming a condition of deployment rather than an afterthought.
Six more we are watching form
AI systems engineer
The spine from earlier in this article, held by a person. Owns requirements, interface contracts, the verification plan and the configuration baseline for an AI system, and signs that it meets what was asked. Closest existing analogue is a systems engineer in aerospace or defence, and in our experience people from those backgrounds convert into this faster than anyone from a pure software track.
Agent security engineer
Splitting off from application security, because the threat model genuinely changed. Prompt injection through retrieved content, tool scoping, agent identity and credentials, exfiltration through a summarisation step, and adversarial testing of a system that can be talked into things. Conventional application security training does not cover an attacker who writes English.
AI reliability engineer
Site reliability engineering for probabilistic systems. The existing discipline assumes services are up or down and responses correct or erroneous. This role owns the service level objectives for a system that is up, fast, and quietly wrong some percentage of the time, which requires quality as a monitored signal sitting beside latency and error rate.
AI cost and capacity analyst
Financial operations pointed at tokens, and increasingly its own job at scale. Cost per resolved task by workflow, model routing policy, cache hit economics, and the build against buy question every quarter as prices move. We have seen this pay for itself inside a month at organisations spending seriously on inference.
Data curation and eval set owner
Distinct from data engineering, and distinct from evaluation engineering. This is the person who decides which cases represent the problem, sources them, labels them with domain experts, and maintains them as the world changes. It is closer to editorial judgment than to pipeline work, and it is the highest-leverage job in the building that nobody has a title for.
Human review operations lead
Where a system keeps a human in the loop at volume, somebody has to design that loop: what gets escalated, how a reviewer sees enough context to decide quickly, how reviewer decisions feed back into the eval set, and how you detect a reviewer rubber-stamping. This is operations design, and it is the difference between a human-in-the-loop claim and a real control.
The pattern worth noticing: every one of these is a recombination of the same four areas, weighted differently, with the systems engineering spine holding several of them together. That is the argument for training on the areas and staying indifferent to the title. A title tells you which slice an organisation has decided to staff. It does not tell you what to learn.
One caution on the second group. A role that is splitting off is a real opportunity and a real risk. The upside is that scarce skill with no salary band attached is usually underpriced relative to its value, and you can define the job. The downside is that a function which has not settled can be reabsorbed, so hold it as a specialisation on top of a durable base rather than instead of one. That base is the four areas, and for most people it is still best acquired as a working software engineer, which is the next section.
How to become a software engineer, now that agents write the code
This is the question we get more than any other, and it now arrives with an anxious clause attached: is it still worth it if the machine can write the code? The short answer is yes, and more than before, but the path has changed shape and following the old one will leave you optimising for the depreciating column.
The long answer is six steps. Each has a milestone you can check, and the order matters, because each step is the prerequisite for judging the next one honestly.
Before the steps, the honest framing. The old path assumed that if you could produce working code you would be given a job producing working code, and that judgment would accumulate as a side effect over several years of doing that. The first half of that assumption is what broke. Production is no longer scarce, so nobody will pay you for years while judgment accrues quietly. You have to acquire judgment deliberately and demonstrate it early, which is what every milestone below is designed to produce.
What this path is not
It is not a certification sequence and it is not a language checklist. Certifications are useful as structured reading and weak as evidence. The service that has been running for a month, and the incident you diagnosed at midnight, are the evidence.
Is the field still worth entering
Yes. More software is being written, by more people, against more ambitious problems. What shrank is the number of people paid purely to type it. Enter for the judgment, not for the typing, and the field is larger than it has ever been.
Both routes, and a positioning grid for deciding which build to attempt given what you currently hold.
1. One language, properly.
Python or TypeScript are the pragmatic defaults, and the choice matters far less than the depth. Properly means modules rather than scripts, functions with types, a test suite, dependency management, error handling that distinguishes expected failure from a bug, and code somebody else can run without you in the room. The temptation now is to skip this because an agent will write it for you. Do not. This is the layer you will be checking the agent against for the rest of your career, and you cannot check what you have never built.
Milestone:
a small installable package with a test suite and a readme, on a public repository, that a stranger can install and use.
2. Read code faster than you write it.
This is the step that did not exist on the old path and now belongs second. Your working life is going to consist largely of judging code you did not write, most of it produced seconds ago by a machine with no stake in it. Reading fluency is trainable and almost nobody trains it deliberately. Do it by working inside codebases that are not yours: read a library you depend on until you can explain its main abstraction, then fix something real in it.
Milestone:
a merged pull request in a project you did not start, where you had to understand surrounding code to make the change safely.
3. Build and operate a service.
Not build. Build and operate. An HTTP service with persistent storage, authentication, a deployment you can repeat, structured logs you can query, and a metric you actually look at. Operating is the part that teaches, because it is where you learn that a thing which runs is different from a thing which runs at three in the morning while you are asleep.
Milestone:
a service that has been live for a month, with one incident you diagnosed from your own logs and wrote up afterwards.
4. Make correctness executable.
Tests, continuous integration, and a gate that can block a merge. Then extend the same instinct to the parts that are not deterministic, which means an eval set with a threshold. This step is the one that converts you from someone with opinions about quality into someone who can prove it, and it is the precise skill that lets you direct an agent rather than negotiate with it.
Milestone:
a continuous integration gate that has blocked one of your own changes, and you agreed with it.
5. Design the system, not the file.
Where the boundaries go, what crosses them, what each side may assume, how data is modelled, what happens when a dependency is slow or absent, and what the thing costs per unit of work. This is where the systems engineering spine starts to matter, and it is the level agents are weakest at, which is exactly why it is where your value concentrates.
Milestone:
a design document for something non-trivial, reviewed by somebody more experienced, that records the option you rejected and why.
6. Direct agents against a specification you wrote.
Now put it together. Take a feature, write the specification including what is out of scope, have agents implement it, review the result against your own criteria, and take responsibility for it in production. Judge yourself on the specification and the review, not on the implementation.
Milestone:
something in production that you specified, an agent largely wrote, you reviewed line by line, and you are on call for.
Two honest notes about where people stall. Steps three and four are where most self-taught engineers stop, and they are the two that most distinguish a professional from an enthusiast, because both require operating something over time rather than building it once. Time is the input and it cannot be compressed. Second, step two is the one most likely to be skipped entirely, because reading is invisible work that produces nothing to show. Skip it and you will hit a ceiling the moment your job becomes reviewing rather than producing, which is now roughly your second year.
Time to competence, honestly
Twelve to twenty four months to employable from a technical starting point, longer from a non-technical one. Anyone promising a twelve week timeline is selling the twelve week course. Steps three and four require operating something over time, and that is a calendar constraint, not an effort one.
What employers check now
Can you explain code you did not write, out loud, under questioning
Have you been on call for something you built
Can you show a test or eval that blocked a change
Can you state what your system costs to run
Can you describe a decision you got wrong and how you found out
The portfolio that works
Not five tutorials with different colour schemes. Three deployed systems, each with a specification, an eval or test suite, a stated cost, a documented failure mode, and an honest limitation. Depth of evidence beats breadth of frameworks by a wide margin.
Routing in from where you actually are
From no technical background
Steps one through three in order, and give step one longer than feels necessary. The risk specific to your position is that agents make you productive before you are competent, which feels like progress and is not. Deliberately write some things without assistance, purely as training, the way a pilot practises manual flight. Expect two years and plan your finances for it.
From analytics or SQL work
You have data modelling judgment already, which is most of step five, and you are usually missing steps one, three and four. Version control as a habit, packaging, and deployment are the specific gaps that SQL-centred careers allow you to skip. Your advantage is that you know what the business means by its terms, which is scarce and hard to teach.
From data engineering
You hold steps one and three in a pipeline shape and need them in a service shape, which is a smaller move than it sounds. Your real gap is usually step two, reading unfamiliar application code, and the non-determinism adjustment described in your role card above. Retrieval, freshness and lineage are already yours, so area one is closer than you think.
From science or research
You have statistical thinking, which is the hardest thing for traditionally trained engineers to acquire, and you are usually missing all of step three. The notebook to production distance is the whole assignment. Treat step one as non-optional even though you can already write code that works, because "works" and "someone else can operate it" are different standards.
From a bootcamp or a degree
You likely have step one and a version of step four, and almost never step three, because operating something is hard to fit into a course. Go straight there. A single service you have run for a month is worth more in an interview than every project in the curriculum, precisely because it is the part the curriculum could not give you.
From a domain career, changing lanes
Your domain knowledge is an asset the map values highly, and the mistake is discarding it to start over as a generic junior. Do not. Aim at software engineering inside the industry you already understand, where your knowledge of which failures are unacceptable makes you immediately useful. This is the fastest route we see work for people over thirty five.
A closing note on the entry-level question, because it sits underneath all six routes. It is genuinely harder to get the first job than it was in 2019, and it is dishonest to pretend otherwise. The mechanism is the depreciating column: the traditional first job was largely implementation of well-specified work under supervision, and that is the part agents cover most completely.
What has not changed is that organisations still need people who can be trusted with consequences, and they have no reliable way to identify them. That is the opening. Every milestone in this section exists because it is a piece of evidence about trustworthiness rather than about productivity. A candidate who can walk through an incident they diagnosed, a change their own gate blocked, and a decision they got wrong is answering the only question the hiring manager actually has, and very few candidates are answering it.
If you want the compressed version of all six steps against an AI system specifically, that is exactly what
the twelve week programme
above is. Run it in public, with the systems engineering thread made explicit, and you finish with six artifacts and a revised requirements note. That collection is a stronger claim than most résumés carry.
On data engineering
An earlier version of this article routed this section toward data engineering, which remains an excellent adjacent bet for the reasons in
the role card
above: retrieval is a serving layer, and every quality complaint ends in the data path. Software engineering is the broader base, and steps one through five carry across to it almost entirely.
If you already have the job
Run the six steps as an audit rather than a curriculum. Most working engineers can produce evidence for one, three and five, and stall on two, four and six. Those three are the ones the market is now pricing.
How to turn this into a company
The other question we get constantly. The skills map makes a specific and useful argument here, even though it never mentions startups: if implementation is cheap and judgment is scarce, then the barrier to starting something has fallen dramatically while the barrier to starting something
worth doing
has not moved at all.
That asymmetry explains most of what is happening in the market. The number of people who can build a working AI product has increased enormously. The number who can identify a problem worth solving, grade the solution honestly, and make the unit economics work has not. Area four is the whole game.
Five steps, in this order, and the order matters more than any individual step.
The most common failure
Building the product before the eval. If you cannot grade the output, you cannot tell a customer why they should trust it, you cannot improve it deliberately, and you cannot tell whether a model change helped. Companies die here quietly, looking busy.
1. Pick a domain you actually know.
Your advantage is never the model, because everyone can call the same model. It is the edge cases you already have in your head, the vocabulary you use correctly without thinking, and the reason the obvious solution does not work in your industry. If you do not have a domain, that is the first thing to acquire, and it is worth taking a job to get it.
2. Find the expensive, repeated, judgment-heavy task.
The shape to look for is work that is done many times, requires expertise, is currently done by hand, and where being wrong is noticed. Being noticed matters: it means the task has an implicit quality bar you can measure against, which becomes your eval set.
3. Write the eval before you build the app.
Fifty real cases with correct answers, sourced from the domain rather than imagined. This is your specification, your sales argument and your development loop, all in one document. It is also the step that tells you honestly whether the problem is tractable, before you spend six months finding out.
4. Ship a thin slice fast, to one real customer.
One workflow, real data, and ideally real money, even a small amount. The letter's area four language about knowing when to test a quick MVP applies precisely here. A slice in production teaches you more in two weeks than a quarter of design.
5. Prove the unit economics before you scale.
Cost per resolved task below the price you can charge, with the margin surviving the cases that need a retry, a verifier and a human review. AI companies can grow revenue and lose more money per customer as they do. Know your number before you find out at scale.
The two by two in the figure above is the positioning question underneath all of this. Strong engineering and thin domain knowledge means you should build tools for engineers or find a founding partner who lives in the problem. Strong domain and thin engineering means your eval set is the asset, and you should trade it for build capacity rather than spending a year learning to code alone. Both together is the quadrant where a small team beats an incumbent, because the edge cases are already in your head and the implementation is no longer the hard part. Neither yet means learn in public: pick one domain, one stack, ship small systems monthly, and let the portfolio make the argument for you.
The asymmetry to exploit
The barrier to building something has collapsed. The barrier to building something
worth doing
has not moved at all. Everyone can call the same model; almost nobody can grade the output honestly.
Three questions before you start
Could you write fifty graded examples today, from memory?
Does someone currently pay a person to do this task?
Would being wrong be noticed by the buyer?
Three yes answers is a business. Two is a project. One is a demo.
Where this goes wrong
Five failure modes we would expect from this map, including two that are failures of enthusiasm rather than of the framework.
Treating version zero as the finished artifact
The release is four areas of prose and an explicit promise of more detail to come. Building a rigid training curriculum on it, or worse a hiring rubric, imports a precision that is not there. Use it as a structure for thinking and expect it to change.
Reading software fundamentals as reassurance
It is easy for an experienced engineer to see area two and conclude that nothing much has changed. The letter's actual claim is more demanding: fundamentals matter because you now have to catch tradeoffs you did not make, at the speed an agent makes them. That is harder than making them yourself, and having the knowledge is not the same as applying it at review speed.
Skipping area four because it has no verifier
Three of the four areas can be practised with fast feedback. Area four cannot, so it is the one that gets deferred indefinitely, and it is also the one where value is concentrating. If your training plan has no block that forces you to choose a problem and be wrong about it, you have trained three quarters of the map.
Confusing tool fluency with capability
Being fast in a particular agentic coding tool feels like skill and depreciates like a framework. The durable version is the routine underneath: how you evaluate a new tool, how you decide whether to keep it, and how you rebuild your workflow when it changes. Ng puts that routine inside area three deliberately.
Assuming the map generalises to your regulated context
It is a general map, drawn largely from a general job market. In aviation, pharmaceutical research, defence and federal work the binding constraints are frequently the ones the map does not name: what evidence an auditor requires, what data may not move, and what must remain attributable to a named human. Add those constraints before you plan against it, because they change the architecture, not just the paperwork.
Common questions
Is prompt engineering dead?
Not dead, demoted. It is not one of the four areas, and the letter does not list it as a named building block; it survives as a small component of building AI applications. What replaced it at the top of the list is measurement, error analysis and specification writing. The practical reading is that phrasing a request well is now table stakes rather than an expertise, and the differentiated skill is knowing what correct means and being able to prove it.
Do I still need to learn machine learning and the mathematics?
The letter names machine learning, deep learning and statistical techniques inside area one, so it does not treat them as obsolete. What has clearly changed is the weighting: training models from scratch is not discussed, and the emphasis is on the system around a model rather than the model itself. Our practical answer is that you need enough statistics to design an evaluation and reason about a distribution, which is a real requirement, and you do not need to be able to derive backpropagation to be excellent at this work. If you intend to do research, that answer changes entirely.
Which of the four areas should I start with?
Start with whichever one your current job does not force you to practise, which is the gap column in the role matrix above. If you are starting from nothing, go in the letter's own order, because area one gives you something to build, area two makes it survivable, area three makes you fast, and area four is what you will be evaluated on once the first three are in place.
Is it still worth becoming a software engineer?
Yes, and the map is part of the argument rather than against it. Ng ranks software engineering fundamentals second of four and states that architecture, testing, security, scalability, reliability and cost still matter because you need to understand tradeoffs well enough to steer agents correctly. What changed is which parts of the job carry the value: reading, boundary decisions, verification design and specification went up, while syntax recall, boilerplate and implementing a finished design went down. Enter for the first list. The
six step path
above is written for exactly this question.
Is programming being replaced or reborn?
Reborn, on the evidence so far. Every previous step up in abstraction, from assembly to compiled languages to managed runtimes and libraries, removed a category of manual work, produced predictions that programmers were finished, and ended with more programmers building more ambitious things. This step differs in one important way: the new abstraction layer is probabilistic rather than deterministic, so specifying precisely and verifying rigorously stop being professional virtues and become the job itself. We work through the three ledgers of what appreciated, depreciated and is genuinely new in
the rebirth section
.
Where does systems engineering fit into all of this?
Nowhere in the letter, and underneath everything in practice. The map names four skills, and skills do not ship; systems do. Requirements, interface control, verification against validation, configuration baselines and hazard analysis are what turn four separate competencies into one system somebody can take responsibility for. It matters more for AI than for conventional software because an agentic application is a system of systems whose interesting failures are emergent and cross-boundary. Our full treatment, including the five documents we actually keep, is in
the systems engineering section
.
Does this mean junior engineers are not being hired?
The letter says nothing about entry-level hiring in either direction, so anyone citing it as evidence on that question is extrapolating, including us. What the map does support is a narrower claim: the specific activity that entry-level work used to consist of, implementing well-specified tasks under supervision, is the activity agents cover best. The reasonable response is not despair, it is to arrive with evidence of judgment rather than evidence of implementation, because implementation is no longer the scarce input.
Is there an official course or curriculum for the four areas?
Not as of this writing. DeepLearning.AI published
AI Coding Workflows: From Cloud to Local
alongside the letter in the same issue, which is relevant to area three, but it is not presented as the official course for the map, and no one-course-per-area plan has been announced. The twelve week programme in this article is ours, not theirs.
How is this different from every other AI roadmap?
Most roadmaps are a list of technologies in a suggested order. This one is a claim about where value sits, derived from what employers were actually asking for across a large corpus of postings and interviews. That is a different kind of object, and it is why the four areas contain almost no product names. The practical difference is that a technology roadmap expires when the technology does, and this one only expires when the economics change.
What if I disagree with the four areas?
Reasonable people already do, and the critiques are worth reading. The most substantive ones argue that four broad labels are not a usable competence map without connecting each competency to the failure it prevents, and that specific areas deserve their own place: user experience design for systems that are slow and sometimes wrong, data curation, cost management, and the human collaboration norms needed when several people share a codebase written mostly by agents. Our own seven additions overlap with several of those, and our largest disagreement is the omission of systems engineering, which we think is the difference between four skills and a shipped system. Ng has invited feedback through a survey linked from the letter, which suggests the map is expected to move.
Next steps
If you read nothing else, read the source:
The AI Engineering Skills Map
takes about six minutes and is worth forming your own view on before accepting anyone's summary, including this one.
If you want to act on it today, run one error analysis session on something you already operate. Fifty real interactions, read by hand, categorised, counted, largest class fixed and added to an eval set. It is the cheapest exercise on this page and reliably the most informative.
If you are an engineer wondering where you stand, do the ledger exercise from
the rebirth section
on last week's calendar. Split your hours into what appreciated, what depreciated, and what is genuinely new. It takes fifteen minutes and it produces a specific list rather than a vague unease.
If you are responsible for something reaching production, write the two documents from
the systems engineering section
: a one page requirements note and an evaluation plan that maps each requirement to the evidence that satisfies it. Most teams discover a requirement nobody can currently satisfy, and discovering it on paper is considerably cheaper than discovering it in a deployment review.
If you are building the underlying machinery, the engineering detail sits in our other Signals:
agent harness architecture
for the loop itself,
the evaluation harness
for area one,
context engineering as a budget
for the retrieval and window problem,
cost and latency engineering
for week nine, and
prompt injection and LLM security
for the trust boundary work. What we test in the open is published in
the AI Lab
, and the full library is on the
Signals index
.
If you are deciding how to train a team against this map rather than yourself, that is a conversation worth having properly.
Talk to the engineers
who ship this work.
The one exercise
Fifty real interactions. Read by hand. Categorised. Counted. Largest class fixed and added to an eval set.
It costs an afternoon, needs no new tooling, and it is the closest thing to a free lunch on this entire page.
Corrections
Everything attributed to Ng is sourced to the letter. If we have misread him anywhere, we would rather know. The distinction between his claims and ours is deliberate throughout, and any blurring of it is our error.
by
Dr. Fereydun Hashemi
Zorost Intelligence
( Go Deeper )
The AI Lab
How we engineer agents, retrieval, and calibrated models.
Visit >>
( Briefing )
Talk to the engineers
A working session on this topic with the team that ships it.
Get in touch >>
Related Signals
Agentic AI Engineering
Structured output: getting data instead of prose from a model
24 JUL 2026
>>
Agentic AI Engineering
Agent failure taxonomy: ten classes, with recovery for each
24 JUL 2026
>>
Agentic AI Engineering
Cost and latency engineering for LLM systems
24 JUL 2026
>>
Agentic AI Engineering
Prompt injection: securing an LLM system that reads untrusted text
24 JUL 2026
>>
All Signals