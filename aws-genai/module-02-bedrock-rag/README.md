# Module 2 — Bedrock RAG

**Track:** AWS GenAI  
**Status:** Locked  
**XP:** 200  
**Unlocks:** Bedrock Knowledge Bases, managed RAG on AWS  
**Requires:** Module 1 complete

---

## What You'll Build

Build a RAG pipeline using Bedrock Knowledge Bases. Upload a set of documents to S3, create a Knowledge Base that indexes them, and query it via the Bedrock RetrieveAndGenerate API. Compare this managed approach against the manual ChromaDB pipeline from Level 5.

---

## What are Bedrock Knowledge Bases?

Bedrock Knowledge Bases is AWS's managed RAG service. Instead of building the chunking → embedding → vector store → retrieval pipeline yourself, AWS manages it for you.

You provide:
- A data source (S3 bucket with your documents)
- A vector store (Amazon OpenSearch Serverless, or others)
- An embedding model (Amazon Titan Embeddings or Cohere)

AWS handles:
- Document chunking and embedding
- Vector store management
- Retrieval at query time
- Optionally: generating a response using a foundation model (RetrieveAndGenerate)

---

## Key Concepts

- S3 as a document store — uploading and organising source documents
- The `CreateKnowledgeBase` and `StartIngestionJob` APIs
- The difference between `Retrieve` (returns chunks) and `RetrieveAndGenerate` (returns a full response)
- Chunking strategies in Bedrock — fixed size, semantic, hierarchical
- Vector store options: Amazon OpenSearch Serverless, Aurora pgvector, Pinecone, Redis
- Syncing the Knowledge Base when documents change

---

## Key Code Pattern

```python
import boto3

bedrock_agent_runtime = boto3.client('bedrock-agent-runtime', region_name='us-east-1')

response = bedrock_agent_runtime.retrieve_and_generate(
    input={'text': 'What were the key findings about patient outcomes?'},
    retrieveAndGenerateConfiguration={
        'type': 'KNOWLEDGE_BASE',
        'knowledgeBaseConfiguration': {
            'knowledgeBaseId': 'YOUR_KB_ID',
            'modelArn': 'arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-sonnet-4-5-20251001-v2:0'
        }
    }
)

print(response['output']['text'])
print(response['citations'])  # source chunks retrieved
```

---

## Completion Checklist

1. What is a Bedrock Knowledge Base and what does it manage for you vs what you still control?
2. What is an ingestion job and when do you need to run one?
3. What is the difference between the `Retrieve` and `RetrieveAndGenerate` APIs?
4. How do you update the Knowledge Base when your source documents change?
5. What are the vector store options and when would you choose each?
6. How does the managed RAG approach compare to building your own with ChromaDB? What do you gain and what do you lose?

---

## Resources

- [Bedrock Knowledge Bases documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html)
- [RetrieveAndGenerate API](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_RetrieveAndGenerate.html)
- [Amazon OpenSearch Serverless](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless.html)

---

## Your Build

Add your code to the `builds/` folder. Include the setup script (creating the Knowledge Base) and the query script separately.
