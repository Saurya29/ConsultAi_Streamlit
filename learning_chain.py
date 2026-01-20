# learning_chain.py

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

def load_learning_chain(llm, learning_retriever):
    prompt = ChatPromptTemplate.from_template(
        """
        You are a consulting tutor helping a candidate understand
        core consulting concepts clearly and intuitively.

        Use ONLY the provided context to answer.

        Context:
        {context}

        Question:
        {question}
        """
    )

    chain = (
        {
            "context": learning_retriever,
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain


__all__ = ["load_learning_chain"]
