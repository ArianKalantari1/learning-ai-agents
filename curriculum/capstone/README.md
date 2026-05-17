# Capstone — Research Intelligence Network

**XP:** 600  
**Unlocks:** Everything. This is the final project.  
**Requires:** Levels 1–10 complete

---

## What This Is

A production-grade multi-agent system that takes any complex research or analysis question and completes it through coordinated agent collaboration.

This is not a tutorial. There are no step-by-step instructions. You have the 10 levels. You design the architecture, make the tradeoffs, build the system, and evaluate whether it works. The only constraints are the ones listed in Part A.

---

## Honest Framing

Before you write a line of code, read this.

**What current AI agents actually are:**  
Orchestrated LLMs. The agents in this system do not have goals, intentions, or autonomy. They follow instructions encoded in system prompts, call tools your code provides, and pass text back through a coordinator you designed. The "intelligence" is distributed across the orchestration architecture, the prompts, the tool selection, and the underlying models. Not fake — genuinely useful — but different from what "AI agent" implies in marketing.

**What is real and valuable right now:**
- Complex tasks broken into subtasks get done more reliably than one-shot prompting
- Specialist agents produce better outputs than generalist ones on the same task
- Parallel execution genuinely reduces wall-clock time for independent work
- The critic-analyst pattern genuinely improves output quality
- Human-in-the-loop gates genuinely reduce consequential errors

**What is coming (2–3 years):**
- A2A (Agent-to-Agent) protocol — agents that discover and call other agents without a human-defined orchestrator
- Persistent agents with genuine memory that generalises from experience
- Agent marketplaces where specialist agents are hired dynamically
- Self-improving agent networks that update their own prompts and routing based on outcome feedback

Your capstone builds the foundation layer that those systems will sit on. Part F asks you to write about the gap between what you built and where it's going.

---

## The System

Build a Research Intelligence Network that:

1. Accepts any complex research question via a web interface
2. Deploys a team of specialist agents to complete it
3. Shows the user a live reasoning trace — what each agent did and why
4. Delivers a structured output with sources and confidence levels
5. Runs as a production FastAPI service with streaming
6. Has a working eval suite that measures output quality vs a single-agent baseline

### Agent Team (minimum viable)

| Agent | Role |
|-------|------|
| Commander | Receives the task, decomposes it, routes to the right agents, assembles the final output |
| Researcher | Web search, document retrieval, source evaluation — every claim must come with a source chunk ID |
| Analyst | Synthesises findings, identifies contradictions, fills gaps — writes inline citations per claim |
| Critic | Challenges the analyst's synthesis, forces it to be defended or revised |
| Claim Verifier | Runs NLI over every factual claim against its cited source chunk — flags contradictions and unsupported claims before output |
| Output | Formats the final result with reasoning trace, inline citations, and a hallucination risk summary |

You may add agents. You may not remove the Critic or the Claim Verifier — they are the quality layer that separates this from a chatbot.

### Constraints

- The reasoning trace must be visible to the user (not hidden internal state)
- The system must handle one agent failing without killing the whole pipeline
- You must implement a hard cost ceiling per request
- At least two agents must run in parallel at some point in the pipeline
- The eval suite must compare your system against a single Claude call on the same question
- Every factual claim in the final output must carry an inline citation to a specific retrieved source chunk
- The Claim Verifier must run before the Output Agent — unsupported claims are flagged, not silently included

---

## Hallucination Reduction

This section matters more than any other in the capstone. A research system that produces confident, well-formatted, wrong answers is worse than no system at all.

### The core problem

LLMs hallucinate. They generate text that sounds authoritative and is factually wrong. In a research system this is catastrophic — the user is relying on the output to be accurate. The Critic-Analyst debate improves logical consistency but does not catch factual errors that both agents accept as true.

You need a verification layer that checks claims against sources mechanically, not just conversationally.

### Technique 1 — Inline citation grounding

Every factual claim in every agent's output must reference a specific source chunk by ID.

**How it works:**
- The Researcher returns chunks with IDs: `{ id: "src_03", text: "...", url: "...", retrieved_at: "..." }`
- The Analyst is prompted to write: "Interest rates rose 3% in Q3 [src_03]" not "Interest rates rose"
- The Output Agent renders citations inline and in a reference list
- The Claim Verifier checks that every `[src_XX]` reference actually exists in the source pool

This alone eliminates a large class of hallucinations — the agent cannot confidently assert something it has no source for without the citation being obviously missing.

