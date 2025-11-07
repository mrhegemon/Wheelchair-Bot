# Wheelchair-Bot 🦽

A universal **tele-robotics kit** that turns almost any powered wheelchair into a remotely driven robot using commodity parts, an Android phone and/or Raspberry Pi, and a camera—accessed through a secure web interface. **Lightweight stack (no ROS)**.

## Features

- 🎮 **Web-based joystick control** - Control from any device with a web browser
- 📹 **WebRTC video/audio streaming** - Low-latency real-time video feed
- 🛑 **Safety-first design** - E-stop monitoring and automatic safety checks
- 📡 **Network resilience** - LTE/Wi-Fi status monitoring with automatic fallback
- 🚀 **Lightweight** - FastAPI + WebSockets, no ROS required
- 🔒 **Secure** - Built with security in mind for remote access

## Architecture

The system consists of five microservices:

### Services

1. **teleopd** (port 8000) - Teleoperation daemon
   - WebSocket endpoint for real-time commands
   - REST API for configuration and status
   - Command validation and processing

2. **streamer** (port 8001) - Camera capture and streaming
   - WebRTC video/audio streaming
   - Supports libcamera and GStreamer
   - Configurable resolution and framerate

3. **safety-agent** (port 8002) - Safety monitoring
   - E-stop monitoring and triggering
   - Command timeout detection
   - Automatic safety checks

4. **net-agent** (port 8003) - Network monitoring
   - LTE/Wi-Fi status monitoring
   - DNS health checks
   - Network interface management

5. **web-client** (port 8080) - Web interface
   - Joystick control interface
   - Video stream display
   - System status monitoring

## Quick Start

### Prerequisites

- Python 3.9 or higher
- Linux system (tested on Raspberry Pi OS and Ubuntu)
- Camera device (USB webcam or Raspberry Pi Camera)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/mrhegemon/Wheelchair-Bot.git
cd Wheelchair-Bot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. (Optional) Copy and configure settings:
```bash
cp config/config.example.yaml config/config.yaml
# Edit config/config.yaml as needed
```

### Running the System

Start all services:
```bash
./start.sh
```

Access the web interface at `http://localhost:8080`

Stop all services:
```bash
./stop.sh
```

### Running Individual Services

You can also run services individually for development:

```bash
# Teleopd service
cd services/teleopd
python main.py

# Streamer service
cd services/streamer
python main.py

# Safety agent
cd services/safety_agent
python main.py

# Net agent
cd services/net_agent
python main.py

# Web client
cd web_client
python -m http.server 8080
```

## Usage

### Web Interface

1. Open `http://localhost:8080` in a web browser
2. Wait for the connection status to show "Connected"
3. Use the joystick to control the wheelchair:
   - **Click/touch and drag** the joystick to move
   - **Adjust speed** with the slider
   - **Emergency stop** button for immediate halt
4. Monitor video stream and system status

### Keyboard Controls (Optional)

- **Arrow keys**: Control direction
- **Spacebar**: Emergency stop

### API Endpoints

#### Teleopd (Port 8000)

- `GET /status` - Get service status
- `GET /config` - Get configuration
- `POST /config` - Update configuration
- `POST /estop` - Trigger emergency stop
- `POST /estop/reset` - Reset emergency stop
- `WS /ws/commands` - WebSocket for real-time commands

#### Streamer (Port 8001)

- `GET /status` - Get stream status
- `GET /config` - Get stream configuration
- `POST /config` - Update stream configuration
- `WS /ws/webrtc` - WebSocket for WebRTC signaling

#### Safety Agent (Port 8002)

- `GET /status` - Get safety status
- `GET /config` - Get safety configuration
- `POST /config` - Update safety configuration
- `GET /alerts` - Get recent safety alerts
- `POST /alerts/clear` - Clear all alerts
- `POST /monitor/start` - Start safety monitoring
- `POST /monitor/stop` - Stop safety monitoring

