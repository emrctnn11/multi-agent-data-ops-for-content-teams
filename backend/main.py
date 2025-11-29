import os
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from pydantic import BaseModel
from supabase import create_client, Client
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

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

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_ANON_KEY")

if not url or not key:
    raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY must be set in environment variables")

supabase: Client = create_client(url, key)

class PRDRequest(BaseModel):
    prd_content: str

@app.get("/")
def read_root():
    return {"status" : "active", "message": "Multi-Agent Orchestrator is ready."}

@app.post("/start-workflow")
async def start_workflow(request: PRDRequest):
    """
     Gets a PRD content and starts the workflow to generate content based on it.
    """

    try:
        new_run = {
            "prd_text": request.prd_content,
            "status": "pending",
            "current_step": "init",
            "final_output": None
        }

        respsonse = supabase.table("workflow_runs").insert(new_run).execute()

        return {
            "message": "Workflow started successfully.",
            "run_id": respsonse.data[0]['id'],
            "data": respsonse.data[0]
        }
    
    except Exception as e:
        print(f"Error starting workflow: {e}")
        raise HTTPException(status_code=500, detail=str(e))