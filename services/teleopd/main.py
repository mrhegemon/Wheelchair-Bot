"""
Teleopd Service - Main teleoperation daemon
Handles WebSocket commands and REST API for configuration/status
"""
import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, List, Set

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Data models
class Command(BaseModel):
    """Command model for wheelchair control"""
    type: str = Field(..., description="Command type: move, stop, estop")
    direction: str | None = Field(None, description="Direction: forward, backward, left, right")
    speed: float | None = Field(None, ge=0.0, le=1.0, description="Speed value 0.0-1.0")
    timestamp: float = Field(default_factory=lambda: datetime.now().timestamp())


class Config(BaseModel):
    """Configuration model"""
    max_speed: float = Field(1.0, ge=0.0, le=1.0)
    enable_estop: bool = True
    control_mode: str = "joystick"
    timeout_seconds: int = 5


class Status(BaseModel):
    """Status model"""
    connected_clients: int
    last_command: str | None
    last_command_time: float | None
    estop_active: bool
    config: Config


# Application state
app_state = {
    "config": Config(),
    "last_command": None,
    "last_command_time": None,
    "estop_active": False,
    "active_connections": set()
}


# FastAPI app
app = FastAPI(
    title="Teleopd Service",
    description="Teleoperation daemon for wheelchair robot control",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ConnectionManager:
    """Manage WebSocket connections"""
    
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.add(websocket)
        logger.info(f"Client connected. Total connections: {len(self.active_connections)}")
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.discard(websocket)
        logger.info(f"Client disconnected. Total connections: {len(self.active_connections)}")
    
    async def broadcast(self, message: dict):
        """Broadcast message to all connected clients"""
        disconnected = set()
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Error broadcasting to client: {e}")
                disconnected.add(connection)
        
        # Clean up disconnected clients
        for conn in disconnected:
            self.disconnect(conn)


manager = ConnectionManager()


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "teleopd",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/status", response_model=Status)
async def get_status():
    """Get current service status"""
    return Status(
        connected_clients=len(manager.active_connections),
        last_command=app_state["last_command"],
        last_command_time=app_state["last_command_time"],
        estop_active=app_state["estop_active"],
        config=app_state["config"]
    )


@app.get("/config", response_model=Config)
async def get_config():
    """Get current configuration"""
    return app_state["config"]


@app.post("/config", response_model=Config)
async def update_config(config: Config):
    """Update configuration"""
    app_state["config"] = config
    logger.info(f"Configuration updated: {config.dict()}")
    
    # Broadcast config change to all clients
    await manager.broadcast({
        "type": "config_update",
        "config": config.dict()
    })
    
    return config


@app.post("/estop")
async def emergency_stop():
    """Trigger emergency stop"""
    app_state["estop_active"] = True
    app_state["last_command"] = "estop"
    app_state["last_command_time"] = datetime.now().timestamp()
    
    logger.warning("EMERGENCY STOP ACTIVATED")
    
    # Broadcast e-stop to all clients
    await manager.broadcast({
        "type": "estop",
        "timestamp": app_state["last_command_time"]
    })
    
    return {"status": "estop_activated"}


@app.post("/estop/reset")
async def reset_estop():
    """Reset emergency stop"""
    app_state["estop_active"] = False
    logger.info("Emergency stop reset")
    
    await manager.broadcast({
        "type": "estop_reset",
        "timestamp": datetime.now().timestamp()
    })
    
    return {"status": "estop_reset"}


@app.websocket("/ws/commands")
async def websocket_commands(websocket: WebSocket):
    """WebSocket endpoint for real-time commands"""
    await manager.connect(websocket)
    
    try:
        # Send initial status
        await websocket.send_json({
            "type": "connected",
            "config": app_state["config"].dict(),
            "estop_active": app_state["estop_active"]
        })
        
        while True:
            # Receive command from client
            data = await websocket.receive_json()
            
            # Validate command
            try:
                command = Command(**data)
            except Exception as e:
                await websocket.send_json({
                    "type": "error",
                    "message": f"Invalid command: {str(e)}"
                })
                continue
            
            # Check e-stop
            if app_state["estop_active"] and command.type != "estop":
                await websocket.send_json({
                    "type": "error",
                    "message": "E-stop is active. Reset e-stop before sending commands."
                })
                continue
            
            # Process command
            logger.info(f"Command received: {command.dict()}")
            app_state["last_command"] = command.type
            app_state["last_command_time"] = command.timestamp
            
            # Handle e-stop command
            if command.type == "estop":
                app_state["estop_active"] = True
                logger.warning("E-STOP via WebSocket")
            
            # Broadcast command to other clients (for monitoring)
            await manager.broadcast({
                "type": "command_executed",
                "command": command.dict()
            })
            
            # Send acknowledgment
            await websocket.send_json({
                "type": "ack",
                "command": command.type,
                "timestamp": datetime.now().timestamp()
            })
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        logger.info("WebSocket client disconnected")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        manager.disconnect(websocket)


@app.on_event("startup")
async def startup_event():
    """Startup event"""
    logger.info("Teleopd service starting up")


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event"""
    logger.info("Teleopd service shutting down")


def main():
    """Main entry point"""
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )


if __name__ == "__main__":
    main()
