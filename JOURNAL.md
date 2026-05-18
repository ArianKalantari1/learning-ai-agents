# Learning Journal

One entry per level completed. Write it before moving on.

Focus on: what you built, what finally clicked, what took longest, a bug you hit.

---

## Entry Template

```
## Level X — [Name]
Date: YYYY-MM-DD
XP earned: XXX

What I built:
[One paragraph]

What clicked:
[The mental model that finally made sense]

What confused me:
[The thing that took longest to understand — be specific]

A bug I hit:
[What the bug was, why it happened, how I fixed it]

What I would do differently:
[If you started this level again tomorrow]
```

---

*(Entries go below as you complete each level)*

## Level 1 — Foundation
Date: 2026-05-18
XP earned: 100

What I built:
A single-file Python calculator agent. The user types a maths question in natural language, Claude decides to call a calculator tool, my code runs the calculation, and Claude wraps the result back into a natural reply. Two API calls, one tool, one Python file.

What clicked:
The difference between the JSON tool definition and the Python function. The JSON definition is the advertisement — it tells Claude what the tool is called, what it does, and what inputs it expects. The Python function is the actual implementation that runs on my machine. Claude only ever sees the JSON; it never sees or runs my code. That separation is not just architectural — it is also a security boundary. My actual business logic, API keys, and proprietary code stay local. I only share a description of what the tool can do, not how it does it.

The second thing that clicked was why there are two API calls. The first call lets Claude reason about what tool is needed and produce a tool_use block. My code then runs the tool. The second call gives Claude the result so it can translate it back into natural language. Claude has to pause in the middle because it cannot execute anything itself — it can only request and interpret.

What confused me:
Question five — why Claude does not run tools itself. My first instinct was about configuration, like tools just need to be defined first. But the real answer is more fundamental: Claude is a language model that returns text. A tool_use block is just structured text saying "please run this with these inputs." Claude has no ability to execute code, make system calls, or touch a filesystem. It is purely a reasoning and language layer. My Python script is the executor. Once that clicked, the whole architecture made sense — Claude decides, my code acts.

A bug I hit:
Nothing broke at the code level, but the mental model broke first. I initially thought the agent loop was one continuous process inside Claude. It is not. The loop lives in my code. I write the append logic, I make the second API call, I decide what to do with the result. Claude is stateless between calls.

What I would do differently:
Think about tokens earlier. Every tool definition is injected into every API call, which means adding lots of tools gets expensive fast. I passed one small tool here so it was invisible, but I can already see why MCP exists — to avoid bundling every tool definition into every message. Next time I would count tokens from the start and think about what really needs to be in context.
