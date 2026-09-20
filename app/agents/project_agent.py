import os
import re
from typing import List, Optional
from github import Github
from github.GithubException import GithubException, RateLimitExceededException
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from app.llm import get_gemini_model
from app.state import JobAnalysis, ProjectRecommendation

class ProjectRecommendationList(BaseModel):
    recommendations: List[ProjectRecommendation] = Field(
        description="Ranked list of projects from best to worst fit."
    )

def sanitize_github_username(raw_input: str) -> str:
    """Extracts clean username if the user provided a full GitHub URL."""
    cleaned = raw_input.strip().rstrip('/')
    match = re.search(r"github\.com/([^/]+)$", cleaned)
    if match:
        return match.group(1)
    return cleaned.lstrip('@')

def fetch_user_github_projects(username_or_url: str, token: Optional[str] = None, max_repos: int = 10) -> List[dict]:
    """
    Pulls public repositories and extracts names, descriptions, 
    primary languages, topics, and truncated READMEs.
    """
    clean_username = sanitize_github_username(username_or_url)
    auth_token = token or os.getenv("GITHUB_TOKEN")
    gh = Github(auth_token) if auth_token else Github()
    
    repo_data = []
    try:
        user = gh.get_user(clean_username)
        repos = user.get_repos(sort="updated", direction="desc")
        
        count = 0
        for repo in repos:
            if repo.fork or count >= max_repos:
                continue
            
            readme_content = ""
            try:
                content_file = repo.get_readme()
                readme_content = content_file.decoded_content.decode("utf-8")[:1000]
            except GithubException:
                pass

            repo_data.append({
                "name": repo.name,
                "description": repo.description or "No description provided",
                "language": repo.language or "Unknown",
                "topics": repo.get_topics(),
                "readme_snippet": readme_content
            })
            count += 1
            
    except RateLimitExceededException:
        print(f"⚠️ GitHub API rate limit hit. Provide a GITHUB_TOKEN in .env for 5,000 requests/hr.")
        return []
    except GithubException as e:
        print(f"⚠️ Error fetching repos for {clean_username}: {e}")
        return []
        
    return repo_data

def recommend_projects_for_job(repos: List[dict], job_analysis: JobAnalysis) -> List[ProjectRecommendation]:
    if not repos:
        return []

    llm = get_gemini_model(temperature=0.0)
    structured_llm = llm.with_structured_output(ProjectRecommendationList)

    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a Principal Software Architect evaluating candidate portfolio projects.
Review the candidate's GitHub repositories against the target job requirements.
Select and rank the top 2-3 projects that best demonstrate the required skills and tech stack.
Give each an alignment score from 1 to 10 and justify why the candidate should highlight it."""),
        ("user", """
Target Job Analysis:
{job_analysis}

Candidate GitHub Repositories:
{repos}
""")
    ])

    chain = prompt | structured_llm
    result = chain.invoke({
        "job_analysis": job_analysis.model_dump_json(),
        "repos": str(repos)
    })

    return result.recommendations