# Capstone 9 — Knowledge Graph Builder

**XP:** 800  
**Difficulty:** Advanced  
**Requires:** Levels 1–8 (RAG, memory, multi-agent, evaluation)  
**Estimated build time:** 4–5 days  
**API cost:** ~$0.20–0.60 per document corpus (extraction passes)

---

## Why This Exists

Vector search answers questions like "what documents are about X?" Knowledge graphs answer questions like "how does X relate to Y, and what connects them?"

These are fundamentally different questions, and most RAG systems can only answer the first one. If you ask a standard RAG system "which researchers influenced this author's work, and who did those researchers collaborate with?" it retrieves relevant chunks and tries to synthesise an answer from context windows. It misses connections. It can't traverse a graph.

Knowledge graphs extract entities (people, organisations, concepts, events) and the relationships between them, then store that structure in a queryable form. Queries that require following chains of relationships — "what caused X?" "who connected A to B?" "what happened between these two events?" — require a graph, not a vector store.

The accuracy problem you identified with large vector stores is exactly what knowledge graphs solve. When you have 10,000 documents and semantic similarity is no longer discriminating enough, structured relationship extraction gives you the precision layer that vector search can't.

---

## What This Unlocks

**Roles:**
- Knowledge Engineering specialist — rare and increasingly valued
- AI Engineer at companies with complex document relationships (legal, biomedical, intelligence)
- Data Engineer who understands AI-powered ETL pipelines
- Any role at a company needing to make sense of large unstructured document archives

**Industries where this is immediately valuable:**
- **Biomedical research:** Drug interactions, gene networks, clinical trial relationships
- **Legal:** Case law relationships, precedent chains, contract party networks
- **Intelligence/journalism:** Entity relationship networks, event timelines
- **Finance:** Corporate ownership structures, supply chain dependencies
- **Any company with complex internal documentation:** "How does policy X relate to process Y?"

**What you can say:** "I built a pipeline that reads unstructured documents and extracts a queryable knowledge graph. Here's how I handled entity disambiguation, relationship extraction accuracy, and the precision improvement over pure vector search on complex relational queries."

---

## The System

Build a pipeline that:

1. Reads a corpus of unstructured documents
2. Extracts named entities (people, organisations, locations, concepts, events)
3. Extracts relationships between those entities from the text
4. Resolves duplicates (same entity mentioned with different names)
5. Stores the graph in Neo4j
6. Answers natural language questions by translating them to graph queries
7. Compares answer quality against a pure vector RAG baseline on relational questions

---

## Technologies

| Component | Technology | Why |
|-----------|-----------|-----|
| Named Entity Recognition | spaCy + LLM-based extraction | spaCy for speed on standard entities; LLM for domain-specific and relationship extraction |
| Graph database | Neo4j (local via Docker) | Industry standard for graph data, Cypher query language |
| Graph visualisation | pyvis or Neo4j Bloom | See the graph you're building — essential for debugging |
| Entity disambiguation | Fuzzy matching + LLM verification | "Apple Inc." and "Apple" and "AAPL" are the same entity |
| Graph querying | LLM → Cypher translation | Translate natural language to Cypher, execute, interpret results |
| Vector comparison | Your existing RAG setup | Compare graph query precision against vector retrieval on the same questions |

---

## Research Areas

- **Information Extraction (IE)** — the NLP field covering entity and relationship extraction from text
- **Entity Resolution / Deduplication** — how to know that two mentions refer to the same real-world entity
- **Knowledge Graph Completion** — inferring missing relationships from existing graph structure
- **Graph Neural Networks (GNNs)** — using neural networks that operate on graph structure directly
- **Ontology design** — how to define the types of entities and relationships in your graph schema

**Papers worth reading:**
- "REBEL: Relation Extraction By End-to-end Language generation" (Cabot & Navigli, 2021)
- "SROIE: Scanned Receipts OCR and Information Extraction" — practical IE benchmark
- "A Survey on Knowledge Graphs" (Hogan et al., 2021) — comprehensive overview
- "From Text to Knowledge: The Information Extraction Pipeline" — Stanford NLP course notes

---

## Agent Team

