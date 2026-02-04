import streamlit as st
import os
import chromadb
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings, StorageContext
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="My Local AI Agent", page_icon="🤖")
st.title("🤖 Chat with your PDF (Persistent & Private)")

# 2. CACHE RESOURCES
@st.cache_resource(show_spinner=False)
def load_rag_engine():
    # --- SETUP LLM & EMBEDDINGS ---
    Settings.llm = Ollama(model="llama3.2:1b", request_timeout=360.0)
    Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
    
    # --- SETUP DATABASE (The Upgrade) ---
    # We define a folder on your disk to save the data
    db_path = "./chroma_db"
    collection_name = "my_practice_docs"

    # Initialize the database client (Persistent = saves to disk)
    db_client = chromadb.PersistentClient(path=db_path)
    
    # Create (or get) a collection (think of this as a "Table" in SQL)
    chroma_collection = db_client.get_or_create_collection(collection_name)
    
    # Tell LlamaIndex to use this Chroma collection as its storage
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # --- LOGIC: CREATE vs LOAD ---
    # If the collection is empty, it means this is the first run.
    if chroma_collection.count() == 0:
        with st.spinner("First run: Reading PDF and saving to database..."):
            # Load the PDF
            documents = SimpleDirectoryReader("data").load_data()
            # Create the index AND save it to the storage_context (Disk)
            index = VectorStoreIndex.from_documents(
                documents, storage_context=storage_context
            )
    else:
        with st.spinner("Database found! Loading existing memory..."):
            # Load the existing index from the storage_context (Disk)
            index = VectorStoreIndex.from_vector_store(
                vector_store, storage_context=storage_context
            )
            
    # Return the engine (upgraded to 'chat' so it remembers context)
    return index.as_chat_engine(chat_mode="context", system_prompt="You are a helpful expert.")

# Initialize the engine
query_engine = load_rag_engine()

# 3. CHAT INTERFACE
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. HANDLE INPUT
if prompt := st.chat_input("Ask something about your document..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # We use 'chat' here instead of 'query'
            response = query_engine.chat(prompt)
            st.markdown(response.response)
    
    st.session_state.messages.append({"role": "assistant", "content": response.response})