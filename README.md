# 🤖 Local RAG Agent (Privacy-First)

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![LlamaIndex](https://img.shields.io/badge/Framework-LlamaIndex-purple)
![Ollama](https://img.shields.io/badge/Model-Llama3.2-orange)
![ChromaDB](https://img.shields.io/badge/VectorDB-ChromaDB-green)
![Status](https://img.shields.io/badge/Status-Active-green)

A fully local, offline Retrieval-Augmented Generation (RAG) system that allows you to chat with your private PDF documents without sending data to the cloud. Built for privacy, speed, and zero cost.

---

## 🚀 Features

-   **100% Offline:** Runs entirely on your local hardware using Ollama.
-   **Persistent Memory:** Uses **ChromaDB** to save your document index to disk. You only need to build the index once!
-   **Explainable AI:** Provides **Citations** (Source Nodes) for every answer, showing exactly which part of the PDF was used.
-   **Privacy Focused:** Your data never leaves your laptop.
-   **Smart Context:** Uses Vector Embeddings to understand specific details in your documents.

## 🛠️ Tech Stack

-   **LLM:** Llama 3.2 (1B Parameter) via Ollama
-   **Orchestration:** LlamaIndex
-   **Embeddings:** HuggingFace (`BAAI/bge-small-en-v1.5`)
-   **Interface:** Streamlit
-   **Vector Database:** ChromaDB (Persistent Storage)

---

## ⚙️ Installation Guide

### Prerequisites
1.  **Install Python** (3.10 or higher).
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
    pip install -r requirements.txt
    ```

---

## 📖 How to Use

1.  Place your PDF document inside a folder named `data` in the project root.
2.  Run the application:
    ```bash
    streamlit run app.py
    ```
3.  **First Run:** The app will take a moment to read your PDF and save it to `chroma_db` (Disk).
4.  **Next Runs:** The app will load instantly from the database!

---

## 🧠 System Architecture

```mermaid
graph TD
    User[User Query] --> UI(Streamlit UI);
    UI --> Engine{LlamaIndex};
    
    subgraph "Storage Layer"
    Engine -->|Retrieve| DB[(ChromaDB)];
    DB -->|Source Chunks| Engine;
    end
    
    Engine -->|Prompt + Context| LLM[Ollama / Llama 3.2];
    LLM -->|Answer| UI;
    UI -->|Show Citations| User;
