# Yappy - Semantic Video Search

A Django application with semantic video search capabilities using sentence transformers and FAISS.

## Features

- Semantic search for videos based on descriptions and transcriptions
- Vector similarity search using pgvector or FAISS
- Web interface and API for searching
- Embedded video player in search results

## Getting Started with Docker

### Prerequisites

- Docker and Docker Compose installed on your system

### Running the Application

1. Clone this repository:
   ```
   git clone <repository-url>
   cd yappy
   ```

2. Start the application with Docker Compose:
   ```
   docker-compose up -d
   ```

3. The application will be available at http://localhost:8000/

### Database Setup

The first time you run the application, you'll need to set up the database schema and create the pgvector extension:

1. Connect to the database container:
   ```
   docker-compose exec db psql -U postgres
   ```

2. Create the vector extension:
   ```sql
   CREATE EXTENSION IF NOT EXISTS vector;
   ```

3. Exit the PostgreSQL shell:
   ```
   \q
   ```

## API Usage

The API is available at `/api/search/` and accepts GET requests with a `text` parameter:

```
GET /api/search/?text=your search query
```

## Web Interface

The web interface is available at `/search/` and provides a simple search form that returns video results with embedded players.

## Development

To run the application locally without Docker:

1. Set up a virtual environment:
   ```
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the development server:
   ```
   python manage.py runserver
   ```

## License

[Your license information]
