# ⚡ CareerOS AI — Agentic Job Application Copilot

> An intelligent, autonomous multi-agent copilot that transforms standard job applications into high-signal, tailored submissions with real-time technical interview preparation.

[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Google Gemini](https://img.shields.io/badge/Model-Gemini%202.5%20Flash-4285F4?style=flat&logo=google&logoColor=white)](https://ai.google.dev/)
[![TailwindCSS](https://img.shields.io/badge/TailwindCSS-v3-38B2AC?style=flat&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)

---

## 🎯 Overview

**CareerOS AI** acts as an end-to-end "Operating System" for job seekers. Rather than relying on simple one-shot LLM prompts, CareerOS orchestrates an interconnected fleet of specialized, autonomous agents. The platform parses job requirements, evaluates candidate profiles, matches GitHub repositories, generates tailored cover letters, and runs an interactive mock interview studio with real-time scoring.

---

## 🏗️ Multi-Agent Architecture

```text
                                  [ Candidate Input ]
                         (Resume PDF/Text + Target JD + GitHub)
                                          │
                                          ▼
                             ┌─────────────────────────┐
                             │     orchestrator.py     │
                             └────────────┬────────────┘
                                          │
                  ┌───────────────────────┼───────────────────────┐
                  ▼                       ▼                       ▼
       ┌────────────────────┐   ┌───────────────────┐   ┌───────────────────┐
       │   JD Analyzer      │   │   Resume Parser   │   │  GitHub Profiler  │
       │     Agent          │   │      Agent        │   │     Agent         │
       └──────────┬─────────┘   └─────────┬─────────┘   └─────────┬─────────┘
                  │                       │                       │
                  └───────────────────────┼───────────────────────┘
                                          ▼
                               ┌─────────────────────┐
                               │    Gap Analysis     │
                               │        Agent        │
                               └──────────┬──────────┘
                                          │
                         ┌────────────────┴────────────────┐
                         ▼                                 ▼
              ┌─────────────────────┐           ┌─────────────────────┐
              │    Cover Letter     │           │   Interview Kit     │
              │       Agent         │           │       Agent         │
              └─────────────────────┘           └──────────┬──────────┘
                                                           │
                                                           ▼
                                                ┌─────────────────────┐
                                                │   Evaluator Agent   │
                                                │   (Live Scoring)    │
                                                └─────────────────────┘
🤖 The Agent Fleet
Agent	Module	Responsibility
Job Analyzer Agent	app/agents/jd_agent.py	Extracts hard requirements, tech stacks, domain concepts, and soft skills into structured Pydantic models.
Resume Parser Agent	app/agents/resume_agent.py	Extracts text from uploaded PDFs, parsing core experiences, skills, and projects.
GitHub Profiler Agent	app/agents/project_agent.py	Connects to the GitHub API, indexes public repositories, parses READMEs, and ranks matching projects (1–10).
Gap Analysis Agent	app/agents/matching_agent.py	Cross-analyzes JD requirements against the candidate's profile to identify missing skills and suggest high-impact resume tweaks.
Cover Letter Agent	app/agents/cover_letter_agent.py	Crafts a tailored cover letter referencing proven metrics and matching GitHub repositories.
Interview & Evaluator Agents	
app/agents/interview_agent.py


app/agents/evaluator_agent.py

Synthesizes targeted technical and behavioral interview questions focused on identified gaps; provides real-time evaluations, scoring (1–10), and model answers.
🛠️ Tech Stack
Backend: FastAPI (Python 3.10+)
AI Orchestration: Google Gemini (gemini-3-flash-preview) via LangChain Google GenAI
Frontend: Vanilla HTML5, Tailwind CSS (CDN), Lucide Icons, Vanilla JavaScript
Templating: Jinja2
Integrations: PyGithub (GitHub REST API), PyPDF (Document Parsing)
📂 Repository Structure
Plaintext
CareerOS---AI/
├── app/
│   ├── agents/
│   │   ├── cover_letter_agent.py   # Tailored pitch writer
│   │   ├── evaluator_agent.py      # Real-time answer scoring & feedback
│   │   ├── interview_agent.py      # Dynamic interview question generator
│   │   ├── jd_agent.py             # Structured job description analyzer
│   │   ├── matching_agent.py       # Gap analysis and resume suggestions
│   │   ├── project_agent.py        # GitHub API repository ranker
│   │   └── resume_agent.py         # PDF parsing and profile extraction
│   ├── llm.py                      # Centralized Gemini LLM client configuration
│   ├── orchestrator.py             # Multi-agent state pipeline coordinator
│   └── state.py                    # Pydantic schemas and application state
├── templates/
│   └── index.html                  # Responsive UI workspace
├── .env.example                    # Sample environment variables
├── .gitignore                      # Git exclusion rules
├── main.py                         # FastAPI application entrypoint & API routes
└── requirements.txt                # Project dependencies
🚀 Quickstart Guide
1. Clone the Repository
Bash
git clone [https://github.com/nausheenali02/CareerOS---AI.git](https://github.com/nausheenali02/CareerOS---AI.git)
cd CareerOS---AI
2. Set Up Virtual Environment
Bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
3. Configure Environment Variables
Create a .env file in the root directory:
Bash
GEMINI_API_KEY=your_gemini_api_key_here
GOOGLE_API_KEY=your_gemini_api_key_here
GITHUB_TOKEN=your_github_classic_token_here  # Optional: prevents rate-limiting
4. Run the Application
Bash
python main.py
Open your browser and navigate to:
Plaintext
[http://127.0.0.1:8000](http://127.0.0.1:8000)
