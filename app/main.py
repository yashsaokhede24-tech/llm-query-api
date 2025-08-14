from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from typing import List
import requests
from .pipeline import RetrievalPipeline

app = FastAPI(
    title="LLM Query–Retrieval System",
    description="Semantic document QA for insurance, legal, HR, and compliance",
    version="1.0.0",
)

TEAM_TOKEN = "17a4d98258f8d7d8d27a6b78bbc43181314f83936eb11ca1a4e0d1d31e4f44ff"

class RunRequest(BaseModel):
    documents: str  # PDF blob URL
    questions: List[str]

class RunResponse(BaseModel):
    answers: List[str]

pipeline = RetrievalPipeline()

@app.post("/api/v1/hackrx/run", response_model=RunResponse)
def run_submission(
    req: RunRequest,
    authorization: str = Header(None)
):
    if authorization != f"Bearer {TEAM_TOKEN}":
        raise HTTPException(status_code=401, detail="Unauthorized")
    pdf_url = req.documents
    pdf_bytes = requests.get(pdf_url).content
    answers = pipeline.process(pdf_bytes, req.questions)
    return RunResponse(answers=answers)