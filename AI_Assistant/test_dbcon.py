from db import get_db_connection


# conn.close()

def get_claim_by_id(claim_id: str):  
    conn = get_db_connection()
    print("Database connection established successfully.")
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

print(get_claim_by_id("C0000001"))  # Replace with a valid claim ID for testing