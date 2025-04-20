# QV-RAG

A simple and efficient RAG (Retrieval-Augmented Generation) engine for semantic search and document retrieval.

> **Note**: This is an experimental project used for research and development. The engine is functional but will continue to evolve and improve over time.

## Features

- **Simple API**: Easy-to-use interface for document management and querying
- **Multiple Document Types**: Support for text, markdown, HTML, and JSON files
- **Smart Chunking**: Intelligent text splitting with metadata preservation
- **Semantic Search**: Built-in semantic search using ChromaDB
- **Metadata Support**: Flexible metadata handling for better document organization

## Installation

```bash
pip install qv-rag
```

## Quick Start

```python
from qv_rag.engine import RAGEngine

# Initialize the engine
engine = RAGEngine(
    collection_name="my_docs",
    chunk_size=1000,
    chunk_overlap=200
)

# Add documents
engine.add_texts(["Python is a popular programming language."])
engine.add_file("document.md")

# Query documents
results = engine.query("What is Python?")
for result in results:
    print(result['text'])
    print(f"Score: {result['distance']}")
```

## Usage Examples

### Adding Documents

```python
# Add text with metadata
engine.add_texts(
    texts=["Document content"],
    metadatas=[{"source": "manual", "category": "docs"}]
)

# Add a file
engine.add_file("document.md", metadata={"source": "file"})
```

### Querying

```python
# Simple query
results = engine.query("What is machine learning?")

# Query with filters
results = engine.query(
    "What is Python?",
    where={"category": "docs"},
    top_k=3
)
```

### Supported File Types

- Text files (`.txt`)
- Markdown files (`.md`)
- HTML files (`.html`, `.htm`)
- JSON files (`.json`)
- PDF files (`.pdf`) --> must be further improved

## License

MIT License
