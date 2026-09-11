# This will contain the data structure that the API acceps/returns.

from pydantic import BaseModel

class NoteCreate(BaseModel):
    title: str
    content: str
"""
This means FastAPI expects a request like:

{
    "title": "Python OOP",
    "content": "Learning classes and objects"
}
"""

class NoteUpdate(BaseModel):
    title: str
    content: str

class AskRequest(BaseModel):
    question: str