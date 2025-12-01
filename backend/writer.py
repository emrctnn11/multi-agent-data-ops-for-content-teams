from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv

from state import AgentState

from config import OPENAI_API_KEY

load_dotenv()

llm = ChatOpenAI(api_key=OPENAI_API_KEY, model="gpt-4o", temperature=0)


def writer_node(state: AgentState):
    """
    Writer agent that creates a draft based on the PRD text and research data.
    """

    print("--- Writer Agent Started ---")

    prd_text = state.get["prd_text"]

    research_data = state.get["research_data"]

    system_prompt = """ You are a skilled content writer. Using the provided Product Requirements Document (PRD) and research data, create a well-structured and engaging draft for the target audience. Ensure clarity, coherence, and alignment with the PRD objectives."""

    user_message = f"""
    Here is the PRD text:
    {prd_text}

    Please write a blog draft.
    """

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_message),
    ]

    response = llm.invoke(messages)

    print("--- Writer Agent Completed ---")
    return {"draft_text": response.content, "revision_count": 0}
