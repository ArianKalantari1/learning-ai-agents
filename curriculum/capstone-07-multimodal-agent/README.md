# Capstone 7 — Multimodal Research Agent

**XP:** 750  
**Difficulty:** Advanced  
**Requires:** Levels 1–7, Capstone 1 (Research Intelligence Network)  
**Estimated build time:** 3–4 days  
**API cost:** ~$0.30–0.80 per complex query (vision calls are more expensive)

---

## Why This Exists

Real documents are not plain text.

A financial report has tables and charts. A research paper has figures and diagrams. A contract has scanned pages. A competitor's website has screenshots. A medical record has hand-written notes photographed on a phone.

The first generation of RAG systems treated everything as text. They either skipped images entirely or extracted broken text from PDFs and called it done. That era is over. Claude 3, GPT-4V, and Gemini can see. The architecture of AI systems needs to match.

This capstone extends the Research Intelligence Network (Capstone 1) with vision. It forces you to think about how to route different input types to the right model, how to extract structured information from images, and how to synthesise insights across modalities — a chart says something that the paragraph next to it doesn't, and a complete analysis needs both.

---

## What This Unlocks

**Roles:**
- Multimodal AI Engineer — one of the fastest-growing specialisations
- Document AI Engineer (legal tech, insurance, healthcare, finance)
- AI researcher at companies processing complex real-world documents
- Any role at companies with large unstructured document archives

**Industries where this matters immediately:**
- **Legal:** Contracts with exhibits, court documents with attachments
- **Finance:** Annual reports, investor presentations, charts
- **Healthcare:** Medical imaging (adjacent), scanned patient records
- **Real estate:** Property documents, floor plans, photos
- **Academic research:** Papers with figures and tables

**What you can say:** "I built a multimodal research agent that can analyse documents containing text, charts, tables, and images. Here's how I solved the routing problem and how I validated that vision outputs were accurate."

---

## The System

Extend Capstone 1 (Research Intelligence Network) to handle:

1. PDF documents with images, charts, and tables
2. Screenshots of websites or applications
3. Data visualisations (bar charts, line charts, scatter plots)
4. Documents with mixed content (text + figures on the same page)

The system must:
- Classify each input chunk by type (text / image / chart / table / mixed)
- Route each type to the appropriate processing agent
- Extract structured information from visual content, not just describe it
- Synthesise text and visual findings into a unified analysis
- Flag when a chart contradicts the accompanying text

---

## Technologies

| Component | Technology | Why |
|-----------|-----------|-----|
| PDF processing | PyMuPDF (fitz) | Extracts text and images from PDFs, page by page |
| Image classification | Claude Vision or CLIP embeddings | Route: is this a chart, a photo, a diagram, or a table? |
| Vision LLM | Claude 3.5 Sonnet (vision) or GPT-4V | Highest accuracy for chart interpretation and document understanding |
| Chart data extraction | Vision LLM + structured output | Extract the actual data from a chart, not just "this is a bar chart" |
| Table extraction | Camelot or tabula-py (for PDF tables) + Vision LLM fallback | Structured tables → pandas DataFrame |
| Multimodal embeddings | CLIP or Nomic Embed Vision | Embed images for semantic search alongside text |

---

## Research Areas

- **Multimodal learning** — how vision-language models are trained to understand both image and text jointly
- **Document Understanding** — the research field covering information extraction from complex documents
- **Chart-to-Data extraction** — converting visual charts back into structured numerical data
- **Optical Character Recognition (OCR)** — extracting text from images, why it's harder than it looks
- **Cross-modal alignment** — how to combine information from different modalities into a coherent representation

**Papers worth reading:**
- "LLaVA: Visual Instruction Tuning" (Liu et al., 2023) — multimodal instruction-following
- "DocVQA: A Dataset for VQA on Document Images" (Mathew et al., 2020) — document understanding benchmarks
- "ChartQA: A Benchmark for Question Answering about Charts" (Masry et al., 2022)
- "Nougat: Neural Optical Understanding for Academic Documents" (Blecher et al., 2023)

---

## Agent Team

