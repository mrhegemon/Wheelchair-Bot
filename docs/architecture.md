# Architecture

This document describes the architecture of the Wheelchair Bot project.

## Overview

Wheelchair Bot is a monorepo containing three main packages:

1. **Backend** - FastAPI-based REST API service
2. **Frontend** - React-based web interface
3. **Shared** - Common utilities and types

## Component Diagram

```
┌─────────────────┐
│    Frontend     │
│   (React App)   │
└────────┬────────┘
         │ HTTP/REST
         │
┌────────▼────────┐
│     Backend     │
│  (FastAPI API)  │
└────────┬────────┘
         │
┌────────▼────────┐
│  Hardware/Bot   │
│   Interface     │
└─────────────────┘
```

## Backend (packages/backend)

The backend is built with FastAPI and provides a REST API for controlling the wheelchair bot.

### Key Components:

- **main.py** - FastAPI application with route definitions
- **config.py** - Configuration management using Pydantic
- **wheelchair_bot/** - Main package directory

### API Endpoints:

- `GET /` - API information
- `GET /health` - Health check
- `GET /api/status` - Get bot status
- `POST /api/move` - Send movement commands

## Frontend (packages/frontend)

The frontend is a React application built with Vite.

### Key Components:

- **App.jsx** - Main application component with controls
- **main.jsx** - Entry point
- **vite.config.js** - Vite configuration with API proxy

### Features:

- Real-time status display
- Movement controls (forward, backward, left, right, stop)
- Responsive design

## Shared (packages/shared)

The shared package contains common code used by both backend and frontend (primarily backend in this case).

### Key Components:

- **types.py** - Pydantic models for data validation
- **constants.py** - Shared constants

### Models:

- `Direction` - Enum for movement directions
- `BotStatus` - Status of the wheelchair bot
- `MoveCommand` - Movement command structure

## Communication Flow

1. User interacts with Frontend UI
2. Frontend sends HTTP request to Backend API
3. Backend validates request and sends command to hardware
4. Backend returns response to Frontend
5. Frontend updates UI with new status

## Technology Stack

### Backend:
- FastAPI - Web framework
- Uvicorn - ASGI server
- Pydantic - Data validation
- Python 3.9+

### Frontend:
- React 18
- Vite - Build tool
- Modern JavaScript (ES6+)

### Development Tools:
- pytest - Testing
- black - Code formatting
- ruff - Linting
- ESLint - JavaScript linting

## Future Enhancements

- WebSocket support for real-time updates
- Authentication and authorization
- Database for logging and analytics
- Mobile app interface
- Video streaming integration
- Sensor data integration
