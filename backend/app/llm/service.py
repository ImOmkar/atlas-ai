
from app.llm.providers.gemini import (
    GeminiProvider,
)

from app.llm.providers.deepseek import (
    DeepSeekProvider,
)

from app.llm.providers.groq import (
    GroqProvider,
)

from app.core.config import settings

class LLMService:

    def __init__(self):

        if settings.llm_provider == "gemini":

            self.provider = (
                GeminiProvider()
            )

        elif settings.llm_provider == "deepseek":

            self.provider = (
                DeepSeekProvider()
            )

        elif settings.llm_provider == "groq":

            self.provider = (
                GroqProvider()
            )

        else:

            raise ValueError(
                "Unsupported LLM Provider"
            )

    def generate(
        self,
        prompt: str,
    ):

        return self.provider.generate(
            prompt,
        )



if __name__ == "__main__":
    
    llm = LLMService()

    print(
        llm.generate(
            "Say Hello."
        )
    )