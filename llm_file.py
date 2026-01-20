# llm_file.py

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()  # 🔑 loads .env into environment

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.7,
    groq_api_key=os.getenv("GROQ_API_KEY")
)

__all__ = ["llm"]
