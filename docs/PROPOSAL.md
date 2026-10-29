# Project Proposal

## Knowledge-Vault
### An Agentic RAG-based Multi-Agent System for Automated Generation of Syllabus-Aligned Interactive Study Material

| | |
|---|---|
| **Submitted by** | ________ , ________ , ________ , ________ |
| **Programme / Semester** | B.Tech CSE, ____ Semester |
| **Project Guide** | ________________ |
| **Department** | Computer Science & Engineering, ________________ |
| **Date** | ____ / ____ / 2026 |

---

## 1. Executive Summary

Knowledge-Vault is an AI engine that **writes the study material for any syllabus by itself**. A user enters only the requirements: university, course, semester, subject and syllabus. A team of AI agents then researches the internet, gathers and verifies credible sources, and produces a complete, exam-oriented study pack:

- 📘 **Interactive E-book** (HTML): visual explanations, expandable Q&A, diagrams, quizzes
- 📄 **Exam Notebook** (print-ready A4 PDF): dense revision notes, ★ important topics, step-by-step solved numericals
- 🃏 **Flashcards**: spaced-repetition revision
- ✅ **Quizzes / MCQs**: self-assessment

The team has already produced reference material by hand (interactive e-books for BCS402, BCS502, BCS503, BIT601 and BCS055, and a 5th-semester AKTU exam notebook). These prove the format and act as the **gold standard** that the engine must learn to match automatically, at scale, for every subject of every university.

The generated material is delivered to students through a market-ready **web application** with free previews and low-cost paid content.

---

## 2. Background and Motivation

**The student's problem.** Before an exam, a typical university student:
1. searches the syllabus on the university website,
2. hunts for notes on Google, YouTube, Telegram and WhatsApp groups,
3. cannot tell which notes are correct or which topics carry marks,
4. ends up studying from scattered, unverified, uninteresting material.

**The content creator's problem.** Making one high-quality, exam-focused subject book by hand takes **days**. A single university such as AKTU offers dozens of programmes, each with 40+ subjects across 8 semesters. Covering one university by hand is impractical, and covering every university is impossible.

**The technology opportunity.** LLMs can now write fluent explanations, RAG can ground them in real sources, and AI agents can plan and use tools such as web search. Combined carefully, with verification, they can do the work of a whole editorial team in minutes.

---

## 3. Problem Statement

> *To design and build an autonomous AI system that, given only the requirements of a university subject, researches credible sources on the internet and generates accurate, syllabus-aligned, exam-focused study material in multiple interactive formats, and to deliver it to students through a commercially operational application.*

---

## 4. Objectives

| # | Objective | Measurable Target |
|---|---|---|
| O1 | Build a multi-agent Agentic-RAG content engine | End-to-end generation from requirements to study pack |
| O2 | Syllabus parsing into a structured topic tree | ≥ 95% of syllabus topics correctly extracted |
| O3 | Autonomous web research with source ranking | ≥ 5 credible sources per topic |
| O4 | Grounded, exam-oriented content generation | ≥ 90% syllabus coverage |
| O5 | Automated fact verification | ≥ 90% faithfulness (claims supported by sources) |
| O6 | PYQ-based topic importance (★) | ≥ 70% PYQ hit-rate on a held-out exam paper |
| O7 | Multi-format rendering from one content source | E-book, PDF, flashcards and quiz from the same JSON |
| O8 | Efficiency | One complete subject in < 30 minutes at low API cost |
| O9 | Market-ready delivery | Deployed web app with auth, library and payments |

*Targets are planned goals to be validated in the evaluation phase.*

---

## 5. Scope

**In scope**
- The Knowledge-Vault Engine (all agents, knowledge store, verifier, renderers)
- A PYQ analyser for topic importance
- A pilot content library: AKTU B.Tech CSE, at least one full semester
- A web application: sign-up and login, university/course/semester selection, library, e-book reader, PDF viewer, flashcards, quizzes, progress tracking
- Payment integration (Razorpay) for paid subjects and semester bundles, plus an admin panel
- An evaluation framework and experimental results

**Out of scope for this project (future work)**
- Native iOS app
- Video content generation
- Full coverage of every university (the architecture supports it; the pilot covers one)

---

## 6. Proposed Solution

### 6.1 How It Works: An AI Editorial Team

