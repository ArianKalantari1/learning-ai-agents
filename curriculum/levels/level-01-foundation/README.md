# Level 1 — Foundation

**Status:** In Progress  
**XP:** 100  
**Unlocks:** Tool calling, the agent loop

---

## What You'll Build

A single-file Python calculator agent. The user types a maths question in natural language. Claude decides to call a calculator tool. Your code runs the calculation and sends the result back. Claude responds naturally.

---

## Key Concepts

- What an API call looks like
- What tool definitions are and why they cost tokens
- What `stop_reason='tool_use'` means
- Why the messages list grows with each turn
- The difference between Claude deciding and your code executing

---

## Study Material

Read [study-material.md](study-material.md) before building. It covers the full mental model for tool calling, the agent loop, and the messages list.

---

## Completion Checklist

Answer all six before marking this level complete:

1. Why does the agent make two API calls instead of one?
2. What does `stop_reason='tool_use'` mean and what do you do when you see it?
3. Why does the messages list grow with every turn?
4. What is the difference between the tool JSON definition and the Python function?
5. Why does Claude not run tools itself?
6. What happens to tokens when you add tool definitions?

---

## Resources

- [Anthropic tool use docs](https://docs.anthropic.com/en/docs/build-with-claude/tool-use)
- [Anthropic Python SDK](https://github.com/anthropic-sdk/anthropic-sdk-python)
- [Building effective agents — Anthropic](https://www.anthropic.com/research/building-effective-agents)

---

## Your Build

Add your code to the `builds/` folder. Note any bugs you hit and how you fixed them here.

---

## Next

Once you've answered all six questions and your build works: write a reflection in [JOURNAL.md](../../JOURNAL.md), update your XP in [README.md](../../README.md), then move to [Level 2](../level-02-making-it-real/).
