# Capstone 8 — Fine-Tuning vs Prompting Showdown

**XP:** 800  
**Difficulty:** Expert  
**Requires:** Levels 1–10, AWS GenAI Track Module 5 (LoRA/PEFT)  
**Estimated build time:** 4–6 days  
**Cost:** GPU compute for training (~$5–30 on RunPod or Lambda Labs) + API calls for comparison

---

## Why This Exists

Fine-tuning is the most misunderstood decision in AI engineering.

Most people reach for fine-tuning when a model doesn't perform well on their domain. That instinct is often wrong. A well-crafted prompt with good examples frequently outperforms a fine-tuned model — and costs a fraction of the time and money to build. Conversely, there are cases where no amount of prompting will get you there, and fine-tuning is the only path.

The decision between prompting and fine-tuning is one of the highest-leverage calls you will make as a GenAI lead. Getting it wrong wastes months and significant compute budget. Getting it right is what separates a thoughtful engineer from someone who just follows tutorials.

This capstone doesn't just teach you how to fine-tune. It teaches you when — and when not to — by forcing you to run the rigorous comparison yourself.

---

## What This Unlocks

**Roles:**
- ML Engineer / AI Engineer at companies with proprietary data
- GenAI Lead who can make the prompting vs fine-tuning decision defensibly
- Any role where the company wants to own a model tuned on their data
- Research roles at companies exploring frontier model customisation

**When fine-tuning is actually justified:**
- You need consistent formatting/structure that prompting can't reliably enforce
- You have thousands of high-quality labeled examples and the task is well-defined
- Latency is critical and you need a smaller, faster model at the same quality as a larger prompted one
- You have data the model has never seen (highly specialised domain knowledge)
- You want to distil a larger model's capability into a smaller one

**When prompting wins:**
- You have fewer than 500 good examples (fine-tuning will overfit)
- The task is diverse and open-ended
- You're iterating quickly — fine-tuning a new model every time requirements change is slow
- The base model already knows the domain (most things it does)

**What you can say:** "I ran a rigorous comparison of fine-tuning vs prompting on [specific task]. The fine-tuned model won on [X] but lost on [Y] at 10x the cost to produce. Here's the decision framework I use."

---

## The System

This capstone is structured as an experiment, not a product. You will:

1. Select a specific, well-defined task (see options below)
2. Build four systems to compare: base model, few-shot prompted, fine-tuned (LoRA), fine-tuned (QLoRA)
3. Build an eval suite that measures each system rigorously across the same test set
4. Run the comparison and produce a decision document: which approach wins, under what conditions, and why

**Recommended tasks (pick one):**

**Option A — Structured Extraction:** Extract structured information (entities, dates, amounts) from legal or financial documents. The model must return valid JSON every time.

**Option B — Domain Q&A:** Answer questions about a specialised domain (Australian medical regulations, Japanese tax law, specific industry documentation). The model must produce accurate answers only from the provided knowledge.

**Option C — Style Transfer:** Rewrite text in a specific voice (formal academic, plain English, marketing copy). The model must consistently match the target style.

---

## Technologies

| Component | Technology | Why |
|-----------|-----------|-----|
| Base model | Llama 3.1 8B (Meta) | Free, capable, small enough to fine-tune on accessible hardware |
| LoRA training | Hugging Face PEFT library | Parameter-Efficient Fine-Tuning — only trains adapter weights, not full model |
| QLoRA | bitsandbytes quantisation + PEFT | 4-bit quantised LoRA — enables training on GPU with 16GB VRAM |
| Training acceleration | Unsloth | 2x faster LoRA fine-tuning with lower memory usage |
| Experiment tracking | Weights & Biases (W&B) | Log training loss, eval metrics, compare runs |
| Eval framework | Your Capstone 6 framework | Use what you've already built |
| Inference | vLLM or Hugging Face pipeline | Serve the fine-tuned model for evaluation |

**Hardware needed:**
- LoRA on Llama 3.1 8B: 16GB VRAM minimum (NVIDIA RTX 4080 or A10G on RunPod)
- QLoRA on Llama 3.1 8B: 10GB VRAM (RTX 3080 or T4 on Google Colab)
- Training time: 1–3 hours for 1,000 examples, 3–8 hours for 10,000

---

## Research Areas

