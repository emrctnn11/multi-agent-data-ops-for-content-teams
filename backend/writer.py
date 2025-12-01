from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv

from state import AgentState

from config import GEMINI_API_KEY

load_dotenv()

llm = ChatGoogleGenerativeAI(
    google_api_key=GEMINI_API_KEY, 
    model="gemini-2.5-pro", 
    temperature=0
)



def writer_node(state: AgentState):
    """
    Writer agent that creates a draft based on the PRD text and research data.
    """

    print("--- [2/4] Writer Agent Started ---")

    prd_text = state.get("prd_text")

    research_data = state.get("prd_text")

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

    print("--- [2/4] Writer Agent Completed ---")
    return {"draft_text": response.content}
