import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()


GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL_NAME = os.getenv("GROQ_MODEL_NAME")

groq_client = Groq(api_key=GROQ_API_KEY)


def task_decomposer(user_question):

    decomposer_prompt = f"""
    You are an AI task decomposer

    GOAL:
    Your goal is understand the user question and give independent tasks which is required to fulfill a user question

    INSTRUCTIONS:

    - If user gives a statement, return ""
    - You are only responsible to give steps which are required to fulfill a user question.
    - Please provide the task names in sequential order which are required to satisfy a user question.
    - Please provide task in simple words and clear words.
    - separate each task in a new line.
    - each task should be small and independent.
    - do not invent any random task.
    - do not hallucinate please
    - be as meticulous as you can.
    - Iterate multiple times before you come up with a final answer
    - Do not give steps for things not mentioned in user question
    - if user gives some statement, rather than asking question you can return "" . eg - my name is rahul ( this is a statement rather than question )

    DATA:

    user quesion: {user_question}


    OUTPUT FORMAT:

    see you have to give list of task and each task will be in single line

    eg - 

    create a password
    get current time

    """

    ai_response = groq_client.chat.completions.create(model=GROQ_MODEL_NAME, messages=[{
        'role': 'user',
        'content': decomposer_prompt
    }])

    return ai_response.choices[0].message.content
