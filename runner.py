import asyncio
from agent_loop import agent_loop
from mcp_config.client import connect, discover_tools, disconnect
import json
import sqlite3


async def startup():
    client = await connect()
    connection = sqlite3.connect("memory.db")
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_question TEXT,
            final_answer TEXT,
            embedding TEXT
        )
    """)

    connection.commit()
    connection.close()

    tools = await discover_tools(client)

    tools_json = [
        {
            "tool_name": tool.name,
            "tool_description": tool.description,
            "input_schema": tool.input_schema,
        }
        for tool in tools
    ]
    # Convert to a JSON string
    tools_json = json.dumps(tools_json, indent=2)
    return (client, tools_json)


async def runner():
    print("="*40)
    print("Autonomous Agent with Persistent Memory")
    print("="*40)

    (client, tools) = await startup()

    while True:
        user_question = input("USER: ").strip().lower()

        if user_question in ["exit", "bye", "quit"]:
            print("AI: GoodBye !!!!")
            break

        state = await agent_loop(user_question, tools, client)

        if state["final_answer"] == "":
            print(f"AI: Sorry !! Terminatting")
            break

        print(f"AI: {state["final_answer"]}\n")

    await disconnect(client)


if __name__ == "__main__":
    asyncio.run(runner())
