# Level 7 — Multi-Agent Systems

**Status:** Locked  
**XP:** 400  
**Unlocks:** asyncio, parallel agent execution  
**Requires:** Level 6 complete

---

## What You'll Build

A competitive analysis agent. The user inputs a company name. A supervisor agent spawns three parallel subagents:
1. One researches the company's products
2. One researches their competitors
3. One analyses their pricing

All three run concurrently using `asyncio`. The supervisor synthesises the results into a final report.

---

## Key Concepts

- How `asyncio` enables parallel agent execution
- Why parallelism matters: 4 agents × 10 seconds sequential = 40 seconds, parallel = ~10 seconds
- How agents communicate results back to a supervisor
- How to handle one subagent failing while others succeed
- The cost tradeoff: parallel agents are faster but the same total token cost
- When NOT to use multi-agent (most simple tasks don't need it)

---

## Key Code Pattern

```python
import asyncio

async def run_parallel_agents(tasks):
    results = await asyncio.gather(*[
        call_subagent_async(task["content"], task["system"], task["tools"])
        for task in tasks
    ])
    return results
```

The Anthropic SDK is synchronous by default — you run it in a thread pool executor to make it work with asyncio.

---

## Completion Checklist

1. What is `asyncio.gather()` and why do you use it for parallel agents?
2. Why is the Anthropic SDK run in a thread pool executor rather than called directly with `await`?
3. How do you handle a subagent that raises an exception without killing the whole pipeline?
4. What is the difference between parallelism (Level 7) and just having multiple agents (Level 4)?
5. When does multi-agent parallelism NOT help?
6. How do you track cost when running agents in parallel?

---

## Resources

- [Python asyncio docs](https://docs.python.org/3/library/asyncio.html)
- [Building effective agents — Anthropic](https://www.anthropic.com/research/building-effective-agents)
- [AutoGen — multi-agent framework](https://arxiv.org/abs/2308.08155)

---

## Your Build

Add your code to the `builds/` folder.

---

## Next

[Level 8 — Evaluation](../level-08-evaluation/)
