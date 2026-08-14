def build_prompt(
    question: str,
    context: list[str],
    history: list[str],
) -> str:

    conversation = "\n".join(
        history,
    )

    joined_context = "\n\n".join(
        context,
    )


    return f"""
You are Atlas AI.

Answer ONLY using the provided context.

If the answer cannot be found,
say you don't know.

Conversation History:

{conversation}

Context:

{joined_context}

Question:

{question}
"""