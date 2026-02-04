# 🤖 Local RAG Agent (Privacy-First)

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![LlamaIndex](https://img.shields.io/badge/Framework-LlamaIndex-purple)
![Ollama](https://img.shields.io/badge/Model-Llama3.2-orange)
![Status](https://img.shields.io/badge/Status-Active-green)

A fully local, offline Retrieval-Augmented Generation (RAG) system that allows you to chat with your private PDF documents without sending data to the cloud. Built for privacy, speed, and zero cost.

---

## 🚀 Features

-   **100% Offline:** Runs entirely on your local hardware using Ollama.
-   **Zero Cost:** No OpenAI API keys or subscription fees required.
-   **Privacy Focused:** Your data never leaves your laptop.
-   **Smart Context:** Uses Vector Embeddings to understand specific details in your documents.
-   **Interactive UI:** Clean chat interface built with Streamlit.

## 🛠️ Tech Stack

-   **LLM:** Llama 3.2 (1B Parameter) via Ollama
-   **Orchestration:** LlamaIndex
-   **Embeddings:** HuggingFace (`BAAI/bge-small-en-v1.5`)
-   **Interface:** Streamlit
-   **Vector Store:** In-memory VectorStoreIndex

---

## ⚙️ Installation Guide

### Prerequisites
1.  **Install Python** (3.9 or higher).
2.  **Install Ollama:** Download from [ollama.com](https://ollama.com).
3.  **Pull the Model:** Open your terminal and run:
    ```bash
    ollama pull llama3.2:1b
    ```

### Setup
1.  Clone the repository:
    ```bash
    git clone [https://github.com/Tharindu-Lakshimal-AI-Lab/local-rag-agent.git](https://github.com/Tharindu-Lakshimal-AI-Lab/local-rag-agent.git)
    cd local-rag-agent
    ```

2.  Create a virtual environment:
    ```bash
    python -m venv .venv
    # Windows:
    .venv\Scripts\activate
    # Mac/Linux:
    source .venv/bin/activate
    ```

3.  Install dependencies:
    ```bash
    pip install llama-index llama-index-llms-ollama llama-index-embeddings-huggingface streamlit
    ```

---

## 📖 How to Use

1.  Place your PDF document inside a folder named `data` in the project root.
2.  Run the application:
    ```bash
    streamlit run app.py
    ```
3.  Open your browser to the URL shown (usually `http://localhost:8501`).
4.  Start chatting with your document!

---

## 🧠 System Architecture

```mermaid
graph LR
    A[User Query] --> B(Streamlit UI);
    B --> C{LlamaIndex};
    C -->|Retrieve| D[Vector Store];
    D -->|Context| C;
    C -->|Prompt + Context| E[Ollama / Llama 3.2];
    E -->|Answer| B;
