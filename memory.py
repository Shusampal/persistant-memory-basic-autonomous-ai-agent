import numpy as np
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import os
import sqlite3
import json
load_dotenv()

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
model = SentenceTransformer(EMBEDDING_MODEL)


def create_embedding(text):
    return model.encode(text)


def get_cosine_similarity(vector1, vector2):
    v1 = np.array(vector1)
    v2 = np.array(vector2)

    return np.dot(v1, v2)/(
        np.linalg.norm(v1) * np.linalg.norm(v2)
    )


def get_semantic_memory(user_question, top_k=3, threshold=0.0):

    user_question_embedding = create_embedding(user_question)

    connection = sqlite3.connect("memory.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT 
            user_question , 
            final_answer , 
            embedding 
        FROM memory
    """)

    rows = cursor.fetchall()

    connection.close()

    results = []

    for row in rows:
        (user_question, final_answer, embedding) = row

        embedding_vector = json.loads(embedding)

        cosine_score = get_cosine_similarity(
            user_question_embedding, embedding_vector)

        if cosine_score > threshold:
            results.append({
                "cosine_score": cosine_score,
                "user_question": user_question,
                "final_answer": final_answer,
            })

    results.sort(key=lambda item: item["cosine_score"], reverse=True)

    return results[:top_k]


def add_semantic_memory(user_question, final_answer):

    full_text = user_question + "" + final_answer
    full_text_embedding = create_embedding(full_text)

    connection = sqlite3.connect("memory.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO memory (user_question, final_answer, embedding)
        VALUES (?, ?, ?)
        """,
        (user_question, final_answer, json.dumps(full_text_embedding.tolist())),
    )

    connection.commit()
    connection.close()
