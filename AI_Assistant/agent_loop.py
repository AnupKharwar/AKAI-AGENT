from agent_state import (
    create_state,
    add_task,
    add_action,
    record_observation,
    add_result,
    complete_task,
    all_tasks_completed,
    next_step,
    can_continue,
    finish
)

from agent_task_planner import (
    decompose_task
)


async def run_agent_loop(
    user_request,
    planner,
    execute_action,
    format_answer,
    tools,
    client,
    agent_role
):

    state = create_state(user_request)

    state["agent_role"] = agent_role

    # --------------------------------
    # Step 1: Create Task Plan
    # --------------------------------

    planned_tasks = decompose_task(
        user_request
    )

    for task in planned_tasks:

        add_task(
            state,
            task
        )

    print("\nTask Plan")
    print("---------")

    for item in state["tasks"]:

        print(
            "-",
            item["task"]
        )

    # --------------------------------
    # Main Loop
    # --------------------------------

    while can_continue(state):

        # --------------------------------
        # Finished?
        # --------------------------------

        if all_tasks_completed(state):

            print(
                f"\n--- Step {state['current_step'] + 1} ---"
            )

            print("Planner Decision:")
            print("FINISH")

            answer = format_answer(
                state
            )

            finish(
                state,
                answer
            )

            break

        print(
            f"\n--- Step {state['current_step'] + 1} ---"
        )

        # --------------------------------
        # Planner
        # --------------------------------

        decision = planner(
            state,
            tools
        )

        print(
            "Planner Decision:"
        )

        print(decision)

        # --------------------------------
        # FINISH
        # --------------------------------

        if (
            isinstance(decision, str)
            and decision.strip().upper() == "FINISH"
        ):

            answer = format_answer(
                state
            )

            finish(
                state,
                answer
            )

            break

        # --------------------------------
        # Validate
        # --------------------------------

        if not isinstance(
            decision,
            dict
        ):

            add_result(
                state,
                "Planner returned invalid format."
            )

            next_step(state)

            continue

        action = decision.get(
            "action"
        )

        task_name = decision.get(
            "task"
        )

        if not action:

            add_result(
                state,
                "Planner returned no action."
            )

            next_step(state)

            continue

        if not task_name:

            add_result(
                state,
                "Planner returned no task."
            )

            next_step(state)

            continue

        # ==================================
        # ANSWER_DIRECTLY
        # ==================================

        if action == "ANSWER_DIRECTLY":

            print(
                f"Answering directly for task: "
                f"{task_name}"
            )

            add_action(
                state,
                {
                    "action":
                    "ANSWER_DIRECTLY",
                    "task":
                    task_name
                }
            )

            complete_task(
                state,
                task_name
            )

            add_result(
                state,
                f"Answered directly: "
                f"{task_name}"
            )

            print(
                f"Task Completed: "
                f"{task_name}"
            )

            next_step(state)

            continue

        # ==================================
        # USE_TOOL
        # ==================================

        if action != "USE_TOOL":

            add_result(
                state,
                f"Unknown action: {action}"
            )

            next_step(state)

            continue

        tool_name = decision.get(
            "tool"
        )

        arguments = decision.get(
            "arguments",
            {}
        )

        if not tool_name:

            add_result(
                state,
                "Planner did not provide a tool."
            )

            next_step(state)

            continue

        # --------------------------------
        # Validate Tool
        # --------------------------------

        available_tools = {
            tool.name
            for tool in tools
        }

        if tool_name not in available_tools:

            add_result(
                state,
                f"Unknown tool: {tool_name}"
            )

            next_step(state)

            continue

        state["current_task"] = (
            task_name
        )

        # --------------------------------
        # Execute Tool
        # --------------------------------

        try:

            observation = await execute_action(
                decision,
                state,
                client
            )

        except Exception as ex:

            observation = (
                f"Error: {str(ex)}"
            )

        print(
            "Observation:",
            observation
        )

        # --------------------------------
        # Update State
        # --------------------------------

        add_action(
            state,
            {
                "action":
                "USE_TOOL",
                "task":
                task_name,
                "tool":
                tool_name,
                "arguments":
                arguments
            }
        )

        record_observation(
            state,
            tool_name,
            observation
        )

        add_result(
            state,
            observation
        )

        # --------------------------------
        # Complete Task
        # --------------------------------

        if (
            isinstance(
                observation,
                str
            )
            and not observation.lower().startswith(
                "error"
            )
        ):

            complete_task(
                state,
                task_name
            )

            print(
                f"Task Completed: "
                f"{task_name}"
            )

        else:

            add_result(
                state,
                "Tool execution failed."
            )

        # --------------------------------
        # Debug Status
        # --------------------------------

        print("\nTask Status:")

        for task in state["tasks"]:

            print(
                f"{task['task']} "
                f"=> "
                f"{task['status']}"
            )

        next_step(state)

    return state