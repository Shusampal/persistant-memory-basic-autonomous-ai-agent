def create_state(user_request, tasks, tools=[], memory=[], max_steps=5):
    return {
        "user_request": user_request,
        "available_tools": tools,
        "tasks": tasks,
        "available_memory": memory,
        "current_task": None,
        "current_step": 0,
        "max_steps": max_steps,
        "actions": [],
        "observations": [],
        "finished": False,
        "final_answer": ""
    }


def complete_task(state, task):
    normalized_task = (
        task
        .strip()
        .lower()
        .replace("_", " ")
    )

    for item in state["tasks"]:
        if item["task"] == normalized_task:
            item["status"] = "completed"
            return True

    return False


def add_action(state, action):
    state["actions"].append(action)


def record_observation(
    state,
    action,
    status,
    observation
):
    state["current_task"] = action
    state["observations"].append({
        "step": state["current_step"],
        "action": action,
        "status": status,
        "observation": observation
    })


def next_step(state):
    state["current_step"] += 1


def can_continue(state):
    return (
        not state["finished"]
        and state["current_step"] < state["max_steps"]
    )


def finish(state, answer):
    state["final_answer"] = answer
    state["finished"] = True


# def get_pending_tasks(state):
#     return [
#         item["task"]
#         for item in state["tasks"]
#         if item["status"] == "pending"
#     ]


# def all_tasks_completed(state):

#     if not state["tasks"]:
#         return False

#     return all(
#         item["status"] == "completed"
#         for item in state["tasks"]
#     )
