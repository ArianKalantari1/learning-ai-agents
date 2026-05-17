# Level 4 — Agent Architecture

**Status:** Locked  
**XP:** 250  
**Unlocks:** Orchestration, task decomposition, subagents  
**Requires:** Level 3 complete

---

## What You'll Build

A report generation agent. The user gives a topic — climate change, electric vehicles, the housing crisis — and the orchestrator:
1. Asks Claude to decompose the topic into 4 subtasks dynamically
2. Sends each subtask to a specialist subagent with its own system prompt
3. Assembles the outputs into a formatted report
4. Returns it via the Streamlit UI from Level 2

---

## Key Concepts

- The orchestrator/subagent pattern — the most important architecture in agentic AI
- How to make an orchestrator that plans dynamically (not hardcoded subtasks)
- How to pass outputs from one agent into the next
- Why specialist system prompts produce better outputs than one generic prompt
- When to use multi-agent vs single-agent
- The cost tradeoff: more agents = more API calls

---

## Study Material

Read [study-material.md](study-material.md) before building.

---

## Completion Checklist

1. What is the difference between an orchestrator and a subagent?
2. Why do specialist system prompts produce better results than one generic prompt?
3. How do you pass context from one subagent to another?
4. When should you use multi-agent vs single-agent?
5. Why does multi-agent cost more tokens, and when is that cost justified?
6. How does task decomposition quality affect the final output?

---

## Resources

- [Building effective agents — Anthropic](https://www.anthropic.com/research/building-effective-agents) — read the orchestrator/subagent section twice
- [LLM-powered autonomous agents — Lilian Weng](https://lilianweng.github.io/posts/2023-06-23-agent/) — read the planning section
- [ReAct paper](https://arxiv.org/abs/2210.03629) — revisit the multi-agent examples in section 3

---

## Your Build

Add your code to the `builds/` folder.

---

## Next

[Level 5 — Memory and State](../level-05-memory-and-state/)
