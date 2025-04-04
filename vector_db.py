# import chromadb
from llama_index.core import StorageContext
# from llama_index.vector_stores.chroma import ChromaVectorStore  # Import ChromaVectorStore
import os
import config

from llama_index.vector_stores.faiss import FaissVectorStore
import faiss




def get_vector_store():
    persist_dir = os.path.abspath(config.CHROMA_DB_PATH)
    os.makedirs(persist_dir, exist_ok=True)

    index_path = os.path.join(persist_dir, "faiss_index.index")

    # Try to read index if it exists
    if os.path.exists(index_path):
        try:
            faiss_index = faiss.read_index(index_path)
        except Exception as e:
            print(f"⚠️ Failed to read existing FAISS index: {e}")
            print("🔁 Creating a fresh FAISS index...")
            faiss_index = faiss.IndexFlatL2(384)  # adjust if using different embedding dims
    else:
        faiss_index = faiss.IndexFlatL2(384)

    # Setup vector store
    vector_store = FaissVectorStore(faiss_index=faiss_index)

    # Save the index back if it's new or modified
    try:
        vector_store.persist(index_path)
    except Exception as e:
        print(f"⚠️ Could not persist FAISS index: {e}")

    return StorageContext.from_defaults(vector_store=vector_store)

# def delete_file_vectors(file_name):
#     """Delete vectors related to a specific file without clearing the entire DB."""
#     chroma_client = chromadb.PersistentClient(path=os.getenv("CHROMA_DB_PATH", "./vector_db"))
#     collection = chroma_client.get_or_create_collection(name="test_collection")

#     # Use metadata filtering to delete only the specific file’s vectors
#     collection.delete(where={"file_name": file_name})  
