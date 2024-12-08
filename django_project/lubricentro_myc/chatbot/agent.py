from pydantic_ai import Agent
from pydantic_ai.models.gemini import GeminiModel

from django_project.settings import GEMINI_API_KEY

model = GeminiModel("gemini-1.5-flash", api_key=GEMINI_API_KEY)
agent = Agent(model)
