# 🧠 Second Brain

> A personal knowledge management system that stores your notes and lets you search and interact with them using AI.

**Second Brain** is a backend project built to explore how an AI-powered personal knowledge system can be designed from the ground up.

The project started with simple local JSON-based note storage and gradually evolved toward a more scalable architecture using **PostgreSQL, pgvector, embeddings, semantic search, and Gemini AI**.

The goal is to build a system where you can save what you learn, retrieve information using natural language, and eventually ask your knowledge base questions like a personal AI assistant.

---

## ✨ Features

### 📝 Note Management

Create, read, update, and delete notes through REST APIs.

* Create notes with a title and content
* Fetch all notes
* Fetch a note by ID
* Update existing notes
* Delete notes

### 🔎 Keyword Search

Search notes using traditional text-based matching.

The search checks both:

* Note title
* Note content

### 🧠 Semantic Search

Instead of relying only on exact keywords, Second Brain converts note content into vector embeddings.

This allows searches based on **meaning rather than exact words**.

For example:

```text
Query:
"How can I efficiently find an element in an ordered collection?"

```

can retrieve a note about:

```text
"Binary search repeatedly divides the search space in half."
```

even though the query doesn't contain the exact same words.

The project uses **Gemini embeddings** and PostgreSQL's **pgvector** extension for vector similarity search.

### 🤖 AI Study Assistant

The `/ask` endpoint uses Google's Gemini model to answer technical questions.

The AI is currently configured as a study assistant that explains technical concepts clearly and uses examples when useful.

---

## 🏗️ Architecture

The current architecture follows a simple layered approach:

```text
                Client / API Consumer
                        │
                        ▼
                 ┌─────────────┐
                 │   FastAPI   │
                 │  main.py    │
                 └──────┬──────┘
                        │
              ┌─────────┴─────────┐
              │                   │
              ▼                   ▼
      ┌───────────────┐    ┌──────────────┐
      │ NoteManager   │    │ AI Service   │
      │               │    │              │
      │ Business      │    │ Gemini LLM   │
      │ Logic         │    │ Embeddings   │
      └───────┬───────┘    └──────┬───────┘
              │                   │
              └─────────┬─────────┘
                        ▼
                ┌──────────────┐
                │ PostgreSQL   │
                │ + pgvector   │
                └──────────────┘
```

### Request Flow

When a note is created:

```text
User
  │
  ▼
POST /notes
  │
  ▼
FastAPI
  │
  ▼
NoteManager
  │
  ├── Generate Gemini embedding
  │
  └── Store title + content + embedding
          │
          ▼
      PostgreSQL
```

When a semantic search is performed:

```text
Search Query
     │
     ▼
Generate Query Embedding
     │
     ▼
PostgreSQL + pgvector
     │
     ▼
Vector Similarity Search
     │
     ▼
Top K Relevant Notes
```

---

## 🛠️ Tech Stack

| Component             | Technology        |
| --------------------- | ----------------- |
| Language              | Python            |
| API Framework         | FastAPI           |
| Database              | PostgreSQL        |
| Vector Search         | pgvector          |
| Database Driver       | psycopg           |
| AI Model              | Google Gemini     |
| Text Embeddings       | Gemini Embeddings |
| Environment Variables | python-dotenv     |
| API Documentation     | FastAPI / Swagger |

The repository currently contains separate modules for the API, database connection, note management, AI services, embeddings, and similarity experimentation.

---

## 📁 Project Structure

```text
secondBrain-versions/
│
├── main.py
│   └── FastAPI application and API endpoints
│
├── note_manager.py
│   └── Note CRUD operations and semantic search
│
├── database.py
│   └── PostgreSQL connection and pgvector registration
│
├── ai_service.py
│   └── Gemini AI and embedding functionality
│
├── embedding_search.py
│   └── Embedding and semantic-search experimentation
│
├── similarity.py
│   └── Similarity calculation experiments
│
├── generate_embeddings.py
│   └── Embedding generation experiments
│
├── models.py
│   └── Request/response models
│
├── embedding_test.py
│   └── Embedding-related experiments
│
├── test_ai.py
│   └── AI service tests
│
├── test_similarity.py
│   └── Similarity tests
│
├── notes.json
│   └── Earlier JSON-based note storage
│
├── requirements.txt
│   └── Python dependencies
│
└── .gitignore
```

The repository currently contains the code from different stages of the project's development, hence the `secondBrain-versions` name.

---

# 🚀 Getting Started

## Prerequisites

Make sure you have the following installed:

* Python 3.10+
* PostgreSQL
* PostgreSQL `pgvector` extension
* A Google Gemini API key

---

## 1. Clone the Repository

```bash
git clone https://github.com/vikrant987123/secondBrain-versions.git

cd secondBrain-versions
```

---

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure PostgreSQL

Create a PostgreSQL database:

```sql
CREATE DATABASE notes_db;
```

Enable the `pgvector` extension:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

The current database layer uses PostgreSQL with `pgvector` and registers vector support through `psycopg`.

### Database Configuration

Update the database connection in `database.py` according to your local PostgreSQL setup:

```python
DATABASE_URL = "postgresql://postgres:<password>@localhost:5432/notes_db"
```

> **Security note:** Avoid committing real database passwords or API keys to GitHub. Prefer environment variables such as `DATABASE_URL`.

---

