# Level 2 — Making it Real

**Status:** Locked  
**XP:** 150  
**Unlocks:** Multi-tool dispatch, error handling, Streamlit UI  
**Requires:** Level 1 complete

---

## What You'll Build

Extend the calculator agent into a proper chat loop. The user types questions continuously until they type "quit". Add a second tool — a unit converter (km to miles, celsius to fahrenheit). Add error handling so the agent doesn't crash on bad input. Wrap it in a Streamlit UI.

---

## Key Concepts

- How to build a `while True` input loop
- The tool dispatch pattern (`tool_map` with `**kwargs`)
- How the messages list acts as conversation memory
- What happens when a tool fails and how to tell Claude about it
- Why you always send tool results back even on errors
- Streamlit basics — `st.chat_input`, `st.chat_message`, `st.session_state`

---

## Study Material

Read [study-material.md](study-material.md) before building.

---

## Completion Checklist

1. Why does the messages list grow across turns, and why does that give Claude "memory"?
2. What happens to the messages list when you restart the program, and how do you fix that?
3. Why do you always send a tool result back even when the tool fails?
4. What does `**tool_input` do and why is it better than hardcoding the function call?
5. What is `st.session_state` and why does Streamlit need it?
6. How is the Streamlit UI connected to the agent loop — what actually changes?

---

## Resources

- [Streamlit docs — chat elements](https://docs.streamlit.io/develop/api-reference/chat)
- [Streamlit session state](https://docs.streamlit.io/develop/concepts/architecture/session-state)
- [Tool use best practices — Anthropic](https://docs.anthropic.com/en/docs/build-with-claude/tool-use#best-practices-for-tool-definitions)

---

## Your Build

Add your code to the `builds/` folder.

---

## Next

[Level 3 — Reasoning Patterns](../level-03-reasoning-patterns/)
