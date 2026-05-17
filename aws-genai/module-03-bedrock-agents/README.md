# Module 3 — Bedrock Agents

**Track:** AWS GenAI  
**Status:** Locked  
**XP:** 200  
**Unlocks:** Bedrock managed agent runtime  
**Requires:** Module 2 complete

---

## What You'll Build

Build and deploy a Bedrock Agent — AWS's managed agent runtime. The agent will have access to a custom action group (your tool definitions) backed by a Lambda function. Compare this managed approach against the hand-rolled agent loop you built in Levels 1-4.

---

## What are Bedrock Agents?

Bedrock Agents is AWS's managed orchestration layer for AI agents. Instead of writing your own agent loop, tool dispatch, and state management, AWS runs it for you.

You define:
- The agent's instructions (system prompt)
- Action groups (tools — defined as OpenAPI schemas)
- Lambda functions that back each action group
- Optionally: a Knowledge Base for RAG

AWS handles:
- The ReAct loop
- Tool calling and result injection
- Session management
- Tracing and observability

---

## Key Concepts

- Action groups — the Bedrock equivalent of tool definitions
- OpenAPI schema for defining tool inputs/outputs
- Lambda functions as the execution layer for actions
- The `InvokeAgent` API — starting and continuing agent sessions
- Session attributes — passing context between agent invocations
- Agent aliases and versions — deploying different versions of an agent
- Guardrails — AWS's built-in content filtering for agents

---

## Key Code Pattern

```python
import boto3

bedrock_agent_runtime = boto3.client('bedrock-agent-runtime', region_name='us-east-1')

response = bedrock_agent_runtime.invoke_agent(
    agentId='YOUR_AGENT_ID',
    agentAliasId='TSTALIASID',
    sessionId='user-session-123',
    inputText='What are the top three competitors for Atlassian?'
)

# Response comes as a streaming EventStream
for event in response['completion']:
    if 'chunk' in event:
        print(event['chunk']['bytes'].decode())
```

---

## Completion Checklist

1. What is a Bedrock Agent action group and how does it map to a tool in the manual approach?
2. How does Lambda connect to a Bedrock Agent action group?
3. What is an OpenAPI schema and why does Bedrock Agents require one?
4. What does session management in Bedrock Agents handle that you had to do manually before?
5. What are Bedrock Guardrails and when would you configure them?
6. What are the tradeoffs of using Bedrock Agents vs building your own agent loop?

---

## Resources

- [Bedrock Agents documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/agents.html)
- [InvokeAgent API](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html)
- [Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html)
- [Action groups with Lambda](https://docs.aws.amazon.com/bedrock/latest/userguide/agents-action-create.html)

---

## Your Build

Add your code to the `builds/` folder. Include the Lambda function, the OpenAPI schema, and the invocation script.
