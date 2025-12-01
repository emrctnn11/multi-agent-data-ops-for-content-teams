from langgraph.graph import StateGraph, END

from state import AgentState
from researcher import researcher_node
from writer import writer_node
from fact_checker import fact_checker_node
from style_polisher import style_polisher_node


def check_review_status(state: AgentState):
    """It makes a path split based on the results of the Fact-Checker. The returned string is the name of the next node."""

    status = state.get("review_status")

    if status == "approve":
        print("Fact Checker approved the draft. Proceeding to Style Polisher.")
        return "style_polisher"
    ##revise
    else:
        print("Fact Checker requested revisions. Returning to Writer.")
        return "writer"
    
workflow = StateGraph(AgentState)

workflow.add_node("researcher", researcher_node)
workflow.add_node("writer", writer_node)
workflow.add_node("fact_checker", fact_checker_node)
workflow.add_node("style_polisher", style_polisher_node)

workflow.set_entry_point("researcher")

workflow.add_edge("researcher", "writer")
workflow.add_edge("writer", "fact_checker")

workflow.add_conditional_edges(
    "fact_checker", 
    check_review_status, 
    {
    "writer": "writer",
    "style_polisher": "style_polisher",
    }
)

workflow.add_edge("style_polisher", END)

app_graph = workflow.compile()
