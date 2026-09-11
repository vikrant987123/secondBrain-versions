# This will contain your API endpoints
from fastapi import FastAPI, HTTPException, status

from note_manager import NoteManager
from models import NoteCreate, NoteUpdate, AskRequest
from ai_service import ask_ai

app = FastAPI()

manager = NoteManager()

@app.get("/notes")
def get_notes():
    return manager.get_notes()

@app.get("/notes/search")
def search_notes(keyword: str):
    return manager.search_notes(keyword)

@app.get("/notes/semantic-search")
def semantic_search_notes(query: str, top_k: int = 3):

    return manager.semantic_search(
        query,
        top_k
    )

@app.get("/notes/{note_id}")
def get_note(note_id: int):
    note = manager.get_note(note_id)

    if note is None:
        raise HTTPException(
            status_code = 404,
            detail = "Note not found"
        )

    return note

@app.post("/notes")
def create_note(note: NoteCreate):
    return manager.add_note(
        note.title,
        note.content
    )

@app.put("/notes/{note_id}")
def update_note(note_id: int, note: NoteUpdate):

    updated_note = manager.update_note(
        note_id,
        note.title,
        note.content
    )

    if updated_note is None:
        raise HTTPException(
            status_code = 404,
            detail = "Note not found"
        )

    return updated_note

@app.delete("/notes/{note_id}")
def delete_note(note_id: int):
    deleted = manager.delete_note(note_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail = "Note not found"
        )

    return{
        "message" : "Note deleted successfully"
    }

@app.post("/ask")
def ask_question(request: AskRequest):
    answer = ask_ai(request.question)

    return {
        "answer": answer
    }

