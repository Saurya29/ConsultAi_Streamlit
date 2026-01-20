# case_example.py  (or case_examples_chain.py)

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough


def load_case_examples_chain(llm, case_example_retriever):
    prompt = ChatPromptTemplate.from_template(
        """
        You are a consulting trainer.

        A candidate is asking for REAL consulting case examples.
        Use the provided context (from a casebook) to:

        - Share relevant case examples
        - Identify the business problem type
        - Mention industries if applicable
        - Highlight key lessons or approaches

        Context:
        {context}

        Question:
        {question}
        """
    )

    chain = (
        {
            "context": case_example_retriever,
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain


__all__ = ["load_case_examples_chain"]
