# this file is to generate embeddings for the rows which has null in the embedding column

from database import get_connection
from ai_service import create_embedding

with get_connection() as conn:
    with conn.cursor() as cursor:

        cursor.execute(
            """
            SELECT id, title, content
            FROM notes
            WHERE embedding IS NULL
            """
        )

        notes = cursor.fetchall()

        for note_id, title, content in notes:

            text = f"{title}\n{content}"

            embedding = create_embedding(text)

            cursor.execute(
                """
                UPDATE notes
                SET embedding = %s
                WHERE id = %s
                """,
                (embedding, note_id)
            )
