# Module 1 — Bedrock Foundations

**Track:** AWS GenAI  
**Status:** Locked  
**XP:** 200  
**Unlocks:** AWS Bedrock, foundation models as a service

---

## What You'll Build

Make your first API call to Claude via AWS Bedrock instead of the Anthropic API directly. Replicate the Level 1 calculator agent using Bedrock as the inference layer. Compare the API structure, latency, and cost model between Bedrock and the direct Anthropic API.

---

## What is Bedrock?

AWS Bedrock is a managed service that gives you API access to foundation models from multiple providers — Anthropic (Claude), Meta (Llama), Mistral, Amazon (Titan), and others — through a single AWS API.

Why would you use Bedrock instead of the Anthropic API directly?
- **Enterprise compliance** — data stays within your AWS account and VPC
- **IAM integration** — access control through standard AWS identity management
- **Unified billing** — model costs on your AWS bill alongside other infrastructure
- **Multi-model access** — switch between providers without managing multiple API keys
- **AWS ecosystem** — native integration with S3, Lambda, CloudWatch, etc.

---

## Key Concepts

- How to call Bedrock via the `boto3` SDK (the AWS Python SDK)
- The `InvokeModel` vs `Converse` API — when to use each
- IAM roles and permissions for Bedrock access
- Model IDs in Bedrock — how to reference Claude vs other models
- Cross-region inference — why some models require specific regions
- On-demand vs provisioned throughput — the pricing model

---

## Key Code Pattern

```python
import boto3
import json

bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

response = bedrock.converse(
    modelId='anthropic.claude-sonnet-4-5-20251001-v2:0',
    messages=[
        {"role": "user", "content": [{"text": "What is 847 divided by 13?"}]}
    ],
    inferenceConfig={"maxTokens": 512}
)

print(response['output']['message']['content'][0]['text'])
```

The `Converse` API is the recommended approach — it provides a unified interface across all Bedrock models.

---

## Completion Checklist

1. What is AWS Bedrock and why would you use it instead of the Anthropic API directly?
2. What IAM permissions does a Lambda function need to call Bedrock?
3. What is the difference between the `InvokeModel` and `Converse` APIs?
4. How do you reference the Claude Sonnet model in a Bedrock API call?
5. What is cross-region inference and when do you need it?
6. How does the Bedrock pricing model differ from the Anthropic API pricing model?

---

## Resources

- [AWS Bedrock documentation](https://docs.aws.amazon.com/bedrock/)
- [Bedrock Converse API](https://docs.aws.amazon.com/bedrock/latest/userguide/conversation-inference.html)
- [boto3 Bedrock runtime client](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-runtime.html)
- [Bedrock supported models](https://docs.aws.amazon.com/bedrock/latest/userguide/models-supported.html)

---

## Your Build

Add your code to the `builds/` folder.
