import os
import io
from typing import Optional, List
from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from dotenv import load_dotenv

from app.orchestrator import run_application_pipeline
from app.agents.resume_agent import extract_text_from_pdf
from app.agents.interview_agent import generate_interview_kit
from app.agents.evaluator_agent import evaluate_interview_answer
from app.state import ApplicationState

load_dotenv()

app = FastAPI(title="CareerOS AI")
templates = Jinja2Templates(directory="templates")

# In-memory store for the active session's application state
latest_state: Optional[ApplicationState] = None

@app.get("/", response_class=HTMLResponse)
async def serve_dashboard(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name="index.html"
    )

@app.post("/api/run-pipeline")
async def execute_agent_pipeline(
    jd_text: str = Form(...),
    resume_text: Optional[str] = Form(""),
    github_username: Optional[str] = Form(""),
    resume_pdf: Optional[UploadFile] = File(None)
):
    global latest_state
    final_resume = resume_text or ""
    if resume_pdf and resume_pdf.filename:
        pdf_bytes = await resume_pdf.read()
        final_resume = extract_text_from_pdf(io.BytesIO(pdf_bytes))

    latest_state = run_application_pipeline(
        raw_resume=final_resume,
        raw_jd=jd_text,
        github_username=github_username.strip() if github_username and github_username.strip() else None
    )

    return {
        "missing_skills": latest_state.missing_skills,
        "resume_suggestions": latest_state.resume_suggestions,
        "recommended_projects": [p.model_dump() for p in latest_state.recommended_projects],
        "cover_letter_draft": latest_state.cover_letter_draft
    }

@app.get("/api/generate-interview")
async def get_interview_prep():
    global latest_state
    if not latest_state or not latest_state.job_analysis:
        return {"error": "Please run an application pipeline first to calibrate questions."}

    kit = generate_interview_kit(
        job_analysis=latest_state.job_analysis,
        candidate_profile=latest_state.candidate_profile,
        missing_skills=latest_state.missing_skills
    )
    return {"questions": [q.model_dump() for q in kit.questions]}

class AnswerSubmission(BaseModel):
    question: str
    ideal_talking_point: str
    candidate_answer: str

@app.post("/api/evaluate-answer")
async def evaluate_answer(submission: AnswerSubmission):
    result = evaluate_interview_answer(
        question=submission.question,
        ideal_talking_point=submission.ideal_talking_point,
        candidate_answer=submission.candidate_answer
    )
    return result.model_dump()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)