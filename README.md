# Wheelchair-Bot

A Raspberry Pi-based controller application for wheelchair robots with motor control, keyboard interface, and safety features.

## Features

- **Motor Control**: Differential drive motor control using GPIO pins
- **Keyboard Interface**: Simple keyboard control for testing and operation
- **Safety Features**: Emergency stop and speed limiting
- **Mock Mode**: Test without Raspberry Pi hardware
- **PWM Speed Control**: Smooth speed control using PWM
- **Configurable**: JSON-based configuration for easy customization

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
├── wheelchair_controller/      # Main controller package
│   ├── __init__.py            # Package initialization
│   ├── controller.py          # Main wheelchair controller
│   ├── motor_driver.py        # Motor driver interface
│   └── keyboard_control.py    # Keyboard control interface
├── config/                    # Configuration files
│   └── default_config.json    # Default configuration
├── tests/                     # Test files (future)
├── main.py                    # Main entry point
├── requirements.txt           # Python dependencies
└── README.md                  # This file
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

### Running Unit Tests

Run the test suite:

```bash
python3 -m unittest tests.test_controller -v
```

All tests use mock GPIO, so they can be run on any system without Raspberry Pi hardware.

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

