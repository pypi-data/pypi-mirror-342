from phi.agent import Agent,RunResponse
from phi.tools.youtube_tools import YouTubeTools
from phi.model.google import Gemini
from taskAI import config
from dotenv import load_dotenv
import os

load_dotenv()
def get_youtube_agent():
    return Agent(
        tools=[YouTubeTools()],
        show_tool_calls=True,
        model=Gemini(id=config.model), 
        description="You are a YouTube agent. Retrieve captions and summarize them.",
        markdown=True
    )