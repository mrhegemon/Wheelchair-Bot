# Hardware Setup Guide

## Required Components

### Minimum Setup

1. **Raspberry Pi 4** (2GB RAM minimum, 4GB recommended)
2. **MicroSD Card** (16GB minimum, 32GB recommended)
3. **USB Webcam** or Raspberry Pi Camera Module
4. **Power Supply** (5V 3A for Raspberry Pi)
5. **Powered Wheelchair** with accessible control interface

### Optional Components

1. **LTE Modem/Dongle** for cellular connectivity
2. **GPS Module** for location tracking
3. **Additional Sensors** (ultrasonic, IMU, etc.)
4. **Arduino/Microcontroller** for motor control interface
5. **Battery Pack** for portable operation

## Raspberry Pi Setup

### 1. Install Operating System

Download and flash Raspberry Pi OS:

```bash
# Use Raspberry Pi Imager or manual flash
sudo dd if=raspios.img of=/dev/sdX bs=4M status=progress
```

### 2. Initial Configuration

```bash
# Update system
sudo apt-get update
sudo apt-get upgrade -y

# Install required system packages
sudo apt-get install -y \
    python3-pip \
    python3-dev \
    git \
    libcamera-apps \
    gstreamer1.0-tools \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-bad \
    gstreamer1.0-plugins-ugly \
    libgstreamer1.0-dev \
    v4l-utils \
    network-manager
```

### 3. Enable Camera

For Raspberry Pi Camera Module:

```bash
sudo raspi-config
# Navigate to: Interface Options -> Camera -> Enable
sudo reboot
```

Verify camera:

```bash
# For Pi Camera
libcamera-hello

# For USB webcam
v4l2-ctl --list-devices
```

### 4. Clone and Install Wheelchair-Bot

```bash
cd ~
git clone https://github.com/mrhegemon/Wheelchair-Bot.git
cd Wheelchair-Bot
pip3 install -r requirements.txt
```

### 5. Configure Auto-Start (Optional)

Create systemd service:

```bash
sudo nano /etc/systemd/system/wheelchair-bot.service
```

Add:

```ini
[Unit]
Description=Wheelchair Bot Service
After=network.target

[Service]
Type=forking
User=pi
WorkingDirectory=/home/pi/Wheelchair-Bot
ExecStart=/home/pi/Wheelchair-Bot/start.sh
ExecStop=/home/pi/Wheelchair-Bot/stop.sh
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable service:

```bash
sudo systemctl enable wheelchair-bot.service
sudo systemctl start wheelchair-bot.service
```

## Camera Configuration

### USB Webcam

List available cameras:

```bash
v4l2-ctl --list-devices
```

Test camera:

```bash
ffplay /dev/video0
```

### Raspberry Pi Camera Module

Test camera:

```bash
libcamera-hello --timeout 5000
libcamera-vid -t 10000 -o test.h264
```

Update configuration:

```yaml
# config/config.yaml
streamer:
  camera:
    device: "/dev/video0"  # or appropriate device
    resolution: "640x480"
    framerate: 30
```

## Network Configuration

### Wi-Fi Setup

```bash
sudo nmcli dev wifi connect "SSID" password "PASSWORD"
```

### LTE/Cellular Setup

For USB LTE modems:

```bash
# Install ModemManager
sudo apt-get install -y modemmanager network-manager

# List modems
mmcli -L

# Connect
nmcli connection add type gsm ifname '*' con-name lte apn "your.apn"
nmcli connection up lte
```

### Static IP (Optional)

```bash
sudo nmcli connection modify "connection-name" \
    ipv4.addresses "192.168.1.100/24" \
    ipv4.gateway "192.168.1.1" \
    ipv4.dns "8.8.8.8" \
    ipv4.method manual
```

## Motor Control Interface

### Option 1: GPIO Direct Control

For simple motor controllers that accept PWM:

```python
import RPi.GPIO as GPIO

# Setup GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)  # Motor 1 direction
GPIO.setup(18, GPIO.OUT)  # Motor 1 PWM
# ... configure other pins
```

### Option 2: Serial/USB Interface

Many wheelchair controllers use serial communication:

```python
import serial

