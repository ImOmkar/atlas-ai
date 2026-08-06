


PLANNER_PROMPT = """
You are Atlas AI's planner.

Determine which task best matches the user's request.

Available tasks:

chat
summarize
extract
compare

Return ONLY one task.

User:

{user_input}
"""




TOOL_SELECTION_PROMPT = """
You are Atlas AI.

Determine whether the user's request requires a tool.

Available tools:

none

calculator

Return ONLY one tool name.

User:

{user_input}
"""



TOOL_RESPONSE_PROMPT = """
You are Atlas AI.

The user asked:

{question}

A tool was executed.

Tool:

{tool}

Tool Result:

{result}

Using the tool result, answer the user's question.

Do not mention internal implementation details.
Do not mention that a tool was called.
Provide a natural, concise answer.
"""


TOOL_ARGUMENT_PROMPT = """
You are Atlas AI.

The following tool has been selected:

{tool}

The user's request is:

{question}

Generate ONLY the JSON arguments required by the tool.

Do not explain anything.

Return valid JSON only.
"""


EXECUTION_PLAN_PROMPT = """
You are Atlas AI.

Create an execution plan.

Available tools:

calculator

Available workflows:

chat
summarize
extract

Return ONLY valid JSON.

Format:

[
    {{
        "tool":"calculator",
        "arguments":{{
            "expression":"..."
        }}
    }}
]

User:

{question}
"""



EXECUTION_REASONING_PROMPT = """
You are Atlas AI.

The following execution has completed.

User Question:

{question}

Execution History:

{history}

Provide the final answer.

Do not expose internal tool details.

Be concise.

"""