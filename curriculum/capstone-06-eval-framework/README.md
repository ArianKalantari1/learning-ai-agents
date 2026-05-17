# Capstone 6 — LLM Evaluation Framework

**XP:** 700  
**Difficulty:** Advanced  
**Requires:** Levels 1–8 (evaluation concepts, observability, multi-agent basics)  
**Estimated build time:** 3–4 days  
**API cost:** ~$0.05–0.20 per eval run (LLM-as-judge calls)

---

## Why This Exists

Almost every team building AI products has the same problem: they don't know if their system is getting better or worse.

They ship a new prompt. They run it manually on 5 examples. It looks fine. They push to production. Two weeks later users complain the answers are worse. The team has no data to investigate with. They don't know what changed, when it changed, or what to roll back to.

This is the most common failure mode in production AI — not the model, not the architecture, but the absence of systematic evaluation. Without evals, every change is a guess. With evals, changes become decisions.

The person on any AI team who builds and owns the eval framework is indispensable. They are the person who can say "version 3 is 12% worse on factual accuracy and 8% better on tone — here's the tradeoff." No one can make a responsible product decision without that person.

This capstone builds that capability from scratch.

---

## What This Unlocks

**Roles:**
- AI/ML Engineer with evaluation specialisation (rare and valued)
- AI Platform Engineer ("the person who makes the rest of the team's work measurable")
- GenAI Lead — you cannot lead an AI team without evaluation infrastructure
- ML Ops Engineer who understands the LLM-specific evaluation problem

**What sets you apart:** Anyone can prompt an LLM and say "it looks good." Very few people have built a systematic framework that catches regressions before they reach users. This is the difference between a junior AI engineer and someone trusted to lead.

**What you can say:** "I built an evaluation framework for an LLM application. It catches quality regressions automatically, measures cost and latency per version, and uses LLM-as-judge for dimensions that can't be measured with exact matching. Here's the dashboard."

---

## The System

Build an evaluation framework for an LLM application that:

1. Runs a test suite of questions against any version of the system
2. Scores each answer across multiple dimensions using LLM-as-judge
3. Compares results across versions to detect regressions
4. Tracks cost and latency per version alongside quality metrics
5. Flags specific question types where a new version underperforms the previous one
6. Produces a report that a non-technical person can read and act on

The framework must be applicable to any LLM system — you build it against one of your existing capstones (recommended: Capstone 1 — Research Intelligence Network).

---

## Technologies

| Component | Technology | Why |
|-----------|-----------|-----|
| Eval runner | Python + pytest-style structure | Reproducible, version-controlled test suites |
| LLM-as-judge | Claude Sonnet or GPT-4 | Scores answers on subjective dimensions |
| Metrics storage | SQLite or Postgres | Per-run, per-question results need to be queryable |
| Dashboard | Streamlit or Evidence.dev | Visualise metric trends across versions |
| RAGAS | ragas Python library | Pre-built RAG-specific metrics (faithfulness, relevance) |
| Regression detection | Statistical comparison (Wilcoxon test or simple delta threshold) | Know when a change is signal vs noise |

---

## The Four Evaluation Dimensions

Not all quality is measurable the same way. You need different techniques for different dimensions.

**1 — Exact Match (for factual questions with known answers)**
Is "Paris" the right answer? Simple string comparison. Only works when ground truth is known.

**2 — RAGAS Metrics (for RAG systems)**
Faithfulness (are claims supported by sources?), answer relevance, context precision, context recall. Use the ragas library. These are automated and don't require LLM calls.

**3 — LLM-as-Judge (for subjective quality)**
Use a second LLM to score the answer on a rubric: accuracy (1–5), completeness (1–5), clarity (1–5), appropriate tone (1–5). The judge LLM must use chain-of-thought before scoring — scoring without reasoning is unreliable.

**4 — Human Review (for calibration)**
For 10% of your eval set, have a human score alongside the LLM judge. Calculate inter-rater agreement. If the LLM judge and human disagree consistently, your judge prompt needs revision.

---

## Research Areas

