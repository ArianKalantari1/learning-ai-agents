# Level 10 — Advanced Patterns

**Status:** Locked  
**XP:** 500  
**Unlocks:** Human-in-the-loop, checkpointing, safety design  
**Requires:** Level 9 complete

---

## What You'll Build

A long-running research agent with human-in-the-loop. The user asks a big research question. The agent:
- Works in the background, checkpointing its progress to disk every few steps
- Pauses before any action marked as "irreversible" (saving a file, sending a message) and asks for human confirmation
- Resumes from the last checkpoint if it crashes

---

## Key Concepts

- Why human-in-the-loop is a safety requirement, not just a nice-to-have
- What checkpointing is — serialising agent state to disk so it can resume after failure
- The difference between synchronous and asynchronous agent design
- How to classify actions as reversible vs irreversible
- When to give an agent full autonomy vs always require approval
- Designing for failure — what happens when a tool call times out?

---

## Why This Level Matters

The Air Canada chatbot case (2024): an AI agent gave a customer incorrect refund policy information. Court ruled Air Canada liable. The lesson: agents that can commit to anything on behalf of a user or organisation need human approval gates for consequential decisions.

The general failure pattern across early agent deployments:
1. Too much autonomy too early
2. No cost or step limits
3. Irreversible actions without human approval
4. Safety as an afterthought rather than core architecture

Level 10 is about baking the right constraints in from the start.

---

## Completion Checklist

1. What is a checkpoint and what does it contain?
2. How do you classify an action as reversible vs irreversible?
3. What does the human-in-the-loop approval flow look like in code?
4. How do you resume from a checkpoint after a crash?
5. What is the difference between a step counter (Level 3) and a full checkpoint system?
6. When is it appropriate to give an agent full autonomy without approval gates?

---

## Resources

- [Anthropic responsible scaling policy](https://www.anthropic.com/research/responsible-scaling-policy)
- [Building effective agents — Anthropic](https://www.anthropic.com/research/building-effective-agents)

---

## Your Build

Add your code to the `builds/` folder.

---

## Congratulations

If you've reached this point with working builds and answered every completion checklist: update your XP to 3,150 in [README.md](../../README.md), log the date in [ACHIEVEMENTS.md](../../ACHIEVEMENTS.md), write a final journal entry in [JOURNAL.md](../../JOURNAL.md).

Then start the AWS track, or find a real project to apply this to.
