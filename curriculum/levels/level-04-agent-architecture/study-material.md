# Level 4 — Agent Architecture
## Study Material: Planning, Orchestration, and Subagents

> Read this before or alongside the hands-on build.
> Goal: understand how to break complex tasks into manageable pieces and delegate them — the foundation of every serious AI system.

---

## What Changes at Level 4?

Levels 1-3 were single-agent systems. One Claude instance, one chain of reasoning, one sequence of tool calls.

Level 4 introduces **multiple agents working together**.

The core idea: some tasks are too complex for one agent to handle well in one go. The solution is to break the task into subtasks and give each subtask to a specialist agent that's optimised for exactly that job.

This is called **orchestration** — and it's how real production AI systems are built.

---

## The Problem That Level 4 Solves

Imagine asking a single agent:
> "Write me a report on climate change — include an executive summary, key statistics, regional impacts, and a conclusion."

A single agent will try to do everything at once. It'll write mediocre content across all sections because it's juggling too many responsibilities simultaneously. It has one system prompt trying to be a researcher, a writer, a statistician, and an editor all at once.

The better approach:

```
Orchestrator agent
├── Research subagent    → finds facts and statistics
├── Writing subagent     → writes each section
├── Statistics subagent  → validates numbers and data
└── Editor subagent      → reviews and improves the final output
```

Each subagent has a focused system prompt, specific tools, and one clear job. The orchestrator coordinates them and assembles the final result.

---

## The Orchestrator / Subagent Pattern

This is the most important architectural pattern in agentic AI.

**Orchestrator** — the manager agent. It:
- Receives the user's complex goal
- Breaks it into subtasks
- Delegates each subtask to the right subagent
- Collects results
- Assembles and returns the final output

**Subagent** — the specialist worker. It:
- Receives one specific subtask
- Has a focused system prompt for that task
- Has only the tools it needs
- Returns one clear output

```
User
 │
 ▼
Orchestrator ("break this into parts and coordinate")
 ├──→ Subagent 1: Summary writer    → "Write executive summary"
 ├──→ Subagent 2: Stats finder      → "Find key statistics"
 ├──→ Subagent 3: Regional analyst  → "Analyse regional impacts"
 └──→ Subagent 4: Conclusion writer → "Write conclusion"
          │
          ▼
     Orchestrator assembles all outputs
          │
          ▼
        User gets final report
```

---

## What is a Subagent in Code?

A subagent is just another Claude API call — with a different system prompt and different tools.

```python
def run_subagent(task, system_prompt, tools=None):
    """A subagent is just a focused API call."""
    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=2048,
        system=system_prompt,
        tools=tools or [],
        messages=[
            {"role": "user", "content": task}
        ]
    )
    return response.content[0].text
```

That's it. A subagent isn't a special class or framework — it's a Claude API call with a focused purpose.

**The orchestrator calls subagents like tools:**

```python
def orchestrator(user_goal):
    subtasks = plan_subtasks(user_goal)
    
    summary    = run_subagent(subtasks["summary"],    SUMMARY_SYSTEM_PROMPT)
    statistics = run_subagent(subtasks["statistics"], STATS_SYSTEM_PROMPT, tools=[search_tool])
    impacts    = run_subagent(subtasks["impacts"],    ANALYSIS_SYSTEM_PROMPT, tools=[search_tool])
    conclusion = run_subagent(subtasks["conclusion"], WRITING_SYSTEM_PROMPT)
    
    final = assemble_report(summary, statistics, impacts, conclusion)
    return final
```

---

## Task Decomposition — The Hard Part

The orchestrator's most important job is **breaking the goal into the right subtasks**.

This is harder than it sounds. A bad decomposition produces worse results than just asking one agent to do everything.

**Good decomposition principles:**

**1. Each subtask should be independently completable.**
A subagent should be able to finish its task without needing results from another subagent. If subtask B needs subtask A's output, they're not independent — run A first, then B with A's result.

**2. Each subtask should have one clear output.**
"Write the executive summary" is good. "Write the executive summary and also find statistics and check the conclusion" is bad. One job per subagent.

**3. Subtasks should map to different expertise.**
If two subtasks require the same skills and tools, they probably don't need separate subagents. Merge them.

**Bad decomposition:**
```
Subtask 1: "Write the whole report"
Subtask 2: "Make it better"
```

**Good decomposition:**
```
Subtask 1: "Find 5 key statistics about climate change with sources"
Subtask 2: "Write a 150-word executive summary of climate change"
Subtask 3: "Analyse regional impacts in Asia, Europe, and North America"
Subtask 4: "Write a 100-word conclusion with actionable recommendations"
```

---

## How to Pass Context Between Agents

Subagents don't share memory. Each one starts fresh. So if subagent 2 needs the output of subagent 1, you pass it explicitly.

```python
# Run subagent 1
statistics = run_subagent(
    "Find 5 key climate statistics",
    STATS_SYSTEM_PROMPT
)

# Pass subagent 1's output into subagent 2's task
conclusion = run_subagent(
    f"Write a conclusion using these statistics: {statistics}",
    WRITING_SYSTEM_PROMPT
)
```

