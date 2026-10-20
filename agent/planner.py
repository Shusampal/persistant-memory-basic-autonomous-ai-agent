import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()


GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL_NAME = os.getenv("GROQ_MODEL_NAME")


groq_client = Groq(api_key=GROQ_API_KEY)


def plan_next_action(state):

    planner_prompt = f"""
    You are an AI task planner

    GOAL:
    Your goal is understand the user question and the current state of the agent and suggest next action to perform

    INSTRUCTIONS:
    - you are only responsible to give next action to perform.
    - you have agent state data which will have lots of data.
    - please do not hallucinate and take a good look in the current state before planning next action
    - in case you decide a action, send only the tool name as a string.
    - agent state has many data which are discussed in AGENT STATE section below about what data and what those means.
    - be meticulous and use agent state as source of truth
    - check all observations and see the status of tasks which already has been performed.
    - if you see any task has been pending or failure , try it one more time.
    - one task should not be performed more than thrice.
    - if any task is not able to complete after thrice , you should return TERMINATE.
    - when you think all tasks listed are completed successfully, return FINISH
    - check available memory which is present in agent state carefully.
    - see if user question can be satisfied by available memory then return FINISH
    - in case you do not get a appropriate tool, just return FINISH as a string.

    AGENT STATE:
    - user_request: It contains the user's original question
    - available_tools: It contains all tools at your disposal. every tool can have ( tool_name , tool_description , input_schema)
    - tasks: this contains all tasks to be performed.
    - current_task: it tracks which task is curently performed.
    - current_step: it symbolizes which step we are currently at.
    - max_steps: it symbolizes how much steps agents can take at max.
    - actions: it is a list which has actions which has been performed
    - observations: it will have a list which will have detail of each observation.things like action , status , observation
    - finished: it symbolizes whether now we are finished or not of all tasks.
    - final_answer: it is last extracted answer which has to be presented to user
    - available_memory: It is last memories of agent , contains user_question and final_answer

    DATA:
    You will get all data in agent state below:
    {state}


    OUTPUT FORMAT:
    the output should be a string and nothing else
    eg - current_time
    """

    ai_response = groq_client.chat.completions.create(model=GROQ_MODEL_NAME, messages=[{
        'role': 'user',
        'content': planner_prompt
    }])

    return ai_response.choices[0].message.content
