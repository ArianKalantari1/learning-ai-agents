# Capstone 11 — Production LLM Observatory

**XP:** 750  
**Difficulty:** Advanced  
**Requires:** Levels 1–9 (production, streaming, observability concepts)  
**Estimated build time:** 3–4 days  
**API cost:** ~$0.05–0.15 per monitored session

---

## Why This Exists

Every AI system that goes to production becomes a black box.

Requests go in. Responses come out. You have no idea which agent called which tool, how long each step took, what it cost, or whether quality has drifted since you last looked. When something breaks or gets expensive, you find out from a user complaint or a billing alert. By then the damage is done.

Observability is the practice of making the internal state of a system externally visible without changing its behaviour. For traditional software, this is solved — logging, tracing, and metrics are table stakes. For LLM systems, almost nobody has this figured out yet. The tooling is immature, the patterns are being established right now, and the engineers who understand it are building it from scratch at companies paying senior salaries to have it.

This capstone builds a full observability platform for a multi-agent LLM system: traces every agent call, measures cost and latency at every step, detects quality regressions, and surfaces everything in a dashboard that a non-technical team member can read and act on.

---

## What This Unlocks

**Roles:**
- AI Platform Engineer — builds the infrastructure other AI engineers depend on
- ML Ops Engineer with LLM specialisation
- GenAI Lead — you cannot manage a production AI system without this data
- Any senior engineering role at a company with AI products in production

**What changes when you have this:**
- "Why is this response wrong?" becomes answerable (trace the specific agent call that produced the error)
- "Did the new prompt improve quality?" becomes measurable (compare traces before and after the change)
- "Why is our API bill higher this month?" becomes diagnosable (token counts per endpoint, per agent, per user)
- "Is quality regressing?" becomes visible before users notice (anomaly detection on quality scores)

**What you can say:** "I built a production observability platform for our LLM application. It traces every agent call with latency and token counts, runs automated quality scoring, and detects regressions before they reach users. Here's the dashboard."

---

## The System

Build an observability platform that wraps any multi-agent system and provides:

1. **Distributed tracing** — every agent call as a span in a trace, with parent-child relationships preserved
2. **Cost tracking** — token counts and dollar cost per span, per trace, per endpoint, per day
3. **Latency tracking** — time per span, p50/p95/p99 distribution per endpoint
4. **Quality scoring** — automated scoring of a sample of outputs using LLM-as-judge
5. **Anomaly detection** — alerts when cost, latency, or quality metrics deviate significantly
6. **Dashboard** — real-time and historical view, readable by a non-engineer

Target the observability at one of your existing capstone systems (Capstone 1 is recommended).

---

## Technologies

| Component | Technology | Why |
|-----------|-----------|-----|
| Tracing instrumentation | OpenTelemetry (Python SDK) | Industry standard, vendor-neutral, exportable to any backend |
| Trace storage | Jaeger (local via Docker) or Grafana Tempo | Store and query distributed traces |
| Metrics | Prometheus + custom metrics | Cost, latency, token counts as time-series metrics |
| Dashboard | Grafana | Industry standard for operational dashboards |
| Quality scoring | LLM-as-judge (from your Capstone 6 framework) | Automated quality scores sampled from production traffic |
| Anomaly detection | Z-score or moving average with threshold alerts | Detect when metrics deviate from baseline |
| Log aggregation | Structured JSON logs → Grafana Loki | Search logs in context with traces |

**Alternative lightweight stack (if Docker orchestration is overwhelming):**
- SQLite for trace storage
- Streamlit dashboard instead of Grafana
- Same concepts, less infrastructure overhead

---

## Research Areas

- **Distributed tracing** — how to follow a request across multiple services and agents
- **OpenTelemetry** — the open standard for observability instrumentation
- **Site Reliability Engineering (SRE)** — Google's approach to production operations
- **The four golden signals** — latency, traffic, errors, saturation (Google SRE)
- **LLM-specific observability challenges** — why standard APM tools miss what matters for LLM systems
- **Sampling strategies** — you can't trace 100% of requests in production; how to sample intelligently

**Resources worth reading:**
- Google SRE Book (free online) — especially chapters on monitoring and alerting
- OpenTelemetry documentation — the concepts section, not just the how-to
- "Observability Engineering" (Majors, Fong-Jones, Miranda) — if you want to go deep
- LangSmith and LangFuse documentation — commercial tools doing what you're building, useful for reference

