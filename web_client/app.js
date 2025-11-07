// Wheelchair Robot Controller Web Client
// Handles WebSocket communication, joystick control, and WebRTC streaming

class WheelchairController {
    constructor() {
        // Service endpoints
        this.teleopdUrl = 'ws://localhost:8000/ws/commands';
        this.teleopdRestUrl = 'http://localhost:8000';
        this.streamerUrl = 'ws://localhost:8001/ws/webrtc';
        this.safetyUrl = 'http://localhost:8002';
        this.netAgentUrl = 'http://localhost:8003';

        // WebSocket connection
        this.ws = null;
        this.reconnectInterval = 3000;
        this.reconnectTimer = null;

        // WebRTC
        this.peerConnection = null;
        this.streamWs = null;

        // State
        this.estopActive = false;
        this.currentSpeed = 0.5;
        this.joystickActive = false;
        this.joystickPosition = { x: 0, y: 0 };

        // Initialize
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.connectWebSocket();
        this.startStatusPolling();
    }

    setupEventListeners() {
        // E-stop button
        document.getElementById('estop-btn').addEventListener('click', () => {
            this.triggerEstop();
        });

        // E-stop reset button
        document.getElementById('estop-reset-btn').addEventListener('click', () => {
            this.resetEstop();
        });

        // Speed slider
        const speedSlider = document.getElementById('speed-slider');
        speedSlider.addEventListener('input', (e) => {
            this.currentSpeed = e.target.value / 100;
            document.getElementById('speed-value').textContent = e.target.value + '%';
        });

        // Joystick
        this.setupJoystick();

        // Keyboard controls (optional)
        this.setupKeyboardControls();
    }

    setupJoystick() {
        const joystickArea = document.getElementById('joystick-area');
        const joystick = document.getElementById('joystick');
        const areaRect = joystickArea.getBoundingClientRect();
        const radius = areaRect.width / 2;

        let isDragging = false;

        const moveJoystick = (clientX, clientY) => {
            const rect = joystickArea.getBoundingClientRect();
            const centerX = rect.left + radius;
            const centerY = rect.top + radius;

            let deltaX = clientX - centerX;
            let deltaY = clientY - centerY;

            // Limit to circle
            const distance = Math.sqrt(deltaX * deltaX + deltaY * deltaY);
            const maxDistance = radius - 40;

            if (distance > maxDistance) {
                const angle = Math.atan2(deltaY, deltaX);
                deltaX = Math.cos(angle) * maxDistance;
                deltaY = Math.sin(angle) * maxDistance;
            }

            // Update joystick position
            joystick.style.transform = `translate(calc(-50% + ${deltaX}px), calc(-50% + ${deltaY}px))`;

            // Calculate normalized position (-1 to 1)
            this.joystickPosition.x = deltaX / maxDistance;
            this.joystickPosition.y = -deltaY / maxDistance; // Invert Y for forward/backward

            // Send command
            this.sendJoystickCommand();
        };

        const resetJoystick = () => {
            joystick.style.transform = 'translate(-50%, -50%)';
            this.joystickPosition = { x: 0, y: 0 };
            this.joystickActive = false;
            joystick.classList.remove('active');
            this.sendStopCommand();
        };

        // Mouse events
        joystick.addEventListener('mousedown', (e) => {
            isDragging = true;
            this.joystickActive = true;
            joystick.classList.add('active');
            e.preventDefault();
        });

        document.addEventListener('mousemove', (e) => {
            if (isDragging) {
                moveJoystick(e.clientX, e.clientY);
            }
        });

        document.addEventListener('mouseup', () => {
            if (isDragging) {
                isDragging = false;
                resetJoystick();
            }
        });

        // Touch events
        joystick.addEventListener('touchstart', (e) => {
            isDragging = true;
            this.joystickActive = true;
            joystick.classList.add('active');
            e.preventDefault();
        });

        document.addEventListener('touchmove', (e) => {
            if (isDragging && e.touches.length > 0) {
                moveJoystick(e.touches[0].clientX, e.touches[0].clientY);
            }
        });

        document.addEventListener('touchend', () => {
            if (isDragging) {
                isDragging = false;
                resetJoystick();
            }
        });
    }

    setupKeyboardControls() {
        const keys = {};

        document.addEventListener('keydown', (e) => {
            keys[e.key] = true;

            // E-stop on spacebar
            if (e.key === ' ') {
                e.preventDefault();
                this.triggerEstop();
            }
        });

        document.addEventListener('keyup', (e) => {
            keys[e.key] = false;
        });

        // Optional: Arrow key control
        setInterval(() => {
            if (this.joystickActive) return; // Joystick takes priority

            let x = 0, y = 0;
            if (keys['ArrowUp']) y = 1;
            if (keys['ArrowDown']) y = -1;
            if (keys['ArrowLeft']) x = -1;
            if (keys['ArrowRight']) x = 1;

            if (x !== 0 || y !== 0) {
                this.joystickPosition = { x, y };
                this.sendJoystickCommand();
            }
        }, 100);
    }

    connectWebSocket() {
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
            return;
        }

        console.log('Connecting to teleopd WebSocket...');
        this.ws = new WebSocket(this.teleopdUrl);

