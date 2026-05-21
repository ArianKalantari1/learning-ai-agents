# Level 8 — Evaluation and Reliability

**Status:** Locked  
**XP:** 350  
**Unlocks:** Evals, observability, hallucination detection  
**Requires:** Level 7 complete

---

## What You'll Build

An eval suite for the calculator agent. Write 20 test cases with known correct answers. Run the agent against all 20 and measure:
1. Accuracy — did it get the right answer?
2. Tool call reliability — did it use the tool or answer from its own knowledge?
3. Latency — how long did each call take?
4. Token cost — how many tokens per question?

Add a guardrail that catches and flags hallucinated answers.

---

## Key Concepts

- What evals are and why they matter more than intuition-based testing
- How to measure tool call reliability (not just output correctness)
- What observability means — logging every tool call and decision
- How to detect hallucinations in tool-calling agents
- Why you run evals before every significant change to the agent

---

## Completion Checklist

1. What is the difference between a unit test and an eval?
2. How do you measure whether an agent used a tool vs answered from its own knowledge?
3. What is a hallucination guardrail and how do you implement one?
4. What does observability mean in the context of an agent system?
5. Why is latency an important eval metric for agents specifically?
6. What should trigger you to re-run evals?

---

## Resources

- [Anthropic evals guide](https://docs.anthropic.com/en/docs/test-and-evaluate)
- [Braintrust](https://www.braintrustdata.com/) — eval platform worth knowing
- [Building effective agents — Anthropic](https://www.anthropic.com/research/building-effective-agents)

---

## Your Build

Add your eval suite to the `builds/` folder. Include the 20 test cases, the runner script, and a results summary.

---

## Next

[Level 9 — Production Agents](../level-09-production/)
