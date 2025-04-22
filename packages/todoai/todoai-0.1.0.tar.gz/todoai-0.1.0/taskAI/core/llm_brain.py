from taskAI import config
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import Runnable


llm = None


def init_llm():
    global llm
    if not config.api_key:
        raise ValueError("Gemini API key not set. Run taskAI.setup() first.")
    
    llm = ChatGoogleGenerativeAI(
        model=config.model,
        google_api_key=config.api_key,
        temperature=0.7
    )

def run_llm(prompt: str) -> str:
    if llm is None:
        init_llm()
    return llm.invoke(prompt).content