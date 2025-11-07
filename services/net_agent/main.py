"""
Net Agent Service - Network monitoring and management
Monitors LTE/Wi-Fi status, DNS, and secure access
"""
import asyncio
import logging
import subprocess
from datetime import datetime
from typing import Dict, List, Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn
import psutil

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Data models
class NetworkInterface(BaseModel):
    """Network interface information"""
    name: str
    type: str  # wifi, ethernet, cellular
    status: str  # up, down
    ip_address: Optional[str] = None
    mac_address: Optional[str] = None
    signal_strength: Optional[int] = None  # For wireless interfaces


class NetworkConfig(BaseModel):
    """Network configuration"""
    check_interval_seconds: int = Field(5, ge=1, description="Network check interval")
    primary_interface: Optional[str] = Field(None, description="Primary network interface")
    dns_servers: List[str] = Field(default_factory=lambda: ["8.8.8.8", "8.8.4.4"])
    enable_fallback: bool = Field(True, description="Enable automatic fallback")


class NetworkStatus(BaseModel):
    """Network status"""
    interfaces: List[NetworkInterface]
    active_interface: Optional[str]
    internet_accessible: bool
    dns_working: bool
    last_check_time: float
    config: NetworkConfig


# Application state
app_state = {
    "config": NetworkConfig(),
    "interfaces": [],
    "active_interface": None,
    "internet_accessible": False,
    "dns_working": False,
    "last_check_time": None,
    "monitoring_active": False,
    "monitoring_task": None
}


# FastAPI app
app = FastAPI(
    title="Net Agent Service",
    description="Network monitoring and management service",
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


def get_interface_type(name: str) -> str:
    """Determine interface type from name"""
    if name.startswith("wl") or name.startswith("wlan"):
        return "wifi"
    elif name.startswith("ww") or name.startswith("ppp"):
        return "cellular"
    elif name.startswith("eth") or name.startswith("en"):
        return "ethernet"
    else:
        return "unknown"


async def scan_network_interfaces() -> List[NetworkInterface]:
    """Scan available network interfaces"""
    interfaces = []
    
    try:
        # Get network interface information using psutil
        net_if_addrs = psutil.net_if_addrs()
        net_if_stats = psutil.net_if_stats()
        
        for iface_name, addrs in net_if_addrs.items():
            # Skip loopback
            if iface_name == "lo" or iface_name.startswith("lo"):
                continue
            
            # Get interface stats
            stats = net_if_stats.get(iface_name)
            if not stats:
                continue
            
            # Get IP and MAC addresses
            ip_addr = None
            mac_addr = None
            
            for addr in addrs:
                if addr.family == 2:  # AF_INET (IPv4)
                    ip_addr = addr.address
                elif addr.family == 17:  # AF_PACKET (MAC)
                    mac_addr = addr.address
            
            interface = NetworkInterface(
                name=iface_name,
                type=get_interface_type(iface_name),
                status="up" if stats.isup else "down",
                ip_address=ip_addr,
                mac_address=mac_addr,
                signal_strength=None  # Would need platform-specific code
            )
            
            interfaces.append(interface)
            
    except Exception as e:
        logger.error(f"Error scanning network interfaces: {e}")
    
    return interfaces


async def check_internet_connectivity() -> bool:
    """Check if internet is accessible"""
    try:
        # Try to ping a reliable host
        result = subprocess.run(
            ["ping", "-c", "1", "-W", "2", "8.8.8.8"],
            capture_output=True,
            timeout=3
        )
        return result.returncode == 0
    except Exception as e:
        logger.error(f"Internet connectivity check failed: {e}")
        return False


async def check_dns() -> bool:
    """Check if DNS is working"""
    try:
        # Try to resolve a domain
        result = subprocess.run(
            ["nslookup", "google.com"],
            capture_output=True,
            timeout=3
        )
        return result.returncode == 0
    except Exception as e:
        logger.error(f"DNS check failed: {e}")
        return False


async def network_monitor():
    """Main network monitoring loop"""
    logger.info("Network monitoring started")
    app_state["monitoring_active"] = True
    
    while app_state["monitoring_active"]:
        try:
            config = app_state["config"]
            app_state["last_check_time"] = datetime.now().timestamp()
            
            # Scan network interfaces
            interfaces = await scan_network_interfaces()
            app_state["interfaces"] = [iface.dict() for iface in interfaces]
            
            # Determine active interface
            active = None
            for iface in interfaces:
                if iface.status == "up" and iface.ip_address:
                    active = iface.name
                    if config.primary_interface and iface.name == config.primary_interface:
                        break
            
            app_state["active_interface"] = active
            
            # Check internet connectivity
            app_state["internet_accessible"] = await check_internet_connectivity()
            
            # Check DNS
            app_state["dns_working"] = await check_dns()
            
            # Log status
            logger.info(
                f"Network status - Active: {active}, "
                f"Internet: {app_state['internet_accessible']}, "
                f"DNS: {app_state['dns_working']}"
            )
            
            # Wait for next check
            await asyncio.sleep(config.check_interval_seconds)
            
        except asyncio.CancelledError:
            logger.info("Network monitoring cancelled")
            break
        except Exception as e:
            logger.error(f"Network monitoring error: {e}")
            await asyncio.sleep(config.check_interval_seconds)
    
    app_state["monitoring_active"] = False
    logger.info("Network monitoring stopped")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "net-agent",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/status", response_model=NetworkStatus)
async def get_status():
    """Get current network status"""
    interfaces = [NetworkInterface(**iface) for iface in app_state["interfaces"]]
    
    return NetworkStatus(
        interfaces=interfaces,
        active_interface=app_state["active_interface"],
        internet_accessible=app_state["internet_accessible"],
        dns_working=app_state["dns_working"],
        last_check_time=app_state["last_check_time"] or 0,
        config=app_state["config"]
    )


@app.get("/config", response_model=NetworkConfig)
async def get_config():
    """Get current network configuration"""
    return app_state["config"]


@app.post("/config", response_model=NetworkConfig)
async def update_config(config: NetworkConfig):
    """Update network configuration"""
    app_state["config"] = config
    logger.info(f"Network configuration updated: {config.dict()}")
    return config


@app.post("/monitor/start")
async def start_monitoring():
    """Start network monitoring"""
    if app_state["monitoring_active"]:
        return {"status": "already_running"}
    
    # Start monitoring task
    task = asyncio.create_task(network_monitor())
    app_state["monitoring_task"] = task
    
    return {"status": "started"}


@app.post("/monitor/stop")
async def stop_monitoring():
    """Stop network monitoring"""
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
    logger.info("Net agent service starting up")
    # Auto-start monitoring
    await start_monitoring()


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event"""
    logger.info("Net agent service shutting down")
    await stop_monitoring()


def main():
    """Main entry point"""
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8003,
        reload=True,
        log_level="info"
    )


if __name__ == "__main__":
    main()
