# Capstone 5 — Agentic Code Interpreter

**XP:** 800  
**Difficulty:** Advanced  
**Requires:** Levels 1–9 (tool calling, agent loops, sandboxing concepts)  
**Estimated build time:** 3–5 days  
**API cost:** ~$0.10–0.40 per complex analysis task

---

## Why This Exists

The most powerful thing you can give an AI agent is the ability to run code.

Text generation is limited by what the model was trained on. Code execution is not. An agent that can write Python, run it, read the output, and iterate can solve problems that no amount of prompting can — data analysis, mathematical computation, file manipulation, API calls, visualisation generation.

This is the architecture behind GPT's Code Interpreter (now called Advanced Data Analysis), Anthropic's tool use, and most serious AI data tools. It's also one of the most technically demanding patterns to implement correctly — because code execution means arbitrary code execution, which means you need a sandbox.

The challenge is not getting the LLM to write code. It will. The challenge is running that code safely, handling errors intelligently, and building an iteration loop that actually converges on correct answers rather than hallucinating plausible-looking output.

---

## What This Unlocks

**Roles:**
- AI/ML Engineer at data-heavy companies (finance, healthcare, logistics)
- AI Product Engineer building internal analytics tools
- Data Engineering lead who understands AI augmentation
- Any company using AI for business intelligence — which is increasingly all of them

**What sets you apart:** Most candidates can prompt an LLM to write code. Very few have actually built the execution layer — the sandbox, the error handling loop, the output interpretation. That engineering work is what separates a demo from a production system.

**Projects you can launch after this:**
- An AI analyst that answers questions about any CSV or database in plain English
- An AI debugging assistant that runs code and explains what's wrong
- A financial analysis agent that pulls data, runs calculations, and produces reports autonomously

**What you can say:** "I built a code execution agent with a sandboxed Python environment. Here's how I handled security, error loops, and the tradeoff between autonomy and reliability."

---

## The System

Build an agent that:

1. Receives a question about a dataset in plain English
2. Plans the analysis steps needed to answer it
3. Writes Python code for each step
4. Executes that code in a sandboxed environment
5. Reads the output — including errors
6. Iterates: if the code fails, the agent debugs and retries
7. Produces a structured answer with supporting visualisations

The system must handle:
- Code that fails (syntax errors, runtime errors, wrong output)
- Questions that require multiple sequential code steps
- Code that generates charts or visualisations (not just text output)
- Edge cases in the data (missing values, wrong types, empty results)

---

## Technologies

| Component | Technology | Why |
|-----------|-----------|-----|
| Code execution sandbox | E2B (cloud sandbox) or Docker container | Prevents arbitrary code from accessing host system |
| Python runtime | Standard Python 3.11+ | With pandas, matplotlib, numpy pre-installed in sandbox |
| LLM | Claude Sonnet (code writing quality matters) | Strong code generation, understands error messages |
| Output parsing | Structured output with tool use | Code, stdout, stderr, and generated files as separate fields |
| Visualisation | matplotlib or plotly in sandbox, return as base64 PNG | Render charts without a display server |

**The sandboxing question — why it matters:**
If you run LLM-generated code without a sandbox, you are executing arbitrary untrusted code on your machine. The LLM can be prompted (directly or indirectly) to delete files, make network requests, or exfiltrate data. E2B creates isolated microVMs per execution. Docker is a lower-cost alternative. Never use `exec()` or `subprocess` on the host machine without isolation.

---

## Research Areas

- **Sandboxed code execution** — how to isolate code execution environments (VMs, containers, WebAssembly)
- **Program synthesis** — the field of automatically generating programs from specifications
- **ReAct pattern** — the reason-act-observe loop that drives iterative code generation
- **Chain-of-thought for code** — how decomposing a complex analysis task into steps improves code generation accuracy
- **Tool use in LLMs** — how models learn to generate structured tool calls vs free-text code

**Papers worth reading:**
- "PAL: Program-aided Language Models" (Gao et al., 2022) — the foundation of this pattern
- "Code as Policies" (Liang et al., 2022) — applying code generation to robotics decision-making
- "Self-Debugging: Teaching LLMs to Debug Their Predicted Programs" (Chen et al., 2023)

