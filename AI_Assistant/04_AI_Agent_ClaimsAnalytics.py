import asyncio

from mcp_client import (
    connect,
    disconnect,
    discover_tools
)

from agent_planner import planner
from agent_executor import execute_action
from agent_loop import run_agent_loop
from agent_answer import format_answer


async def main():

    client = await connect()

    tools = await discover_tools(client)

    print("\nChoose Your Agent Role\n")

    print("1. Claim Analytics")
    print("2. Provider")
    print("3. Payer")
    print("4. Healthcare Professional")
    print("5. Healthcare Researcher")

    choice = input("\nEnter your choice : ")

    print()
    print("Available Tools")
    print("----------------")

    for tool in tools:
        print(tool.name)

    user_request = input("\nUser : ")




    state = await run_agent_loop(
        user_request,
        planner,
        execute_action,
        format_answer,
        tools,
        client,
        choice
    )

    print()
    print("Final Answer:")
    print(state["final_answer"])

    await disconnect(client)


if __name__ == "__main__":
    asyncio.run(main())
