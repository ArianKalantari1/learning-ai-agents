# Module 4 — SageMaker Basics

**Track:** AWS GenAI  
**Status:** Locked  
**XP:** 200  
**Unlocks:** AWS SageMaker, training and inference  
**Requires:** Module 3 complete (or Level 5 of core curriculum)

---

## What You'll Build

Deploy an open-source model (Llama or Mistral from Hugging Face) to a SageMaker real-time inference endpoint. Call it via the SageMaker runtime API. Then deploy the same model using SageMaker Jumpstart to compare the managed vs manual approach.

---

## What is SageMaker?

AWS SageMaker is the full-stack ML platform. Where Bedrock gives you managed access to foundation models you don't modify, SageMaker is for when you need to:
- Train or fine-tune your own models
- Deploy open-source models you host yourself
- Build custom training pipelines
- Run batch inference at scale
- Manage the full ML lifecycle

**Bedrock vs SageMaker:**

| Use Case | Bedrock | SageMaker |
|----------|---------|----------|
| Call Claude, Llama, etc. via API | Yes | Not directly |
| Deploy your own trained model | No | Yes |
| Fine-tune a model | Limited | Full control |
| Run custom training code | No | Yes |
| Batch inference on large datasets | Limited | Yes |

---

## Key Concepts

- SageMaker inference endpoints — real-time vs async vs batch
- Hugging Face integration — deploying models from the Hub
- Instance types for inference — ml.g5 (GPU), ml.m5 (CPU)
- SageMaker Jumpstart — pre-built model deployments with one click
- The `sagemaker` Python SDK vs `boto3` — when to use each
- Endpoint auto-scaling — handling variable traffic
- Deleting endpoints — critical for cost management

---

## Key Code Pattern

```python
from sagemaker.huggingface import HuggingFaceModel
import sagemaker

role = sagemaker.get_execution_role()

hf_model = HuggingFaceModel(
    model_data=None,  # pull from Hub
    role=role,
    transformers_version='4.37',
    pytorch_version='2.1',
    py_version='py310',
    env={
        'HF_MODEL_ID': 'mistralai/Mistral-7B-Instruct-v0.2',
        'HF_TASK': 'text-generation'
    }
)

predictor = hf_model.deploy(
    initial_instance_count=1,
    instance_type='ml.g5.2xlarge'
)

response = predictor.predict({'inputs': 'Explain RAG in one paragraph.'})

# IMPORTANT: delete when done
predictor.delete_endpoint()
```

---

## Completion Checklist

1. What is the difference between a real-time endpoint, an async endpoint, and batch transform?
2. How do you choose the right instance type for a 7B parameter model?
3. What is SageMaker Jumpstart and when would you use it vs deploying manually?
4. What does the `sagemaker` SDK handle that `boto3` alone cannot?
5. How does auto-scaling work for SageMaker endpoints and why do you need it?
6. What happens to your AWS bill if you forget to delete a SageMaker endpoint?

---

## Resources

- [SageMaker documentation](https://docs.aws.amazon.com/sagemaker/)
- [SageMaker Python SDK](https://sagemaker.readthedocs.io/)
- [Hugging Face on SageMaker](https://huggingface.co/docs/sagemaker/index)
- [SageMaker Jumpstart](https://docs.aws.amazon.com/sagemaker/latest/dg/studio-jumpstart.html)

---

## Your Build

Add your code to the `builds/` folder. Include an endpoint cleanup script — run it after testing.
