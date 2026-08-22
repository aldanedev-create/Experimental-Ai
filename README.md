# Experimental AI

A lightweight, local AI assistant that runs in GitHub Codespaces using
[Ollama](https://ollama.com/) and a small Qwen coding model.

Experimental AI is designed to work as both a **general-purpose AI
assistant** and a **programming assistant**, with additional
Flaxon-specific knowledge through Retrieval-Augmented Generation (RAG).

> **Status:** Experimental / Active Development

---

## Features

- 🤖 General-purpose AI assistant
- 💻 Programming assistance
- 🌐 HTML, CSS, JavaScript and TypeScript support
- 🐍 Python assistance
- 🗄️ SQL and database questions
- 🔧 Git and software engineering help
- 🧠 Flaxon-specific knowledge through RAG
- 📚 Local Flaxon documentation knowledge base
- 🔎 Semantic document search
- ⚡ Cached document indexing
- 🖥️ Runs inside GitHub Codespaces
- 🆓 Uses locally running open-source AI tooling
- 🔐 No external AI API key required for model inference

---

## How It Works

Experimental AI combines a local language model with a Flaxon
knowledge base.

```text
                    Experimental AI
                          │
              ┌───────────┴───────────┐
              │                       │
       General Knowledge        Flaxon Knowledge
              │                       │
          Qwen Model              RAG System
              │                       │
      HTML / CSS / JS          Flaxon Documentation
      Python / SQL / Git       Flaxon Examples
              │                 Flaxon Code
              │                       │
              └───────────┬───────────┘
                          │
                          ▼
                    AI Response