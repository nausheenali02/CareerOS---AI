from typing import List
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from app.llm import get_gemini_model
from app.state import CandidateProfile, JobAnalysis

class InterviewQuestion(BaseModel):
    category: str = Field(description="Category: 'Technical', 'System Design', or 'Behavioral/HR'")
    question: str
    target_skill_or_topic: str
    ideal_talking_point: str = Field(description="Key concepts or projects the candidate should mention in their answer.")

class InterviewPrepKit(BaseModel):
    questions: List[InterviewQuestion] = Field(description="Curated list of technical and behavioral interview questions.")

def generate_interview_kit(
    job_analysis: JobAnalysis, 
    candidate_profile: CandidateProfile, 
    missing_skills: List[str]
) -> InterviewPrepKit:
    llm = get_gemini_model(temperature=0.3)
    structured_llm = llm.with_structured_output(InterviewPrepKit)

    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a Hiring Manager and Lead Technical Interviewer.
Build a high-signal interview question set (3-4 questions) tailored to the candidate's background and target role.
Focus on missing skills and key technical trade-offs."""),
        ("user", """
Target Job Analysis:
{job_analysis}

Candidate Profile:
{candidate_profile}

Missing Skills:
{missing_skills}
""")
    ])

    chain = prompt | structured_llm
    return chain.invoke({
        "job_analysis": job_analysis.model_dump_json(),
        "candidate_profile": candidate_profile.model_dump_json(),
        "missing_skills": ", ".join(missing_skills) if missing_skills else "None"
    })