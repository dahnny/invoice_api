# INVOICE API

This is a simple invoice API built with FastAPI, PostgreSQL, and Docker. It allows you to create, retrieve, update, and delete invoices. The API also supports user authentication and authorization.

## Features
- Create, retrieve, update, and delete invoices
- User authentication and authorization
- PDF generation for invoices
- Email notifications for invoice events
- Docker support for easy deployment
- Celery for background tasks

## Requirements
- Python 3.8 or higher
- PostgreSQL
- Docker (for deployment)
- Docker Compose (for local development)

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/invoice-api.git
   cd invoice-api
   ```
2. Create a `.env` file in the root directory and set the required environment variables. You can use the `.env.example` file as a reference.
3. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the database migrations:
   ```bash
   alembic upgrade head
   ```
5. Start the application:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```
6. (Optional) If you want to run the application using Docker, use the following command:
   ```bash
   docker-compose up --build
   ```   

## Usage
You can access the API at `http://localhost:8000`. The API documentation is available at `http://localhost:8000/docs`.

## Running Tests
To run the tests, use the following command:
```bash
pytest
```