This explicit passing of context is both the strength and the weakness of multi-agent systems. Strength: each agent has exactly the context it needs, nothing more. Weakness: the orchestrator has to manage all of it manually.

---

## When to Decompose vs Do It in One Shot

More agents is not always better. In fact, for most tasks, one agent is better.

**Use a single agent when:**
- The task is straightforward and fits in one context window
- Steps depend heavily on each other's outputs
- Speed and cost matter more than specialisation
- The task is short enough that one good system prompt handles it

**Use multiple agents when:**
- The task genuinely requires different expertise in different sections
- Sections are truly independent and can run in parallel
- The total task is too long for one context window
- Quality of each section matters more than overall speed

**The rule of thumb:**
> Start with one agent. Add orchestration only when you hit a real limitation — quality, context length, or parallelism.

Most beginners jump to multi-agent too early because it sounds impressive. Then they discover it's slower, costs more, and is harder to debug than a single well-prompted agent.

---

## The Cost of Multi-Agent Systems

Every subagent is a separate API call. Each API call costs tokens.

```
Single agent approach:
  1 API call × 2000 tokens = 2000 tokens total

Orchestrator + 4 subagents approach:
  5 API calls × ~1500 tokens each = 7500 tokens total
```

Multi-agent costs roughly 3-5x more than single-agent for the same task. Sometimes that cost is worth it for quality or parallelism. Often it isn't.

This is why Level 8 (Evaluation) matters — you need to measure whether the multi-agent approach actually produces better results before committing to the extra cost.

---

## Different System Prompts — Why They Matter

Each subagent has a different system prompt that shapes its personality, focus, and behaviour.

```python
STATS_SYSTEM_PROMPT = """
You are a data researcher specialising in climate science.
Your job is to find accurate, cited statistics.
Always include the source and year for every statistic.
Never make up numbers. If you can't find a statistic, say so.
Return exactly 5 statistics in a numbered list.
"""

WRITING_SYSTEM_PROMPT = """
You are a professional report writer.
Your job is to write clear, engaging prose for a general audience.
Avoid jargon. Use short sentences. Be specific, not vague.
Write exactly the number of words requested, no more.
"""

ANALYSIS_SYSTEM_PROMPT = """
You are a regional policy analyst.
Your job is to analyse how issues affect specific geographic regions.
Always compare regions to each other.
Support every claim with a specific example.
"""
```

Notice how each prompt gives the subagent a **specific identity, constraints, and output format**. This is what makes the specialist approach work — you're not just splitting the work, you're optimising each piece for its specific job.

---

## Key Mental Models for Level 4

**An orchestrator is just an agent whose tools are other agents.**
The orchestrator calls subagents the same way Level 1 called the calculator. The only difference is the "tool" is another Claude API call instead of a Python function.

**Subagents don't share memory — you pass context explicitly.**
No subagent knows what another subagent did unless you tell it. This is a feature, not a bug — it keeps each agent focused.

**System prompts are the personality of each agent.**
The same Claude model, the same API, but completely different behaviour based on the system prompt. This is the real power of LLMs in multi-agent systems.

**Decomposition quality determines output quality.**
Garbage in, garbage out. If the orchestrator breaks the task badly, every subagent will produce mediocre results. Invest time in making the decomposition prompt excellent.

**More agents = more cost + more complexity.**
Always justify the multi-agent approach with a clear reason: parallelism, specialisation, or context length. Never add agents for complexity's sake.

---

## Common Mistakes at Level 4

**Hardcoding the subtasks instead of letting the orchestrator plan them.**
If you hardcode "always break into summary, stats, impacts, conclusion", your orchestrator can't adapt to different topics. Let Claude plan the decomposition dynamically.

**Giving subagents too much context.**
Subagents work better with focused, minimal context — just what they need for their specific task. Passing the entire conversation history to every subagent is wasteful and confusing.

**Building multi-agent when one agent would do.**
Before writing an orchestrator, try solving the task with one well-prompted agent. If the quality is good enough, ship that. Add orchestration only when you need it.

**Not formatting subagent outputs.**
If you don't specify the output format in each subagent's system prompt, you get inconsistent outputs that are hard to assemble. Always tell each subagent exactly what format to return.

---

## Sources to Read

- [Building effective agents — Anthropic](https://www.anthropic.com/research/building-effective-agents) — the orchestrator/subagent section is directly relevant here. Read it twice.
- [LLM-powered autonomous agents — Lilian Weng](https://lilianweng.github.io/posts/2023-06-23-agent/) — read the planning section.
- [ReAct paper](https://arxiv.org/abs/2210.03629) — revisit from Level 3. The multi-agent examples in section 3 are now directly relevant.

---

## What You Should Be Able to Explain After Level 4

1. What is the difference between an orchestrator and a subagent?
2. Why do specialist system prompts produce better results than one generic prompt?
3. How do you pass context from one subagent to another?
4. When should you use multi-agent vs single-agent?
5. Why does multi-agent cost more tokens, and when is that cost justified?
6. How does task decomposition quality affect the final output?