---

## The Four Layers of LLM Observability

Standard APM (Application Performance Monitoring) tools track request latency and error rates. That's necessary but not sufficient for LLM systems. You need four layers:

**Layer 1 — Infrastructure metrics** (standard APM)
Request rate, error rate, API latency, memory/CPU. Tools like Datadog or Prometheus handle this well.

**Layer 2 — LLM-specific metrics** (what standard APM misses)
Token counts per call, cost per call, model selection per call, prompt/completion token ratio, context window utilisation. These don't exist in standard APM — you instrument them.

**Layer 3 — Agent-level tracing** (what LLM frameworks miss)
Which agent called which tool? How long did each agent's reasoning take vs tool execution? What was the agent's input and output? These need custom instrumentation at the agent level.

**Layer 4 — Quality metrics** (what most observability misses entirely)
Is the output actually good? Cost and latency tell you nothing about quality. Sample 10% of production outputs, score them with LLM-as-judge, track the score distribution over time.

---

## Build Stages

### Part A — Instrumentation Layer
Build the wrapper that instruments your existing multi-agent system without modifying its core logic. Every LLM call must produce a span containing:
- `trace_id` (unique per user request)
- `span_id` (unique per agent call within the trace)
- `parent_span_id` (which agent spawned this one)
- `agent_name`
- `start_time`, `end_time`, `duration_ms`
- `input_tokens`, `output_tokens`, `estimated_cost_usd`
- `model_used`
- `tool_calls` (array of tool names called)
- `status` (success / error / timeout)

Start simple: a Python decorator that wraps every agent function and writes structured JSON to a file. This is the foundation everything else builds on.

### Part B — Trace Visualisation
Get traces into Jaeger or a SQLite-based viewer. Run your target system on 10 test queries. Open the trace viewer. Can you see the parent-child relationships? Can you identify which agent took the most time? Which was most expensive? If not, your instrumentation is incomplete.

### Part C — Cost Dashboard
Build the cost tracking dashboard. Show: cost per request (current session), cost by agent (which agent is most expensive?), cost trend over time (is cost per request stable?), daily cost projection.

This dashboard should be the first thing you open if you get a billing surprise.

### Part D — Quality Sampling
Sample 10% of production outputs and run them through your LLM-as-judge from Capstone 6. Store scores in the database. Add quality metrics to the dashboard. Run 50 queries through your target system to generate enough data for meaningful charts.

### Part E — Anomaly Detection
Build three alerts:
1. **Cost anomaly:** a single request costs more than 3× the p95 cost baseline
2. **Latency anomaly:** a single request takes more than 3× the p95 latency baseline
3. **Quality regression:** the 10-request rolling average quality score drops below a threshold

These don't need to be complex. A z-score calculation or a simple moving average with a threshold is sufficient.

### Part F — Dashboard Polish and Handoff
Build the "manager dashboard" — the one view that a non-engineer can look at every morning and know if the system is healthy. It shows: current quality score (green/amber/red), today's cost vs yesterday's, request volume, and any active alerts. No raw numbers — always contextualised ("+12% vs yesterday", "2 anomalies in the last hour").

---

## Completion Checklist

- [ ] Instrumentation layer: every LLM call produces a span with all required fields
- [ ] Trace visualisation: parent-child agent relationships visible in trace viewer
- [ ] Cost dashboard: cost per request, cost by agent, daily trend
- [ ] Latency dashboard: p50/p95/p99 per endpoint and per agent
- [ ] Quality sampling: 10% of outputs scored, trend visible in dashboard
- [ ] Cost anomaly detection working (test by injecting an expensive request)
- [ ] Latency anomaly detection working
- [ ] Quality regression detection working (test by degrading the system prompt)
- [ ] Manager dashboard: green/amber/red health view with contextualised numbers

---

## What Completing This Demonstrates

- You understand production engineering, not just building
- You can make an AI system's internals visible without modifying its behaviour
- You think about cost, latency, and quality as first-class constraints, not afterthoughts
- You can build infrastructure that makes the rest of the team's work better

This is what "engineering at scale" means — not necessarily large user counts, but the operational maturity to know when your system is healthy, when it isn't, and why.
