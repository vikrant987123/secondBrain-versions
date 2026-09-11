import psycopg
from pgvector.psycopg import register_vector

DATABASE_URL = "postgresql://postgres:superuser@localhost:5432/notes_db"

def get_connection():
    conn = psycopg.connect(DATABASE_URL)
    register_vector(conn)
    return conn
    # return psycopg.connect(DATABASE_URL)


# One other thing: psycopg's with get_connection() as conn: handles committing a successful transaction and rolling back if an exception occurs, which is convenient for this small application.