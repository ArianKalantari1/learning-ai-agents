# Level 3 — Reasoning Patterns
## Study Material: ReAct, Chain of Thought, and Multi-Step Agents

> Read this before or alongside the hands-on build.
> Goal: understand how agents think before they act — and why that makes them dramatically more reliable.

---

## What Changes at Level 3?

Level 1 and 2 were single-step agents. User asks a question, Claude calls one tool, done.

Level 3 is about **multi-step reasoning**. Some questions can't be answered with one tool call. They require a sequence of actions where each step informs the next.

Example:
> "What is the population of Sydney divided by the population of Melbourne?"

A single tool call can't answer this. You need to:
1. Look up Sydney's population
2. Look up Melbourne's population
3. Divide them

And Claude needs to figure out that sequence **on its own**, without you hardcoding it.

This is where agents start feeling genuinely intelligent.

---

## What is ReAct?

ReAct stands for **Reason + Act**. It's the most important reasoning pattern in agentic AI.

Published in a 2022 research paper, it's a simple but powerful idea:

> Before taking any action, the agent writes out its reasoning. Then it acts. Then it observes the result. Then it reasons again. Then it acts again.

The cycle looks like this:

```
Thought:  "I need to find Sydney's population first."
Action:   web_search("Sydney population 2024")
Observation: "Sydney population is 5.3 million"

Thought:  "Now I need Melbourne's population."
Action:   web_search("Melbourne population 2024")
Observation: "Melbourne population is 5.1 million"

Thought:  "Now I can divide: 5.3 / 5.1 = 1.039"
Action:   calculator("5.3 / 5.1")
Observation: "1.0392156..."

Thought:  "I have everything I need to answer the question."
Answer:   "Sydney's population is about 1.04x Melbourne's population."
```

Each Thought → Action → Observation cycle is one loop iteration. The agent keeps looping until it decides it has enough information to answer.

---

## Why Does Reasoning Before Acting Matter?

Without explicit reasoning, Claude jumps straight to actions. Sometimes it picks the wrong tool, skips a step, or answers from its own knowledge instead of using tools.

With reasoning, Claude is forced to:
- Plan the steps before executing them
- Check whether each step actually answered what it needed
- Catch its own mistakes before they compound

**The analogy:** Imagine asking someone to solve a maths problem. If they just blurt out the answer, they might get it wrong. If they write out each step, they catch errors along the way. ReAct is Claude writing out its working.

---

## Chain of Thought Prompting

ReAct is built on an older technique called **chain of thought prompting**.

The idea: if you ask Claude to think step by step, it produces better, more accurate answers than if you just ask for the answer directly.

**Without chain of thought:**
```
User:   "What is 15% of 840?"
Claude: "126"  ← sometimes wrong
```

**With chain of thought:**
```
User:   "What is 15% of 840? Think step by step."
Claude: "15% means 15/100. So I need 840 × 0.15.
         840 × 0.1 = 84
         840 × 0.05 = 42
         84 + 42 = 126.
         The answer is 126." ← consistently correct
```

The reasoning tokens aren't wasted — they actually change the computation Claude does to reach the answer. This was one of the most surprising discoveries in LLM research.

In ReAct, you make chain of thought explicit by giving Claude a format to follow: Thought, Action, Observation.

---

## How You Implement ReAct in Code

You don't need a special library. ReAct is implemented through two things:

**1. A system prompt that tells Claude to reason before acting:**

```python
system = """You are a research agent. 

Before every action, write your reasoning using this format:
Thought: [your reasoning about what to do next]
Action: [the tool you will call]

After receiving a tool result, write:
Observation: [what you learned from the result]

Keep reasoning and acting until you have enough information to answer.
When you're done, write:
Answer: [your final response to the user]"""
```

**2. A loop that keeps running until Claude says it's done:**

```python
while True:
    response = client.messages.create(
        model="claude-opus-4-5",
        system=system,
        tools=tools,
        messages=messages
    )
    
    if response.stop_reason == 'end_turn':
        print(response.content[0].text)
        break
    
    if response.stop_reason == 'tool_use':
        tool_use = next(b for b in response.content if b.type == 'tool_use')
        result = tool_map[tool_use.name](**tool_use.input)
        
        messages.append({"role": "assistant", "content": response.content})
        messages.append({"role": "user", "content": [
            {"type": "tool_result", "tool_use_id": tool_use.id, "content": result}
        ]})
        # loop again — Claude will reason about the result and decide next step
```

The loop is the same as Level 2. The difference is Claude now **reasons between steps** rather than jumping straight to tool calls.

---

## How to Detect When the Agent is Done

There are three ways an agent can "be done":

**1. Claude says end_turn with a final answer.**
The clean case. Claude reasoned through everything, got the answer, stopped naturally.