- **LLM-as-judge reliability** — when can you trust an LLM to evaluate another LLM? When can't you?
- **Goodhart's Law in AI evaluation** — "when a measure becomes a target, it ceases to be a good measure"
- **Evaluation dataset construction** — what makes a good test set? How do you avoid test set contamination?
- **Inter-rater reliability** — how to measure agreement between evaluators (Cohen's Kappa)
- **Calibration** — the relationship between a model's confidence and its actual accuracy

**Papers worth reading:**
- "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena" (Zheng et al., 2023)
- "RAGAS: Automated Evaluation of Retrieval Augmented Generation" (Es et al., 2023)
- "Can Large Language Models be Consistent Evaluators?" (Wang et al., 2023)

---

## Agent Team

This capstone is less about agent orchestration and more about evaluation pipeline architecture. The "agents" here are the evaluation passes:

| Component | Role |
|-----------|------|
| Test Runner | Executes each test question against the system under evaluation. Captures response, latency, and token counts. Stores to database. |
| RAGAS Scorer | For RAG-enabled systems: runs faithfulness, answer relevance, context precision, context recall using the ragas library. |
| LLM Judge | Scores each response on the rubric dimensions. Uses chain-of-thought. Temperature set to 0 for reproducibility. |
| Regression Detector | Compares current run's scores against the previous run. Flags dimensions where the delta exceeds the threshold. Produces a regression report. |
| Cost/Latency Tracker | Aggregates token counts and timing per version. Calculates cost per query at current API pricing. |
| Report Generator | Produces the human-readable report: headline metrics, regressions flagged, question-level breakdown for any dimension that regressed. |

---

## Build Stages

### Part A — Test Suite Design
Before any code: design your test suite. 20–30 questions across at least 3 categories (easy, medium, hard). For each question, write what a good answer looks like — not the exact answer, but the criteria. This is the hardest part of evaluation and it happens before any code.

Questions to ask yourself: What would a bad answer look like? What would a mediocre answer look like? What would an excellent answer look like? Write these down for 5 representative questions. These become your rubric.

### Part B — Test Runner + Storage
Build the runner: execute all 20 questions against your system, store results (question, response, latency, tokens, version tag) in SQLite. Run it twice with the same system to verify reproducibility. Results should be near-identical.

### Part C — LLM Judge
Build the judge. Use Claude Sonnet with a structured scoring prompt:

```
You are evaluating an AI system's response.
Question: {question}
Response: {response}

Score the response on each dimension from 1 to 5.
Think step by step before scoring. Provide your reasoning, then the score.

Dimensions:
- Accuracy: Is the information correct?
- Completeness: Does it fully answer the question?
- Clarity: Is it clear and well-structured?
```

Validate: run the same response through the judge 3 times. Scores should vary by at most 1 point. If they vary more, your prompt needs to be more specific.

### Part D — RAGAS Integration
If your target system uses RAG (Capstone 1 does), integrate ragas. Run faithfulness and answer relevance on your test set. Compare with the LLM judge scores — they should broadly correlate.

### Part E — Regression Detection
Introduce a deliberate regression: modify the system prompt of your target system in a way that makes answers worse. Run the eval. Does the framework detect it? Can you identify which questions regressed and on which dimensions?

This is the test that matters. If the framework misses a 20% quality drop, it's not useful.

### Part F — Dashboard + Report
Build a Streamlit dashboard showing: metric trends across versions, per-dimension scores, question-level breakdown, cost per query by version. Make it readable by someone non-technical.

Run the eval on your system 3 times after making different changes. Show 3 data points on the trend chart.

---

## Completion Checklist

- [ ] Test suite: 20+ questions with documented quality criteria
- [ ] Test runner stores results with version tagging to SQLite
- [ ] LLM judge scoring 4 dimensions with chain-of-thought
- [ ] Judge reproducibility validated: ≤1 point variance across 3 runs on same input
- [ ] RAGAS metrics integrated (faithfulness + answer relevance minimum)
- [ ] Regression detector: flags dimensions where delta > threshold
- [ ] Deliberate regression test passed: framework detected the introduced degradation
- [ ] Cost/latency tracking per version
- [ ] Dashboard with metric trends across 3+ versions
- [ ] Human calibration: 10% of questions reviewed by human, inter-rater agreement calculated

---

## What Completing This Demonstrates

- You understand that "it looks good" is not a quality standard
- You can build systems that make AI quality measurable and comparable across versions
- You understand the limits of LLM-as-judge and how to calibrate it against human review
- You think about AI products as things that must be maintained and monitored, not just shipped

Every serious company building AI products needs this. Most don't have it. Being the person who builds it is one of the highest-leverage contributions an AI engineer can make.
