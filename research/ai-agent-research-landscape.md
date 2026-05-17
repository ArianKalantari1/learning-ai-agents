# The AI Agent Research Landscape
## What's Solved, What's Being Worked On, What's Unsolved

> Reading material for the train.
> Balanced depth — concepts explained clearly with real technical grounding.
> No build project attached. This is pure understanding.

---

## Why This Matters for You as a Builder

Most tutorials teach you how to use today's tools. This material teaches you why those tools exist, what their limits are, and where the field is heading — so when new research drops, you understand it immediately rather than starting from scratch.

Every section follows the same structure:
- **What it is** — the concept explained clearly
- **What's solved** — what you can use today with confidence
- **What's being worked on** — active research, partial solutions
- **What's unsolved** — genuine open problems
- **Why it matters for agents** — direct connection to what you're building

---

# Part 1 — Continual Learning and Self-Improvement

## What it is

Continual learning is the ability of an AI system to learn from new experiences over time without forgetting what it already knows. In humans this is natural — you learn a new skill without forgetting how to walk. In neural networks it's surprisingly hard.

Current LLMs like Claude are trained once on a massive dataset, then frozen. Their weights — the numerical parameters that encode everything they know — don't change during deployment. Every conversation starts from the same base model.

The gap between "frozen model" and "model that genuinely improves from experience" is one of the central challenges in AI research right now.

---

## What's Solved

**In-context learning** is fully solved and production-ready.

By passing examples, instructions, and past context in the messages list, you can make an agent behave as if it's learned from experience — without changing any weights. This is what you're building in this curriculum.

```
Frozen model + rich context = agent that appears to learn
```

It's not true learning — the model weights didn't change — but for most practical applications it's good enough and it's available today.

**Fine-tuning** is also well understood. You take a pre-trained model and continue training it on your specific dataset. Anthropic, OpenAI, and Google all offer fine-tuning APIs. The result is a model with baked-in knowledge of your domain.

Use cases where fine-tuning works well:
- Domain-specific language (medical, legal, financial terminology)
- Consistent output formatting
- Brand voice and tone
- Specialised reasoning patterns

**Retrieval Augmented Generation (RAG)** — covered in depth in Part 2 — is the practical workaround for giving agents access to new information without retraining. Solved and widely deployed.

---

## What's Being Worked On

**Catastrophic forgetting** is the central problem in continual learning. When you fine-tune a model on new data, it tends to overwrite old knowledge. The model gets better at the new task and worse at everything else.

Several approaches are being actively researched:

**Elastic Weight Consolidation (EWC)** — identifies which weights are most important for old tasks and penalises changing them when learning new ones. Like telling a student "don't forget your maths while you're learning history."

**Progressive Neural Networks** — instead of updating existing weights, add new network columns for new tasks while keeping old ones frozen. Old knowledge is structurally protected. Used in Google DeepMind's research.

**Experience Replay** — while learning new things, periodically replay examples from old tasks to prevent forgetting. Biologically inspired — humans consolidate memories during sleep through a similar mechanism.

**Parameter-Efficient Fine-Tuning (PEFT)** — instead of updating all model weights, update only a small set of additional parameters (called adapters or LoRA layers) while keeping the base model frozen. Dramatically reduces catastrophic forgetting and compute cost. Currently the most practical approach for production systems.

LoRA (Low-Rank Adaptation) is the most widely used PEFT method right now. Anthropic, OpenAI, and open-source projects like Hugging Face all support it.

**Curriculum learning** — training on tasks in a specific order, from simple to complex, the way good teachers structure lessons. Reduces forgetting and improves generalisation. Active research area.

---

## What's Unsolved

**True online learning** — updating model weights in real time during deployment, from every conversation, without degrading performance. This would mean Claude genuinely learns from talking to you. Currently impossible at production scale without catastrophic forgetting.

**Knowing what to learn vs what to ignore** — humans are selective about what they commit to long-term memory. Current models either learn everything (catastrophic forgetting) or nothing (frozen weights). The middle ground — selectively updating based on importance — is an open problem.

**Verifying that learning was correct** — if a model updates its beliefs based on new information, how do you verify the update was accurate and didn't introduce errors or biases? No good solution exists.

**Self-directed learning** — agents that identify their own knowledge gaps and seek out information to fill them, the way a curious person would. Some early research exists but it's far from reliable.

---

## Why It Matters for Your Agent Work

Right now an agent's "learning" is:
- In-context: what you pass in the messages list each session
- RAG-based: what it retrieves from the knowledge base you curate

The practical path to an agent that genuinely improves:
1. Log every decision and outcome (you control this)
2. Curate the logs into structured lessons (you control this)
3. Periodically fine-tune on your curated data (possible today via API)
4. Use PEFT/LoRA to update specific behaviours without forgetting general capability (possible today with open-source models)

That's buildable with current tools. The research frontier is about making it cheaper, more reliable, and more autonomous.

---

