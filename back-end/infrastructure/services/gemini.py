from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import BaseMessage
from domain.services.generative_ai import IGenerativeAIService
from common.constants import GEMINI_API_KEY

class GeminiService(IGenerativeAIService):
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model='gemini-2.5-flash',
            google_api_key=GEMINI_API_KEY
        )
    
    def invoke(self, messages: list[BaseMessage]):
        return self.llm.invoke(messages)
