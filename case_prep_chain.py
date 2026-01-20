# case_prep_chain.py

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


case_prompts = {
    "Profitability": "A retail chain has seen a 15% drop in net profits...",
    "Market Entry": "A European beverage company wants to enter the Indian market...",
    "M&A": "Your client is considering acquiring a smaller competitor...",
    "Growth Strategy": "A SaaS company wants to increase revenue by 30% in 2 years..."
}


def load_case_prep_chain(llm):
    system_prompt = """
    You are a consulting case interviewer for a top-tier firm (McKinsey, BCG, Bain).

    Conduct a realistic case interview:
    - Ask structured follow-up questions
    - Keep a professional interviewer tone
    - Follow a logical flow: clarification → framework → analysis → recommendation

    If the candidate types 'end' or 'done', switch to evaluation mode and:
    - Score Structure, Problem Solving, Communication, Business Acumen (out of 10)
    - Give a final verdict: Pass / Needs Improvement
    """

    prompt = ChatPromptTemplate.from_template(
        system_prompt + "\n\nCandidate input:\n{input}"
    )

    chain = prompt | llm | StrOutputParser()

    return chain


__all__ = ["load_case_prep_chain", "case_prompts"]
