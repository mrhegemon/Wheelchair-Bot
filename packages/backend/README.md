# Backend Package

This package contains the backend API service for the Wheelchair Bot project.

## Features

- FastAPI-based REST API
- Health monitoring endpoints
- Movement control API
- Configuration management

## Development

### Setup

```bash
cd packages/backend
pip install -e ".[dev]"
```

### Running the server

```bash
python -m wheelchair_bot.main
```

Or with uvicorn directly:

```bash
uvicorn wheelchair_bot.main:app --reload
```

The API will be available at `http://localhost:8000`

### API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Testing

```bash
pytest
```

## API Endpoints

- `GET /` - API information
- `GET /health` - Health check
- `GET /api/status` - Get wheelchair bot status
- `POST /api/move` - Send movement commands
