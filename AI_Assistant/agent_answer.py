from openai import OpenAI
from dotenv import load_dotenv
import os

from agent_planner import planner
from agent_executor import execute_action
from agent_loop import run_agent_loop


load_dotenv()

client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)


def format_answer(state):

    prompt = f"""
The user asked:
{state["user_request"]}

Tasks:
{state["tasks"]}

Actions performed:
{state["actions"]}

Observations:
{state["observations"]}

Intermediate Results:
{state["results"]}

Give the user a natural and concise answer.

Do not mention:
- planner
- agent loop
- MCP
- internal state
- tools
- internal reasoning

"""
    roles = {
    "1": "You are a Claim Analytics. Explain the claims details with Diagnosis and Procedure code description and include Notes with 2 lines of summary.",

    "2": "You are a Provider. Explain the claims details with Diagnosis and Procedure code description and include Notes with 2 lines of summary with denial reasons.",

    "3": "You are a Payer. Explain the claims details with Diagnosis and Procedure code description and include Notes with 2 lines of summary with denial amount, reasons and outstanding day and balance.",

    "4": "You are a Healthcare Professional. Describe claims details including medical conditions and treatments clearly.",

    "5": "You are a Healthcare Researcher. You are an expert in healthcare research and can provide insights into the latest studies and findings."
    }


    response = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=[
            {
                    "role": "system",
                    "content": roles.get(
                        state["agent_role"],
                        "You are a helpful AI assistant."
                    )
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content.strip()
