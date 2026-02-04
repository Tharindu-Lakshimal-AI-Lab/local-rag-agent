import streamlit as st
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="My Local AI Agent", page_icon="🤖")
st.title("🤖 Chat with your PDF (Local & Private)")

# 2. CACHE RESOURCES (Important!)
# We use @st.cache_resource so the AI doesn't reload every time you click a button.
# If we didn't do this, it would re-read the PDF every time you typed a letter!
@st.cache_resource
def load_rag_engine():
    # Setup the Brain (Ollama)
    Settings.llm = Ollama(model="llama3.2:1b", request_timeout=360.0)
    
    # Setup the Embeddings
    Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
    
    # Load Data & Index
    with st.spinner("Loading knowledge base... This helps me think."):
        documents = SimpleDirectoryReader("data").load_data()
        index = VectorStoreIndex.from_documents(documents)
        return index.as_query_engine()

# Initialize the engine (Run the function above)
query_engine = load_rag_engine()

# 3. CHAT INTERFACE
# Initialize chat history if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. HANDLE USER INPUT
if prompt := st.chat_input("Ask something about your document..."):
    # Show user message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generate AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = query_engine.query(prompt)
            st.markdown(response)
    
    # Save AI response to history
    st.session_state.messages.append({"role": "assistant", "content": str(response)})