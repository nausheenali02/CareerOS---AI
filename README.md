# 🤖 CareerOS — AI 
live: https://careeros-ai-qllj.onrender.com

> **An AI-powered multi-agent career copilot that analyzes job descriptions, resumes, and GitHub projects to provide personalized career insights and interview preparation.**

CareerOS — AI streamlines the job application process by connecting **Job Description Analysis, Resume Parsing, GitHub Profiling, Gap Analysis, Cover Letter Generation, and AI Interview Evaluation** into one intelligent workflow.

---

## ✨ Features

* 🔍 **Job Analysis** — Extracts technical requirements, tech stack, domain concepts, and soft skills from JDs.
* 📄 **Resume Parsing** — Extracts skills, education, experience, and projects from PDF resumes.
* 💻 **GitHub Profiling** — Analyzes public repositories and ranks projects based on relevance to the target role.
* 🧩 **Gap Analysis** — Compares the candidate profile with job requirements and identifies missing skills.
* ✍️ **Cover Letter Generation** — Creates tailored cover letters using relevant skills and projects.
* 🎯 **Interview Preparation** — Generates technical and behavioral questions based on the JD and identified gaps.
* 📊 **Answer Evaluation** — Scores interview responses from 1–10 and provides feedback and model answers.

---

## 🤖 Agent Fleet

| Agent              | File                    | Responsibility                           |
| ------------------ | ----------------------- | ---------------------------------------- |
| 🔍 Job Analyzer    | `jd_agent.py`           | Analyzes job descriptions                |
| 📄 Resume Parser   | `resume_agent.py`       | Extracts candidate profile from PDFs     |
| 💻 GitHub Profiler | `project_agent.py`      | Analyzes and ranks GitHub projects       |
| 🧩 Gap Analysis    | `matching_agent.py`     | Finds skill gaps and resume improvements |
| ✍️ Cover Letter    | `cover_letter_agent.py` | Generates tailored cover letters         |
| 🎯 Interview       | `interview_agent.py`    | Generates targeted interview questions   |
| 📊 Evaluator       | `evaluator_agent.py`    | Evaluates interview answers              |

---

## 🧠 Architecture

```text
              Job Description
                     │
                     ▼
              ┌─────────────┐
              │ Job Analyzer│
              └──────┬──────┘
                     │
     ┌───────────────┼───────────────┐
     ▼               ▼               ▼
  Resume          GitHub          Job Profile
  Agent           Agent              │
     └───────────────┼───────────────┘
                     ▼
              ┌─────────────┐
              │ Gap Analysis│
              └──────┬──────┘
                     │
          ┌──────────┼──────────┐
          ▼          ▼          ▼
       Resume     Cover      Interview
       Tips       Letter       Agent
                                │
                                ▼
                           Evaluator
```

The workflow is coordinated through a centralized **Orchestrator** with structured **Pydantic state models**.

---

## 🛠️ Tech Stack

**Backend:** FastAPI, Python 3.10+, Pydantic, Jinja2
**AI:** Google Gemini `gemini-3-flash-preview`, LangChain Google GenAI
**Frontend:** HTML5, Tailwind CSS, Vanilla JavaScript, Lucide Icons
**Integrations:** PyGithub, PyPDF

---

## 📂 Project Structure

```text
CareerOS---AI/
├── app/
│   ├── agents/
│   │   ├── jd_agent.py
│   │   ├── resume_agent.py
│   │   ├── project_agent.py
│   │   ├── matching_agent.py
│   │   ├── cover_letter_agent.py
│   │   ├── interview_agent.py
│   │   └── evaluator_agent.py
│   ├── llm.py
│   ├── orchestrator.py
│   └── state.py
├── templates/
│   └── index.html
├── .env.example
├── main.py
└── requirements.txt
```

---

## 🚀 Getting Started

### 1. Clone

```bash
git clone https://github.com/nausheenali02/CareerOS---AI.git
cd CareerOS---AI
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
```

For Windows:

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure `.env`

```env
GEMINI_API_KEY=your_gemini_api_key
GOOGLE_API_KEY=your_gemini_api_key
GITHUB_TOKEN=your_github_token
```

`GITHUB_TOKEN` is optional but helps avoid GitHub API rate limits.

### 5. Run

```bash
python main.py
```

Open:

```text
http://127.0.0.1:8000
```

---

## 🔮 Future Scope

* LinkedIn & portfolio analysis
* Personalized learning roadmap
* Job tracking and analytics
* Voice-based mock interviews
* Coding interview agent
* Persistent candidate profiles

---

## 👩‍💻 Author

**Nausheen Ali**
B.Tech CSE | AI/ML

* GitHub: `github.com/nausheenali02`
* LinkedIn: `linkedin.com/in/nausheen-ali-72583628a/`
* Email: `nausheenali839@gmail.com`

---

⭐ **CareerOS — AI: Analyze → Match → Improve → Apply → Prepare**