        this.ws.onopen = () => {
            console.log('WebSocket connected');
            this.updateConnectionStatus(true);
            if (this.reconnectTimer) {
                clearTimeout(this.reconnectTimer);
                this.reconnectTimer = null;
            }
        };

        this.ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.handleWebSocketMessage(data);
        };

        this.ws.onerror = (error) => {
            console.error('WebSocket error:', error);
        };

        this.ws.onclose = () => {
            console.log('WebSocket disconnected');
            this.updateConnectionStatus(false);
            this.scheduleReconnect();
        };
    }

    scheduleReconnect() {
        if (!this.reconnectTimer) {
            this.reconnectTimer = setTimeout(() => {
                console.log('Attempting to reconnect...');
                this.connectWebSocket();
            }, this.reconnectInterval);
        }
    }

    handleWebSocketMessage(data) {
        console.log('Received:', data);

        switch (data.type) {
            case 'connected':
                console.log('Connected to teleopd');
                if (data.estop_active) {
                    this.estopActive = true;
                    this.updateEstopStatus(true);
                }
                break;

            case 'estop':
                this.estopActive = true;
                this.updateEstopStatus(true);
                break;

            case 'estop_reset':
                this.estopActive = false;
                this.updateEstopStatus(false);
                break;

            case 'ack':
                // Command acknowledged
                break;

            case 'error':
                console.error('Server error:', data.message);
                this.updateCurrentCommand('Error: ' + data.message);
                break;

            case 'command_executed':
                // Another client executed a command
                break;

            case 'config_update':
                console.log('Config updated:', data.config);
                break;
        }
    }

    sendCommand(command) {
        if (!this.ws || this.ws.readyState !== WebSocket.OPEN) {
            console.error('WebSocket not connected');
            return;
        }

        this.ws.send(JSON.stringify(command));
    }

    sendJoystickCommand() {
        const { x, y } = this.joystickPosition;
        
        // Determine direction
        let direction = null;
        let speed = Math.sqrt(x * x + y * y);

        if (speed < 0.1) {
            this.sendStopCommand();
            return;
        }

        // Normalize speed
        speed = Math.min(speed, 1.0) * this.currentSpeed;

        // Determine primary direction
        if (Math.abs(y) > Math.abs(x)) {
            direction = y > 0 ? 'forward' : 'backward';
        } else {
            direction = x > 0 ? 'right' : 'left';
        }

        const command = {
            type: 'move',
            direction: direction,
            speed: speed,
            timestamp: Date.now() / 1000
        };

        this.sendCommand(command);
        this.updateCurrentCommand(`${direction} @ ${(speed * 100).toFixed(0)}%`);
    }

    sendStopCommand() {
        const command = {
            type: 'stop',
            timestamp: Date.now() / 1000
        };

        this.sendCommand(command);
        this.updateCurrentCommand('stop');
    }

    triggerEstop() {
        console.log('Triggering E-STOP');
        const command = {
            type: 'estop',
            timestamp: Date.now() / 1000
        };

        this.sendCommand(command);
        this.estopActive = true;
        this.updateEstopStatus(true);
    }

    async resetEstop() {
        try {
            const response = await fetch(`${this.teleopdRestUrl}/estop/reset`, {
                method: 'POST'
            });

            if (response.ok) {
                this.estopActive = false;
                this.updateEstopStatus(false);
            }
        } catch (error) {
            console.error('Failed to reset e-stop:', error);
        }
    }

    async startStatusPolling() {
        // Poll status from all services
        setInterval(async () => {
            await this.updateServiceStatuses();
        }, 2000);
    }

    async updateServiceStatuses() {
        // Safety status
        try {
            const response = await fetch(`${this.safetyUrl}/status`);
            if (response.ok) {
                const data = await response.json();
                document.getElementById('safety-status').textContent = 
                    data.monitoring_active ? 'Active' : 'Inactive';
            }
        } catch (error) {
            document.getElementById('safety-status').textContent = 'Error';
        }

        // Network status
        try {
            const response = await fetch(`${this.netAgentUrl}/status`);
            if (response.ok) {
                const data = await response.json();
                const status = data.internet_accessible ? 
                    (data.active_interface || 'Connected') : 'No Internet';
                document.getElementById('network-status').textContent = status;
            }
        } catch (error) {
            document.getElementById('network-status').textContent = 'Error';
        }
    }

    updateConnectionStatus(connected) {
        const statusEl = document.getElementById('connection-status');
        if (connected) {
            statusEl.textContent = 'Connected';
            statusEl.className = 'status-badge connected';
        } else {
            statusEl.textContent = 'Disconnected';
            statusEl.className = 'status-badge disconnected';
        }
    }

    updateEstopStatus(active) {
        const statusEl = document.getElementById('estop-status');
        const resetBtn = document.getElementById('estop-reset-btn');

        if (active) {
            statusEl.textContent = 'E-STOP ACTIVE';
            statusEl.className = 'status-badge estop-active';
            resetBtn.disabled = false;
        } else {
            statusEl.textContent = 'Normal';
            statusEl.className = 'status-badge ok';
            resetBtn.disabled = true;
        }
    }

    updateCurrentCommand(command) {
        document.getElementById('current-command').textContent = command;
    }
}

// Initialize controller when page loads
document.addEventListener('DOMContentLoaded', () => {
    window.controller = new WheelchairController();
});
