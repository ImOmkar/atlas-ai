

SUMMARY_PROMPT = """
You are Atlas AI.

Summarize the following document.

Requirements:

- Preserve important facts.
- Keep section names if present.
- Use bullet points where appropriate.
- Do not invent information.
- Base the summary only on the document.

Document:

{document}
"""