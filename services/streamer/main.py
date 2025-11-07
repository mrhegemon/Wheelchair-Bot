"""
Streamer Service - Camera capture and WebRTC streaming
Handles video/audio streaming using libcamera/GStreamer and WebRTC
"""
import asyncio
import logging
import json
from typing import Dict, Optional

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn
from aiortc import RTCPeerConnection, RTCSessionDescription, VideoStreamTrack
from aiortc.contrib.media import MediaBlackhole, MediaPlayer, MediaRecorder
from av import VideoFrame
import fractions

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Data models
class StreamConfig(BaseModel):
    """Stream configuration model"""
    resolution: str = Field("640x480", description="Video resolution")
    framerate: int = Field(30, ge=1, le=60, description="Frames per second")
    device: str = Field("/dev/video0", description="Camera device")
    audio_enabled: bool = Field(True, description="Enable audio streaming")


class StreamStatus(BaseModel):
    """Stream status model"""
    active: bool
    peer_connections: int
    config: StreamConfig


# Application state
app_state = {
    "config": StreamConfig(),
    "peer_connections": {},
    "active_streams": 0
}


# FastAPI app
app = FastAPI(
    title="Streamer Service",
    description="Camera capture and WebRTC streaming service",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CameraStreamTrack(VideoStreamTrack):
    """
    A video track that reads from camera using GStreamer or libcamera
    Falls back to test pattern if camera is not available
    """
    
    def __init__(self, device="/dev/video0", resolution="640x480", framerate=30):
        super().__init__()
        self.device = device
        self.resolution = resolution
        self.framerate = framerate
        self.counter = 0
        
        # Try to initialize camera
        try:
            # In production, this would use GStreamer or libcamera
            # For now, we'll use a placeholder
            logger.info(f"Initializing camera: {device} at {resolution}@{framerate}fps")
        except Exception as e:
            logger.error(f"Camera initialization failed: {e}")
    
    async def recv(self):
        """Generate video frames"""
        pts, time_base = await self.next_timestamp()
        
        # In production, this would capture from camera
        # For now, generate a test pattern
        width, height = map(int, self.resolution.split('x'))
        frame = VideoFrame(width=width, height=height)
        
        # Simple test pattern
        for p in frame.planes:
            p.update(bytes([self.counter % 256] * (p.width * p.height)))
        
        self.counter += 1
        frame.pts = pts
        frame.time_base = time_base
        
        return frame


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "streamer",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/status", response_model=StreamStatus)
async def get_status():
    """Get current stream status"""
    return StreamStatus(
        active=app_state["active_streams"] > 0,
        peer_connections=len(app_state["peer_connections"]),
        config=app_state["config"]
    )


@app.get("/config", response_model=StreamConfig)
async def get_config():
    """Get current stream configuration"""
    return app_state["config"]


@app.post("/config", response_model=StreamConfig)
async def update_config(config: StreamConfig):
    """Update stream configuration"""
    app_state["config"] = config
    logger.info(f"Stream configuration updated: {config.dict()}")
    return config


@app.websocket("/ws/webrtc")
async def websocket_webrtc(websocket: WebSocket):
    """WebSocket endpoint for WebRTC signaling"""
    await websocket.accept()
    pc = RTCPeerConnection()
    pc_id = id(pc)
    app_state["peer_connections"][pc_id] = pc
    
    logger.info(f"WebRTC peer connection established: {pc_id}")
    
    try:
        # Add video track
        config = app_state["config"]
        video_track = CameraStreamTrack(
            device=config.device,
            resolution=config.resolution,
            framerate=config.framerate
        )
        pc.addTrack(video_track)
        app_state["active_streams"] += 1
        
        # Handle ICE connection state changes
        @pc.on("iceconnectionstatechange")
        async def on_ice_connection_state_change():
            logger.info(f"ICE connection state: {pc.iceConnectionState}")
            if pc.iceConnectionState == "failed":
                await pc.close()
        
        while True:
            message = await websocket.receive_json()
            msg_type = message.get("type")
            
            if msg_type == "offer":
                # Handle WebRTC offer
                offer = RTCSessionDescription(
                    sdp=message["sdp"],
                    type=message["type"]
                )
                await pc.setRemoteDescription(offer)
                
                # Create answer
                answer = await pc.createAnswer()
                await pc.setLocalDescription(answer)
                
                # Send answer
                await websocket.send_json({
                    "type": pc.localDescription.type,
                    "sdp": pc.localDescription.sdp
                })
                logger.info("WebRTC answer sent")
                
            elif msg_type == "ice_candidate":
                # Handle ICE candidate
                candidate = message.get("candidate")
                if candidate:
                    logger.info("ICE candidate received")
                
            elif msg_type == "close":
                break
    
    except WebSocketDisconnect:
        logger.info(f"WebRTC client disconnected: {pc_id}")
    except Exception as e:
        logger.error(f"WebRTC error: {e}")
    finally:
        # Cleanup
        if pc_id in app_state["peer_connections"]:
            del app_state["peer_connections"][pc_id]
        if app_state["active_streams"] > 0:
            app_state["active_streams"] -= 1
        await pc.close()


@app.on_event("startup")
async def startup_event():
    """Startup event"""
    logger.info("Streamer service starting up")


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event"""
    logger.info("Streamer service shutting down")
    # Close all peer connections
    for pc in app_state["peer_connections"].values():
        await pc.close()


def main():
    """Main entry point"""
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    )


if __name__ == "__main__":
    main()
