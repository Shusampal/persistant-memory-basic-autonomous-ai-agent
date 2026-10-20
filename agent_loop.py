from agent.decomposer import task_decomposer
from agent.formatter import get_final_answer
from agent.memExtractory import memory_extractor
from agent.planner import plan_next_action
from agent.state import add_action, create_state, can_continue, finish, next_step, record_observation
from mcp_config.client import execute_tool
from memory import add_semantic_memory, get_semantic_memory


async def agent_loop(user_question, tools, client):

    # Step 1 ( run decomposer to get all taks )
    steps = task_decomposer(user_question)

    # Step 2 ( parse the tasks )
    parsed_tasks = []
    if steps != "":
        parsed_tasks = [line.strip() for line in steps.splitlines()]

    # Step 3 ( get semantic available memory )
    memory = get_semantic_memory(user_question)

    # Step 3 ( create a agent state )
    agent_state = create_state(user_question, parsed_tasks, tools, memory)

    # Step 4 ( start loop )
    while can_continue(agent_state):
        next_action = plan_next_action(agent_state)

        if next_action.strip().lower() == 'finish':
            # all tasks are completed
            # get structured answer
            # update agent state
            # add memory if needed
            # present to user
            final_answer = get_final_answer(agent_state)
            finish(agent_state, final_answer)
            memory_extracted = memory_extractor(user_question, final_answer)
            if memory_extracted != "NONE":
                add_semantic_memory(user_question, final_answer)
            return agent_state
        elif next_action.strip().lower() == 'none':
            # no available tool can acheive
            # we just mark it success in agent
            # continue with next task
            add_action(agent_state, next_action)
            record_observation(
                agent_state,
                next_action,
                "success",
                "This step is ignored intentionally"
            )
            next_step(agent_state)
            continue
        elif next_action.strip().lower() == 'terminate':
            # agent has run into action
            # terminate whole agent process
            # give appropriate error to user
            return agent_state
        else:
            # available tool has been selected
            # execute the action
            # update the agent state
            # continue the loop
            tool_result = await execute_tool(client, next_action)
            add_action(agent_state, next_action)
            record_observation(
                agent_state,
                next_action,
                "success",
                tool_result
            )
            next_step(agent_state)

    return agent_state
