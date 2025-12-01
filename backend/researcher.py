import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv

from state import AgentState
from config import GEMINI_API_KEY

llm = ChatGoogleGenerativeAI(
    google_api_key=GEMINI_API_KEY, 
    model="gemini-2.5-pro", 
    temperature=0
)



def researcher_node(state: AgentState):
    """
    Researcher agent that gathers information based on the PRD text.
    """

    print("--- [1/4] Research Agent Started ---")

    prd_text = state["prd_text"]

    system_prompt = "You are a diligent researcher tasked with gathering relevant information based on the provided Product Requirements Document (PRD). Your goal is to collect accurate and comprehensive data that will inform the content creation process."

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(
            content=f"Here is the PRD text:\n{prd_text}\n\nPlease research and provide relevant information that can be used for content creation."
        ),
    ]

    response = llm.invoke(messages)

    print("--- [1/4] Research Agent Completed ---")
    return {"research_data": response.content}
