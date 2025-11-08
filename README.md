# Wheelchair-Bot

A comprehensive wheelchair robotics platform with motor control, safety features, and a complete emulator for development and testing without hardware.

## Features

- **🦽 Hardware Control**: Differential drive motor control using GPIO pins
- **🎮 Multiple Input Methods**: Keyboard, gamepad, joystick support
- **🛡️ Safety Features**: Emergency stop, deadman switch, and speed limiting
- **🔬 Complete Emulator**: Full physics-based simulation for development without hardware
- **⚡ PWM Speed Control**: Smooth speed control using PWM
- **🧪 Comprehensive Testing**: 95 tests with 74% coverage
- **⚙️ Configurable**: YAML/JSON-based configuration for easy customization

## Quick Start

### Emulator (No Hardware Required)

Run the wheelchair emulator for development and testing:

```bash
# Install dependencies
pip install -e ".[dev]"

# Run emulator
wheelchair-sim --config config/default.yaml

# Run tests
make test
```

See [EMULATOR.md](EMULATOR.md) for complete emulator documentation.

## Hardware Requirements

- Raspberry Pi (any model with GPIO pins)
- Motor driver board (L298N, L293D, or similar)
- Two DC motors for differential drive
- Power supply appropriate for your motors
- (Optional) Motor encoders for feedback

## GPIO Pin Configuration

Default GPIO pin assignments (BCM mode):

| Function | GPIO Pin |
|----------|----------|
| Left Motor Forward | 17 |
| Left Motor Backward | 18 |
| Left Motor Enable (PWM) | 12 |
| Right Motor Forward | 22 |
| Right Motor Backward | 23 |
| Right Motor Enable (PWM) | 13 |

These can be customized in `config/default_config.json`.

## Installation

### On Raspberry Pi

1. Clone the repository:
```bash
git clone https://github.com/mrhegemon/Wheelchair-Bot.git
cd Wheelchair-Bot
```

2. Install dependencies:
```bash
pip3 install -r requirements.txt
```

Note: Uncomment `RPi.GPIO` in `requirements.txt` when installing on actual Raspberry Pi hardware.

### For Development/Testing (without Raspberry Pi)

```bash
git clone https://github.com/mrhegemon/Wheelchair-Bot.git
cd Wheelchair-Bot
```

No additional dependencies required for mock mode.

## Usage

### Basic Usage

Run the controller with mock GPIO (for testing without hardware):

```bash
python3 main.py --mock
```

Run on actual Raspberry Pi hardware:

```bash
sudo python3 main.py
```

Note: `sudo` is required for GPIO access on Raspberry Pi.

### Command Line Options

```bash
python3 main.py [OPTIONS]

Options:
  --mock              Use mock GPIO (for testing without Raspberry Pi)
  --max-speed SPEED   Maximum speed percentage (0-100, default: 80)
  --turn-speed SPEED  Turn speed percentage (0-100, default: 60)
  --verbose, -v       Enable verbose logging
  -h, --help          Show help message
```

### Keyboard Controls

Once running, use these keys to control the wheelchair:

- **W** - Move Forward
- **S** - Move Backward
- **A** - Turn Left
- **D** - Turn Right
- **Space** - Stop
- **Q** - Quit

## Project Structure

```
Wheelchair-Bot/
├── src/wheelchair/             # Emulator and simulation framework
│   ├── interfaces.py           # Abstract interfaces for all subsystems
│   ├── config.py               # Configuration system (YAML/TOML)
│   ├── factory.py              # Factory for creating emulator instances
│   ├── cli.py                  # Command-line interface
│   └── emulator/               # Emulator implementations
│       ├── drive.py            # Differential drive physics
│       ├── controller.py       # Scriptable controller input
│       ├── sensors.py          # IMU and proximity sensors
│       ├── power.py            # Battery simulation
│       ├── safety.py           # Safety monitoring
│       └── loop.py             # Simulation event loop
├── wheelchair_bot/             # Core wheelchair control library
│   ├── wheelchairs/            # Wheelchair models
│   ├── controllers/            # Controller interfaces
│   ├── motors/                 # Motor control
│   └── safety/                 # Safety features
├── wheelchair_controller/      # Legacy controller package
│   ├── controller.py           # Main wheelchair controller
│   ├── motor_driver.py         # Motor driver interface
│   └── keyboard_control.py    # Keyboard control interface
├── tests/                      # Test suite for existing code
├── src/tests/                  # Emulator test suite (76 tests)
├── config/                     # Configuration files
│   ├── default.yaml            # Emulator configuration
│   └── default_config.json     # Hardware configuration
├── scripts/
│   └── run_tests.py            # Consolidated test runner
├── Makefile                    # Build and test targets
├── main.py                     # Main entry point
├── pyproject.toml              # Python project metadata
├── README.md                   # This file
└── EMULATOR.md                 # Emulator documentation
```

## Configuration

Edit `config/default_config.json` to customize:

- GPIO pin assignments
- Speed limits
- Safety features
- Motor parameters

## Safety Features

- **Speed Limiting**: Maximum speed can be configured
- **Emergency Stop**: Immediate halt capability
- **Input Validation**: All speed values are clamped to safe ranges
- **Graceful Shutdown**: Proper cleanup of GPIO resources

## Development

### Running Tests

Run the complete test suite (95 tests):

```bash
# Run all tests with coverage
make test

# Or use the test runner directly
python scripts/run_tests.py

# Run specific test modules
pytest tests/test_controller.py -v
pytest src/tests/test_emulator_drive.py -v
```

