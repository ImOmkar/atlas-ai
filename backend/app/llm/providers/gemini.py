from google import genai

from app.core.config import settings

client = genai.Client(
    api_key=settings.gemini_api_key,
)


from app.llm.base import BaseLLMProvider

from app.ai.gemini import (
    generate_response,
)


class GeminiProvider(
    BaseLLMProvider,
):

    def generate(
        self,
        prompt: str,
    ) -> str:

        return generate_response(
            prompt,
        )

def generate_response(
    prompt: str,
) -> str:

    response = client.models.generate_content(
        model=settings.gemini_chat_model,
        contents=prompt,
    )

    return response.text


def rewrite_query(
    prompt: str,
) -> str:

    response = client.models.generate_content(
        model=settings.gemini_chat_model,
        contents=prompt,
    )

    return response.text



def rerank_chunks(
    prompt: str,
) -> str:

    response = client.models.generate_content(
        model=settings.gemini_chat_model,
        contents=prompt,
    )

    return response.text



def plan_task(
    prompt: str,
) -> str:

    response = client.models.generate_content(
        model=settings.gemini_chat_model,
        contents=prompt,
    )

    return response.text.strip()



def choose_tool(
    prompt: str,
) -> str:

    response = client.models.generate_content(
        model=settings.gemini_chat_model,
        contents=prompt,
    )

    return response.text.strip()



def generate_tool_response(
    prompt: str,
) -> str:

    response = client.models.generate_content(
        model=settings.gemini_chat_model,
        contents=prompt,
    )

    return response.text.strip()


def generate_tool_arguments(
    prompt: str,
) -> str:

    response = client.models.generate_content(
        model=settings.gemini_chat_model,
        contents=prompt,
    )

    return response.text.strip()


def generate_execution_plan(
    prompt: str,
) -> str:

    response = client.models.generate_content(
        model=settings.gemini_chat_model,
        contents=prompt,
    )

    return response.text.strip()


def generate_execution_response(
    prompt: str,
) -> str:

    response = client.models.generate_content(
        model=settings.gemini_chat_model,
        contents=prompt,
    )

    return response.text.strip()


