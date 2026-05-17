# Curriculum Overview

Ten levels. Each one has a build. You don't move on until the build works and you can explain it.

---

## Level 1 — Foundation

**XP:** 100

How does an AI agent actually work at the lowest level? Tool calling, the agent loop, API structure.

**Build:** A single-file Python calculator agent. User types a maths question, Claude calls a calculator tool, your code runs it, Claude responds.

**Key concepts:** API call structure, tool definitions and token cost, `stop_reason='tool_use'`, the messages list, Claude decides / your code executes.

---

## Level 2 — Making it Real

**XP:** 150

A real agent isn't a one-shot script. It's a loop that keeps running, handles multiple tools, and recovers from errors.

**Build:** Extend the calculator agent into a chat loop with a second tool (unit converter). Wrap it in a Streamlit UI. Add error handling.

**Key concepts:** `while True` input loop, tool dispatch pattern (`tool_map` with `**kwargs`), messages list as memory, error handling that doesn't crash, Streamlit basics.

---

## Level 3 — Reasoning Patterns

**XP:** 200

How do you get an agent to think before it acts? ReAct (Reason + Act) is the most important pattern in agentic AI.

**Build:** A research agent that answers multi-step questions. It must look up two pieces of data, then combine them — figuring out the sequence on its own.

**Key concepts:** ReAct pattern (Thought / Action / Observation), chain-of-thought prompting, multi-step tool call loop, detecting done vs still-working, self-reflection, step counters.

---

## Level 4 — Agent Architecture

**XP:** 250

Complex tasks need planning. Some agents break big tasks into subtasks and delegate them.

**Build:** A report generation agent. Orchestrator breaks any topic into subtasks, sends each to a specialist subagent, assembles the final report.

**Key concepts:** Orchestrator/subagent pattern, task decomposition, passing context between agents, specialist system prompts, when to use multi-agent vs single-agent, cost tradeoffs.

---

## Level 5 — Memory and State

**XP:** 300

Without memory, every conversation starts from zero. Memory is what makes an agent feel intelligent over time.

**Build:** A personal assistant with three tiers of memory — in-conversation (messages list), session (JSON file), and semantic search over past conversations (vector store).

**Key concepts:** Short-term vs long-term memory, vector embeddings, cosine similarity, RAG pipeline, what to save vs what to forget, memory as a privacy concern.

---

## Level 6 — MCP and Tool Ecosystems

**XP:** 300

Why define every tool manually? MCP (Model Context Protocol) is Anthropic's open standard for connecting agents to tools dynamically.

**Build:** Convert the calculator agent to MCP. Build an MCP server exposing your tools. Compare token cost and complexity vs Level 1.

**Key concepts:** Why MCP exists, what an MCP server is, how Claude discovers tools from it, `tools=[]` vs MCP connection, token cost at scale, open standard benefits.

---

## Level 7 — Multi-Agent Systems

**XP:** 400

One agent has limits. Multiple specialised agents working in parallel can do far more.

**Build:** A competitive analysis agent. Supervisor spawns three parallel subagents (products, competitors, pricing) using asyncio. Synthesises results into a report.

**Key concepts:** asyncio for parallel execution, agents communicating results back to supervisor, handling one subagent failing, parallelism vs cost, when NOT to use multi-agent.

---

## Level 8 — Evaluation and Reliability

**XP:** 350

How do you know your agent is actually working correctly? You need evals — automated tests that measure agent behaviour.

**Build:** An eval suite for the calculator agent. 20 test cases. Measure accuracy, tool call reliability, latency, token cost. Add a hallucination guardrail.

**Key concepts:** What evals are and why they matter more than intuition, measuring tool call reliability, observability and logging, hallucination detection, running evals before every change.

---

## Level 9 — Production Agents

**XP:** 400

Building something that works locally is different from building something 1,000 people use.

**Build:** Productionise the Level 2 agent. Add streaming, cost tracking, prompt caching, rate limit handling with exponential backoff, and a FastAPI wrapper.

**Key concepts:** Streaming with the Anthropic SDK, exponential backoff, prompt caching and cost reduction, API wrapper design, real cost of running agents at scale.

---

## Level 10 — Advanced Patterns

**XP:** 500

The hardest problems in agentic AI — trust, long-running tasks, and working safely in the real world.

**Build:** A long-running research agent with human-in-the-loop. Checkpoints progress to disk. Pauses before irreversible actions. Resumes from the last checkpoint after a crash.

**Key concepts:** Human-in-the-loop as a safety requirement, checkpointing, sync vs async agent design, designing for failure, when to require approval vs allow full autonomy.

---

## How the Levels Connect

```
Level 1   one tool, one shot
Level 2   many tools, chat loop
Level 3   multi-step reasoning
Level 4   planning and delegation
Level 5   memory across sessions
Level 6   dynamic tool discovery (MCP)
Level 7   parallel agents
Level 8   knowing it works (evals)
Level 9   running in the real world
Level 10  trust, safety, and resilience
```

The calculator agent from Level 1 is still inside the Level 10 agent — it just has ten layers of thinking and infrastructure around it.
