import os
from langchain_google_genai import ChatGoogleGenerativeAI

def get_gemini_model(temperature: float = 0.0):
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    return ChatGoogleGenerativeAI(
        model="gemini-3-flash-preview",
        temperature=temperature,
        google_api_key=api_key,
    )