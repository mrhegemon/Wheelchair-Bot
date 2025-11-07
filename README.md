# 🦽 Wheelchair Bot

A modern monorepo for wheelchair automation and control, featuring a FastAPI backend and React frontend.

## 📋 Overview

Wheelchair Bot is a comprehensive solution for controlling and monitoring a wheelchair bot through a web interface. The project is organized as a monorepo with separate packages for backend, frontend, and shared utilities.

## 🏗️ Project Structure

```
Wheelchair-Bot/
├── packages/
│   ├── backend/           # FastAPI REST API service
│   ├── frontend/          # React web interface
│   └── shared/            # Shared utilities and types
├── docs/                  # Documentation
├── pyproject.toml         # Root Python configuration
├── package.json           # Root workspace configuration
└── README.md              # This file
```

## ✨ Features

### Backend
- RESTful API built with FastAPI
- Health monitoring endpoints
- Movement control API
- Configuration management
- Comprehensive test suite

### Frontend
- Modern React-based UI
- Real-time status monitoring
- Intuitive movement controls
- Responsive design
- API integration via proxy

### Shared
- Common data models (Pydantic)
- Shared constants and utilities
- Type definitions

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- Node.js 18 or higher
- npm 9 or higher

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/mrhegemon/Wheelchair-Bot.git
   cd Wheelchair-Bot
   ```

2. **Install Python dependencies**
   ```bash
   # Install shared library
   cd packages/shared && pip install -e ".[dev]" && cd ../..
   
   # Install backend
   cd packages/backend && pip install -e ".[dev]" && cd ../..
   ```

3. **Install Node.js dependencies**
   ```bash
   npm install
   ```

### Running the Application

1. **Start the backend** (in one terminal):
   ```bash
   cd packages/backend
   python -m wheelchair_bot.main
   ```
   API available at: http://localhost:8000

2. **Start the frontend** (in another terminal):
   ```bash
   cd packages/frontend
   npm run dev
   ```
   Web interface available at: http://localhost:3000

## 📚 Documentation

- [Getting Started Guide](docs/getting-started.md)
- [Architecture Overview](docs/architecture.md)
- [Backend README](packages/backend/README.md)
- [Frontend README](packages/frontend/README.md)
- [Shared Library README](packages/shared/README.md)

## 🧪 Testing

Run backend tests:
```bash
cd packages/backend
pytest
```

Run shared library tests:
```bash
cd packages/shared
pytest
```

## 🛠️ Development

### Code Formatting
```bash
black packages/
```

### Linting
```bash
# Python
ruff check packages/

# JavaScript
cd packages/frontend && npm run lint
```

## 📝 API Endpoints

- `GET /` - API information
- `GET /health` - Health check
- `GET /api/status` - Get wheelchair bot status
- `POST /api/move` - Send movement commands
- Interactive docs at: http://localhost:8000/docs

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## 🔗 Links

- [API Documentation](http://localhost:8000/docs) (when backend is running)
- [GitHub Repository](https://github.com/mrhegemon/Wheelchair-Bot)