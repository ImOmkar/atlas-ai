from google import genai

from app.core.config import settings

client = genai.Client(
    api_key=settings.gemini_api_key,
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