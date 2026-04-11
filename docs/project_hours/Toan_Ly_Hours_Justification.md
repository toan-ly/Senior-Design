# Toan Ly - Summary of Hours and Justification

## Hour totals

| Period | Hours |
|--------|------:|
| Fall semester | 61 |
| Spring semester | 92 |
| **Total** | **153** |

Fall consisted of **27 hours** of course deliverables (documentation, diagrams, presentations, reports, peer review) and **34 hours** of early project work, including research on LLMs and RAG, sourcing and organizing DSM-5 reference material, and standing team meetings.

Spring consisted of **15 hours** on course artifacts (test plan, user-facing documentation, slides, poster, self-assessment, and final report) and **77 hours** of technical work on MedAssist.

Most of my spring engineering effort went to the **RAG pipeline** and **chat agent**: ingesting and chunking the knowledge base, building and tuning the vector index, wiring retrieval and reranking, and integrating the LlamaIndex/OpenAI agent with tools and chat memory so answers stay grounded in DSM-5 content. That block of time reflects repeated iteration when retrieval quality, latency, or dependencies did not behave as expected on the first pass.

I also spent substantial time on **backend APIs** and **PostgreSQL integration** (e.g., auth-related flows, data used by chat and tracking features), plus work on the **Streamlit frontend** and **component integration** — fixing environment issues, and end-to-end bugs that only appeared when the UI called the API against a real database and vector store.

Additional hours went to **Docker and Compose** (bringing up Qdrant, Postgres, and the app consistently), **RAG evaluation** (structured tests and scripts to assess responses), and **team meetings** for design decisions, demos, and integration checkpoints. Meeting time is high because backend, data, and AI pieces had to stay aligned with the frontend and schema as both sides evolved.

