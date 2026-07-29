# College Consultant - Qdrant PDF Knowledge Base

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





