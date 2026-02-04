from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# --- CONFIGURATION START ---

# 1. SETUP LLM (The Brain)
# We tell LlamaIndex to talk to your local Ollama instead of OpenAI.
# "request_timeout" is high because local laptops can be slower than servers.
Settings.llm = Ollama(model="llama3.2:1b", request_timeout=360.0)

# 2. SETUP EMBEDDINGS (The Translator)
# OpenAI usually handles this. Since we are offline, we need a local tool
# to turn text into numbers. This downloads a small model (BAAI) automatically.
print("Initializing embedding model (this happens only once)...")
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

# --- CONFIGURATION END ---

# 3. LOAD DATA
# Make sure your PDF is inside a folder named 'data'
print("Loading your PDF...")
documents = SimpleDirectoryReader("data").load_data()

# 4. INDEX DATA
# This will take a bit longer on your laptop than OpenAI did.
print("Creating Index...")
index = VectorStoreIndex.from_documents(documents)

# 5. CHAT
query_engine = index.as_query_engine()
print("Ready! Ask a question (or type 'exit' to stop).")

while True:
    question = input("\nYour Question: ")
    if question.lower() == "exit":
        break
    
    print("Thinking...")
    response = query_engine.query(question)
    print(f"Answer: {response}")