from langchain_openai import ChatOpenAI
from src.config import settings


def make_llm(temp: float = 0.4):
    return ChatOpenAI(model="gpt-4o-mini", temperature=temp, api_key=settings.openai_api_key)