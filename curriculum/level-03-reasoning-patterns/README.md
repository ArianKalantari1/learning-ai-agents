# Level 3 — Reasoning Patterns

**Status:** Locked  
**XP:** 200  
**Unlocks:** ReAct reasoning, chain of thought, multi-step loops  
**Requires:** Level 2 complete

---

## What You'll Build

A research agent that answers multi-step questions. Example: "What is the population of Sydney divided by the population of Melbourne?" The agent must look up Sydney's population, look up Melbourne's population, then divide them — figuring out that sequence entirely on its own.

Add a `web_search` mock tool and a `calculator` tool. The agent reasons step by step before each action.

---

## Key Concepts

- What ReAct means: the agent writes its reasoning before calling a tool
- How chain-of-thought prompting changes agent behaviour
- What a multi-step tool call loop looks like in code
- How to detect when the agent is done vs still working
- Why self-reflection matters
- Why you always need a step counter

---

## Study Material

Read [study-material.md](study-material.md) before building. This level introduces the most important pattern in agentic AI.

---

## Completion Checklist

1. What does ReAct stand for and what problem does it solve?
2. Why does writing out reasoning before acting produce better results?
3. What does the messages list look like after three tool calls?
4. Why do you always need a step counter in a multi-step agent loop?
5. What is self-reflection and when would you use it?
6. What is the difference between the chat loop (Level 2) and the reasoning loop (Level 3)?

---

## Resources

- [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629)
- [Anthropic agents overview](https://docs.anthropic.com/en/docs/agents)
- [Chain of thought prompting — Wei et al.](https://arxiv.org/abs/2201.11903)

---

## Your Build

Add your code to the `builds/` folder.

---

## Next

[Level 4 — Agent Architecture](../level-04-agent-architecture/)
