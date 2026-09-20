from io import BytesIO
from typing import List
from pypdf import PdfReader
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from app.llm import get_gemini_model
from app.state import CandidateProfile, JobAnalysis

class ResumeGapAnalysis(BaseModel):
    missing_skills: List[str] = Field(
        description="Critical technical skills or qualifications present in the JD but absent from the resume."
    )
    resume_suggestions: List[str] = Field(
        description="Actionable, bullet-level rewrites or additions to better align with the job description."
    )

def extract_text_from_pdf(pdf_source) -> str:
    """Extracts raw text from a PDF file path or file-like buffer."""
    reader = PdfReader(pdf_source)
    extracted_text = [page.extract_text() for page in reader.pages if page.extract_text()]
    return "\n".join(extracted_text)

def parse_candidate_profile(resume_text: str) -> CandidateProfile:
    """Parses raw resume text into a structured CandidateProfile model."""
    llm = get_gemini_model(temperature=0.0)
    structured_llm = llm.with_structured_output(CandidateProfile)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Extract key skills, total years of experience, and notable projects from the candidate's resume."),
        ("user", "Candidate Resume:\n\n{resume_text}")
    ])
    
    chain = prompt | structured_llm
    profile = chain.invoke({"resume_text": resume_text})
    profile.raw_resume_text = resume_text
    return profile

def analyze_resume_vs_jd(candidate_profile: CandidateProfile, job_analysis: JobAnalysis) -> ResumeGapAnalysis:
    """Identifies missing skills and generates targeted resume improvement suggestions."""
    llm = get_gemini_model(temperature=0.0)
    structured_llm = llm.with_structured_output(ResumeGapAnalysis)

    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an elite Career Coach and ATS specialist.
Compare the candidate's profile against the target job requirements.
Identify missing technical skills and suggest high-impact resume improvements that highlight relevant experience without fabricating facts."""),
        ("user", """
Target Job Analysis:
{job_analysis}

Candidate Profile:
{candidate_profile}
""")
    ])

    chain = prompt | structured_llm
    return chain.invoke({
        "job_analysis": job_analysis.model_dump_json(),
        "candidate_profile": candidate_profile.model_dump_json()
    })

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    
    sample_resume = """
    Software Engineer with 3 years experience in Python, Flask, and SQLite.
    Built automated data pipelines and REST APIs.
    Familiar with Git and basic Docker containers.
    """
    
    print("Testing Resume Parser...")
    parsed_profile = parse_candidate_profile(sample_resume)
    print(parsed_profile.model_dump_json(indent=2))