### Technique 2 — NLI verification pass

Natural Language Inference (NLI) classifies whether a *hypothesis* (a claim made by the agent) is **Entailed**, **Contradicted**, or **Neutral** relative to a *premise* (the source chunk it cites).

**Why this matters:** An agent can cite a source correctly but still misrepresent it. NLI catches this.

**How to implement it:**
```python
from sentence_transformers import CrossEncoder

nli_model = CrossEncoder("cross-encoder/nli-deberta-v3-base")

def verify_claim(claim: str, source_chunk: str) -> dict:
    # returns scores for [contradiction, neutral, entailment]
    scores = nli_model.predict([[source_chunk, claim]])
    label = ["contradiction", "neutral", "entailment"][scores.argmax()]
    return {"claim": claim, "label": label, "confidence": float(scores.max())}
```

Run this for every (claim, source_chunk) pair before the Output Agent renders anything.

**Thresholds:**
- `entailment` with confidence > 0.7 → pass
- `neutral` → flag as "weakly supported" — include but note it
- `contradiction` → block from output, route back to Analyst for correction or removal

The `cross-encoder/nli-deberta-v3-base` model runs locally (no API cost), takes under 100ms per claim on CPU, and is accurate enough for this use case. You do not need a GPU.

### Technique 3 — Atomic claim decomposition

Before running NLI, decompose complex sentences into atomic claims — one fact per claim.

"Interest rates rose 3% in Q3 while inflation remained above target" is two claims.
Run NLI on each separately. A compound sentence can be half-true; atomic decomposition catches this.

Use a small LLM call to decompose: "Break this sentence into individual factual claims, one per line."

### Technique 4 — Consistency checking across workers

When multiple Researcher agents return findings on related topics, their claims about the same facts should agree. If Worker A says "unemployment was 4.2%" and Worker B says "unemployment was 3.8%", that conflict needs resolving before synthesis — not after.

Add a consistency check in the Commander after all workers complete: compare overlapping claims, flag discrepancies, route disagreements to the Analyst as explicit conflicts to resolve rather than silently merging.

### What to log

Every Claim Verifier run should write a structured log:
```json
{
  "claim": "...",
  "source_id": "src_03",
  "nli_label": "entailment",
  "nli_confidence": 0.84,
  "action": "pass"
}
```

This log is the evidence that your system cared about quality. In an interview, showing this log is worth more than showing the final output.

---

## Build Stages

### Part A — Architecture Design

*Before writing any code.*

Produce:
1. A data flow diagram — how does a request move through the system?
2. An agent roster — for each agent: system prompt summary, tools available, input format, output format
3. A communication pattern decision — hub-and-spoke, pipeline, blackboard, or hybrid? Justify it.
4. A failure mode analysis — what breaks if each agent fails? What's the recovery?
5. A cost estimate — tokens per request, estimated cost per 1,000 requests

Do not start Part B until you've reviewed Part A with someone (or written a self-critique of your own design).

### Part B — Core Build

Build the system end-to-end. Working is more important than polished. The full pipeline must run on at least three different test questions before you move on.

Put your code in `builds/`.

### Part C — Stress Testing

Break it deliberately:
- What happens with a vague or ambiguous question?
- What happens when a tool returns an error?
- What happens when the Critic agent disagrees with the Analyst and they loop?
- What happens when the question requires more context than fits in one agent's context window?
- What's the most expensive request you can trigger? How do you stop it?

Document every failure you find and what you did about it.

### Part D — Evaluation

Build an eval suite with at least 10 test questions and known good answers (or known good structure — not every question has one right answer).

**Baseline metrics:**
- Output quality vs single-agent baseline (use a rating scale, not just vibes)
- Latency: total time, time per agent
- Cost: total tokens, cost per request
- Failure rate: how often does the pipeline not complete?
- Reasoning trace quality: does the trace actually explain what happened?

**Hallucination metrics (required):**

Run RAGAS over your eval set. RAGAS measures four dimensions of RAG quality:

| Metric | What it measures |
|--------|-----------------|
| **Faithfulness** | Are the claims in the answer supported by the retrieved context? (This is your NLI score operationalised.) |
| **Answer Relevance** | Does the answer actually address the question asked? |
| **Context Precision** | Are the retrieved chunks relevant to the question? Or is the system pulling in noise? |
| **Context Recall** | Did the retrieval miss important source material that was available? |