| Agent | Role |
|-------|------|
| Document Ingester | Reads documents, chunks by paragraph or section. Tags each chunk with source metadata (document ID, page, section). |
| Entity Extractor | For each chunk: identifies named entities and their types. Uses spaCy first (fast), LLM second for ambiguous or domain-specific entities. Returns: `{entity: str, type: str, context: str, confidence: float}` |
| Relationship Extractor | For each chunk: identifies relationships between entities found in that chunk. Returns: `{subject: str, predicate: str, object: str, source_chunk: str, confidence: float}` |
| Entity Resolver | Across all extracted entities: groups mentions of the same real-world entity. Uses fuzzy string matching + LLM verification for ambiguous cases. Produces a canonical entity list. |
| Graph Writer | Takes canonical entities and resolved relationships. Writes to Neo4j using the Cypher MERGE statement (creates if not exists, skips if duplicate). |
| Graph Query Agent | Receives natural language question. Translates to Cypher. Executes against Neo4j. Returns structured results. Handles translation failures (not every question is answerable by graph traversal). |
| Answer Synthesiser | Takes graph query results and synthesises a natural language answer. Does not invent facts — only interprets what the graph returned. |

---

## Build Stages

### Part A — Data and Schema Design
Before any code: define your domain and your graph schema. What types of entities exist? What types of relationships exist between them? This is your ontology.

Example for a corpus of academic papers:
- Entity types: Person, Institution, Paper, Concept, Dataset
- Relationship types: AUTHORED_BY, AFFILIATED_WITH, CITES, USES_DATASET, INTRODUCES_CONCEPT

Write this down. An ambiguous schema produces an ambiguous graph.

Choose a corpus: 50–100 documents in a domain you understand well enough to validate extraction quality.

### Part B — Entity Extraction Pipeline
Build the extractor on 10 documents. Evaluate: are the entities correct? What's being missed? What's being hallucinated? The LLM will sometimes invent entities that aren't in the text. Build validation: cross-reference every extracted entity against the source chunk — if the entity name doesn't appear in the text, flag it.

### Part C — Relationship Extraction
Build the relationship extractor. Harder than entity extraction — relationships are implicit, directional, and context-dependent. Test with 10 documents. Measure precision: what percentage of extracted relationships are actually correct? Below 70% precision means your extraction prompt needs significant rework before you build the graph.

### Part D — Entity Resolution
Run your extractor on the full corpus. Now handle duplicates: "John Smith", "J. Smith", "Smith (2019)" might all refer to the same person. Build the resolver. Start with exact matching, add fuzzy matching (Levenshtein distance), use LLM for ambiguous cases where fuzzy matching gives conflicting signals.

### Part E — Graph Construction and Visualisation
Write the resolved entities and relationships to Neo4j. Visualise using pyvis. Look at it. Does it make sense? Are there obvious errors (disconnected clusters that should be connected, suspicious hubs)? Graph visualisation is your primary debugging tool at this stage.

### Part F — Natural Language Querying
Build the query agent. The hard part: not every natural language question maps cleanly to a Cypher query. Build graceful failure: if the question can't be answered by graph traversal, say so and fall back to vector search rather than returning an empty result.

Test with 15 questions: 10 relational ("who collaborated with X?", "what papers cite Y?") and 5 that require the vector fallback ("what does this paper say about quantum computing?").

### Part G — Comparison with Vector RAG
Run the same 10 relational questions against a pure vector RAG system. Compare precision. The graph should win on relational questions. If it doesn't, investigate why — the likely culprits are poor relationship extraction or inadequate entity resolution.

---

## Completion Checklist

- [ ] Graph schema documented before coding (entity types, relationship types)
- [ ] Entity extractor: precision measured on 10-document sample
- [ ] Entity extractor: hallucination guard — flags entities not present in source text
- [ ] Relationship extractor: precision ≥70% on sample set before full corpus run
- [ ] Entity resolver: handles exact match, fuzzy match, and LLM disambiguation
- [ ] Graph in Neo4j: visualised and validated for obvious structural errors
- [ ] Query agent: Cypher translation working for 10 relational questions
- [ ] Query agent: graceful fallback to vector search for non-relational questions
- [ ] Comparison: graph vs vector RAG on 10 relational questions, precision documented

---

## What Completing This Demonstrates

- You understand the structural difference between vector search and graph traversal, and when each is appropriate
- You've solved the entity resolution problem — harder than it sounds, critical in practice
- You can build an information extraction pipeline that produces reliable structured output from messy text
- You understand graph databases and Cypher, a genuinely different paradigm from relational SQL or vector stores

This is a rare skill set. Most AI engineers can build RAG. Very few can build the knowledge extraction layer that makes RAG smarter on relational questions.
