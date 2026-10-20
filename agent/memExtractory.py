from groq import Groq
from dotenv import load_dotenv
import os


load_dotenv()


GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL_NAME = os.getenv("GROQ_MODEL_NAME")


groq_client = Groq(api_key=GROQ_API_KEY)


def memory_extractor(user_question, final_answer):

    extractor_prompt = f"""
        You are an AI memory extractor
    
        GOAL:
        Your goal is understand the user question,final answer and return if something should be stored as a memory
    
        INSTRUCTIONS:
        1.you are only responsible to extract memory.
        2.understand user question and final answer very carefully.
        3.evaluate if for the user question and answer, anything should be stored as mempry.
        4.if yes, return the exact memory string which should be stored.
        5.if you feel nothing should be stored as memory return NONE
        6.do not hallucinate
        7.do not invent or guess memory
    
        DATA:
        user question: {user_question}
        final answer: {final_answer}
    
    
        OUTPUT FORMAT:
        the output should be a string and language should be simple
        eg - 

        user_question: my name is Rahul
        final_answe: great to meet you rahul

        you can return - user's name is Rahul
        """

    ai_response = groq_client.chat.completions.create(model=GROQ_MODEL_NAME, messages=[{
        'role': 'user',
        'content': extractor_prompt
    }])

    return ai_response.choices[0].message.content