**2. Claude calls a tool that produces the final answer.**
Sometimes the last step is a tool call (e.g. a final calculation). After sending the result back, Claude's next response will be `end_turn` with the answer.

**3. Claude gets stuck in a loop.**
This happens. Claude calls a tool, gets a result, calls the same tool again with slightly different input, gets stuck. You need a safety counter:

```python
max_steps = 10
steps = 0

while steps < max_steps:
    steps += 1
    response = client.messages.create(...)
    
    if response.stop_reason == 'end_turn':
        break
    
    # handle tool use...

if steps >= max_steps:
    print("Agent hit maximum steps — stopping.")
```

Always add a step counter. Infinite loops mean infinite API costs.

---

## Self-Reflection

A powerful extension of ReAct is asking Claude to **reflect on its own answer** before returning it.

After Claude produces a final answer, you make one more API call:

```python
reflection_prompt = f"""
The agent produced this answer: {final_answer}

Original question: {user_question}

Does this answer actually address the question? 
Is anything missing or incorrect?
If yes, continue reasoning. If the answer is complete and correct, confirm it.
"""
```

This catches a common failure mode: Claude answers a slightly different question than the one asked. Self-reflection forces it to check before committing.

It costs one extra API call. For important questions, it's worth it.

---

## What the Messages List Looks Like in a Multi-Step Agent

After three tool calls, the messages list looks like this:

```
[
  {role: "user",      content: "What is Sydney's pop divided by Melbourne's?"},

  {role: "assistant", content: [
      TextBlock("Thought: I need Sydney's population first."),
      ToolUseBlock(name="web_search", input={"query": "Sydney population"})
  ]},

  {role: "user",      content: [
      {type: "tool_result", content: "Sydney population is 5.3 million"}
  ]},

  {role: "assistant", content: [
      TextBlock("Observation: Sydney is 5.3M. Now I need Melbourne."),
      ToolUseBlock(name="web_search", input={"query": "Melbourne population"})
  ]},

  {role: "user",      content: [
      {type: "tool_result", content: "Melbourne population is 5.1 million"}
  ]},

  {role: "assistant", content: [
      TextBlock("Observation: Melbourne is 5.1M. Now I can divide."),
      ToolUseBlock(name="calculator", input={"expression": "5.3 / 5.1"})
  ]},

  {role: "user",      content: [
      {type: "tool_result", content: "1.0392156862745098"}
  ]},

  {role: "assistant", content: [
      TextBlock("Answer: Sydney's population is about 1.04x Melbourne's.")
  ]}
]
```

Notice how each step builds on the last. The messages list is now the agent's **working memory** — a complete record of its reasoning process.

Also notice the token cost. This conversation is now quite long. This is why Level 5 (memory management) and Level 9 (caching) matter.

---

## The Difference Between Levels 1, 2, and 3

| | Level 1 | Level 2 | Level 3 |
|---|---------|---------|----------|
| Steps per question | 1 | 1-2 | Many |
| Tools | 1 | 2 | 2+ |
| Reasoning | None | None | Explicit (ReAct) |
| Loop | No | Chat loop | Reasoning loop inside chat loop |
| Agent decides sequence? | No | No | Yes |

Level 3 is the first time Claude is genuinely **planning**. It decides what to do next based on what it just learned. That's what makes it an agent rather than an autocomplete.

---

## Common Mistakes at Level 3

**Not adding a step counter.**
Without it, a stuck agent runs forever and burns through your API credits. Always add `max_steps`.

**Making the system prompt too vague.**
If you don't explicitly tell Claude to reason before acting, it often skips the reasoning and jumps straight to tool calls. The Thought/Action/Observation format needs to be in the system prompt.

**Expecting Claude to always get the sequence right.**
Sometimes Claude tries to use the calculator before it has the numbers. This is a failure mode to observe and debug. Fix it by making the system prompt clearer about the required sequence.

---

## Why This Level Matters More Than Any Other

Every advanced agent pattern — planning, orchestration, multi-agent systems — is built on ReAct.

When you see an agent that:
- Breaks a complex task into steps
- Delegates to subagents
- Checks its own work
- Recovers from errors

...it's doing ReAct at multiple levels. Understanding the simple version deeply here means every advanced pattern later will make immediate sense.

---

## Sources to Read

- [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629) — the original paper. Read the abstract and the examples.
- [Anthropic agents overview](https://docs.anthropic.com/en/docs/agents)
- [Chain of thought prompting — Wei et al.](https://arxiv.org/abs/2201.11903) — abstract and Figure 1 are enough.

---

## What You Should Be Able to Explain After Level 3

1. What does ReAct stand for and what problem does it solve?
2. Why does writing out reasoning before acting produce better results?
3. What does the messages list look like after three tool calls?
4. Why do you always need a step counter in a multi-step agent loop?
5. What is self-reflection and when would you use it?
6. What is the difference between the chat loop (Level 2) and the reasoning loop (Level 3)?