| Agent | Human equivalent | Responsibility |
|---|---|---|
| **Planner** | Chief Editor | Reads the syllabus, builds the unit/topic plan, decides depth and format per topic |
| **Researcher** | Research Assistant | Searches the web, reads pages, filters and ranks credible sources (RAG *retrieval*) |
| **PYQ Analyser** | Senior Teacher | Studies past papers and marks topics that carry the most marks (★) |
| **Writer** | Author | Writes concepts, tables, diagrams, solved numericals and exam-format answers from the sources (RAG *generation*) |
| **Verifier** | Proof-reader / Fact-checker | Checks every claim against its source, re-solves numericals, flags missing topics, and returns faulty sections for rewriting |
| **Renderer** | Designer / Publisher | Turns verified content into the e-book, PDF notebook, flashcards and quizzes |

The **LLM** is the brain of each agent, **RAG** keeps the content factual, and the **agents** together form the **engine**.

### 6.2 Architecture

```
 Requirements ─► Planner ─► Researcher ─► Knowledge Store (vector DB)
                    │                              │
                    └──► PYQ Analyser ──────────┐   │
                                               ▼   ▼
                                     Writer Agent ◄──┐
                                          │          │ feedback
                                          ▼          │
                                     Verifier Agent ─┘
                                          │ (passes)
                                          ▼
                              Structured Content (JSON)
                                          │
                ┌──────────────┬──────────┴──────┬──────────────┐
                ▼              ▼                 ▼              ▼
         Interactive      PDF Exam          Flashcards       Quizzes
           E-book         Notebook
                └──────────────┴────────┬────────┴──────────────┘
                                        ▼
                     Web App (Library · Reader · Payments)
```

### 6.3 Key Design Decisions

1. **One content schema, many formats.** Content is generated once as structured JSON (units → topics → blocks such as concept, table, diagram, numerical, Q&A, flashcard, MCQ) and then rendered into every format. This guarantees consistency and saves cost.
2. **Grounding over guessing.** The Writer may only use retrieved evidence and must cite it. This is the main defence against hallucination.
3. **Verify, then publish.** No section is published until the Verifier passes it. Numericals are re-computed with code.
4. **Original writing, cited sources.** Sources are used for understanding and citation, never copied verbatim, which avoids copyright problems.
5. **Model-agnostic.** The LLM provider can be swapped (Claude, other APIs or open-source models) to balance quality and cost.
6. **Human-in-the-loop.** An admin review step before publishing paid content.

---

## 7. Novelty and Contribution

| Existing approach | Limitation | Knowledge-Vault |
|---|---|---|
| Textbooks / guide books | Generic, static, expensive, slow to update | Syllabus-exact, interactive, low-cost, regenerated on demand |
| Free online notes | Unverified, scattered, not exam-focused | Verified with citations, ★ exam importance |
| ChatGPT-style chatbots | Answer one question at a time, hallucinate, unaware of syllabus | Produces the complete book, grounded and verified |
| RAG chatbots (common projects) | Only answer questions over given documents | Autonomously researches *and authors* full multi-format material |
| STORM (Stanford, 2024) | Generic Wikipedia-style articles | Curriculum-aligned, exam-oriented, multi-format, PYQ-aware |

**Contributions:**
1. A multi-agent Agentic-RAG pipeline for **curriculum-aligned** long-form educational content.
2. A **verification loop** that combines claim-level fact checking with numerical re-computation.
3. A **PYQ-driven importance model** for exam-focused prioritisation.
4. A **single-source, multi-format** content schema and rendering system.
5. An **evaluation benchmark** comparing AI-generated material with expert hand-crafted material.

---

## 8. Methodology and Work Plan

| Phase | Weeks | Deliverables | Owner |
|---|---|---|---|
| 1. Research & Design | 1–2 | Literature survey, content JSON schema, architecture document | All |
| 2. Planner + Research Agents | 3–5 | Syllabus parser, web research pipeline, vector knowledge store | Member 1 |
| 3. Writer + PDF Renderer | 6–8 | First full subject (e.g. BCS501 DBMS) auto-generated as a PDF notebook | Member 2 |
| 4. Verifier + E-book/Flashcards | 9–10 | Verification loop; interactive e-book, flashcard and quiz renderers | Members 2 & 3 |
| 5. PYQ Analyser + Evaluation | 11–12 | ★ importance model, metrics dashboard, ablation experiments | Member 3 |
| 6. Web App + Payments | 13–14 | Auth, library, reader, Razorpay, admin panel, deployment | Member 4 |
| 7. Pilot & Report | 15–16 | Real-student pilot, results, final report, demo | All |

