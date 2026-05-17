# Capstone 3 — Adaptive Learning Coach

**XP:** 800  
**Requires:** Levels 1–10 complete (memory, evaluation, HITL, production)

---

## What This Is

An agent that teaches. Not a static Q&A bot — a system that assesses where you are, builds a personalised curriculum, teaches concept by concept, quizzes, tracks what's landed and what hasn't, and adapts the plan based on results.

The Adaptive Learning Coach demonstrates the hardest cluster of patterns in the curriculum: long-running agents with checkpointing, persistent memory that generalises across sessions, human-in-the-loop gates, and feedback loops that modify the agent's own plan. These patterns are not academic — they're what separates a useful agent from a parlour trick, and they're the architecture of the next generation of enterprise AI tools.

This capstone has no single correct architecture. How you design the feedback loop, how the agent decides when to push a student forward vs re-teach, and how you structure the knowledge base are your decisions. This document gives you the constraints and the evaluation criteria. The design is yours.

---

## The System

Build a learning agent that:

1. Assesses the student's current knowledge before teaching anything
2. Builds a personalised study plan based on the assessment
3. Teaches one concept at a time, mixing explanation and Socratic questioning
4. Quizzes after each concept and scores the result
5. Adapts the curriculum based on quiz performance — re-teaching what hasn't landed, accelerating through what has
6. Remembers where the student is across sessions (close the app, come back the next day, pick up exactly where you left off)
7. Checks in with the student before advancing to harder material (HITL gate)
8. Provides the mentor/operator a dashboard showing each student's progress

The knowledge domain is yours to choose. Default recommendation: use the 10-level curriculum in this repo as the knowledge base. This makes the Adaptive Learning Coach self-referential — it teaches the curriculum it lives inside.

---

## Agent Team

| Agent | Role |
|-------|------|
| Assessment Agent | Runs a structured diagnostic before the first session. Tests breadth (do you know what RAG is?) and depth (explain why cosine similarity works for vector search). Produces a knowledge map: confident / uncertain / blank for each concept in the curriculum. |
| Curriculum Designer | Takes the knowledge map and builds a personalised study plan. Which concepts to teach first? Which to skip? Which need more time? Writes the plan to persistent storage so it survives across sessions. |
| Teaching Agent | Delivers one concept at a time using RAG over the knowledge base. Explains. Gives an example. Asks the student to restate it in their own words before moving on. |
| Socratic Agent | Alternates with the Teaching Agent. Instead of explaining, asks questions that force the student to reason. Knows when to give a hint vs when to wait. |
| Help Agent | Activated when a student explicitly asks for help outside of a quiz or teaching sequence — e.g., "I'm stuck on this build." Manages the five-level help escalation ladder. Tracks which level has already been given for the current stuck point and never repeats a level. Routes to HITL (human mentor) after Level 5. |
| Quiz Agent | Tests understanding with 3–5 questions after each concept. Questions escalate in difficulty. Marks answers and records the score. |
| Progress Tracker | Writes to persistent storage after every interaction: what was taught, quiz scores, time spent, help requests and levels given, student notes. This is the memory layer that survives session restarts. |
| Adaptation Agent | Reviews quiz results after each concept and adjusts the curriculum plan. If score < 70%, queue a re-teach from a different angle. If score is 100%, consider skipping the next introductory concept. |
| Mentor Dashboard Agent | On request (or scheduled), produces a summary for the operator: which students are behind, which concepts are causing the most failures, which students have hit Level 5 help (need human intervention), which students haven't logged in. |

The key architectural insight: the Curriculum Designer's plan is a living document. The Adaptation Agent modifies it. The Progress Tracker reads and writes it. The Help Agent tracks escalation state per stuck instance. Multiple agents share state through a single persistent store — designing that store correctly is most of the architectural work.

---

## Memory Architecture

This is where most implementations fail. Think carefully before you build.

**What needs to persist across sessions:**
- The student's knowledge map (from Assessment)
- The curriculum plan (from Curriculum Designer, modified by Adaptation Agent)
- Every concept taught: when, how, what example was used
- Every quiz: questions asked, answers given, score
- Student-written notes
- Time spent per concept

**What does NOT need to persist:**
- The conversation messages list (each session starts fresh from a state summary)
- Intermediate agent reasoning (unless useful for the dashboard)

**Storage options by scale:**
- JSON files per student: simple, works for a cohort of 5–20 students, breaks at scale
- SQLite: one step up, still local, gives you queries
- Postgres: production-grade, overkill for a cohort MVP

For a 5-person cohort, JSON files per student are fine. Design the schema carefully — changing it mid-cohort means migrating existing student data.

---

## Help Philosophy — The Coach Does Not Do the Work

This is the most important design constraint in the whole capstone.

The coach exists to guide students to understanding, not to hand them answers. A student who asks "what's the answer?" and gets it has learned nothing. A student who asks "I'm stuck, can you help?" and gets a nudge in the right direction has learned something — and remembers it, because they did the final step themselves.

