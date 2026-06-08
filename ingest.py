import os
import re
import random
from config import DOCS_PATH
from langchain_text_splitters import RecursiveCharacterTextSplitter


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _extract_doc_title(text: str) -> str:
    """Return the text of the first H1 ('# Title') line, or empty string."""
    match = re.search(r"^#\s+(.+)", text, re.MULTILINE)
    return match.group(1).strip() if match else ""


def _extract_source(text: str) -> str:
    """
    Return the URL from a '**Source:** <url>' line.
    Falls back to the document title if no source URL is found.
    """
    match = re.search(r"\*\*Source:\*\*\s*(https?://\S+)", text)
    if match:
        return match.group(1).strip()
    return _extract_doc_title(text)


def _build_header_index(text: str) -> list[tuple[int, str]]:
    """
    Scan *text* and return a list of (char_offset, header_text) pairs for
    every ## or ### heading (in document order).  Used to map a chunk's
    start_index back to the nearest preceding section heading.
    """
    headers = []
    for match in re.finditer(r"^#{2,3}\s+(.+)", text, re.MULTILINE):
        headers.append((match.start(), match.group(1).strip()))
    return headers


def _nearest_section(start_index: int, header_index: list[tuple[int, str]],
                     doc_title: str) -> str:
    """
    Given a chunk's start_index and the document's header_index, return the
    text of the nearest ## / ### heading that appears *before* the chunk.
    Falls back to doc_title if no heading precedes the chunk.
    """
    section = doc_title  # default fallback
    for offset, header_text in header_index:
        if offset <= start_index:
            section = header_text
        else:
            break  # headers are in order; no need to keep scanning
    return section


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def load_documents(path: str = DOCS_PATH) -> list[dict]:
    """
    Read every .md file from *path* and return a list of document dicts.

    Each dict contains:
        text      (str)  – full file contents
        source    (str)  – URL extracted from the '**Source:**' line, or doc_title fallback
        filename  (str)  – bare filename, e.g. 'tripadvisor-gainesville.md'
        doc_title (str)  – text of the H1 heading at the top of the file
    """
    documents = []
    for filename in sorted(os.listdir(path)):
        if not filename.endswith(".md"):
            continue
        filepath = os.path.join(path, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()

        doc_title = _extract_doc_title(text)
        documents.append({
            "text": text,
            "source": _extract_source(text),
            "filename": filename,
            "doc_title": doc_title,
        })

    print(f"Loaded {len(documents)} document(s): "
          f"{[d['filename'] for d in documents]}")
    return documents


def chunk_text(documents: list[dict]) -> list[dict]:
    """
    Split each document into overlapping chunks using LangChain's
    RecursiveCharacterTextSplitter, then attach rich metadata to every chunk.

    Chunking spec:
        chunk_size  = 600 characters
        overlap     = 100 characters
        separators  = [\\n\\n, \\n, '. ', ' ', '']
        min_length  = 50 characters (filters out short headers/fragments)

    Each returned chunk dict contains:
        text      (str)  – the chunk text
        source    (str)  – source URL or fallback parent document title
        filename  (str)  – parent filename
        doc_title (str)  – H1 title of the parent document
        section   (str)  – nearest preceding ## / ### heading, or doc_title
                           if no heading precedes the chunk
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=100,
        separators=["\n\n", "\n", ". ", " ", ""],
        add_start_index=True,   # gives us chunk.metadata["start_index"]
    )

    all_chunks = []
    min_length = 50

    for doc in documents:
        text = doc["text"]
        header_index = _build_header_index(text)

        # LangChain Document objects carry metadata through the split
        lc_docs = splitter.create_documents(
            texts=[text],
            metadatas=[{
                "source": doc["source"],
                "filename": doc["filename"],
                "doc_title": doc["doc_title"],
            }],
        )

        for lc_doc in lc_docs:
            chunk_content = lc_doc.page_content.strip()
            # Filter out chunks that are too short (e.g. less than 50 chars)
            if len(chunk_content) < min_length:
                continue

            start_idx = lc_doc.metadata.get("start_index", 0)
            section = _nearest_section(start_idx, header_index,
                                       doc["doc_title"])
            all_chunks.append({
                "text": chunk_content,
                "source": lc_doc.metadata["source"],
                "filename": lc_doc.metadata["filename"],
                "doc_title": lc_doc.metadata["doc_title"],
                "section": section,
            })

    print(f"Created {len(all_chunks)} chunk(s) from "
          f"{len(documents)} document(s) (with min_length={min_length}).")
    return all_chunks


# ---------------------------------------------------------------------------
# Verification
# ---------------------------------------------------------------------------

def verify_chunks(chunks: list[dict], n: int = 5) -> None:
    """Print *n* random chunks with their character count and metadata."""
    sample = random.sample(chunks, min(n, len(chunks)))
    print("\n" + "=" * 70)
    print(f"VERIFICATION — {n} random chunks")
    print("=" * 70)
    for i, chunk in enumerate(sample, 1):
        print(f"\n--- Chunk {i} ---")
        print(f"  filename  : {chunk['filename']}")
        print(f"  doc_title : {chunk['doc_title']}")
        print(f"  section   : {chunk['section']}")
        print(f"  source    : {chunk['source']}")
        print(f"  char count: {len(chunk['text'])}")
        print(f"  text      :\n{chunk['text']}")
    print("\n" + "=" * 70)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    docs = load_documents()
    chunks = chunk_text(docs)
    verify_chunks(chunks)
