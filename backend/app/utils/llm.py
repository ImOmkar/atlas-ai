import json


def clean_llm_json(
    text: str,
) -> str:

    return (
        text
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )


def parse_llm_json(
    text: str,
):

    return json.loads(
        clean_llm_json(text)
    )