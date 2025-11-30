from typing import TypedDict, Optional

class AgentState(TypedDict):
    run_id: str
    prd_text: str

    research_data: Optional[str]
    draft_text: Optional[str]

    critique_comments: Optional[str]
    review_status: str
    revision_count: int

    final_post: Optional[str]