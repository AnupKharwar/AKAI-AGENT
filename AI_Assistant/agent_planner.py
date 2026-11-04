import json

from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)


def build_tool_descriptions(tools):

    descriptions = ""
   
    for tool in tools:

        schema = getattr(tool, "input_schema", {})

        descriptions += f"""
Tool:
{tool.name}

Description:
{tool.description}

Schema:
{json.dumps(schema, indent=2)}

Required Parameters:
{schema.get("required", [])}
----------------------------
"""

    return descriptions

def planner(state, tools):

    tool_descriptions = build_tool_descriptions(tools)
    example = """
    {
        "tool": "get_claim_by_id",
        "arguments": {
            "claim_id": "C0000010"
        }
    }
    """
    prompt = f"""
You are an AI Planner.

Your job is to decide ONLY the next action.

User Request:
{state["user_request"]}

Completed Actions:
{state["actions"]}

Previous Observations:
{state["observations"]}

Available Tools:
{tool_descriptions}

Rules:

1. Choose only ONE next action.
2. Never repeat an action that has already been completed.
3. Use the observations to decide what is still required.
4. If the user's request has been completely satisfied, return FINISH.
6. Do not explain your answer.
7. Extract tool arguments from the user request.
8. Follow the Input Schema exactly.
9. Return ONLY tool name with valid JSON.
Example:{example}

If complete return:

FINISH

Next Action:
"""

    response = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=[
            {
                "role": "system",
                "content": "You are an AI planner."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    # return response.choices[0].message.content.strip()
    content = response.choices[0].message.content.strip()
    if content == "FINISH":
        return "FINISH"

    return json.loads(content)

