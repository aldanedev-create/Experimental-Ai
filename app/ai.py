import requests

from rag import search_flaxon_docs


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5-coder:1.5b"


SYSTEM_PROMPT = """
You are a general-purpose AI assistant with special knowledge
of the Flaxon Python backend framework.

When answering Flaxon questions, use the provided Flaxon
documentation.

Do not invent Flaxon APIs.

If the documentation does not contain the answer, clearly
say that the information was not found in the Flaxon
documentation.

You can answer normal questions too.
"""


def ask_ai(message: str) -> str:

    results = search_flaxon_docs(message)

    documents = results.get("documents", [[]])[0]

    context = "\n\n---\n\n".join(documents)

    prompt = f"""
{SYSTEM_PROMPT}

FLAXON DOCUMENTATION:

{context}

USER QUESTION:

{message}

ANSWER:
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        },
        timeout=300
    )

    response.raise_for_status()

    return response.json()["response"]