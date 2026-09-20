from typing import List
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from app.llm import get_gemini_model

class AnswerEvaluation(BaseModel):
    score: int = Field(ge=1, le=10, description="Score from 1 to 10 based on depth, correctness, and relevance.")
    strengths: List[str] = Field(description="Strong points in the candidate's answer.")
    weak_areas: List[str] = Field(description="Missing context or technical inaccuracies.")
    improved_answer_sample: str = Field(description="A concise, high-impact model answer.")

def evaluate_interview_answer(
    question: str, 
    ideal_talking_point: str, 
    candidate_answer: str
) -> AnswerEvaluation:
    llm = get_gemini_model(temperature=0.2)
    structured_llm = llm.with_structured_output(AnswerEvaluation)

    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a Senior Technical Hiring Manager and Interview Assessor.
Evaluate the candidate's response to an interview question.
Be rigorous, objective, and constructive. Provide a score (1-10), strengths, weak areas, and an improved sample answer."""),
        ("user", """
Question Asked:
{question}

Expected Talking Points:
{ideal_talking_point}

Candidate's Answer:
{candidate_answer}
""")
    ])

    chain = prompt | structured_llm
    return chain.invoke({
        "question": question,
        "ideal_talking_point": ideal_talking_point,
        "candidate_answer": candidate_answer
    })