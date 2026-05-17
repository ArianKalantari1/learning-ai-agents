# Capstone 13 — Constitutional AI & Self-Critique

**XP:** 850  
**Difficulty:** Expert  
**Requires:** Levels 1–10 (especially Level 10 — safety, HITL, advanced patterns)  
**Estimated build time:** 4–5 days  
**API cost:** ~$0.20–0.60 per conversation (2-3x a standard chatbot — self-critique requires extra passes)

---

## Why This Exists

Every AI system you build will eventually produce an output that causes harm.

Not maliciously. Not because the model is broken. Because language models predict plausible text, and plausible text is not always safe, accurate, or appropriate. When an AI system is making decisions — in customer service, in healthcare, in education, in legal contexts — the cost of a bad output is real.

Constitutional AI is Anthropic's approach to this problem. Instead of relying entirely on RLHF (human feedback on millions of examples) to train alignment, it adds a self-critique layer: the model generates a response, then critiques that response against a set of principles (the "constitution"), then revises the response based on the critique. The revised response is demonstrably safer and more helpful than the first.

This capstone implements Constitutional AI from scratch — not by calling a pre-aligned model, but by building the critique-revision loop yourself. You will specify your own constitution, build the critique agent, build the revision agent, and measure the improvement. Then you'll understand not just that aligned AI works, but how it works and why.

---

## What This Unlocks

**Roles:**
- AI Safety Engineer — the role dedicated to making AI systems behave as intended
- GenAI Lead — you cannot lead an AI team responsibly without understanding alignment
- AI Researcher — this is foundational to the current state of the field
- Any senior AI role at a company where AI is used in high-stakes contexts (healthcare, finance, legal, education)

**Why this matters beyond the job market:**
AI safety is not a niche concern. As AI systems are deployed in more consequential contexts — medical advice, legal guidance, educational content, hiring decisions — the question of whether they behave reliably according to values becomes critical. The engineer who understands both the capability and the alignment is more valuable than the engineer who only knows the capability.

**What you can say:** "I implemented the Constitutional AI critique-revision loop from scratch. I specified my own constitution, built the judge and reviser agents, and ran a rigorous comparison showing the improvement. Here's the data on where it helps most and where it fails to catch harmful outputs."

---

## The System

Build a chatbot with Constitutional AI. The system has three phases for every response:

**Phase 1 — Generation**
The base chatbot generates an initial response. No filtering, no critique. Raw generation.

**Phase 2 — Critique**
A separate critique agent evaluates the initial response against the constitution. It produces a structured critique: which principles (if any) does this response violate? How severely? What specifically is problematic?

**Phase 3 — Revision**
A revision agent receives the initial response and the critique. It produces a revised response that addresses the identified issues while maintaining helpfulness. If the critique found no issues, the revision agent passes through the original.

The user only sees the revised response. The critique is logged for analysis.

---

## Technologies

| Component | Technology | Why |
|-----------|-----------|-----|
| Base chatbot | Claude Haiku (fast, cheap for base generation) | First pass doesn't need high quality — the critique loop improves it |
| Critique agent | Claude Sonnet (high reasoning quality) | Critique requires careful evaluation, not just generation |
| Revision agent | Claude Haiku (guided by the critique) | Revision is constrained by the critique — lower reasoning burden |
| Constitution storage | YAML or JSON file | Version-controlled, human-readable principles |
| Evaluation framework | Your Capstone 6 framework | Measure improvement across versions |
| Logging | Structured JSON | Store initial response + critique + revision for analysis |

---

## Writing a Constitution

The constitution is a list of principles that your AI system must uphold. Each principle must be:
- **Specific enough to evaluate** — "be helpful" is not a principle; "do not recommend medical treatments without noting the importance of consulting a doctor" is
- **Prioritised** — when principles conflict, which wins?
- **Testable** — you must be able to write a test case that violates the principle and verify the critique catches it

**Example constitution for an educational chatbot:**

```yaml
principles:
  - id: accuracy
    priority: 1
    statement: "Do not state facts you are uncertain about as if they are certain. Use hedging language ('research suggests', 'generally', 'in most cases') when appropriate."
    
  - id: age_appropriate
    priority: 1  
    statement: "Responses must be appropriate for the student's stated age level. Do not expose younger students to content appropriate only for adults."
    
  - id: no_doing_work_for_student
    priority: 2
    statement: "Do not complete assignments, write essays, or solve problems for the student. Guide them to the answer rather than providing it."
    
  - id: intellectual_honesty
    priority: 2
    statement: "Acknowledge the limits of your knowledge. If a question is beyond the scope of what you can reliably answer, say so."
    
  - id: source_attribution
    priority: 3
    statement: "When making factual claims, indicate the general category of source (research, historical record, established science) rather than presenting opinions as facts."
```

---

## Research Areas

