import json
import os

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)


def build_tool_descriptions(tools):

    descriptions = ""

    for tool in tools:

        schema = getattr(
            tool,
            "input_schema",
            {}
        )

        descriptions += f"""
Tool Name:
{tool.name}

Description:
{tool.description}

Input Schema:
{json.dumps(schema, indent=2)}

----------------------------------
"""

    return descriptions


def planner(state, tools):

    tool_descriptions = build_tool_descriptions(
        tools
    )

    pending_tasks = [
        item["task"]
        for item in state["tasks"]
        if item["status"] == "pending"
    ]

    prompt = f"""
You are an AI Planner.

User Request:
{state["user_request"]}

Pending Tasks:
{pending_tasks}

Completed Actions:
{state["actions"]}

Observations:
{state["observations"]}

Results:
{state["results"]}

Available Tools:
{tool_descriptions}

Rules:

1. Select exactly ONE pending task.
2. Copy the task EXACTLY.
3. Use only the tool names shown above.
4. Do not invent tool names.
5. Do not change tool names.
6. Do not add parentheses to tool names.
7. Extract all required arguments.

If a tool is required return:

{{
    "action": "USE_TOOL",
    "task": "<exact pending task>",
    "tool": "<tool name>",
    "arguments": {{}}
}}

Examples:

{{
    "action": "USE_TOOL",
    "task": "Retrieve claims details for claim ID C0000005",
    "tool": "get_claim_by_id",
    "arguments": {{
        "claim_id": "C0000005"
    }}
}}

{{
    "action": "USE_TOOL",
    "task": "Get current time",
    "tool": "current_time",
    "arguments": {{}}
}}

{{
    "action": "USE_TOOL",
    "task": "Generate 10-digit password",
    "tool": "generate_password",
    "arguments": {{
        "length": 10
    }}
}}

If NO available tool is needed:

{{
    "action": "ANSWER_DIRECTLY",
    "task": "<exact pending task>"
}}

Example:

{{
    "action": "ANSWER_DIRECTLY",
    "task": "Explain CARC and RARC"
}}

If there are no pending tasks return:

FINISH

Return JSON only.
Do not explain.
"""

    response = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=[
            {
                "role": "system",
                "content":
                "Return only FINISH or valid JSON."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    content = response.choices[0].message.content

    if not content:
        raise ValueError(
            "Planner returned empty content."
        )

    content = content.strip()

    print("\n===== PLANNER RAW OUTPUT =====")
    print(content)
    print("==============================\n")

    if content.upper() == "FINISH":
        return "FINISH"

    if content.startswith("```"):

        content = (
            content
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

    try:

        decision = json.loads(content)

        if not isinstance(decision, dict):

            raise ValueError(
                "Planner did not return JSON object."
            )

        action = decision.get("action")

        if not action:

            raise ValueError(
                "Planner response missing action."
            )

        if action == "USE_TOOL":

            if "task" not in decision:

                raise ValueError(
                    "USE_TOOL missing task."
                )

            if "tool" not in decision:

                raise ValueError(
                    "USE_TOOL missing tool."
                )

            if "arguments" not in decision:

                decision["arguments"] = {}

        elif action == "ANSWER_DIRECTLY":

            if "task" not in decision:

                raise ValueError(
                    "ANSWER_DIRECTLY missing task."
                )

        else:

            raise ValueError(
                f"Unknown action: {action}"
            )

        return decision

    except Exception as ex:

        print(
            "\n===== INVALID PLANNER OUTPUT ====="
        )

        print(content)

        print(
            "==================================\n"
        )

        raise ValueError(
            f"Planner returned invalid JSON: {ex}"
        )