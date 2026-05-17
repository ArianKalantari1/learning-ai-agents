# Module 5 — SageMaker Fine-Tuning

**Track:** AWS GenAI  
**Status:** Locked  
**XP:** 200  
**Unlocks:** Fine-tuning with LoRA/PEFT on AWS  
**Requires:** Module 4 complete

---

## What You'll Build

Fine-tune a small open-source model (Mistral 7B or Llama 3 8B) using LoRA on SageMaker. Use a domain-specific dataset (medical, legal, or code — your choice). Evaluate the fine-tuned model against the base model on 10 held-out examples. Deploy the fine-tuned model to an endpoint.

---

## What is Fine-Tuning and Why Does LoRA Matter?

Full fine-tuning updates all model weights. For a 7B parameter model, that means updating 7 billion floating point numbers — requires massive GPU memory and compute.

LoRA (Low-Rank Adaptation) updates only a tiny fraction of the weights — typically 0.1–1% of total parameters — by inserting small adapter matrices into the attention layers. The base model is kept frozen.

This means:
- Fine-tuning a 7B model on a single A10G GPU (SageMaker ml.g5.2xlarge) instead of a cluster
- Training time of hours instead of days
- The base model's general capabilities are preserved
- Multiple LoRA adapters can be swapped in/out for different domains

---

## Key Concepts

- LoRA hyperparameters: `r` (rank), `alpha`, `dropout`, `target_modules`
- The training data format for instruction fine-tuning — prompt/completion pairs
- SageMaker training jobs — how they differ from notebook-based training
- S3 for training data and model artifacts
- PEFT library from Hugging Face — the standard LoRA implementation
- Quantisation (QLoRA) — reducing memory requirements further with 4-bit weights
- Merging LoRA weights back into the base model for deployment

---

## Key Code Pattern

```python
from sagemaker.huggingface import HuggingFace
import sagemaker

role = sagemaker.get_execution_role()

# Training script handles the LoRA setup
hf_estimator = HuggingFace(
    entry_point='train.py',          # your training script
    source_dir='./scripts',
    role=role,
    instance_type='ml.g5.2xlarge',   # A10G GPU — enough for 7B with LoRA
    instance_count=1,
    transformers_version='4.37',
    pytorch_version='2.1',
    py_version='py310',
    hyperparameters={
        'model_id': 'mistralai/Mistral-7B-Instruct-v0.2',
        'lora_r': 16,
        'lora_alpha': 32,
        'epochs': 3,
        'per_device_train_batch_size': 4
    }
)

hf_estimator.fit({'training': 's3://your-bucket/training-data/'})
```

---

## Completion Checklist

1. What is LoRA and why does it work with far less compute than full fine-tuning?
2. What do the `r` and `alpha` hyperparameters in LoRA control?
3. What format does your training data need to be in for instruction fine-tuning?
4. How does a SageMaker training job differ from running training code in a notebook?
5. What is QLoRA and when would you choose it over standard LoRA?
6. After training, how do you evaluate whether the fine-tuned model is actually better?

---

## Resources

- [PEFT library — Hugging Face](https://huggingface.co/docs/peft)
- [LoRA paper (Hu et al., 2021)](https://arxiv.org/abs/2106.09685)
- [SageMaker training jobs](https://docs.aws.amazon.com/sagemaker/latest/dg/train-model.html)
- [QLoRA paper (Dettmers et al., 2023)](https://arxiv.org/abs/2305.14314)

---

## Your Build

Add your training script, dataset, and evaluation results to the `builds/` folder. Include a brief write-up of what the fine-tune improved and what it didn't.
