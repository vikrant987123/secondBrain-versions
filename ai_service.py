import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def ask_ai(question):
    response = client.models.generate_content(
        model = "gemini-3.5-flash-lite",
        contents = (
            "You are a helpful study assistant."
            "Explain technical concepts clearly and simply."
            "Use examples when helpful.\n\n"
            f"Question:{question}"
        )
    )

    return response.text

def create_embedding(text):
    response = client.models.embed_content(
        model = "gemini-embedding-001",
        contents = text
    )

    return response.embeddings[0].values