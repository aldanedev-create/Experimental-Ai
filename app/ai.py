import requests

from rag import search_flaxon_docs


OLLAMA_URL = "http://localhost:11434/api/generate"

MODEL = "qwen2.5-coder:1.5b"


SYSTEM_PROMPT = """
You are MY AI, a general-purpose AI and programming assistant.

You can help with:

- General questions
- HTML
- CSS
- JavaScript
- TypeScript
- Python
- SQL
- Git
- Linux
- Computer science
- Software engineering
- Flaxon

You should provide practical, accurate answers.

When answering Flaxon-specific questions, use the supplied
Flaxon documentation.

Never invent Flaxon APIs.

If the Flaxon documentation does not contain enough information,
say that clearly.

For normal programming questions, use your existing knowledge.
"""


def is_flaxon_question(message: str) -> bool:

    text = message.lower()

    flaxon_terms = [
        "flaxon",
        "flaxon framework",
        "flaxon api",
        "flaxon route",
        "flaxon routing",
        "flaxon middleware",
        "flaxon websocket",
        "flaxon auth",
        "flaxon plugin",
        "flaxon validation",
        "flaxon cli"
    ]

    return any(
        term in text
        for term in flaxon_terms
    )


def ask_ai(message: str) -> str:

    context = ""

    if is_flaxon_question(message):

        results = search_flaxon_docs(
            message,
            results=3
        )

        if results:

            context_parts = []

            for result in results:

                context_parts.append(
                    f"""
SOURCE: {result["source"]}

{result["text"]}
"""
                )

            context = "\n---\n".join(
                context_parts
            )

    prompt = f"""
{SYSTEM_PROMPT}

"""

    if context:

        prompt += f"""
RELEVANT FLAXON DOCUMENTATION:

{context}

"""

    prompt += f"""
USER:

{message}

ANSWER:
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.2
            }
        },
        timeout=300
    )

    response.raise_for_status()

    return response.json()["response"]