---

## Agent Team

| Agent | Role |
|-------|------|
| Task Planner | Receives the user's question and the dataset schema. Breaks the analysis into a sequence of discrete steps. Writes a plan before any code is generated. |
| Code Writer | Receives one step from the plan and writes Python code to execute it. Uses structured output — code block only, no prose mixed in. |
| Sandbox Executor | Receives code, runs it in the isolated environment, returns stdout, stderr, exit code, and any generated files. |
| Error Interpreter | If stderr is non-empty or exit code != 0, interprets the error and produces a corrected version of the code. Tracks retry count — max 3 attempts per step. |
| Output Synthesiser | Receives the final code outputs (text + visualisations) and writes a structured answer to the original question. Does not generate new calculations — only interprets what the code actually produced. |
| Safety Monitor | Runs before execution. Scans generated code for obvious sandbox escape attempts (file system access outside allowed paths, network calls, subprocess spawning). Blocks and rerequests if flagged. |

---

## Build Stages

### Part A — Sandbox Setup
Get E2B or Docker running and execute a simple Python script from your application. Print "hello world". Read the output. This sounds trivial — it takes most people 2–3 hours the first time. The sandbox configuration is where most implementations fail.

Verify your sandbox:
- Can execute Python with pandas, matplotlib, numpy
- Cannot access the host file system beyond the working directory
- Cannot make outbound network requests (optional but recommended)
- Returns stdout, stderr, and exit code correctly

### Part B — Single-Step Code Execution
Write a single code generation → execute → read output loop. Give the agent a simple dataset (a CSV with 100 rows) and ask "what is the average age?" The agent writes code, runs it, and returns the answer. No iteration yet — just the happy path.

### Part C — Error Handling Loop
Deliberately trigger errors. Feed the agent malformed code. Feed it a question about a column that doesn't exist. The Error Interpreter must handle:
- Syntax errors (fix the code)
- Runtime errors (fix the logic)
- Wrong output (the code ran but the answer is wrong — the hardest case)

Cap retries at 3. If 3 retries fail, return "I could not answer this question" with the error context. Do not loop forever.

### Part D — Multi-Step Analysis
Add the Task Planner. Give the agent a question that requires 3+ steps: "Find the top 5 customers by revenue, calculate their average order value, and show a bar chart."

Each step must produce output that the next step can use. The planner must understand data dependencies between steps.

### Part E — Visualisation Output
Add chart generation. The sandbox must return charts as base64-encoded PNGs. Your application renders them alongside the text answer. Test with: histograms, bar charts, scatter plots, time series.

### Part F — Safety Layer + Evaluation
Add the Safety Monitor. Build an eval suite with 20 questions across 3 datasets. Measure: correct answer rate, retry rate, average steps per query, average cost per query.

Write a 400-word reflection: What types of questions did the agent fail on? What did the error patterns tell you about how the LLM thinks about code? What would break this system if 1,000 users used it simultaneously?

---

## Completion Checklist

- [ ] Sandbox running: executes Python, cannot access host FS, returns stdout/stderr/exit code
- [ ] Single-step code execution working on simple questions
- [ ] Error handling loop with max 3 retries per step
- [ ] Multi-step planner: 3+ step analysis chains working
- [ ] Visualisation output: charts returned as base64 PNG and rendered
- [ ] Safety Monitor blocking obvious sandbox escape attempts
- [ ] Eval suite: 20 questions, correct answer rate measured
- [ ] Retry rate and cost per query logged
- [ ] Reflection write-up complete

---

## What Completing This Demonstrates

- You understand sandboxed execution and why it matters for security
- You've implemented the ReAct loop in a context where errors are real and consequential
- You can build systems that are more reliable than single-shot generation through iteration
- You understand the gap between "the LLM wrote code" and "the code was executed and the answer is correct"

The Code Interpreter pattern is in every serious data AI product. Most implementations are insecure, loop-prone, or brittle. Yours will not be.
