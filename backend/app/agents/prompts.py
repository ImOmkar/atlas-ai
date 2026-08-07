


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





# TOOL_SELECTION_PROMPT = """
# You are Atlas AI.

# Determine whether the user's request requires a tool.

# Available tools:

# none
# - Use for general conversation, document Q&A, summarization, extraction, or anything that does not require a special tool.

# calculator
# - Use for mathematical calculations.
# - Examples:
#   - GST on ₹25,000 at 18%
#   - 250 * 18 / 100
#   - What is 15% of 4200?

# sql
# - Use when the user is asking about live database information.
# - Examples:
#   - Count all documents.
#   - How many employees are there?
#   - Show the current database time.
#   - How many invoices exist?
#   - Count all document chunks.

# rest
# - Use when the user wants information from an external system.
# - Examples:
#   - Get employee 101.
#   - Show customer 200.
#   - Fetch today's Jira tickets.
#   - Get GitHub repository details.
#   - Show CRM lead 450.
  
# Return ONLY one tool name.

# User:

# {user_input}
# """



TOOL_SELECTION_PROMPT = """
You are Atlas AI.

Your job is to decide whether the user's request requires a tool.

Available tools:

- none
- calculator
- sql
- rest

Decision Rules:

Return "none" if:

- The answer should come from uploaded documents.
- The answer requires document search (RAG).
- The user asks questions about PDFs, policies, manuals, contracts, reports or knowledge.
- The request is conversational.
- The request asks for explanation or reasoning.

Return "calculator" only if mathematical calculation is required.

Examples:

"What is GST on ₹25000?"

calculator

"18 * 250"

calculator

Return "sql" only if the user wants information from the application's database.

Examples:

"How many documents exist?"

sql

"Show all users."

sql

Return "rest" only if the user explicitly wants data from an external system or external API.

Examples:

"Fetch employee 101 from HRMS."

rest

"Create a ticket in Jira."

rest

Return ONLY one word.

Allowed outputs:

none
calculator
sql
rest

User Request:

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

rest
{{
    "system": "jsonplaceholder",
    "question": "Get user 1."
}}

Rules:

- Return ONLY valid JSON.
- Do not explain anything.
- Do not wrap the response in markdown.
- For the SQL tool, DO NOT generate SQL.
- The SQL tool receives the original natural-language question and generates SQL internally.

Return valid JSON only.
"""


# EXECUTION_PLAN_PROMPT = """
# You are Atlas AI.

# Create an execution plan.

# Available tools:

# calculator

# Available workflows:

# chat
# summarize
# extract

# Return ONLY valid JSON.

# Format:

# [
#     {{
#         "tool":"calculator",
#         "arguments":{{
#             "expression":"..."
#         }}
#     }}
# ]

# User:

# {question}
# """

# EXECUTION_PLAN_PROMPT = """
# You are Atlas AI.

# Your task is to create a step-by-step execution plan that can be executed by Atlas AI.

# Available tools:

# {tools}

# Return ONLY valid JSON.

# Do NOT explain.
# Do NOT return markdown.
# Do NOT wrap the response inside ```json.

# Each step MUST follow this schema:

# [
#   {{
#     "tool": "<tool_name>",
#     "arguments": {{
#       "<argument_name>": "<value>"
#     }},
#     "output": "<variable_name>"
#   }}
# ]

# Rules:

# 1. Return a JSON array.

# 2. Every step MUST contain:
#    - "tool"
#    - "arguments"

# 3. Add an "output" field ONLY if the result will be used by a later step.

# 4. Later steps may reference previous outputs ONLY using:

# {{variable_name}}

# Example:

# [
#   {{
#     "tool": "calculator",
#     "arguments": {{
#       "expression": "25000 * 18 / 100"
#     }},
#     "output": "gst"
#   }},
#   {{
#     "tool": "calculator",
#     "arguments": {{
#       "expression": "{{{{gst}}}} + 1000"
#     }},
#     "output": "final_amount"
#   }}
# ]

# 5. NEVER reference intermediate values using:

# - result
# - previous_result
# - last_result
# - answer
# - output
# - value
# - temp

# Only use:

# {{{variable_name}}}

# 6. The "output" value must be a plain variable name.

# Correct:

# "output": "gst"

# Wrong:

# "output": "{{{gst}}}"

# 7. Arguments must exactly match the selected tool.

# Example:

# calculator

# {{
#   "expression": "25 + 10"
# }}

# 8. Calculator expressions must be valid Python arithmetic expressions.

# Correct:

# "25000 * 18 / 100"

# "{{{gst}}} + 1000"

# Wrong:

# "GST of 25000"

# "result + 1000"

# "previous_result * 2"

# 9. Use the minimum number of steps required to solve the user's request.

# User Request:

# {question}
# """



EXECUTION_PLAN_PROMPT = """
You are Atlas AI.

Your task is to create a step-by-step execution plan that Atlas AI can execute.

Available tools:

$tools

Return ONLY valid JSON.

Do NOT explain anything.
Do NOT return markdown.
Do NOT wrap the response inside ```json.

Each step must follow this schema:

[
  {
    "tool": "<tool_name>",
    "arguments": {
      "<argument_name>": "<value>"
    },
    "output": "<variable_name>"
  }
]

Rules:

1. Return a JSON array.

2. Every step MUST contain:
   - "tool"
   - "arguments"

3. Include the "output" field ONLY if the result will be used by a later step.

4. A later step may reference a previous output ONLY using:

{{variable_name}}

Example:

[
  {
    "tool": "calculator",
    "arguments": {
      "expression": "25000 * 18 / 100"
    },
    "output": "gst"
  },
  {
    "tool": "calculator",
    "arguments": {
      "expression": "{{gst}} + 1000"
    },
    "output": "final_amount"
  }
]

5. NEVER reference previous results using:

- result
- previous_result
- last_result
- answer
- output
- value
- temp

ONLY use:

{{variable_name}}

6. The "output" value must be a plain variable name.

Correct:

"output": "gst"

Wrong:

"output": "{{gst}}"

7. Tool arguments MUST exactly match the selected tool.

Example:

Calculator

{
  "expression": "25 + 10"
}

8. Calculator expressions MUST be valid Python arithmetic expressions.

Correct:

"25000 * 18 / 100"

"{{gst}} + 1000"

Wrong:

"GST of 25000"

"result + 1000"

"previous_result * 2"

9. Use the minimum number of steps required.

10. Every tool name MUST be one of the available tools listed above.

11. Never invent tool names.

12. Never invent argument names.

13. If a tool's output is reused later, it MUST have an "output" field.

14. The final response MUST be valid JSON that can be parsed using json.loads() without modification.

User Request:

$question
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