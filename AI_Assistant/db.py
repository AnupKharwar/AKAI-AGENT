import pg8000

def get_db_connection():
    # Connect to the PostgreSQL database
    conn = pg8000.connect(
        host="localhost",
        port=5432,
        database="CAM",
        user="camuser",
        password="admin"
    )
    return conn