ser = serial.Serial('/dev/ttyUSB0', 9600)
ser.write(b'FORWARD 50\n')
```

### Option 3: Arduino Bridge

Use Arduino as interface to wheelchair controller:

1. Connect Arduino to Raspberry Pi via USB
2. Program Arduino to receive commands and control motors
3. Modify teleopd to send commands via serial

Example Arduino code structure:

```cpp
void setup() {
    Serial.begin(9600);
    // Setup motor control pins
}

void loop() {
    if (Serial.available()) {
        String command = Serial.readStringUntil('\n');
        // Parse and execute command
        controlMotors(command);
    }
}
```

## E-Stop Wiring

⚠️ **CRITICAL SAFETY COMPONENT**

### Hardware E-Stop

Connect physical emergency stop button:

1. **Normally Closed (NC) E-Stop Button**
2. Connect to GPIO pin (e.g., GPIO 27)
3. Use pull-up resistor
4. Wire in series with wheelchair's existing e-stop if possible

```python
import RPi.GPIO as GPIO

ESTOP_PIN = 27
GPIO.setmode(GPIO.BCM)
GPIO.setup(ESTOP_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def check_estop():
    return GPIO.input(ESTOP_PIN) == GPIO.LOW
```

### Software Integration

Modify safety_agent to monitor hardware e-stop:

```python
async def monitor_hardware_estop():
    while True:
        if check_estop():
            await trigger_estop("Hardware E-Stop activated")
        await asyncio.sleep(0.1)  # Check 10 times per second
```

## Power Management

### Power Supply Options

1. **Wall Power**: Standard 5V 3A adapter for testing
2. **Wheelchair Battery**: Use DC-DC converter (e.g., 24V -> 5V)
3. **Separate Battery Pack**: For portable testing

### DC-DC Converter Setup

For wheelchair battery integration:

```
Wheelchair Battery (12V/24V)
    ↓
DC-DC Buck Converter (5V 5A output)
    ↓
Raspberry Pi
```

Recommended converters:
- Mean Well SD-15B-5 (15W)
- DROK LM2596 (adjustable)

## Mounting

### Raspberry Pi Mounting

1. Use vibration-dampening case
2. Ensure adequate ventilation
3. Protect from moisture
4. Easy access to ports

### Camera Mounting

1. Front-facing position
2. Stable mounting (avoid vibration)
3. Protected from weather
4. Adjustable angle

### Cable Management

1. Secure all cables
2. Strain relief on connectors
3. Use cable ties/conduit
4. Keep away from moving parts

## Testing Checklist

Before full deployment:

- [ ] All services start without errors
- [ ] Camera stream is visible
- [ ] Web interface accessible
- [ ] WebSocket commands work
- [ ] E-stop functions correctly
- [ ] Network connectivity stable
- [ ] Safety monitoring active
- [ ] Motor control responds correctly
- [ ] System survives reboot
- [ ] Battery/power adequate

## Troubleshooting

### Camera Issues

```bash
# Check camera permissions
ls -l /dev/video*
sudo usermod -a -G video $USER

# Test with v4l2
v4l2-ctl --list-formats-ext -d /dev/video0
```

### Network Issues

```bash
# Check interfaces
ip addr show

# Test connectivity
ping -c 4 8.8.8.8

# Check DNS
nslookup google.com
```

### Permission Issues

```bash
# Add user to groups
sudo usermod -a -G gpio,i2c,spi,video,dialout $USER

# Reboot for changes to take effect
sudo reboot
```

## Safety Recommendations

1. **Always test in controlled environment**
2. **Keep manual override accessible**
3. **Test e-stop before every use**
4. **Monitor battery levels**
5. **Have emergency contact available**
6. **Follow local regulations**
7. **Use appropriate insurance**
8. **Regular maintenance checks**

## Advanced: Android Integration

### Using Android as Camera

1. Install IP Webcam app on Android
2. Configure streamer to use IP camera stream
3. Update configuration with Android IP

```yaml
streamer:
  camera:
    device: "http://192.168.1.50:8080/video"
    resolution: "1280x720"
    framerate: 30
```

### Android as Secondary Controller

Create Android app using WebSocket client to connect to teleopd service.

---

For additional help, see the main README.md or open an issue on GitHub.
