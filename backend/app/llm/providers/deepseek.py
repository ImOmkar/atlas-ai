from openai import OpenAI

from app.core.config import settings

from app.llm.base import BaseLLMProvider


class DeepSeekProvider(
    BaseLLMProvider,
):

    def __init__(self):

        self.client = OpenAI(
            api_key=settings.deepseek_api_key,
            base_url=settings.deepseek_base_url,
        )

    def generate(
        self,
        prompt: str,
    ) -> str:

        response = self.client.chat.completions.create(

            model="deepseek-chat",

            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],

            temperature=0,
        )

        return (
            response
            .choices[0]
            .message
            .content
        )