| Agent | Role |
|-------|------|
| Document Ingester | Receives a document (PDF, image, URL). Extracts pages as images + raw text. Outputs a list of chunks with type tags: `{type: "text" | "image" | "chart" | "table" | "mixed", content: ..., page: int}` |
| Input Router | Classifies each chunk and routes to the appropriate specialist agent. Uses fast vision classification for image chunks. |
| Text Researcher | Handles pure text chunks. Same as Capstone 1 Researcher. |
| Vision Analyst | Handles photo/diagram chunks. Describes the visual content and extracts key information relevant to the research question. |
| Chart Reader | Specialised for data visualisations. Extracts the actual data values, axis labels, units, and trend. Returns structured data, not descriptions. |
| Table Extractor | Handles tabular data. Returns a structured representation (JSON or markdown table) that downstream agents can reason over. |
| Cross-Modal Synthesiser | Receives findings from all specialist agents. Identifies agreements and contradictions across modalities. ("The chart shows revenue declining, but the text says revenue grew 12% — this requires investigation.") |
| Output Agent | Formats the final report with citations that reference specific pages and content types. |

---

## Build Stages

### Part A — PDF Decomposition
Before any AI: get PyMuPDF extracting pages as images and text from a real PDF. Test with a financial report (complex tables + charts) and an academic paper (figures + equations). Verify: every page is accounted for, images are extracted at readable resolution, text extraction handles multi-column layouts.

### Part B — Input Routing
Build the classifier. For each extracted chunk, determine: is this primarily text, an image, a chart, or a table? Use Claude Vision with a classification prompt. Test with 20 sample chunks. Measure classification accuracy — you need to know where the router makes mistakes before building the full pipeline.

### Part C — Chart Reader
This is the hardest agent. Build it in isolation first. Give it 10 different charts (bar, line, pie, scatter) and ask it to extract the data. Measure accuracy against the actual values. A chart reader that hallucinates data points is worse than no chart reader — it produces confident wrong answers.

Structured output requirement: the Chart Reader must return a JSON object with axis labels, data series, and values. If it can't extract reliable data, it returns `{"extractable": false, "reason": "..."}` — not a hallucinated approximation.

### Part D — Full Pipeline Integration
Integrate all agents with the Capstone 1 base. Run a full analysis on a complex document: a company annual report. Does the synthesiser correctly identify where the charts and text agree? Where do they conflict?

### Part E — Cross-Modal Contradiction Detection
Build the contradiction detector explicitly. If the Vision Analyst's chart data conflicts with the Text Researcher's findings, the synthesiser must flag it rather than silently choosing one. Test with a document where you've deliberately introduced a contradiction.

### Part F — Evaluation
Build an eval suite with 10 multimodal questions across different document types. For each question, score: text accuracy, visual accuracy, synthesis quality (did it correctly combine both?), contradiction detection (if applicable). Compare against a text-only version of the same system.

---

## Completion Checklist

- [ ] PDF decomposition: text and images extracted, all pages accounted for
- [ ] Input router: classifies text/image/chart/table, accuracy tested on 20 samples
- [ ] Chart Reader: returns structured JSON, validated on 10 chart types
- [ ] Chart Reader: returns `extractable: false` when data can't be reliably extracted (no hallucination)
- [ ] Table Extractor: returns structured data for PDF tables
- [ ] Full pipeline: document → router → specialists → synthesiser → report working end-to-end
- [ ] Cross-modal contradiction detector: flags and reports conflicts between text and visuals
- [ ] Eval suite: 10 multimodal questions, compared against text-only baseline
- [ ] Reflection: where did the vision models fail? What document types break the pipeline?

---

## What Completing This Demonstrates

- You understand multimodal architecture — not just "I used a vision model" but how to route, extract, and synthesise across modalities
- You know the failure modes of vision models (hallucination in chart reading) and how to guard against them
- You can extend an existing system with new capabilities without breaking the core
- You understand real-world document complexity — the gap between clean text and actual documents

Documents are everywhere. Most AI systems treat them as text. The ones that don't have a significant competitive advantage. This capstone shows you know how to build them.
