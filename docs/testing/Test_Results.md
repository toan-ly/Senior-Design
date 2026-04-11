# Test Results

**Authors:** Toan Ly, Daniel Lindsey  
**Related document:** [Test Plan (PDF)](Test_Plan.pdf)  




## Results by test case

| ID | Focus | Result | Notes |
|----|--------|--------|--------|
| MA-01 | Document loading | Pass | Configured sources under `data/raw` load without errors; non-empty text extracted for ingestion. |
| MA-02 | Text chunking | Pass | Chunk size and overlap match `configs/dev.yaml` (`chunk_size`, `chunk_overlap`); no empty or oversized chunks observed in sampled runs. |
| MA-03 | Summary metadata | Pass | Ingestion produces nodes with summary metadata when the summary extractor is enabled in the pipeline. |
| MA-04 | Embedding creation | Pass | Embeddings generated for ingested nodes; vectors present with consistent dimensions for the chosen embedding model. |
| MA-05 | Ingestion cache reuse | Pass | Second run with unchanged inputs and existing `data/cache/ingestion_cache.json` avoids redundant work; faster completion than cold run. |
| MA-06 | Index persistence / reload | Pass | Index artifacts under configured storage (`data/index_store` / Qdrant collection) persist; queries succeed after application restart. |
| MA-07 | Basic query retrieval | Pass | Queries grounded in DSM-5 material return responses that reflect retrieved context. |
| MA-08 | Out-of-scope query handling | Pass | Off-topic prompts yield cautious or non-specific replies rather than invented clinical detail; exact wording depends on LLM and prompts. |
| MA-09 | Retrieval ranking | Pass | Top retrieved nodes align with query intent in spot checks; reranker settings in config influence ordering as expected. |
| MA-10 | Query response time | Pass | Interactive latency acceptable for demo use. |
| MA-11 | Large document ingestion | Pass | Full DSM-scale ingestion completes without crash in tested environment; duration and memory depend on machine and API limits. |
| MA-12 | End-to-end RAG workflow | Pass | Ingest → index → query path runs end-to-end with no unhandled runtime errors in validated scenarios. |
| MA-13 | Database schema | Pass | Schema supports users, messages, scores, and journal entries. |
| MA-14 | Backend–database integration | Pass | API-driven reads/writes (auth, chat history, journal, scores) reflect correctly in Postgres. |
| MA-15 | Frontend accessibility / usability | Pass | Streamlit UI readable and navigable via mouse/keyboard. |
| MA-16 | End-to-end application | Pass | Docker Compose stack (frontend, backend, Postgres, Qdrant) supports login, chat, journal, and resources in integrated runs. |
| MA-17 | Journal functionality | Pass | Create, view, and edit flows behave as expected; data persists across sessions for the same user. |
| MA-18 | Feedback functionality | Pass | Users can submit feedback from the UI; inbox/mail flow behaves as designed for notifications and follow-up. |
| MA-19 | Account modification | Pass | Username, password, and email updates persist; session behavior re-tested after changes. |
| MA-20 | Reference / resources links | Pass | Resources page links open the expected external destinations in browser tests. |

