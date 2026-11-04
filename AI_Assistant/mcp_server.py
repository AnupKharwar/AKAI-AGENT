from datetime import datetime
from fastmcp import FastMCP
from db import get_db_connection

mcp = FastMCP("Time Server")

@mcp.tool()

def current_time():

    """Return the current date and time."""

    return datetime.now().strftime(
        "%d-%m-%Y %H:%M:%S"
    )


import random

@mcp.tool()

def roll_dice():

    """Roll a six-sided dice."""
    return random.randint(1,6)

import secrets
import string

@mcp.tool()

def generate_password(length: int = 12):

    """
    Generate a secure password.
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


@mcp.tool()

def get_claim_by_id(claim_id: str):
    """
    Returns claim details for a claim.

      Retrieve claim details by claim ID.

    Args:
        claim_id: Unique claim identifier such as 'C0000010'.

    Returns:
        Claim record from CLAIM_DETAIL table.
    """
    print(f"claim_id received: {claim_id}")
    conn = get_db_connection()
    cur = conn.cursor()
    query = """
    SELECT *
    FROM "CAM_ACCESS".CLAIM_DETAIL
    WHERE Claim_ID = %s
    """
    cur.execute(query, (claim_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row



if __name__ == "__main__":
    print("Starting MCP server..")
    mcp.run()
