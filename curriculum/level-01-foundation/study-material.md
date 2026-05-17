# Level 1 — Foundation
## Study Material: How AI Agents Actually Work

> Read this before or alongside the hands-on build.
> Goal: understand the theory so the code makes sense when you type it.

---

## What is an AI Agent?

A regular AI (like Claude in a chat window) takes input and produces text output. That's it.

An AI **agent** is different. It can:
- Decide to take **actions** (call tools, run code, search the web)
- Observe the **results** of those actions
- Use those results to continue reasoning toward a goal

The key word is **loop**. An agent doesn't just respond once — it reasons, acts, observes, reasons again, acts again, until the job is done.

```
Regular AI:   User → Claude → Response. Done.

AI Agent:     User → Claude → Action → Result → Claude → Action → Result → Claude → Response
```

---

## The Three Core Ideas of Level 1

### 1. Tool Calling

Claude by itself can only produce text. It can't run Python, look things up, or do reliable arithmetic. Tools give Claude **capabilities beyond text**.

A tool is two things:
- A **JSON definition** — tells Claude the tool exists, what it does, and what inputs it needs
- A **Python function** — the actual code that runs when Claude decides to use it

Claude never runs the tool itself. It says *"I want to call this tool with these inputs"* and then **your code** runs it.

This is the most important mental model in agentic AI:

> **Claude decides. Your code executes.**

### 2. The Agent Loop

The agent loop is the cycle of:
1. Send message to Claude (with tools available)
2. Claude responds — either with an answer OR a tool call request
3. If tool call: your code runs the tool, sends result back to Claude
4. Claude responds with final answer
5. Repeat from step 1 for the next message

```
┌─────────────────────────────────────────┐
│              Agent Loop                  │
│                                         │
│  User Input                             │
│      ↓                                  │
│  Claude reasons                         │
│      ↓                                  │
│  stop_reason == 'tool_use'?             │
│      ↓ Yes              ↓ No            │
│  Run tool         Print response        │
│      ↓                                  │
│  Send result back to Claude             │
│      ↓                                  │
│  Claude gives final answer              │
│      ↓                                  │
│  Back to User Input                     │
└─────────────────────────────────────────┘
```

### 3. The Messages List

Claude has **no memory between API calls**. Every time you call the API, Claude starts fresh.

The `messages` list is how you give Claude memory. You pass the entire conversation history with every API call. Claude reads it all and responds as if it remembers the whole conversation.

```python
messages = [
    {"role": "user",      "content": "What is 10 * 5?"},
    {"role": "assistant", "content": [ToolUseBlock(...)]},
    {"role": "user",      "content": [tool_result: "50"]},
]
```

Each turn adds two new entries to the list. The list grows as the conversation grows.

---

## Why Two API Calls?

This confuses most beginners. Here's the explanation:

**Call 1** — "Claude, here is the user's question and your available tools. What do you want to do?"

Claude responds: "I want to call the calculator with expression '10 * 5'. Here's my reasoning."

Claude then **stops**. It can't run your Python code. It just says what it wants done.

**Your code runs** the calculator. Gets back "50".

**Call 2** — "Claude, here is the full conversation including the calculator result '50'. Now finish answering the user."

Claude responds: "10 multiplied by 5 is 50."

This is why you need two calls — one to get Claude's tool call decision, and one to get Claude's final response after you've run the tool.

---

## What is stop_reason?

Every Claude API response includes a `stop_reason` field. It tells you *why* Claude stopped generating text.

| stop_reason | What it means |
|-------------|---------------|
| `end_turn` | Claude finished responding naturally. No tool needed. |
| `tool_use` | Claude wants to call a tool. It's waiting for the result. |
| `max_tokens` | Claude hit the token limit. Response was cut off. |

In your agent loop, `stop_reason == 'tool_use'` is your signal to run the tool and send the result back.

---

## What are Tokens?

Tokens are how the API measures text. Roughly:
- 1 token ≈ 4 characters or ¾ of a word
- "Hello world" = 2 tokens
- "What is 847 divided by 13?" = about 8 tokens

**Why tokens matter for agents:**

Every API call has a cost measured in tokens — both input (what you send) and output (what Claude returns).

When you add tool definitions to your API call, you're adding tokens. A calculator tool definition adds roughly 100 tokens to every single API call — even if Claude never uses the tool. With 50 tools, that's thousands of extra tokens per call.

This is exactly why MCP (Level 6) exists — to solve the token cost problem of manually defined tools.

