from typing import List, Optional
from pydantic import BaseModel, Field

class JobAnalysis(BaseModel):
    required_skills: List[str] = Field(default_factory=list)
    preferred_skills: List[str] = Field(default_factory=list)
    core_responsibilities: List[str] = Field(default_factory=list)
    tech_stack: List[str] = Field(default_factory=list)

class CandidateProfile(BaseModel):
    raw_resume_text: str = ""
    extracted_skills: List[str] = Field(default_factory=list)
    experience_years: Optional[float] = None
    notable_projects: List[str] = Field(default_factory=list)

class ProjectRecommendation(BaseModel):
    project_name: str
    match_reason: str
    alignment_score: int = Field(ge=1, le=10)

class ApplicationState(BaseModel):
    raw_resume_text: str = ""
    raw_job_description: str = ""
    github_username: Optional[str] = None
    
    job_analysis: Optional[JobAnalysis] = None
    candidate_profile: Optional[CandidateProfile] = None
    missing_skills: List[str] = Field(default_factory=list)
    resume_suggestions: List[str] = Field(default_factory=list)
    recommended_projects: List[ProjectRecommendation] = Field(default_factory=list)
    cover_letter_draft: Optional[str] = None