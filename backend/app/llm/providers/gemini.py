from google import genai

from app.core.config import settings

from app.llm.base import BaseLLMProvider


class GeminiProvider(
    BaseLLMProvider,
):

    def __init__(self):

        self.client = genai.Client(
            api_key=settings.gemini_api_key,
        )

        self.model = settings.gemini_chat_model

    def generate(
        self,
        prompt: str,
    ) -> str:

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
        )

        return response.text.strip()



# def rewrite_query(
#     prompt: str,
# ) -> str:

#     response = client.models.generate_content(
#         model=settings.gemini_chat_model,
#         contents=prompt,
#     )

#     return response.text



# def rerank_chunks(
#     prompt: str,
# ) -> str:

#     response = client.models.generate_content(
#         model=settings.gemini_chat_model,
#         contents=prompt,
#     )

#     return response.text



# def plan_task(
#     prompt: str,
# ) -> str:

#     response = client.models.generate_content(
#         model=settings.gemini_chat_model,
#         contents=prompt,
#     )

#     return response.text.strip()



# def choose_tool(
#     prompt: str,
# ) -> str:

#     response = client.models.generate_content(
#         model=settings.gemini_chat_model,
#         contents=prompt,
#     )

#     return response.text.strip()



# def generate_tool_response(
#     prompt: str,
# ) -> str:

#     response = client.models.generate_content(
#         model=settings.gemini_chat_model,
#         contents=prompt,
#     )

#     return response.text.strip()


# def generate_tool_arguments(
#     prompt: str,
# ) -> str:

#     response = client.models.generate_content(
#         model=settings.gemini_chat_model,
#         contents=prompt,
#     )

#     return response.text.strip()


# def generate_execution_plan(
#     prompt: str,
# ) -> str:

#     response = client.models.generate_content(
#         model=settings.gemini_chat_model,
#         contents=prompt,
#     )

#     return response.text.strip()


# def generate_execution_response(
#     prompt: str,
# ) -> str:

#     response = client.models.generate_content(
#         model=settings.gemini_chat_model,
#         contents=prompt,
#     )

#     return response.text.strip()


