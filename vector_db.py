import os
import faiss
from llama_index.vector_stores.faiss import FaissVectorStore
from llama_index.core import StorageContext
import config
# import asyncio


def get_vector_store():
    persist_dir = os.path.abspath(config.CHROMA_DB_PATH)
    os.makedirs(persist_dir, exist_ok=True)

    index_path = os.path.join(persist_dir, "faiss_index.index")
    dim = 384  # Match this with your embedding model (e.g., MiniLM)

    # Load or create FAISS index
    if os.path.exists(index_path):
        try:
            faiss_index = faiss.read_index(index_path)
        except Exception as e:
            print(f"⚠️ Failed to load FAISS index: {e}")
            print("🔁 Creating new index...")
            faiss_index = faiss.IndexFlatL2(dim)
    else:
        faiss_index = faiss.IndexFlatL2(dim)

    # Create vector store
    vector_store = FaissVectorStore(faiss_index=faiss_index)

    # Persist the index
    try:
        faiss.write_index(faiss_index, index_path)
    except Exception as e:
        print(f"⚠️ Could not persist FAISS index to disk: {e}")

    # Return storage context
    return StorageContext.from_defaults(vector_store=vector_store)
