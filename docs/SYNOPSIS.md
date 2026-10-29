# Project Synopsis

## Knowledge-Vault: An Agentic RAG-based Multi-Agent System for Automated Generation of Syllabus-Aligned Interactive Study Material

| | |
|---|---|
| **Project Type** | Major Project (10 Credits) |
| **Domain** | Generative AI, Natural Language Processing, AI Agents, Machine Learning |
| **Programme** | B.Tech (Computer Science & Engineering) |
| **Team Members** | 1. ________ (Roll No. ______)  2. ________ (Roll No. ______)  3. ________ (Roll No. ______)  4. ________ (Roll No. ______) |
| **Project Guide** | ________________ |
| **Session** | 2026–27 |

---

## 1. Abstract

University students spend a large share of their exam preparation time searching for reliable, syllabus-specific study material across textbooks, websites, videos and unofficial notes. Existing resources are either generic (not aligned to a particular university's syllabus), unverified, or static and uninteresting. Producing high-quality, exam-focused material by hand for every subject of every course of every university is not feasible.

**Knowledge-Vault** is an autonomous AI engine that takes only the *requirements* of a subject (university, course, semester, subject code and syllabus) as input, and on its own researches the internet, collects and ranks credible sources, and generates complete, exam-oriented study material in multiple formats: **interactive HTML e-books, print-ready PDF exam notebooks, flashcards and quizzes**. The system is built as an **Agentic Retrieval-Augmented Generation (RAG)** pipeline in which specialised agents (Planner, Researcher, Writer, Verifier and Renderer) collaborate like an editorial team. Every generated claim is grounded in retrieved sources and checked by a verification agent to reduce hallucination. An analyser of previous-year questions (PYQs) marks high-weightage topics automatically.

The engine will be evaluated against hand-crafted reference e-books on syllabus coverage, factual faithfulness, PYQ hit-rate, human preference, and time and cost per subject. Its output is delivered to students through a web application with free and paid content.

**Keywords:** Generative AI, Large Language Models, Retrieval-Augmented Generation, Multi-Agent Systems, Automated Content Generation, EdTech.

---

## 2. Introduction

Large Language Models (LLMs) can explain concepts, summarise text and write structured documents. Used on their own, however, they *hallucinate*: they state incorrect facts confidently and do not know the exact syllabus or exam pattern of a particular university. **Retrieval-Augmented Generation (RAG)** reduces this by first retrieving relevant documents and then generating text grounded in them. **AI Agents** extend LLMs further: they can plan, call tools (web search, page readers, code execution), and iteratively improve their own output.

Knowledge-Vault combines these three ideas into a single engine that turns a syllabus into a finished, verified, multi-format study pack. The first target is AKTU (Dr. A.P.J. Abdul Kalam Technical University) B.Tech students. The design is curriculum-agnostic, so it can be extended to any university and any programme (B.Tech, BCA, B.Sc, MBA, B.Pharm and others).

---

## 3. Problem Statement

1. Study material is **scattered** across textbooks, websites, YouTube and unofficial PDFs. Students waste time finding and filtering it.
2. Most resources are **not aligned** to a specific university's syllabus and exam pattern, so students cannot tell what is important for marks.
3. Free online notes are often **unverified** and contain errors. Plain LLM chatbots hallucinate.
4. Conventional material is **static and dull**, with no interactivity, self-testing or revision aids.
5. Creating high-quality, exam-focused material **manually takes days per subject**, which makes it impossible to cover every subject of every university.

**There is a need for an automated system that can produce accurate, syllabus-aligned, exam-focused and interactive study material for any curriculum, at scale and at low cost.**

---

## 4. Objectives

1. To design a **multi-agent Agentic-RAG engine** that accepts subject requirements and autonomously produces complete study material.
2. To build a **syllabus parser** that converts a syllabus document into a structured hierarchy of units, topics and subtopics.
3. To implement a **web research agent** that searches, extracts, de-duplicates and ranks credible sources for every topic.
4. To generate **exam-oriented content** (concepts, comparison tables, diagrams, step-by-step solved numericals and exam-format answers) grounded in the retrieved sources, with citations.
5. To implement a **verification agent** that detects unsupported claims, factual errors and missing syllabus topics.
6. To analyse **previous-year question papers** and automatically rank topics by exam importance (★).
7. To render one structured content source into **multiple formats**: interactive HTML e-book, A4 PDF exam notebook, flashcards and quizzes.
8. To **evaluate** generated material quantitatively against hand-crafted reference material.
9. To deliver the material through a **web application** with user accounts and a payment system for premium content.

---

## 5. Literature Survey (Summary)

| # | Work | Contribution | Relevance / Gap |
|---|---|---|---|
| 1 | Lewis et al., *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*, NeurIPS 2020 | Introduced RAG: retrieval + generation to ground LLM outputs | Foundation of our grounding approach; it answers questions but does not author long documents |
| 2 | Yao et al., *ReAct: Synergizing Reasoning and Acting in Language Models*, ICLR 2023 | LLMs that interleave reasoning with tool use | Basis of our research agent's search–read–reason loop |
| 3 | Shao et al., *STORM: Assisting in Writing Wikipedia-like Articles From Scratch with LLMs*, NAACL 2024 | Multi-perspective research followed by outline and long-article generation | Closest prior work; generic articles only, with no syllabus alignment, exam focus or multiple formats |
| 4 | Wu et al., *AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation*, 2023 | Framework for collaborating LLM agents | Inspires our Planner/Researcher/Writer/Verifier team design |
| 5 | Min et al., *FActScore: Fine-grained Atomic Evaluation of Factual Precision*, EMNLP 2023 | Breaks text into atomic claims and verifies each against sources | Basis of our Verifier agent and faithfulness metric |
| 6 | Es et al., *RAGAS: Automated Evaluation of Retrieval Augmented Generation*, 2023 | Reference-free RAG metrics (faithfulness, relevance) | Used in our evaluation framework |
| 7 | Zheng et al., *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena*, NeurIPS 2023 | Strong LLMs as evaluators of generated text | Used for rubric-based quality scoring |
| 8 | Gao et al., *Retrieval-Augmented Generation for Large Language Models: A Survey*, 2023 | Survey of naive, advanced and modular RAG | Guides chunking, re-ranking and retrieval design |
| 9 | Settles & Meeder, *A Trainable Spaced Repetition Model for Language Learning*, ACL 2016 | Half-life regression for spaced-repetition scheduling | Basis for flashcard revision scheduling |

**Research gap:** Existing systems either answer questions (RAG chatbots) or write generic articles (STORM). None of them autonomously produce **curriculum-aligned, exam-focused, verified, multi-format** study material for a specific university syllabus. Knowledge-Vault addresses this gap.

---

## 6. Proposed Methodology

### 6.1 System Architecture

```
            ┌──────────────────────────────────────────────┐
 INPUT ───► │ University · Course · Semester · Subject     │
            │ Syllabus (PDF/text) · optional PYQ papers    │
            └───────────────────────┬──────────────────────┘
                                    ▼
  [1] Planner Agent ── syllabus parsing → Units → Topics → Subtopics (JSON)
                                    ▼
  [2] Research Agent ── query generation → web search → page extraction
                        → de-duplication → source credibility ranking
                                    ▼
  [3] Knowledge Store ── chunking + embeddings → vector database
                                    ▼
  [4] PYQ Analyser ── question extraction → embedding clustering
                        → topic frequency → ★ importance score
                                    ▼
  [5] Writer Agent ── retrieval per topic → grounded generation with citations:
                        concepts, tables, diagrams (Mermaid/SVG),
                        solved numericals, 2/7/10-mark answers
                                    ▼
  [6] Verifier Agent ── atomic claim checking vs sources, numerical
                        re-computation, syllabus coverage check
                        → feedback loop to Writer until it passes
                                    ▼
  [7] Structured Content (JSON schema), the single source of truth
                                    ▼
  [8] Renderers ──► Interactive HTML E-book │ A4 PDF Notebook │
                    Flashcards │ Quizzes / MCQs
                                    ▼
  [9] Web App ── auth · library · reader · payments · progress
```

### 6.2 Module Description

1. **Planner Agent:** Uses an LLM with structured (JSON-schema) output to convert the syllabus into a topic tree, and plans the depth and format required for each topic.
2. **Research Agent:** For each topic, generates diverse search queries, calls a web search API, extracts clean text from pages, removes duplicates, and scores each source (domain trust, relevance, recency).
3. **Knowledge Store:** Splits sources into chunks, embeds them with a sentence-embedding model, and stores them in a vector database for semantic retrieval with re-ranking.
4. **PYQ Analyser:** Extracts questions from past papers (with OCR if scanned), clusters semantically similar questions, maps clusters to syllabus topics, and computes an importance score from frequency and marks.
5. **Writer Agent:** Retrieves the top-ranked chunks for each topic and writes original, exam-oriented content in the target style. Hand-crafted reference e-books act as few-shot style examples. Every factual paragraph carries source citations.
6. **Verifier Agent:** Splits generated text into atomic claims and checks each against the retrieved evidence (FActScore-style). It re-computes numericals with code execution and checks that every syllabus topic is covered. Failing sections go back to the Writer.
7. **Renderers:** Template engines (Jinja2 + HTML/CSS/JS, WeasyPrint for PDF) turn the JSON content into an interactive e-book, a two-column print-ready PDF notebook, flashcard decks and quizzes.
8. **Web Application:** Students choose university → course → semester → subject and read, revise and test themselves. Premium content is unlocked through an integrated payment gateway (Razorpay).

### 6.3 Evaluation Plan

| Metric | Method |
|---|---|
| **Syllabus Coverage (%)** | Share of syllabus topics present in the generated material |
| **Faithfulness (%)** | Share of atomic claims supported by the cited sources (FActScore / RAGAS) |
| **Numerical Accuracy (%)** | Solved numericals checked against verified solutions |
| **PYQ Hit-Rate (%)** | Share of a held-out exam paper's questions covered by the material |
| **Human Preference** | Blind comparison by students and faculty: generated vs hand-crafted e-books (5-point rubric) |
| **Efficiency** | Generation time and API cost (₹) per subject |
| **Ablation Study** | Plain LLM vs RAG vs Agentic RAG with verifier, to show the contribution of each component |

---

## 7. Tools and Technologies

| Category | Technology |
|---|---|
| Programming | Python 3.11, TypeScript |
| LLM | Claude API (with option to switch to other LLM providers or open-source models) |
| Agent Orchestration | Custom agent loop / LangGraph |
| Web Search & Extraction | Search API (Tavily / Brave / Serper), trafilatura, BeautifulSoup |
| Embeddings & Vector DB | Sentence-Transformers, pgvector / ChromaDB |
| ML / Analysis | scikit-learn (clustering), NumPy, Pandas |
| OCR | Tesseract / PaddleOCR (scanned PYQ papers) |
| Rendering | Jinja2, HTML/CSS/JavaScript, WeasyPrint (PDF), Mermaid (diagrams) |
| Backend | FastAPI |
| Frontend | Next.js, Tailwind CSS |
| Database & Auth | PostgreSQL (Supabase) |
| Payments | Razorpay |
| DevOps | Git/GitHub, Docker, GitHub Actions, Vercel |

**Hardware:** Standard laptop (8 GB+ RAM); no GPU required because LLM inference runs through an API.

---

## 8. Expected Outcomes

1. A working **Knowledge-Vault Engine** that generates a complete subject study pack from requirements alone.
2. Generated material in **four formats**: interactive e-book, PDF exam notebook, flashcards and quizzes.
3. A **verified content library** for at least one full semester of AKTU B.Tech CSE (5+ subjects) as a pilot.
4. A deployed **web application** with student accounts and payments for premium content.
5. A **quantitative evaluation report** comparing the engine against hand-crafted material and simpler baselines.
6. A research paper / project report documenting the system and results.

---

## 9. Applications and Future Scope

- Expansion to **any university, course and language** (including Hindi and other regional-language editions).
- **AI Tutor:** RAG chatbot answering doubts from the generated book, with page citations.
- **AI Answer Checker:** grading photographed handwritten answers against marking rubrics.
- **Personalised revision** using spaced repetition and weak-topic prediction.
- **B2B use:** coaching institutes and colleges generating material for their own courses.
- Android app and offline mode.

---

## 10. Project Timeline

| Phase | Duration | Work |
|---|---|---|
| 1 | Weeks 1–2 | Requirement analysis, literature survey, content schema design |
| 2 | Weeks 3–5 | Planner + Research agents, knowledge store |
| 3 | Weeks 6–8 | Writer agent, PDF notebook renderer, first full subject generated |
| 4 | Weeks 9–10 | Verifier agent, interactive e-book, flashcard and quiz renderers |
| 5 | Weeks 11–12 | PYQ analyser, evaluation framework, ablation experiments |
| 6 | Weeks 13–14 | Web application, payment integration, deployment |
| 7 | Weeks 15–16 | Pilot with real students, results, report and presentation |

---

## 11. References

1. P. Lewis et al., "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks," *NeurIPS*, 2020.
2. S. Yao et al., "ReAct: Synergizing Reasoning and Acting in Language Models," *ICLR*, 2023.
3. Y. Shao et al., "Assisting in Writing Wikipedia-like Articles From Scratch with Large Language Models (STORM)," *NAACL*, 2024.
4. Q. Wu et al., "AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation," *arXiv:2308.08155*, 2023.
5. S. Min et al., "FActScore: Fine-grained Atomic Evaluation of Factual Precision in Long Form Text Generation," *EMNLP*, 2023.
6. S. Es et al., "RAGAS: Automated Evaluation of Retrieval Augmented Generation," *arXiv:2309.15217*, 2023.
7. L. Zheng et al., "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena," *NeurIPS*, 2023.
8. Y. Gao et al., "Retrieval-Augmented Generation for Large Language Models: A Survey," *arXiv:2312.10997*, 2023.
9. B. Settles and B. Meeder, "A Trainable Spaced Repetition Model for Language Learning," *ACL*, 2016.
