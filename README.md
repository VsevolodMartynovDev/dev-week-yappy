# Yappy Search API

A Django REST Framework backend for semantic search with tensor processing.

## Setup and Installation

1. Clone the repository
2. Create and activate a virtual environment (recommended)
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run migrations:
   ```
   python manage.py migrate
   ```
5. Start the development server:
   ```
   python manage.py runserver
   ```

## API Usage

### Search Endpoint

**URL**: `/api/search/`

**Method**: `GET`

**Body**:
```json
{
    "text": "Your search query or #hashtags"
}
```

**Response**:
```json
[
    "https://s3.ritm.media/hackaton-itmo/example1.mp4",
    "https://s3.ritm.media/hackaton-itmo/example2.mp4",
    "https://s3.ritm.media/hackaton-itmo/example3.mp4",
    "https://s3.ritm.media/hackaton-itmo/example4.mp4",
    "https://s3.ritm.media/hackaton-itmo/example5.mp4",
    "https://s3.ritm.media/hackaton-itmo/example6.mp4",
    "https://s3.ritm.media/hackaton-itmo/example7.mp4",
    "https://s3.ritm.media/hackaton-itmo/example8.mp4",
    "https://s3.ritm.media/hackaton-itmo/example9.mp4",
    "https://s3.ritm.media/hackaton-itmo/example10.mp4"
]
```

## Examples

### Search with Plain Text

```json
{
    "text": "mountain hiking adventure"
}
```

### Search with Hashtags

```json
{
    "text": "#mountain #hiking #adventure"
}
```