# Part 2 — Memory and RAG Advances

## What it is

Memory in AI agents is the mechanism for persisting and retrieving information across sessions. Without it every conversation starts blank.

RAG (Retrieval Augmented Generation) is the dominant approach: store information in a vector database, convert queries to embeddings, find semantically similar stored content, inject it into the context window.

```
User asks: "What did we decide about the Melbourne expansion?"
     ↓
Query embedded → vector search → retrieve relevant past decisions
     ↓
Inject retrieved context into Claude's prompt
     ↓
Claude answers with knowledge of past decisions
```

This is what you'll build at Level 5 of the curriculum.

---

## What's Solved

**Basic RAG** is production-ready and widely deployed. The core pipeline:

1. **Chunking** — split documents into pieces (paragraphs, sentences, fixed token sizes)
2. **Embedding** — convert each chunk to a vector using an embedding model
3. **Storage** — store vectors in a vector database (ChromaDB, Pinecone, Weaviate, pgvector)
4. **Retrieval** — at query time, embed the query and find nearest vectors by cosine similarity
5. **Injection** — add retrieved chunks to the context window before the LLM call

Tools for this are mature: LangChain, LlamaIndex, and direct SDK implementations all work reliably.

**Semantic search** — finding content by meaning rather than exact keywords — is solved. Embedding models from OpenAI, Anthropic, and Cohere are excellent.

**Hybrid search** — combining semantic search with traditional keyword search (BM25) — is well understood and often outperforms either alone. Used in production at most major AI companies.

---

## What's Being Worked On

**Contextual retrieval** — Anthropic published this in late 2024. Standard RAG loses context when chunks are split from their source documents. A chunk that says "the revenue increased by 23%" is meaningless without knowing what company and what period.

Contextual retrieval adds a summary of the source document to each chunk before embedding:

```
Standard chunk:    "The revenue increased by 23%"
Contextual chunk:  "From Q3 2024 Acme Corp earnings report: 
                    The revenue increased by 23%"
```

Retrieval accuracy improves dramatically. This is production-ready today.

**Multi-vector retrieval** — instead of one embedding per chunk, generate multiple embeddings representing different aspects (summary, keywords, hypothetical questions this chunk answers). Retrieve using any of them. Better coverage, fewer missed relevant chunks.

**Graph RAG** — Microsoft Research published this in 2024. Instead of treating documents as isolated chunks, build a knowledge graph of entities and relationships first. Retrieval traverses the graph rather than doing flat vector search.

```
Standard RAG:   "find chunks similar to this query"
Graph RAG:      "find the entity → traverse its relationships → 
                 retrieve connected context"
```

Dramatically better for complex multi-hop questions. Still maturing but promising.

**Agentic RAG** — instead of one retrieval step, the agent iteratively retrieves, reasons about whether it has enough information, and retrieves again if needed. Treats retrieval as a tool the agent calls in a loop.

**Memory hierarchies** — modelling agent memory after human memory:
- Working memory: current context window
- Episodic memory: specific past events and conversations
- Semantic memory: general facts and knowledge
- Procedural memory: how to do things (workflows, patterns)

Each tier has different storage, retrieval, and decay characteristics. MemGPT (now Letta) pioneered this approach.

---

## What's Unsolved

**Memory contradiction resolution** — when new information conflicts with stored memory, which wins? How do you update stored beliefs without corrupting the whole knowledge base? No clean solution.

**Memory decay and forgetting** — not all memories should last forever. How do you decide what to keep, what to summarise, and what to delete? Human memory decays naturally based on recency and importance. Implementing this reliably in agent systems is unsolved.

**Cross-agent shared memory** — in a multi-agent system, how do multiple agents share a consistent memory without conflicts? If two agents update the same memory simultaneously, which update wins? Distributed systems research applies here but no agent-specific solution exists.

**Episodic memory that generalises** — humans can take a specific past experience and generalise it into a principle. Current RAG retrieves specific chunks but doesn't generalise across them automatically.

---

## Memory Architecture for Production Agents

```
Working memory      → current conversation context window
Episodic memory     → RAG over past decisions, meetings, conversations  
Semantic memory     → company knowledge base, policies, org chart
Procedural memory   → workflow templates, decision frameworks
```

Each tier uses different technology:
- Working memory: the messages list (Level 1)
- Episodic + Semantic: ChromaDB or Pinecone (Level 5)
- Procedural: structured JSON/markdown in system prompt (Level 4)

---

# Part 3 — Multi-Agent Coordination and Communication

## What it is

Multi-agent systems are networks of AI agents that communicate, coordinate, and collaborate to complete tasks too complex for a single agent.

The core challenge: agents are fundamentally isolated. Each one has its own context window, its own state, its own goals. Making them work together reliably requires solving coordination, communication, and trust problems that don't exist in single-agent systems.

---

## What's Solved

**Sequential orchestration** — one agent delegates to another, waits for the result, continues. This is what you build at Level 4. Reliable, well-understood, production-ready.

