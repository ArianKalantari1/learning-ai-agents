# Level 2 — Making it Real
## Study Material: Chat Loops, Multiple Tools, and Error Handling

> Read this before or alongside the hands-on build.
> Goal: understand what makes an agent feel like a real product, not just a script.

---

## What Changes at Level 2?

Level 1 was a one-shot script. You hardcoded a question, ran the script, got one answer, it exited.

Level 2 is a real agent. The user types questions continuously. The agent keeps running. Multiple tools are available. Errors are handled gracefully. And at the end — we wrap it in a Streamlit chat UI so it actually looks like a product.

The core agent loop from Level 1 doesn't change. We're just adding layers around it.

```
Level 1:  One question → hardcoded → script exits
Level 2:  Any question → typed in real time → keeps running → Streamlit UI
```

---

## The Chat Loop

A chat loop is a `while True` loop that keeps the agent running until the user decides to stop.

```python
while True:
    user_input = input("You: ")
    
    if user_input.lower() == "quit":
        break
    
    # run the agent with user_input
    # print the response
    # loop again
```

Simple idea — but it changes everything about how the agent feels. Instead of editing code to change the question, the user just types. This is the foundation of every chatbot ever built.

**The messages list becomes the full conversation history:**

```
Turn 1:
  messages = [
    {role: "user", content: "What is 10 * 5?"}
  ]

Turn 2:
  messages = [
    {role: "user",      content: "What is 10 * 5?"},
    {role: "assistant", content: "The answer is 50."},
    {role: "user",      content: "Now divide that by 2"}
  ]

Turn 3:
  messages = [
    {role: "user",      content: "What is 10 * 5?"},
    {role: "assistant", content: "The answer is 50."},
    {role: "user",      content: "Now divide that by 2"},
    {role: "assistant", content: "50 divided by 2 is 25."},
    {role: "user",      content: "Add 7 to that"}
  ]
```

Notice Claude can now say "that" and know what it refers to. The conversation history gives Claude context across turns. This is the simplest form of agent memory.

---

## Multiple Tools

At Level 1 we had one tool: calculator.

At Level 2 we add a second: unit converter (km to miles, celsius to fahrenheit, etc).

Why does this matter? Because now Claude has to **choose** between tools. When the user asks "convert 100km to miles", Claude needs to pick `unit_converter`, not `calculator`. When they ask "what is 50 * 3", Claude needs to pick `calculator`.

The tool descriptions do this work. Claude reads both descriptions and picks the right one.

```python
tools = [
    {
        "name": "calculator",
        "description": "Use for arithmetic calculations: addition, subtraction, multiplication, division.",
        ...
    },
    {
        "name": "unit_converter",
        "description": "Use for converting between units: km/miles, celsius/fahrenheit, kg/pounds.",
        ...
    }
]
```

**The tool_map handles dispatch automatically:**

```python
tool_map = {
    "calculator": calculator,
    "unit_converter": unit_converter
}

# Claude picks "unit_converter", your code runs it — no if/else needed
result = tool_map[tool_use.name](**tool_use.input)
```

This is why the dispatch pattern matters — it scales to any number of tools without changing the logic.

---

## Error Handling

What happens when something goes wrong?

- User types "divide 10 by zero" → calculator crashes
- User types "convert bananas to miles" → unit converter doesn't know what to do
- The API times out → the whole program crashes

Without error handling, any of these ends the session. The user loses their conversation. That's bad.

**The right pattern: always send a result back, even on errors.**

```python
def calculator(expression):
    try:
        result = eval(expression)
        return str(result)
    except ZeroDivisionError:
        return "Error: Cannot divide by zero"
    except Exception as e:
        return f"Error: {str(e)}"
```

Why return the error string instead of raising an exception? Because you need to send *something* back to Claude. If you send nothing, the messages list breaks. If you send the error, Claude can read it and respond helpfully:

```
User:   "What is 10 divided by 0?"
Tool:   "Error: Cannot divide by zero"
Claude: "You can't divide by zero — it's mathematically undefined.
         Would you like to try a different calculation?"
```

This is a much better user experience than the program crashing.

**The golden rule of tool error handling:**

> Always send a tool_result back to Claude, even if the tool failed. The content can be an error message. Claude will handle it gracefully.

---

## Conversation Memory Across Sessions

At Level 2 the messages list still resets when you restart the program. Every new session starts blank.

We'll fix this by saving the messages list to a JSON file at the end of every session and loading it at the start of the next.

```python
import json

def load_history():
    try:
        with open("conversation.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_history(messages):
    with open("conversation.json", "w") as f:
        json.dump(messages, f)
```

This is the simplest form of **persistent memory**. The agent now remembers things you told it last week.

It's also where you start thinking about privacy — that JSON file contains everything the user ever said. Who can read it? Where is it stored? These questions matter at Level 5 (Memory) but are worth thinking about now.

---

## Streamlit — Wrapping the Agent in a UI

Once the chat loop works in the terminal, we add Streamlit. Streamlit lets you build web UIs in pure Python — no HTML, no JavaScript needed.

**The basic Streamlit chat pattern:**

```python
import streamlit as st

st.title("AI Calculator Agent")

# Display conversation history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Get user input
if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    response = run_agent(prompt)
    st.session_state.messages.append({"role": "assistant", "content": response})
```

`st.session_state` is Streamlit's way of keeping data alive between rerenders. Every time a user sends a message, Streamlit reruns the whole script — `session_state` is what persists across those reruns.

**The mental model:**

Your `agent.py` logic doesn't change. You're just replacing `input()` and `print()` with Streamlit's chat components. The agent loop, tool dispatch, error handling — all identical. Streamlit is just a skin on top.

---

## Key Mental Models for Level 2

**The loop is the agent.**
An agent that exits after one answer is a script. An agent that keeps running and handles anything the user throws at it is a product. The `while True` loop is what makes the difference.

**Multiple tools = Claude making choices.**
When you have two tools, Claude starts reasoning about which one to pick. Your job is to write descriptions clear enough that Claude always picks the right one. This is prompt engineering at the tool level.

**Errors are just another kind of result.**
Don't try to hide errors from Claude. Send them back as tool results. Claude will use them to give a better response than your code ever could.

**Session state is just a list.**
Whether it's a Python list, a JSON file, or a database — conversation memory is just a stored sequence of messages. Streamlit's `session_state`, your `messages` list, and the JSON file are all the same idea at different levels of persistence.

---

## Sources to Read

- [Streamlit docs — chat elements](https://docs.streamlit.io/develop/api-reference/chat)
- [Streamlit session state](https://docs.streamlit.io/develop/concepts/architecture/session-state)
- [Tool use best practices — Anthropic](https://docs.anthropic.com/en/docs/build-with-claude/tool-use#best-practices-for-tool-definitions)

---

## What You Should Be Able to Explain After Level 2

1. Why does the messages list grow across turns, and why does that give Claude "memory"?
2. What happens to the messages list when you restart the program, and how do you fix that?
3. Why do you always send a tool result back even when the tool fails?
4. What does `**tool_input` do and why is it better than hardcoding the function call?
5. What is `st.session_state` and why does Streamlit need it?
6. How is the Streamlit UI connected to the agent loop — what actually changes?
