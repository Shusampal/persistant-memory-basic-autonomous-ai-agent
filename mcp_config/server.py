import secrets
import string
import random
from datetime import datetime

from fastmcp import FastMCP

mcp = FastMCP("My MCP Server")


@mcp.tool()
def current_time():
    """Return the current local date and time in DD-MM-YYYY HH:MM:SS format."""
    return datetime.now().strftime("%d-%m-%Y %H:%M:%S")


@mcp.tool()
def roll_dice():
    """Roll a fair six-sided die and return a random integer between 1 and 6."""
    return random.randint(1, 6)


@mcp.tool()
def generate_password(length: int = 12):
    """
    Generate a cryptographically secure random password.

    Args:
        length: The desired password length. Defaults to 12 characters.

    Returns:
        A randomly generated password containing letters, digits, and
        punctuation characters.
    """
    alphabet = (
        string.ascii_letters
        + string.digits
        + string.punctuation
    )

    return "".join(
        secrets.choice(alphabet)
        for _ in range(length)
    )


if __name__ == "__main__":
    mcp.run()
