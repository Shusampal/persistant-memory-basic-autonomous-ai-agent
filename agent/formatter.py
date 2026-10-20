import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()


GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL_NAME = os.getenv("GROQ_MODEL_NAME")


groq_client = Groq(api_key=GROQ_API_KEY)


def get_final_answer(state):

    formatter_prompt = f"""
    You are an AI answer formatter

    GOAL:
    Your goal is understand the user question, understand the full state of the agent and full a clean and human friendly and human simple language answer

    INSTRUCTIONS:
    1.you are only responsible to get a structured final answer and nothing else.
    2.give answer in a way human gives answer to another human.
    3.do not use special symbols if not needed.
    4.avoid jargons and hard words.
    5.use agent state as your only source of truth and nothing else.
    6.see all observations and user request and then decide what to provide as a final answer
    7.do not invent or guess answer
    8.be meticulous and do not hallucinate
    9.check memory in agent state very carefully.
    10.if you think answer to given user question can be made and done from available memory , use it

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
    the output should be a string and language should be simple
    eg - The current time is 10:54 PM
    """

    ai_response = groq_client.chat.completions.create(model=GROQ_MODEL_NAME, messages=[{
        'role': 'user',
        'content': formatter_prompt
    }])

    return ai_response.choices[0].message.content