```python
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision, context_recall

results = evaluate(
    dataset=your_eval_dataset,
    metrics=[faithfulness, answer_relevancy, context_precision, context_recall]
)
```

Install: `pip install ragas`

**NLI pass rate (required):** What percentage of claims in your final outputs are classified as `entailment` by the Claim Verifier? This is your headline hallucination metric. Report it. A system with 85%+ entailment rate across 10 questions is genuinely trustworthy. Below 70% means the system is producing too many unsupported claims.

**The comparison that matters:** Run the same 10 questions through a single Claude call with no retrieval. Compare RAGAS faithfulness scores. If your multi-agent system with citation grounding and NLI verification doesn't produce a higher faithfulness score than raw Claude, your retrieval and verification pipeline is not adding value — investigate why before declaring it done.

### Part E — Production

- FastAPI wrapper with streaming (user sees output as it generates)
- Cost ceiling enforced server-side
- Request logging (every agent call, latency, token count)
- Basic rate limiting
- A simple frontend (Streamlit is fine) that shows the reasoning trace live

### Part F — Reflection Write-Up

Write 500–1,000 words covering:

1. **What you built:** A plain description of the system, what it can do, what it can't.
2. **What's orchestration vs what's intelligence:** Be specific. Which parts are pattern matching? Which parts produced outputs that genuinely surprised you?
3. **Where it would break at scale:** If 10,000 people used this tomorrow, what fails first?
4. **What you'd build differently if A2A existed:** Assume agents can discover and call each other without your orchestrator. What changes?
5. **What you'd build differently if agents had persistent memory:** Assume each agent remembers its past runs. What changes?
6. **One thing you'd want to research further:** Based on what you saw while building, what research paper would you look for next?

This write-up is the most important artefact in your portfolio. It demonstrates that you understand what you built, not just that you can build it.

---

## Completion Checklist

- [ ] Architecture design documented before coding started
- [ ] Full pipeline runs on 3+ test questions
- [ ] Critic-Analyst debate pattern implemented
- [ ] At least 2 agents run in parallel
- [ ] Hard cost ceiling enforced
- [ ] One agent failure does not kill the pipeline
- [ ] Every factual claim carries an inline citation to a source chunk
- [ ] Claim Verifier Agent implemented using NLI (cross-encoder/nli-deberta-v3-base)
- [ ] Claim Verifier log written per request (claim, source, NLI label, confidence, action)
- [ ] Atomic claim decomposition implemented before NLI pass
- [ ] Cross-worker consistency check implemented
- [ ] RAGAS eval run: faithfulness, answer relevance, context precision, context recall reported
- [ ] NLI pass rate reported across eval set
- [ ] Multi-agent vs single-agent faithfulness comparison done
- [ ] FastAPI service with streaming and request logging
- [ ] Reasoning trace visible to the user
- [ ] Part F reflection write-up complete

---

## What Completing This Demonstrates

- You understand multi-agent architecture, not just multi-agent frameworks
- You can design for failure, not just for the happy path
- You know when multi-agent helps and when it doesn't (the eval forces this)
- You can articulate what current agent systems actually are vs what they're marketed as
- You can deploy a working system, not just a notebook

That combination is rare. Most people who claim to build AI agents are assembling LangChain abstractions without understanding the layer beneath. You've built the layer beneath. This capstone proves it.

---

## Resources

**Multi-agent architecture:**
- [Building effective agents — Anthropic](https://www.anthropic.com/research/building-effective-agents)
- [AutoGen — multi-agent framework paper](https://arxiv.org/abs/2308.08155)
- [Generative Agents (25 agents in a simulated town)](https://arxiv.org/abs/2304.03442)
- [A2A Protocol — Google (2025)](https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/)
- [The actual state of agent reliability — SWE-bench results](https://www.swebench.com/)

**Hallucination reduction and evaluation:**
- [RAGAS — Retrieval-Augmented Generation Assessment](https://arxiv.org/abs/2309.15217) — the eval framework used in Part D
- [DeBERTa — the model behind cross-encoder/nli-deberta-v3-base](https://arxiv.org/abs/2006.03654)
- [FactScore — breaking claims into atomic facts for verification](https://arxiv.org/abs/2305.14251)
- [FEVER — the benchmark that NLI-based fact checking is evaluated on](https://fever.ai/)
- [Self-RAG — an approach where the model itself learns to retrieve and verify](https://arxiv.org/abs/2310.11511)