*Owners to be adjusted to team size.*

---

## 9. Evaluation Strategy

**Benchmark:** the team's hand-crafted e-books and exam notebook serve as the reference ("gold standard").

| Metric | What it shows |
|---|---|
| Syllabus Coverage % | Completeness |
| Faithfulness % (FActScore / RAGAS) | Factual correctness and freedom from hallucination |
| Numerical Accuracy % | Correctness of solved problems |
| PYQ Hit-Rate % | Exam usefulness |
| Human Preference (blind test, 5-point rubric) | Quality relative to hand-made material |
| Time and ₹ Cost per Subject | Scalability and business viability |

**Ablation study:** (a) plain LLM → (b) LLM + RAG → (c) Agentic RAG → (d) Agentic RAG + Verifier, to show how much each component contributes.

**Pilot:** release to a group of real students before semester exams, then measure usage, feedback and paid conversions.

---

## 10. Technology Stack

| Layer | Technology |
|---|---|
| Engine | Python, FastAPI, Claude API (swappable), LangGraph / custom agent loop |
| Research | Web search API (Tavily / Brave / Serper), trafilatura, BeautifulSoup |
| Retrieval | Sentence-Transformers embeddings, pgvector / ChromaDB, re-ranking |
| ML | scikit-learn (PYQ clustering), Tesseract / PaddleOCR |
| Rendering | Jinja2, HTML/CSS/JS, WeasyPrint, Mermaid |
| Web App | Next.js, Tailwind CSS, Supabase (PostgreSQL, Auth, Storage) |
| Payments | Razorpay (UPI, cards, net banking) |
| DevOps | GitHub, Docker, GitHub Actions, Vercel |

---

## 11. Business Model

| Tier | Offering | Indicative Price |
|---|---|---|
| **Free** | Syllabus view, Unit 1 of every subject, sample flashcards | ₹0 |
| **Subject** | Full e-book + PDF notebook + flashcards + quizzes for one subject | ₹49 – ₹99 |
| **Semester Pass** | All subjects of a semester | ₹199 – ₹299 |
| **B2B** | Custom material for coaching institutes and colleges | Licence-based |

**Why it can scale:** after the engine is built, the marginal cost of a new subject is only a few rupees of API usage. Every new university's syllabus becomes a new product line.

**Go-to-market:** start with AKTU B.Tech CSE (where reference content already exists), grow through student WhatsApp/Telegram groups and campus ambassadors, then expand branch by branch and university by university.

---

## 12. Risks and Mitigation

| Risk | Mitigation |
|---|---|
| Hallucinated or incorrect content | RAG grounding, Verifier agent, numerical re-computation, human review before publishing |
| Copyright of source material | Original synthesis with citations; no verbatim copying; prefer open sources (NPTEL, OER, Wikipedia) |
| Low-quality web sources | Source credibility scoring and multi-source agreement |
| API cost | Caching, smaller models for simple steps, cost tracking per subject |
| Content piracy after purchase | Signed, expiring links; watermarking with the buyer's details; in-app reader |
| Syllabus changes | Regeneration on demand from the updated syllabus |

---

## 13. Resources Required

- **Hardware:** team laptops (no GPU needed; LLM inference runs through an API)
- **Software:** open-source tools and free tiers (Supabase, Vercel, GitHub)
- **Paid services (estimated):** LLM API and web search API credits; Razorpay charges a percentage per transaction only
- **Data:** university syllabi (public), previous-year question papers, open educational resources

---

## 14. Expected Outcomes

1. A working Knowledge-Vault Engine: requirements in, complete multi-format study pack out.
2. A verified pilot library covering at least one full semester of AKTU B.Tech CSE.
3. A deployed, market-ready web application with payments.
4. An evaluation report with quantitative results and an ablation study.
5. A project report and a research paper suitable for conference submission.

---

## 15. Conclusion

Knowledge-Vault turns the slow, manual work of preparing exam-ready study material into an automated, verifiable and scalable AI process. Technically, it brings together the most in-demand areas of current AI engineering (LLMs, Retrieval-Augmented Generation, multi-agent systems and rigorous evaluation) in one production system. Socially and commercially, it gives every student, at any university, affordable and trustworthy material matched to their exact syllabus.

---

*References: see [SYNOPSIS.md](./SYNOPSIS.md#11-references).*
