import os 
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key = os.getenv("GEMINI_API_KEY")
)

notes = [
    "Binary search works efficiently on sorted arrays.",
    "A binary search repeatedly divides the search space in half.",
    "Python classes contain attributes and methods.",
    "FastAPI is a Python framework for building APIs."
]

for note in notes:

    response = client.models.embed_content(
        model = "gemini-embedding-001",
        contents=note
    )

    embedding = response.embeddings[0].values

    print("\nNOTE:")
    print(note)
    print("Number of dimensions:", len(embedding))
    print("First 5 numbers:", embedding[:5])