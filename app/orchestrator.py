import os
from typing import Optional
from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate
from app.llm import get_gemini_model
from app.state import ApplicationState
from app.agents.jd_agent import analyze_job_description
from app.agents.resume_agent import parse_candidate_profile, analyze_resume_vs_jd
from app.agents.project_agent import fetch_user_github_projects, recommend_projects_for_job

load_dotenv()

def generate_cover_letter(state: ApplicationState) -> str:
    """Generates a targeted, high-impact cover letter using aggregate state data."""
    llm = get_gemini_model(temperature=0.4)
    
    top_projects = [
        f"- {p.project_name}: {p.match_reason}" 
        for p in state.recommended_projects[:2]
    ]
    projects_str = "\n".join(top_projects) if top_projects else "N/A"

    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a professional Executive Career Strategist.
Write a targeted, high-impact cover letter (under 300 words).
Connect the candidate's verified skills and highlighted projects to the target role's core responsibilities.
Avoid generic clichés like 'I am writing to express my interest'. Lead directly with impact, technical alignment, and results."""),
        ("user", """
Target Job Core Responsibilities:
{responsibilities}

Candidate Skills:
{skills}

Highlighted GitHub Projects:
{projects}
""")
    ])

    chain = prompt | llm
    response = chain.invoke({
        "responsibilities": state.job_analysis.core_responsibilities if state.job_analysis else [],
        "skills": state.candidate_profile.extracted_skills if state.candidate_profile else [],
        "projects": projects_str
    })
    
    # Ensure clean text extraction across newer Gemini SDK structures
    if isinstance(response.content, list):
        text_chunks = [
            chunk["text"] for chunk in response.content 
            if isinstance(chunk, dict) and "text" in chunk
        ]
        return "\n".join(text_chunks)
    return str(response.content)

def run_application_pipeline(
    raw_resume: str, 
    raw_jd: str, 
    github_username: Optional[str] = None
) -> ApplicationState:
    """
    Coordinates the multi-agent pipeline:
    1. Parse Job Description
    2. Parse Resume Profile
    3. Run Gap Analysis (Missing skills & suggestions)
    4. Fetch and match GitHub projects (if username provided)
    5. Draft customized cover letter
    """
    print("🚀 Initializing Application Pipeline with Gemini...")
    state = ApplicationState(
        raw_resume_text=raw_resume,
        raw_job_description=raw_jd,
        github_username=github_username
    )

    # 1. Analyze Job Description
    print("🔎 [1/5] Analyzing Job Description...")
    state.job_analysis = analyze_job_description(state.raw_job_description)

    # 2. Parse Candidate Resume
    print("📄 [2/5] Parsing Resume Profile...")
    state.candidate_profile = parse_candidate_profile(state.raw_resume_text)

    # 3. Gap Analysis
    print("🧠 [3/5] Computing Resume vs JD Gap Analysis...")
    gap_result = analyze_resume_vs_jd(state.candidate_profile, state.job_analysis)
    state.missing_skills = gap_result.missing_skills
    state.resume_suggestions = gap_result.resume_suggestions

    # 4. GitHub Project Matching
    if state.github_username:
        print(f"🐙 [4/5] Pulling GitHub repos for @{state.github_username}...")
        repos = fetch_user_github_projects(state.github_username)
        print("🎯 Ranking best matching portfolio projects...")
        state.recommended_projects = recommend_projects_for_job(repos, state.job_analysis)
    else:
        print("⏩ [4/5] Skipping GitHub inspection (no username provided).")

    # 5. Tailored Cover Letter Draft
    print("✍️ [5/5] Drafting Tailored Cover Letter...")
    state.cover_letter_draft = generate_cover_letter(state)

    print("✅ Pipeline execution complete!\n")
    return state

if __name__ == "__main__":
    sample_jd = """
    Senior Python Engineer at Fintech Scale-up.
    Requirements:
    - 4+ years Python, FastAPI, Docker, and PostgreSQL.
    - Experience with Redis caching and asynchronous messaging (Celery/RabbitMQ).
    - Architecture review and API optimization.
    """

    sample_resume = """
    Software Engineer with 3 years building web apps.
    Stack: Python, Flask, SQLite, Celery, Git, and Docker.
    Built automated data processing pipelines and backend services.
    """

    final_state = run_application_pipeline(
        raw_resume=sample_resume,
        raw_jd=sample_jd,
        github_username="tiangolo"
    )

    print("=" * 60)
    print("📋 APPLICATION REPORT SUMMARY")
    print("=" * 60)
    print("\nMissing Skills:\n  - " + "\n  - ".join(final_state.missing_skills))
    print("\nResume Suggestions:\n  - " + "\n  - ".join(final_state.resume_suggestions))
    print("\nRecommended Projects to Highlight:")
    for proj in final_state.recommended_projects:
        print(f"  • {proj.project_name} (Score: {proj.alignment_score}/10): {proj.match_reason}")
    print("\nTailored Cover Letter Draft:\n")
    print(final_state.cover_letter_draft)