**Parallel execution with asyncio** — running multiple independent subagents concurrently. Well-understood Python engineering. Level 7 of the curriculum.

**Role-based agent design** — giving each agent a specific system prompt, tools, and responsibilities. The specialist vs generalist pattern. Widely used in production (CrewAI, AutoGen, LangGraph all built on this).

**Tool standardisation via MCP** — Anthropic's Model Context Protocol. Agents discover and connect to tools via a standard interface. Production-ready. Level 6 of the curriculum.

---

## What's Being Worked On

**Agent communication protocols** — right now agents communicate by passing text through an orchestrator. There's no standard for how agents negotiate, request help, or share partial results. Several proposals exist:

- **Agent Protocol** (open source) — a standard REST API for agent communication
- **MCP extensions** — Anthropic is working on extending MCP beyond tools to agent-to-agent communication
- **A2A (Agent-to-Agent)** — Google's proposed protocol for agents to discover and communicate with each other across systems. Announced 2025.

None of these are fully standardised yet. The industry is in the competing-protocols phase that precedes standardisation.

**Emergent coordination** — instead of hardcoded orchestration, agents that negotiate and self-organise around tasks. Research from Stanford, MIT, and DeepMind shows promising results in controlled settings. Not production-ready.

**Agent debate and verification** — one agent produces an answer, another critiques it, a third adjudicates. Improves accuracy on complex reasoning tasks. Partially production-ready.

---

## What's Unsolved

**Deadlock prevention** — in complex multi-agent systems, agents can end up waiting for each other in a cycle (A waits for B, B waits for C, C waits for A). Detecting and preventing deadlocks in dynamic agent networks is an open problem.

**Fault tolerance** — if one agent in a network fails, how do the others recover? No standard approach.

**Agent trust** — in an open agent marketplace, how does an orchestrator know that a subagent is trustworthy? A malicious subagent could return false results, exfiltrate data, or manipulate the orchestrator. Cryptographic approaches exist in theory but aren't deployed at scale.

**Collective intelligence** — can a network of mediocre agents produce results better than one excellent agent? Sometimes yes, sometimes no. No reliable framework for predicting when multi-agent adds value vs just adding cost and complexity.

---

# Part 4 — Real-World Applications and Case Studies

## What's Actually Deployed Today

### Software Engineering
- **GitHub Copilot Workspace** — takes a GitHub issue and generates a full plan, code changes, and tests
- **Devin (Cognition AI)** — autonomous software engineer; plans, codes, runs tests, debugs, and iterates
- **Claude Code (Anthropic)** — agentic coding in the terminal
- **Cursor** — AI code editor with MCP integration

### Research and Knowledge Work
- **Perplexity** — multi-step research agent; searches, reads, synthesises, cites
- **NotebookLM (Google)** — RAG over your personal documents
- **Elicit** — AI research assistant for academic literature

### Business Operations
- **Salesforce Agentforce** — CRM agents handling customer inquiries and lead qualification
- **ServiceNow AI Agents** — IT support agents that diagnose issues and run remediation scripts
- **Harvey** — AI agent for legal work; reviews contracts, identifies risks, drafts responses

---

## What the Failures Teach Us

**Air Canada chatbot (2024)** — gave a customer incorrect refund policy information. Court ruled Air Canada liable. Lesson: agents need guardrails for factual claims about policies.

**Early AutoGPT deployments** — users gave agents too much autonomy too early. Agents ran up large API bills, made irreversible decisions, got stuck in loops. Lesson: always add step counters, cost limits, and approval gates for irreversible actions.

**Bing Chat early release (2023)** — without proper guardrails, the agent could be manipulated into producing harmful outputs. Lesson: safety constraints need to be baked into the architecture, not bolted on afterward.

The general pattern across failures:
1. Too much autonomy too early
2. No cost or step limits
3. Irreversible actions without human approval
4. Guardrails treated as optional rather than required

This is exactly why Level 10 covers human-in-the-loop and safety as core architecture, not afterthoughts.

---

## The Honest Summary

**Solved:**
- Basic tool calling and agent loops
- RAG and semantic memory
- Sequential and parallel multi-agent
- Fine-tuning and PEFT
- Production deployment at scale

**Being Worked On:**
- Continual learning without forgetting
- Better memory (contextual RAG, graph RAG)
- Agent communication standards (MCP, A2A)
- Self-improving workflows
- Long-horizon task execution

**Unsolved:**
- True online learning from experience
- Cross-agent shared memory without conflicts
- Agent trust and verification at scale
- Collective intelligence — when does it actually help?
- Privacy in open agent marketplaces
- Alignment of complex agent networks

The gap between solved and unsolved is where careers are made right now.

Everything in the solved column is what this curriculum teaches you to build. Everything in being-worked-on is what you'll read about in research papers over the next 12 months. Everything in unsolved is where the PhDs are being written — and where the next generation of products will come from.
