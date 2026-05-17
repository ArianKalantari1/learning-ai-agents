# Level 9 — Production Agents

**Status:** Locked  
**XP:** 400  
**Unlocks:** Streaming, prompt caching, production deployment  
**Requires:** Level 8 complete

---

## What You'll Build

Productionise the Level 2 chat agent. Add:
1. Response streaming — the user sees output as it's generated
2. A cost tracker that logs tokens per session
3. Prompt caching for repeated context
4. Rate limit handling with exponential backoff
5. A FastAPI wrapper so it runs as a web service

---

## Key Concepts

- How streaming works with the Anthropic SDK — `client.messages.stream()`
- What exponential backoff is and why you need it for rate limits
- How prompt caching reduces cost on repeated context (system prompts, tool definitions)
- What a FastAPI wrapper looks like and why you'd build one
- The real cost of running an agent at scale — tokens × requests × users

---

## Completion Checklist

1. How does streaming change the user experience and why does it matter?
2. What is exponential backoff and why do you use it instead of fixed-delay retries?
3. What parts of a prompt are good candidates for caching? What are not?
4. How does prompt caching work technically in the Anthropic SDK?
5. What does FastAPI add over running the agent as a plain Python script?
6. If your agent runs 1,000 requests per day at an average of 2,000 tokens per request, what's the rough monthly token cost?

---

## Resources

- [Anthropic streaming docs](https://docs.anthropic.com/en/docs/streaming)
- [Prompt caching — Anthropic](https://docs.anthropic.com/en/docs/prompt-caching)
- [FastAPI](https://fastapi.tiangolo.com/)

---

## Your Build

Add your code to the `builds/` folder. Include both the FastAPI app and a simple load test.

---

## Next

[Level 10 — Advanced Patterns](../level-10-advanced-patterns/)