**The rule:** The coach always gives the minimum viable help needed to unblock the student. It never skips levels.

### The Help Escalation Ladder

When a student is stuck and asks for help, the coach works through these levels in order. The student must explicitly ask to go further — the coach never volunteers the next level unprompted.

| Level | What the coach does | Example |
|-------|--------------------|---------| 
| 1 — Reframe | Asks a question that points the student at the right part of the problem | "What does the orchestrator know at that point in the pipeline?" |
| 2 — Hint | One concrete nudge. Not the answer, but a direction | "Think about what happens if two agents try to write to the same state at the same time." |
| 3 — Resource | Points to a specific article, section, or example from the knowledge base | "Take another look at Level 7, the section on asyncio and shared state — it covers exactly this pattern." |
| 4 — Partial reveal | Shows the structure without the substance — a skeleton, a diagram, a pattern name | "The pattern you want is called a mutex. Look up how to use `asyncio.Lock()` in Python and apply it here." |
| 5 — Worked example | Walks through a *different* but analogous problem step by step, then asks the student to apply the same approach to their problem | "Here's how this pattern works in a different context. Now try applying the same logic to your case." |

Level 5 is the maximum. The coach never solves the student's actual problem for them. If a student has been through all five levels and is still stuck, that's a signal to the HITL gate — escalate to the human mentor, not do the work on the student's behalf.

### Why this matters architecturally

This is not just a pedagogical choice. It requires a distinct architectural decision: the Help Agent (see below) must know what level of help has already been given for the current problem, so it doesn't repeat Level 2 when the student is asking for Level 3.

This means the help escalation state is part of the persistent memory schema — per concept, per stuck instance. Add it.

### The student controls the pace of help

The student must explicitly request each level. The coach never says "let me give you a hint" unprompted. The interaction looks like this:

> **Student:** I don't understand how the Section Builder agents share state without overwriting each other.  
> **Coach:** What part specifically is unclear — how they write to the schema, or how writes from parallel agents stay isolated?  
> **Student:** How parallel writes stay isolated.  
> **Coach:** [Level 1 — reframe] Think about what happens if two of them try to update the same field at the same time. What could go wrong?  
> **Student:** One could overwrite the other?  
> **Coach:** Exactly. So what mechanism would prevent that?  
> **Student:** I'm not sure. Can you give me a hint?  
> **Coach:** [Level 2 — hint] There's a standard pattern for protecting shared resources in async code. It involves a "lock." Look that up and come back.  
> **Student:** I found asyncio.Lock but I'm not sure how to apply it here.  
> **Coach:** [Level 3 — resource] Section 3 of Level 7 in the curriculum covers this exact scenario with a code example. Try working through that first.

This is what "guided" looks like. The student is doing the reasoning. The coach is pointing, not carrying.

---

## HITL Gates

The coach must pause and check in with the student at three defined points:

1. **After Assessment:** "Based on your assessment, here's the plan I've put together. Does this look right? Is there anything you want to adjust before we start?"
2. **Before advancing to a new module:** "You've completed [module]. The next module covers [topic] which builds on everything you've done. Ready to continue, or do you want to revisit anything first?"
3. **After three consecutive below-average quiz scores:** "You've found the last three concepts challenging. I'd like to try a different teaching approach before we continue. Is that okay?"
4. **After Level 5 help with no resolution:** "You've been working through this for a while. I think a conversation with your mentor would help more than another hint from me. [Contact mentor link]"

The student must explicitly confirm before the agent advances. This is not optional decoration — it's the pattern that makes a learning agent trustworthy rather than a runaway tutor.

---

## Cost Model

| Setup | Per 30-min session | Notes |
|-------|-------------------|-------|
| Local (Ollama Llama 3.1 8B) | $0 | Reasonable for English content; quiz marking accuracy degrades |
| Claude Haiku | $0.01–0.04 | Suitable for most agents |
| Claude Sonnet | $0.10–0.35 | Use for Assessment Agent and Socratic Agent where nuanced reasoning matters most |
| Recommended split | $0.03–0.10/session | Haiku for quiz, progress, teaching; Sonnet for assessment and Socratic |

**For a 5-student cohort over 5 weeks:** 10 sessions per student × 5 students = 50 sessions. At $0.07/session average: ~$3.50 total API cost. This is not a constraint.

**For the knowledge base:** Use this curriculum as the RAG source. Each level README becomes a retrievable document. Students using the Adaptive Learning Coach to study the curriculum they're building is the intended use.

---

## Build Stages

### Part A — Architecture Design

Before writing any code:

1. Design the persistent state schema — every field, its type, who writes it, who reads it
2. Design the agent roster — system prompt summary, tools, input/output for each agent
3. Design the HITL gates — exactly when does the agent pause? What triggers each gate? What does the student confirm?
4. Design the feedback loop — how does the Adaptation Agent decide to re-teach? What's the threshold? What changes in the curriculum plan?
5. Sketch a session flow — what happens in a student's first session? Their fifth? Their last?