#### Net Agent (Port 8003)

- `GET /status` - Get network status
- `GET /config` - Get network configuration
- `POST /config` - Update network configuration
- `POST /monitor/start` - Start network monitoring
- `POST /monitor/stop` - Stop network monitoring

## Hardware Setup

### Raspberry Pi Setup

1. **Install Raspberry Pi OS** (Lite or Desktop)

2. **Enable camera** (if using Pi Camera):
```bash
sudo raspi-config
# Enable Camera in Interface Options
```

3. **Install system dependencies**:
```bash
sudo apt-get update
sudo apt-get install -y python3-pip libcamera-apps gstreamer1.0-tools
```

4. **Clone and install** as described above

### Arduino/Android Integration

The system can integrate with:
- **Arduino** for motor control (connect via serial/USB)
- **Android phone** as secondary camera or sensor input

### Wheelchair Integration

Connect the system to your wheelchair's control system:

1. **Safety first**: Ensure E-stop functionality is wired correctly
2. **Motor control**: Interface with wheelchair's motor controller
3. **Power**: Use wheelchair's battery with appropriate voltage regulation
4. **Mounting**: Securely mount Raspberry Pi and camera

⚠️ **WARNING**: Always test in a safe environment. Ensure E-stop is accessible and functional.

## Configuration

Edit `config/config.yaml` to customize:

- Service ports and hosts
- Camera device and resolution
- Safety check intervals
- Network preferences
- E-stop behavior

Example:
```yaml
streamer:
  camera:
    device: "/dev/video0"
    resolution: "1280x720"
    framerate: 30
```

## Security Considerations

For production use:

1. **Enable HTTPS** using reverse proxy (nginx/traefik)
2. **Add authentication** to web interface
3. **Configure CORS** properly in services
4. **Use VPN** for remote access (WireGuard recommended)
5. **Firewall rules** to restrict access
6. **Keep system updated** regularly

## Development

### Project Structure

```
Wheelchair-Bot/
├── services/
│   ├── teleopd/          # Teleoperation daemon
│   ├── streamer/         # Video/audio streaming
│   ├── safety_agent/     # Safety monitoring
│   └── net_agent/        # Network monitoring
├── web_client/           # Web interface
│   ├── index.html
│   ├── style.css
│   └── app.js
├── config/               # Configuration files
├── docs/                 # Documentation
├── requirements.txt      # Python dependencies
├── start.sh             # Start all services
└── stop.sh              # Stop all services
```

### Adding Features

The modular architecture makes it easy to extend:

1. **Add new commands**: Extend the Command model in teleopd
2. **Add sensors**: Create new monitoring endpoints
3. **Custom UI**: Modify web_client files
4. **Additional safety**: Extend safety-agent checks

## Troubleshooting

### Camera not working

```bash
# List available cameras
v4l2-ctl --list-devices

# Test camera
libcamera-hello

# Update device in config
# Edit config/config.yaml: streamer.camera.device
```

### Services not starting

```bash
# Check if ports are in use
lsof -i :8000
lsof -i :8001

# Check service logs
journalctl -u wheelchair-bot
```

### WebSocket connection fails

- Ensure firewall allows WebSocket connections
- Check browser console for errors
- Verify service URLs in web_client/app.js

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is open source. Please check LICENSE file for details.

## Safety Disclaimer

⚠️ **IMPORTANT**: This software controls physical hardware. Always:
- Test in safe, controlled environments
- Have manual override capability
- Ensure E-stop is always accessible
- Follow all safety regulations
- Never leave system unattended during operation

The authors assume no liability for any accidents or damages.

## Credits

Built with:
- [FastAPI](https://fastapi.tiangolo.com/)
- [aiortc](https://github.com/aiortc/aiortc)
- [psutil](https://github.com/giampaolo/psutil)

---

**Made with ❤️ for accessibility and robotics**