from langchain_core.prompts import ChatPromptTemplate
from app.llm import get_gemini_model
from app.state import JobAnalysis

SYSTEM_PROMPT = """You are an expert Technical Recruiter and Job Description Analyst.
Your goal is to parse raw job descriptions and extract structured information with zero fluff.

Rules:
1. Extract explicit technical requirements and soft skills separately.
2. Highlight the core engineering responsibilities.
3. Group all identifiable tools, languages, and frameworks into the tech stack list.
4. If something is not explicitly mentioned or clearly implied, do not hallucinate it.
"""

def analyze_job_description(jd_text: str) -> JobAnalysis:
    llm = get_gemini_model(temperature=0.0)
    structured_llm = llm.with_structured_output(JobAnalysis)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("user", "Analyze the following job description:\n\n{jd_text}")
    ])
    
    chain = prompt | structured_llm
    return chain.invoke({"jd_text": jd_text})

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    
    sample_jd = """
    We are looking for a Senior Python Engineer to design distributed backend systems.
    Must have 4+ years with Python, FastAPI, Docker, and PostgreSQL.
    Experience with Redis, Celery, and AWS is a huge plus.
    """
    
    print("Testing JD Agent...")
    output = analyze_job_description(sample_jd)
    print(output.model_dump_json(indent=2))