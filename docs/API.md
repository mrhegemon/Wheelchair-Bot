# API Documentation

## Teleopd Service API

**Base URL**: `http://localhost:8000`

### REST Endpoints

#### Get Status
```http
GET /status
```

**Response**:
```json
{
  "connected_clients": 1,
  "last_command": "move",
  "last_command_time": 1699564320.123,
  "estop_active": false,
  "config": {
    "max_speed": 1.0,
    "enable_estop": true,
    "control_mode": "joystick",
    "timeout_seconds": 5
  }
}
```

#### Get Configuration
```http
GET /config
```

**Response**:
```json
{
  "max_speed": 1.0,
  "enable_estop": true,
  "control_mode": "joystick",
  "timeout_seconds": 5
}
```

#### Update Configuration
```http
POST /config
Content-Type: application/json

{
  "max_speed": 0.8,
  "enable_estop": true,
  "control_mode": "joystick",
  "timeout_seconds": 5
}
```

#### Trigger Emergency Stop
```http
POST /estop
```

**Response**:
```json
{
  "status": "estop_activated"
}
```

#### Reset Emergency Stop
```http
POST /estop/reset
```

**Response**:
```json
{
  "status": "estop_reset"
}
```

### WebSocket Endpoint

```
ws://localhost:8000/ws/commands
```

#### Client -> Server Messages

**Move Command**:
```json
{
  "type": "move",
  "direction": "forward",
  "speed": 0.5,
  "timestamp": 1699564320.123
}
```

Direction: `forward`, `backward`, `left`, `right`

**Stop Command**:
```json
{
  "type": "stop",
  "timestamp": 1699564320.123
}
```

**Emergency Stop**:
```json
{
  "type": "estop",
  "timestamp": 1699564320.123
}
```

#### Server -> Client Messages

**Connection Confirmation**:
```json
{
  "type": "connected",
  "config": { ... },
  "estop_active": false
}
```

**Command Acknowledgment**:
```json
{
  "type": "ack",
  "command": "move",
  "timestamp": 1699564320.456
}
```

**Error**:
```json
{
  "type": "error",
  "message": "E-stop is active. Reset e-stop before sending commands."
}
```

**E-Stop Notification**:
```json
{
  "type": "estop",
  "timestamp": 1699564320.789
}
```

---

## Streamer Service API

**Base URL**: `http://localhost:8001`

### REST Endpoints

#### Get Status
```http
GET /status
```

**Response**:
```json
{
  "active": true,
  "peer_connections": 1,
  "config": {
    "resolution": "640x480",
    "framerate": 30,
    "device": "/dev/video0",
    "audio_enabled": true
  }
}
```

#### Get Configuration
```http
GET /config
```

#### Update Configuration
```http
POST /config
Content-Type: application/json

{
  "resolution": "1280x720",
  "framerate": 30,
  "device": "/dev/video0",
  "audio_enabled": true
}
```

### WebSocket Endpoint

```
ws://localhost:8001/ws/webrtc
```

Used for WebRTC signaling (offer/answer exchange).

---

## Safety Agent API

**Base URL**: `http://localhost:8002`

### REST Endpoints

#### Get Status
```http
GET /status
```

**Response**:
```json
{
  "estop_active": false,
  "last_check_time": 1699564320.123,
  "last_command_time": 1699564319.456,
  "command_timeout": false,
  "monitoring_active": true,
  "config": { ... }
}
```

#### Get Alerts
```http
GET /alerts?limit=20
```

**Response**:
```json
{
  "alerts": [
    {
      "level": "warning",
      "message": "Command timeout detected",
      "timestamp": 1699564320.123
    }
  ],
  "total": 15
}
```

#### Clear Alerts
```http
POST /alerts/clear
```

#### Start Monitoring
```http
POST /monitor/start
```

#### Stop Monitoring
```http
POST /monitor/stop
```

---

## Net Agent API

**Base URL**: `http://localhost:8003`

### REST Endpoints

#### Get Status
```http
GET /status
```

**Response**:
```json
{
  "interfaces": [
    {
      "name": "wlan0",
      "type": "wifi",
      "status": "up",
      "ip_address": "192.168.1.100",
      "mac_address": "aa:bb:cc:dd:ee:ff",
      "signal_strength": null
    }
  ],
  "active_interface": "wlan0",
  "internet_accessible": true,
  "dns_working": true,
  "last_check_time": 1699564320.123,
  "config": { ... }
}
```

#### Get Configuration
```http
GET /config
```

#### Update Configuration
```http
POST /config
Content-Type: application/json

{
  "check_interval_seconds": 5,
  "primary_interface": "wlan0",
  "dns_servers": ["8.8.8.8", "8.8.4.4"],
  "enable_fallback": true
}
```

---

## Example Usage

### Python Client

```python
import asyncio
import websockets
import json

async def control_wheelchair():
    uri = "ws://localhost:8000/ws/commands"
    
    async with websockets.connect(uri) as websocket:
        # Wait for connection message
        response = await websocket.recv()
        print(f"Connected: {response}")
        
        # Send move command
        command = {
            "type": "move",
            "direction": "forward",
            "speed": 0.5,
            "timestamp": time.time()
        }
        await websocket.send(json.dumps(command))
        
        # Wait for acknowledgment
        response = await websocket.recv()
        print(f"Response: {response}")

asyncio.run(control_wheelchair())
```

### JavaScript Client

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/commands');

ws.onopen = () => {
    console.log('Connected');
    
    // Send move command
    ws.send(JSON.stringify({
        type: 'move',
        direction: 'forward',
        speed: 0.5,
        timestamp: Date.now() / 1000
    }));
};

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log('Received:', data);
};
```

### cURL Examples

```bash
# Get teleopd status
curl http://localhost:8000/status

# Trigger emergency stop
curl -X POST http://localhost:8000/estop

# Get network status
curl http://localhost:8003/status

# Update configuration
curl -X POST http://localhost:8000/config \
  -H "Content-Type: application/json" \
  -d '{"max_speed": 0.8, "enable_estop": true, "control_mode": "joystick", "timeout_seconds": 5}'
```
