# # This will contain your OOP/business logic.

from database import get_connection
from ai_service import create_embedding

class NoteManager:
    def add_note(self, title, content):
        embedding = create_embedding(content)

        with get_connection() as conn:
            with conn.cursor() as cursor:

                cursor.execute(
                    """
                    INSERT INTO notes (title, content, embedding)
                    VALUES (%s, %s, %s)
                    RETURNING id, title, content
                    """,
                    (title,content,embedding)
                )

                note = cursor.fetchone()

        return {
            "id": note[0],
            "title": note[1],
            "content": note[2]
        }

    def get_notes(self):
        with get_connection() as conn:
            with conn.cursor() as cursor:

                cursor.execute(
                    """
                    SELECT id, title, content
                    FROM notes
                    ORDER BY id
                    """
                )

                notes = cursor.fetchall()

        return [
            {
                "id": note[0],
                "title": note[1],
                "content": note[2]
            }
            for note in notes
        ]

    def get_note(self, note_id):
        with get_connection() as conn:
            with conn.cursor() as cursor:

                cursor.execute(
                    """
                    SELECT id, title, content
                    FROM notes
                    WHERE id = %s
                    """,
                    (note_id,)
                )

                note = cursor.fetchone()

        if note is None:
            return None

        return {
            "id": note[0],
            "title": note[1],
            "content": note[2]
        }

    def search_notes(self, keyword):
        with get_connection() as conn:
            with conn.cursor() as cursor:

                cursor.execute(
                    """
                    SELECT id, title, content
                    FROM  notes
                    WHERE title ILIKE %s
                        OR content ILIKE %s
                    ORDER BY id
                    """,
                    (f"%{keyword}%",f"%{keyword}%")
                )

                notes = cursor.fetchall()

        return [
            {
                "id": note[0],
                "title": note[1],
                "content": note[2]
            }
            for note in notes
        ]

    def update_note(self, note_id, title, content):
        with get_connection() as conn:
            with conn.cursor() as cursor:

                cursor.execute(
                    """
                    UPDATE notes
                    SET title = %s,
                        content = %s
                    WHERE id = %s
                    RETURNING id, title, content
                    """,
                    (title, content, note_id)
                )

                note = cursor.fetchone()

        if note is None:
            return None

        return {
            "id": note[0],
            "title": note[1],
            "content": note[2]
        }

    def delete_note(self, note_id):
        with get_connection() as conn:
            with conn.cursor() as cursor:

                cursor.execute(
                    """
                    DELETE FROM notes
                    WHERE id = %s
                    """,
                    (note_id,)
                )

                deleted = cursor.rowcount > 0

        return deleted

    def semantic_search(self, query, top_k=3):
        query_embedding = create_embedding(query)

        with get_connection() as conn:
            with conn.cursor() as cursor:

                cursor.execute(
                    """
                    SELECT
                        id,
                        title,
                        content,
                        embedding <=> %s::vector AS distance
                    FROM notes
                    WHERE embedding IS NOT NULL
                    ORDER BY embedding <=> %s::vector
                    LIMIT %s
                    """,
                    (
                        query_embedding,
                        query_embedding,
                        top_k
                    )
                )

                notes = cursor.fetchall()

        return [
            {
                "id": note[0],
                "title": note[1],
                "content": note[2],
                "distance": note[3]
            }
            for note in notes
        ]
    
# import os
# import json

# class NoteManager:
#     def __init__(self):
#         self.notes = self.load_notes()

#     def load_notes(self):
#         if not os.path.exists("notes.json"):
#             return []
        
#         try:
#             with open("notes.json","r") as file:
#                 return json.load(file)
#         except (json.JSONDecodeError,EOFError):
#             return []
        
#     def save_notes(self): #it will save notes 
#         with open("notes.json","w") as file:
#             json.dump(self.notes,file,indent=4)

#     def add_note(self, title, content):
#         if self.notes:
#             new_id = max( note["id"] for note in self.notes) + 1
#         else:
#             new_id = 1

#         note = {
#             "id": new_id,
#             "title": title,
#             "content": content
#         }

#         self.notes.append(note)
#         self.save_notes()

#         return note


#     def get_notes(self):#will return all notes
#         return self.notes

#     def get_note(self, note_id):
#         for note in self.notes:
#             if note["id"] == note_id:
#                 return note

#         return None

#     def search_notes(self,keyword):#based on keyword it gives note from the keyword
#         keyword = keyword.lower()

#         return [
#             note 
#             for note in self.notes
#             if keyword in note["title"].lower()
#             or keyword in note["content"].lower()
#         ]

#     def update_note(self, note_id, title, content):
#         note = self.get_note(note_id)

#         if note is None:
#             return None

#         note["title"] = title
#         note["content"] = content

#         self.save_notes()

#         return note

#     def delete_note(self,note_id):
        
#         note = self.get_note(note_id)
#                 # #Re-number remaining notes
#                 # for index, note in enumerate(self.notes, start=1):
#                 #     note["id"] = index
        
#         if note is None:
#             return False

#         self.notes.remove(note)
#         self.save_notes()
                
#         return True