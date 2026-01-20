from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

def load_prepare_chain(llm, prepare_retriever):
    prompt = ChatPromptTemplate.from_template(
        """
        You are a consulting coach.
        Use ONLY the provided context to answer the question.

        Context:
        {context}

        Question:
        {question}
        """
    )

    chain = (
        {
            "context": prepare_retriever,
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain
