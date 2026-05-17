# Level 5 — Memory and State

**Status:** Locked  
**XP:** 300  
**Unlocks:** RAG, vector embeddings, persistent memory  
**Requires:** Level 4 complete

---

## What You'll Build

A personal assistant agent with memory. It remembers things the user tells it across sessions. Build three tiers:
1. In-conversation memory — the messages list (already know this)
2. Session memory — saved to a JSON file (introduced in Level 2)
3. Semantic search over past conversations — a simple vector store (new at this level)

---

## Key Concepts

- The difference between short-term and long-term memory
- What a vector embedding is and why similarity search works
- What RAG (Retrieval Augmented Generation) means
- The RAG pipeline: chunk → embed → store → retrieve → inject
- How to decide what to save vs what to forget
- Why memory is a privacy and security concern

---

## Study Material

No uploaded study material for this level yet. Read the research docs first:
- [AI Agent Research Landscape — Part 2: Memory and RAG Advances](../../research/ai-agent-research-landscape.md#part-2--memory-and-rag-advances)
- [Deep Technical Edition — Concept 4: Memory and RAG](../../research/ai-agent-deep-technical.md#concept-4--memory-and-retrieval-augmented-generation)

---

## Completion Checklist

1. What is the difference between in-context memory and persistent memory?
2. What is a vector embedding and why does cosine similarity find relevant chunks?
3. Describe the full RAG pipeline from document to response.
4. What is chunking and why does chunk size matter?
5. What is contextual retrieval and why does it improve accuracy?
6. What are three ways memory can become a privacy risk in production?

---

## Resources

- [Contextual Retrieval — Anthropic (2024)](https://www.anthropic.com/news/contextual-retrieval)
- [ChromaDB](https://www.trychroma.com/) — simple local vector store to start with
- [MemGPT paper](https://arxiv.org/abs/2310.08560) — memory hierarchies for agents
- [RAG original paper (Lewis et al., 2020)](https://arxiv.org/abs/2005.11401)

---

## Your Build

Add your code to the `builds/` folder.

---

## Next

[Level 6 — MCP and Tool Ecosystems](../level-06-mcp-and-tools/)
