from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, Document
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from groq import Groq
import config
import vector_db
import streamlit as st

# from llama_index.llms import Ollama


embedding_model = HuggingFaceEmbedding(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    use_auth_token=config.HF_API_KEY,
)

llm = Groq(api_key=config.GROQ_API_KEY)


def summarize_requirement(file_path, file_name):
    reader = SimpleDirectoryReader(input_dir=file_path)
    docs = reader.load_data()

    vector_db.delete_file_vectors(file_name)

    storage_context = vector_db.get_vector_store()

    index = VectorStoreIndex.from_documents(
        docs, storage_context=storage_context, embed_model=embedding_model
    )
    retriever = index.as_retriever()
    retrieved_docs = retriever.retrieve("Summarize this requirement.")
    retrieved_text = "\n\n".join([doc.text for doc in retrieved_docs])  # Extract text

    st.write(retrieved_text)
    # we can pass query from UI as well--- query__>""" edding """

    response = llm.chat.completions.create(
        model="gemma2-9b-it",
        messages=[{"role": "user", "content": f"Summarize: {retrieved_text}"}],
    )

    # st.write(response.choices[0].message.content)

    return response.choices[0].message.content


import fitz


def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file using PyMuPDF (fitz)."""
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text("text") + "\n"
    return text


def answer_query(user_query, file_path, file_name, model_name):
    reader = SimpleDirectoryReader(input_dir=file_path)
    docs = reader.load_data()
    # document object

    processed_docs = []
    for doc in docs:
        if doc.metadata.get("file_path", "").endswith(".pdf"):
            extracted_text = extract_text_from_pdf(doc.metadata["file_path"])
            processed_docs.append(Document(text=extracted_text))
        else:
            processed_docs.append(doc)

    # st.write([doc.text for doc in processed_docs])

    # vector_db.delete_file_vectors(file_name)

    storage_context = vector_db.get_vector_store()
    index = VectorStoreIndex.from_documents(
        processed_docs, storage_context=storage_context, embed_model=embedding_model
    )

    retriever = index.as_retriever()
    retrieved_docs = retriever.retrieve(user_query)
    retrieved_text = "\n\n".join([doc.text for doc in retrieved_docs])

    response = llm.chat.completions.create(
        model=model_name,
        messages=[
            {
                "role": "system",
                "content": "You are an expert AI assistant that extracts and answers questions based on uploaded documents.",
            },
            {
                "role": "user",
                "content": f"User Query: {user_query}\n\nRelevant Extracted Text:\n{retrieved_text}",
            },
        ],
        temperature=0.7,  # Adjust for better factual accuracy
    )

    return response.choices[0].message.content.strip() if response.choices else ""
