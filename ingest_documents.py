from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

# 1. Load PDF
from langchain_community.document_loaders import PyPDFLoader
import os

PDF_PATH = os.path.join("data", "Case-in-Point-2013.pdf")
loader = PyPDFLoader(PDF_PATH)
documents = loader.load()

pages = loader.load()

# 2. Split text
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=100
)

# 3. Manual section tagging based on page numbers
PART_PAGE_RANGES = {
    "prepare_yourself": range(10, 69),
    "learning": range(69, 130),
    "case_prep": range(130, 325),
}

structured_docs = []

for i, page in enumerate(pages):
    text = page.page_content
    part = "general"

    for tag, page_range in PART_PAGE_RANGES.items():
        if i in page_range:
            part = tag
            break

    chunks = splitter.split_text(text)

    for j, chunk in enumerate(chunks):
        structured_docs.append(
            Document(
                page_content=chunk,
                metadata={
                    "page_number": i + 1,
                    "part": part,
                    "source": "Case in Point",
                    "chunk_id": f"page_{i+1}_chunk_{j}"
                }
            )
        )

print("✅ Structured docs created:", len(structured_docs))

# Export structured documents
documents = structured_docs
__all__ = ["documents"]
