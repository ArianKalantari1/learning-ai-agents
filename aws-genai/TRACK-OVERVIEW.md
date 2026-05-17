# AWS GenAI Track

A parallel track covering AWS tools for building and deploying AI systems in production.

This track is independent of the core 10-level curriculum but complements it directly. Pick it up once you're comfortable with Level 3+ — the core agent concepts will make the AWS abstractions much easier to understand.

**Total XP:** 1,200 (6 modules × 200 XP)

---

## Why This Track

The core curriculum teaches you to build AI agents. This track teaches you to deploy them on infrastructure that enterprises actually use. AWS has the largest market share in cloud AI/ML and hiring managers in Australia and globally expect familiarity with Bedrock or SageMaker for most senior AI engineering roles.

The two tracks map to each other directly:

| Core Curriculum | AWS Equivalent |
|----------------|----------------|
| Anthropic API direct | Bedrock — Anthropic models via AWS |
| RAG with ChromaDB | Bedrock Knowledge Bases |
| Tool-calling agents | Bedrock Agents |
| Custom fine-tuning | SageMaker fine-tuning |
| FastAPI deployment | SageMaker endpoints + API Gateway |
| Eval suite | SageMaker Clarify + CloudWatch |

---

## Module Map

| # | Module | XP | Status |
|---|--------|----|--------|
| 1 | [Bedrock Foundations](module-01-bedrock-foundations/) — Foundation models as a service | 200 | Locked |
| 2 | [Bedrock RAG](module-02-bedrock-rag/) — Knowledge Bases | 200 | Locked |
| 3 | [Bedrock Agents](module-03-bedrock-agents/) — Managed agent runtime | 200 | Locked |
| 4 | [SageMaker Basics](module-04-sagemaker-basics/) — Training and inference | 200 | Locked |
| 5 | [SageMaker Fine-Tuning](module-05-sagemaker-fine-tuning/) — LoRA and PEFT | 200 | Locked |
| 6 | [Production MLOps](module-06-production-mlops/) — Pipelines and monitoring | 200 | Locked |

---

## How to Use This Track

1. You need an AWS account. Free tier covers most of the learning here if you're careful about cleaning up resources.
2. Set up AWS CLI and configure credentials before starting Module 1.
3. Each module has a build project. Do the build, not just the reading.
4. Clean up AWS resources after each module to avoid unexpected charges.
5. Log your progress in [JOURNAL.md](../JOURNAL.md) and [ACHIEVEMENTS.md](../ACHIEVEMENTS.md).

---

## Cost Awareness

AWS resources cost real money. For this track:
- Bedrock API calls: charged per token, similar to Anthropic API
- SageMaker training: charged by instance-hour — use the smallest instance that works
- SageMaker endpoints: charged while running — **delete endpoints when done**
- Bedrock Knowledge Bases: storage costs — delete when done with module

Estimated cost to complete the full track with careful resource management: AUD $20–50.