## 5. Configure Gemini API

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
```

The application loads this variable using `python-dotenv` and initializes the Gemini client from it.

---

# ▶️ Running the Application

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

FastAPI also provides interactive API documentation at:

```text
http://127.0.0.1:8000/docs
```

---

# 📡 API Endpoints

## Get All Notes

```http
GET /notes
```

Returns all stored notes.

---

## Get a Note

```http
GET /notes/{note_id}
```

Example:

```http
GET /notes/1
```

---

## Create a Note

```http
POST /notes
```

Request:

```json
{
  "title": "Binary Search",
  "content": "Binary search works efficiently on sorted arrays."
}
```

When a note is created, its content is converted into an embedding before being stored.

---

## Update a Note

```http
PUT /notes/{note_id}
```

Request:

```json
{
  "title": "Binary Search Algorithm",
  "content": "Binary search repeatedly divides the search space in half."
}
```

---

## Delete a Note

```http
DELETE /notes/{note_id}
```

Example:

```http
DELETE /notes/1
```

---

## Keyword Search

```http
GET /notes/search?keyword=binary
```

This performs traditional text matching against the title and content of notes.

---

## 🧠 Semantic Search

```http
GET /notes/semantic-search?query=how to search efficiently&top_k=3
```

The query is converted into an embedding and compared against stored note embeddings using pgvector.

The API returns the most relevant notes based on vector distance.

Example response:

```json
[
  {
    "id": 1,
    "title": "Binary Search",
    "content": "Binary search works efficiently on sorted arrays.",
    "distance": 0.12
  }
]
```

---

# 🤖 Ask the AI

```http
POST /ask
```

Request:

```json
{
  "question": "Explain binary search with an example."
}
```

Response:

```json
{
  "answer": "Binary search is an efficient searching algorithm..."
}
```

The current implementation sends the question to Gemini with a study-assistant prompt.

---

# 🔍 Keyword Search vs Semantic Search

Second Brain currently supports two different approaches to finding information.

### Keyword Search

```text
Query
  ↓
Text Matching
  ↓
Matching Notes
```

Useful when you know the exact words you're looking for.

### Semantic Search

```text
Query
  ↓
Embedding
  ↓
Vector Similarity
  ↓
Relevant Notes
```

Useful when you remember the **concept** but not the exact wording.

For example:

```text
Stored note:
"Binary search repeatedly divides the search space in half."

Query:
"How can I make searching faster in a sorted array?"
```

A semantic search can identify the relationship between these two pieces of text even though their wording is different.

---

# 🧪 Development Journey

This repository intentionally contains multiple stages of development.

### Version 1 — JSON Storage

The project initially stored notes locally in:

```text
notes.json
```

This version focused on implementing basic CRUD operations without introducing a database. The earlier implementation can still be seen in the commented code inside `note_manager.py`.

### Version 2 — PostgreSQL

The project moved from local JSON storage to PostgreSQL to provide persistent structured storage.

### Version 3 — Embeddings

Notes started being converted into vector embeddings using Gemini.

### Version 4 — Semantic Search

PostgreSQL + pgvector was introduced to perform vector similarity searches directly in the database.

### Version 5 — AI Assistant

Gemini was integrated to allow users to ask technical questions through the `/ask` endpoint.

The repository is intended to preserve this progression so the development of the system can be followed step by step.

---

# 🎯 Future Roadmap

The current implementation is an early foundation for a much more capable Second Brain.

Possible future improvements:

* [ ] Connect semantic search results with the AI assistant
* [ ] Implement Retrieval-Augmented Generation (RAG)
* [ ] Ask questions specifically about saved notes
* [ ] Automatically summarize notes
* [ ] Generate tags using AI
* [ ] Support multiple types of knowledge sources
* [ ] Add authentication
* [ ] Add a frontend interface
* [ ] Improve database configuration using environment variables
* [ ] Add proper database migrations
* [ ] Add automated tests
* [ ] Add pagination
* [ ] Improve embedding management when notes are updated
* [ ] Add hybrid keyword + semantic search
* [ ] Add conversation history
* [ ] Build a personalized AI study assistant

---

# 🧩 What I Am Learning From This Project

This project is also being developed as a learning journey around modern backend and AI systems.

Key concepts explored include:

* REST API development with FastAPI
* Layered backend architecture
* PostgreSQL database integration
* Vector databases and pgvector
* Text embeddings
* Cosine similarity
* Semantic search
* AI API integration
* Environment variable management
* Retrieval-Augmented Generation
* Designing AI-powered backend systems

---

# 🤝 Contributing

This is primarily a personal learning project, but suggestions and improvements are welcome.

If you'd like to contribute:

```bash
git fork
git clone
git checkout -b feature/your-feature
```

Make your changes and open a pull request.

---

# 📜 License

This project is currently intended as a personal learning and development project.

Add a license here if/when the repository is released under a specific open-source license.

---

## ⭐ Project Status

🚧 **Work in Progress**

Second Brain is actively evolving from a basic note-taking API into a more complete AI-powered personal knowledge system.

The repository intentionally preserves different stages of development so that the evolution from **simple CRUD → database-backed notes → embeddings → semantic search → AI-assisted knowledge retrieval** can be followed.

---

## 🔗 Repository

[Second Brain — GitHub Repository](https://github.com/vikrant987123/secondBrain-versions?utm_source=chatgpt.com)

> **Build your memory. Search your knowledge. Let AI help you understand it. 🧠**
