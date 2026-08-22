from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer


DOCS_DIR = Path(__file__).parent.parent / "flaxon_docs"

client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection(
    name="flaxon_docs"
)

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def load_documents():
    documents = []

    for file in DOCS_DIR.rglob("*"):
        if file.suffix.lower() not in {".md", ".txt", ".py"}:
            continue

        try:
            text = file.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue

        if text.strip():
            documents.append(
                {
                    "path": str(file),
                    "text": text
                }
            )

    return documents


def index_documents():
    documents = load_documents()

    if not documents:
        print("No Flaxon documentation found.")
        return

    for index, document in enumerate(documents):
        embedding = embedding_model.encode(
            document["text"]
        ).tolist()

        collection.upsert(
            ids=[str(index)],
            documents=[document["text"]],
            metadatas=[
                {
                    "source": document["path"]
                }
            ],
            embeddings=[embedding]
        )

    print(f"Indexed {len(documents)} Flaxon documents.")


def search_flaxon_docs(question: str, results: int = 4):
    embedding = embedding_model.encode(
        question
    ).tolist()

    result = collection.query(
        query_embeddings=[embedding],
        n_results=results
    )

    return result