# Level 6 — MCP and Tool Ecosystems

**Status:** Locked  
**XP:** 300  
**Unlocks:** Model Context Protocol, dynamic tool discovery  
**Requires:** Level 5 complete

---

## What You'll Build

Convert the Level 1 calculator agent to use MCP (Model Context Protocol). Build a simple MCP server that exposes your calculator and unit converter as tools. Connect Claude to it. Compare token cost and code complexity against the manual approach from Level 1.

---

## Key Concepts

- Why MCP exists — the manual approach doesn't scale past ~10 tools
- What an MCP server is and how Claude discovers tools from it
- The difference between `tools=[]` (manual) and an MCP connection
- How MCP reduces token cost for large tool sets
- Why MCP is an open standard and what that means for the ecosystem

---

## Completion Checklist

1. Why doesn't the manual `tools=[]` approach scale?
2. What does an MCP server do and how does Claude communicate with it?
3. What is the difference between defining tools manually vs via MCP in terms of token cost?
4. How does Claude discover available tools from an MCP server?
5. What does "open standard" mean and why does it matter for MCP?
6. When would you still choose manual tool definition over MCP?

---

## Resources

- [MCP introduction — Anthropic](https://docs.anthropic.com/en/docs/mcp)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [MCP specification](https://modelcontextprotocol.io)

---

## Your Build

Add your code to the `builds/` folder. Include both the MCP server and the client agent.

---

## Next

[Level 7 — Multi-Agent Systems](../level-07-multi-agent-systems/)
