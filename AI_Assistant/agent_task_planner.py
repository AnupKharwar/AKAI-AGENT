import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)


def decompose_task(user_request):

    prompt = f"""
You are an AI task planner.

Your job is to create ONLY the minimum tasks
required to answer the user's request.

Rules:

1. Create ONLY tasks explicitly required.
2. Never ask follow-up questions.
3. Never ask for additional context.
4. Never create research tasks.
5. Never create validation tasks.
6. Never create explanation tasks unless requested.
7. Keep tasks short.
8. Put tasks in execution order.
9. Return one task per line.
10. Do not number tasks.
11. Do not explain anything.

Examples:

User:
What is the claim details of claim ID C0000004?

Output:
Retrieve claim ID C0000004 details

User:
What is CARC and RARC in claims denial?

Output:
Explain CARC and RARC in claims denial

User:
Get claim C0000005 and current time and generate a 10 digit password

Output:
Retrieve claim ID C0000005 details
Get current time
Generate 10-digit password

User Request:

{user_request}
"""

    response = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=[
            {
                "role": "system",
                "content":
                "Return only tasks. One task per line."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    result = response.choices[0].message.content.strip()

    tasks = []

    for line in result.splitlines():

        line = line.strip()

        if not line:
            continue

        # remove accidental numbering
        line = line.lstrip("1234567890.- ")

        tasks.append(line)

    return tasks