# retriever_setup.py

import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

# 🔹 Import documents from your existing ingestion file
from ingest_documents import documents

# Embedding model
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

FAISS_PATH = "faiss_index"

# 🔹 Load FAISS if it exists, otherwise create it
if os.path.exists(FAISS_PATH):
    vectorstore = FAISS.load_local(
        FAISS_PATH,
        embeddings=embedding_model,
        allow_dangerous_deserialization=True
    )
    print("✅ FAISS index loaded from disk")
else:
    print("⏳ Creating FAISS index (first run)...")
    vectorstore = FAISS.from_documents(documents, embedding_model)
    vectorstore.save_local(FAISS_PATH)
    print("✅ FAISS index created and saved")

# 🔹 Prepare retrievers by filtering on metadata["part"]
prepare_retriever = vectorstore.as_retriever(
    search_kwargs={
        "filter": lambda metadata: metadata.get("part") == "prepare_yourself"
    }
)

learning_retriever = vectorstore.as_retriever(
    search_kwargs={
        "filter": lambda metadata: metadata.get("part") == "learning"
    }
)

case_prep_retriever = vectorstore.as_retriever(
    search_kwargs={
        "filter": lambda metadata: metadata.get("part") == "case_prep"
    }
)

print("✅ Retrievers loaded and filtered by part.")

__all__ = [
    "prepare_retriever",
    "learning_retriever",
    "case_prep_retriever",
]
