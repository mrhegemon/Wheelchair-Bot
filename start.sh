#!/bin/bash
# Start all Wheelchair Robot services

echo "Starting Wheelchair Robot services..."

# Start services in background
echo "Starting teleopd service on port 8000..."
cd services/teleopd && python main.py &
TELEOPD_PID=$!

echo "Starting streamer service on port 8001..."
cd ../streamer && python main.py &
STREAMER_PID=$!

echo "Starting safety agent service on port 8002..."
cd ../safety_agent && python main.py &
SAFETY_PID=$!

echo "Starting net agent service on port 8003..."
cd ../net_agent && python main.py &
NETAGENT_PID=$!

echo "Starting web client on port 8080..."
cd ../../web_client && python -m http.server 8080 &
WEBCLIENT_PID=$!

echo ""
echo "All services started!"
echo "================================"
echo "Teleopd:     http://localhost:8000"
echo "Streamer:    http://localhost:8001"
echo "Safety:      http://localhost:8002"
echo "Net Agent:   http://localhost:8003"
echo "Web Client:  http://localhost:8080"
echo "================================"
echo ""
echo "Process IDs:"
echo "  Teleopd: $TELEOPD_PID"
echo "  Streamer: $STREAMER_PID"
echo "  Safety: $SAFETY_PID"
echo "  Net Agent: $NETAGENT_PID"
echo "  Web Client: $WEBCLIENT_PID"
echo ""
echo "To stop all services, run: ./stop.sh"

# Save PIDs to file for stop script
cat > .service_pids << EOF
$TELEOPD_PID
$STREAMER_PID
$SAFETY_PID
$NETAGENT_PID
$WEBCLIENT_PID
EOF

# Wait for all background processes
wait