### Emulator Development

The emulator enables development without hardware:

```bash
# Run emulator with custom duration
wheelchair-sim --duration 30

# Run emulator at 2x speed
# Edit config/default.yaml: simulation.realtime_factor: 2.0
wheelchair-sim --config config/default.yaml

# See emulator documentation
cat EMULATOR.md
```

### Manual Testing

Test the controller interactively:

```bash
python3 main.py --mock --verbose
```

Or run the demo script:

```bash
python3 demo.py
```

These run the controller in mock mode with verbose logging for testing.

### Adding New Control Methods

The modular design makes it easy to add new control interfaces:

1. Create a new control class in `wheelchair_controller/`
2. Import and initialize in `main.py`
3. Implement your control logic using the `WheelchairController` API

## Troubleshooting

### GPIO Permission Errors

Run with `sudo`:
```bash
sudo python3 main.py
```

### Import Errors

Ensure you're in the correct directory:
```bash
cd /path/to/Wheelchair-Bot
python3 main.py
```

### Motor Not Responding

1. Check GPIO connections
2. Verify power supply to motors
3. Test with `--verbose` flag for detailed logging
4. Verify pin assignments in configuration



# 🦽 Wheelchair Bot WebRTC Controller

A web-based controller interface for remotely operating a wheelchair bot using WebRTC technology.

## Features

- **Real-time Video Streaming**: View live video feed from the bot's camera
- **WebRTC Data Channel**: Low-latency control commands
- **Responsive UI**: Works on desktop and mobile devices
- **Multiple Control Methods**:
  - On-screen directional buttons
  - Keyboard controls (WASD or Arrow keys)
  - Touch controls for mobile devices
- **Speed Control**: Adjustable speed slider (0-100%)
- **Connection Status**: Real-time connection state monitoring

## Quick Start

### Opening the Controller

1. Open `index.html` in a modern web browser (Chrome, Firefox, Edge, or Safari)
2. Enter the WebSocket server URL (default: `ws://localhost:8080`)
3. Click "Connect" to establish connection with the bot

### Controls

#### Keyboard Controls
- **W** or **↑**: Move forward
- **S** or **↓**: Move backward
- **A** or **←**: Turn left
- **D** or **→**: Turn right
- **Space** or **Esc**: Stop

#### On-Screen Controls
- Use the directional buttons for movement
- Click and hold for continuous movement
- Release to stop

#### Speed Control
- Adjust the speed slider to set movement speed (0-100%)

## Architecture

### Components

1. **index.html**: Main HTML structure and UI layout
2. **styles.css**: Styling and responsive design
3. **webrtc.js**: WebRTC connection management and signaling
4. **controller.js**: UI event handling and control logic

### WebRTC Flow

1. **Connection**: Client connects to signaling server via WebSocket
2. **Signaling**: Exchange SDP offers/answers and ICE candidates
3. **Media Stream**: Receive video stream from bot
4. **Data Channel**: Bidirectional control command channel
5. **Commands**: Send movement commands in JSON format

### Command Format

Commands sent through the data channel:

```json
{
  "type": "movement",
  "direction": "forward|backward|left|right|stop",
  "speed": 50,
  "timestamp": 1699999999999
}
```

## Server Requirements

The web controller expects a WebRTC signaling server that:

1. Accepts WebSocket connections
2. Handles WebRTC signaling messages (offer, answer, ICE candidates)
3. Provides video stream from bot's camera
4. Receives control commands via data channel

### Expected Signaling Messages

#### Client → Server
- `offer`: WebRTC offer with SDP
- `answer`: WebRTC answer with SDP
- `ice-candidate`: ICE candidate for connection establishment

#### Server → Client
- `answer`: WebRTC answer to client's offer
- `ice-candidate`: ICE candidates from server

## Browser Compatibility

- Chrome/Edge 80+
- Firefox 75+
- Safari 14+
- Opera 67+

**Note**: WebRTC requires HTTPS for production deployments (except localhost)

## Development

### Local Testing

1. Serve the files using any web server:
   ```bash
   # Python 3
   python -m http.server 8000
   
   # Node.js
   npx http-server
   ```

2. Open browser to `http://localhost:8000`

### STUN Servers

The controller uses Google's public STUN servers by default:
- `stun:stun.l.google.com:19302`
- `stun:stun1.l.google.com:19302`

For production, consider using your own TURN servers for better reliability.

## Security Considerations

- Always use HTTPS in production
- Implement proper authentication on the signaling server
- Validate and sanitize all control commands on the bot side
- Consider implementing command rate limiting
- Use secure WebSocket (WSS) for production deployments

## Customization

### Changing Control Layout

Edit `index.html` to modify the control button layout.

### Styling

Modify `styles.css` to customize colors, fonts, and layout.

### Adding New Commands

1. Add new buttons/controls in `index.html`
2. Add event listeners in `controller.js`
3. Define command format and send via `webrtc.sendCommand()`

## Troubleshooting

### Connection Issues

- Verify the signaling server URL is correct
- Check browser console for error messages
- Ensure WebSocket server is running and accessible
- Check firewall settings

### No Video Stream

- Verify the bot is sending video tracks
- Check browser permissions for media playback
- Look for errors in the browser console

### Control Commands Not Working

- Ensure data channel is open (check connection info panel)
- Verify the bot is processing received commands
- Check browser console for command send errors

