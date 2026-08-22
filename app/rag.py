from pathlib import Path
import hashlib
import json

import chromadb
from sentence_transformers import SentenceTransformer


DOCS_DIR = Path(__file__).parent.parent / "flaxon_docs"
DB_DIR = Path(__file__).parent.parent / "chroma_db"

COLLECTION_NAME = "flaxon_docs"
MANIFEST_FILE = DB_DIR / "manifest.json"

CHUNK_SIZE = 1500
CHUNK_OVERLAP = 200
TOP_RESULTS = 3


client = chromadb.PersistentClient(path=str(DB_DIR))

collection = client.get_or_create_collection(
    name=COLLECTION_NAME
)

embedding_model = None


def get_embedding_model():
    global embedding_model

    if embedding_model is None:
        embedding_model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

    return embedding_model


def load_documents():
    documents = []

    for file in DOCS_DIR.rglob("*"):

        if file.suffix.lower() not in {
            ".md",
            ".txt",
            ".py"
        }:
            continue

        try:
            text = file.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue

        if text.strip():
            documents.append(
                {
                    "path": str(file),
                    "text": text
                }
            )

    return documents


def split_text(text):
    chunks = []

    start = 0

    while start < len(text):

        end = start + CHUNK_SIZE

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += CHUNK_SIZE - CHUNK_OVERLAP

    return chunks


def calculate_manifest(documents):

    data = []

    for document in documents:

        path = Path(document["path"])

        data.append(
            {
                "path": str(path),
                "size": path.stat().st_size,
                "modified": path.stat().st_mtime_ns
            }
        )

    raw = json.dumps(
        data,
        sort_keys=True
    ).encode()

    return hashlib.sha256(raw).hexdigest()


def needs_reindex(manifest):

    if not MANIFEST_FILE.exists():
        return True

    try:
        old_manifest = json.loads(
            MANIFEST_FILE.read_text()
        )

        return old_manifest.get("hash") != manifest

    except Exception:
        return True


def index_documents():

    documents = load_documents()

    if not documents:
        print("No Flaxon documentation found.")
        return

    manifest = calculate_manifest(documents)

    if not needs_reindex(manifest):

        print(
            f"Flaxon index already exists "
            f"({collection.count()} chunks)."
        )

        return

    print("Building Flaxon knowledge index...")

    chunks = []
    metadatas = []
    ids = []

    chunk_number = 0

    for document in documents:

        file_chunks = split_text(
            document["text"]
        )

        for chunk in file_chunks:

            chunks.append(chunk)

            metadatas.append(
                {
                    "source": document["path"]
                }
            )

            ids.append(
                f"chunk-{chunk_number}"
            )

            chunk_number += 1

    print(
        f"Creating embeddings for "
        f"{len(chunks)} chunks..."
    )

    model = get_embedding_model()

    embeddings = model.encode(
        chunks,
        batch_size=16,
        show_progress_bar=True
    ).tolist()

    collection.upsert(
        ids=ids,
        documents=chunks,
        metadatas=metadatas,
        embeddings=embeddings
    )

    MANIFEST_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    MANIFEST_FILE.write_text(
        json.dumps(
            {
                "hash": manifest
            }
        )
    )

    print(
        f"Indexed {len(chunks)} Flaxon chunks."
    )


def search_flaxon_docs(
    question: str,
    results: int = TOP_RESULTS
):

    if collection.count() == 0:
        return []

    model = get_embedding_model()

    embedding = model.encode(
        question
    ).tolist()

    result = collection.query(
        query_embeddings=[embedding],
        n_results=results
    )

    documents = result.get(
        "documents",
        [[]]
    )[0]

    metadatas = result.get(
        "metadatas",
        [[]]
    )[0]

    return [
        {
            "text": document,
            "source": metadata.get(
                "source",
                "unknown"
            )
        }
        for document, metadata
        in zip(documents, metadatas)
    ]