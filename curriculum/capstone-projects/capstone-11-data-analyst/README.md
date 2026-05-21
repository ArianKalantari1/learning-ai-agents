# Capstone 12 — Autonomous Data Analyst

**XP:** 800  
**Difficulty:** Advanced  
**Requires:** Levels 1–9, Capstone 5 (Code Interpreter is a prerequisite — you need sandboxed execution)  
**Estimated build time:** 4–5 days  
**API cost:** ~$0.15–0.40 per analysis session

---

## Why This Exists

Every company has data. Most companies don't have enough data analysts to answer the questions their data could answer.

A good data analyst does something that seems simple: they receive a messy dataset, explore it without being told what to look for, form hypotheses about what's interesting, test those hypotheses with statistics and visualisation, and communicate what they found in plain English. That process takes hours.

An autonomous data analyst agent does the same thing — not as well, not with the same intuition, but fast enough and good enough that a business user who would never get a data analyst's time can now get answers in minutes.

The commercial value is immediate and obvious. The technical challenge is significant: the agent must make decisions about what to investigate, not just answer questions it's been asked. It must explore before it can explain. That's a different architecture from a question-answering system.

---

## What This Unlocks

**Roles:**
- AI Data Engineer — bridges data engineering and AI systems
- AI Product Engineer building analytics or BI tools
- Any role at a company that has data and wants to extract more value from it without hiring more analysts
- Freelance AI developer: "I'll build you an AI analyst for your business data" is a real proposition right now

**Industries where this pays immediately:**
- E-commerce: customer behaviour, product performance, churn patterns
- Healthcare: patient outcome patterns, operational efficiency
- Finance: portfolio analysis, risk pattern detection
- Operations: supply chain anomalies, process efficiency

**What you can say:** "I built an autonomous data analyst agent that explores datasets without being told what to look for. Here's how it decides what's interesting, how it validates its own hypotheses with code, and here's an analysis it produced on a dataset it had never seen."

---

## The System

Build an agent that:

1. Receives a dataset (CSV, database connection, or API) and a plain English objective ("understand what drives customer churn" or "find anomalies in this transaction data")
2. **Explores** the dataset autonomously — profiles it, identifies data quality issues, discovers what columns exist and what they contain
3. **Forms hypotheses** — what might be interesting here? What patterns are worth testing?
4. **Tests each hypothesis** with code — writes and runs statistical analysis and visualisation code
5. **Iterates** — findings from one analysis inform the next hypothesis
6. **Synthesises** a structured report: key findings, supporting evidence (charts + statistics), data quality issues found, recommended next steps

The agent is autonomous between steps. It does not ask the user what to do next — it decides. The user provides the initial objective and receives the final report.

---

## Technologies

| Component | Technology | Why |
|-----------|-----------|-----|
| Code execution | E2B sandbox or Docker (from Capstone 5) | Safe execution of generated analysis code |
| Data profiling | ydata-profiling (formerly pandas-profiling) | Automated statistical profiling of any DataFrame |
| Statistics | scipy.stats in sandbox | Hypothesis testing, correlation analysis, distribution fitting |
| Visualisation | matplotlib + seaborn in sandbox | Generate charts; return as base64 PNG |
| LLM | Claude Sonnet | High-quality reasoning needed for hypothesis generation and synthesis |
| Report generation | Structured markdown + embedded charts | Final output format |

---

## Research Areas

- **Exploratory Data Analysis (EDA)** — the practice this agent automates
- **Automated Machine Learning (AutoML)** — the broader field of automating ML pipelines (related but distinct)
- **Statistical hypothesis testing** — t-tests, chi-squared, ANOVA — how the agent validates its findings
- **Anomaly detection** — statistical and ML approaches to finding unusual patterns
- **Data storytelling** — how to communicate data findings to non-technical audiences

**Resources worth reading:**
- "The Art of Data Science" (Peng & Matsui) — the manual version of what you're automating
- "Storytelling with Data" (Knaflic) — how findings should be communicated
- "Think Stats" (Downey) — statistical thinking for programmers

---

## Agent Team

