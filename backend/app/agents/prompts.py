


# PLANNER_PROMPT = """
# You are Atlas AI's planner.

# Determine which task best matches the user's request.

# Available tasks:

# chat
# summarize
# extract
# compare

# Return ONLY one task.

# User:

# {user_input}
# """


PLANNER_PROMPT = """
You are Atlas AI.

Determine the user's intent.

Available tasks:

CHAT
- General conversation.
- Document question answering.
- Mathematical calculations.
- Database questions.
- Questions that require tools such as calculator or SQL.
- Examples:
  - How many casual leaves are allowed?
  - GST on ₹25000 at 18%
  - Count all documents.
  - Show current database time.
  - How many employees are there?

SUMMARIZE
- Summarize an entire document.
- Examples:
  - Summarize this document.
  - Give me a summary of the HR policy.

EXTRACT
- Extract structured information from a document.
- Examples:
  - Extract invoice fields.
  - Extract bank statement transactions.
  - Extract employee details into JSON.

COMPARE
- Compare two or more documents.

Return ONLY one task name.

User:

{user_input}
"""





TOOL_SELECTION_PROMPT = """
You are Atlas AI.

Determine whether the user's request requires a tool.

Available tools:

none
- Use for general conversation, document Q&A, summarization, extraction, or anything that does not require a special tool.

calculator
- Use for mathematical calculations.
- Examples:
  - GST on ₹25,000 at 18%
  - 250 * 18 / 100
  - What is 15% of 4200?

sql
- Use when the user is asking about live database information.
- Examples:
  - Count all documents.
  - How many employees are there?
  - Show the current database time.
  - How many invoices exist?
  - Count all document chunks.

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


# TOOL_ARGUMENT_PROMPT = """
# You are Atlas AI.

# The following tool has been selected:

# {tool}

# The user's request is:

# {question}

# Generate ONLY the JSON arguments required by the tool.

# Do not explain anything.

# Return valid JSON only.
# """


TOOL_ARGUMENT_PROMPT = """
You are Atlas AI.

The following tool has been selected:

{tool}

The user's request is:

{question}

Generate ONLY the JSON arguments required for the selected tool.

Tool schemas:

calculator
{{
    "expression": "<mathematical expression>"
}}

sql
{{
    "question": "<original user question>"
}}

Rules:

- Return ONLY valid JSON.
- Do not explain anything.
- Do not wrap the response in markdown.
- For the SQL tool, DO NOT generate SQL.
- The SQL tool receives the original natural-language question and generates SQL internally.

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