from langchain_google_genai import GoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage, BaseMessage

class IGenerativeAIService:
    def invoke(self, messages: list[BaseMessage]):
        pass

class GenerativeAIService:
    def __init__(self, llm_repository: IGenerativeAIService):
        self.llm_repository = llm_repository
        self.messages = []

    def invoke(self, user_message: str, system_message: str = None) -> str:
        if system_message:
            self.messages.append(SystemMessage(system_message))
        self.messages.append(HumanMessage(user_message))
        response = self.llm_repository.invoke(self.messages)
        self.messages = []
        return response.content