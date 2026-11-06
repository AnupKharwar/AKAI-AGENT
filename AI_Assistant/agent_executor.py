from mcp_client import execute_tool


async def execute_action(decision, state, client):

    tool_name = decision["tool"]

    arguments = decision.get(
        "arguments",
        {}
    )


    result = await execute_tool(
        client,
        tool_name,
        arguments
    )

    if hasattr(result, "content"):

        if result.content:

            return result.content[0].text

    return str(result)