| Agent | Role |
|-------|------|
| Data Profiler | Receives dataset. Runs automated profiling: schema, data types, null rates, value distributions, correlations. Returns a structured profile that all other agents reference. |
| Data Quality Inspector | Identifies issues: missing values, outliers, inconsistent formats, suspicious patterns. Flags but does not fix — the human needs to know what's in their data before trusting any analysis. |
| Hypothesis Generator | Reads the profile and the user's objective. Generates a ranked list of 5–8 hypotheses worth testing. Examples: "Churn correlates with subscription tier", "Anomalies cluster around month-end dates", "High-value customers have shorter first-purchase windows." |
| Analysis Agent | Takes one hypothesis. Writes Python code to test it (statistical test + visualisation). Executes in sandbox. Interprets results: is the hypothesis supported, rejected, or inconclusive? What's the effect size? |
| Iteration Planner | After each analysis: should we go deeper on this finding, test a related hypothesis, or move to the next item in the queue? Manages the exploration queue. |
| Report Writer | Assembles all findings into a structured report: Executive Summary, Key Findings (ranked by impact), Supporting Evidence (embedded charts), Data Quality Issues, Recommended Next Steps. Plain English throughout — no statistical jargon without explanation. |

---

## Build Stages

### Part A — Data Profiling
Build the Data Profiler. Use ydata-profiling as a starting point (it produces a comprehensive HTML report automatically) then build a structured JSON version that your agents can consume. Test on 3 different datasets: a simple e-commerce CSV, a messy real-world CSV with quality issues, and a time-series dataset.

### Part B — Hypothesis Generation
Build the Hypothesis Generator. Feed it the data profile and an objective. Measure: are the hypotheses reasonable given the data? Are they specific enough to be testable? Are they ranked sensibly (most likely to be interesting first)?

Test with a dataset where you already know the answers. Does the agent generate the hypotheses that match the real patterns?

### Part C — Analysis Loop (single hypothesis)
Build the Analysis Agent on a single hypothesis first. It writes code, runs it, interprets results. Test with 5 pre-defined hypotheses across different statistical tests (correlation, group comparison, distribution analysis, time series trend, anomaly detection).

### Part D — Iteration and Exploration Loop
Add the Iteration Planner. The agent now runs multiple hypotheses sequentially, with each analysis informing what to test next. Run the full exploration loop on a dataset with 5+ interesting patterns seeded in it. Does the agent find at least 3 of them without being told where to look?

### Part E — Data Quality Integration
Add the Data Quality Inspector. The report must include a Data Quality section that appears before any findings — the reader needs to know the reliability of the data before trusting the analysis.

Test with a deliberately dirty dataset: missing values, outliers, inconsistent date formats, duplicate rows.

### Part F — Full Report Generation + Evaluation
Run the complete system on 3 datasets where you know the ground truth (real insights that should be found). Measure: what percentage of the known insights did the agent surface? What false positives (non-findings reported as findings) did it produce? How readable is the report to a non-technical person?

Ask a non-technical person to read one of the reports and explain what they learned. If they can't extract the key findings, the report writer needs revision.

---

## Completion Checklist

- [ ] Data profiler: structured JSON profile covering schema, distributions, correlations, null rates
- [ ] Data quality inspector: identifies missing values, outliers, format inconsistencies
- [ ] Hypothesis generator: produces 5+ testable, ranked hypotheses from profile + objective
- [ ] Analysis agent: tests one hypothesis with appropriate statistical test + visualisation
- [ ] All code executed in sandbox (from Capstone 5) — no direct execution
- [ ] Iteration planner: runs 5+ hypothesis tests in a coherent exploration sequence
- [ ] Full exploration loop: finds 3+ seeded patterns in test dataset without being told where to look
- [ ] Report: executive summary + ranked findings + embedded charts + data quality + next steps
- [ ] Non-technical readability test: a non-technical person can explain 3 key findings from the report

---

## What Completing This Demonstrates

- You can build agents that make autonomous decisions, not just answer questions
- You understand the full data analysis workflow well enough to encode it in an agent
- You've combined code execution (Capstone 5) with multi-agent orchestration in a commercially valuable product
- You can produce output that a non-technical person can act on

This is the pattern behind GitHub Copilot for data — the analyst that scales. A business user with this tool doesn't need to wait for a data analyst. That's a meaningful product.
