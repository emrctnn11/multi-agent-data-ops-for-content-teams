import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from supabase import create_client, Client
from graph import app_graph
import traceback

app = FastAPI(title="Multi-Agent Content Ops")
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_ANON_KEY")


supabase: Client = create_client(url, key)


class PRDRequest(BaseModel):
    prd_content: str


@app.get("/")
def read_root():
    return {
        "status": "active",
        "message": "Welcome to the Multi-Agent Content Ops Backend!",
    }


@app.post("/start-workflow")
async def start_workflow(request: PRDRequest):
    """
    Get frontend PRD content and start the multi-agent workflow.
    """
    print(f"\n>>> New workflow request received. {request.prd_content[:50]}...")

    try:
        initial_data = {
            "prd_text": request.prd_content,
            "status": "running",
            "current_step": "researcher",
            "final_output": None,
        }
        db_response = supabase.table("workflow_runs").insert(initial_data).execute()
        run_id = db_response.data[0]["id"]
        print(f">>> Workflow initialized with Run ID: {run_id}")

        inputs = {
            "run_id": run_id,
            "prd_text": request.prd_content,
            "revision_count": 0,
        }

        final_state = app_graph.invoke(inputs)

        print("DEBUG: Final State Anahtarları:", final_state.keys())
        print("DEBUG: Final Post Değeri:", final_state.get("final_post"))

        final_post = final_state.get("final_post")
        print(">>> Workflow completed. Storing final output...")

        update_data = {
            "status": "completed",
            "final_output": final_post,
            "current_step": "completed",
        }

        supabase.table("workflow_runs").update(update_data).eq("id", run_id).execute()

        return {
            "message": "Workflow completed successfully.",
            "run_id": run_id,
            "final_post": final_post,
            "data": final_state,
        }

    except Exception as e:
        print("!!! HATA OLUŞTU !!!")
        traceback.print_exc()  # <--- BU SATIR HATANIN KONUMUNU GÖSTERECEK

        if "run_id" in locals():
            supabase.table("workflow_runs").update({"status": "failed"}).eq(
                "id", run_id
            ).execute()

        raise HTTPException(status_code=500, detail=str(e))
