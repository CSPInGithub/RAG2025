import chromadb
from llama_index.core import StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore  # Import ChromaVectorStore
import os
import config

def get_vector_store():
    # Initialize ChromaDB client
    chroma_client = chromadb.PersistentClient(path=config.CHROMA_DB_PATH)

    collection_name = "test_collection"

    
    # Create or get a collection
    collection = chroma_client.get_or_create_collection(name=collection_name)

    # Initialize LlamaIndex's ChromaVectorStore
    vector_store = ChromaVectorStore(chroma_collection=collection)

    # Return storage context with correct vector store
    return StorageContext.from_defaults(vector_store=vector_store)

def delete_file_vectors(file_name):
    """Delete vectors related to a specific file without clearing the entire DB."""
    chroma_client = chromadb.PersistentClient(path=os.getenv("CHROMA_DB_PATH", "./vector_db"))
    collection = chroma_client.get_or_create_collection(name="test_collection")

    # Use metadata filtering to delete only the specific file’s vectors
    collection.delete(where={"file_name": file_name})  