The feedback loop design is the hardest decision. A loop that re-teaches too aggressively becomes frustrating. A loop that advances too readily doesn't help. Make a call, build it, and observe what happens.

### Part B — Core Build

Build the minimum viable coach:

Assessment → Curriculum Plan → Teach one concept → Quiz → record result → HITL gate → continue or re-teach

No dashboard, no Socratic agent, no Adaptation Agent yet. Just the basic loop working end-to-end. Test with yourself as the student. The full loop must run three times without breaking before moving on.

### Part C — Memory and Continuity

Implement the Progress Tracker and persistence layer. Test:
- Close the app. Restart it. Does the student pick up where they left off?
- What does "where they left off" actually mean? (Last concept taught? Last quiz score? Last HITL gate position?)
- Deliberately corrupt the state file. What does the agent do?

Continuity across sessions is non-negotiable. If you can't pass this test, Part B is not complete.

### Part D — Adaptation Loop

Implement the Adaptation Agent and the full feedback loop. Run the coach through at least five concepts with deliberately wrong quiz answers to trigger re-teaching. Verify:
- Re-teaching uses a different explanation approach (not the same text again)
- The curriculum plan is modified and persists
- A student who scores 100% consistently can accelerate past introductory material

### Part E — Socratic Mode and HITL

Add the Socratic Agent and implement all three HITL gates. Test each gate manually — confirm the agent genuinely stops and waits, doesn't simulate a pause and continue anyway.

### Part F — Mentor Dashboard and UI

Build:
- Streamlit UI for the student: conversational, shows where they are in the curriculum, shows quiz scores, allows them to write notes
- Mentor dashboard: table view of all students, progress per student, concepts causing the most failures, days since last session

### Part G — Cohort Pilot

Run the coach with a real user (yourself, a friend, or a cohort student) for at least two sessions covering at least three concepts. Collect:
- Did the assessment reflect their actual knowledge?
- Did the curriculum plan make sense to them?
- Did the HITL gates feel natural or annoying?
- Did re-teaching actually improve quiz scores?
- What would you change?

Document this honestly. Real usage exposes things no amount of test case design catches.

### Part H — Reflection Write-Up

Write 500–1,000 words covering:

1. **What you built:** What can the coach do? What can't it?
2. **The feedback loop in practice:** How well does the Adaptation Agent actually work? Did re-teaching improve quiz scores? Show the data.
3. **The memory question:** What did you store? What did you wish you'd stored? What did you store that turned out to be useless?
4. **HITL in a learning context:** When did the HITL gates feel right? When did they feel intrusive? What would you change?
5. **Persistent memory as a privacy concern:** You are storing detailed learning histories for real people. What are the implications? What would a responsible data policy look like?
6. **Where this goes if you keep building:** What's the one feature that would make this genuinely better?

---

## Completion Checklist

- [ ] Architecture design and state schema documented before coding
- [ ] Help escalation state included in the persistent memory schema
- [ ] Assessment → Curriculum Plan → Teach → Quiz loop working end-to-end
- [ ] Continuity across sessions: student picks up where they left off after restart
- [ ] Adaptation loop: re-teaching triggered by low quiz scores, curriculum plan modified
- [ ] Re-teaching uses a different explanation (not copy-paste of original)
- [ ] Socratic Agent implemented
- [ ] Help Agent implemented with all five escalation levels
- [ ] Help Agent never repeats a level already given for the current stuck point
- [ ] Help Agent escalates to human mentor (HITL) after Level 5 — does not solve the problem itself
- [ ] All four HITL gates implemented and verified (including the Level 5 escalation gate)
- [ ] Mentor dashboard shows which students have hit Level 5 help requests
- [ ] Streamlit UI with quiz display, progress view, and student notes
- [ ] Real user pilot: 2+ sessions, 3+ concepts, at least one help request tested end-to-end
- [ ] Part H reflection write-up complete

---

## What Completing This Demonstrates

- You understand long-running agents with persistent state — the hardest category to build correctly
- You implemented a genuine feedback loop that modifies the agent's own plan based on outcomes
- You used HITL as a trust mechanism, not a UX afterthought
- You managed multi-agent shared state correctly across sessions
- You ran a real-world pilot and have honest data about what worked

The agents that will be commercially significant in the next three years are long-running, personalised, and memory-enabled. This capstone builds all three from scratch.

---

## Cohort Context

If you are building this as part of a cohort program, configure the Adaptive Learning Coach to teach the cohort curriculum — the 10 levels and the CareerSync capstone as the knowledge base. Students use the coach as a 24/7 study resource while they build CareerSync in parallel.

This creates a natural feedback loop: students use the coach to learn the concepts they need, they build CareerSync to apply those concepts, and the coach's progress data tells the program mentor which students are struggling and where.

**Deployment for a cohort:** Host on a small EC2 instance or Railway. Each student gets their own state file. The mentor accesses the dashboard with a separate login. Streamlit Cloud free tier works for an MVP if you're comfortable with shared sessions.