- **Constitutional AI** — Anthropic's original paper and the technique itself
- **RLHF (Reinforcement Learning from Human Feedback)** — the alignment technique Constitutional AI was designed to complement
- **Value alignment** — the broader problem of encoding human values into AI systems
- **Specification gaming** — how AI systems find unexpected ways to satisfy their objectives that violate the intent
- **Goodhart's Law revisited** — the challenges of measuring alignment vs achieving it
- **AI ethics** — not as a compliance exercise but as a design question: whose values should the constitution encode?

**Papers worth reading:**
- "Constitutional AI: Harmlessness from AI Feedback" (Bai et al., 2022) — the original Anthropic paper
- "Training Language Models to Follow Instructions with Human Feedback" (Ouyang et al., 2022) — RLHF
- "Concrete Problems in AI Safety" (Amodei et al., 2016) — the foundational safety research agenda
- "Reward Hacking and the Alignment Problem" — Anthropic alignment research

---

## Agent Team

| Agent | Role |
|-------|------|
| Base Generator | Produces the initial response to the user's message. System prompt is minimal — this is the unconstrained version. The point is to see what the model does without the constitutional layer. |
| Principle Classifier | Before critique: identifies which principles in the constitution are potentially relevant to this response. Not all principles apply to all responses — don't run irrelevant checks. |
| Critique Agent | For each relevant principle: evaluates whether the initial response violates it. Returns: `{principle_id: str, violation: bool, severity: "none"|"minor"|"major"|"critical", explanation: str, specific_text: str}` |
| Revision Agent | Receives the initial response and the critique. Revises to address all non-none severity violations while maintaining helpfulness. If it cannot address a violation without making the response unhelpful, it flags the conflict. |
| Conflict Resolver | When the revision agent flags a principle-helpfulness conflict: applies the priority ordering from the constitution. High-priority safety principles override helpfulness. Low-priority style principles yield to helpfulness. |
| Quality Checker | Post-revision: verifies the revised response still answers the user's actual question. A response that passes all constitutional checks but doesn't help the user has failed. |

---

## Build Stages

### Part A — Constitution Design
Write your constitution for a specific use case (education, customer service, medical information — pick one). Minimum 8 principles across at least 3 priority levels. For each principle, write:
- 2 test inputs that should trigger a violation
- 1 test input that should pass without triggering a violation

If you can't write these test cases, the principle is too vague.

### Part B — Base System + Logging
Build the base chatbot and the logging layer. Before any critique: run your 24 test cases (8 principles × 3 test inputs) through the base system. Log every input/output. Measure: how many of the known-violation inputs does the base system actually produce harmful outputs for? This is your baseline.

### Part C — Critique Agent
Build the critique agent. For each principle: does it correctly identify violations and non-violations? Evaluate on your 24 test cases. Measure: precision (did it flag actual violations?) and recall (did it miss violations?). A critique agent with low recall is dangerous — it gives a false sense of safety.

### Part D — Revision Agent
Build the revision agent. Run the complete pipeline (generate → critique → revise) on your 24 test cases. Measure:
- Did revision address the identified violations?
- Did revision preserve the helpful content?
- Did revision introduce new violations while fixing old ones?

### Part E — Helpfulness Cost
This is the hardest tradeoff. Constitutional AI makes outputs safer but sometimes less useful. Run 20 benign requests through the full pipeline. Measure quality before and after revision using your eval framework. What is the helpfulness cost of the constitutional layer? Where does it over-refuse?

### Part F — Failure Mode Analysis
Find the inputs that break your system:
- Inputs that trigger violations the critique misses
- Inputs where the revision fails to fix the violation
- Inputs where the revision is so constrained it becomes unhelpful
- Inputs that reveal conflicts between principles

Document each failure. Explain why it happened. Propose a fix where one exists.

### Part G — Full Evaluation Report
Write 500–800 words: What does your constitution cover well? Where does it fail? What is the helpfulness cost? If you were deploying this in your chosen use case, what additional principles would you add? What principles would you remove because they don't justify their helpfulness cost?

---

## Completion Checklist

- [ ] Constitution: 8+ principles, 3 priority levels, 3 test cases per principle written before coding
- [ ] Base system baseline: 24 test cases run, violation rate documented
- [ ] Critique agent: precision and recall measured on all 24 test cases
- [ ] Revision agent: violation fix rate measured, helpfulness preservation measured
- [ ] Full pipeline: generate → critique → revise working end-to-end
- [ ] Helpfulness cost measured: 20 benign requests, quality before vs after revision
- [ ] Failure mode analysis: at least 5 inputs that break the system, documented with explanation
- [ ] Principle conflict: at least 1 case where principles conflict documented and resolved per priority order
- [ ] Evaluation report: 500+ words, honest about what works and what doesn't

---

## What Completing This Demonstrates

- You understand alignment not as a checkbox but as an engineering problem
- You can translate values into testable, specific, prioritised principles
- You have experience with the core tradeoff in AI safety: safety vs helpfulness
- You understand why Constitutional AI works and where it fails

The AI field is moving fast and the safety question is following it. The engineer who can build capable AI systems AND reason carefully about their alignment is increasingly who gets trusted with the most consequential applications. This capstone builds both muscles simultaneously.
