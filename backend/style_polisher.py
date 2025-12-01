from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv

from state import AgentState

from config import OPENAI_API_KEY

load_dotenv()

llm = ChatOpenAI(api_key=OPENAI_API_KEY, model="gpt-4o", temperature=0)


def style_polisher_node(state: AgentState):
    """
    Style Polisher agent that refines the draft for style, tone, and readability.
    """

    print("--- [4/4] Style Polisher Agent Started ---")

    draft_text = state.get("draft_text")

    system_prompt = """ 
    You are an award-winning Blog Editor.
        Your mission: To edit the assigned draft in a way that enhances reading pleasure, NEVER altering the meaning or facts.

        You Need to:
        - Correct spelling and grammar errors.
        - Break up and simplify long and complex sentences.
        - Tone: Make it professional, friendly, and trustworthy.
        - Add fluid transitions between paragraphs.
        - Finally, submit a post ready for publication in Markdown format.
        """
    user_message = f"""
    Here is the draft text: {draft_text}
    Please polish the style, tone, and readability of the draft.
    """

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_message),
    ]

    response = llm.invoke(messages)

    print("--- [4/4] Style Polisher Agent Completed ---")
    return {"final_draft": response.content}
