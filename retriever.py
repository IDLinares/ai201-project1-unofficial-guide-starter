import hashlib
import chromadb
from chromadb.utils import embedding_functions
from config import CHROMA_COLLECTION, CHROMA_PATH, EMBEDDING_MODEL, N_RESULTS

# sentence-transformers downloads the model on first use — this may take
# 30–60 seconds the very first time. Subsequent runs use a local cache.
_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name=EMBEDDING_MODEL
)
_client = chromadb.PersistentClient(path=CHROMA_PATH)
_collection = _client.get_or_create_collection(
    name=CHROMA_COLLECTION,
    embedding_function=_ef,
    metadata={"hnsw:space": "cosine"},
)


def get_collection():
    """Return the ChromaDB collection."""
    return _collection


def embed_and_store(chunks: list[dict]) -> None:
    """
    Embed a list of chunks and store them in the vector database.

    Each chunk dict must have: text, source, filename, doc_title, section.
    IDs are derived from a SHA-1 hash of each chunk's text so re-runs are
    idempotent — ChromaDB will skip duplicates with the same ID.

    The section heading/source context is prepended to the chunk text before
    embedding so that retrieval benefits from the structural metadata.
    """
    documents = []
    metadatas = []
    ids = []

    for chunk in chunks:
        # Prepend section + source context before embedding
        context_prefix = f"[{chunk['section']}] ({chunk['source']})\n"
        enriched_text = context_prefix + chunk["text"]

        chunk_id = hashlib.sha1(chunk["text"].encode()).hexdigest()

        documents.append(enriched_text)
        metadatas.append({
            "source": chunk["source"],
            "filename": chunk["filename"],
            "doc_title": chunk["doc_title"],
            "section": chunk["section"],
            "raw_text": chunk["text"],
        })
        ids.append(chunk_id)

    _collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids,
    )
    print(f"Stored {_collection.count()} total chunks in the vector database.")


def retrieve(query: str, n_results: int = N_RESULTS) -> list[dict]:
    """
    Find the most relevant chunks for a user's question.

    Uses ChromaDB cosine similarity search. Returns up to n_results chunk
    dicts, each with:
        text     – raw chunk text (without the prepended context prefix)
        source   – source URL or doc title
        section  – nearest section heading in the parent document
        distance – cosine distance (lower = more similar)

    Returns an empty list if the collection has no data yet.
    """
    if _collection.count() == 0:
        return []

    results = _collection.query(
        query_texts=[query],
        n_results=n_results,
        include=["documents", "metadatas", "distances"],
    )

    docs = results["documents"][0]
    metas = results["metadatas"][0]
    dists = results["distances"][0]

    chunks = []
    for doc, meta, dist in zip(docs, metas, dists):
        chunk = {
            "text": meta.get("raw_text", doc),
            "source": meta["source"],
            "section": meta["section"],
            "doc_title": meta["doc_title"],
            "distance": dist,
        }
        print(
            f"  [dist: {dist:.3f}] [{meta['section']}] "
            f"({meta['source']})\n  {chunk['text'][:500]}...\n"
        )
        chunks.append(chunk)

    return chunks


# ---------------------------------------------------------------------------
# Evaluation — tests from the Evaluation Plan in planning.md
# ---------------------------------------------------------------------------

EVAL_QUESTIONS = [
    "What are some free or cheap things to do in Gainesville?",
    "Are there any outdoor activities within 2 miles of campus?",
    "Is the Cade Museum a good place for kids?",
    "Is there a place to see Broadway performances around UF?",
    "Can I walk to the beach from campus?",
]


def run_eval() -> None:
    """Print top-k retrieval results for each evaluation question."""
    print("\n" + "=" * 70)
    print("RETRIEVAL EVALUATION")
    print("=" * 70)
    for i, question in enumerate(EVAL_QUESTIONS, 1):
        print(f"\nQ{i}: {question}")
        print("-" * 60)
        chunks = retrieve(question)
        if not chunks:
            print("  (no results — collection is empty)")
    print("=" * 70)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    from ingest import load_documents, chunk_text

    docs = load_documents()
    chunks = chunk_text(docs)
    embed_and_store(chunks)
    run_eval()
