"""
Safety Agent Service - Monitors E-stop and safety conditions
Ensures safe operation of the wheelchair robot
"""
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn
import aiohttp

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Data models
class SafetyConfig(BaseModel):
    """Safety configuration model"""
    check_interval_seconds: int = Field(1, ge=1, description="Safety check interval")
    command_timeout_seconds: int = Field(5, ge=1, description="Command timeout")
    enable_auto_estop: bool = Field(True, description="Enable automatic e-stop")
    teleopd_url: str = Field("http://localhost:8000", description="Teleopd service URL")


class SafetyStatus(BaseModel):
    """Safety status model"""
    estop_active: bool
    last_check_time: float
    last_command_time: Optional[float]
    command_timeout: bool
    monitoring_active: bool
    config: SafetyConfig


class Alert(BaseModel):
    """Safety alert model"""
    level: str = Field(..., description="Alert level: info, warning, critical")
    message: str
    timestamp: float = Field(default_factory=lambda: datetime.now().timestamp())


# Application state
app_state = {
    "config": SafetyConfig(),
    "estop_active": False,
    "last_check_time": None,
    "last_command_time": None,
    "monitoring_active": False,
    "monitoring_task": None,
    "alerts": []
}


# FastAPI app
app = FastAPI(
    title="Safety Agent Service",
    description="Safety monitoring and e-stop management",
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


async def check_teleopd_status():
    """Check teleopd service status"""
    config = app_state["config"]
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{config.teleopd_url}/status", timeout=2) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data
                else:
                    logger.error(f"Teleopd status check failed: {resp.status}")
                    return None
    except Exception as e:
        logger.error(f"Failed to check teleopd status: {e}")
        return None


async def trigger_estop(reason: str):
    """Trigger emergency stop on teleopd"""
    config = app_state["config"]
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{config.teleopd_url}/estop", timeout=2) as resp:
                if resp.status == 200:
                    logger.warning(f"E-STOP triggered: {reason}")
                    app_state["estop_active"] = True
                    add_alert("critical", f"E-STOP triggered: {reason}")
                    return True
                else:
                    logger.error(f"Failed to trigger e-stop: {resp.status}")
                    return False
    except Exception as e:
        logger.error(f"Failed to trigger e-stop: {e}")
        return False


def add_alert(level: str, message: str):
    """Add a safety alert"""
    alert = Alert(level=level, message=message)
    app_state["alerts"].append(alert.dict())
    # Keep only last 100 alerts
    if len(app_state["alerts"]) > 100:
        app_state["alerts"] = app_state["alerts"][-100:]


async def safety_monitor():
    """Main safety monitoring loop"""
    logger.info("Safety monitoring started")
    app_state["monitoring_active"] = True
    
    while app_state["monitoring_active"]:
        try:
            config = app_state["config"]
            app_state["last_check_time"] = datetime.now().timestamp()
            
            # Check teleopd status
            status = await check_teleopd_status()
            
            if status:
                # Update e-stop status
                app_state["estop_active"] = status.get("estop_active", False)
                app_state["last_command_time"] = status.get("last_command_time")
                
                # Check for command timeout
                if config.enable_auto_estop and app_state["last_command_time"]:
                    time_since_command = datetime.now().timestamp() - app_state["last_command_time"]
                    
                    if time_since_command > config.command_timeout_seconds:
                        if not app_state["estop_active"]:
                            await trigger_estop(f"Command timeout: {time_since_command:.1f}s")
            else:
                # Teleopd not responding
                if config.enable_auto_estop and not app_state["estop_active"]:
                    await trigger_estop("Teleopd service not responding")
            
            # Wait for next check
            await asyncio.sleep(config.check_interval_seconds)
            
        except asyncio.CancelledError:
            logger.info("Safety monitoring cancelled")
            break
        except Exception as e:
            logger.error(f"Safety monitoring error: {e}")
            await asyncio.sleep(config.check_interval_seconds)
    
    app_state["monitoring_active"] = False
    logger.info("Safety monitoring stopped")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "safety-agent",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/status", response_model=SafetyStatus)
async def get_status():
    """Get current safety status"""
    config = app_state["config"]
    last_cmd_time = app_state["last_command_time"]
    
    command_timeout = False
    if last_cmd_time:
        time_since_command = datetime.now().timestamp() - last_cmd_time
        command_timeout = time_since_command > config.command_timeout_seconds
    
    return SafetyStatus(
        estop_active=app_state["estop_active"],
        last_check_time=app_state["last_check_time"] or 0,
        last_command_time=last_cmd_time,
        command_timeout=command_timeout,
        monitoring_active=app_state["monitoring_active"],
        config=config
    )


@app.get("/config", response_model=SafetyConfig)
async def get_config():
    """Get current safety configuration"""
    return app_state["config"]


@app.post("/config", response_model=SafetyConfig)
async def update_config(config: SafetyConfig):
    """Update safety configuration"""
    app_state["config"] = config
    logger.info(f"Safety configuration updated: {config.dict()}")
    return config


@app.get("/alerts")
async def get_alerts(limit: int = 20):
    """Get recent safety alerts"""
    alerts = app_state["alerts"][-limit:]
    return {"alerts": alerts, "total": len(app_state["alerts"])}


@app.post("/alerts/clear")
async def clear_alerts():
    """Clear all alerts"""
    count = len(app_state["alerts"])
    app_state["alerts"] = []
    return {"cleared": count}


@app.post("/monitor/start")
async def start_monitoring():
    """Start safety monitoring"""
    if app_state["monitoring_active"]:
        return {"status": "already_running"}
    
    # Start monitoring task
    task = asyncio.create_task(safety_monitor())
    app_state["monitoring_task"] = task
    
    return {"status": "started"}


@app.post("/monitor/stop")
async def stop_monitoring():
    """Stop safety monitoring"""
    if not app_state["monitoring_active"]:
        return {"status": "not_running"}
    
    app_state["monitoring_active"] = False
    
    # Cancel monitoring task
    if app_state["monitoring_task"]:
        app_state["monitoring_task"].cancel()
        try:
            await app_state["monitoring_task"]
        except asyncio.CancelledError:
            pass
        app_state["monitoring_task"] = None
    
    return {"status": "stopped"}


@app.on_event("startup")
async def startup_event():
    """Startup event"""
    logger.info("Safety agent service starting up")
    # Auto-start monitoring
    await start_monitoring()


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event"""
    logger.info("Safety agent service shutting down")
    await stop_monitoring()


def main():
    """Main entry point"""
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8002,
        reload=True,
        log_level="info"
    )


if __name__ == "__main__":
    main()