- **LoRA (Low-Rank Adaptation)** — how training low-rank matrices on top of frozen weights produces efficient fine-tuning
- **QLoRA** — combining quantisation with LoRA to reduce memory requirements
- **Catastrophic forgetting** — why fine-tuning on a specific task can degrade performance on everything else
- **Data quality vs quantity** — why 500 excellent examples outperform 5,000 mediocre ones
- **Overfitting in fine-tuning** — how to detect it and why it happens faster in LLMs than traditional ML
- **Knowledge distillation** — using a larger model to generate training data for fine-tuning a smaller one

**Papers worth reading:**
- "LoRA: Low-Rank Adaptation of Large Language Models" (Hu et al., 2021) — the foundational paper
- "QLoRA: Efficient Finetuning of Quantized LLMs" (Dettmers et al., 2023)
- "The False Promise of Imitating Proprietary LLMs" (Gudibande et al., 2023) — why fine-tuning on GPT outputs doesn't work as expected
- "LIMA: Less Is More for Alignment" (Zhou et al., 2023) — 1,000 examples can match 52,000 if quality is right

---

## Build Stages

### Part A — Dataset Construction
Before any model work: build your training dataset. 500–1,000 high-quality labeled examples for your chosen task. Quality requirements:
- Inputs are representative of real-world variation
- Outputs are definitively correct — no ambiguous examples
- No duplicates
- 80% train / 10% validation / 10% test split, done before any training

**The most common mistake:** using a large noisy dataset when a small clean one would be better. Read the LIMA paper before building your dataset.

### Part B — Baseline: Zero-Shot and Few-Shot Prompting
Before any fine-tuning: run the base model (Llama 3.1 8B) on your test set with zero-shot and few-shot (5-example) prompts. Measure performance using your eval framework. This is your baseline. Every subsequent comparison is relative to this.

### Part C — LoRA Fine-Tuning
Fine-tune Llama 3.1 8B with LoRA on your training dataset. Key decisions to log:
- Learning rate (start: 2e-4)
- LoRA rank (start: 16, experiment with 8 and 32)
- LoRA alpha (start: 32)
- Number of epochs (start: 3, watch for overfitting on validation loss)

Track training and validation loss in W&B. Stop training when validation loss stops improving (early stopping). Run on your test set. Compare against the prompting baseline.

### Part D — QLoRA Fine-Tuning
Repeat with QLoRA (4-bit quantisation). Compare: training speed, GPU memory usage, final model quality. QLoRA should produce a similar result to LoRA at lower memory cost.

### Part E — Rigorous Comparison
Run all four systems (zero-shot, few-shot, LoRA, QLoRA) through your eval framework. Measure:
- Task accuracy (the primary metric for your chosen task)
- Consistency (does it produce the same answer if you ask the same question twice?)
- General capability degradation (does fine-tuning make it worse at tasks outside the training domain?)
- Inference cost (fine-tuned models need hosting; prompting uses an API)
- Time to produce (how long did each approach take to build?)

### Part F — Decision Document
Write a 500-word decision document: Given this task and this dataset, which approach should you use and why? Include your data. Be specific about where fine-tuning wins, where prompting wins, and what the conditions are. This is the artefact you show in an interview.

---

## Completion Checklist

- [ ] Dataset: 500+ examples, clean, split 80/10/10 before training
- [ ] Baseline measured: zero-shot and few-shot on test set using eval framework
- [ ] LoRA fine-tune completed: training and validation loss tracked in W&B
- [ ] Early stopping implemented: training stopped when validation loss plateaued
- [ ] QLoRA fine-tune completed: GPU memory usage compared against LoRA
- [ ] All four systems run on identical test set
- [ ] General capability degradation measured (out-of-domain test)
- [ ] Inference cost and time-to-produce documented for each approach
- [ ] Decision document: 500 words, data-backed, conditions specified

---

## What Completing This Demonstrates

- You can fine-tune a real open-source model, not just call an API
- You understand LoRA and QLoRA at implementation level, not just concept level
- You have a data-backed framework for deciding when to fine-tune vs prompt
- You think about the full cost of a decision: compute, time, maintenance, quality

The person who can say "I ran this comparison, here's what the data showed, and here's the decision I'd make in your context" is trusted with architecture decisions. The person who defaults to "let's fine-tune it" or "prompting is always enough" is not.
