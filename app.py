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
    db_path = "./chroma_db"
    collection_name = "my_practice_docs"

    # Initialize the database client (Persistent = saves to disk)
    db_client = chromadb.PersistentClient(path=db_path)
    
    # Create (or get) a collection
    chroma_collection = db_client.get_or_create_collection(collection_name)
    
    # Tell LlamaIndex to use this Chroma collection
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # --- LOGIC: CREATE vs LOAD ---
    if chroma_collection.count() == 0:
        with st.spinner("First run: Reading PDF and saving to database..."):
            documents = SimpleDirectoryReader("data").load_data()
            index = VectorStoreIndex.from_documents(
                documents, storage_context=storage_context
            )
    else:
        with st.spinner("Database found! Loading existing memory..."):
            index = VectorStoreIndex.from_vector_store(
                vector_store, storage_context=storage_context
            )
            
    # Return the engine (Chat Mode = Context)
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
            # 1. Get the response object
            response = query_engine.chat(prompt)
            
            # 2. Display the main answer
            st.markdown(response.response)
            
            # 3. CITATION FEATURE (The Upgrade)
            with st.expander("📚 View Source Evidence"):
                for i, node in enumerate(response.source_nodes):
                    st.markdown(f"**Source Chunk {i+1}:**")
                    st.info(f"...{node.text}...")
                    
                    file_name = node.metadata.get('file_name', 'Unknown')
                    page_num = node.metadata.get('page_label', 'Unknown')
                    st.caption(f"📍 Found in: **{file_name}**, Page **{page_num}**")
            
            # 4. Save the assistant's response to history
            st.session_state.messages.append({"role": "assistant", "content": response.response})