from ai_service import create_embedding
from similarity import cosine_similarity


notes = [
    "Binary search works efficiently on sorted arrays.",
    "A binary search repeatedly divides the search space in half.",
    "Python classes contain attributes and methods.",
    "FastAPI is a Python framework for building APIs."
]

embedded_notes = []

for note in notes:
    embedding = create_embedding(note)

    embedded_notes.append({
        "text": note,
        "embedding": embedding
    })

def semantic_search(query, embedded_notes, top_k=3):
    query_embedding = create_embedding(query)

    results = []

    for note in embedded_notes:
        score = cosine_similarity(
            query_embedding,
            note["embedding"]
        )

        results.append({
            "text": note["text"],
            "score": score
        })

    results.sort(
        key = lambda result: result["score"],
        reverse = True
    )

    return results[:top_k]


# for note in embedded_notes:
#     print("Text:", note["text"])
#     print("Vector size:", len( note["embedding"] ))
#     print("First 5:", note["embedding"][:5])
#     print()

# query = "How can I efficiently find an item in an ordered array?"
query = "What is object oriented programming?"

results = semantic_search(query,embedded_notes)

# query_embedding = create_embedding(query)

# print("Query:", query)
# print("Query vector size:", len(query_embedding))
# print("Query first 5:", query_embedding[:5])

# for note in embedded_notes:
#     score = cosine_similarity(
#         query_embedding,
#         note["embedding"]
#     )

#     print("Score:", score)
#     print("Note:", note["text"])
#     print()

print("\nSearch results:\n")

for result in results:
    print("Score:", result["score"])
    print("Note:", result["text"])
    print()