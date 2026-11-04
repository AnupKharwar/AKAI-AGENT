from mcp_client import execute_tool


async def execute_action(action, client):

    tool_name = action["tool"]
    arguments = action.get("arguments", {})

    result = await execute_tool(
        client,
        tool_name,
        arguments
    )

    if hasattr(result, "content"):

        if result.content:

            return result.content[0].text

    return str(result)