---

## The Tool Definition Explained

When you define a tool, you're writing a JSON description that Claude reads:

```python
{
    "name": "calculator",
    "description": "Always use this for arithmetic. Never calculate yourself.",
    "input_schema": {
        "type": "object",
        "properties": {
            "expression": {
                "type": "string",
                "description": "The expression to evaluate, e.g. '847 / 13'"
            }
        },
        "required": ["expression"]
    }
}
```

Each field has a specific purpose:

**name** — The identifier. Claude uses this to say "I want to call `calculator`." Your `tool_map` dictionary uses this exact name to find the right Python function.

**description** — Instructions to Claude about *when* to use this tool. This is prompt engineering inside the tool definition. The stronger this description, the more reliably Claude calls the tool instead of guessing.

**input_schema** — Defines what Claude must provide when calling the tool. Claude reads this and knows it needs to supply a string called `expression`. The example `'847 / 13'` nudges Claude to translate natural language into clean Python arithmetic.

**required** — Lists which fields are mandatory. Claude won't call the tool without providing these.

---

## The Dispatch Pattern

When you have multiple tools, you need a clean way to call whichever one Claude chose. This is the `tool_map` pattern:

```python
tool_map = {
    "calculator": calculator,
    "unit_converter": unit_converter,
    "weather": get_weather
}

# Claude tells you which tool it wants
tool_name = tool_use.name        # e.g. "calculator"
tool_input = tool_use.input      # e.g. {"expression": "10 * 5"}

# Dynamically call the right function
result = tool_map[tool_name](**tool_input)
```

`**tool_input` unpacks the dictionary as keyword arguments. So:
```python
tool_map["calculator"](**{"expression": "10 * 5"})
# is the same as:
calculator(expression="10 * 5")
```

This pattern works for any number of tools without changing the dispatch logic.

---

## The Full Agent Loop in Plain English

1. User types a question
2. You send it to Claude along with your tool definitions
3. Claude reads the question and the tools available
4. Claude decides: "I need to use the calculator for this"
5. Claude sets `stop_reason = 'tool_use'` and returns a `ToolUseBlock`
6. Your code detects `stop_reason == 'tool_use'`
7. Your code extracts the tool name and input from the `ToolUseBlock`
8. Your code runs the calculator function
9. Your code appends Claude's tool call response to the messages list
10. Your code appends the tool result to the messages list
11. Your code makes a second API call with the full updated messages list
12. Claude reads the full conversation including the result
13. Claude formulates a natural language answer
14. You print it

---

## Key Mental Models to Lock In

**Claude is the brain, your code is the hands.**
Claude never executes anything. It only decides and communicates. Your Python code does all real-world actions.

**The messages list is the memory.**
Claude has no state between calls. The messages list is the entire conversation history you pass with every request. Without it, Claude has no idea what happened before.

**Tool definitions are instructions to Claude, not to your code.**
The JSON you write in `tools=[]` is read by Claude to understand what tools exist and when to use them. Your Python function is separate — it's what actually runs.

**stop_reason is your control signal.**
`tool_use` means "run my tool and come back". `end_turn` means "I'm done, show this to the user."

---

## Common Mistakes at Level 1

**Forgetting to pass `tools=tools` to the API call.**
If you don't pass the tools, Claude has no idea they exist and will just answer everything from its own knowledge.

**Hardcoding the tool call instead of using tool_map.**
Fine for one tool, but breaks as soon as you add a second. Always use the dispatch pattern from day one.

**Not sending the tool result back.**
If you run the tool but don't append the result to messages and make a second API call, Claude never gets the answer and can't respond properly.

**Using `eval()` in production.**
Fine for learning, dangerous in production because it executes any Python code. For real tools, use a proper maths library.

---

## Sources to Read

- [Anthropic Tool Use Docs](https://docs.anthropic.com/en/docs/build-with-claude/tool-use) — the official guide, read the "How it works" section
- [Anthropic Python SDK](https://github.com/anthropic-sdk/anthropic-sdk-python)
- [Building effective agents — Anthropic](https://www.anthropic.com/research/building-effective-agents)

---

## What You Should Be Able to Explain After Level 1

1. Why does the agent make two API calls instead of one?
2. What does `stop_reason='tool_use'` mean and what do you do when you see it?
3. Why does the messages list grow with every turn?
4. What is the difference between the tool JSON definition and the Python function?
5. Why does Claude not run tools itself?
6. What happens to tokens when you add tool definitions?
