# Module 6 — Production MLOps

**Track:** AWS GenAI  
**Status:** Locked  
**XP:** 200  
**Unlocks:** MLOps, deployment pipelines, monitoring  
**Requires:** Module 5 complete

---

## What You'll Build

Build a full ML pipeline using SageMaker Pipelines that automates: data validation → training → evaluation → model registration → deployment. Add CloudWatch monitoring to track latency, error rates, and model quality drift. Set up alerts that trigger when the model degrades.

---

## What is MLOps?

MLOps is the practice of applying software engineering discipline to machine learning — version control, CI/CD, testing, monitoring, and automated deployment for models instead of just code.

Without MLOps:
- Model training is manual and hard to reproduce
- Deployment is ad-hoc and risky
- Model degradation goes undetected
- No audit trail of what model version is in production

With MLOps:
- Training is automated and reproducible
- Deployment is gated by quality checks
- Production is monitored continuously
- Every model version is tracked

---

## Key Concepts

- SageMaker Pipelines — defining ML workflows as DAGs
- Pipeline steps: Processing, Training, Evaluation, RegisterModel, CreateModel
- Model Registry — versioning models and controlling promotion to production
- A/B testing with SageMaker production variants — sending a percentage of traffic to a new model
- CloudWatch metrics for SageMaker endpoints — InvocationsPerInstance, ModelLatency, 5XXError
- SageMaker Model Monitor — detecting data drift and model quality degradation
- EventBridge — triggering pipeline runs on schedule or on S3 data arrival

---

## Key Code Pattern

```python
from sagemaker.workflow.pipeline import Pipeline
from sagemaker.workflow.steps import TrainingStep, ProcessingStep
from sagemaker.workflow.model_step import ModelStep

# Define steps
preprocessing_step = ProcessingStep(
    name='PreprocessData',
    processor=sklearn_processor,
    inputs=[...],
    outputs=[...]
)

training_step = TrainingStep(
    name='TrainModel',
    estimator=hf_estimator,
    inputs={'training': preprocessing_step.properties.ProcessingOutputConfig...}
)

# Assemble pipeline
pipeline = Pipeline(
    name='GenAIModelPipeline',
    steps=[preprocessing_step, training_step, ...],
    sagemaker_session=sagemaker_session
)

pipeline.upsert(role_arn=role)
pipeline.start()
```

---

## Completion Checklist

1. What is a SageMaker Pipeline and why is it better than a notebook for production training?
2. What is the SageMaker Model Registry and what problem does it solve?
3. How do production variants work and why would you use them for a model rollout?
4. What is model drift and how does SageMaker Model Monitor detect it?
5. How would you automatically retrain a model when new data arrives in S3?
6. What metrics would you put on a CloudWatch dashboard for a production LLM endpoint?

---

## Resources

- [SageMaker Pipelines](https://docs.aws.amazon.com/sagemaker/latest/dg/pipelines.html)
- [SageMaker Model Registry](https://docs.aws.amazon.com/sagemaker/latest/dg/model-registry.html)
- [SageMaker Model Monitor](https://docs.aws.amazon.com/sagemaker/latest/dg/model-monitor.html)
- [CloudWatch metrics for SageMaker](https://docs.aws.amazon.com/sagemaker/latest/dg/monitoring-cloudwatch.html)

---

## Your Build

Add your pipeline definition, monitoring configuration, and a CloudWatch dashboard screenshot to the `builds/` folder.

---

## Track Complete

If you've completed all 6 modules: update your AWS XP to 1,200 in [README.md](../../README.md), log the date in [ACHIEVEMENTS.md](../../ACHIEVEMENTS.md), and write a reflection in [JOURNAL.md](../../JOURNAL.md).

You now have practical experience with the full AWS AI/ML stack — from calling foundation models to deploying and monitoring production pipelines.
