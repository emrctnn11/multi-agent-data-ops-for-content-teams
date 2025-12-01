from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from state import AgentState
from dotenv import load_dotenv

from config import GEMINI_API_KEY

load_dotenv()

llm = ChatGoogleGenerativeAI(
    google_api_key=GEMINI_API_KEY, 
    model="gemini-2.5-pro", 
    temperature=0
)


def fact_checker_node(state: AgentState):
    """
    Fact Checker agent that quickly reviews the draft for glaring issues.
    """

    print("--- [3/4] Fact Checker Agent Started ---")

    draft_text = state.get("draft_text")
    research_data = state.get("research_data")
    revision_count = state.get("revision_count", 0)

    if revision_count >= 1:
        print("Maximum revisions reached. Skipping Fact Checker.")
        return {"review_status": "approve", "critique_comments": "None"}

    system_prompt = """ You are a meticulous Fact checker. Your task is to quickly review the provided draft for any glaring issues such as factual inaccuracies, 
    
    Rules:
        1. Reject if the draft contains a claim or numerical data that is NOT included in the research notes.
        2. Reject if the draft strays from the topic.

        Output Format:
        Your answer must begin ONLY with one of these two words: "APPROVAL" or "REVISED."

        If you use "REVISED," list below what needs to be corrected.
    ."""

    user_message = f"""
    Here is the research data: {research_data}
    Here is the draft text: {draft_text}
    
    Please review the draft and provide your feedback.
    """

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_message),
    ]

    response = llm.invoke(messages)
    content = response.content

    if content.startswith("APPROVAL"):
        print("--- [3/4] Fact Checker Agent Completed: APPROVED ---")
        return {"review_status": "approve", "critique_comments": None}
    else:
        print(f"--- [3/4] Fact Checker Agent Completed: REVISED ---")

        return {
            "review_status": "revise",
            "critique_comments": content,
            "revision_count": revision_count + 1,
        }
