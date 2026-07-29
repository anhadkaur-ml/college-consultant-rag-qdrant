# College Consultant - Qdrant PDF Knowledge Base

This is a new project. It does not modify the earlier SQLite project.

## Project structure

```text
Qdrant Project 1/
|-- data/
|   `-- qdrant_storage/       # ignored local Qdrant files
|-- documents/
|   `-- college_database_prospectus.pdf
|-- qdrant/
|   |-- client.py             # Cloud/local Qdrant connection
|   |-- collection.py         # cosine collection and vector store
|   |-- embeddings.py         # Gemini embedding model
|   `-- utils.py              # stable point IDs and PDF fingerprint
|-- schemas/
|   |-- knowledge_base.py     # seed/search result types
|   `-- outputs.py            # structured chatbot response
|-- main.py                   # interactive chatbot
|-- models.py                 # Gemini chat and embedding models
|-- pdf_loader.py             # PDF loading and recursive splitting
|-- prompts.py                # agent system instructions
|-- services.py               # agent, indexing, and retrieval use cases
|-- tools.py                  # LangChain knowledge-base tool
|-- vector_db.py              # compatibility imports
|-- config.py
|-- seed_database.py
|-- search.py
|-- verify_pdf.py
|-- .env.example
`-- requirements.txt
```

The structure follows the same document → split → embed → Qdrant → retriever
flow as the LangChain semantic-search guide, while keeping each responsibility
in a short top-level module.

## Cloud Free Tier or local?

The instructor note says "qdrant, free collection create." That likely means:

- **Recommended: Qdrant Cloud Free Tier.** It visibly demonstrates creating a
  managed free cluster and collection. It needs `QDRANT_URL` and
  `QDRANT_API_KEY`.
- **Fallback: local persistent Qdrant.** It is free, needs no Qdrant account,
  and stores data under `data/qdrant_storage/`. It is ideal for offline
  development but may not satisfy an instructor who expects a Cloud dashboard.

Both modes use the same collection/seeding/search code. Only the client changes.

## Setup

1. Create and activate a virtual environment:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

2. Copy `.env.example` to `.env`, then add your own keys. Never commit `.env`.

3. For Cloud, create a Qdrant Free cluster, copy its HTTPS endpoint and API key,
   and use:

   ```dotenv
   GOOGLE_API_KEY=...
   QDRANT_MODE=cloud
   QDRANT_URL=https://...cloud.qdrant.io
   QDRANT_API_KEY=...
   QDRANT_COLLECTION=college_prospectus
   ```

4. For the no-account local fallback:

   ```dotenv
   GOOGLE_API_KEY=...
   QDRANT_MODE=local
   QDRANT_LOCAL_PATH=data/qdrant_storage
   QDRANT_COLLECTION=college_prospectus
   ```

## Run one stage at a time

First verify PDF loading and splitting without any network call:

```powershell
python verify_pdf.py
```

Then seed the collection:

```powershell
python seed_database.py
```

Run it a second time if you want to verify idempotency: the first run reports
`seeded`, while an unchanged second run reports `already_seeded`.

Finally test similarity search:

```powershell
python search.py "Which colleges are in Ludhiana?"
python search.py "What is the annual fee at Chitkara University?"
```

Each result prints its similarity score, PDF filename, and human-readable page.

Start the interactive chatbot after seeding:

```powershell
python main.py
```

The agent uses the retriever tool when it needs facts and cites the PDF page in
its answer.

## Retriever tool (not a chain)

`tools.py` creates a LangChain `@tool`. It invokes the Qdrant
vector store through `as_retriever(search_type="similarity")` and returns both
formatted source/page text and the original `Document` artifacts. There is no
retrieval chain.

## Why this differs from the SQLite project

| SQLite structured extraction | Qdrant semantic knowledge base |
|---|---|
| LLM/Pydantic turns PDF facts into fixed fields | PDF pages remain `Document` objects and become chunks |
| Stores rows and columns | Stores embeddings plus text/metadata payloads |
| Best for exact filters, joins, and calculations | Best for meaning-based natural-language retrieval |
| Query needs known schema/SQL | Query is embedded and matched by vector similarity |
| Missing schema fields lose information | Original chunk text remains available |

The two approaches are complementary: SQLite is strong for exact structured
questions; Qdrant is strong for locating relevant unstructured passages.

## DSR / viva talking points

1. **Why split?** A whole page can contain unrelated facts. Smaller overlapping
   chunks make the relevant meaning less diluted.
2. **Why overlap 200 characters?** It reduces loss when a sentence or fact lies
   across a chunk boundary.
3. **Why cosine distance?** It compares embedding direction and is a standard
   similarity metric for dense text embeddings.
4. **Why metadata?** `source`, `page_number`, and `start_index` make retrieved
   answers traceable to the original PDF.
5. **Why idempotent seeding?** Stable UUIDs derived from PDF/chunk identity make
   repeated runs safe. Changed or removed chunks are replaced rather than
   duplicated.
6. **Why a retriever tool?** An agent can decide when knowledge-base lookup is
   needed. A fixed chain retrieves on every run.
7. **Where are secrets?** Only in ignored `.env`; the repository contains names
   and placeholders, never credentials.
